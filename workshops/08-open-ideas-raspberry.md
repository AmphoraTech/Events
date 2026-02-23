# Workshop 8: Open ideas with Raspberry Pi

**Format:** 30 min presentation + 45 min kickstart + 2h tinkering · **Hardware:** Raspberry Pi 3 per team · **Prize:** Optional (e.g. Pi for “most creative”, “best demo”, or raffle)

---

## Format overview

| Block | Duration | Purpose |
|-------|----------|---------|
| **Presentation** | 30 min | Intro to the Pi, what’s possible, and the open ideas list. Show a couple of quick demos if you have them. |
| **Kickstart** | 45 min | Choose an idea, get the Pi booted and on the network, install one or two things, run a “hello world” for that idea (e.g. serve a page, send one MQTT message, log an event). |
| **Tinkering** | 2h | Open-ended: deepen the chosen idea, combine two ideas, or go off in a direction of your own. No fixed script — explore, break things, ask for help. |

**Total:** ~3h15 (with short breaks as needed).

---

## Learning objectives

- See the Raspberry Pi as a flexible platform for small projects (hardware, software, cloud, automation).
- Pick one direction and get something working in 45 minutes.
- Spend 2 hours tinkering without a strict script: experiment, iterate, and optionally demo at the end.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; one Pi per team (or per person if you have enough). Base image can be minimal (Raspberry Pi OS Lite or Desktop) or pre-loaded with common tools (Python 3, Docker, Node, etc.) depending on which ideas you want to support.
- **Teams:** 1–3 people; solo is fine for tinkering.
- **Network:** WiFi (or Ethernet) so Pis can reach the internet and each other. Optional: shared MQTT broker, shared API, or tunnel (ngrok) for “show my Pi to the room.”
- **Optional hardware per team:** USB webcam or sensor only if you want to support those ideas; no LEDs or breadboards required.

---

## Presentation (30 min)

**Goal:** Set context and inspiration. Use the Pi live if possible (e.g. one Pi on the big screen).

### 1. Why Raspberry Pi for tinkering (≈5 min)

- Cheap, always-on, Linux, network — good for prototypes, learning, and small automation.
- Pi 3 limits: 1 GB RAM, 4 cores; avoid heavy GUI or huge containers. Plenty for scripts, small servers, and light cloud use.

### 2. What we’ll do today (≈5 min)

- **30 min:** This presentation + overview of open ideas.
- **45 min:** Pick an idea, get the Pi running, do a minimal “hello world” for that idea.
- **2h:** Tinker. Go deeper, combine ideas, or try something else. Optional 5‑min demos at the end.

### 3. Open ideas overview (≈15 min)

- Walk through the list below (or your shortened version). For each, one sentence: what it is and what “hello world” could be in 45 min.
- If you have demos: e.g. “here’s a Pi serving a page,” “here’s an action triggered by HTTP,” “here’s a script that posts to Slack when a file appears.”

### 4. Logistics (≈5 min)

- How to get the roster (team ↔ Pi IP). How to get help (facilitator, Slack, sticky notes). Where to find docs (pin a short link list). Optional: “demo slot” sign-up for the last 20 minutes.

---

## Open ideas list (for handout and slides)

Participants **choose one** (or combine two) and use the 45 min kickstart + 2h tinkering to explore. These are starting points, not step-by-step labs.

1. **Small web app on the Pi**  
   Serve a tiny site (Flask, FastAPI, or static HTML + JS). Add a form, a counter, or a “status” page. Optional: put it behind a tunnel (ngrok) so others can open it.

2. **Event to action (no hardware)**  
   Expose HTTP routes (e.g. /on, /off) that write state to a file or log. Trigger the same action from cron or when a file appears in a folder. “Event → action” with only software.

3. **Scheduled jobs and cron**  
   Use cron to run a script every minute (or every 5). Script can: append to a log, call an API, send a message, or update a file. Explore “the Pi as a tiny scheduler.”

4. **File watcher and automation**  
   When a file appears in a folder (e.g. `inbox/`), run a script: move it, parse it, POST it somewhere, or send a notification. Use inotify/watchdog or a simple poll loop.

5. **HTTP “webhook” endpoint**  
   Expose a small HTTP endpoint on the Pi (e.g. POST /hook). When something calls it (browser, curl, or a cloud service), run an action: log, write to file, run a command, or forward to another service.

6. **Send data to the cloud**  
   Script that collects a “sensor” (simulated or real: CPU temp, random value) and POSTs to a REST API, or publishes to MQTT. Optional: simple dashboard (e.g. static page that polls an API) showing last value.

7. **Tiny container on the Pi**  
   Run one small Docker (or Podman) container: e.g. Alpine + minimal HTTP server or a one-off script. Trigger it from the host (cron or a small Flask app that runs `docker run`). Swap the image and see behaviour change.

8. **Pi as a tiny “bot” or notifier**  
   Script that reacts to an event (time, file, HTTP call) and sends a message: email, Slack, Discord, or Telegram. “When X happens, notify me.”

9. **Two Pis talking**  
   One Pi runs a small HTTP API; the other (or your laptop) calls it. Pass a message, a counter, or a simple “ping/pong.” Optional: form a ring or broadcast (see Workshop 7).

10. **Mix and match**  
    Combine two ideas: e.g. “file in folder → script → POST to cloud + log” or “webhook → run container → send Slack message.”

---

## Kickstart (45 min)

**Goal:** Every team has chosen an idea, has a Pi that boots and is on the network, and has done at least one “hello world” for that idea.

### Suggested flow

1. **Choose idea (5 min)**  
   From the list above (or your own). Write it on a sticky or in a shared doc so facilitators know what to help with.

2. **Boot and connect (10 min)**  
   Power the Pi, find its IP (router, `arp -a`, or screen/keyboard). SSH in (`ssh pi@<ip>`). Optional: shared WiFi + printed roster of hostnames or IPs.

3. **Install / check one thing (10 min)**  
   Depending on the idea: `python3 --version`, `pip install flask`, `docker run hello-world`, install `mosquitto_clients`, or clone a tiny example repo. Don’t over-prepare — just enough to unblock the “hello world.”

4. **Hello world for your idea (20 min)**  
   - **Web app:** Run a one-file Flask app that returns “Hello” and open it in a browser.  
   - **Event to action:** Run a Flask app that writes to a file on GET /trigger and curl it once.  
   - **Cron:** One crontab entry that appends a line to a file every minute.  
   - **File watcher:** Create `inbox/`, run a script that prints “File!” when you `touch inbox/test.txt`.  
   - **Webhook:** Flask route that logs the request body and returns 200.  
   - **Cloud:** One script that POSTs one JSON payload to a given URL (or one MQTT publish).  
   - **Container:** `docker run` one image and see it print or serve one response.  
   - **Notifier:** One script that sends one message to Slack/Discord/Telegram/email.  
   - **Two Pis:** One Pi serves GET /ping; the other (or laptop) curls it.

By the end of the 45 min, each team should have “one thing working” for their chosen idea. That’s the launchpad for the 2h tinkering.

---

## Tinkering (2h)

- **No fixed script.** Teams (or individuals) deepen their idea, try a second idea, or go in a new direction.
- **Facilitator role:** Unblock (network, permissions, missing packages), give short tips, point to docs. Don’t lead step-by-step — let people explore.
- **Optional:**  
  - Short “how’s it going?” check at ~1h (one sentence per team).  
  - Last 20–30 min: voluntary 2–3 min demos (what you built, what you learned, what broke).
- **Optional prize:** Pi or small prize for “most creative,” “best demo,” or raffle among everyone who demos.

---

## Prep checklist

- [ ] **Pis:** One per team (or per person); SD cards with base OS (and optional pre-installed tools).
- [ ] **Network:** WiFi (or Ethernet) and a way to get Pi IPs (DHCP list, mDNS, or roster after boot).
- [ ] **Handout/slide:** One page with the 10 open ideas + format (30 min / 45 min / 2h). Link to Python/Flask/Docker quick refs if useful.
- [ ] **Optional hardware:** USB devices only if you want to support camera/sensor ideas; no LEDs or breadboards.
- [ ] **Optional cloud:** Shared MQTT broker, request-bin style URL, or “ingest” API for “send data to cloud” and “notifier” ideas. Optional Slack/Discord/Telegram webhook or bot token (with clear “lab only” rules).
- [ ] **Optional:** One “demo” Pi connected to the projector for the presentation and for quick “hello world” demos.

---

## Facilitation notes

- **Presentation:** Keep it short and visual. One or two live demos (e.g. “here’s a Pi serving a page,” “here’s an action triggered by HTTP”) go further than many slides.
- **Kickstart:** Circulate and help teams that are stuck (SSH, IP, permissions, syntax). A printed “cheat sheet” with SSH command and one Flask one-liner can save a lot of time.
- **Tinkering:** It’s fine if some teams change idea mid-way. The goal is engagement and experimentation, not a polished product. If someone finishes “their” idea early, suggest combining with another or helping another team.
- **Demos:** Keep them short (2–3 min). “What did you build? What would you do next?” is enough.

---

## If you have extra time

- Add a “show and tell” board (e.g. Miro or a shared doc) where teams post one screenshot or one sentence about their project.
- Offer a “second round” of ideas for teams that want a new challenge in the last hour (e.g. “now add a webhook to your web app” or “now make two Pis cooperate”).
