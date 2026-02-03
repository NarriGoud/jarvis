import re
from tools import system, web, alerts
from tools.knowledge import query_knowledge_base as get_personal_knowledge 
from tools import vision

def route(message: str):
    # 1. Basic Cleaning
    msg = message.lower().strip()
    
    # 2. Remove filler words
    clean_msg = re.sub(r'\b(jarvis|hey|please|can you|tell me|what is|show me|the|who is|about)\b', '', msg).strip()

    if not clean_msg or clean_msg in ["hello", "hi"]:
        return "Yes, Narendra? I'm listening."
    
    if any(k in clean_msg for k in ["screenshot", "capture screen", "save screen"]):
        return vision.take_screenshot()

    # ---------------------------------------------------------
    # 3. INTENT BYPASS (The Fix)
    # ---------------------------------------------------------
    # If the user wants to "send", "alert", or mentions "telegram",
    # we MUST return None so the LLM can coordinate multiple tools.
    bypass_keywords = ["telegram", "send", "alert", "message", "notify"]
    if any(k in clean_msg for k in bypass_keywords):
        print(f"📡 Complex Intent Detected ({clean_msg}) -> Routing to Brain.")
        return None

    # ------------------
    # KNOWLEDGE BASE INTERCEPTOR
    # ------------------
    personal_keywords = ["marketmind", "market mind", "townlink", "sri anjaneya traders", "my business", "my project"]
    if any(k in clean_msg for k in personal_keywords):
        print(f"🧠 Local Knowledge Lookup: {clean_msg}")
        return get_personal_knowledge(clean_msg)

    # ------------------
    # PHYSICAL ACTIONS
    # ------------------
    if re.search(r"\b(open|launch)\b.*\b(chrome|browser)\b", clean_msg):
        return web.open_chrome()
    
    if re.search(r"\b(new|another)\b.*\btab\b", clean_msg):
        return web.new_tab()

    if re.search(r"\b(close|exit|quit)\b.*\btab\b", clean_msg):
        return web.close_tab()

    if re.search(r"\b(close|exit|quit)\b.*\b(chrome|browser)\b", clean_msg):
        return web.close_chrome()

    # ------------------
    # SYSTEM STATS (Now only runs if it didn't hit the bypass)
    # ------------------
    if any(k in clean_msg for k in ["cpu", "processor"]):
        return system.cpu()

    if any(k in clean_msg for k in ["ram", "memory"]):
        return system.ram()

    if any(k in clean_msg for k in ["disk", "storage", "space"]):
        return system.disk()

    if any(k in clean_msg for k in ["time", "date", "clock"]):
        return system.now()

    # ------------------
    # FALLBACK
    # ------------------
    return None