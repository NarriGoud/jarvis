import speech_recognition as sr
import os

# Initialize the recognizer
r = sr.Recognizer()

def calibrate():
    with sr.Microphone() as source:
        print("🎤 Calibrating for fan noise... please stay quiet.")
        # Sample for 3 seconds for better accuracy
        r.adjust_for_ambient_noise(source, duration=3)
        
        # High threshold to filter out your PC fan
        r.energy_threshold = max(r.energy_threshold, 800)
        r.dynamic_energy_threshold = False
        
        print(f"✅ Online Calibration complete. Threshold locked at: {int(r.energy_threshold)}")

def listen(speaker_module=None):
    with sr.Microphone() as source:
        # Settings for a snappier feel
        r.pause_threshold = 0.8
        r.phrase_threshold = 0.4
        r.non_speaking_duration = 0.3
        
        print("🎤 Listening (Online)...")
        try:
            # timeout=None waits forever for you to start
            audio = r.listen(source, timeout=None, phrase_time_limit=None)
            
            # Instant Barge-in: Kill Jarvis's voice as soon as you stop talking
            if speaker_module and speaker_module.is_speaking():
                speaker_module.stop_speaking()
                print("🛑 Interrupted playback.")

            print("🧠 Recognizing (Google)...")
            
            # Reverting to Google Cloud Recognition
            text = r.recognize_google(audio)
            
            if text.strip():
                return text.lower().strip()
            
            return None

        except sr.UnknownValueError:
            # This triggers if it hears noise but no words
            return None
        except sr.RequestError as e:
            print(f"⚠️ Google Service Error: {e}")
            return None
        except Exception as e:
            print(f"Voice Error: {e}")
            return None