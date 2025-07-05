 : ╭─ ✕ Error (04:08:26) ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                      │
│  An unexpected error occurred during generation or tool execution:                                                   │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Traceback (most recent call last):
  File "C:\Users\past9\OneDrive\Desktop\project\clia\gui\main.py", line 68, in main
    user_task_raw = Prompt.ask(Text(f"{THEME['user_prompt_icon']} ", style=THEME['user_title']))
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\rich\prompt.py", line 149, in ask
    return _prompt(default=default, stream=stream)
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\rich\prompt.py", line 292, in __call__
    value = self.get_input(self.console, prompt, self.password, stream=stream)
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\rich\prompt.py", line 211, in get_input
    return console.input(prompt, password=password, stream=stream)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\rich\console.py", line 2165, in input
    result = input()
EOFError
❯ : ╭─ i Info (04:08:27) ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                      │
│  Chat interrupted by user. Exiting.                                                                                  │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

C:\Users\past9\OneDrive\Desktop\project\data_ui>