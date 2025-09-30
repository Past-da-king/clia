                                                                                                                                                          │
│  An error occurred: 'NoneType' object is not iterable Traceback (most recent call last): File                                                             │
│  "C:\Users\past9\OneDrive\Desktop\project\clia\gui\main.py", line 105, in main async for event in ai_core.process_message(gemini_history,                 │
│  user_task_input): ...<12 lines>... console.print(create_message_panel(event["content"], role="error")) File                                              │
│  "C:\Users\past9\OneDrive\Desktop\project\clia\core\ai_core.py", line 49, in process_message for part in chunk.candidates[0].content.parts:               │
│  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ TypeError: 'NoneType' object is not iterable                 ![![alt text](image-2.png)](image-1.png)