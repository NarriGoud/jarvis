from fastapi import APIRouter, HTTPException
from core import router, brain

api = APIRouter()

@api.post("/chat")
def chat(data: dict):
    msg = data.get("message", "").strip()

    if not msg:
        raise HTTPException(status_code=400, detail="Message required")

    # 1. Local Interceptor (Instant actions like "Open Chrome")
    local_reply = router.route(msg)
    if local_reply:
        return {"reply": local_reply, "source": "local"}

    # 2. Deep Thinking (Complex queries & Tools)
    # This now calls the loop inside brain.py
    result = brain.think(msg)
    
    return result