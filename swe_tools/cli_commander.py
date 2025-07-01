import subprocess
from typing import Optional
from swe_tools.__init__ import mcp

@mcp.tool(name="execute_shell_command", description="Executes a given command in the system's command-line interface and returns its output, including standard output and standard error. Useful for running system commands, scripts, or interacting with the shell.")
def execute_shell_command(command: str, working_directory: Optional[str] = None) -> str:
    """
    Executes a given command in the system's command-line interface and returns its output, including standard output and standard error. Useful for running system commands, scripts, or interacting with the shell.

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
