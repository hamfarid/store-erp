from __future__ import annotations
from celery import shared_task
from datetime import datetime, timezone


@shared_task(name="example.add")
def add(x: int, y: int) -> int:
    """Add two numbers and return the result.

    Usage:
        from src.tasks.example_tasks import add
        res = add.delay(2, 3)
        print(res.get(timeout=10))
    """
    return x + y


@shared_task(name="system.heartbeat")
def heartbeat() -> dict:
    """Lightweight heartbeat task for liveness checks.

    Returns a small payload with current UTC timestamp.
    """
    return {
        "status": "ok",
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
