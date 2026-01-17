from __future__ import annotations
import os
import sys
import importlib


def test_heartbeat_function_returns_payload():
    # Configure Celery to in-memory before import
    os.environ["CELERY_BROKER_URL"] = "memory://"
    os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"

    # Import after env is set so celery_app picks it up
    tasks_mod = importlib.import_module("src.tasks.example_tasks")

    result = tasks_mod.heartbeat()
    assert isinstance(result, dict)
    assert result.get("status") == "ok"
    assert "ts" in result


def test_beat_schedule_contains_heartbeat():
    os.environ["CELERY_BROKER_URL"] = "memory://"
    os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"
    # Re-import celery_app to ensure it uses env overrides in this test process
    if "src.celery_app" in sys.modules:
        importlib.reload(sys.modules["src.celery_app"])  # type: ignore[arg-type]
    celery_app_mod = importlib.import_module("src.celery_app")
    app = getattr(celery_app_mod, "celery_app")

    schedule = getattr(app.conf, "beat_schedule", {})
    assert "system-heartbeat-30s" in schedule
    assert schedule["system-heartbeat-30s"]["task"] == "system.heartbeat"
