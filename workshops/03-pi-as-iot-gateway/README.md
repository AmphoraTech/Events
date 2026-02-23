# Workshop 3: Pi as IoT gateway — sensor to cloud

**Format:** 35 min theory + 1h25 hands-on + 15 min team presentations · **Hardware:** Raspberry Pi 3 per team · **Prize:** Pi for first end-to-end flow or best dashboard · **Total:** ~2h15

**Example files in this folder:** `sensor_sim.py`, `forwarder.py`

---

## Learning objectives

- Describe the role of an edge device: collect data, optionally process, send to cloud.
- Build a pipeline: simulated sensor → format → send (HTTP POST or Lambda).
- Optionally display the last value in a simple dashboard.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; pre-flash one SD image with Python 3 and `requests` (and optionally `paho-mqtt` if using MQTT).
- **Teams:** 2–3 people per team, one Pi per team.
- **Cloud:** One shared endpoint to receive telemetry (e.g. API Gateway + Lambda that stores last payload in DynamoDB or writes to S3, and optionally returns "last value" for the dashboard). Or a simple public "request bin" style URL for testing.

---

## Theory (35 min)

### 1. Edge devices and gateways (≈8 min)

- **Edge:** Device close to the "thing" (sensor, machine). Often resource-limited, may have intermittent connectivity.
- **Gateway:** Aggregates or forwards data from edge to cloud (or to another tier). The Pi here acts as gateway: it "has" the sensor (simulated) and sends data onward.
- **Why not send raw from sensor:** Formatting, batching, retry, security (e.g. TLS, API key) are easier on a Pi than on a tiny MCU.

### 2. Events and telemetry (≈7 min)

- **Telemetry:** Data about state or measurements (temperature, count, status). Often time-series: many small events over time.
- **When to run logic on device vs cloud:** Simple rules (e.g. "if temp > 40 then send alert") can run on Pi; heavy analytics or aggregation usually in cloud. Today we do minimal processing on Pi (format, maybe filter) and send to cloud.

### 3. Pipeline: sensor → format → send (≈5 min)

- **Structure:** Read sensor (or simulated output) → normalize (units, schema) → send (HTTP POST with JSON). Idempotency and timestamps help with duplicates and ordering.
- **Payload example:** `{"device_id": "pi-team1", "timestamp": "2025-02-23T10:00:00Z", "temperature": 22.5, "unit": "celsius"}`.

### 4. Why structure and idempotency matter (≈5 min)

- **Schema:** Same fields and types so the cloud can parse and store consistently.
- **Idempotency:** Sending the same event twice shouldn't create duplicate "actions"; use an id or timestamp so the backend can dedupe if needed.

### 5. Optional: dashboard (≈5 min)

### 6. Buffer / Q&A (≈5 min)

- **Idea:** A simple page that shows "last value received." Backend stores last payload; frontend polls (e.g. every 2 s) and updates the display. CORS must be allowed if the page is served from a different origin.

---

## Hands-on (1h25)

### Part 1: Simulated sensor (≈20 min)

**Goal:** Produce a stream of "sensor" readings on the Pi.

1. **Option A — file:** Use `sensor_sim.py` in this folder. Writes `timestamp,temperature` to `sensor_data.txt` every 5 seconds. Copy to Pi and run: `nohup python3 sensor_sim.py &` or in tmux/screen.
2. **Option B — MQTT (if broker available):** Publish to a topic with payload `{"temperature": 22.5, "timestamp": "..."}`.
3. **Run in background** so it keeps producing data.

**Handout:** "Part 1: Implement a simulated sensor that produces temperature (or another metric) every few seconds, either to a file or to MQTT."

### Part 2: Pipeline — read, format, POST (≈35 min)

**Goal:** Read the sensor output, format as JSON, POST to the cloud endpoint.

1. **Reader + POST:** Use `forwarder.py` in this folder. Set `URL` and `DEVICE_ID`; it reads `sensor_data.txt` and POSTs JSON every 30 seconds.
2. **Endpoint:** Facilitator provides URL (e.g. `POST https://xxx.execute-api.region.amazonaws.com/ingest`). Run periodically (loop or cron). Verify payloads arrive in cloud.

**Handout:** "Part 2: Build a script that reads your sensor output, formats it as JSON, and POSTs to the provided URL. Run it at least every 30–60 seconds."

### Part 3: Optional dashboard (≈35 min)

**Goal:** A minimal web page that shows the last value received by the cloud.

1. **Backend:** Add `GET /last` that returns the last stored payload. Enable CORS.
2. **Frontend:** Static HTML + JS: poll `GET <api-url>/last` every 2 s, update a `<div>` with latest temperature and timestamp.
3. **Prize angle:** "Best dashboard" or first team with end-to-end working.

**Handout:** "Part 3 (optional): Add a GET endpoint that returns the last value; build a small page that polls and displays it."

---

## Team presentations (15 min)

- **Goal:** Teams show their pipeline (sensor → POST) and optionally their dashboard.
- **Format:** 2–3 min per team: show one payload in the cloud or one dashboard view; one thing that worked, one thing they'd improve.
- **If many teams:** Pick 4–5 to present, or quick round: "who has data in the cloud? Who has a dashboard?"

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

- Add a simple "alert" in the Lambda: if temperature > 28, write to SNS or log "ALERT".
- Compare MQTT vs HTTP: latency, ease of many subscribers, reliability.
