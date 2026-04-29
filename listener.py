"""
listener.py
EdTech Honeypot -- fake student portal socket listener.
"""

import socket
import threading
import argparse
import signal
import sys
from datetime import datetime
from attack_logger import log_attack

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
FAKE_BANNER  = (
    "\r\n"
    "==========================================\r\n"
    "   Welcome to EdTech Student Portal       \r\n"
    "      Secure Login -- v3.1.4              \r\n"
    "==========================================\r\n"
    "\r\n"
    "Username: "
)

RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
RESET  = "\033[0m"

shutdown_event = threading.Event()


def handle(conn, addr):
    ip, port = addr
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = log_attack(ip, port)

    print(
        RED + "[ALERT] " + RESET + now + " | " +
        "Connection from " + YELLOW + ip + ":" + str(port) + RESET + " | " +
        "Attempts: " + CYAN + str(entry["attempts"]) + RESET
    )

    try:
        conn.settimeout(3)
        conn.sendall(FAKE_BANNER.encode("utf-8"))
    except Exception as send_err:
        print(RED + "[ERROR] " + str(send_err) + RESET)
    finally:
        try:
            conn.recv(256)
        except Exception:
            pass
        conn.close()


def start(host, port):
    print("")
    print(GREEN + "==========================================" + RESET)
    print(GREEN + "   EdTech Honeypot -- Listener Active     " + RESET)
    print(GREEN + "==========================================" + RESET)
    print("  Listening on : " + host + ":" + str(port))
    print("  Dashboard    : http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop")
    print("")

    def _shutdown(sig, frame):
        print(YELLOW + "\n[INFO] Shutting down..." + RESET)
        shutdown_event.set()
        sys.exit(0)

    signal.signal(signal.SIGINT,  _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
    except OSError as e:
        print(RED + "[ERROR] Cannot bind: " + str(e) + RESET)
        sys.exit(1)

    server.listen(10)
    server.settimeout(1.0)

    while not shutdown_event.is_set():
        try:
            conn, addr = server.accept()
            t = threading.Thread(target=handle, args=(conn, addr), daemon=True)
            t.start()
        except socket.timeout:
            continue
        except OSError:
            break

    server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EdTech Honeypot Listener")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    start(args.host, args.port)