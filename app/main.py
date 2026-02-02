from fastapi import FastAPI
import platform
import time

from app.api import api
from app.config import APP_NAME, VERSION

app = FastAPI(title=APP_NAME, version=VERSION)

app.include_router(api)


@app.get("/")
def home():
    return {
        "status": "Jarvis is online 🚀",
        "system": platform.system(),
        "time": time.ctime()
    }
