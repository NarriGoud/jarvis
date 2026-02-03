# tools/vision.py
import pyautogui
import os
import time

def take_screenshot():
    """Captures the screen and returns a status message for Jarvis to speak."""
    save_path = os.path.join(os.getcwd(), "images")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    filename = f"jarvis_snap_{int(time.time())}.png"
    full_path = os.path.join(save_path, filename)

    try:
        pyautogui.screenshot().save(full_path)
        # Return a confirmation so Jarvis can say it
        return f"I've captured the screen and saved it as {filename} in your images folder, Narendra."
    except Exception as e:
        return f"I encountered an error while capturing the screen: {str(e)}"