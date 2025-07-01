import os
from swe_tools.__init__ import mcp

@mcp.tool(name="delete_files", description="Deletes one or more specified files from the filesystem. This action is permanent and should be used with caution. Multiple file paths can be provided as a comma-separated string.")
def delete_files(paths: str) -> str:
    """
    Deletes one or more specified files from the filesystem. This action is permanent and should be used with caution. Multiple file paths can be provided as a comma-separated string.

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

