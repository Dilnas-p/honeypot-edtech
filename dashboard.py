"""
dashboard.py
Flask web dashboard for the EdTech Honeypot.
Run this separately from listener.py.

Usage:
    python dashboard.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, jsonify
from attack_logger import get_all_logs, get_stats

app = Flask(__name__)


@app.route("/")
def index():
    stats = get_stats()
    logs  = get_all_logs()
    return render_template("dashboard.html", stats=stats, logs=logs)


@app.route("/api/logs")
def api_logs():
    """JSON endpoint — lets the dashboard auto-refresh without a page reload."""
    return jsonify({
        "stats": get_stats(),
        "logs":  get_all_logs(),
    })


if __name__ == "__main__":
    print("\n  EdTech Honeypot Dashboard")
    print("  Open → http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)