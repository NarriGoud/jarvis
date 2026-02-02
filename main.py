import os
import subprocess
import sys


def start():
    print("🚀 Starting Jarvis Core...")

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    start()
