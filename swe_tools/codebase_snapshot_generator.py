import os
from typing import Optional
from swe_tools.__init__ import mcp
from swe_tools.utils import is_ignored, DEFAULT_IGNORE_PATTERNS

@mcp.tool(name="generate_codebase_snapshot", description="Creates a detailed string snapshot of a specified directory, including file paths and line-numbered content. This is useful for capturing the current state of a codebase or specific files for analysis or restoration. Ignored files and directories can be excluded.")
def generate_codebase_snapshot(path: str = ".", ignore: Optional[str] = None) -> str:
    """
    Creates a detailed string snapshot of a specified directory, including file paths and line-numbered content. This is useful for capturing the current state of a codebase or specific files for analysis or restoration. Ignored files and directories can be excluded.

    Args:
        path: The root directory to snapshot (e.g., '.'). Defaults to current directory.
        ignore: Optional comma-separated string of glob patterns to ignore.
    """
    user_ignore_patterns = [p.strip() for p in ignore.split(',')] if ignore else []
    all_ignore_patterns = list(set(DEFAULT_IGNORE_PATTERNS + user_ignore_patterns))
    abs_root = os.path.abspath(path)
    if not os.path.isdir(abs_root): return f"Error: Source directory not found: {abs_root}"
    snapshot_parts = []
    for dirpath, dirnames, filenames in os.walk(abs_root, topdown=True):
        dirs_to_remove = {d for d in dirnames if is_ignored(os.path.relpath(os.path.join(dirpath, d), abs_root), all_ignore_patterns)}
        dirnames[:] = [d for d in dirnames if d not in dirs_to_remove]
        for filename in sorted(filenames):
            filepath = os.path.join(dirpath, filename)
            relative_filepath = os.path.relpath(filepath, abs_root).replace("\\", "/")
            if is_ignored(relative_filepath, all_ignore_patterns): continue
            snapshot_parts.append(f"$${relative_filepath}\n```\n")
            try:
                with open(filepath, "r", encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        snapshot_parts.append(f"{i + 1}:{line.rstrip()}\n")
            except Exception as e:
                snapshot_parts.append(f"Error reading file: {e}\n")
            snapshot_parts.append("```\n\n")
    return "".join(snapshot_parts) if snapshot_parts else "Snapshot complete. No files found."
