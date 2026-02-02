import requests
from app.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(message: str):
    """Sends a high-priority alert to Narendra's Telegram."""
    if not message:
        return "Sir, the alert message was empty."

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🚨 *JARVIS ALERT* 🚨\n\n{message}",
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"📲 Telegram Alert Sent: {message[:30]}...")
            return "Alert sent to your phone, sir."
        else:
            return f"Failed to send alert. Status: {response.status_code}"
    except Exception as e:
        return f"Alert system error: {e}"