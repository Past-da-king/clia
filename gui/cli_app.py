#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import textwrap
from datetime import datetime
from typing import List, Any, Dict
import asyncio
import traceback
from system_prompt import AI_SYSTEM_PROMPT

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

# Attempt to import the Google GenAI library (the NEW SDK)
try:
    from google import genai
    from google.genai import types
    from google.genai import errors as genai_errors
except ImportError:
    print("Error: The NEW 'google-genai' library is not installed.")
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

# Use a supported model for the "thinking" feature
MODEL_NAME = "gemini-2.5-flash"
SYSTEM_PROMPT = AI_SYSTEM_PROMPT
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

# --- Helper Function ---
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
    elif role == "thinking":
        title_markup = f"[{THEME['thought_title']}]{THEME['thinking_title_icon']} Thinking [dim]({timestamp})[/]"
        border_color = THEME["thought_title"]
    elif role == "error":
        title_markup = f"[{THEME['error_title']}]{THEME['error_title_icon']} Error [dim]({timestamp})[/]"
        border_color = "red"
    else: # info
        title_markup = f"[{THEME['info_title']}]{THEME['info_title_icon']} Info [dim]({timestamp})[/]"

    if not text.strip():
        return

    console.print(Panel(
        Markdown(text, inline_code_lexer="python"),
        title=Text.from_markup(title_markup),
        title_align="left",
        box=box_preset,
        border_style=border_color,
        padding=(1, 2)
    ))

def show_welcome_screen():
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
    try:
        client = genai.Client()
    except Exception as e:
        print_message(f"Failed to create Gen AI Client. Is GOOGLE_API_KEY set?\n\nDetails: {e}", role="error")
        sys.exit(1)

    print_message(f"🤖 CLI SWE AI Initializing... Using Model: {MODEL_NAME}")
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

                gemini_tools = [types.Tool(function_declarations=[mcp_tool_to_genai_tool(t) for t in mcp_tools_response.tools])]

                generation_config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=gemini_tools,
                    thinking_config=types.ThinkingConfig(
                        include_thoughts=True,
                        thinking_budget=-1
                    )
                )

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

                        final_response = None
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

                                # FIX: Robustly check if a valid function_call object exists in any part.
                                if not any(hasattr(part, 'function_call') and part.function_call for part in candidate.content.parts):
                                    final_response = response
                                    break

                                history.append(candidate.content)
                                function_call_part = next((p for p in candidate.content.parts if hasattr(p, 'function_call') and p.function_call), None)
                                
                                if not function_call_part:
                                    final_response = response
                                    break

                                function_call = function_call_part.function_call
                                tool_name = function_call.name
                                tool_args = dict(function_call.args)

                                live.stop()
                                print_message(f"Calling tool `{tool_name}` with arguments: `{tool_args}`", role="info")
                                tool_result = await mcp_session.call_tool(tool_name, tool_args)
                                history.append(types.Part.from_function_response(name=tool_name, response={"result": str(tool_result)}))
                                print_message(f"Tool `{tool_name}` returned a result.", role="info")
                                live.start()

                            if not final_response:
                                print_message("Task may be incomplete due to reaching the maximum number of tool turns.", role="bot")

                        if final_response:
                            thoughts_text = ""
                            answer_text = ""
                            for part in final_response.candidates[0].content.parts:
                                if not hasattr(part, 'text') or not part.text:
                                    continue
                                if hasattr(part, 'thought') and part.thought:
                                    thoughts_text += part.text
                                else:
                                    answer_text += part.text

                            if thoughts_text:
                                print_message(thoughts_text, role="thinking")
                            if answer_text:
                                print_message(answer_text, role="bot")
                                history.append(final_response.candidates[0].content)

                        console.print(Rule(style=THEME["separator_style"]))

                    except KeyboardInterrupt:
                        print_message("\nChat interrupted by user. Exiting.", role="info")
                        break
                    except Exception as e:
                        print_message(f"An error occurred: {e}", role="error")
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