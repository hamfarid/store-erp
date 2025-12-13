import json
import sys
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5002"


def pick_headers(h):
    keys = [
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "X-XSS-Protection",
        "Content-Security-Policy",
        "Referrer-Policy",
        "Permissions-Policy",
        "Access-Control-Allow-Headers",
    ]
    return {k: h.get(k) for k in keys}


out = {}

# Health endpoint
r = requests.get(f"{BASE}/api/health", timeout=5)
out["health"] = {
    "status": r.status_code,
    "headers": pick_headers(r.headers),
    "body": r.json(),
}

# CSRF token endpoint
r2 = requests.get(f"{BASE}/api/csrf-token", timeout=5)
out["csrf"] = {
    "status": r2.status_code,
    "headers": pick_headers(r2.headers),
    "set_cookie": r2.headers.get("Set-Cookie"),
    "body": r2.json(),
}

print(json.dumps(out, ensure_ascii=False, indent=2))
