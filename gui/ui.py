# -*- coding: utf-8 -*-

from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from gui.config import THEME, USER_NAME, BOT_NAME, MODEL_NAME

console = Console()

def print_message(text: str, role: str = "info", title: str | None = None, end: str = "\n"):
    """Prints a styled message panel."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    box_preset = box.ROUNDED
    border_color = THEME["panel_border"]
    title_markup = ""

    if title:
        title_markup = f"[{THEME['info_title']}]{THEME['info_title_icon']} {title} [dim]({timestamp})[/]"
    elif role == "user":
        title_markup = f"[{THEME['user_title']}]{THEME['user_title_icon']} {USER_NAME} [dim]({timestamp})[/]"
        box_preset = box.HEAVY
    elif role == "bot":
        title_markup = f"[{THEME['bot_title']}]{THEME['bot_title_icon']} {BOT_NAME} [dim]({timestamp})[/]"
        border_color = THEME["accent_border"]
    elif role == "error":
        title_markup = f"[{THEME['error_title']}]{THEME['error_title_icon']} Error [dim]({timestamp})[/]"
        border_color = "red"
    elif role == "tool_code":
        title_markup = f"[{THEME['tool_call_style']}]{THEME['tool_call_icon']} Tool Call [dim]({timestamp})[/]"
        border_color = THEME["tool_call_style"]
    elif role == "file_tag":
        title_markup = f"[{THEME['info_title']}]{THEME['file_tag_icon']} File Tag [dim]({timestamp})[/]"
        border_color = THEME["panel_border"]
    else: # info
        title_markup = f"[{THEME['info_title']}]{THEME['info_title_icon']} Info [dim]({timestamp})[/]"

    console.print(Panel(
        Markdown(text, inline_code_lexer="python"),
        title=Text.from_markup(title_markup),
        title_align="left",
        box=box_preset,
        border_style=border_color,
        padding=(1, 2)
    ), end=end)

def show_welcome_screen():
    """Displays the initial welcome message."""
    welcome_text = Text("""

██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗
██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║██║
██║  ███╗█████╗  ██╔████╔██║██║██╔██╗ ██║██║
██║   ██║██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║
╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║██║
 ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝

""", style="bold #6495ED", justify="center") # Changed color to Cornflower Blue
    welcome_subtext = Text(f"Welcome! You are chatting with {MODEL_NAME}.", justify="center", style="#32CD32") # Changed color to Lime Green
    panel = Panel(
        Text.from_markup(f"{welcome_text}\n\n{welcome_subtext}"),
        title=f"[{THEME['info_title']}]Connection Established[/]",
        border_style=THEME['info_title'],
        box=box.DOUBLE
    )
    console.print(Align.center(panel))