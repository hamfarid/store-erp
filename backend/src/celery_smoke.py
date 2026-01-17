"""
Celery smoke test that enqueues a simple task and waits for the result.
Requires a running Redis instance (default redis://localhost:5606/0).
"""

from __future__ import annotations
import os

import redis
from celery.result import AsyncResult
from typing import Any, cast
from src.celery_app import celery_app
from src.tasks.example_tasks import add


def _redis_available(url: str) -> bool:
    try:
        r = redis.from_url(url)
        return bool(r.ping())
    except Exception:
        return False


def main() -> int:
    url = os.getenv("REDIS_URL", "redis://localhost:5606/0")
    if not _redis_available(url):
        print(f"Redis not reachable at {url}. Start Redis and retry.")
        return 2

    # Ensure the example task is registered with the app
    _ = add  # noqa: F841

    res = cast(AsyncResult, celery_app.send_task("example.add", args=(2, 3)))
    value = cast(Any, res.get(timeout=15))
    print(f"Task result: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
