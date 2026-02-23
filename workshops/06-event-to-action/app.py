"""Flask app: GET /on, /off, /status — write state to file and log. No hardware required."""
from flask import Flask, jsonify
from datetime import datetime
import os

STATE_FILE = "/home/pi/state.txt"
LOG_FILE = "/home/pi/action.log"
app = Flask(__name__)


def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} {msg}\n")


@app.route("/on")
def on():
    with open(STATE_FILE, "w") as f:
        f.write("on")
    log("on")
    return jsonify(status="on"), 200


@app.route("/off")
def off():
    with open(STATE_FILE, "w") as f:
        f.write("off")
    log("off")
    return jsonify(status="off"), 200


@app.route("/status")
def status():
    s = "off"
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            s = f.read().strip() or "off"
    return jsonify(status=s), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
