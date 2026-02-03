import speech_recognition as sr
import os
import json

# Initialize the recognizer
r = sr.Recognizer()

def calibrate():
    with sr.Microphone() as source:
        print("🎤 Calibrating for fan noise... please stay quiet.")
        # Sample for 3 seconds for high accuracy
        r.adjust_for_ambient_noise(source, duration=3)
        
        # Lock the threshold to prevent fan-noise "creeping"
        r.energy_threshold = max(r.energy_threshold, 600)
        r.dynamic_energy_threshold = False
        
        print(f"✅ Offline Calibration complete. Threshold locked at: {int(r.energy_threshold)}")

def listen(speaker_module=None):
    with sr.Microphone() as source:
        # Snappy settings for fluid conversation
        r.pause_threshold = 0.8
        r.phrase_threshold = 0.4
        r.non_speaking_duration = 0.3
        
        print("🎤 Listening (Offline)...")
        try:
            # We still use sr.listen to handle the microphone energy logic
            audio = r.listen(source, timeout=None, phrase_time_limit=None)
            
            # Instant Barge-in: Kill audio as soon as speech is captured
            if speaker_module and speaker_module.is_speaking():
                speaker_module.stop_speaking()
                print("🛑 Interrupted playback.")

            print("🧠 Recognizing Locally...")

            # --- OFFLINE RECOGNITION BLOCK ---
            # This replaces r.recognize_google(audio)
            # You must point 'model_path' to where you extracted the Vosk folder
            model_path = os.path.join(os.getcwd(), "core", "vosk-model")
            
            if not os.path.exists(model_path):
                print("❌ Error: Vosk model not found in core/vosk-model")
                return None

            # recognize_vosk is built into the speech_recognition library
            raw_data = r.recognize_vosk(audio)
            
            # Vosk returns a JSON string, we need to extract the 'text' field
            result = json.loads(raw_data)
            text = result.get("text", "")
            
            return text if text.strip() else None

        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Offline Voice Error: {e}")
            return None