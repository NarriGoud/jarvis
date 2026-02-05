from fastapi import FastAPI
import platform
import time
from tools.observer import GhostLog
import threading

from app.api import api
from app.config import APP_NAME, VERSION

app = FastAPI(title=APP_NAME, version=VERSION)

# Include your main chat/tools router
app.include_router(api)
# Initialize logging
observer = GhostLog()

@app.get("/")
def home():
    return {
        "status": f"{APP_NAME} is online 🚀",
        "system": platform.system(),
        "time": time.ctime()
    }

@app.get("/health")
def health():
    """Simple endpoint for the .bat file to check if the Brain is awake."""
    return {"status": "ready"}