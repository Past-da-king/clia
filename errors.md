  hello                                                                    ┃
┃                                                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
╭─ ℹ️ Info (23:47:14) ────────────────────────────────────────────────────────╮
│                                                                           │
│  Thoughts:                                                                │
│                                                                           │
╰───────────────────────────────────────────────────────────────────────────╯
╭─ ❗ Error (23:47:14) ─────────────────────────────────────────────────────╮
│                                                                           │
│  An error occurred during generation or tool execution: print_message()   │
│  got an unexpected keyword argument 'end'                                 │
│                                                                           │
╰───────────────────────────────────────────────────────────────────────────╯
Traceback (most recent call last):
  File "C:\Users\past9\OneDrive\Desktop\project\clia\gui\main.py", line 97, in main
    print_message(part.text, role="info", end="")
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: print_message() got an unexpected keyword argument 'end'