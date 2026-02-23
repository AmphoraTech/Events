# Workshop 1: Capture the Flag (CTF) on the Pi

**Format:** 35 min theory + 1h25 hands-on + 15 min team presentations · **Hardware:** Raspberry Pi 3 per team · **Prize:** Pi for winning team · **Total:** ~2h15

---

## Learning objectives

- Understand what "attack surface" means and how default configs create risk.
- Practice finding and fixing weak credentials and hidden endpoints.
- Experience a simple CTF format: find flags, submit proof, score by speed/completion.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; pre-flash one SD image for all units to save time.
- **Teams:** 2–3 people per team, one Pi per team.
- **Network:** One SSID, e.g. `192.168.10.0/24`; each Pi gets a static IP or DHCP reservation (e.g. `192.168.10.11` … `192.168.10.20`).
- **Roles:** Each team's Pi is their "target"; attacking can be done by the facilitator's laptop, or teams attack another team's Pi (assign targets to avoid chaos).

---

## Theory (35 min)

### 1. Attack surface (≈8 min)

- **Definition:** Everything that can be reached from the network (ports, services, web paths).
- **Why it matters:** Each open port or endpoint is a potential entry point; reducing surface reduces risk.
- **On a typical Pi:** SSH (22), maybe HTTP (80/443), possibly VNC or other services. Show `ss -tlnp` or `netstat` output and relate to "what an attacker can touch."

### 2. Default passwords and weak configs (≈7 min)

- **Default credentials:** Many devices ship with `pi`/`raspberry` or similar; first step in hardening is changing them.
- **Weak configs:** PermitRootLogin yes, empty passwords, default API keys in code.
- **Good habits:** Strong password or SSH keys, disable root login, use non-default ports if desired (optional to mention).

### 3. Services in context (≈5 min)

- **SSH:** Remote shell; if someone gets in, they have shell access — so protect credentials and consider fail2ban.
- **HTTP:** Web server; any path or file can be discovered by scanning or guessing (e.g. `/admin`, `/backup`, `/.git`). Hidden paths are classic CTF targets.

### 4. What a "flag" is (≈5 min)

- **Format:** Often a string like `FLAG{something-secret}` or `CTF_team1_flag2_abc123`. Submitting this string proves you completed the challenge.
- **Why CTF works for learning:** Clear goal, immediate feedback, gamification. Explain your submission process (form, Discord, paper).

### 5. Rules and ethics (≈5 min)

### 6. Buffer / Q&A (≈5 min)

- Only attack the designated targets (your assigned Pi or the lab network).
- No DoS, no modifying other teams' data beyond what's allowed. Announce how you'll verify submissions (e.g. timestamp, screenshot).

---

## Hands-on (1h25)

### Setup (first 10 min)

- Power on all Pis; ensure they get IPs. Hand out a sheet: team name, their Pi IP, and (if applicable) the IP they are allowed to attack.
- Ensure every team can SSH or access the target (e.g. `ssh pi@<target-ip>` with the password you set on the image). Clarify submission: where to send flags and deadline.

### Flag 1: Harden SSH / change default (≈25 min)

- **Goal:** Prove you've secured the Pi (or, in "attack" mode, that you logged in with the default and then changed it).
- **Defender version:** Teams log into their own Pi, change the default password (and optionally create a new user), document the change. Flag = a phrase you set, e.g. `FLAG{ssh-hardened}`, given after they show the new user or passwd change.
- **Attacker version:** Teams attack the target Pi: SSH with default `pi`/`raspberry` (or whatever you left on the image), then change the password and capture a "proof" file you hid (e.g. `cat /home/pi/flag1.txt`). Flag content: `FLAG{default-be-gone}`.
- **Handout:** "Flag 1: Log in to the target Pi and either (a) change the default password and document it, or (b) read the contents of `/home/pi/flag1.txt` and submit that string."

### Flag 2: Hidden HTTP endpoint or file (≈35 min)

- **Goal:** Discover something not linked from the main page (recon and enumeration).
- **Setup on image:** Lightweight web server (e.g. `python -m http.server 8080` or nginx) serving a folder. Root has `index.html`; a hidden path has the flag, e.g. `/secret.txt` or `/admin/flag2.txt` with content `FLAG{hidden-path-123}`.
- **Tasks:** Teams use browser, `curl`, or a simple script to find the path (guessing, or dirbuster-style if you provide a wordlist). First to submit the exact flag string gets Flag 2.
- **Handout:** "Flag 2: The target runs a web server on port 8080. Find the URL that returns the second flag and submit the full flag string."

### Flag 3: Token in a container or service (≈30 min)

- **Goal:** Slightly harder — find a running service or container that holds a secret.
- **Setup on image:** e.g. a Docker container that serves HTTP and returns a flag when you hit `http://<pi>:9090/flag`, or a small binary/script that prints a flag when run with a specific argument. Flag: `FLAG{container-token}`.
- **Tasks:** Teams discover the port (nmap), interact with the service, or find the correct command/argument. Submit the flag string.
- **Handout:** "Flag 3: A service on the target (port and path to be discovered) returns the third flag. Submit the full flag string."

### Scoring (last 5 min of hands-on)

- Collect submissions (timestamp or order of submission for ties). Announce winner; award Pi.

---

## Team presentations (15 min)

- **Goal:** Each team (or a few volunteers) briefly shares what they did and what they learned.
- **Format:** 2–3 min per team: which flags they got, one trick that worked, or one thing that surprised them. If many teams, pick 4–5 to present or do a quick round ("one sentence per team").
- **Facilitator:** Briefly recap attack surface, default credentials, enumeration, and how flags map to "proof of compromise" or "proof of fix."

---

## Example flag format and submission

- **Flag format:** `FLAG{descriptive-name}` so submissions are easy to check.
- **Submission:** Google Form with fields: Team name, Flag 1, Flag 2, Flag 3, Optional screenshot. Or a shared sheet with timestamp.

---

## Prep checklist

- [ ] **Image:** Raspberry Pi OS (or similar) with SSH enabled, default user `pi` and a known password (or leave default for Flag 1).
- [ ] **Services:** Web server on 8080 with `index.html` and hidden path (e.g. `/secret.txt` or `/admin/flag2.txt`) containing Flag 2.
- [ ] **Flag 3:** Container or script serving Flag 3 on a known port (e.g. 9090); document path/command for answer key.
- [ ] **Network:** DHCP or static IPs; list of team → Pi IP (and target IP if teams attack each other).
- [ ] **Handouts:** One sheet per team with rules, IPs, submission link, and flag descriptions (as above).
- [ ] **Submission:** Form or sheet ready; facilitator has answer key (exact flag strings).
- [ ] **Optional:** Attacker laptop with `nmap`, browser, `curl`, SSH client for demos.

---

## Troubleshooting

- **Can't SSH:** Check IP, password, and that `sshd` is running. Ensure network allows port 22.
- **Web server not responding:** Confirm process is running and firewall allows 8080; check `curl http://<pi>:8080/` from another machine.
- **Flag 3 not found:** Verify container/script is running and port is open; provide a hint (e.g. "check ports 9090 and 8080").

---

## If you have extra time

- Add a "bonus" flag: e.g. find a file with a typo in the path (`/secert.txt`) or a simple base64-encoded flag in the page source.
- Short debrief: "What would you do next to harden this Pi in production?" (firewall, fail2ban, keys-only SSH.)
