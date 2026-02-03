import speech_recognition as sr
import winsound

r = sr.Recognizer()

def calibrate():
    with sr.Microphone() as source:
        print("🎤 Calibrating for fan noise... please stay quiet.")
        # Step 1: Sample the room for 3 seconds instead of 2 for better accuracy
        r.adjust_for_ambient_noise(source, duration=3)
        
        # Step 2: Set a higher floor. If 350 was spamming, 600-800 is safer.
        # If it still spams, change 600 to 1000 below.
        r.energy_threshold = max(r.energy_threshold, 600)
        
        # Step 3: Disable dynamic adjustment so he doesn't get "too sensitive" over time
        r.dynamic_energy_threshold = False
        
        print(f"✅ Calibration complete. Threshold locked at: {int(r.energy_threshold)}")

def listen(speaker_module=None):
    with sr.Microphone() as source:
        # --- NOISE REJECTION SETTINGS ---
        r.pause_threshold = 0.8       # Wait 0.8s of silence to end a sentence
        r.phrase_threshold = 0.4      # Sound must last 0.4s to be speech (filters clicks)
        r.non_speaking_duration = 0.3 # Snappy transition
        
        print("🎤 Listening...")
        try:
            # timeout=None means he waits forever for you to start
            # phrase_time_limit=None means he won't cut you off mid-sentence
            audio = r.listen(source, timeout=None, phrase_time_limit=None)
            
            # Instant Barge-in: Kill Jarvis's voice if he's talking
            if speaker_module and speaker_module.is_speaking():
                speaker_module.stop_speaking()
                print("🛑 Interrupted playback.")

            print("🧠 Recognizing...")
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            # This happens when it hears "something" but it's not words (like the fan)
            return None
        except Exception as e:
            print(f"Voice Error: {e}")
            return None