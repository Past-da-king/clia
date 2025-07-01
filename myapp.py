#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gemini Rich CLI Chatbot - v4.0 "Enhanced UI" Edition
======================================================
A major visual overhaul of the scrolling UI, focusing on polish,
detail, and a more immersive user experience.

Features:
- An immersive, stylized welcome screen.
- A simple, intuitive, scrolling chat interface.
- Timestamped messages for a professional chat log feel.
- Conversation separators for ultimate readability.
- Enhanced aesthetics with icons, a new spinner, and a refined color theme.
- A dynamic "Thinking" panel that appears only during generation.
- The live generation block is transient, erased after completion for a clean look.
"""

import os
import sys
from datetime import datetime

# Attempt to import necessary libraries
try:
    from dotenv import load_dotenv
    from rich.console import Console, Group
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
    print("pip install google-genai rich python-dotenv")
    sys.exit(1)

# Attempt to import the Google GenAI library
try:
    from google import genai
    from google.genai import types
    from google.genai import errors
except ImportError:
    print("Error: The Google GenAI library is not installed.")
    print("Please run the following command to install it:")
    print("pip install google-genai")
    sys.exit(1)

# --- Configuration ---
load_dotenv()

MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"
SYSTEM_PROMPT_STRING = """You are Gemini, a friendly and powerful AI assistant running in a stylized terminal application. Your responses should be formatted with Markdown for clarity and style. Be helpful and concise."""

SAFETY_SETTINGS = [
    types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold='BLOCK_ONLY_HIGH'),
    types.SafetySetting(category='HARM_CATEGORY_HARASSMENT', threshold='BLOCK_ONLY_HIGH'),
    types.SafetySetting(category='HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold='BLOCK_ONLY_HIGH'),
    types.SafetySetting(category='HARM_CATEGORY_DANGEROUS_CONTENT', threshold='BLOCK_ONLY_HIGH'),
]

# --- UI Configuration ---
USER_NAME = "User"
BOT_NAME = "Gemini"

THEME = {
    "user_prompt_icon": "❯",
    "user_title_icon": "👤",
    "bot_title_icon": "🤖",
    "thinking_title_icon": "🧠",
    "info_title_icon": "ℹ️",
    "error_title_icon": "❗",
    "user_title": "bold #F5A9B8",  # Light Pink
    "bot_title": "bold #89CFF0",   # Baby Blue
    "error_title": "bold #FF5733", # Orange-Red
    "info_title": "bold #FFC300",  # Vivid Yellow
    "thought_title": "#FFC300",   # Vivid Yellow
    "panel_border": "#3A3B3C",    # Dark Gray
    "accent_border": "#89CFF0",  # Baby Blue
    "thinking_spinner": "arc",
    "separator_style": "#3A3B3C",
}

console = Console()

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
    except errors.APIError as e:
        print_message(f"API Error\n\nDetails: {e}", role="error")
        sys.exit(1)
    except Exception as e:
        print_message(f"Unexpected Error\n\nDetails: {e}", role="error")
        sys.exit(1)

def print_message(text: str, role: str = "info"):
    """Prints a styled message panel with a timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    box_preset = box.ROUNDED
    border_color = THEME["panel_border"]

    if role == "user":
        title = f"[{THEME['user_title']}]{THEME['user_title_icon']} {USER_NAME} [dim]({timestamp})[/][/]"
        box_preset = box.HEAVY
        border_color = THEME["panel_border"]
    elif role == "bot":
        title = f"[{THEME['bot_title']}]{THEME['bot_title_icon']} {BOT_NAME} [dim]({timestamp})[/][/]"
        box_preset = box.ROUNDED
        border_color = THEME["accent_border"]
    elif role == "error":
        title = f"[{THEME['error_title']}]{THEME['error_title_icon']} Error [dim]({timestamp})[/][/]"
        border_color = "red"
    else: # info
        title = f"[{THEME['info_title']}]{THEME['info_title_icon']} Info [dim]({timestamp})[/][/]"
        border_color = "yellow"

    console.print(Panel(
        Markdown(text, inline_code_lexer="python"),
        title=Text.from_markup(title),
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
╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║███████╗
 ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
""", style="bold cyan", justify="center")
    welcome_subtext = Text(f"Welcome to the Gemini CLI. You are chatting with {MODEL_NAME}.", justify="center")
    panel = Panel(
        Text.from_markup(f"{welcome_text}\n\n{welcome_subtext}"),
        title=f"[{THEME['info_title']}]Connection Established[/]",
        border_style=THEME['info_title'],
        box=box.DOUBLE
    )
    console.print(Align.center(panel, vertical="middle"))

def main():
    """Main function to run the chat application."""
    client = get_gemini_client()
    try:
        chat = client.chats.create(model=MODEL_NAME)
    except Exception as e:
        print_message(f"Failed to initialize chat session: {e}", role="error")
        sys.exit(1)

    show_welcome_screen()

    while True:
        try:
            prompt_text = Text(f"{THEME['user_prompt_icon']} ", style=THEME['user_title'])
            user_input = Prompt.ask(prompt_text)

            if user_input.lower() in ["quit", "exit"]:
                print_message("Session ended. Goodbye!")
                break
            
            print_message(user_input, role="user")
            
            final_answer = ""
            with Live(console=console, screen=False, auto_refresh=True, vertical_overflow="visible", transient=True) as live:
                try:
                    config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT_STRING,
                        safety_settings=SAFETY_SETTINGS,
                        thinking_config=types.ThinkingConfig(
                            include_thoughts=True,
                            thinking_budget=-1
                        )
                    )
                    response_stream = chat.send_message_stream(user_input, config=config)
                    
                    thoughts_text = ""
                    answer_text = ""
                    
                    for chunk in response_stream:
                        for part in chunk.candidates[0].content.parts:
                            if not part.text: continue
                            if part.thought:
                                thoughts_text += part.text
                            else:
                                answer_text += part.text
                        
                        spinner = Spinner(THEME["thinking_spinner"], text=" Thinking...")
                        
                        thinking_panel = Panel(
                            Markdown(thoughts_text),
                            title=Text.from_markup(f"{THEME['thinking_title_icon']} [{THEME['thought_title']}]Thinking...[/]"),
                            border_style=THEME["thought_title"]
                        )
                        
                        answer_panel = Panel(
                            Markdown(answer_text + "▌"),
                            title=f"[{THEME['bot_title']}]{THEME['bot_title_icon']} {BOT_NAME} is Replying...[/]",
                            border_style=THEME["accent_border"]
                        )
                        
                        # CORRECTED: Use a Group to combine the spinner and the panels
                        # This avoids the 'copy' error on the Spinner object.
                        display_group = Group(
                            spinner,
                            thinking_panel if thoughts_text else "",
                            answer_panel
                        )
                        live.update(display_group)
                    
                    final_answer = answer_text

                except Exception as e:
                    print_message(f"An error occurred during generation: {e}", role="error")
                    break
            
            if final_answer:
                print_message(final_answer, role="bot")
                console.print(Rule(style=THEME["separator_style"]))

        except KeyboardInterrupt:
            console.print("\n")
            print_message("Chat interrupted by user. Goodbye!")
            break
        except Exception as e:
            print_message(f"An unexpected error occurred: {e}", role="error")
            break

if __name__ == "__main__":
    main() 