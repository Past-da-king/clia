import os
from swe_tools.__init__ import mcp

@mcp.tool(name="read_file_content", description="Retrieves and returns the entire content of a single specified file. This is useful for examining the exact contents of a file for analysis or modification.")
def read_file_content(path: str) -> str:
    """
    Retrieves and returns the entire content of a single specified file. This is useful for examining the exact contents of a file for analysis or modification.

    Args:
        path: The path to the file to fetch.
    """
    try:
        if not os.path.isfile(path): return f"Error: Path is not a file or does not exist: {path}"
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {e}"
