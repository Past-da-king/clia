# cli_swe_ai.py (with Conversational Memory)
import asyncio
import os
import sys
import textwrap
from typing import List, Any, Dict

from dotenv import load_dotenv

from google import genai
from google.genai import types

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import Tool as MCPTool

# --- Configuration ---
MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"
MCP_SERVER_SCRIPT = "cli.py" 
MAX_TOOL_TURNS = 15

# --- Helper Function (No changes needed) ---
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

    if not os.path.exists(MCP_SERVER_SCRIPT):
        print(f"❌ ERROR: Tool server script '{MCP_SERVER_SCRIPT}' not found.")
        sys.exit(1)

    server_params = StdioServerParameters(command=sys.executable, args=[MCP_SERVER_SCRIPT])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_session:
            await mcp_session.initialize()
            print("✅ MCP Tool Server Connected.")

            mcp_tools_response = await mcp_session.list_tools()
            if not mcp_tools_response or not mcp_tools_response.tools:
                print("❌ ERROR: No tools found on the MCP server.")
                return

            # Define the generation configuration, including the system prompt
            generation_config = types.GenerateContentConfig(
                tools=[types.Tool(function_declarations=[mcp_tool_to_genai_tool(t) for t in mcp_tools_response.tools])],
                system_instruction="""
You are an expert, autonomous software engineering AI. Your sole purpose is to complete user-given tasks by interacting with a local file system and command line using a specific set of tools. You MUST operate under the following principles and directives.

## Core Philosophy: Trust, but Verify

1.  **Maintain Conversational Context:** You MUST remember the entire conversation history, including the user's previous requests and your own previous actions and responses. Use this context to understand follow-up requests.
2.  **The File System is the Ground Truth:** The user's file system is the ultimate source of truth. While you remember our conversation (e.g., that you *tried* to edit a file), you MUST NOT assume a file operation succeeded or that a file's content is what you expect it to be. You MUST use your tools to read and verify the state of files before and after you act.
3.  **Be Methodical and Cautious:** Break down every complex task into a sequence of small, verifiable steps. Your operational loop for any given task is always: **Plan -> Act -> Observe -> Repeat**.

## Tool Usage Mandates: Your Constitution

You MUST adhere to these rules for tool selection. Misusing a tool will lead to failure.

#### 1. `directory_tree_viewer`
-   **Purpose:** Your "high-level sight." Use this to quickly understand the project's folder and file structure.
-   **Mandatory Use Cases:** As the **very first step** in a new or unfamiliar project to get a "map" of the codebase.

#### 2. `codebase_snapshot_generator`
-   **Purpose:** Your "detailed sight." Use this to read the complete, line-numbered contents of an entire directory.
-   **Mandatory Use Cases:** After getting the layout, use this tool to read the actual code to formulate a detailed implementation plan.

#### 3. `codebase_restorer`
-   **Purpose:** For bulk-writing operations. It overwrites completely.
-   **Mandatory Use Cases:** 1. Creating entirely new files. 2. Completely replacing the content of an existing file.
-   **PROHIBITED USE CASES:** **You MUST NOT use this tool for small edits, insertions, or deletions.**

#### 4. `line_editor`
-   **Purpose:** Your surgical scalpel for modifying **existing** files.
-   **Mandatory Use Cases:** Adding, deleting, or changing specific lines in a file. This is your primary modification tool.

#### 5. `file_fetcher`
-   **Purpose:** Your "focused sight" for reading a **single** file.
-   **Mandatory Use Cases:** To verify the result of a `line_editor` or `codebase_restorer` operation on a single file before proceeding.

#### 6. `file_deleter`
-   **Purpose:** To remove files.
-   **Mandatory Use Cases:** Deleting temporary or obsolete source files as part of a refactoring task.

#### 7. `cli_commander`
-   **Purpose:** Your interface to the shell for **ANY** action that is not direct file reading or writing.
-   **Mandatory Use Cases:** **Validation via tests (`pytest`)**, running the application (`python main.py`), installing dependencies (`pip install`), using version control (`git status`). This is your primary way to verify the correctness of your code.

## Final Directive
Always think step-by-step. Use the conversational history to inform your plan. Announce your plan, execute a single tool, analyze the result, and then announce your next plan. Your goal is to be a transparent and reliable engineer.
                """,
                thinking_config=types.ThinkingConfig(include_thoughts=True)
            )

            print("\n" + "="*50)
            print("🤖 CLI SWE AI is ready. Type your task, or 'exit' to quit.")
            print("="*50 + "\n")

            # --- THE FIX: Initialize history OUTSIDE the loop ---
            history = []

            while True:
                user_task = input("➡️  You: ")
                if user_task.lower() in ["exit", "quit"]:
                    print("👋 Goodbye!")
                    break
                if not user_task.strip():
                    continue

                # --- THE FIX: APPEND the new user message to the existing history ---
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

                    for part in candidate.content.parts:
                        if part.thought:
                            print(f"🤔 AI's Thoughts:\n{textwrap.indent(part.text, '    ')}")

                    if not candidate.content.parts or not candidate.content.parts[0].function_call:
                        break # The model has a final text answer
                    
                    # The model wants to use a tool, append its request to history
                    history.append(candidate.content)
                    
                    function_call = candidate.content.parts[0].function_call
                    tool_name = function_call.name
                    tool_args = dict(function_call.args)

                    print(f"⚙️  AI wants to run: {tool_name}({', '.join(f'{k}={v!r}' for k, v in tool_args.items())})")
                    tool_result = await mcp_session.call_tool(tool_name, tool_args)
                    
                    history.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={"result": str(tool_result)}
                        )
                    )
                    print(f"    - Result: {str(tool_result)[:200]}...\n")
                    if turn_count < MAX_TOOL_TURNS:
                        print("💡 Thinking...")
                
                final_response_text = response.text
                print("\n✅ AI Response:\n" + "="*15)
                for line in textwrap.wrap(final_response_text, width=80):
                    print(line)
                print("="*15 + "\n")

                # --- THE FIX: Append the model's final response to history ---
                history.append(candidate.content)
                
                if turn_count >= MAX_TOOL_TURNS:
                    print("⚠️  Warning: Maximum tool turns reached. Task may be incomplete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")