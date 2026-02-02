import psutil
import platform
import time

def cpu():
    # interval=1 is recommended for an accurate reading
    usage = psutil.cpu_percent(interval=1)
    return f"The current CPU usage is {usage}%."

def ram():
    mem = psutil.virtual_memory()
    # Convert bytes to GB for readability
    used_gb = round(mem.used / (1024**3), 2)
    return f"RAM usage is at {mem.percent}%. You are using {used_gb} GB."

def disk():
    d = psutil.disk_usage('/')
    free_gb = round(d.free / (1024**3), 2)
    return f"You have {free_gb} GB of free storage remaining."

def now():
    # Returns a readable string of the current time
    return f"It is currently {time.ctime()}."