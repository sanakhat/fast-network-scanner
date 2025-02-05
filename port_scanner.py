import socket
import threading
from queue import Queue

def get_target_ip(target):
    """Resolves a domain name to an IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Invalid target: {target}")
        exit()

def scan_port(target_ip, port):
    """Scans a single port and adds it to open_ports if open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)  # Short timeout for fast scanning
        if s.connect_ex((target_ip, port)) == 0:
            print(f"[+] Port {port} is open")
            open_ports.append(port)

def threader():
    """Thread worker function to process ports in parallel."""
    while True:
        port = queue.get()
        scan_port(TARGET_IP, port)
        queue.task_done()

# Get target from user
TARGET = input("Enter target IP or domain: ").strip()
TARGET_IP = get_target_ip(TARGET)

# Port range (adjust as needed)
PORTS = range(1, 1025)
THREADS = 100  # Number of threads

open_ports = []
queue = Queue()

# Create and start threads
for _ in range(THREADS):
    t = threading.Thread(target=threader, daemon=True)
    t.start()

# Add ports to queue
for port in PORTS:
    queue.put(port)

# Wait for all threads to complete
queue.join()

print(f"\nOpen ports on {TARGET} ({TARGET_IP}): {open_ports}")
