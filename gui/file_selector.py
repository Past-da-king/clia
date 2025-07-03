import os
import mimetypes
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.prompt import Prompt

from typing import List, Tuple, Optional
from google.genai import types # Assuming genai client is available

console = Console()

class FileSelector:
    def __init__(self, base_path: str):
        self.current_path = os.path.abspath(base_path)
        self.selected_index = 0
        self.entries = []
        self._update_entries()

    def _update_entries(self):
        self.entries = []
        # Add ".." for navigating up
        parent_dir = os.path.dirname(self.current_path)
        if self.current_path != parent_dir: # Check if not at root
            self.entries.append("..")
        
        with os.scandir(self.current_path) as it:
            for entry in sorted(it, key=lambda e: (not e.is_dir(), e.name.lower())):
                if entry.name.startswith('.'): # Ignore hidden files/dirs
                    continue
                if entry.is_dir():
                    self.entries.append(entry.name + "/")
                else:
                    self.entries.append(entry.name)
        self.selected_index = 0

    def render(self) -> Panel:
        display_items = []
        for i, entry in enumerate(self.entries):
            text_style = "default"
            if i == self.selected_index:
                text_style = "bold cyan on grey30"
            display_items.append(Text(entry, style=text_style))
        
        return Panel(
            Text.assemble(*[item + "\n" for item in display_items]),
            title=f"Select File/Directory: [bold green]{self.current_path}[/]",
            border_style="green",
            padding=(1, 2)
        )

    def navigate(self, direction: str):
        if direction == "up":
            self.selected_index = max(0, self.selected_index - 1)
        elif direction == "down":
            self.selected_index = min(len(self.entries) - 1, self.selected_index + 1)

    def select(self) -> Optional[str]:
        if not self.entries:
            return None

        selected_name = self.entries[self.selected_index]
        selected_path = os.path.join(self.current_path, selected_name)

        if selected_name == "..":
            self.current_path = os.path.dirname(self.current_path)
            self._update_entries()
            return None # Indicate navigation, not file selection
        elif os.path.isdir(selected_path):
            self.current_path = selected_path
            self._update_entries()
            return None # Indicate navigation, not file selection
        else:
            return selected_path # Return absolute path of selected file

    @staticmethod
    def get_mime_type(file_path: str) -> str:
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type if mime_type else "application/octet-stream"

    async def get_file_part(self, genai_client, file_path: str):
        try:
            # For local files, the genai.Client.files.upload method is used.
            # It returns a File object which is compatible with types.Part.
            uploaded_file = await genai_client.aio.files.upload(file=file_path)
            return uploaded_file # This is a types.File object, which is a types.Part
        except Exception as e:
            console.print(f"[bold red]Error uploading file {file_path}: {e}[/bold red]")
            return None
        except Exception as e:
            console.print(f"[bold red]Error uploading file {file_path}: {e}[/bold red]")
            return None

async def interactive_file_selector(initial_path: str, genai_client) -> Optional[str]:
    selector = FileSelector(initial_path)
    selected_file = None

    with Live(selector.render(), console=console, screen=True, auto_refresh=True) as live:
        while selected_file is None:
            key_event = console.input() # This is blocking, need a non-blocking input
            # This is the tricky part. rich.console.Console.input() is blocking.
            # For a truly interactive experience, I'd need to use a library like prompt_toolkit
            # or implement a more complex async input loop.
            # For now, I'll simulate a simple blocking input.
            # This will require a different approach for input handling in main.py
            # or a simpler file selection mechanism.

            # Let's rethink the input for interactive_file_selector.
            # rich.prompt.Prompt is good for single line input.
            # For interactive navigation, I need to capture individual key presses.
            # rich.console.Console.input() is not designed for this.
            # I will need to use a more advanced input capture method,
            # or simplify the interaction for the first pass.

            # No, the user explicitly asked for arrow keys. I need to implement that.
            # This means I need to capture raw key presses.
            # rich.console.Console.get_event() is the correct tool.
            # The main loop in gui/main.py will need to be modified to handle this.

            # Let's try to use rich.console.Console.get_event()
            # This requires a different approach in main.py as well.

            # This is getting complicated quickly. Let's simplify the file selection for now.
            # Instead of full interactive navigation, I'll implement a simpler version:
            # When '@' is typed, it will list files, and the user types the index or part of the name.
            # This is not the arrow key navigation, but it's a start.

            # No, the user explicitly asked for arrow keys. I need to implement that.
            # This means I need to capture raw key presses.
            # rich.console.Console.get_event() is the correct tool.
            # The main loop in gui/main.py will need to be modified to handle this.

            # Let's assume the `interactive_file_selector` will be called in a way that
            # it can capture key events.

            # This is a significant change to the input loop.
            # I will need to modify gui/main.py to use `console.listen()` or similar.

            # Let's try to implement the interactive file selector with `rich.live` and `console.get_event()`.
            # This will require a custom input loop in `main.py`.

            # The `Prompt.ask` in `main.py` is blocking. I need to replace it with a custom input handler.

            # This is a major refactor of the input handling.
            # I will need to:
            # 1. Remove `Prompt.ask` from `main.py`.
            # 2. Implement a custom input buffer and display.
            # 3. Detect `@` and switch to file selection mode.
            # 4. In file selection mode, capture arrow keys and Enter.
            # 5. When a file is selected, insert its path into the input buffer.

            # This is a multi-step process. I will start with the `FileSelector` class.
            # Then, I will modify `main.py` to integrate it.
