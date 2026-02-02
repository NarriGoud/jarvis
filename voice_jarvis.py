import requests
import time
from core.voice import listen, calibrate
from core.speaker import speak, stop_speaking, is_speaking

API_URL = "http://127.0.0.1:8000/chat"
WAKE_WORD = "hey jarvis"
SESSION_LIMIT = 20  # Increased for more natural multi-turn flow

def ask_jarvis(text):
    try:
        res = requests.post(API_URL, json={"message": text}, timeout=30)
        data = res.json()
        return data.get("reply"), data.get("source")
    except Exception as e:
        return f"Brain unreachable: {e}", "system"

def main():
    print("🤖 Jarvis: Dynamic Process Tracking Mode")
    calibrate() 
    speak("Jarvis is online.")
    
    # Wait for startup greeting to finish before listening
    while is_speaking():
        time.sleep(0.1)

    active = False
    last_interaction = 0

    while True:
        # 1. Handle Auto-Sleep
        if active and (time.time() - last_interaction > SESSION_LIMIT):
            active = False
            print("💤 Session timed out. Entering sleep mode...")

        # 2. Listen for Input
        text = listen()
        if not text:
            continue
        
        # BARGE-IN: If you speak, the AI instantly stops its current audio
        stop_speaking()

        text = text.lower().strip()
        print(f"🔍 DEBUG (Heard): {text}")

        # --- 3. Wake Word Logic (Fuzzy Matching) ---
        if not active:
            if any(word in text for word in [WAKE_WORD, "jarvis", "hey jar"]):
                active = True
                last_interaction = time.time()
                
                # Check for "One-Shot" commands (e.g., "Hey Jarvis, what's the time?")
                command = text.replace(WAKE_WORD, "").replace("jarvis", "").replace("hey jar", "").strip()
                if not command:
                    speak("Yes, sir?")
                    while is_speaking(): time.sleep(0.1)
                    continue 
                else:
                    text = command # Immediately process the attached command
            else:
                continue 

        # --- 4. Exit Logic ---
        if any(w in text for w in ["exit", "bye", "goodbye", "go to sleep"]):
            speak("Goodbye, sir.")
            while is_speaking(): time.sleep(0.1)
            active = False
            continue

        # --- 5. Process Command ---
        last_interaction = time.time()
        print("🧠 Processing...")
        reply, source = ask_jarvis(text)

        if reply:
            print(f"🤖 ({source}): {reply}")
            speak(reply)
            
            # --- THE DYNAMIC FIX ---
            # No more fixed timers. We wait exactly until the speech process ends.
            print("🔇 Jarvis is speaking...")
            while is_speaking():
                time.sleep(0.1)
            
            # Small 0.3s pause for room echo to settle before mic re-opens
            time.sleep(0.3)
            
            # Reset timer after speaking is finished
            last_interaction = time.time() 

if __name__ == "__main__":
    main()