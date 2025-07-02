import subprocess
import os
from typing import Optional
from swe_tools.__init__ import mcp

@mcp.tool(name="run_shell_command", description="...")
def run_shell_command(command: str, working_directory: Optional[str] = None, timeout: int = 30) -> str:
    """
    Executes a given command in a robust, non-blocking way that captures all output
    without deadlocking. Works for any command, including Python, npm, etc.
    """
    if not command:
        return "Error: No command provided."

    try:
        # Set up environment to prevent interactive prompts
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,  # Prevent hanging on input
            text=True,
            cwd=working_directory,
            env=env,
        )

        stdout, stderr = process.communicate(timeout=timeout)
        return_code = process.returncode

        output = [
            f"Status: {'Success' if return_code == 0 else 'Failure'}",
            f"Return Code: {return_code}",
            "--- stdout ---",
            stdout.strip(),
            "--- stderr ---",
            stderr.strip()
        ]
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        timeout_output = [
            "Status: Failure",
            "Return Code: -1 (Terminated due to timeout)",
            f"Error: Command '{command}' timed out after {timeout} seconds and was terminated.",
            "--- stdout (captured before timeout) ---",
            stdout.strip() if stdout else "No stdout captured.",
            "--- stderr (captured before timeout) ---",
            stderr.strip() if stderr else "No stderr captured."
        ]
        return "\n".join(timeout_output)

    except Exception as e:
        return f"Error executing command '{command}': {e}"