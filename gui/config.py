# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from .system_prompt import AI_SYSTEM_PROMPT

load_dotenv()

# --- Configuration ---
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
    "tool_call_icon": "🛠️",
    "user_title": "bold #FF69B4",  # Hot Pink
    "bot_title": "bold #6495ED",  # Cornflower Blue
    "error_title": "bold #FF4500", # Orange Red
    "info_title": "bold #32CD32", # Lime Green
    "thought_title": "#FFD700", # Gold
    "tool_call_style": "bold #8A2BE2", # Blue Violet
    "panel_border": "#4F4F4F", # Dim Gray
    "accent_border": "#6495ED", # Cornflower Blue
    "thinking_spinner": "dots", # Changed spinner style
    "separator_style": "#4F4F4F", # Dim Gray
}
