# -*- coding: utf-8 -*-

import asyncio
from typing import List, Any, Dict, AsyncGenerator, Protocol
from google.genai import types as gemini_types
from google.genai.client import Client as GeminiClient
from groq import AsyncGroq
import json
from core.config import SYSTEM_PROMPT

class BaseProvider(Protocol):
    async def generate_content_stream(self, history: List[Any], system_instruction: str) -> AsyncGenerator[Dict[str, Any], None]:
        ...

class GeminiProvider:
    def __init__(self, client: GeminiClient, model_name: str, gemini_tools: List[gemini_types.Tool]):
        self.client = client
        self.model_name = model_name
        self.gemini_tools = gemini_tools

    async def generate_content_stream(self, history: List[Any], system_instruction: str) -> AsyncGenerator[Dict[str, Any], None]:
        config = gemini_types.GenerateContentConfig(
            tools=self.gemini_tools,
            system_instruction=system_instruction,
            thinking_config=gemini_types.ThinkingConfig(include_thoughts=True)
        )
        
        stream = await self.client.aio.models.generate_content_stream(
            model=self.model_name,
            contents=history,
            config=config
        )

        async for chunk in stream:
            yield {"type": "gemini_chunk", "data": chunk}

class GroqProvider:
    def __init__(self, client: AsyncGroq, model_name: str, tools: List[Dict[str, Any]]):
        self.client = client
        self.model_name = model_name
        self.tools = tools

    async def generate_content_stream(self, history: List[Any], user_input: str) -> AsyncGenerator[Dict[str, Any], None]:
        # History is a list of {"role": "...", "content": "..."}
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_input})

        # Groq stream
        stream = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=self.tools,
            stream=True,
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=1,
        )

        async for chunk in stream:
            yield {"type": "groq_chunk", "data": chunk}

class GeminiProvider:
    def __init__(self, client: GeminiClient, model_name: str, gemini_tools: List[gemini_types.Tool]):
        self.client = client
        self.model_name = model_name
        self.gemini_tools = gemini_tools

    async def generate_content_stream(self, history: List[Any], user_input: str) -> AsyncGenerator[Dict[str, Any], None]:
        # Convert simple history to Gemini Content if necessary
        gemini_history = []
        for m in history:
            role = 'model' if m['role'] == 'assistant' else m['role']
            gemini_history.append(gemini_types.Content(role=role, parts=[gemini_types.Part.from_text(text=m['content'])]))
        
        gemini_history.append(gemini_types.Content(role='user', parts=[gemini_types.Part.from_text(text=user_input)]))

        config = gemini_types.GenerateContentConfig(
            tools=self.gemini_tools,
            system_instruction=SYSTEM_PROMPT,
            thinking_config=gemini_types.ThinkingConfig(include_thoughts=True)
        )
        
        stream = await self.client.aio.models.generate_content_stream(
            model=self.model_name,
            contents=gemini_history,
            config=config
        )

        async for chunk in stream:
            yield {"type": "gemini_chunk", "data": chunk}
