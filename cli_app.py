#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import textwrap
from datetime import datetime
from typing import List, Any, Dict
import asyncio
import traceback

# Attempt to import necessary libraries
try:
    from dotenv import load_dotenv
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.live import Live
    from rich.prompt import Prompt
    from rich.spinner import Spinner
    from rich.text import Text
    from rich.align import Align
    from rich.rule import Rule
    from rich import box
except ImportError:
    print("Error: Required Python packages are not installed.")
    print("Please run the following command to install them:")
    print("pip install google-genai rich python-dotenv anyio")
    sys.exit(1)

# Attempt to import the Google GenAI library
try:
    from google import genai
    from google.genai import types
    from google.genai import errors as genai_errors
except ImportError:
    print("Error: The Google GenAI library is not installed.")
    print("Please run the following command to install it:")
    print("pip install google-genai")
    sys.exit(1)

# Attempt to import MCP libraries
try:
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client, StdioServerParameters
    from mcp.types import Tool as MCPTool
except ImportError:
    print("Error: The MCP library is not installed.")
    print("Please run the following command to install it:")
    print("pip install 'mcp[cli]'")
    sys.exit(1)

# Set stdout encoding to UTF-8 for emoji support
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
load_dotenv()

MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"
MCP_SERVER_SCRIPT = "swe_tools.run_server"
MAX_TOOL_TURNS = 15

# --- UI Configuration ---
USER_NAME = "You"
BOT_NAME = "Gemini"
THEME = {
    "user_prompt_icon": "❯",
    "user_title_icon": "👤",
    "bot_title_icon": "🤖",
    "thinking_title_icon": "🧠",
    "info_title_icon": "ℹ️",
    "error_title_icon": "❗",
    "user_title": "bold #F5A9B8",
    "bot_title": "bold #89CFF0",
    "error_title": "bold #FF5733",
    "info_title": "bold #FFC300",
    "thought_title": "#FFC300",
    "panel_border": "#3A3B3C",
    "accent_border": "#89CFF0",
    "thinking_spinner": "arc",
    "separator_style": "#3A3B3C",
}
console = Console()

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

# --- Application Logic ---
def get_gemini_client():
    """Initializes and returns the Gemini client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print_message("GOOGLE_API_KEY not found in your environment.", role="error")
        sys.exit(1)
    try:
        client = genai.Client(api_key=api_key)
        _ = client.models.list()
        return client
    except genai_errors.APIError as e:
        print_message(f"API Error\n\nDetails: {e}", role="error")
        sys.exit(1)
    except Exception as e:
        print_message(f"Unexpected Error on Client Init\n\nDetails: {e}", role="error")
        sys.exit(1)

def print_message(text: str, role: str = "info"):
    """Prints a styled message panel."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    box_preset = box.ROUNDED
    border_color = THEME["panel_border"]
    title_markup = ""

    if role == "user":
        title_markup = f"[{THEME['user_title']}]{THEME['user_title_icon']} {USER_NAME} [dim]({timestamp})[/]"
        box_preset = box.HEAVY
    elif role == "bot":
        title_markup = f"[{THEME['bot_title']}]{THEME['bot_title_icon']} {BOT_NAME} [dim]({timestamp})[/]"
        border_color = THEME["accent_border"]
    elif role == "error":
        title_markup = f"[{THEME['error_title']}]{THEME['error_title_icon']} Error [dim]({timestamp})[/]"
        border_color = "red"
    else: # info
        title_markup = f"[{THEME['info_title']}]{THEME['info_title_icon']} Info [dim]({timestamp})[/]"

    console.print(Panel(
        Markdown(text, inline_code_lexer="python"),
        title=Text.from_markup(title_markup),
        title_align="left",
        box=box_preset,
        border_style=border_color,
        padding=(1, 2)
    ))

def show_welcome_screen():
    """Displays the initial welcome message."""
    welcome_text = Text(f"""
 ██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗
██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║██║
██║  ███╗█████╗  ██╔████╔██║██║██╔██╗ ██║██║
██║   ██║██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║
╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║██║
 ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝
""", style="bold cyan", justify="center")
    welcome_subtext = Text(f"Welcome! You are chatting with {MODEL_NAME}.", justify="center")
    panel = Panel(
        Text.from_markup(f"{welcome_text}\n\n{welcome_subtext}"),
        title=f"[{THEME['info_title']}]Connection Established[/]",
        border_style=THEME['info_title'],
        box=box.DOUBLE
    )
    console.print(Align.center(panel))

async def main():
    """Main function to run the chat application."""
    client = get_gemini_client()
    
    print_message("🤖 CLI SWE AI Initializing...")
    print_message(f"🧠 Using Model: {MODEL_NAME}")
    print_message(f"🛠️  Looking for tool server: {MCP_SERVER_SCRIPT}")

    server_params = StdioServerParameters(command=sys.executable, args=["-m", MCP_SERVER_SCRIPT], env={**os.environ.copy(), 'PYTHONPATH': os.getcwd()})

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as mcp_session:
                await mcp_session.initialize()
                print_message("✅ MCP Tool Server Connected.")

                mcp_tools_response = await mcp_session.list_tools()
                if not mcp_tools_response or not mcp_tools_response.tools:
                    print_message("❌ ERROR: No tools found on the MCP server.", role="error")
                    return

                gemini_tools = types.Tool(function_declarations=[mcp_tool_to_genai_tool(t) for t in mcp_tools_response.tools])
                generation_config = types.GenerateContentConfig(tools=[gemini_tools])

                show_welcome_screen()
                history = []

                while True:
                    try:
                        user_task = Prompt.ask(Text(f"{THEME['user_prompt_icon']} ", style=THEME['user_title']))
                        if user_task.lower() in ["exit", "quit"]:
                            print_message("Session ended. Goodbye!")
                            break
                        if not user_task.strip():
                            continue

                        print_message(user_task, role="user")
                        history.append(types.Content(role='user', parts=[types.Part.from_text(text=user_task)]))
                        
                        final_answer = ""
                        spinner = Spinner(THEME["thinking_spinner"], text=Text(" Thinking...", style=THEME["thought_title"]))
                        
                        with Live(spinner, console=console, screen=False, auto_refresh=True, vertical_overflow="visible", transient=True) as live:
                            turn_count = 0
                            while turn_count < MAX_TOOL_TURNS:
                                turn_count += 1
                                
                                response = await client.aio.models.generate_content(
                                    model=MODEL_NAME,
                                    contents=history,
                                    config=generation_config
                                )
                                candidate = response.candidates[0]
                                
                                if not candidate.content.parts or not candidate.content.parts[0].function_call:
                                    final_answer = response.text
                                    break
                                
                                history.append(candidate.content)
                                function_call = candidate.content.parts[0].function_call
                                tool_name = function_call.name
                                tool_args = dict(function_call.args)

                                live.stop()
                                tool_message = f"Calling tool `{tool_name}` with arguments: `{tool_args}`"
                                print_message(tool_message, role="info")
                                
                                tool_result = await mcp_session.call_tool(tool_name, tool_args)
                                
                                history.append(types.Part.from_function_response(name=tool_name, response={"result": str(tool_result)}))
                                print_message(f"Tool `{tool_name}` returned a result.", role="info")

                                live.start()
                                live.update(spinner)

                            if turn_count >= MAX_TOOL_TURNS:
                                final_answer = "Task may be incomplete due to reaching the maximum number of tool turns."

                        if final_answer:
                            print_message(final_answer, role="bot")
                            # --- THE FIX: Use the keyword argument `text=` ---
                            history.append(types.Content(role="model", parts=[types.Part.from_text(text=final_answer)]))
                        
                        console.print(Rule(style=THEME["separator_style"]))

                    except KeyboardInterrupt:
                        print_message("\nChat interrupted by user. Exiting.", role="info")
                        break
                    except Exception as e:
                        print_message(f"An error occurred during generation or tool execution: {e}", role="error")
                        traceback.print_exc()
                        continue
    
    except Exception as e:
        print_message(f"❌ An unexpected error occurred during MCP server connection: {e}", role="error")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ A fatal error occurred: {e}")
        traceback.print_exc()