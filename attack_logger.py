"""
attack_logger.py
Handles reading and writing attack logs to logs.json.
"""

import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.json")


def _load() -> list:
    """Load existing logs from file."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def _save(logs: list):
    """Save logs back to file."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def log_attack(ip: str, port: int):
    """
    Record a new attack attempt.
    If the IP already exists, increment its attempt count.
    Returns the updated log entry.
    """
    logs = _load()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if this IP already has an entry
    for entry in logs:
        if entry["ip"] == ip:
            entry["attempts"] += 1
            entry["last_seen"] = now
            entry["ports"].append(port)
            _save(logs)
            return entry

    # New attacker
    entry = {
        "ip":        ip,
        "port":      port,
        "ports":     [port],
        "timestamp": now,
        "last_seen": now,
        "attempts":  1,
    }
    logs.append(entry)
    _save(logs)
    return entry


def get_all_logs() -> list:
    """Return all attack log entries, newest first."""
    logs = _load()
    return sorted(logs, key=lambda x: x["last_seen"], reverse=True)


def get_stats() -> dict:
    """Return summary statistics."""
    logs = _load()
    total_attempts = sum(e["attempts"] for e in logs)
    return {
        "total_attacks":  total_attempts,
        "unique_ips":     len(logs),
        "recent":         sorted(logs, key=lambda x: x["last_seen"], reverse=True)[:5],
    }