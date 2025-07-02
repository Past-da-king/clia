import subprocess
from typing import Optional
from swe_tools.__init__ import mcp

@mcp.tool(name="run_shell_command", description="This tool executes arbitrary shell commands directly on the underlying operating system's command-line interface (CLI). It is designed for comprehensive interaction with the system, allowing for the execution of system utilities (e.g., `ls`, `dir`, `cat`, `grep`, `find`), scripts (e.g., Python, Bash), version control operations (e.g., `git status`, `git diff`), file system manipulations (e.g., `mkdir`, `rm`, `cp`, `mv`), and inspection of system configurations or logs. The command is run as a subprocess, and its execution is not sandboxed, meaning it has the same permissions as the AI agent itself. The tool captures and returns the full output, including both standard output (stdout) and standard error (stderr), along with the command's exit status and numerical return code. A return code of 0 typically indicates successful execution, while any non-zero value signifies an error. The output format explicitly separates these components for clear interpretation. Users must specify the `command` string, and can optionally provide a `working_directory` (absolute path) to control the execution context; if omitted, the command runs in the AI agent's current working directory. Be aware that commands executed via this tool can have significant side effects, including modifying the file system, initiating network connections, or altering system state. Therefore, extreme caution and explicit user confirmation are paramount before executing any command that could lead to unintended consequences.")
def run_shell_command(command: str, working_directory: Optional[str] = None) -> str:
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
