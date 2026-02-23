# Workshop 6: "Event to action" — triggers and side effects on the Pi

**Format:** 35 min theory + 1h25 hands-on + 15 min team presentations · **Hardware:** Raspberry Pi 3 per team (no extra hardware) · **Prize:** Pi for first cloud-triggered action or most creative trigger chain · **Total:** ~2h15

**Example files in this folder:** `app.py`

---

## Learning objectives

- Map "event → function" to concrete actions: trigger (HTTP, cron, file) → action (write file, log, call API).
- Run a small web server on the Pi that performs an "action" when called.
- Chain triggers: local first (HTTP, cron, file), then optionally cloud (webhook/Lambda) → Pi → action.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; Raspberry Pi OS with Python 3 and Flask (or similar). No GPIO, LEDs, or breadboards.
- **Per team:** One Pi. Optional for cloud: API Gateway + Lambda that can call the Pi (e.g. HTTP to Pi's IP or via ngrok/tunnel).

---

## Theory (35 min)

### 1. Event-driven: trigger → action (≈8 min)

- **Same idea as in software:** An event happens → a "handler" runs → an effect occurs. Here the effect is something the Pi does: write to a file, append to a log, call another URL, or run a command.
- **Triggers we'll use:** HTTP request to the Pi, cron (time), file dropped in a folder, and optionally a cloud webhook that calls the Pi.
- **Why it's useful:** Webhooks, automation, status endpoints (e.g. "when build finishes, hit this URL and the Pi logs it or forwards it").

### 2. Actions without hardware (≈7 min)

- **File / log:** Append a timestamp and a message to a file. Easy to inspect and debug. "Action" = one line written.
- **HTTP out:** Call another API (e.g. Slack, a Lambda, or a request bin). "Action" = one request sent.
- **Command:** Run a script or shell command (e.g. `touch`, `echo`, or a custom script). Keep it simple and safe.
- **State:** Keep a simple "state" in a file (e.g. on/off, counter) and return it in the HTTP response. Lets you "toggle" or "increment" from the outside.

### 3. Same mental model as "event → function" (≈5 min)

- **In code:** Event (e.g. webhook) → Lambda/handler → response or side effect.
- **Here:** Event (HTTP/cron/file/cloud) → script on Pi → write file / call API / return state. The "function" is "do this action and return 200."

### 4. Idempotency and safety (≈5 min)

- **Idempotency:** Calling the same endpoint twice with the same input should be safe (e.g. append is fine; overwrite might need care).
- **No secrets in URLs:** If the Pi is reachable from the internet (e.g. via tunnel), don't put tokens in the path; use headers or body.

### 5. Optional: cloud trigger (≈5 min)

### 6. Buffer / Q&A (≈5 min)

- **Idea:** Something in the cloud (e.g. Lambda invoked by API Gateway) sends an HTTP request to the Pi (or to a tunnel like ngrok). Pi receives request → performs action (e.g. writes to log, calls another API) → returns 200. So "cloud event → Pi → action."
- **Caveat:** Pi must be reachable (same network as caller, or tunnel). Use short-lived URL; no secrets in URL.

---

## Hands-on (1h25)

### Part 1: Action via HTTP (≈35 min)

**Goal:** A small web server on the Pi that, when called (e.g. GET /on, GET /off), performs an action and returns 200.

1. **State file:** Use a file (e.g. `/home/pi/state.txt`) to hold `on` or `off`; server reads and updates it.
2. **Routes:** GET /on, GET /off, GET /status. Use `app.py` in this folder — copy to the Pi and run `python3 app.py`. Adjust paths (STATE_FILE, LOG_FILE) if needed (e.g. use current directory).
3. **Test:** `curl http://<pi-ip>:5000/on`, then `curl http://<pi-ip>:5000/status`.

**Handout:** "Part 1: Implement HTTP routes /on and /off that write state to a file and optionally log. Add /status that returns the current state. Test with curl."

### Part 2: Trigger from cron or file (≈30 min)

**Goal:** Same "action" (write to log or update state), but triggered by time or by a file appearing.

1. **Cron:** `* * * * * curl -s http://127.0.0.1:5000/on` (or a script that appends to a log file).
2. **File trigger:** Folder `trigger/`. When a file appears (inotify or poll), run a script that appends "File: <filename>" to the log and optionally calls Flask /on or /off.

**Handout:** "Part 2: Trigger the same action (a) every minute via cron (curl your /on or a script), and (b) when a file is dropped in trigger/ (inotify/watchdog → append to log or call your Flask app)."

### Part 3: Cloud-triggered action (≈25 min, optional)

**Goal:** An HTTP request from the internet (or from AWS) hits the Pi and triggers the action.

1. **Reachability:** Same network → use Pi IP. Different network → use tunnel (e.g. ngrok `ngrok http 5000`).
2. **Lambda:** Create a Lambda that does `requests.get("http://<pi-url>/on")`. Trigger Lambda via API Gateway (e.g. GET /trigger). So: user or cron calls API → Lambda runs → Lambda calls Pi → Pi performs action.
3. **Demo:** Show "cloud event → Pi → action" (e.g. show log or state file updated).

**Prize:** Pi for first team with working cloud-triggered action, or for "most creative trigger chain" (e.g. MQTT + file + HTTP).

---

## Team presentations (15 min)

- **Goal:** Teams show their trigger chain (HTTP, cron, file, or cloud) and the resulting action (log, state file, or API call).
- **Format:** 2–3 min per team: demo one trigger; show log or state file. One thing that worked, one thing they'd add.
- **If many teams:** Pick 4–5 to present, or quick round: "who got cloud trigger working?"

---

## Prep checklist

- [ ] **Pi image:** Raspberry Pi OS with Python 3 and Flask. No GPIO or hardware required.
- [ ] **Optional:** Ngrok or cloudflared for tunnel; API Gateway + Lambda that calls Pi or tunnel URL. Short handout with "how to get a public URL for your Pi" if using tunnels.

---

## Troubleshooting

- **Flask not reachable:** Run with `host="0.0.0.0"`; check firewall (port 5000).
- **Cloud can't reach Pi:** Same network → use Pi IP. Different network → use tunnel (ngrok) and give Lambda the HTTPS URL.
- **Permission denied writing file:** Use a path the app can write to (e.g. `/home/pi/` or current directory); avoid `/root` unless running as root.

---

## If you have extra time

- Add a route that forwards the request body to another URL (e.g. Slack webhook) so "cloud → Pi → Slack."
- Add a simple "counter" action: each call increments a number in a file; /status returns the count.
