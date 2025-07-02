# -*- coding: utf-8 -*-

import os
import sys
from google import genai
from google.genai import errors as genai_errors
from gui.ui import print_message

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
    except genai_errors.APIError as e:
        print_message(f"API Error\n\nDetails: {e}", role="error")
        sys.exit(1)
    except Exception as e:
        print_message(f"Unexpected Error on Client Init\n\nDetails: {e}", role="error")
        sys.exit(1)

