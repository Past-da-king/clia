from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import sys
import os
from datetime import datetime
import re
import traceback
import uuid
import json

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui.client import get_gemini_client
from gui.config import MODEL_NAME, SYSTEM_PROMPT, MAX_TOOL_TURNS
from gui.tool_utils import mcp_tool_to_genai_tool

from swe_tools.__init__ import mcp as clia_mcp # Import the FastMCP instance

from google.genai import types
from google.genai import errors as genai_errors

app = FastAPI()

# Global state for Gemini client
gemini_client = None
session_histories = {} # Stores chat history for each WebSocket connection

async def initialize_gemini_client():
    global gemini_client
    if gemini_client:
        return # Already initialized

    try:
        gemini_client = get_gemini_client()
        print("Gemini client initialized successfully.")
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        traceback.print_exc()
        # Handle error, perhaps send a message to the client

@app.on_event("startup")
async def startup_event():
    await initialize_gemini_client()
    # Mount the MCP server as an ASGI application
    app.mount("/mcp_tools", clia_mcp.streamable_http_app(), name="mcp_tools")

    # Get tools from the mounted MCP server
    mcp_tools_response = await clia_mcp.list_tools()
    if not mcp_tools_response:
        print("ERROR: No tools found on the MCP server.")
        return

    gemini_tools = types.Tool(function_declarations=[mcp_tool_to_genai_tool(t) for t in mcp_tools_response])
    app.state.generation_config = types.GenerateContentConfig(
        tools=[gemini_tools],
        system_instruction=SYSTEM_PROMPT,
        thinking_config=types.ThinkingConfig(
            include_thoughts=True
        )
    )
    print("AI components initialized successfully.")

@app.get("/", response_class=HTMLResponse)
async def home():
    with open(os.path.join(os.path.dirname(__file__), "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected.")
    
    # Initialize chat history for this session
    current_history = [] 

    # Send initial welcome message
    

    while True:
        try:
            message = await websocket.receive_json()
            print(f"Received message: {message}")

            if message["type"] == "user_message":
                user_text = message.get("text", "")
                file_data_list = message.get("files", []) # List of {filename, content_base64, mime_type}

                content_parts = []
                if user_text:
                    content_parts.append(types.Part.from_text(text=user_text))

                # Process attached files
                for file_data in file_data_list:
                    # In a real scenario, you'd upload these files to Gemini's file API
                    # For now, we'll simulate or use a placeholder
                    # This part needs careful implementation as Gemini's file API is async
                    # and requires file_uri, not direct content.
                    # For this prototype, we'll just add a text part indicating file presence
                    await websocket.send_json({
                        "type": "info_message",
                        "content": f"Received file: {file_data['filename']} ({file_data['mime_type']}). File processing for Gemini API is a complex topic and will be simplified for this prototype."
                    })
                    content_parts.append(types.Part.from_text(text=f"User attached file: {file_data['filename']}"))


                if not content_parts:
                    continue

                current_history.append(types.Content(role='user', parts=content_parts))
                
                await websocket.send_json({"type": "typing_indicator", "status": "start"})

                final_answer_parts = []
                turn_count = 0
                
                while turn_count < MAX_TOOL_TURNS:
                    turn_count += 1
                    
                    stream = await gemini_client.aio.models.generate_content_stream(
                        model=MODEL_NAME,
                        contents=current_history,
                        config=app.state.generation_config # Use the stored generation_config
                    )
                    
                    function_call = None
                    response_content_parts = []

                    async for chunk in stream:
                        for part in chunk.candidates[0].content.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                function_call = part.function_call
                            
                            if part.text:
                                if hasattr(part, 'thought') and part.thought:
                                    await websocket.send_json({"type": "thoughts", "content": part.text})
                                else:
                                    await websocket.send_json({"type": "agent_message_stream", "content": part.text})
                                    final_answer_parts.append(part) # Accumulate parts for final answer
                        
                        response_content_parts.extend(chunk.candidates[0].content.parts)

                    if function_call:
                        current_history.append(types.Content(role="model", parts=response_content_parts))
                        tool_name = function_call.name
                        tool_args = dict(function_call.args)

                        # Check for permissions
                        permissions = {}
                        permissions_file = "permissions.json"
                        if os.path.exists(permissions_file):
                            with open(permissions_file, "r") as f:
                                try:
                                    permissions = json.load(f)
                                except json.JSONDecodeError:
                                    permissions = {}

                        always_allowed_tools = permissions.get("always_allowed", [])

                        if tool_name not in always_allowed_tools:
                            await websocket.send_json({
                                "type": "permission_request",
                                "tool_name": tool_name,
                                "tool_args": str(tool_args)
                            })

                            try:
                                permission_response = await asyncio.wait_for(websocket.receive_json(), timeout=300) # 5 minute timeout
                                if permission_response.get("type") == "permission_response":
                                    if permission_response.get("allow") == "always":
                                        always_allowed_tools.append(tool_name)
                                        with open(permissions_file, "w") as f:
                                            json.dump({"always_allowed": always_allowed_tools}, f)
                                    elif not permission_response.get("allow"): # Denied
                                        await websocket.send_json({"type": "info_message", "content": f"Tool '{tool_name}' was not executed."})
                                        continue
                                else:
                                    await websocket.send_json({"type": "error", "content": "Invalid response to permission request."})
                                    continue
                            except asyncio.TimeoutError:
                                await websocket.send_json({"type": "error", "content": "Permission request timed out."})
                                continue

                        await websocket.send_json({
                            "type": "tool_call",
                            "tool_name": tool_name,
                            "tool_args": str(tool_args)
                        })
                        
                        tool_result = await clia_mcp.call_tool(tool_name, tool_args)

                        # --- FIX: Default handling for all other tools ---
                        # Extract relevant information from the tool_result object
                        result_summary = {}
                        if hasattr(tool_result, 'stdout') and tool_result.stdout:
                            result_summary['stdout'] = tool_result.stdout
                        if hasattr(tool_result, 'stderr') and tool_result.stderr:
                            result_summary['stderr'] = tool_result.stderr
                        if hasattr(tool_result, 'error') and tool_result.error:
                            result_summary['error'] = str(tool_result.error)
                        if hasattr(tool_result, 'structured') and tool_result.structured:
                            result_summary['structured_output'] = tool_result.structured

                        # If no specific output is found, use a concise string representation
                        if not result_summary:
                            tool_output_str = "Tool executed successfully with no direct output."
                        else:
                            # Convert the summary dict to a clean string
                            tool_output_str = json.dumps(result_summary, indent=2)
                        
                        current_history.append(types.Part.from_function_response(name=tool_name, response={"result": tool_output_str}))
                        await websocket.send_json({
                            "type": "tool_result",
                            "tool_name": tool_name,
                            "result": tool_output_str
                        })
                    else:
                        break # No function call, so AI has finished its response

                await websocket.send_json({"type": "typing_indicator", "status": "stop"})

                if turn_count >= MAX_TOOL_TURNS:
                    final_answer_parts.append(types.Part.from_text(text="Task may be incomplete due to reaching the maximum number of tool turns."))

                current_history.append(types.Content(role="model", parts=final_answer_parts))

            elif message["type"] == "ping":
                await websocket.send_json({"type": "pong"})

        except WebSocketDisconnect:
            print("WebSocket disconnected.")
            break
        except genai_errors.ResourceExhausted as e:
            retry_match = re.search(r"retryDelay': '(\d+)s'", str(e))
            if retry_match:
                wait_time = int(retry_match.group(1))
                await websocket.send_json({"type": "info_message", "content": f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying."})
                await asyncio.sleep(wait_time)
            else:
                await websocket.send_json({"type": "info_message", "content": "Rate limit exceeded. Waiting for 60 seconds before retrying."})
                await asyncio.sleep(60)
            continue
        except genai_errors.ClientError as e:
            await websocket.send_json({"type": "error", "content": f"An API error occurred: {e}"})
            print(f"API Error: {e}")
            break
        except Exception as e:
            await websocket.send_json({"type": "error", "content": f"An unexpected error occurred: {e}"})
            print(f"Unexpected Error: {e}")
            break

# Serve static files (like script.js)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, ws="websockets")
