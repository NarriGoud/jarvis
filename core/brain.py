import json
import re
from core.memory import chat_memory
from core import cache  # <--- New Import
from services.groq_ai import ask_groq
from tools.finance import get_market_data
from tools.search import web_search
from tools.knowledge import query_knowledge_base as get_personal_knowledge
from tools.alerts import send_telegram_alert
from tools.shell import execute_shell
from tools.network import ping_host, check_port
from tools import system, web

def think(user_input: str):
    """The central nervous system. Processes input, checks cache, and executes tools."""
    
    # 1. Add User Input to Memory
    chat_memory.add_entry("user", user_input)

    # 2. Cache Interceptor: Check if we already answered this recently (e.g., last 1 hour)
    cached_reply = cache.get_cache(user_input, expiry_seconds=3600)
    if cached_reply:
        chat_memory.add_entry("assistant", cached_reply)
        return {"reply": cached_reply, "source": "cache"}

    try:
        # Agentic Loop (Up to 5 steps)
        for _ in range(5):
            history = chat_memory.get_history()
            response_message = ask_groq(history)
            
            # --- CASE A: Tool Calls ---
            if response_message.get("tool_calls"):
                chat_memory.history.append(response_message)
                
                for tool_call in response_message["tool_calls"]:
                    func_name = tool_call["function"]["name"]
                    call_id = tool_call["id"]
                    args_raw = tool_call["function"]["arguments"]

                    # Robust JSON Repair
                    try:
                        args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                    except json.JSONDecodeError:
                        args_repaired = re.search(r"(\{.*\})", str(args_raw), re.DOTALL)
                        args = json.loads(args_repaired.group(1)) if args_repaired else {}

                    print(f"🔧 Jarvis executing: {func_name}({args})")

                    # Tool Routing
                    result = "Tool not found."
                    if func_name == "get_stock_price":
                        result = get_market_data(args.get("symbol"))
                    elif func_name == "web_search":
                        result = web_search(args.get("query"))
                    elif func_name == "get_personal_knowledge":
                        result = get_personal_knowledge(args.get("query"))
                    elif func_name == "get_system_stats":
                        m = args.get("metric")
                        result = getattr(system, m)() if hasattr(system, m) else "Invalid metric"
                    elif func_name == "send_telegram_alert":
                        result = send_telegram_alert(args.get("message"))
                    elif func_name == "execute_shell":
                        result = execute_shell(args.get("command"))
                    elif func_name == "network_diagnostic":
                        action = args.get("action")
                        if action == "ping": result = ping_host(args.get("target", "8.8.8.8"))
                        elif action == "port": result = check_port(args.get("target"), args.get("port"))
                    elif func_name == "browser_control":
                        act, val = args.get("action"), args.get("query", "")
                        if act == "open": result = web.open_chrome()
                        elif act == "search_youtube": result = web.youtube_search(val)
                        elif act == "navigate": result = web.navigate_to(val)
                        elif act == "close_tab": result = web.close_tab()
                        elif act == "type": result = web.type_text(val)
                        else: result = f"Action {act} not recognized."

                    # Add Tool Result to Memory
                    chat_memory.history.append({
                        "role": "tool",
                        "tool_call_id": call_id,
                        "name": func_name,
                        "content": json.dumps(result)
                    })
                
                continue # Re-think with the new tool data

            # --- CASE B: Final Response ---
            final_text = response_message.get("content")
            if final_text:
                final_text = final_text.strip()
                chat_memory.add_entry("assistant", final_text)
                
                # 3. Save to Cache for future use
                cache.set_cache(user_input, final_text)
                
                return {"reply": final_text, "source": "agent_action"}

        return {"reply": "Sir, I've reached my processing limit.", "source": "agent_limit"}

    except Exception as e:
        print(f"⚠️ Brain Error: {e}")
        return {"reply": "I encountered a processing error in my neural core, sir.", "source": "error"}