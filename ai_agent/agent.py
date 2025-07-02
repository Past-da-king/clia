# ai_agent/agent.py (Stable Version with Conversational History - Thinking feature removed to restore functionality)
import asyncio
import os
import sys
import textwrap
from typing import List, Any, Dict
import traceback

# Set stdout encoding to UTF-8 for emoji support
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv

from google import genai
from google.genai import types

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.types import Tool as MCPTool

# --- Configuration ---
MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"
MCP_SERVER_SCRIPT = "swe_tools.run_server" 
MAX_TOOL_TURNS = 15

# --- Helper Function (This is correct and does not need changes) ---
def mcp_tool_to_genai_tool(mcp_tool: MCPTool) -> types.FunctionDeclaration:
    gemini_properties: Dict[str, Any] = {}
    required_params: List[str] = []
    if mcp_tool.inputSchema:
        schema = mcp_tool.inputSchema
        if 'properties' in schema and isinstance(schema['properties'], dict):
            for param_name, param_details in schema['properties'].items():
                param_type = param_details.get('type', 'STRING').upper()
                param_description = param_details.get('description', f'Parameter {param_name}')
                gemini_properties[param_name] = types.Schema(type=param_type, description=param_description)
        if 'required' in schema and isinstance(schema['required'], list):
            required_params = schema['required']
    return types.FunctionDeclaration(
        name=mcp_tool.name,
        description=mcp_tool.description,
        parameters=types.Schema(type='OBJECT', properties=gemini_properties, required=required_params)
    )

# --- Main AI Orchestration Logic ---
async def main():
    load_dotenv()
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("❌ ERROR: GOOGLE_API_KEY not found.")
            sys.exit(1)
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"❌ ERROR: Failed to create Google GenAI client: {e}")
        sys.exit(1)

    print("🤖 CLI SWE AI Initializing...")
    print(f"🧠 Using Model: {MODEL_NAME}")
    print(f"🛠️  Looking for tool server: {MCP_SERVER_SCRIPT}")

    server_params = StdioServerParameters(command=sys.executable, args=["-m", MCP_SERVER_SCRIPT], env={**os.environ.copy(), 'PYTHONPATH': os.getcwd()})

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_session:
            await mcp_session.initialize()
            print("✅ MCP Tool Server Connected.")

            mcp_tools_response = await mcp_session.list_tools()
            if not mcp_tools_response or not mcp_tools_response.tools:
                print("❌ ERROR: No tools found on the MCP server.")
                return

            gemini_tools = types.Tool(function_declarations=[mcp_tool_to_genai_tool(t) for t in mcp_tools_response.tools])

            # --- THE FIX: Reverted to a simple, clean generation config ---
            # This configuration trusts the model to use the tools based on their descriptions,
            # which was the behavior that worked correctly before.
            generation_config = types.GenerateContentConfig(
                tools=[gemini_tools]
            )

            print("\nAvailable Tools:")
            for tool in gemini_tools.function_declarations:
                print(f"  - {tool.name}: {tool.description[:70]}...")

            print("\n" + "="*50)
            print("🤖 CLI SWE AI is ready. Type your task, or 'exit' to quit.")
            print("="*50 + "\n")

            history = []

            while True:
                user_task = input("➡️  You: ")
                if user_task.lower() in ["exit", "quit"]: break
                if not user_task.strip(): continue

                history.append(types.Content(role='user', parts=[types.Part.from_text(text=user_task)]))
                
                print("\n💡 Thinking...")
                turn_count = 0

                while turn_count < MAX_TOOL_TURNS:
                    turn_count += 1
                    
                    response = await client.aio.models.generate_content(
                        model=MODEL_NAME,
                        contents=history,
                        config=generation_config
                    )
                    candidate = response.candidates[0]
                    
                    # If there's no function call, it's the final answer. Break the loop.
                    if not candidate.content.parts or not candidate.content.parts[0].function_call:
                        break
                    
                    # Otherwise, execute the function call
                    history.append(candidate.content)
                    function_call = candidate.content.parts[0].function_call
                    tool_name = function_call.name
                    tool_args = dict(function_call.args)

                    print(f"⚙️  AI wants to run: {tool_name}({', '.join(f'{k}={v!r}' for k, v in tool_args.items())})")
                    tool_result = await mcp_session.call_tool(tool_name, tool_args)
                    
                    history.append(types.Part.from_function_response(name=tool_name, response={"result": str(tool_result)}))
                    print(f"    - Result: {str(tool_result)[:200]}...\n")

                    if turn_count < MAX_TOOL_TURNS:
                        print("💡 Thinking...")
                
                final_response_text = response.text
                print("\n✅ AI Response:\n" + "="*15)
                for line in textwrap.wrap(final_response_text, width=80):
                    print(line)
                print("="*15 + "\n")
                
                if response.candidates:
                    history.append(response.candidates[0].content)

                if turn_count >= MAX_TOOL_TURNS:
                    print("⚠️  Warning: Maximum tool turns reached. Task may be incomplete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        traceback.print_exc()