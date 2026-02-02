import subprocess
import os

# Security: List of commands Jarvis is NOT allowed to run
BLACKLIST = ["rm -rf", "format", "shutdown", "deltree", "mkfs"]

def execute_shell(command: str):
    """Executes a system command and returns the output."""
    # Safety Check
    if any(forbidden in command.lower() for forbidden in BLACKLIST):
        return "Sir, that command is restricted for safety reasons."

    try:
        # Run command and capture output
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=15
        )
        
        output = result.stdout if result.stdout else result.stderr
        return output.strip() if output else "Command executed with no output."
        
    except subprocess.TimeoutExpired:
        return "The command took too long to execute and was terminated."
    except Exception as e:
        return f"Shell Error: {e}"