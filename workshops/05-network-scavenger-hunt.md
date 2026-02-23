# Workshop 5: Network scavenger hunt — discover and map

**Format:** 30 min theory + 1h30 hands-on · **Hardware:** Raspberry Pi 3 per team (+ optional “mystery” devices) · **Prize:** Pi for winning team

---

## Learning objectives

- Explain how devices are discovered on a LAN (ARP, broadcast, scanning).
- Use basic tools (`ping`, `arp`, `nmap`) to find hosts and open ports.
- Produce a correct “network map” (IP + at least one port per device) and optionally identify services.

---

## Common setup

- **Raspberry Pi 3:** 1 GB RAM; pre-flash one SD image with `nmap`, `ip`/`ifconfig`, `arp`, `ping`. Optional: `tcpdump`, `netstat`/`ss`.
- **Teams:** 2–3 people per team; each team has one Pi (or a laptop) to run scans from.
- **Network:** All target devices (Pis + optional mystery devices) on one VLAN, same subnet (e.g. 192.168.10.0/24). No production or sensitive systems on this network.

---

## Theory (30 min)

### 1. Discovery on a LAN (≈8 min)

- **ARP (Address Resolution Protocol):** Maps IP → MAC. When host A wants to talk to B, A may send an ARP request (“who has IP X?”); B replies with its MAC. The result is cached in the ARP table (`arp -a` or `ip neigh`).
- **Broadcast:** ARP requests are often broadcast; so “who’s on this subnet?” can be discovered by triggering ARP (e.g. ping sweep) and then reading the ARP table.
- **Ping sweep:** Send ICMP echo to each IP in the range; responding IPs are “alive.” Tools: `ping`, or `nmap -sn 192.168.10.0/24`.

### 2. Ports and services (≈7 min)

- **Port:** Number (1–65535) that a service listens on. SSH=22, HTTP=80, HTTPS=443, etc. Knowing which ports are open tells you what might be running.
- **Why inventory matters:** For ops (what’s running where) and security (unexpected open ports = misconfig or compromise). Today we do a simple “one open port per device” map.

### 3. Safe scanning and ethics (≈5 min)

- **Only the lab network:** Designate the subnet (e.g. 192.168.10.0/24). No scanning of WiFi guests, internet, or production.
- **No DoS:** Don’t flood hosts; use normal scan rates. `nmap` default is fine; avoid `-T5` or aggressive options.
- **Rules:** Hand out a short “allowed network” and “forbidden” list; explain that in the workplace, scanning must be authorized.

### 4. Tools we’ll use (≈5 min)

- **ping:** Check if a host is up (ICMP). `ping -c 2 192.168.10.1`
- **arp -a** (or `ip neigh show`): List IP ↔ MAC after traffic. Run after a ping sweep to see learned hosts.
- **nmap:** Port scan. Examples: `nmap -sn 192.168.10.0/24` (host discovery), `nmap -F 192.168.10.11` (fast top 100 ports on one host), `nmap -sV -p 22,80 192.168.10.11` (service version on specific ports).
- **netstat / ss:** On the Pi itself, see what’s listening: `ss -tlnp`.

### 5. What “correct map” means (≈5 min)

- **Deliverable:** A list: for each device (IP), at least one open port, and optionally the guessed service (e.g. 22=SSH, 80=HTTP). Order doesn’t matter; completeness and correctness do.
- **Scoring:** First team to submit a map that matches the answer key wins. Tie-break: optional “service guess” accuracy.

---

## Hands-on (1h30)

### Phase 1: Find all hosts (≈25 min)

1. **Know your subnet:** Facilitator gives the range (e.g. 192.168.10.0/24) and confirms “all targets are in this range.”
2. **Host discovery:**  
   - Option A: `nmap -sn 192.168.10.0/24` (no port scan, just “who’s up”).  
   - Option B: Simple script that pings each IP (e.g. 192.168.10.1–254) and records which respond; then run `arp -a` to see learned neighbours.
3. **List:** Produce a list of responding IPs. Remove the team’s own Pi and the router/gateway if you want “only workshop devices.” Handout can say “find all devices that are workshop Pis or mystery devices; exclude the default gateway.”

**Handout:** “Phase 1: Discover every host in the given subnet. Submit a list of IP addresses (one per device).”

### Phase 2: One open port per device (≈35 min)

1. **Port scan each host:** For each IP from Phase 1, run a port scan. Suggested: `nmap -F <ip>` (fast) or `nmap -p 22,80,443,8080,9090 <ip>` if you know the facilitator only opened a few ports. Goal: find at least one open port per device.
2. **Record:** Build a table: IP | open port(s) | (optional) guessed service.
3. **Service guess (optional):** Use `nmap -sV -p <port> <ip>` to get version info, or guess from port number (22=SSH, 80=HTTP, etc.).

**Handout:** “Phase 2: For each discovered device, find at least one open port. Optional: guess the service (SSH, HTTP, etc.). Submit the full map.”

### Phase 3: Submit and verify (≈20 min)

1. **Submission:** Each team submits a single map (e.g. CSV or table): IP, port, service (optional). Timestamp or order of submission for ties.
2. **Answer key:** Facilitator has the canonical list (all expected IPs and at least one open port per device). Optionally include expected service names.
3. **Scoring:** Full marks = all devices present with at least one correct port. Deduct for wrong ports or missing devices. First correct (or highest score) wins.
4. **Wrap-up:** Short debrief — which tool was most useful; how would you automate this; why visibility matters.

**Prize:** Raspberry Pi for the winning team.

---

## Example commands reference

```bash
# Host discovery (no port scan)
nmap -sn 192.168.10.0/24

# After ping sweep, show ARP table
arp -a
# or
ip neigh show

# Fast port scan on one host
nmap -F 192.168.10.11

# Specific ports, with service detection
nmap -sV -p 22,80,443 192.168.10.11

# What's listening on this machine
ss -tlnp
```

---

## Prep checklist

- [ ] **Network:** One VLAN, subnet decided (e.g. 192.168.10.0/24). All workshop Pis and mystery devices on it; no critical services.
- [ ] **Target list:** Document every device you’ll put on the network: IP (static or reservation), and which port(s) are open (e.g. SSH 22, HTTP 80). This is your answer key.
- [ ] **Pi (or laptop) image:** `nmap`, `ip`, `arp`, `ping`; optional `tcpdump`, `ss`. Same image for all teams.
- [ ] **Rules handout:** Allowed subnet; “no scanning outside this range”; no DoS; submission format and deadline.
- [ ] **Submission:** Form or shared sheet with columns: Team, IP, Port, Service (optional). Facilitator copy of answer key for grading.

---

## Troubleshooting

- **nmap not found:** Install with `sudo apt install nmap` (Debian/Ubuntu). On Pi, use ARM-compatible package.
- **No hosts found:** Confirm the team’s Pi is on the same subnet (e.g. `ip addr`); confirm targets are powered and connected; try pinging the gateway first.
- **Wrong port reported:** Some services listen on non-standard ports; answer key should list what you actually configured. If a team reports a port that’s open but not on the key, accept it if verifiable.

---

## If you have extra time

- Add “mystery” devices: e.g. a second router, a NAS, or a locked-down Pi with only one unusual port open. Name them in the key (e.g. “device at .50 = mystery-box, port 9999”).
- Short discussion: How would you do this continuously (e.g. scheduled scan + diff) or with automation (Ansible, script that outputs JSON)?
