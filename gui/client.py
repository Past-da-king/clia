# -*- coding: utf-8 -*-

import os
import sys
from google import genai
from google.genai import errors as genai_errors
from gui.ui import create_message_panel, console

def get_gemini_client():
    """Initializes and returns the Gemini client, handling errors."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print(create_message_panel("GOOGLE_API_KEY not found in your environment. Please set it in a .env file.", role="error"))
        sys.exit(1)
    
    try:
        # Use the Client constructor which is compatible with the user's environment
        client = genai.Client(api_key=api_key)
        # Test the connection by listing models
        _ = client.models.list()
        return client
    except genai_errors.APIError as e:
        console.print(create_message_panel(f"API Error during client initialization. Check your API key and permissions.\nDetails: {e}", role="error"))
        sys.exit(1)
    except Exception as e:
        console.print(create_message_panel(f"An unexpected error occurred during client initialization.\nDetails: {e}", role="error"))
        sys.exit(1)