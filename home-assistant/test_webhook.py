#!/usr/bin/env python3
"""Send a synthetic ControlMole report to Home Assistant for integration testing.
No 3DS required. Use only over your trusted home network.
"""
import argparse
import json
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--ha", required=True, help="Home Assistant base URL, e.g. http://homeassistant.local:8123")
parser.add_argument("--webhook-id", required=True)
parser.add_argument("--minutes", type=int, default=15)
args = parser.parse_args()
if not 0 <= args.minutes <= 1440:
    parser.error("--minutes must be 0..1440")
url = args.ha.rstrip("/") + "/api/webhook/" + args.webhook_id
payload = json.dumps({"device_id": "vincent-3ds", "used_minutes": args.minutes}).encode()
request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(request, timeout=10) as response:
    print("HTTP", response.status)
