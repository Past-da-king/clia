import os
from dotenv import load_dotenv
from core.system_prompt import AI_SYSTEM_PROMPT

load_dotenv()

# --- Configuration ---
MODEL_NAME = os.environ.get("GOOGLE_MODEL_NAME", "gemini-flash-latest")
GROQ_MODEL_NAME = os.environ.get("GROQ_MODEL_NAME", "moonshotai/kimi-k2-instruct-0905")
SYSTEM_PROMPT = AI_SYSTEM_PROMPT
MAX_TOOL_TURNS = 9
DEFAULT_PROVIDER = os.environ.get("DEFAULT_PROVIDER", "groq")
GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL")
