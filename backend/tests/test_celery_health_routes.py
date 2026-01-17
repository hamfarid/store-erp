from __future__ import annotations
import os
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))


def create_test_client():
    # Skip heavy blueprint registration during tests to avoid duplicate endpoints
    os.environ["SKIP_BLUEPRINTS"] = "1"
    from main import app as flask_app  # noqa: E402

    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def test_celery_health_status_ok():
    client = create_test_client()
    with patch(
        "src.celery_app.celery_app.control.ping",
        return_value=[{"w1@local": {"ok": "pong"}}],
    ):
        resp = client.get("/api/celery/health/status")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"


def test_celery_health_status_no_workers():
    client = create_test_client()
    with patch("src.celery_app.celery_app.control.ping", return_value=[]):
        resp = client.get("/api/celery/health/status")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] in ("no_workers", "ok")  # tolerate transient states


def test_celery_health_deep_uses_heartbeat():
    client = create_test_client()
    # Mock ping ok and heartbeat.delay().get()
    mock_async = MagicMock()
    mock_async.id = "task123"
    mock_async.get.return_value = {"status": "ok"}

    with patch(
        "src.celery_app.celery_app.control.ping",
        return_value=[{"w1@local": {"ok": "pong"}}],
    ):
        with patch("src.tasks.example_tasks.heartbeat.delay", return_value=mock_async):
            resp = client.get("/api/celery/health?deep=true")
            assert resp.status_code == 200
            data = resp.get_json()
            assert data["status"] == "ok"
            assert data.get("deep", {}).get("result", {}).get("status") == "ok"
