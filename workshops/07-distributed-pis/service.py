"""Minimal Flask service: GET /, GET /ping, POST /message. Used for ring or broadcast."""
from flask import Flask, request, jsonify
import socket

app = Flask(__name__)
counter = 0
messages = []


@app.route("/")
def root():
    global counter
    counter += 1
    return jsonify(team="team1", host=get_ip(), counter=counter)


@app.route("/ping")
def ping():
    return jsonify(status="pong")


@app.route("/message", methods=["POST"])
def message():
    data = request.get_json() or {}
    messages.append(data)
    return "", 200


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
