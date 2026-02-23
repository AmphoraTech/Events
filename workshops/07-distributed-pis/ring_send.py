"""Send token to next node in the ring. Set MY_IP and NEXT_IP for each Pi."""
import requests

MY_IP = "192.168.10.11"   # this Pi
NEXT_IP = "192.168.10.12"  # next in ring
payload = {"from": MY_IP, "payload": "ring-token-1"}
r = requests.post(f"http://{NEXT_IP}:5000/message", json=payload, timeout=5)
print(r.status_code)
