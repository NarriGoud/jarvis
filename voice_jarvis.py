import requests
import time
import sys
import core.speaker as speaker  
from core.voice import listen, calibrate
from core.speaker import speak, stop_speaking, is_speaking

# Configuration
API_URL = "http://127.0.0.1:8000/chat"
WAKE_WORD = "hey jarvis"
SESSION_LIMIT = 25 
SILENCE_DELAY = 0.5  # Time to wait after speaking to avoid echo

def ask_jarvis(text):
    """Communicates with the FastAPI brain with robust error handling."""
    try:
        res = requests.post(API_URL, json={"message": text}, timeout=30)
        if res.status_code == 200:
            data = res.json()
            return data.get("reply"), data.get("source")
        return "The neural link is unstable, sir. Error code received.", "system"
    except requests.exceptions.ConnectionError:
        return "OFFLINE", "system"
    except Exception as e:
        return f"Neural link error: {e}", "system"

def main():
    print("🤖 JARVIS: Tactical Command Interface")
    calibrate() 
    
    # Visual indication of readiness
    print("\n" + "="*40)
    print("  SYSTEM STATUS: ONLINE & MONITORING")
    print("="*40 + "\n")
    
    speak("Jarvis is online and ready for your command, Narendra.")
    
    # Wait for the intro to finish so the mic doesn't catch it
    while is_speaking(): time.sleep(0.1)

    active = False
    last_interaction = time.time()

    while True:
        # 1. Session Management (Auto-Sleep)
        if active and (time.time() - last_interaction > SESSION_LIMIT):
            active = False
            print("💤 Session idle. Reverting to Sleep Mode.")
            # Optional: speak("Standing by, sir.")

        # 2. Capture Input
        # The 'speaker' module is passed to 'listen' for instant hardware-level barge-in
        text = listen(speaker_module=speaker)
        
        if not text:
            continue
        
        # 3. Handle Interruptions
        # If we get here, 'listen' has already caught speech. If Jarvis was talking, kill it.
        if is_speaking():
            stop_speaking()
            print("🛑 Playback Terminated by Barge-in.")

        raw_text = text.lower().strip()
        print(f"🔍 DEBUG (Heard): {raw_text}")

        # 4. Instant Stop/Silence Logic (Local Override)
        if any(w in raw_text for w in ["stop", "shut up", "be quiet", "cancel"]):
            print("🤐 Manual override: Jarvis silenced.")
            last_interaction = time.time()
            continue

        # 5. Wake Word & State Logic
        if not active:
            if any(word in raw_text for word in [WAKE_WORD, "jarvis", "hey jar"]):
                active = True
                last_interaction = time.time()
                
                # Extract command from wake sentence
                command = raw_text.replace(WAKE_WORD, "").replace("jarvis", "").strip()
                if not command:
                    speak("I'm listening, sir.")
                    while is_speaking(): time.sleep(0.1)
                    continue 
                else:
                    text_to_process = command 
            else:
                continue 
        else:
            text_to_process = raw_text

        # 6. Session Exit Logic
        if any(w in text_to_process for w in ["exit", "bye", "go to sleep", "dismissed"]):
            speak("Understood. I'll be here if you need me.")
            while is_speaking(): time.sleep(0.1)
            active = False
            continue

        # 7. Neural Processing (Brain Request)
        last_interaction = time.time()
        print("🧠 Thinking...")
        reply, source = ask_jarvis(text_to_process)

        # Handle Boot-up/Offline state
        if reply == "OFFLINE":
            print("⚠️ Waiting for Brain to initialize weights...")
            speak("I am still initializing my neural weights, sir. One moment.")
            while is_speaking(): time.sleep(0.1)
            continue

        # 8. Output Response
        if reply:
            print(f"🤖 ({source}): {reply}")
            speak(reply)
            
            # --- ECHO PREVENTION ---
            # We wait for the speech to finish, then add a tiny buffer.
            # This ensures Jarvis doesn't hear the last word of his own sentence.
            while is_speaking():
                time.sleep(0.1)
            time.sleep(SILENCE_DELAY) 
            
            last_interaction = time.time()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Jarvis powering down. Goodbye, Narendra.")
        sys.exit()