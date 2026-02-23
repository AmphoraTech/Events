# Amphora Tech Events

Home for **all Amphora tech events**: workshops, meetups, and hands-on sessions. Use this page to choose a format and find materials to run an event.

---

## What are Amphora tech events?

Structured sessions where people learn by doing: short theory followed by hands-on practice, often in teams. Formats vary from fixed workshops (~2h15) to open tinkering (~3h30). Events can be run standalone or as a series.

---

## Workshops

**Format:** 35 min theory + 1h25 hands-on + 15 min team presentations. **Total:** ~2h15 per workshop (1–7). Workshop 8: 35 min + 45 min + 2h + 25 min team demos ≈ 3h30.

**Good for:** Security, cloud, automation, networking, distributed systems. **Raspberry Pi 3** per team (no extra hardware). Pis can be offered as prizes.

| # | Workshop | Folder | Format / Prize |
|---|----------|--------|-----------------|
| 1 | Capture the Flag (CTF) on the Pi | [01-ctf-on-the-pi](workshops/01-ctf-on-the-pi/) | ~2h15 · Winner gets Pi |
| 2 | Pi as “mini Lambda” — event-driven to AWS | [02-pi-as-mini-lambda](workshops/02-pi-as-mini-lambda/) | ~2h15 · First Lambda / best design |
| 3 | Pi as IoT gateway — sensor to cloud | [03-pi-as-iot-gateway](workshops/03-pi-as-iot-gateway/) | ~2h15 · First E2E / best dashboard |
| 4 | Lightweight containers on Pi | [04-containers-on-pi](workshops/04-containers-on-pi/) | ~2h15 · Smallest image / best trigger |
| 5 | Network scavenger hunt | [05-network-scavenger-hunt](workshops/05-network-scavenger-hunt/) | ~2h15 · First correct map |
| 6 | “Event to action” (triggers and side effects) | [06-event-to-action](workshops/06-event-to-action/) | ~2h15 · First cloud-triggered action |
| 7 | Tiny distributed system — Pis talking | [07-distributed-pis](workshops/07-distributed-pis/) | ~2h15 · First ring/broadcast |
| 8 | Open ideas with Raspberry Pi | [08-open-ideas-raspberry](workshops/08-open-ideas-raspberry/) | ~3h30 · Optional: best demo / raffle |

Each workshop folder contains a **README.md** (full plan, theory, hands-on, prep checklist) and **example files** (Python, Dockerfile, etc.) where needed.

**Practical notes:** Pi 3 has 1 GB RAM. Pre-flash one SD image per workshop. Teams of 2–3 (solo fine for #8). No LEDs or extra hardware needed.

---

## How to run an event

1. **Pick a workshop** — Open the folder from the table above.
2. **Read the README** — Theory outline, step-by-step hands-on, team presentations, prep checklist, troubleshooting.
3. **Use the example files** — Copy or adapt the code in that folder (e.g. `app.py`, `Dockerfile`) for your Pi image or handouts.
4. **Prepare** — Follow the prep checklist; do a dry run if possible.
5. **Run** — One workshop per slot; use handouts and award prizes as noted.

---

## Other event types (to be added)

- **Talks / lightning talks** — Short presentations; add format and schedule when you run them.
- **Meetups** — Casual get-togethers with a theme.
- **Hackathons / challenges** — Multi-hour or multi-day; link rules and themes here when you have them.

Add new formats by creating a section above and linking to a doc or folder.

---

## Contributing

Add a new workshop by creating a folder under `workshops/` (e.g. `workshops/09-my-workshop/`) with a `README.md` and any example files, then add a row to the workshop table above.
