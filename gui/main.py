#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import traceback
from rich.live import Live
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.text import Text
from rich.rule import Rule
from google.genai import types
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from gui.config import MODEL_NAME, SYSTEM_PROMPT, MCP_SERVER_SCRIPT, MAX_TOOL_TURNS, THEME
from gui.ui import print_message, show_welcome_screen, console
from gui.client import get_gemini_client
from gui.tool_utils import mcp_tool_to_genai_tool

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
                                
                                stream = await client.aio.models.generate_content_stream(
                                    model=MODEL_NAME,
                                    contents=history,
                                    config=generation_config
                                )
                                
                                thoughts = ""
                                answer = ""
                                function_call = None
                                response_content_parts = []

                                async for chunk in stream:
                                    for part in chunk.candidates[0].content.parts:
                                        if hasattr(part, 'function_call') and part.function_call:
                                            function_call = part.function_call
                                        
                                        if part.text:
                                            if hasattr(part, 'thought') and part.thought:
                                                if not thoughts:
                                                    print_message("Thoughts:", role="info")
                                                print_message(part.text, role="info", end="")
                                                thoughts += part.text
                                            else:
                                                if not answer:
                                                    print_message("Answer:", role="bot")
                                                print_message(part.text, role="bot", end="")
                                                answer += part.text
                                    
                                    response_content_parts.extend(chunk.candidates[0].content.parts)

                                    if function_call:
                                        break
                                if function_call:
                                    history.append(types.Content(role="model", parts=response_content_parts))
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
                                else:
                                    final_answer = answer
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
