import sys
from pathlib import Path
from typing import List, Tuple

# Ensure backend/src is importable
SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

# Import the Flask app from main.py
from main import app  # type: ignore  # noqa: E402


def collect_routes() -> List[Tuple[str, str, List[str]]]:
    """Collect (rule, endpoint, methods) for non-static routes.
    Prefer API routes first.
    """
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        allowed = {"GET", "POST", "PUT", "PATCH", "DELETE"}
        methods = sorted([m for m in (rule.methods or set()) if m in allowed])
        routes.append((str(rule), rule.endpoint, methods))
    # Sort to show /api/* first, then others
    routes.sort(key=lambda x: (0 if x[0].startswith("/api/") else 1, x[0]))
    return routes


def run_probe():
    client = app.test_client()
    ok = 0
    total = 0
    print("=== Route probe (test_client) ===")
    for rule, endpoint, methods in collect_routes():
        # Only probe safe GETs
        if "GET" not in methods:
            continue
        # Skip routes likely to mutate or require auth; adjust as needed
        if any(
            seg in rule.lower()
            for seg in ["login", "logout", "upload", "delete", "remove"]
        ):
            continue
        total += 1
        try:
            resp = client.get(rule)
            status = resp.status_code
            status_text = "OK" if 200 <= status < 400 else "FAIL"
            if status_text == "OK":
                ok += 1
            print(f"{status_text:4} {status:3} {rule:60} -> endpoint={endpoint}")
        except Exception as e:
            print(f"ERR  --- {rule:60} -> {e}")
    print(f"=== Summary: {ok}/{total} GET routes responded with <400 ===")


if __name__ == "__main__":
    run_probe()
