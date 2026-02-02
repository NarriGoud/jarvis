# core/memory.py

class JarvisMemory:
    def __init__(self, limit=10):
        self.history = []
        self.limit = limit

    def add_entry(self, role, content):
        self.history.append({"role": role, "content": content})
        # Keep history from getting too long for the LLM context window
        if len(self.history) > self.limit:
            self.history = self.history[-self.limit:]

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []

# Global instance for the app to use
chat_memory = JarvisMemory()