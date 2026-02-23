# Workshop 7: Tiny “distributed system” — Pis talking to each other

**Format:** 35 min theory + 1h25 hands-on + 15 min team presentations · **Hardware:** Raspberry Pi 3 per team · **Prize:** Pi for first team with full “ring” or “broadcast” working · **Total:** ~2h15

---

## Learning objectives

- Expose a minimal HTTP “service” on the Pi and call other Pis’ services.
- Implement simple coordination: call a neighbour, or pass a message along a ring / broadcast to all.
- Observe failure: one Pi unplugged or stopped and how that affects the system.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; pre-flash one SD image with Python 3, Flask, and `requests` (or another HTTP client).
- **Teams:** 2–3 people per team, one Pi per team.
- **Network:** All Pis on same VLAN; each Pi has a known IP (static or DHCP reservation). Facilitator provides a roster: team name ↔ Pi IP.

---

## Theory (35 min)

### 1. Services and APIs (≈8 min)

- **Service:** A process that listens for requests and responds. Here: HTTP server on the Pi that returns JSON or plain text.
- **API:** The “contract”: which URLs, which methods (GET/POST), what request/response shape. We keep it trivial: GET / returns identity and maybe a counter; POST /ping might accept a body and forward it.
- **Calling each other:** Each team’s Pi has an IP. From Pi A, you can `requests.get("http://<Pi-B-IP>/")` so “nodes” talk over HTTP.

### 2. Simple coordination (≈7 min)

- **No heavy theory:** Just “several nodes that need to cooperate.” Two patterns we’ll use:
  - **Ring:** Node 1 → Node 2 → Node 3 → … → Node N → Node 1. A message is passed along; each node forwards to “next” in the list.
  - **Broadcast (simplified):** One node sends to all others (e.g. GET each IP in the roster); or “broadcast” by passing through each node in sequence so everyone sees the message once.
- **Leader election:** Optional: “who is leader?” — e.g. smallest IP or first to respond. We can skip or do a very simple rule (e.g. “leader = Pi with lowest IP”).

### 3. Discovery and roster (≈5 min)

- **Roster:** A list of (team name, Pi IP). Handed out at the start so teams know where to send requests. Alternative: mDNS so Pis find each other by hostname (e.g. `pi-team1.local`); more setup.
- **Discovery:** In a real system you’d use service discovery (DNS, Consul, etc.). Today we keep it simple: static roster.

### 4. Failure (≈5 min)

- **One node down:** If we form a ring and one Pi is off or unreachable, the “next” call will fail (timeout or connection error). Observing this is part of the exercise.
- **Handling:** Timeouts, retries, or “skip and continue” — we’ll discuss after the hands-on. No need to implement full fault tolerance; just see what breaks.

### 5. What “working” means (≈5 min)

### 6. Buffer / Q&A (≈5 min)

- **Minimal service:** GET / returns something (e.g. `{"team": "A", "counter": 0}`). Optional: POST /ping with body that gets forwarded.
- **Ring:** A message (e.g. a token string) is passed from Pi 1 → 2 → 3 → … → N → 1. Each node receives, logs or increments, sends to next. “Working” = full round-trip without crash.
- **Broadcast:** One node sends the same message to every other node (each does GET or POST); all receive it. “Working” = every node got the message once.

---

## Hands-on (1h25)

### Step 1: Minimal service on each Pi (≈25 min)

**Goal:** Each team runs an HTTP server on their Pi that identifies the node and (optionally) holds a counter.

1. **Endpoints:**
   - **GET /** — Returns JSON: `{"team": "<name>", "host": "<pi-ip>", "counter": <n>}`. Counter can start at 0 and increment on each GET (or stay 0 for now).
   - **GET /ping** — Returns `{"status": "pong"}`. Used by others to check liveness.
   - **POST /message** (optional) — Accepts JSON body `{"from": "<ip>", "payload": "..."}`. Appends to a log in memory or file and returns 200. Used for ring/broadcast.
2. **Run:** Flask on port 5000, bind 0.0.0.0. Store counter and (if implemented) message log in process memory or a small file.
3. **Test:** From another machine or Pi, `curl http://<pi-ip>:5000/` and `curl http://<pi-ip>:5000/ping`.

**Handout:** “Step 1: Implement GET / (identity + counter), GET /ping (pong), and optionally POST /message (accept and log a message). Run on port 5000.”

### Step 2: Call each other (≈20 min)

**Goal:** Using the roster, each team’s Pi calls every other Pi’s /ping (or GET /).

1. **Roster:** Facilitator gives a list: Team A = 192.168.10.11, Team B = 192.168.10.12, …
2. **Script or manual:** From Pi A, run `requests.get("http://192.168.10.12:5000/ping")` for each other IP. Collect responses (success/failure, latency). This proves “Pis talking to each other.”
3. **Optional:** Build a simple “dashboard” that GETs each Pi’s / and displays team name and counter in a list.

**Handout:** “Step 2: Using the roster, from your Pi call every other Pi’s /ping (or GET /). Record which respond and any errors.”

### Step 3: Ring or broadcast (≈35 min)

**Goal:** Implement either a ring (message passes 1→2→3→…→N→1) or a broadcast (one node sends to all).

**Ring:**

1. **Order:** Define order (e.g. by IP: .11 → .12 → .13 → … → .11). Each node knows “next” IP from the roster.
2. **Token:** A string (e.g. `"ring-token-1"`). Node 1 POSTs to Node 2’s /message with `{"from": "192.168.10.11", "payload": "ring-token-1"}`. Node 2 receives, logs, then POSTs to Node 3 with same or updated payload. Continue until the token comes back to Node 1.
3. **Success:** Token completes a full round; every node logged it once. **Prize:** First team to demonstrate a full round wins (or each team demonstrates their node’s part in the ring).

**Broadcast:**

1. **One sender:** One designated Pi (e.g. lowest IP) sends the same message to every other Pi via POST /message (or GET with query param). Each recipient logs it.
2. **Success:** All nodes have the message in their log. **Prize:** First team with “all nodes received” wins.

**Handout:** “Step 3: Implement the ring (message passes along the roster until it returns to sender) or broadcast (one node sends to all). Demonstrate a full round or full broadcast.”

### Step 4: Failure (≈10 min)

- **Unplug or stop one Pi** (or stop its Flask process). Run the ring or broadcast again. Observe: timeouts, missing log entries, “next” node unreachable.
- **Debrief:** What would you do in production? (Timeouts, retries, circuit breaker, skip node, etc.) No implementation required; just discussion.

**Prize:** Pi for first team with full ring or full broadcast working (facilitator verifies by checking logs or watching a demo).

---

## Team presentations (15 min)

- **Goal:** Teams show their service, their “call each other” flow, and optionally the ring or broadcast in action.
- **Format:** 2–3 min per team: demo GET / or /ping from another Pi; if they did ring/broadcast, show one round. One thing that broke, one thing they’d do next.
- **If many teams:** Pick 4–5 to present, or quick round: “who has the ring working? Show the token going round.”

---

## Example code snippets

### Minimal Flask service

```python
# service.py
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
```

### Ring: send to next node

```python
# ring_send.py
import requests
import sys

MY_IP = "192.168.10.11"   # this Pi
NEXT_IP = "192.168.10.12" # next in ring
payload = {"from": MY_IP, "payload": "ring-token-1"}
r = requests.post(f"http://{NEXT_IP}:5000/message", json=payload, timeout=5)
print(r.status_code)
```

Each node would have its own NEXT_IP; the last node in the ring points back to the first.

---

## Prep checklist

- [ ] **Pi image:** Python 3, Flask, requests. Port 5000 open (no firewall block).
- [ ] **Network:** One VLAN; static IPs or DHCP reservations so roster is stable.
- [ ] **Roster:** Print or share a table: Team name, Pi IP. Include “next” for ring (e.g. Team A → Team B → Team C → Team A).
- [ ] **Handout:** Step 1–4; roster; definition of “ring” and “broadcast”; how to demonstrate (e.g. show logs or run once with facilitator watching).

---

## Troubleshooting

- **Connection refused:** Ensure Flask is bound to 0.0.0.0 and port 5000; check firewall; ping the other Pi first.
- **Wrong “next” in ring:** Double-check roster order; last node must point to first for a closed ring.
- **Timeout:** Increase timeout in requests (e.g. 10 s); if a Pi is slow or down, ring will hang at that node — good moment to discuss failure.

---

## If you have extra time

- **Leader election:** Each node GETs all others; “leader” = smallest IP that responded. Display “I am leader” or “Leader is X” on a simple page.
- **Structured broadcast:** One node POSTs to all; each recipient adds its ID to the payload and forwards to the next until the initiator gets back a “visited” list (everyone saw the message).
