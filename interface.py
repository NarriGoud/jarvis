# D:\Kelly-1.0.0\jarvis\main.py
from core import voice
from core import speaker
import requests

def run_interface():
    voice.calibrate() # Calibrate mic at start
    
    while True:
        # Pass the speaker module into listen so it can kill audio if you speak
        user_input = voice.listen(speaker_module=speaker)
        
        if not user_input:
            continue

        print(f"🔍 Heard: {user_input}")

        # 1. Stop command - handle locally for instant response
        if any(word in user_input.lower() for word in ["stop", "shut up", "wait"]):
            speaker.stop_speaking()
            continue

        # 2. Send to Brain API
        try:
            response = requests.post("http://127.0.0.1:8000/chat", json={"message": user_input})
            if response.status_code == 200:
                reply = response.json().get("reply")
                print(f"🤖 Jarvis: {reply}")
                speaker.speak(reply) # Speak the answer
        except Exception as e:
            print(f"❌ Brain Unreachable. Make sure app/main.py is running.")

if __name__ == "__main__":
    run_interface()