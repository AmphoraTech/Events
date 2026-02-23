"""Minimal Flask app inside container. Returns hello + time."""
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify(message="hello", time=datetime.utcnow().isoformat())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
