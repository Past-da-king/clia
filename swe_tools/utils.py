import os
import fnmatch
from collections import defaultdict
from typing import List, Dict, Tuple

DEFAULT_IGNORE_PATTERNS = [
    ".git", ".gitignore", ".svn", "node_modules", "venv", ".venv",
    "__pycache__", "build", "dist", "*.log", ".tmp", ".DS_Store"
]

def is_ignored(relative_path: str, ignore_patterns: List[str]) -> bool:
    normalized_path = relative_path.replace("\\", "/")
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(normalized_path, pattern) or fnmatch.fnmatch(os.path.basename(normalized_path), pattern):
            return True
    return False

def parse_multiline_commands(text: str) -> Dict[str, List[Tuple[int, str]]]:    # Replace escaped newlines with actual newlines    processed_text = text.replace('\n', '
')    commands = defaultdict(list)    current_file = None        for line in processed_text.strip().split('
'):        stripped_line = line.strip()        if stripped_line.startswith('

):            # Handle one or more '

 characters            path_part = stripped_line.lstrip('

).strip()            current_file = path_part        elif current_file and ':' in line:            try:                line_num_str, content = line.split(':', 1)                line_num = int(line_num_str)                commands[current_file].append((line_num, content))            except ValueError:                continue    return commands

