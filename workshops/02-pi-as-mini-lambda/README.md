# Workshop 2: Pi as "mini Lambda" — event-driven to AWS

**Format:** 35 min theory + 1h25 hands-on + 15 min team presentations · **Hardware:** Raspberry Pi 3 per team · **Prize:** Pi for "first Lambda deployed" or "cleanest design" · **Total:** ~2h15

**Example files in this folder:** `handler.py`, `app.py`, `lambda_function.py`

---

## Learning objectives

- Explain event-driven execution: one event triggers one unit of work.
- Run "functions" on the Pi triggered by HTTP, cron, and file events.
- Deploy the same logical "function" as an AWS Lambda and compare Pi vs cloud.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; pre-flash one SD image with Python 3, Flask, and `inotify` support (e.g. `pip install flask pyinotify` or `watchdog`).
- **Teams:** 2–3 people per team, one Pi per team.
- **Optional:** AWS accounts (or one shared account with IAM roles); AWS CLI and SAM CLI or Serverless Framework on a laptop, or use Lambda console.

---

## Theory (35 min)

### 1. Event-driven execution (≈8 min)

- **Idea:** Something happens (HTTP request, file appears, time passes) → one unit of code runs → exits. No long-lived "server process" that waits forever; each run is triggered.
- **Contrast:** Traditional server = process always running, handling many requests. Function = process starts on event, handles that event, then stops (conceptually).
- **Benefits:** Scale by number of events; pay (or use resources) per execution; clear mental model "event in → result out."

### 2. From script on a machine to function in the cloud (≈7 min)

- **On the Pi:** A script or small web app that runs when you call it (HTTP) or when cron fires or when a file appears. You own the machine and the runtime.
- **In AWS Lambda:** You provide the code; AWS runs it when an event occurs (HTTP via API Gateway, schedule, S3, etc.). You don't manage OS or capacity.
- **Same mental model:** Event → handler code → response or side effect.

### 3. Use cases (≈5 min)

- **Webhooks:** External service calls your URL → your function runs → does something (e.g. update DB, send message).
- **Cron-style:** Run every minute/hour (EventBridge rule or cron on Pi) to do a task (e.g. backup, cleanup).
- **API handlers:** One URL or path = one logical "action"; good fit for functions.

### 4. Triggers we'll use today (≈5 min)

- **HTTP:** Request to the Pi (e.g. `GET /run`) runs the handler and returns a response.
- **File:** A file dropped in a folder triggers a script (inotify or poll).
- **Schedule:** Cron on Pi; in AWS, EventBridge (CloudWatch Events) for Lambda.

### 5. Quick Lambda overview (≈5 min)

### 6. Buffer / Q&A (≈5 min)

- **What Lambda is:** Run code in response to events; no server to manage; pay per invocation and duration.
- **Typical trigger:** API Gateway HTTP, S3 upload, schedule, SQS. We'll use API Gateway HTTP.
- **Limits:** Timeout, memory, deployment package size — keep the first function simple.

---

## Hands-on (1h25)

### Exercise 1: HTTP- and cron-triggered "function" on the Pi (≈30 min)

**Goal:** Run a small "function" when something triggers it; emphasize "one event → one execution."

1. **Handler script:** Use `handler.py` in this folder (writes current time to `last_run.txt`, prints OK). Copy to the Pi (e.g. `/home/pi/handler.py`).
2. **Trigger by HTTP:** Use `app.py` in this folder — `GET /run` runs the handler logic. Run: `flask run --host=0.0.0.0 --port=5000` or `python3 app.py`.
3. **Trigger by cron:** `* * * * * /usr/bin/python3 /home/pi/handler.py >> /home/pi/cron.log 2>&1`.
4. **Verify:** `curl http://<pi-ip>:5000/run` and check `last_run.txt`; wait a minute and check cron updated it too.

**Handout:** "Exercise 1: Implement a handler that runs on HTTP GET /run and on a 1-minute cron. Prove both triggers update a 'last run' file."

### Exercise 2: File-drop trigger (≈30 min)

**Goal:** Run the "function" when a file appears in a folder (event-driven, no polling in code if possible).

1. **Input folder:** e.g. `/home/pi/inbox`.
2. **Watch the folder:** Use `watchdog` (`pip install watchdog`). Script that watches `inbox/` and when a new file is created, runs the handler (e.g. append filename to a log and move file to `processed/`).
3. **Test:** `echo hello > inbox/test.txt`; confirm handler ran.

**Handout:** "Exercise 2: When a file is dropped in `inbox/`, run your handler (e.g. log the filename and move the file). Use inotify/watchdog, not a tight poll loop."

### Exercise 3: Same idea in AWS Lambda (≈30 min)

**Goal:** Deploy a Lambda that does the same "job" and invoke it via HTTP.

1. **Template:** Use `lambda_function.py` in this folder. Returns `{"status": "ok", "timestamp": "<utc-now>"}`. Use API Gateway HTTP API or REST API to trigger it.
2. **Deploy:** SAM, Serverless Framework, or manual zip upload + API Gateway. Document one path for participants.
3. **Invoke:** `curl https://<api-id>.execute-api.<region>.amazonaws.com/run`. Compare with Pi.

**Handout:** "Exercise 3: Deploy the same logical function as AWS Lambda behind API Gateway. Invoke it with curl and compare with your Pi."

**Prize:** Pi for first team with a working Lambda invocation, or for "cleanest design" (judged by facilitator).

---

## Team presentations (15 min)

- **Goal:** Teams show their Pi "function" and/or their deployed Lambda.
- **Format:** 2–3 min per team: demo HTTP/cron trigger on the Pi, then the same idea in Lambda (curl or browser). One thing that worked, one gotcha.
- **If many teams:** Pick 4–5 to present, or quick round: "who got Lambda deployed? Show the URL."

---

## Prep checklist

- [ ] **Pi image:** Python 3, Flask, `watchdog` or `pyinotify`; optional: cron pre-configured with a placeholder.
- [ ] **Network:** All Pis reachable (WiFi, same subnet); document Pi IPs for testing from laptops.
- [ ] **Lambda template:** Zip with `lambda_function.py` or SAM/serverless template; instructions for creating API Gateway and linking to Lambda.
- [ ] **AWS:** Account(s) or shared account; IAM role for Lambda (basic execution role); optional: SAM CLI / Serverless CLI on facilitator laptop.
- [ ] **Handouts:** Step-by-step for Exercise 1–3; API Gateway URL format; how to submit "done" (e.g. paste curl output).

---

## Troubleshooting

- **Flask not reachable from another machine:** Run with `host="0.0.0.0"`; check firewall (e.g. `ufw allow 5000` if ufw is used).
- **Cron not running:** Check crontab with `crontab -l`; use full paths; check `/home/pi/cron.log` for errors.
- **inotify not firing:** Ensure directory exists and process has write access; on some NFS/network fs, inotify may not work — use local directory on Pi.
- **Lambda timeout/permission:** Increase timeout a few seconds; ensure Lambda execution role has CloudWatch Logs; check API Gateway integration (proxy vs non-proxy).

---

## If you have extra time

- Add a second Lambda trigger: e.g. S3 upload or EventBridge schedule, and compare with cron/file on Pi.
- Discuss cold start: first Lambda invocation may be slower; relate to "no always-on process."
