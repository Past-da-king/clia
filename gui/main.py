#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import traceback
from rich.text import Text
from google.genai import types
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

from gui.config import MCP_SERVER_SCRIPT, THEME
from core.config import MODEL_NAME
from gui.ui import create_message_panel, show_welcome_screen, console
from gui.client import get_gemini_client
from core.tool_utils import mcp_tool_to_genai_tool
from core.ai_core import AICore
from gui.file_completer import FileCompleter

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def main():
    """Main function for the stable Polished Scrolling UI."""
    client = await get_gemini_client()
    gemini_history = []

    console.print(show_welcome_screen())
    console.print(create_message_panel("🤖 CLI SWE AI Initializing..."))
    console.print(create_message_panel(f"🧠 Using Model: {MODEL_NAME}"))
    console.print(create_message_panel(f"🛠️ Looking for tool server: {MCP_SERVER_SCRIPT}"))

    server_params = StdioServerParameters(command=sys.executable, args=["-m", MCP_SERVER_SCRIPT], env={**os.environ.copy(), 'PYTHONPATH': os.getcwd()})

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as mcp_session:
                await mcp_session.initialize()
                console.print(create_message_panel("✅ MCP Tool Server Connected."))

                mcp_tools_response = await mcp_session.list_tools()
                if not mcp_tools_response or not mcp_tools_response.tools:
                    console.print(create_message_panel("❌ ERROR: No tools found on the MCP server.", role="error"))
                    return

                gemini_tools = types.Tool(function_declarations=[mcp_tool_to_genai_tool(t) for t in mcp_tools_response.tools])
              
                ai_core = AICore(client, mcp_session, gemini_tools)

                # Define custom styles for prompt_toolkit
                custom_style = Style.from_dict({
                    'completion-menu': 'bg:#1a1a1a #ffffff',
                    'completion-menu.completion': 'bg:#1a1a1a #ffffff',
                    'completion-menu.completion.current': 'bg:#007bff #ffffff',
                    'completion-menu.completion.meta': 'fg:#888888',
                    'completion-menu.completion.meta.current': 'fg:#ffffff bg:#007bff',
                    'bottom-toolbar': 'bg:#333333 #ffffff',
                })

                # Define a callable for the bottom toolbar
                def get_bottom_toolbar():
                    return HTML(f"<b><style bg=\"#333333\" fg=\"#ffffff\">Press Ctrl-C to exit. Type '@' for file completion.</style></b>")

                # Setup prompt_toolkit session
                session = PromptSession(
                    completer=FileCompleter(),
                    auto_suggest=AutoSuggestFromHistory(),
                    bottom_toolbar=get_bottom_toolbar,
                    style=custom_style
                )

                # Define key bindings
                kb = KeyBindings()

                @kb.add(Keys.ControlC)
                def _(event):
                    """Exit when Ctrl-C is pressed."""
                    event.app.exit()

                while True:
                    try:
                        user_task_input = await session.prompt_async(Text(f"{THEME['user_prompt_icon']} ", style=THEME['user_title']).plain, key_bindings=kb)

                        # Handle None case for user_task_input (Ctrl+D or exit via keybinding)
                        if user_task_input is None:
                            console.print(create_message_panel("Session ended. Goodbye!", role="info"))
                            break

                        if user_task_input.lower() in ["exit", "quit"]:
                            console.print(create_message_panel("Session ended. Goodbye!"))
                            break
                        if not user_task_input.strip():
                            continue

                        console.print(create_message_panel(user_task_input, role="user"))
                        
                        with console.status("[bold green]Thinking...[/bold green]") as status:
                            async for event in ai_core.process_message(gemini_history, user_task_input):
                                if event["type"] == "thoughts":
                                    console.print(create_message_panel(event["content"], role="thoughts"))
                                elif event["type"] == "tool_call":
                                    console.print(create_message_panel(f"Calling tool `{event['tool_name']}` with arguments: `{event['tool_args']}`", role="tool_call"))
                                elif event["type"] == "tool_result":
                                    console.print(create_message_panel(f"""Tool `{event['tool_name']}` returned: 
```json
{str(event['result'])}
```""", role="info", title="Tool Result"))
                                elif event["type"] == "bot_response":
                                    console.print(create_message_panel(event["content"], role="bot"))
                                elif event["type"] == "error":
                                    console.print(create_message_panel(event["content"], role="error"))


                    except EOFError:
                        # User pressed Ctrl-D
                        break
                    except KeyboardInterrupt:
                        # User pressed Ctrl-C, handled by key binding
                        console.print(create_message_panel("\nChat interrupted by user. Exiting.", role="info"))
                        break
                    except Exception as e:
                        error_msg = f"An error occurred: {e}\n{traceback.format_exc()}"
                        console.print(create_message_panel(error_msg, role="error"))
                        continue
    
    except Exception as e:
        console.print(create_message_panel(f"❌ An unexpected error occurred during MCP server connection: {e}\n{traceback.format_exc()}", role="error"))

def run_clia():
    """Entry point for the console script."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]CLI terminated.[/bold red]")
    except Exception as e:
        console.print(f"❌ A fatal error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    run_clia()
