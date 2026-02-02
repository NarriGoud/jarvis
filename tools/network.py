import os
import platform
import subprocess
import socket

def ping_host(hostname="8.8.8.8"):
    """Pings a host to check for internet/server connectivity."""
    # Determine parameter based on OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', hostname]
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return f"Ping to {hostname} successful. Host is online."
    except subprocess.CalledProcessError:
        return f"Ping to {hostname} failed. Host appears to be offline."

def get_ip_info():
    """Returns local and public IP details."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return f"Local IP: {local_ip} | Hostname: {hostname}"

def check_port(host, port):
    """Checks if a specific port is open (useful for checking your API or DB)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, int(port)))
    sock.close()
    return f"Port {port} on {host} is {'OPEN' if result == 0 else 'CLOSED'}."