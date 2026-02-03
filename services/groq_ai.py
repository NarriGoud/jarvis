import requests
import json
import re
from app.config import GROQ_API_KEY, GROQ_URL

# --- Hardened Tool Definitions ---
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get real-time stock price and market data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Ticker (e.g. AAPL)"}
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search for live web data, news, and weather.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_stats",
            "description": "Check the computer's CPU, RAM, or Disk usage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric": {"type": "string", "enum": ["cpu", "ram", "disk", "time"]}
                },
                "required": ["metric"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_control",
            "description": "Physically control the browser (open, search, close).",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["open", "search_google", "navigate", "search_youtube", "close_tab", "close_browser", "new_tab", "type"]
                    },
                    "query": {"type": "string", "description": "Search term or URL."}
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_personal_knowledge",
            "description": "Check this first for info about Narendra, MarketMind AI, TownLink, or his business.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The topic to look up."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_telegram_alert",
            "description": "Send a text message alert to Narendra's Telegram phone app for urgent notifications.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "The alert message content."}
                },
                "required": ["message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_shell",
            "description": "Execute a terminal command on the local system (e.g., list files, check processes).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to run."}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "network_diagnostic",
            "description": "Diagnose network issues using ping or port checking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string", 
                        "enum": ["ping", "port"],
                        "description": "The type of diagnostic to perform."
                    },
                    "target": {
                        "type": "string", 
                        "description": "The host or IP (e.g., '8.8.8.8' or 'google.com')."
                    },
                    "port": {
                        "type": "integer", 
                        "description": "The port number (only required for 'port' action)."
                    }
                },
                "required": ["action", "target"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Captures a screenshot of the current screen and saves it to the root 'images' directory. Use this when the user asks to capture the screen or 'look' at something on their monitor.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
    "type": "function",
    "function": {
      "name": "create_fastapi_project",
      "description": "Creates a new FastAPI project directory with a standard folder structure (app, core, tools).",
      "parameters": {
        "type": "object",
        "properties": {
          "project_name": { "type": "string", "description": "The name for the new project folder." }
        },
        "required": ["project_name"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "organize_screenshots",
      "description": "Moves all files from the images folder into a backup subfolder to keep the workspace clean.",
      "parameters": { "type": "object", "properties": {} }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "media_control",
      "description": "Controls system media playback like playing, pausing, skipping tracks, or adjusting volume.",
      "parameters": {
        "type": "object",
        "properties": {
          "action": { 
            "type": "string", 
            "enum": ["play", "pause", "next", "previous", "volume up", "volume down", "mute"] 
          }
        },
        "required": ["action"]
      }
    }
  }
]

def ask_groq(messages_list: list):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_instruction = {
        "role": "system", 
        "content": (
            "You are Jarvis. Be brief and efficient. "
            "When you receive tool results, synthesize the answer immediately. "
            "Do NOT perform repetitive searches. If the data is missing, tell the user. "
            "You are currently helping Narendra with his projects, including MarketMind AI."
        )
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [system_instruction] + messages_list,
        "tools": TOOLS,
        "tool_choice": "auto",
        "temperature": 0,
        "max_tokens": 1024
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=25)
        
        # --- HEALER LOGIC FOR ERROR 400 (HALLUCINATIONS) ---
        if res.status_code == 400:
            error_details = res.json()
            failed_gen = error_details.get("error", {}).get("failed_generation", "")
            
            if "<function=" in failed_gen:
                print("🔧 Jarvis: Repairing hallucinated tool format...")
                
                # Extract the function name (e.g., web_search)
                name_match = re.search(r"<function=(\w+)", failed_gen)
                # Extract ONLY the JSON block {...} to avoid "Extra data" errors
                json_match = re.search(r"(\{.*\})", failed_gen, re.DOTALL)

                if name_match and json_match:
                    func_name = name_match.group(1).strip()
                    args_str = json_match.group(1).strip()
                    
                    try:
                        # Verify it's valid JSON before returning
                        json.loads(args_str)
                        
                        return {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [{
                                "id": f"call_repaired_{func_name}",
                                "type": "function",
                                "function": {
                                    "name": func_name,
                                    "arguments": args_str
                                }
                            }]
                        }
                    except json.JSONDecodeError as je:
                        print(f"⚠️ Repair failed: JSON decode error: {je}")
            
            print(f"❌ Tool Call Failed: {json.dumps(error_details, indent=2)}")
            return {"role": "assistant", "content": "Sir, I encountered a syntax error in my processing logic."}

        if res.status_code != 200:
            print(f"❌ Groq API Error ({res.status_code}): {res.text}")
            return {"role": "assistant", "content": f"Sir, I encountered a processing error ({res.status_code})."}

        response_data = res.json()
        return response_data["choices"][0]["message"]

    except Exception as e:
        print(f"⚠️ Request Failed: {e}")
        return {"role": "assistant", "content": "I lost connection to my neural network, sir."}