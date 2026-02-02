import requests
from app.config import OPENROUTER_API_KEY, OPENROUTER_URL

def ask_llm(messages_list: list):
    if not OPENROUTER_API_KEY:
        raise Exception("OPENROUTER_API_KEY missing")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Jarvis-Core"
    }

    # Keeping the same personality as Groq for consistency
    system_instruction = {
        "role": "system", 
        "content": "You are Jarvis. Be extremely brief. Answer in 1 or 2 sentences max."
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [system_instruction] + messages_list,
        "temperature": 0.6,
        "max_tokens": 150
    }

    res = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    res.raise_for_status()
    data = res.json()
    
    return data["choices"][0]["message"]["content"].strip()