# Workshop 4: Lightweight containers on Pi — “one box = one execution”

**Format:** 35 min theory + 1h25 hands-on + 15 min team presentations · **Hardware:** Raspberry Pi 3 per team · **Prize:** Pi for “smallest working image” or “most creative trigger” · **Total:** ~2h15

---

## Learning objectives

- Explain containers as isolated, repeatable units of work.
- Relate “one container run” to “one invocation” in serverless (e.g. Lambda).
- Run a small container on the Pi, trigger it via HTTP or file, and swap the “handler” by changing the image.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; use ARM-compatible images (linux/arm/v7 or arm32). Pre-flash base OS with Docker (or Podman) installed.
- **Teams:** 2–3 people per team, one Pi per team.
- **No cloud required.** Keep images small (Alpine-based) to avoid memory pressure.

---

## Theory (35 min)

### 1. Containers as units of work (≈8 min)

- **Definition:** Isolated environment (filesystem, process tree, network) that runs a defined process. Same image → same behavior.
- **Repeatable:** Build once, run anywhere (same arch). On the Pi we use ARM images.
- **Isolation:** Each run can be independent; no shared state unless you mount volumes or use network.

### 2. Relation to serverless (≈7 min)

- **Lambda:** One event → one invocation → one execution environment (conceptually a container) → exit. You don’t manage the box.
- **Pi + container:** One trigger (HTTP, file, cron) → `docker run` (or similar) → container runs, does work, exits. “One box = one execution” if you run a new container per trigger.
- **Contrast with long-lived server:** Here we don’t keep the container running; we start it on demand.

### 3. Why small images matter on Pi (≈5 min)

- **Resource limits:** Pi 3 has 1 GB RAM; large images (e.g. full Ubuntu) are slow to pull and run. Alpine or scratch-based images are better.
- **Fast start:** Smaller image + short-lived process = quick feedback. Closer to “function” experience.
- **Predictable:** Minimal attack surface and fewer moving parts.

### 4. Triggers we’ll use (≈5 min)

- **HTTP:** A web server on the Pi receives a request and runs `docker run <image>` (or `podman run`); the container’s stdout or a file can be the “response.”
- **File drop:** A file appears in a folder → script runs `docker run` with that file mounted or path passed as env.
- **Cron:** Every minute (or N minutes) run `docker run <image>` to simulate scheduled “jobs.”

### 5. ARM and image compatibility (≈5 min)

### 6. Buffer / Q&A (≈5 min)

- **Pi 3 is 32-bit ARM (armv7).** Use images tagged for `arm32v7` or `linux/arm/v7`. Many official images (Alpine, Python, Node) have ARM variants. If an image is amd64-only, it won’t run natively; use ARM-native base.

---

## Hands-on (1h25)

### Step 1: Minimal HTTP server in a container (≈25 min)

**Goal:** Build and run a container that, when started, serves HTTP and returns a simple response (e.g. “Hello” or current time).

1. **Dockerfile (Alpine + one-liner):** Example using Python:
   ```dockerfile
   FROM arm32v7/python:3-alpine
   WORKDIR /app
   RUN pip install --no-cache-dir flask
   COPY app.py .
   CMD ["python", "app.py"]
   ```
   With `app.py` that runs Flask on 0.0.0.0:5000 and returns `{"message": "hello"}` on GET `/`. Or use `arm32v7/alpine` and a static file served by `busybox httpd` if you prefer no Python.
2. **Build on Pi:** `docker build -t myhandler .` (in the directory with Dockerfile and app.py). Run: `docker run --rm -p 5000:5000 myhandler`. From another machine: `curl http://<pi-ip>:5000/`.
3. **Emphasize:** This container is “the handler.” We’ll trigger it in different ways next.

**Handout:** “Step 1: Create a minimal Docker image (Alpine-based) that runs a tiny HTTP server. Build and run it on your Pi and verify with curl.”

### Step 2: Trigger by HTTP — proxy or run-on-request (≈25 min)

**Goal:** When someone calls the Pi (e.g. GET /run), the Pi runs the container and returns the result.

1. **Option A — proxy:** Run the container long-lived (as in Step 1); Nginx or a small Flask app on the Pi proxies /run to the container. Response = container output.
2. **Option B — run on request:** Don’t keep the container running. Run a small Flask app on the Pi that, on GET /run, runs `docker run --rm myhandler` (or `podman run --rm myhandler`) and captures stdout; return that as the HTTP response. Container starts, serves one “logical” request, exits. This is the “one trigger = one execution” model.
3. **Implement Option B:** Handler script runs the container; container can print JSON to stdout; Flask captures and returns it. Example: `result = subprocess.run(["docker", "run", "--rm", "myhandler"], capture_output=True, text=True)` then return `result.stdout` with status 200.

**Handout:** “Step 2: When your Pi receives GET /run, run the container once (docker run --rm), capture its output, and return it as the HTTP response.”

### Step 3: Trigger by file or cron (≈25 min)

**Goal:** Run the same container when a file appears or on a schedule.

1. **File trigger:** Create a folder `inbox/`. When a file appears (inotify or poll every 10 s), run `docker run --rm -v /home/pi/inbox:/inbox myhandler` (or pass file path via env). Container reads from /inbox, does something (e.g. echo file list), exits. Script moves or deletes the file after run to avoid re-triggering.
2. **Cron trigger:** Add crontab: `* * * * * docker run --rm myhandler >> /home/pi/cron.log 2>&1`. Every minute the container runs once. Check log to confirm.
3. **Compare:** Same image, different triggers — like Lambda with API Gateway vs EventBridge schedule.

**Handout:** “Step 3: Trigger the same container (a) when a file is dropped in inbox/, and (b) every minute via cron. Reuse the same image.”

### Step 4: Swap the handler (≈15 min)

**Goal:** Change behavior by swapping the image; trigger stays the same.

1. **Second image:** Build another Dockerfile (e.g. returns `{"message": "goodbye"}` or writes to a file). Tag as `myhandler2`.
2. **Change the trigger script:** Point “run on request” (and optionally cron) to `myhandler2` instead of `myhandler`. Same trigger, different “function.”
3. **Optional:** Run 2–3 containers in sequence or compare resource usage: `docker stats` during a run to see CPU/memory.

**Prize:** “Smallest working image” (e.g. smallest `docker images` size that still passes the trigger test) or “most creative trigger” (e.g. MQTT, file drop, or another idea).

---

## Team presentations (15 min)

- **Goal:** Teams show their container trigger (HTTP, file, or cron) and optionally image size or “handler swap.”
- **Format:** 2–3 min per team: demo one trigger in action; mention image size or creative trigger if applicable.
- **If many teams:** Pick 4–5 to present, or quick round: “who has run-on-request working? Who tried file trigger?”

---

## Example Dockerfile and app (minimal)

```dockerfile
# Dockerfile
FROM arm32v7/python:3-alpine
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

```python
# app.py
from flask import Flask, jsonify
from datetime import datetime
app = Flask(__name__)
@app.route("/")
def root():
    return jsonify(message="hello", time=datetime.utcnow().isoformat())
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

For “run on request” you might use a container that prints one line and exits (e.g. `echo '{"ok":true}'`) instead of Flask, so the Pi script can run it with `docker run --rm` and return stdout quickly.

---

## Prep checklist

- [ ] **Pi image:** Raspberry Pi OS with Docker (or Podman) and ARM architecture; `docker pull arm32v7/alpine` works.
- [ ] **Network:** Pis can pull images (or pre-pull base images to save time).
- [ ] **Handout:** Step 1–4 instructions; note on ARM (use arm32v7 or linux/arm/v7); reminder to keep images small.
- [ ] **Scoring (optional):** How to measure “smallest image” (e.g. `docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}"`).

---

## Troubleshooting

- **Image not found / wrong arch:** Ensure Dockerfile FROM uses an ARM base (e.g. `arm32v7/python:3-alpine`). Avoid amd64-only images.
- **Out of memory:** Limit container memory: `docker run --memory=128m ...`. Close other heavy processes on the Pi.
- **Container exits immediately:** If using Flask, ensure it’s bound to 0.0.0.0 and the Pi script that runs the container either proxies to the container’s port or uses a single-run script that prints and exits.

---

## If you have extra time

- Add a second container that “chains”: trigger 1 runs container A, which writes to a file; trigger 2 (file or cron) runs container B that reads that file.
- Compare `docker run` vs `docker compose run` for one-off jobs.
