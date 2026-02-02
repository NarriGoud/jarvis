import speech_recognition as sr
import winsound

# Initialize the recognizer globally so calibration persists
r = sr.Recognizer()

def calibrate():
    """Samples background noise (like fans) to set a baseline energy threshold."""
    with sr.Microphone() as source:
        print("🎤 Calibrating for fan noise... please stay quiet.")
        # Samples for 2 seconds to distinguish hum from voice
        r.adjust_for_ambient_noise(source, duration=2)
        # Allows the system to adapt if noise levels change slightly
        r.dynamic_energy_threshold = True
        # Small floor to ensure it doesn't get TOO sensitive in a dead silent room
        if r.energy_threshold < 400:
            r.energy_threshold = 400
        print(f"✅ Calibration complete. Energy threshold set to: {int(r.energy_threshold)}")

def listen():
    with sr.Microphone() as source:
        # --- DYNAMIC SETTINGS ---
        # 1. How long it waits after you stop talking (1.2s - 1.5s is the sweet spot)
        r.pause_threshold = 1.3 
        
        # 2. Ensures it doesn't cut you off if you take a quick breath mid-sentence
        r.non_speaking_duration = 0.6 
        
        winsound.Beep(1000, 100)
        print("🎤 Listening...")
        
        try:
            # timeout: seconds to wait for speech to START
            # phrase_time_limit: None lets you speak a long sentence without cutoff
            audio = r.listen(source, timeout=5, phrase_time_limit=None)
            
            # Second beep to signal Jarvis has stopped recording and started thinking
            winsound.Beep(700, 50) 
            print("🧠 Recognizing...")
            
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            # This triggers if it hears sound but can't identify words
            return None
        except Exception as e:
            print(f"Voice Error: {e}")
            return None