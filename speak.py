import sys
import pyttsx3

def main():
    # Join all command line arguments as a single string
    text = " ".join(sys.argv[1:])

    if not text:
        return

    engine = pyttsx3.init()

    # --- Voice Customization ---
    # 150-180 is a natural conversational rate
    engine.setProperty("rate", 175) 
    engine.setProperty("volume", 1.0) # Range 0.0 to 1.0

    # Optional: Change to a female voice if available
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[1].id) # 0 for male, 1 for female

    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    main()