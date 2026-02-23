"""Flask app: GET /run runs the handler logic and returns JSON."""
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/run")
def run():
    with open("/home/pi/last_run.txt", "w") as f:
        f.write(datetime.utcnow().isoformat())
    return jsonify(status="ok", timestamp=datetime.utcnow().isoformat())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
