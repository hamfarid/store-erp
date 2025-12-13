import time

import pytest
import requests

from src.resilience.http_client import http_get
from src.resilience.circuit_breaker import get_circuit_breaker, CircuitOpenError


class MockResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code

    def raise_for_status(self):
        if 500 <= self.status_code <= 599:
            raise requests.HTTPError(f"{self.status_code} Server Error")


def test_http_client_opens_and_short_circuits_then_recovers(monkeypatch):
    service = "external-api"
    url = "https://example.com/test"

    # Configure breaker defaults to be aggressive for tests
    br = get_circuit_breaker(
        service,
        failure_threshold=0.5,
        rolling_window_seconds=60,
        min_throughput=4,
        open_state_seconds=0.05,
        half_open_max_in_flight=1,
        success_quorum_percent=1.0,
    )

    # Sequence: 500, 200, 500, 200, 200
    sequence = [500, 200, 500, 200, 200]
    call_idx = {"i": 0}

    def fake_request(self, method, req_url, timeout=None, **kwargs):  # noqa: ARG002
        assert req_url == url
        i = call_idx["i"]
        if i >= len(sequence):
            code = 200
        else:
            code = sequence[i]
        call_idx["i"] = i + 1
        return MockResponse(code)

    # Patch Session.request
    monkeypatch.setattr(requests.Session, "request", fake_request, raising=True)

    # Explicitly set retries=0 so we consume exactly one status per call
    for _ in range(4):
        try:
            http_get(service, url, retries=0)
        except Exception:
            # some calls will raise on 500 (HTTPError)
            pass

    assert br.state == "OPEN"

    # While OPEN and not ready, should short-circuit fast
    with pytest.raises(CircuitOpenError):
        http_get(service, url, retries=0)

    # After open_state_seconds, allow half-open probe. Provide success then ensure it closes
    time.sleep(0.06)
    resp = http_get(service, url, retries=0)
    assert resp.status_code == 200
    assert br.state == "CLOSED"
