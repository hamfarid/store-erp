"""
HTTP client wrapper with retries, backoff + jitter, and the Circuit Breaker.
Dependency-free except for 'requests'.
"""

from __future__ import annotations

import random
import time
from typing import Optional

import requests

from .circuit_breaker import CircuitOpenError, get_circuit_breaker


DEFAULTS = {
    "failure_threshold": 0.5,
    "rolling_window_seconds": 60,
    "min_throughput": 20,
    "open_state_seconds": 60.0,
    "half_open_max_in_flight": 10,
    "success_quorum_percent": 0.8,
    "retries": 2,
    "timeout_seconds": 10.0,
    "backoff_base": 0.25,
    "backoff_factor": 2.0,
    "jitter": 0.2,
}


def _is_server_error(resp: requests.Response) -> bool:
    try:
        return 500 <= resp.status_code <= 599
    except Exception:
        return False


def _is_retryable_exc(exc: Exception) -> bool:
    return isinstance(
        exc,
        (
            requests.Timeout,
            requests.ConnectionError,
            requests.exceptions.ChunkedEncodingError,
        ),
    )


def http_request(
    service_name: str,
    method: str,
    url: str,
    *,
    session: Optional[requests.Session] = None,
    timeout: Optional[float] = None,
    retries: Optional[int] = None,
    backoff_base: Optional[float] = None,
    backoff_factor: Optional[float] = None,
    jitter: Optional[float] = None,
    breaker_kwargs: Optional[dict] = None,
    **kwargs,
) -> requests.Response:
    """
    Perform an HTTP request with circuit-breaker and retries.

    - service_name: logical name for breaker isolation (e.g., 'crm-api')
    - method: GET/POST/PUT/DELETE/...
    - timeout: per-attempt seconds; defaults to DEFAULTS['timeout_seconds']
    - retries: number of retries after the initial attempt; defaults to DEFAULTS['retries']
    """
    cfg = DEFAULTS.copy()
    if breaker_kwargs:
        cfg.update({k: v for k, v in breaker_kwargs.items() if k in cfg})

    timeout = cfg["timeout_seconds"] if timeout is None else timeout
    retries = cfg["retries"] if retries is None else retries
    backoff_base = cfg["backoff_base"] if backoff_base is None else backoff_base
    backoff_factor = cfg["backoff_factor"] if backoff_factor is None else backoff_factor
    jitter = cfg["jitter"] if jitter is None else jitter

    breaker = get_circuit_breaker(
        service_name,
        failure_threshold=cfg["failure_threshold"],
        rolling_window_seconds=cfg["rolling_window_seconds"],
        min_throughput=cfg["min_throughput"],
        open_state_seconds=cfg["open_state_seconds"],
        half_open_max_in_flight=cfg["half_open_max_in_flight"],
        success_quorum_percent=cfg["success_quorum_percent"],
    )

    sess = session or requests.Session()

    token = breaker.before_call()
    last_exc: Optional[Exception] = None
    # attempts = initial + retries
    total_attempts = max(0, int(retries)) + 1

    for attempt in range(total_attempts):
        try:
            resp = sess.request(method.upper(), url, timeout=timeout, **kwargs)
            # Consider 5xx as failure; 4xx are caller responsibility but not breaker failures
            if _is_server_error(resp):
                if attempt < total_attempts - 1:
                    # backoff and retry
                    wait = backoff_base * (backoff_factor**attempt)
                    wait *= 1 + (random.random() - 0.5) * 2 * jitter
                    time.sleep(max(0.0, wait))
                    continue
                # final failure
                breaker.after_call(token, success=False)
                resp.raise_for_status()  # raises HTTPError
            else:
                breaker.after_call(token, success=True)
            return resp
        except Exception as exc:  # network errors / timeout / last 5xx raise
            last_exc = exc
            if _is_retryable_exc(exc) and attempt < total_attempts - 1:
                wait = backoff_base * (backoff_factor**attempt)
                wait *= 1 + (random.random() - 0.5) * 2 * jitter
                time.sleep(max(0.0, wait))
                continue
            # final failure
            breaker.after_call(token, success=False)
            raise

    # Should not reach here, but keep mypy happy
    if last_exc:
        raise last_exc
    raise CircuitOpenError(f"Circuit '{service_name}' failed without exception")


# Convenience wrappers -------------------------------------------------------


def http_get(service_name: str, url: str, **kwargs) -> requests.Response:
    return http_request(service_name, "GET", url, **kwargs)


def http_post(service_name: str, url: str, **kwargs) -> requests.Response:
    return http_request(service_name, "POST", url, **kwargs)


def http_put(service_name: str, url: str, **kwargs) -> requests.Response:
    return http_request(service_name, "PUT", url, **kwargs)


def http_delete(service_name: str, url: str, **kwargs) -> requests.Response:
    return http_request(service_name, "DELETE", url, **kwargs)
