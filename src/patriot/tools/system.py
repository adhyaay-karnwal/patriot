from __future__ import annotations

import subprocess
from pathlib import Path

from langchain.tools import tool


@tool
def read_text_file(file_path: str, max_bytes: int = 5000, encoding: str = "utf-8") -> str:
    """
    Read part of a text-based configuration, log, or checklist file for review.

    Use this tool when a CyberPatriot task provides documentation, checklists, or exported
    configuration files that need to be inspected. The tool returns up to ``max_bytes`` of
    decoded text so you can reason about the content without loading massive images in one call.
    """
    path = Path(file_path).expanduser()
    if not path.exists():
        return f"Error: The file '{file_path}' was not found."
    if not path.is_file():
        return f"Error: The path '{file_path}' is not a regular file."

    try:
        with path.open("rb") as handle:
            raw_sample = handle.read(max_bytes)
    except Exception as exc:  # pragma: no cover - defensive
        return f"Error: Failed to read '{file_path}': {exc}"

    if not raw_sample:
        return "Note: File is empty or contains unsupported characters."

    try:
        content = raw_sample.decode(encoding, errors="ignore")
    except LookupError:
        return f"Error: Unknown text encoding '{encoding}'."

    try:
        file_size = path.stat().st_size
    except OSError as exc:
        return f"Error: Unable to determine file size for '{file_path}': {exc}"

    if file_size > len(raw_sample):
        return (
            f"File snippet (first {len(raw_sample)} bytes of {file_size}):\n"
            f"{content}\n"
            "Note: Output truncated. Increase max_bytes to read further."
        )

    return content


@tool
def run_shell_command(command: str, timeout_seconds: int = 30) -> str:
    """
    Execute a read-only shell command within the training environment.

    Use this for commands such as `dir`, `ls`, `ipconfig`, `ifconfig`, `netstat`, or other
    non-destructive queries that mirror CyberPatriot-style investigative steps. Avoid
    commands that change system state or require elevated privileges.
    """
    if not command.strip():
        return "Error: No command provided."

    try:
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout_seconds} seconds."
    except Exception as exc:  # pragma: no cover - defensive
        return f"Error: Failed to execute command: {exc}"

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()

    if completed.returncode != 0:
        return (
            f"Command exited with code {completed.returncode}.\n"
            f"STDOUT:\n{stdout or '(no stdout)'}\n"
            f"STDERR:\n{stderr or '(no stderr)'}"
        )

    if stdout and stderr:
        return f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"
    if stdout:
        return stdout
    if stderr:
        return f"STDERR:\n{stderr}"
    return "Command completed with no output."
