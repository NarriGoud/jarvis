import sys
import pyttsx3

def main():
    # Join all command line arguments as a single string
    text = " ".join(sys.argv[1:])

    if not text:
        return

    try:
        # Initialize the offline SAPI5 engine
        engine = pyttsx3.init()

        # --- Voice Personality ---
        # Get list of available voices (Windows usually has David and Zira)
        voices = engine.getProperty('voices')
        
        # 0 = Microsoft David (Male - Authoritative)
        # 1 = Microsoft Zira (Female - Clear)
        # Change the index below to switch personality
        engine.setProperty('voice', voices[0].id) 

        # --- Speech Dynamics ---
        # 175-190 is a "Smart/Fast" rate for a Jarvis-like feel
        engine.setProperty("rate", 185) 
        engine.setProperty("volume", 1.0) 

        # Execution
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        # Fallback to console print if audio driver is busy
        print(f"TTS Error: {e}")

if __name__ == "__main__":
    main()