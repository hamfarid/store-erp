"""
Celery application setup for the Inventory backend.

Uses Redis as the default broker and result backend.
Configure via environment variables:
  REDIS_URL=redis://localhost:5606/0
Run worker (Windows-friendly solo pool):
  python -m celery -A src.celery_app:celery_app worker -l info -P solo
"""

from __future__ import annotations
import os
from celery import Celery
from celery.schedules import crontab

# Broker/result configuration
BROKER_URL = os.getenv("CELERY_BROKER_URL") or os.getenv(
    "REDIS_URL", "redis://localhost:5606/0"
)
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND") or os.getenv(
    "REDIS_URL", "redis://localhost:5606/0"
)

celery_app = Celery(
    "inventory_tasks",
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=[
        "src.tasks.example_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=os.getenv("CELERY_TIMEZONE", "UTC"),
    enable_utc=True,
    task_track_started=True,
)

# Example beat schedule (enabled when celery beat service runs)
celery_app.conf.beat_schedule = {
    "example-add-every-minute": {
        "task": "example.add",
        "schedule": crontab(minute="*"),  # every minute
        "args": (2, 3),
    },
    "system-heartbeat-30s": {
        "task": "system.heartbeat",
        "schedule": 30.0,  # every 30 seconds
    },
}
