import os
from collections import defaultdict
from swe_tools.__init__ import mcp
from swe_tools.utils import parse_multiline_commands

@mcp.tool(name="modify_file_lines", description="Modifies existing files by applying line-by-line changes based on a provided multiline string. This tool is precise and allows for inserting, updating, or deleting specific lines within a file. The format for changes is '$path/to/file.ext\nline_num:new_content'.")
def modify_file_lines(changes: str) -> str:
    """
    Modifies existing files by applying line-by-line changes based on a provided multiline string. This tool is precise and allows for inserting, updating, or deleting specific lines within a file. The format for changes is '$path/to/file.ext\nline_num:new_content'.

    Args:
        changes: A multiline string specifying file paths and line-by-line changes.
                 Format: $path/to/file.ext\nline_num:new_content
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

