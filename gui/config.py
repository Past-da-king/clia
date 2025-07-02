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
