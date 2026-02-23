"""Simulated sensor: writes timestamp,temperature to a file every 5 seconds."""
import time
import random
from datetime import datetime

while True:
    temp = round(18 + random.random() * 10, 1)
    with open("/home/pi/sensor_data.txt", "w") as f:
        f.write(f"{datetime.utcnow().isoformat()},{temp}\n")
    time.sleep(5)
