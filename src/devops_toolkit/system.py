import shutil
import subprocess
import logging
from typing import Optional, List, Union

logger = logging.getLogger(__name__)

def check_binary_exists(cmd: str) -> bool:
    """
    Verifies that a required binary is installed and available in PATH.
    
    Args:
        cmd: The name of the command to check (e.g., 'kubectl').
        
    Returns:
        True if the command exists, False otherwise.
    """
    exists = shutil.which(cmd) is not None
    if not exists:
        logger.warning(f"Binary '{cmd}' not found in PATH.")
    return exists

def run_command(
    cmd: Union[str, List[str]], 
    shell: bool = False, 
    check: bool = True, 
    capture_output: bool = False,
    cwd: Optional[str] = None
) -> subprocess.CompletedProcess:
    """
    Executes a shell command with consistent logging and error handling.
    
    Args:
        cmd: The command to run. Can be a string (if shell=True) or a list of strings.
        shell: Whether to execute the command through the shell.
        check: Whether to raise a CalledProcessError if the command fails.
        capture_output: Whether to capture stdout and stderr.
        cwd: Current working directory for the command.
        
    Returns:
        The CompletedProcess instance.
    """
    cmd_str = cmd if isinstance(cmd, str) else " ".join(cmd)
    logger.debug(f"Executing command: {cmd_str}")

    try:
        # If capture_output is True, we use PIPE. Otherwise, we let it print to stdout/stderr.
        stdout = subprocess.PIPE if capture_output else None
        stderr = subprocess.PIPE if capture_output else None

        result = subprocess.run(
            cmd, 
            shell=shell, 
            check=check, 
            stdout=stdout, 
            stderr=stderr, 
            text=True,
            cwd=cwd
        )
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd_str}")
        if capture_output and e.stderr:
            logger.error(f"Stderr: {e.stderr.strip()}")
        if check:
            raise
        return e
