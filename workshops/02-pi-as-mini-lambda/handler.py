#!/usr/bin/env python3
"""Simple handler: writes current time to a file. Run from cron or from Flask."""
from datetime import datetime

with open("/home/pi/last_run.txt", "w") as f:
    f.write(datetime.utcnow().isoformat())
print("OK")
