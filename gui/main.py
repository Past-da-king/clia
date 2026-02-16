#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import traceback
from dotenv import load_dotenv
from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.console import Group
from rich.markdown import Markdown
from rich import box
from datetime import datetime
from google.genai import types
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

import json

from gui.config import MCP_SERVER_SCRIPT, THEME
from core.config import MODEL_NAME
from gui.ui import create_message_panel, show_welcome_screen, console, create_permission_panel
from gui.client import get_gemini_client
from core.tool_utils import mcp_tool_to_genai_tool
from core.ai_core import AICore
from gui.file_completer import FileCompleter
from gui.tool_completer import ToolCompleter
from gui.completers import CombinedCompleter

PERMISSIONS_FILE = "permissions.json"

always_allowed_tools = set()

def load_permissions():
    global always_allowed_tools
    if os.path.exists(PERMISSIONS_FILE):
        with open(PERMISSIONS_FILE, "r") as f:
            try:
                permissions = json.load(f)
                always_allowed_tools = set(permissions.get("always_allowed", []))
            except json.JSONDecodeError:
                always_allowed_tools = set()
    else:
        # Create an empty permissions file if it doesn't exist
        with open(PERMISSIONS_FILE, "w") as f:
            json.dump({"always_allowed": []}, f)

def save_permissions():
    with open(PERMISSIONS_FILE, "w") as f:
        json.dump({"always_allowed": list(always_allowed_tools)}, f)

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
from core.config import DEFAULT_PROVIDER, GROQ_MODEL_NAME, MODEL_NAME, SYSTEM_PROMPT
from core.providers import GeminiProvider, GroqProvider
from groq import AsyncGroq

async def onboarding_flow(force=False):
    """Interactive onboarding to choose provider and configure API keys."""
    # Reload env to ensure we have latest saved settings
    load_dotenv()
    
    current_provider = os.environ.get("DEFAULT_PROVIDER")
    current_gemini_model = os.environ.get("GOOGLE_MODEL_NAME", MODEL_NAME)
    current_groq_model = os.environ.get("GROQ_MODEL_NAME", GROQ_MODEL_NAME)
    current_base_url = os.environ.get("GROQ_BASE_URL")
    
    # Check if we have enough to skip
    if not force:
        if current_provider == "gemini" and os.environ.get("GOOGLE_API_KEY"):
            return "gemini", current_gemini_model, None
        if current_provider == "groq" and os.environ.get("GROQ_API_KEY"):
            return "groq", current_groq_model, current_base_url

    console.print(Panel(Text("CLIA Setup & Configuration", style="bold cyan"), box=box.ROUNDED))
    
    # 1. Choose Provider
    console.print("\n[bold cyan]1. Choose Provider[/bold cyan]")
    default_provider_idx = "1" if current_provider == "gemini" else "2"
    console.print(f"[1] Gemini (Google) {'(Current)' if current_provider == 'gemini' else ''}")
    console.print(f"[2] Groq / OpenAI-compatible {'(Current)' if current_provider == 'groq' else ''}")
    
    provider_choice = input(f"Select Option (1/2, default {default_provider_idx}): ").strip()
    if not provider_choice:
        provider_choice = default_provider_idx
    
    provider_name = "gemini" if provider_choice == "1" else "groq"
    
    # Save provider choice
    with open(".env", "a") as f:
        f.write(f"\nDEFAULT_PROVIDER={provider_name}")
    os.environ["DEFAULT_PROVIDER"] = provider_name
    
    # 2. Check/Request API Key
    env_key = "GOOGLE_API_KEY" if provider_name == "gemini" else "GROQ_API_KEY"
    api_key = os.environ.get(env_key)
    
    if not api_key:
        console.print(f"\n[bold yellow]No {env_key} found in environment.[/bold yellow]")
        api_key = input(f"Please enter your {provider_name.capitalize()} API Key: ").strip()
        if api_key:
            with open(".env", "a") as f:
                f.write(f"\n{env_key}={api_key}")
            os.environ[env_key] = api_key
            console.print("[green]API Key saved to .env![/green]")
    
    # 3. Model & Base URL Selection
    default_model = current_gemini_model if provider_name == "gemini" else current_groq_model
    base_url = os.environ.get("GROQ_BASE_URL")
    
    if provider_name == "groq":
        console.print(f"\n[bold cyan]2. Provider Settings[/bold cyan]")
        console.print(f"Current Base URL: [bold white]{base_url or 'Default Groq API'}[/bold white]")
        change_url = input("Change Base URL? (y/N): ").lower().strip()
        if change_url == 'y':
            console.print("Paste your custom endpoint (e.g., https://api.moonshot.cn/v1)")
            custom_base = input("Base URL: ").strip()
            if custom_base:
                base_url = custom_base
                with open(".env", "a") as f:
                    f.write(f"\nGROQ_BASE_URL={base_url}")
                os.environ["GROQ_BASE_URL"] = base_url

    console.print(f"\n[bold cyan]3. Model Selection[/bold cyan]")
    console.print(f"Default/Current model: [bold green]{default_model}[/bold green]")
    custom_model = input(f"Enter model name (or Enter to keep): ").strip()
    model_name = custom_model if custom_model else default_model
    
    # Save model choice
    model_env_var = "GOOGLE_MODEL_NAME" if provider_name == "gemini" else "GROQ_MODEL_NAME"
    with open(".env", "a") as f:
        f.write(f"\n{model_env_var}={model_name}")
    os.environ[model_env_var] = model_name
    
    return provider_name, model_name, base_url

async def main():
    """Main function for the stable Polished Scrolling UI."""
    parser = argparse.ArgumentParser(description="CLI SWE AI Assistant")
    parser.add_argument("--provider", "-p", help="Override provider")
    parser.add_argument("--model", "-m", help="Override model")
    parser.add_argument("--base-url", "-b", help="Override API base URL")
    parser.add_argument("--setup", action="store_true", help="Force interactive setup")
    args = parser.parse_args()

    # Smart onboarding
    provider_name, model_name, base_url = await onboarding_flow(force=args.setup)
    
    # CLI Overrides
    if args.provider: provider_name = args.provider
    if args.model: model_name = args.model
    if args.base_url: base_url = args.base_url

    # Check for keys again in case they were missed
    env_key = "GOOGLE_API_KEY" if provider_name == "gemini" else "GROQ_API_KEY"
    if not os.environ.get(env_key):
        # Trigger onboarding again if key is still missing
        provider_name, model_name, base_url = await onboarding_flow(force=True)

    # Client instances
    gemini_client = None
    groq_client = None

    if provider_name == "gemini":
        gemini_client = await get_gemini_client()
    else:
        groq_client = AsyncGroq(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url=base_url
        )
    
    console.print(show_welcome_screen())
    console.print(create_message_panel("🤖 CLI SWE AI Initializing..."))
    console.print(create_message_panel(f"🧠 Provider: {provider_name.capitalize()} | Model: {model_name}"))
    console.print(create_message_panel(f"🛠️ Looking for tool server: {MCP_SERVER_SCRIPT}"))

    load_permissions()

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

                # Store tool descriptions for permission panel
                tool_descriptions = {t.name: t.description for t in mcp_tools_response.tools}

                if provider_name == "gemini":
                    from core.tool_utils import mcp_tool_to_genai_tool
                    gemini_tools = [mcp_tool_to_genai_tool(t) for t in mcp_tools_response.tools]
                    provider = GeminiProvider(gemini_client, model_name, gemini_tools)
                else:
                    from core.tool_utils import mcp_tool_to_openai_tool
                    groq_tools = [mcp_tool_to_openai_tool(t) for t in mcp_tools_response.tools]
                    provider = GroqProvider(groq_client, model_name, groq_tools)

                ai_core = AICore(provider, mcp_session)
                chat_history = []

                # Define custom styles for prompt_toolkit
                custom_style = Style.from_dict({
                    'completion-menu': 'bg:#1a1a1a #ffffff',
                    'completion-menu.completion': 'bg:#1a1a1a #ffffff',
                    'completion-menu.completion.current': 'bg:#007bff #ffffff',
                    'completion-menu.completion.meta': 'fg:#888888',
                    'completion-menu.completion.meta.current': 'fg:#ffffff bg:#007bff',
                    'bottom-toolbar': 'bg:#333333 #ffffff',
                })

                # Initialize completers
                file_completer = FileCompleter()
                tool_names = [t.name for t in mcp_tools_response.tools]
                tool_completer = ToolCompleter(tool_names=tool_names)
                combined_completer = CombinedCompleter(file_completer, tool_completer)

                # Define a callable for the bottom toolbar
                def get_bottom_toolbar():
                    return HTML(f"<b><style bg=\"#9400D3\" fg=\"#ffffff\">Press Ctrl-C to exit. Type '@' for file completion. Type '#' for tool completion.</style></b>")

                # Setup prompt_toolkit session
                session = PromptSession(
                    completer=combined_completer,
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

                        if user_task_input is None:
                            console.print(create_message_panel("Session ended. Goodbye!", role="info"))
                            break
                        if user_task_input.lower() in ["exit", "quit"]:
                            console.print(create_message_panel("Session ended. Goodbye!"))
                            break
                        if not user_task_input.strip():
                            continue

                        console.print(create_message_panel(user_task_input, role="user"))

                        spinner = Spinner("dots", text=Text("Thinking...", style="green"))
                        thought_panel = Panel(
                            Text(""),
                            box=box.DOUBLE,
                            border_style="green",
                            padding=(1, 2),
                            style=f"on {THEME['background_color']}"
                        )
                        live_group = Group(spinner)
                        
                        live = Live(live_group, console=console, auto_refresh=False, vertical_overflow="visible")
                        live.start()
                        
                        first_thought_received = False
                        
                        try:
                            #render spinner only
                            live.refresh()
                            async for event in ai_core.process_message(chat_history, user_task_input):
                                if event["type"] == "stream":
                                        live.refresh() 
                                elif event["type"] == "stream_text":
                                    # Used by Groq for text streaming
                                    live.refresh()
                                elif event["type"] == "thoughts": 
                                    if not first_thought_received:
                                        live_group.renderables.append(thought_panel)
                                        first_thought_received = True
                                    thought_panel.renderable = Markdown(event["content"], inline_code_lexer="python")
                                elif event["type"] == "tool_call":
                                    live.refresh()
                                    
                                    tool_name = event["tool_name"]
                                    tool_args = event["tool_args"]
                                    tool_description = tool_descriptions.get(tool_name, "No description available.")

                                    tool_allowed = False
                                    if tool_name in always_allowed_tools:
                                        tool_allowed = True
                                        console.print(create_message_panel(f"Tool `{tool_name}` automatically allowed (always allowed).", role="info"))
                                    else:
                                        live.stop()
                                        console.print(create_permission_panel(tool_name, str(tool_args), tool_description))
                                        while True:
                                            permission_choice = await session.prompt_async(Text("Enter your choice (1, 2, or 3): ", style="bold white").plain)
                                            if permission_choice == "1":
                                                tool_allowed = True
                                                console.print(create_message_panel(f"Tool `{tool_name}` allowed for this turn.", role="info"))
                                                break
                                            elif permission_choice == "2":
                                                tool_allowed = True
                                                always_allowed_tools.add(tool_name)
                                                save_permissions()
                                                console.print(create_message_panel(f"Tool `{tool_name}` always allowed from now on.", role="info"))
                                                break
                                            elif permission_choice == "3":
                                                tool_allowed = False
                                                console.print(create_message_panel(f"Tool `{tool_name}` denied.", role="info"))
                                                break
                                            else:
                                                console.print(create_message_panel("Invalid choice. Please enter 1, 2, or 3.", role="error"))
                                        live.start()
                                        live.refresh()
                                    
                                    if tool_allowed:
                                        console.print(create_message_panel(f"Calling tool `{tool_name}` with arguments: `{tool_args}`", role="tool_call"))
                                        tool_result = await ai_core.mcp_session.call_tool(tool_name, tool_args)
                                        
                                        # Standardize tool result handling in history
                                        # Note: History management for tool responses is complex across providers.
                                        # For now, we update the simple history list.
                                        
                                        console.print(create_message_panel(f'''Tool `{tool_name}` returned: 
                                                        ```json
                                                        {str(tool_result)}
                                                        ```''', role="info", title="Tool Result"))
                                    else:
                                        tool_result = {"status": "denied", "message": f"Tool call for `{tool_name}` was denied by the user."}
                                        console.print(create_message_panel(f'''Tool `{tool_name}` returned: 
                                                        ```json
                                                        {str(tool_result)}
                                                        ```''', role="info", title="Tool Result"))
                                        live.refresh()
                                elif event["type"] == "tool_result":
                                    # Handled above, but we could add to history here if needed
                                    pass
                                elif event["type"] == "bot_response":
                                    live.stop()  
                                    console.print(create_message_panel(event["content"], role="bot"))
                                    # Add user and bot messages to history
                                    chat_history.append({"role": "user", "content": user_task_input})
                                    chat_history.append({"role": "assistant", "content": event["content"]})
                                    break
                                elif event["type"] == "error":
                                    live.stop()   
                                    console.print(create_message_panel(event["content"], role="error"))
                                    break
                        finally:
    
                            live.stop()

                    except EOFError:
                        break
                    except KeyboardInterrupt:
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
