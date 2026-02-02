import re
from tools import system, web
from tools.knowledge import get_personal_knowledge # Import your new tool

def route(message: str):
    # 1. Basic Cleaning
    msg = message.lower().strip()
    
    # 2. Remove filler words and trigger names
    # Added 'tell me about', 'who is' to support knowledge queries
    clean_msg = re.sub(r'\b(jarvis|hey|please|can you|tell me|what is|show me|the|who is|about)\b', '', msg).strip()

    # If the user just said "Hey Jarvis"
    if not clean_msg or clean_msg in ["hello", "hi"]:
        return "Yes, Narendra? I'm listening."

    # ------------------
    # KNOWLEDGE BASE INTERCEPTOR (New)
    # ------------------
    # If the user asks about your specific projects or business, handle it locally
    personal_keywords = ["marketmind", "market mind", "townlink", "sri anjaneya traders", "my business", "my project"]
    if any(k in clean_msg for k in personal_keywords):
        print(f"🧠 Local Knowledge Lookup: {clean_msg}")
        return get_personal_knowledge(clean_msg)

    # ------------------
    # PHYSICAL ACTIONS (Fuzzy Match)
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
    # SYSTEM STATS
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
    # WEB SHORTCUTS
    # ------------------
    yt_match = re.search(r"(?:search|play)\s+(?:on\s+)?youtube\s+(?:for\s+)?(.*)", clean_msg)
    if yt_match:
        query = yt_match.group(1).strip()
        return web.youtube_search(query)

    # ------------------
    # SPECIAL INTENTS
    # ------------------
    if any(k in clean_msg for k in ["status", "how are you", "system check"]):
        return "All systems online and ready, sir. Neural link is stable. 🚀"

    # ------------------
    # FALLBACK
    # ------------------
    return None