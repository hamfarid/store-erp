import time

import pytest

from src.resilience.circuit_breaker import CircuitBreaker, CircuitOpenError


@pytest.fixture()
def small_breaker():
    # Low thresholds for fast tests
    return CircuitBreaker(
        "test-service",
        failure_threshold=0.5,
        rolling_window_seconds=60,
        min_throughput=4,
        open_state_seconds=0.05,
        half_open_max_in_flight=1,
        success_quorum_percent=1.0,
    )


def _do_call(br: CircuitBreaker, ok: bool):
    token = br.before_call()
    br.after_call(token, success=ok)


def test_trips_open_from_closed(small_breaker: CircuitBreaker):
    br = small_breaker
    # 2/4 failures reach threshold 50% and min throughput
    _do_call(br, ok=False)
    _do_call(br, ok=True)
    _do_call(br, ok=False)
    _do_call(br, ok=True)
    assert br.state == "OPEN"


def test_half_open_allows_probe_and_close_on_success(small_breaker: CircuitBreaker):
    br = small_breaker
    # Trip open first
    _do_call(br, ok=False)
    _do_call(br, ok=True)
    _do_call(br, ok=False)
    _do_call(br, ok=True)
    assert br.state == "OPEN"

    # Not ready yet
    with pytest.raises(CircuitOpenError):
        br.before_call()
    time.sleep(0.06)

    # Now half-open probe
    token = br.before_call()
    # success probe should close (quorum=100%, in_flight=1)
    br.after_call(token, success=True)
    assert br.state == "CLOSED"


def test_half_open_failure_reopens(small_breaker: CircuitBreaker):
    br = small_breaker
    # Trip open first
    _do_call(br, ok=False)
    _do_call(br, ok=True)
    _do_call(br, ok=False)
    _do_call(br, ok=True)

    time.sleep(0.06)
    token = br.before_call()
    br.after_call(token, success=False)
    assert br.state == "OPEN"


def test_open_short_circuits_until_ready(small_breaker: CircuitBreaker):
    br = small_breaker
    # Trip open
    _do_call(br, ok=False)
    _do_call(br, ok=True)
    _do_call(br, ok=False)
    _do_call(br, ok=True)

    # Immediately short-circuit
    with pytest.raises(CircuitOpenError):
        br.before_call()
