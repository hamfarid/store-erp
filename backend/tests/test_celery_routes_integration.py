from __future__ import annotations
import os
from unittest.mock import patch, MagicMock


def create_client():
    os.environ["SKIP_BLUEPRINTS"] = "1"
    from app import create_app

    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_celery_test_wait_true_returns_result():
    client = create_client()

    mock_async = MagicMock()
    mock_async.id = "abc123"
    mock_async.get.return_value = 5

    with patch("src.tasks.example_tasks.add.delay", return_value=mock_async) as m_delay:
        resp = client.get("/api/celery/test?x=2&y=3&wait=true")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["queued"] is True
        assert data["task_id"] == "abc123"
        assert data["result"] == 5
        m_delay.assert_called_once()


def test_celery_status_uses_async_result():
    client = create_client()

    class FakeResult:
        state = "SUCCESS"

        def ready(self):
            return True

        def successful(self):
            return True

        @property
        def result(self):
            return 42

    with patch("src.celery_app.celery_app.AsyncResult", return_value=FakeResult()):
        resp = client.get("/api/celery/status/xyz")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["task_id"] == "xyz"
        assert data["state"] == "SUCCESS"
        assert data["ready"] is True
        assert data["successful"] is True
        assert data["result"] == 42
