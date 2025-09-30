# -*- coding: utf-8 -*-

import re
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.syntax import Syntax
import json
from typing import List
from gui.config import THEME, USER_NAME, BOT_NAME, MODEL_NAME

console = Console()

def create_message_panel(text: str, role: str = "info", title: str | None = None) -> Panel:
    """Creates and returns a styled message panel."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    box_preset = box.ROUNDED
    border_color = THEME["panel_border"]
    title_markup = ""

    renderable_content = None

    if title:
        title_markup = f"[{THEME['info_title']}]{THEME['info_title_icon']} {title} [dim]({timestamp})[/]"
        if title == "Tool Result":
            try:
                json_data = json.loads(text)
                renderable_content = Syntax(json.dumps(json_data, indent=2), "json", theme="monokai", line_numbers=False)
            except json.JSONDecodeError:
                # Attempt to parse the specific output format of view_directory_structure
                match = re.search(r"text='(.*?)'", text, re.DOTALL)
                if match:
                    file_list_str = match.group(1)
                    # Replace escaped newlines with actual newlines
                    file_list_str = file_list_str.replace('\\n', '\n')
                    # Format as a rich list or just a pre-formatted block
                    renderable_content = Syntax(file_list_str, "text", theme="monokai", line_numbers=False)
                else:
                    renderable_content = Markdown(text, inline_code_lexer="python")
    elif role == "user":
        title_markup = f"[{THEME['user_title']}]{THEME['user_title_icon']} {USER_NAME} [dim]({timestamp})[/]"
        box_preset = box.HEAVY
    elif role == "bot":
        title_markup = f"[{THEME['bot_title']}]{THEME['bot_title_icon']} {BOT_NAME} [dim]({timestamp})[/]"
        border_color = THEME["accent_border"]
    elif role == "error":
        title_markup = f"[{THEME['error_title']}]{THEME['error_title_icon']} Error [dim]({timestamp})[/]"
        border_color = "red"
    elif role == "thoughts":
        title_markup = f"[{THEME['thought_title']}]{THEME['info_title_icon']} Thoughts [dim]({timestamp})[/]"
        border_color = THEME["thought_title"]
        box_preset = box.MINIMAL
    elif role == "tool_call":
        title_markup = f"[{THEME['tool_call_style']}]{THEME['tool_call_icon']} Tool Call [dim]({timestamp})[/]"
        border_color = THEME["tool_call_style"]
        box_preset = box.MINIMAL
    else: # info
        title_markup = f"[{THEME['info_title']}]{THEME['info_title_icon']} Info [dim]({timestamp})[/]"

    if renderable_content is None:
        renderable_content = Markdown(text, inline_code_lexer="python")

    panel = Panel(
        renderable_content,
        title=Text.from_markup(title_markup),
        title_align="left",
        box=box_preset,
        border_style=border_color,
        padding=(1, 2),
        style=f"on {THEME['background_color']}"
    )
    return panel

def show_welcome_screen() -> Panel:
    """Creates the initial welcome message panel."""
    welcome_text = Text("""

██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗
██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║██║
██║  ███╗█████╗  ██╔████╔██║██║██╔██╗ ██║██║
██║   ██║██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║
╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║██║
 ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝

""", style="bold #6495ED", justify="center")
    welcome_subtext = Text(f"Welcome! You are chatting with {MODEL_NAME}.", justify="center", style="#32CD32")
    panel = Panel(
        Text.from_markup(f"{welcome_text}\n\n{welcome_subtext}"),
        title=f"[{THEME['info_title']}]Connection Established[/]",
        border_style=THEME['info_title'],
        box=box.DOUBLE
    )
    return Align.center(panel)

def display_file_suggestions(file_list: str, current_input: str) -> Panel:
    """Displays a formatted panel of file suggestions based on current input."""
    files = file_list.splitlines()
    filtered_files = [f for f in files if current_input.lower() in f.lower()]

    if not filtered_files:
        return Panel(Text("No matching files found.", style="dim"), title="File Suggestions", border_style=THEME["panel_border"], style=f"on {THEME['background_color']}")

    # Limit to top N suggestions for readability
    display_files = filtered_files[:10]

    suggestions_text = Text()
    for f in display_files:
        suggestions_text.append(f, style="#ADD8E6") # Light blue for file names
        suggestions_text.append("\n")

    return Panel(
        suggestions_text,
        title="File Suggestions",
        border_style=THEME["accent_border"],
        box=box.ROUNDED,
        padding=(0, 1),
        style=f"on {THEME['background_color']}"
    )
