import os
from swe_tools.__init__ import mcp
from swe_tools.utils import parse_multiline_commands

@mcp.tool(name="restore_files_from_snapshot", description="Reconstructs files and directories from a provided snapshot string. This tool is used to create new files or overwrite existing ones based on the snapshot's content. The snapshot format includes '$filepath' followed by line-numbered code.")
def restore_files_from_snapshot(input_snapshot_content: str, output_directory: str = ".") -> str:
    """
    Reconstructs files and directories from a provided snapshot string. This tool is used to create new files or overwrite existing ones based on the snapshot's content. The snapshot format includes '$filepath' followed by line-numbered code.

    Args:
        input_snapshot_content: The snapshot string with '$filepath' and line-numbered code.
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

