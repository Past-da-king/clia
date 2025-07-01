# mcp_tools.py (Corrected according to FastMCP documentation)

import os
import fnmatch
import platform
import subprocess
import re
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

# This is the high-level helper we are using
from mcp.server.fastmcp import FastMCP

# This name is important for MCP discovery
mcp = FastMCP(
    "CliSweAiTools",
    description="A toolset for an AI to perform software engineering tasks on the command line.",
)

# --- Helper Functions (No changes needed here) ---

DEFAULT_IGNORE_PATTERNS = [
    ".git", ".gitignore", ".svn", "node_modules", "venv", ".venv",
    "__pycache__", "build", "dist", "*.log", "*.tmp", ".DS_Store"
]

def is_ignored(relative_path: str, ignore_patterns: List[str]) -> bool:
    normalized_path = relative_path.replace("\\", "/")
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(normalized_path, pattern) or fnmatch.fnmatch(os.path.basename(normalized_path), pattern):
            return True
    return False

def parse_multiline_commands(text: str) -> Dict[str, List[Tuple[int, str]]]:
    commands = defaultdict(list)
    current_file = None
    for line in text.strip().split('\n'):
        if line.strip().startswith('$$'):
            current_file = line.strip()[2:].strip()
        elif current_file and ':' in line:
            try:
                line_num_str, content = line.split(':', 1)
                line_num = int(line_num_str)
                commands[current_file].append((line_num, content))
            except ValueError:
                continue
    return commands

# --- Tool Definitions (Following FastMCP Documentation) ---
# The schema is now inferred from the function signature (name, parameters, type hints)
# and the docstring (description).

@mcp.tool()
def codebase_snapshot_generator(path: str = ".", ignore: Optional[str] = None) -> str:
    """
    Creates a string snapshot of a directory with line numbers. Uses '$$' as a file delimiter.

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


@mcp.tool()
def file_fetcher(path: str) -> str:
    """
    Retrieves the exact content of a single file.

    Args:
        path: The path to the file to fetch.
    """
    try:
        if not os.path.isfile(path): return f"Error: Path is not a file or does not exist: {path}"
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {e}"


@mcp.tool()
def line_editor(changes: str) -> str:
    """
    Modifies existing files based on line numbers and new content.

    Args:
        changes: A multiline string specifying file paths and line-by-line changes.
                 Format: $$path/to/file.ext\nline_num:new_content
    """
    commands = parse_multiline_commands(changes)
    report = []
    for file_path, edits in commands.items():
        if not os.path.isfile(file_path):
            report.append(f"Error for {file_path}: File not found.")
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
            replacement_map = defaultdict(list)
            for line_num, content in edits:
                replacement_map[line_num].append(content if content.endswith('\n') else content + '\n')
            new_content = []
            processed_lines = set()
            max_line = max(len(original_lines), max(replacement_map.keys()) if replacement_map else 0)
            for i in range(max_line):
                line_num = i + 1
                if line_num in replacement_map:
                    if line_num not in processed_lines:
                        new_content.extend(replacement_map[line_num])
                        processed_lines.add(line_num)
                elif i < len(original_lines):
                    new_content.append(original_lines[i])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_content)
            report.append(f"Successfully modified {file_path}")
        except Exception as e:
            report.append(f"Error modifying {file_path}: {e}")
    return "\n".join(report) if report else "No changes specified."


@mcp.tool()
def file_deleter(paths: str) -> str:
    """
    Deletes one or more files.

    Args:
        paths: A comma-separated string of file paths to delete.
    """
    if not paths: return "Error: No paths provided."
    paths_to_delete = [p.strip() for p in paths.split(',')]
    report = []
    for path in paths_to_delete:
        try:
            if os.path.isfile(path):
                os.remove(path)
                report.append(f"Successfully deleted file: {path}")
            elif os.path.isdir(path):
                report.append(f"Skipped: {path} is a directory.")
            else:
                report.append(f"Warning: File not found: {path}")
        except Exception as e:
            report.append(f"Error deleting {path}: {e}")
    return "\n".join(report)


@mcp.tool()
def cli_commander(command: str, working_directory: Optional[str] = None) -> str:
    """
    Executes a command in the command-line interface.

    Args:
        command: The command to execute.
        working_directory: Optional directory to run the command in.
    """
    if not command: return "Error: No command provided."
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=working_directory, check=False
        )
        output = [
            f"Status: {'Success' if result.returncode == 0 else 'Failure'}",
            f"Return Code: {result.returncode}",
            "--- stdout ---", result.stdout.strip(),
            "--- stderr ---", result.stderr.strip()
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error executing command '{command}': {e}"


@mcp.tool()
def codebase_restorer(input_snapshot_content: str, output_directory: str = ".") -> str:
    """
    Reconstructs files from a line-numbered snapshot string. Used for new files or full overwrites.

    Args:
        input_snapshot_content: The snapshot string with '$$filepath' and line-numbered code.
        output_directory: The target directory to write files to. Defaults to '.'.
    """
    commands = parse_multiline_commands(input_snapshot_content)
    if not commands: return "Error: Input snapshot content is empty or invalid."
    os.makedirs(output_directory, exist_ok=True)
    report = []
    files_created = 0
    for file_path, contents in commands.items():
        full_path = os.path.join(output_directory, file_path)
        try:
            parent_dir = os.path.dirname(full_path)
            if parent_dir: os.makedirs(parent_dir, exist_ok=True)
            file_lines = [c for _, c in contents]
            with open(full_path, 'w', encoding='utf-8') as f:
                f.writelines([line + '\n' for line in file_lines])
            files_created += 1
            report.append(f"Successfully wrote {file_path}")
        except Exception as e:
            report.append(f"Error writing file {file_path}: {e}")
    return f"Restorer finished. Created/modified {files_created} files.\n" + "\n".join(report)


@mcp.tool()
def directory_tree_viewer(path: str = ".", max_depth: int = 3, ignore: Optional[str] = None) -> str:
    """
    Provides a tree-like representation of the directory structure.

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


# This allows the server to be run directly with "python mcp_tools.py"
if __name__ == "__main__":
    mcp.run()