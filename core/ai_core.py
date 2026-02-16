# -*- coding: utf-8 -*-

import asyncio
import json
from typing import List, Any, Dict, AsyncGenerator

from google.genai import types
from google.genai.client import Client

from core.config import MODEL_NAME, SYSTEM_PROMPT, MAX_TOOL_TURNS
from mcp import ClientSession

from core.providers import BaseProvider

class AICore:
    def __init__(self, provider: BaseProvider, mcp_session: ClientSession):
        self.provider = provider
        self.mcp_session = mcp_session

    async def process_message(self, history: List[Any], user_input: str) -> AsyncGenerator[Dict[str, Any], None]:
        # Provider handles history formatting internally or we pass it as is
        # For Gemini, we append types.Content to history in the provider/caller
        # For simplicity, we'll assume history is managed by the caller in the provider's expected format
        
        turn_count = 0
        while turn_count < MAX_TOOL_TURNS:
            turn_count += 1

            bot_response_text = ""
            function_calls = []
            
            async for event in self.provider.generate_content_stream(history, user_input):
                if event["type"] == "gemini_chunk":
                    chunk = event["data"]
                    if chunk.candidates and chunk.candidates[0].content:
                        for part in chunk.candidates[0].content.parts:
                            if part.function_call:
                                function_calls.append(part.function_call)
                            if part.text:
                                if part.thought:
                                    yield {"type": "thoughts", "content": part.text}
                                else:
                                    bot_response_text += part.text
                    yield {"type": "stream", "content": chunk}
                
                elif event["type"] == "groq_chunk":
                    chunk = event["data"]
                    if chunk.choices and chunk.choices[0].delta:
                        delta = chunk.choices[0].delta
                        if delta.tool_calls:
                            # Aggregate tool calls
                            for tc in delta.tool_calls:
                                # Groq streams tool calls in chunks
                                function_calls.append(tc.function)
                        if delta.content:
                            bot_response_text += delta.content
                            yield {"type": "stream_text", "content": delta.content}
                        if hasattr(delta, 'reasoning') and delta.reasoning:
                            yield {"type": "thoughts", "content": delta.reasoning}

            # Handle tool execution (common logic)
            if function_calls:
                # Group and call tools
                for fc in function_calls:
                    # FC format depends on provider
                    # Gemini: fc.name, fc.args
                    # Groq: fc.name, fc.arguments (string)
                    tool_name = getattr(fc, 'name', None)
                    tool_args = getattr(fc, 'args', None) or json.loads(getattr(fc, 'arguments', '{}'))

                    yield {"type": "tool_call", "tool_name": tool_name, "tool_args": tool_args}
                    
                    tool_result = await self.mcp_session.call_tool(tool_name, tool_args)
                    
                    # Update history - this needs to be provider-specific
                    # For now, we'll yield the need for a response update
                    yield {"type": "tool_result", "tool_name": tool_name, "result": tool_result}
                
                continue
            else:
                if bot_response_text:
                    yield {"type": "bot_response", "content": bot_response_text}
                break
        
        if turn_count >= MAX_TOOL_TURNS:
            yield {"type": "error", "content": "Task may be incomplete due to reaching the maximum number of tool turns."}
        
        if turn_count >= MAX_TOOL_TURNS:
            yield {"type": "error", "content": "Task may be incomplete due to reaching the maximum number of tool turns."}
