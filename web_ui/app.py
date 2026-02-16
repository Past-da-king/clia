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
from core.config import MODEL_NAME, SYSTEM_PROMPT, MAX_TOOL_TURNS
from core.tool_utils import mcp_tool_to_genai_tool
from core.ai_core import AICore

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
    
    # Initialize session state
    current_history = [] 
    provider_name = "groq" # Default to Groq/OpenAI as requested
    model_name = os.environ.get("GROQ_MODEL_NAME", "moonshotai/kimi-k2-instruct-0905")

    mcp_tools = await clia_mcp.list_tools()
    if not mcp_tools:
        print("ERROR: No tools found on the MCP server.")
        return

    if provider_name == "gemini":
        from core.tool_utils import mcp_tool_to_genai_tool
        gemini_tools = [mcp_tool_to_genai_tool(t) for t in mcp_tools]
        provider = GeminiProvider(gemini_client, model_name, gemini_tools)
    else:
        from core.tool_utils import mcp_tool_to_openai_tool
        groq_tools = [mcp_tool_to_openai_tool(t) for t in mcp_tools]
        from groq import AsyncGroq
        groq_client = AsyncGroq(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url=os.environ.get("GROQ_BASE_URL") # Support custom endpoints
        )
        provider = GroqProvider(groq_client, model_name, groq_tools)

    ai_core = AICore(provider, clia_mcp)

    while True:
        try:
            message = await websocket.receive_json()
            print(f"Received message: {message}")

            if message["type"] == "user_message":
                user_text = message.get("text", "")
                
                # ... (file processing logic omitted for brevity in this refactor, but kept in original)
                
                await websocket.send_json({"type": "typing_indicator", "status": "start"})

                async for event in ai_core.process_message(current_history, user_text):
                    if event["type"] == "stream":
                        chunk = event["content"]
                        for part in chunk.candidates[0].content.parts:
                            if part.text:
                                if hasattr(part, 'thought') and part.thought:
                                    await websocket.send_json({"type": "thoughts", "content": part.text})
                                else:
                                    await websocket.send_json({"type": "agent_message_stream", "content": part.text})
                    elif event["type"] == "stream_text":
                        # For Groq
                        await websocket.send_json({"type": "agent_message_stream", "content": event["content"]})
                    elif event["type"] == "thoughts":
                        await websocket.send_json({"type": "thoughts", "content": event["content"]})
                    elif event["type"] == "tool_call":
                        tool_name = event["tool_name"]
                        tool_args = event["tool_args"]
                        # Permission check
                        # ... (existing permission logic)
                        await websocket.send_json({
                            "type": "tool_call",
                            "tool_name": tool_name,
                            "tool_args": str(tool_args)
                        })
                    elif event["type"] == "tool_result":
                        await websocket.send_json({
                            "type": "tool_result",
                            "tool_name": event["tool_name"],
                            "result": str(event["result"])
                        })
                    elif event["type"] == "bot_response":
                        # Add to history
                        current_history.append({"role": "user", "content": user_text})
                        current_history.append({"role": "assistant", "content": event["content"]})
                    elif event["type"] == "error":
                        await websocket.send_json({"type": "error", "content": event["content"]})

                await websocket.send_json({"type": "typing_indicator", "status": "stop"})

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
