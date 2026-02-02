from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    reply: str
    source: str  # e.g., 'llm', 'cache', or 'system'
    action_taken: Optional[str] = None