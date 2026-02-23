"""Minimal AWS Lambda handler. Adjust for API Gateway proxy (e.g. body as json.dumps)."""
import json
from datetime import datetime

def lambda_handler(event, context):
    body = {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
