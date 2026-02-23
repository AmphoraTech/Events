"""Read sensor file and POST JSON to cloud endpoint. Set URL and DEVICE_ID."""
import requests
import time
from datetime import datetime

URL = "https://YOUR_API_ENDPOINT/ingest"
DEVICE_ID = "team1"

while True:
    try:
        with open("/home/pi/sensor_data.txt") as f:
            line = f.readline().strip()
        ts, temp = line.split(",")
        payload = {
            "device_id": DEVICE_ID,
            "timestamp": ts,
            "temperature": float(temp),
            "unit": "celsius",
        }
        r = requests.post(URL, json=payload, timeout=5)
        print(r.status_code, payload)
    except Exception as e:
        print("Error", e)
    time.sleep(30)
