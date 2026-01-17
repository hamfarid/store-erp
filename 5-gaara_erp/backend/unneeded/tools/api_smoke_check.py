import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8000"

endpoints = [
    ("GET", f"{BASE}/api/health", None),
    ("GET", f"{BASE}/api/status", None),
]

for method, url, payload in endpoints:
    try:
        if method == "GET":
            with urllib.request.urlopen(url, timeout=5) as r:
                print(f"{method} {url} -> {r.status}")
                print(r.read().decode())
        else:
            data = json.dumps(payload or {}).encode()
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method=method,
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                print(f"{method} {url} -> {r.status}")
                print(r.read().decode())
    except Exception as e:
        print(f"ERR {method} {url}: {e}")
        # continue to next

sys.exit(0)
