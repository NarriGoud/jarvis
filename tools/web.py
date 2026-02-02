import webbrowser
import pyautogui
import time
import urllib.parse

# Global delay to prevent actions from overlapping
pyautogui.PAUSE = 0.5 

def _focus_browser():
    """Ensures the browser is the active window before typing."""
    # This is a common trick: Alt+Tab briefly or click a safe area
    # For now, we assume the browser was the last active window
    pass

def search_chrome(query):
    """
    Uses the Address Bar shortcut (Ctrl+L) to search directly 
    from any existing tab.
    """
    # 1. Focus the address bar (Works as a search box in Chrome)
    pyautogui.hotkey('ctrl', 'l') 
    time.sleep(0.2)
    # 2. Type and Enter
    pyautogui.write(query)
    pyautogui.press('enter')
    return f"Searching Chrome for '{query}' in the current tab."

def search_youtube(query):
    """
    Specifically targets the YouTube search box using the '/' shortcut.
    Note: Only works if the active tab is already on YouTube.
    """
    # YouTube shortcut for focusing search box is '/'
    pyautogui.press('/') 
    time.sleep(0.2)
    # Clear any existing text (Ctrl+A -> Backspace)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    # Type and Enter
    pyautogui.write(query)
    pyautogui.press('enter')
    return f"Searching YouTube for '{query}'."

def open_youtube_same_tab():
    """Forces the current tab to navigate to YouTube."""
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.write('https://www.youtube.com')
    pyautogui.press('enter')
    return "Navigating to YouTube in the current tab."

def tab_manager(action):
    """Handles tab lifecycle management."""
    if action == "new":
        pyautogui.hotkey('ctrl', 't')
        return "New tab opened."
    elif action == "close":
        pyautogui.hotkey('ctrl', 'w')
        return "Tab closed."
    elif action == "next":
        pyautogui.hotkey('ctrl', 'tab')
        return "Switched to next tab."