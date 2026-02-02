import subprocess
import os
import sys

# Global variable to track the active speech process
_active_process = None

def is_speaking():
    """Returns True if Jarvis is currently talking."""
    global _active_process
    return _active_process is not None and _active_process.poll() is None

def stop_speaking():
    """Instantly kills the speech process."""
    global _active_process
    if is_speaking():
        _active_process.terminate()
        _active_process = None

def speak(text: str):
    global _active_process
    stop_speaking() # Interrupt any current speech

    script_path = os.path.join(os.getcwd(), "speak.py")
    _active_process = subprocess.Popen(
        [sys.executable, script_path, text],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )