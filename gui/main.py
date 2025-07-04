#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import traceback
import re 
from datetime import datetime 
from rich.live import Live
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.text import Text
from rich.rule import Rule
from rich.panel import Panel 
from rich.markdown import Markdown 
from google.genai import types
from google.genai import errors as genai_errors
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from gui.config import MODEL_NAME, SYSTEM_PROMPT, MCP_SERVER_SCRIPT, MAX_TOOL_TURNS, THEME, BOT_NAME
from gui.ui import print_message, show_welcome_screen, console 
from gui.file_selector import FileSelector 
from gui.client import get_gemini_client
from gui.tool_utils import mcp_tool_to_genai_tool
import uvicorn

sys.stdout.reconfigure(encoding='utf-8')

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
                
                generation_config = types.GenerateContentConfig(
                    tools=[gemini_tools],
                    system_instruction=SYSTEM_PROMPT,
                    thinking_config=types.ThinkingConfig(
                        include_thoughts=True
                    )
                )

                show_welcome_screen()
                history = []
                
                while True: 
                    try:
                        user_task_raw = Prompt.ask(Text(f"{THEME['user_prompt_icon']} ", style=THEME['user_title']))
                        
                        if user_task_raw.lower() in ["exit", "quit"]:
                            print_message("Session ended. Goodbye!")
                            break
                        if not user_task_raw.strip():
                            continue

                        user_task_parts = []
                        tagged_files = []
                        current_text_part = ""

                        file_tag_pattern = re.compile(r"@([\w./\-]+)")

                        last_idx = 0
                        for match in file_tag_pattern.finditer(user_task_raw):
                            if match.start() > last_idx:
                                current_text_part += user_task_raw[last_idx:match.start()]
                            
                            if current_text_part:
                                user_task_parts.append(types.Part.from_text(text=current_text_part))
                                current_text_part = ""

                            file_path = match.group(1)
                            if os.path.exists(file_path):
                                tagged_files.append(file_path)
                                print_message(f"File added: {file_path}", role="file_tag")
                            else:
                                print_message(f"File not found: {file_path}", role="error")
                            last_idx = match.end()
                        
                        if last_idx < len(user_task_raw):
                            current_text_part += user_task_raw[last_idx:]
                        
                        if current_text_part:
                            user_task_parts.append(types.Part.from_text(text=current_text_part))

                        if not user_task_parts and not tagged_files:
                            continue

                        print_message(user_task_raw, role="user")
                        
                        content_parts = user_task_parts
                        for file_path in tagged_files:
                            try:
                                # get_file_part returns a types.File object
                                uploaded_file = await FileSelector(os.getcwd()).get_file_part(client, file_path)
                                if uploaded_file:
                                    # --- FIX: Create a proper Part from the uploaded File object ---
                                    file_part = types.Part(file_data=types.FileData(
                                        mime_type=uploaded_file.mime_type,
                                        file_uri=uploaded_file.uri
                                    ))
                                    content_parts.append(file_part)
                            except Exception as e:
                                print_message(f"Error processing file {file_path}: {e}", role="error")

                        history.append(types.Content(role='user', parts=content_parts))
                        
                        final_answer = ""
                        spinner = Spinner(THEME["thinking_spinner"], text=Text(" Thinking...", style=THEME["thought_title"]))
                        
                        turn_count = 0
                        while turn_count < MAX_TOOL_TURNS:
                            turn_count += 1
                            
                            with Live(spinner, console=console, screen=False, auto_refresh=True, vertical_overflow="visible", transient=True) as live:
                                stream = await client.aio.models.generate_content_stream(
                                    model=MODEL_NAME,
                                    contents=history,
                                    config=generation_config
                                )
                                
                                thoughts_md = Markdown("")
                                answer_md = Markdown("")
                                function_call = None
                                response_content_parts = []
                                active_section = None
                                live_panel = None

                                async for chunk in stream:
                                    for part in chunk.candidates[0].content.parts:
                                        if hasattr(part, 'function_call') and part.function_call:
                                            function_call = part.function_call
                                        
                                        if part.text:
                                            if hasattr(part, 'thought') and part.thought:
                                                active_section = 'thoughts'
                                                thoughts_md.markup += part.text
                                            else:
                                                if active_section != 'answer':
                                                    active_section = 'answer'
                                                    timestamp = datetime.now().strftime('%H:%M:%S')
                                                    title_markup = f"[{THEME['bot_title']}]{THEME['bot_title_icon']} {BOT_NAME} [dim]({timestamp})[/]"
                                                    if live_panel is not None:
                                                        live_panel.title = Text.from_markup(title_markup)
                                                        live_panel.border_style = THEME["accent_border"]
                                                        live_panel.renderable = answer_md
                                                    else:
                                                        live_panel = Panel(
                                                            answer_md,
                                                            title=Text.from_markup(title_markup),
                                                            border_style=THEME["accent_border"],
                                                            title_align="left",
                                                            padding=(1, 2)
                                                        )
                                                        live.update(live_panel)
                                                answer_md.markup += part.text
                                    
                                    response_content_parts.extend(chunk.candidates[0].content.parts)

                                    if live_panel is None and thoughts_md.markup:
                                        timestamp = datetime.now().strftime('%H:%M:%S')
                                        title_markup = f"[{THEME['info_title']}]{THEME['info_title_icon']} Thoughts [dim]({timestamp})[/]"
                                        live_panel = Panel(
                                            thoughts_md,
                                            title=Text.from_markup(title_markup),
                                            border_style=THEME["panel_border"],
                                            title_align="left",
                                            padding=(1, 2)
                                        )
                                        live.update(live_panel)

                                    if function_call:
                                        live.stop()
                                        if thoughts_md.markup:
                                            print_message(thoughts_md.markup, role="info", title="Thoughts")
                                        break
                            
                            if function_call:
                                history.append(types.Content(role="model", parts=response_content_parts))
                                tool_name = function_call.name
                                tool_args = dict(function_call.args)

                                tool_message = f"Calling tool `{tool_name}` with arguments: `{tool_args}`"
                                print_message(tool_message, role="tool_code")
                                
                                tool_result = await mcp_session.call_tool(tool_name, tool_args)
                                
                                history.append(types.Part.from_function_response(name=tool_name, response={"result": str(tool_result)}))
                                print_message(f"Tool `{tool_name}` returned a result.", role="tool_code")
                            else:
                                final_answer = answer_md.markup
                                if thoughts_md.markup:
                                    print_message(thoughts_md.markup, role="info", title="Thoughts")
                                break

                        if turn_count >= MAX_TOOL_TURNS:
                            final_answer = "Task may be incomplete due to reaching the maximum number of tool turns."

                        if final_answer:
                            print_message(final_answer, role="bot")
                            history.append(types.Content(role="model", parts=[types.Part.from_text(text=final_answer)]))
                        
                        console.print(Rule(style=THEME["separator_style"]))

                    except KeyboardInterrupt:
                        print_message("\nChat interrupted by user. Exiting.", role="info")
                        break
                    except genai_errors.ClientError as e:
                        print_message(f"An API error occurred: {e}", role="error")
                        traceback.print_exc()
                        continue
                    except Exception as e:
                        print_message(f"An unexpected error occurred during generation or tool execution: {e}", role="error")
                        traceback.print_exc()
                        continue
    
    except Exception as e:
        print_message(f"❌ An unexpected error occurred during MCP server connection: {e}", role="error")
        traceback.print_exc()

def run_clia():
    if "--web" in sys.argv:
        # Remove --web argument before passing to uvicorn
        sys.argv.remove("--web")
        # Run the FastAPI app using uvicorn
        # The app object is in web_ui/app.py
        # We need to ensure the current working directory is in sys.path for uvicorn to find web_ui.app
        sys.path.insert(0, os.getcwd())
        uvicorn.run("web_ui.app:app", host="0.0.0.0", port=8000, reload=True, ws="websockets", app_dir="C:/Users/past9/OneDrive/Desktop/project/clia")
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"❌ A fatal error occurred: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    run_clia()