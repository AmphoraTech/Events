# Workshop 3: Pi as IoT gateway — sensor to cloud

**Format:** 35 min theory + 1h25 hands-on + 15 min team presentations · **Hardware:** Raspberry Pi 3 per team · **Prize:** Pi for first end-to-end flow or best dashboard · **Total:** ~2h15

---

## Learning objectives

- Describe the role of an edge device: collect data, optionally process, send to cloud.
- Build a pipeline: simulated sensor → format → send (HTTP POST or Lambda).
- Optionally display the last value in a simple dashboard.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; pre-flash one SD image with Python 3 and `requests` (and optionally `paho-mqtt` if using MQTT).
- **Teams:** 2–3 people per team, one Pi per team.
- **Cloud:** One shared endpoint to receive telemetry (e.g. API Gateway + Lambda that stores last payload in DynamoDB or writes to S3, and optionally returns “last value” for the dashboard). Or a simple public “request bin” style URL for testing.

---

## Theory (35 min)

### 1. Edge devices and gateways (≈8 min)

- **Edge:** Device close to the “thing” (sensor, machine). Often resource-limited, may have intermittent connectivity.
- **Gateway:** Aggregates or forwards data from edge to cloud (or to another tier). The Pi here acts as gateway: it “has” the sensor (simulated) and sends data onward.
- **Why not send raw from sensor:** Formatting, batching, retry, security (e.g. TLS, API key) are easier on a Pi than on a tiny MCU.

### 2. Events and telemetry (≈7 min)

- **Telemetry:** Data about state or measurements (temperature, count, status). Often time-series: many small events over time.
- **When to run logic on device vs cloud:** Simple rules (e.g. “if temp > 40 then send alert”) can run on Pi; heavy analytics or aggregation usually in cloud. Today we do minimal processing on Pi (format, maybe filter) and send to cloud.

### 3. Pipeline: sensor → format → send (≈5 min)

- **Structure:** Read sensor (or simulated output) → normalize (units, schema) → send (HTTP POST with JSON). Idempotency and timestamps help with duplicates and ordering.
- **Payload example:** `{"device_id": "pi-team1", "timestamp": "2025-02-23T10:00:00Z", "temperature": 22.5, "unit": "celsius"}`.

### 4. Why structure and idempotency matter (≈5 min)

- **Schema:** Same fields and types so the cloud can parse and store consistently.
- **Idempotency:** Sending the same event twice shouldn’t create duplicate “actions”; use an id or timestamp so the backend can dedupe if needed.

### 5. Optional: dashboard (≈5 min)

### 6. Buffer / Q&A (≈5 min)

- **Idea:** A simple page that shows “last value received.” Backend stores last payload; frontend polls (e.g. every 2 s) and updates the display. CORS must be allowed if the page is served from a different origin.

---

## Hands-on (1h25)

### Part 1: Simulated sensor (≈20 min)

**Goal:** Produce a stream of “sensor” readings on the Pi.

1. **Option A — file:** A script that every N seconds (e.g. 5) writes a line to a file, e.g. `sensor_data.txt`: `timestamp,temperature` with a random temp (e.g. 18–28°C) or read from `/sys/class/thermal/thermal_zone0/temp` (CPU temp) and convert.
2. **Option B — MQTT (if broker available):** Publish to a topic, e.g. `sensors/team1/temperature`, with payload `{"temperature": 22.5, "timestamp": "..."}`. Other teams can share the broker.
3. **Run in background:** `nohup python3 sensor_sim.py &` or run in a `tmux`/`screen` session.

**Handout:** “Part 1: Implement a simulated sensor that produces temperature (or another metric) every few seconds, either to a file or to MQTT.”

### Part 2: Pipeline — read, format, POST (≈35 min)

**Goal:** Read the sensor output, format as JSON, POST to the cloud endpoint.

1. **Reader:** Script that reads the latest line from the file (or subscribes to MQTT) and builds a payload:
   - `device_id` (e.g. team name or Pi hostname),
   - `timestamp` (ISO UTC),
   - `temperature` (or chosen metric),
   - optional `unit`.
2. **POST:** Use `requests.post(url, json=payload, headers={"Content-Type": "application/json"})`. Handle errors (log and optionally retry once).
3. **Endpoint:** Facilitator provides URL and (if needed) an API key header. Example: `POST https://xxx.execute-api.region.amazonaws.com/ingest` with body `{"device_id": "team1", "timestamp": "...", "temperature": 22.5}`.
4. **Run periodically:** Cron every minute or a loop with `time.sleep(30)` so the Pi keeps sending. Verify in cloud (e.g. CloudWatch Logs, DynamoDB, or request bin) that payloads arrive.

**Handout:** “Part 2: Build a script that reads your sensor output, formats it as JSON, and POSTs to the provided URL. Run it at least every 30–60 seconds.”

### Part 3: Optional dashboard (≈35 min)

**Goal:** A minimal web page that shows the last value received by the cloud.

1. **Backend:** If you control the Lambda/API: add a `GET /last` (or similar) that returns the last stored payload. Enable CORS for the frontend origin.
2. **Frontend:** Static HTML + JS: every 2 seconds call `GET <api-url>/last`, parse JSON, update a `<div>` with the latest temperature (and timestamp). No framework required; host on any static server or open the HTML file and point to the API (mind CORS if file://).
3. **Prize angle:** “Best dashboard” can mean clearest display, or first team with end-to-end (sensor → cloud → dashboard) working.

**Handout:** “Part 3 (optional): Add a GET endpoint that returns the last value; build a small page that polls and displays it.”

---

## Team presentations (15 min)

- **Goal:** Teams show their pipeline (sensor → POST) and optionally their dashboard.
- **Format:** 2–3 min per team: show one payload in the cloud or one dashboard view; one thing that worked, one thing they’d improve.
- **If many teams:** Pick 4–5 to present, or quick round: “who has data in the cloud? Who has a dashboard?”

---

## Example code snippets

### Simulated sensor (file output)

```python
# sensor_sim.py
import time, random
from datetime import datetime

while True:
    temp = round(18 + random.random() * 10, 1)
    with open("/home/pi/sensor_data.txt", "w") as f:
        f.write(f"{datetime.utcnow().isoformat()},{temp}\n")
    time.sleep(5)
```

### Reader and POST

```python
# forwarder.py
import requests, time
from datetime import datetime

URL = "https://YOUR_API_ENDPOINT/ingest"
DEVICE_ID = "team1"

while True:
    try:
        with open("/home/pi/sensor_data.txt") as f:
            line = f.readline().strip()
        ts, temp = line.split(",")
        payload = {"device_id": DEVICE_ID, "timestamp": ts, "temperature": float(temp), "unit": "celsius"}
        r = requests.post(URL, json=payload, timeout=5)
        print(r.status_code, payload)
    except Exception as e:
        print("Error", e)
    time.sleep(30)
```

---

## Prep checklist

- [ ] **Pi image:** Python 3, `requests`; optional: `paho-mqtt` if using MQTT.
- [ ] **Cloud endpoint:** API Gateway + Lambda that accepts POST, stores last payload (e.g. in Lambda env or DynamoDB), and optionally exposes GET /last. CORS enabled for dashboard.
- [ ] **Handout:** Endpoint URL, expected JSON shape, and (if used) API key or header.
- [ ] **Optional:** MQTT broker (e.g. Mosquitto on a central Pi or cloud); topic naming convention.

---

## Troubleshooting

- **POST 403/401:** Check API key or IAM; CORS is for browser, not for Pi.
- **No data in cloud:** Check Lambda logs; ensure Pi can reach the URL (curl from Pi); check JSON encoding.
- **Dashboard CORS:** If opening HTML from file://, browser may block; use a simple HTTP server (e.g. `python -m http.server`) and allow that origin in API Gateway CORS.

---

## If you have extra time

- Add a simple “alert” in the Lambda: if temperature > 28, write to SNS or log “ALERT”.
- Compare MQTT vs HTTP: latency, ease of many subscribers, reliability.
