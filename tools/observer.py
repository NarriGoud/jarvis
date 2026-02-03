import pygetwindow as gw
import time
from core.speaker import speak

class GhostLog:
    def __init__(self):
        self.current_app = None
        self.start_time = time.time()
        self.app_history = {}

    def monitor(self):
        """Background loop to track window changes."""
        while True:
            try:
                window = gw.getActiveWindow()
                if window and window.title:
                    app_name = window.title
                    
                    # Detect change in focus
                    if app_name != self.current_app:
                        self.log_session(app_name)
                        self.current_app = app_name
                        self.start_time = time.time()
                        
                        # INTERESTING FACTOR: Contextual Welcome
                        if "Visual Studio Code" in app_name:
                            print(f"👨‍💻 Context: User started coding.")
                        elif "Chrome" in app_name:
                            print(f"🌐 Context: User is browsing.")

                # CHECK FOR BURNOUT: If in VS Code for > 2 hours (7200 seconds)
                elapsed = time.time() - self.start_time
                if "Visual Studio Code" in app_name:
                    if "MarketMind" in app_name:
                        speak("Welcome back to MarketMind, sir. Resuming the financial intelligence module.")
                    elif "TownLink" in app_name:
                        speak("Opening TownLink project. Connecting to local shop database.")
                    else:
                        speak("Back to the code, sir.")

            except Exception:
                pass
            time.sleep(5) # Check every 5 seconds to save CPU

    def log_session(self, app_name):
        duration = time.time() - self.start_time
        if self.current_app:
            self.app_history[self.current_app] = self.app_history.get(self.current_app, 0) + duration