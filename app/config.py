import os
from dotenv import load_dotenv

load_dotenv()

# --- API KEYS ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # For Vision/Analyze Screen

# --- TELEGRAM CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- ENDPOINTS ---
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- APP INFO ---
APP_NAME = "Jarvis Core"
VERSION = "0.4" # Incremented for new Alert & Vision modules
DEBUG_MODE = True # Useful for seeing those 'Brain Received' logs