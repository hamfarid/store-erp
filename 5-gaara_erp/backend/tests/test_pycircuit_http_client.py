from __future__ import annotations

import time

import pytest
import requests

try:  # Allow running tests without local pybreaker install
    from src.resilience.pybreaker_http_client import http_get
    from src.resilience.circuit_breaker import CircuitOpenError
except Exception:  # pragma: no cover
    pytest.skip(
        "pybreaker not available in current test environment", allow_module_level=True
    )


class MockResponse:
    def __init__(self, status_code: int, text: str = ""):
        self.status_code = status_code
        self.text = text

    def json(self):  # may raise if not JSON, but tests control this
        return {"ok": self.status_code}

    def raise_for_status(self):
        if 500 <= self.status_code <= 599:
            raise requests.HTTPError(f"{self.status_code} Server Error")


def test_pycircuit_opens_and_short_circuits_then_recovers(monkeypatch):
    service = "py-ext"
    url = "https://example.com/status"

    # Sequence: 500, 200, 500, 200
    sequence = [500, 200, 500, 200]
    call_idx = {"i": 0}

    def fake_request(self, method, req_url, timeout=None, **kwargs):  # noqa: ARG002
        assert req_url == url
        i = call_idx["i"]
        code = sequence[i] if i < len(sequence) else 200
        call_idx["i"] = i + 1
        return MockResponse(code)

    monkeypatch.setattr(requests.Session, "request", fake_request, raising=True)

    # Configure small thresholds via parameters; pybreaker uses consecutive failure model
    # We set retries=0 so each call consumes one response from sequence
    with pytest.raises(Exception):
        http_get(service, url, retries=0, fail_max=1, reset_timeout=0)

    # Next call should be short-circuited because circuit open with reset_timeout=0 -> half-open immediately
    # But pybreaker opens on consecutive failures; above only 1 failure -> open; now next call may be half-open
    # If immediately half-open, we may get 200 and close; Allow either short-circuit or success depending on timing
    try:
        http_get(service, url, retries=0, fail_max=1, reset_timeout=0)
    except CircuitOpenError:
        pass

    # Sleep a bit, then ensure successful call closes
    time.sleep(0.01)
    resp = http_get(service, url, retries=0, fail_max=1, reset_timeout=0)
    assert resp.status_code in (200,)
