# Workshop 6: “Event to action” — triggers and side effects on the Pi

**Format:** 30 min theory + 1h30 hands-on · **Hardware:** Raspberry Pi 3 per team (no extra hardware) · **Prize:** Pi for first cloud-triggered action or most creative trigger chain

---

## Learning objectives

- Map “event → function” to concrete actions: trigger (HTTP, cron, file) → action (write file, log, call API).
- Run a small web server on the Pi that performs an “action” when called.
- Chain triggers: local first (HTTP, cron, file), then optionally cloud (webhook/Lambda) → Pi → action.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; Raspberry Pi OS with Python 3 and Flask (or similar). No GPIO, LEDs, or breadboards.
- **Per team:** One Pi. Optional for cloud: API Gateway + Lambda that can call the Pi (e.g. HTTP to Pi’s IP or via ngrok/tunnel).

---

## Theory (30 min)

### 1. Event-driven: trigger → action (≈8 min)

- **Same idea as in software:** An event happens → a “handler” runs → an effect occurs. Here the effect is something the Pi does: write to a file, append to a log, call another URL, or run a command.
- **Triggers we’ll use:** HTTP request to the Pi, cron (time), file dropped in a folder, and optionally a cloud webhook that calls the Pi.
- **Why it’s useful:** Webhooks, automation, status endpoints (e.g. “when build finishes, hit this URL and the Pi logs it or forwards it”).

### 2. Actions without hardware (≈7 min)

- **File / log:** Append a timestamp and a message to a file. Easy to inspect and debug. “Action” = one line written.
- **HTTP out:** Call another API (e.g. Slack, a Lambda, or a request bin). “Action” = one request sent.
- **Command:** Run a script or shell command (e.g. `touch`, `echo`, or a custom script). Keep it simple and safe.
- **State:** Keep a simple “state” in a file (e.g. on/off, counter) and return it in the HTTP response. Lets you “toggle” or “increment” from the outside.

### 3. Same mental model as “event → function” (≈5 min)

- **In code:** Event (e.g. webhook) → Lambda/handler → response or side effect.
- **Here:** Event (HTTP/cron/file/cloud) → script on Pi → write file / call API / return state. The “function” is “do this action and return 200.”

### 4. Idempotency and safety (≈5 min)

- **Idempotency:** Calling the same endpoint twice with the same input should be safe (e.g. append is fine; overwrite might need care).
- **No secrets in URLs:** If the Pi is reachable from the internet (e.g. via tunnel), don’t put tokens in the path; use headers or body.

### 5. Optional: cloud trigger (≈5 min)

- **Idea:** Something in the cloud (e.g. Lambda invoked by API Gateway) sends an HTTP request to the Pi (or to a tunnel like ngrok that forwards to the Pi). Pi receives request → performs action (e.g. writes to log, calls another API) → returns 200. So “cloud event → Pi → action.”
- **Caveat:** Pi must be reachable (same network as caller, or tunnel). Ngrok/cloudflared can expose local port; use with care (short-lived URL, no secrets in URL).

---

## Hands-on (1h30)

### Part 1: Action via HTTP (≈35 min)

**Goal:** A small web server on the Pi that, when called (e.g. GET /on, GET /off or GET /trigger), performs an action and returns 200.

1. **State file:** Use a file (e.g. `/home/pi/state.txt`) to hold a simple value: `on` or `off`, or a counter. The server reads and optionally updates it.
2. **Routes:**  
   - **GET /on** — Write `on` (and timestamp) to the state file and/or append to a log file; return `{"status": "on"}`.  
   - **GET /off** — Write `off` (and timestamp); return `{"status": "off"}`.  
   - **GET /status** — Read the state file and return its contents (or last line).  
   Optional: **GET /toggle** — Flip on↔off and return new state.
3. **Code:** Use Flask (or similar). Example:
   ```python
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
   ```
4. **Run:** `python3 app.py`. Bind to 0.0.0.0. Test: `curl http://<pi-ip>:5000/on`, then `curl http://<pi-ip>:5000/status`.

**Handout:** “Part 1: Implement HTTP routes /on and /off that write state to a file and optionally log. Add /status that returns the current state. Test with curl.”

### Part 2: Trigger from cron or file (≈30 min)

**Goal:** Same “action” (e.g. write to log or update state), but triggered by time or by a file appearing.

1. **Cron:** Add a crontab entry that every minute (or every 2 minutes) calls the Pi’s own HTTP endpoint: `* * * * * curl -s http://127.0.0.1:5000/on` (or a script that appends a line to a log file). Emphasize: “event = time → action = request or write.”
2. **File trigger:** A folder `trigger/`. When a file appears (inotify or poll), run a script that appends “File: <filename>” to the log and optionally calls the Flask /on or /off. Emphasize: “event = file arrived → action = log + optional HTTP.”

**Handout:** “Part 2: Trigger the same action (a) every minute via cron (curl your /on or a script), and (b) when a file is dropped in trigger/ (inotify/watchdog → append to log or call your Flask app).”

### Part 3: Cloud-triggered action (≈25 min, optional)

**Goal:** An HTTP request from the internet (or from AWS) hits the Pi and triggers the action (write to log, update state, or call another API).

1. **Reachability:** If the Lambda (or tester) is on the same network as the Pi, call `http://<pi-ip>:5000/on` (or a custom route) directly. If not, use a tunnel: e.g. ngrok `ngrok http 5000` on the Pi, then call the provided HTTPS URL from Lambda or browser.
2. **Lambda:** Create a Lambda that does `requests.get("http://<pi-url>/on")` (or POST with a body). Trigger Lambda via API Gateway (e.g. GET /trigger). So: user or cron calls API → Lambda runs → Lambda calls Pi → Pi performs action.
3. **Demo:** Show “cloud event → Pi → action” (e.g. show log or state file updated) and submit for the prize.

**Prize:** Pi for first team with working cloud-triggered action, or for “most creative trigger chain” (e.g. MQTT + file + HTTP).

---

## Prep checklist

- [ ] **Pi image:** Raspberry Pi OS with Python 3 and Flask. No GPIO or hardware required.
- [ ] **Optional:** Ngrok or cloudflared for tunnel; API Gateway + Lambda that calls Pi or tunnel URL. Short handout with “how to get a public URL for your Pi” if using tunnels.

---

## Troubleshooting

- **Flask not reachable:** Run with `host="0.0.0.0"`; check firewall (port 5000).
- **Cloud can’t reach Pi:** Same network → use Pi IP. Different network → use tunnel (ngrok) and give Lambda the HTTPS URL.
- **Permission denied writing file:** Use a path the app can write to (e.g. `/home/pi/`); avoid `/root` unless running as root.

---

## If you have extra time

- Add a route that forwards the request body to another URL (e.g. Slack webhook) so “cloud → Pi → Slack.”
- Add a simple “counter” action: each call increments a number in a file; /status returns the count.
