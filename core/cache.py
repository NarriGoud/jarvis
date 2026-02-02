import json
import os
import time

CACHE_FILE = "data/cache.json"

def get_cache(key, expiry_seconds=3600):
    """
    Retrieves a value if it exists and hasn't expired.
    Default expiry is 1 hour (3600 seconds).
    """
    if not os.path.exists(CACHE_FILE):
        return None
        
    try:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
        
        entry = cache.get(key.lower().strip())
        if entry:
            # Check if the data is still fresh
            if time.time() - entry["timestamp"] < expiry_seconds:
                print(f"⚡ Cache Hit: '{key}'")
                return entry["value"]
            else:
                print(f"🗑️ Cache Expired: '{key}'")
    except Exception as e:
        print(f"⚠️ Cache Read Error: {e}")
        
    return None

def set_cache(key, value):
    """Saves a value with a current timestamp."""
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
        except:
            cache = {}

    cache[key.lower().strip()] = {
        "value": value,
        "timestamp": time.time()
    }
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)