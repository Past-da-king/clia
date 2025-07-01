import os
from typing import Optional
from swe_tools.__init__ import mcp
from swe_tools.utils import is_ignored, DEFAULT_IGNORE_PATTERNS

@mcp.tool(name="view_directory_tree", description="Generates a tree-like representation of the file and directory structure starting from a specified path. This helps in visualizing the project layout and identifying files. It supports limiting depth and ignoring specific patterns.")
def view_directory_tree(path: str = ".", max_depth: int = 3, ignore: Optional[str] = None) -> str:
    """
    Generates a tree-like representation of the file and directory structure starting from a specified path. This helps in visualizing the project layout and identifying files. It supports limiting depth and ignoring specific patterns.

    Args:
        path: The root directory to start from. Defaults to '.'.
        max_depth: The maximum depth to traverse. Defaults to 3.
        ignore: Optional comma-separated string of glob patterns to ignore.
    """
    user_ignore_patterns = [p.strip() for p in ignore.split(',')] if ignore else []
    all_ignore_patterns = list(set(DEFAULT_IGNORE_PATTERNS + user_ignore_patterns))
    if not os.path.isdir(path): return f"Error: Directory not found: {path}"
    tree_lines = [f"{os.path.basename(os.path.abspath(path))}/"]
    def _build_tree(dir_path, prefix, current_depth):
        if current_depth >= max_depth: return
        try: items = os.listdir(dir_path)
        except OSError: return
        filtered_items = [item for item in sorted(items) if not is_ignored(os.path.relpath(os.path.join(dir_path, item), path), all_ignore_patterns)]
        pointers = ['├── ' for _ in range(len(filtered_items) - 1)] + ['└── ']
        for pointer, item in zip(pointers, filtered_items):
            tree_lines.append(f"{prefix}{pointer}{item}")
            full_item_path = os.path.join(dir_path, item)
            if os.path.isdir(full_item_path):
                extension = '│   ' if pointer == '├── ' else '    '
                _build_tree(full_item_path, prefix + extension, current_depth + 1)
    _build_tree(path, "", 0)
    return "\n".join(tree_lines)
