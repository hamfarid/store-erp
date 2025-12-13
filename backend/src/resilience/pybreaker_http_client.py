"""
HTTP client wrapper using pybreaker + tenacity.
Opt-in alternative to the dependency-free adapter.
"""

from __future__ import annotations

from typing import Optional

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential,
)
from pybreaker import CircuitBreaker as PyCircuitBreaker, CircuitBreakerError

from .circuit_breaker import CircuitOpenError


DEFAULTS = {
    "fail_max": 5,  # consecutive failures before opening
    "reset_timeout": 60,  # seconds open before half-open
    "retries": 2,  # after initial attempt (total attempts = retries + 1)
    "timeout_seconds": 10.0,
    "backoff_base": 0.25,  # seconds
    "backoff_factor": 2.0,
}


_registry: dict[str, PyCircuitBreaker] = {}


def _get_pybreaker(name: str, *, fail_max: int, reset_timeout: int) -> PyCircuitBreaker:
    br = _registry.get(name)
    if br is None:
        br = PyCircuitBreaker(fail_max=fail_max, reset_timeout=reset_timeout, name=name)
        _registry[name] = br
    return br


def _is_server_error(resp: requests.Response) -> bool:
    try:
        return 500 <= resp.status_code <= 599
    except Exception:
        return False


def _retryable_exc(e: Exception) -> bool:
    return isinstance(
        e,
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
    fail_max: Optional[int] = None,
    reset_timeout: Optional[int] = None,
    **kwargs,
) -> requests.Response:
    cfg = DEFAULTS.copy()
    if fail_max is not None:
        cfg["fail_max"] = int(fail_max)
    if reset_timeout is not None:
        cfg["reset_timeout"] = int(reset_timeout)
    if retries is not None:
        cfg["retries"] = int(retries)
    if timeout is not None:
        cfg["timeout_seconds"] = float(timeout)
    if backoff_base is not None:
        cfg["backoff_base"] = float(backoff_base)
    if backoff_factor is not None:
        cfg["backoff_factor"] = float(backoff_factor)

    br = _get_pybreaker(
        service_name, fail_max=cfg["fail_max"], reset_timeout=cfg["reset_timeout"]
    )
    sess = session or requests.Session()

    @retry(
        retry=(
            retry_if_exception_type((requests.Timeout, requests.ConnectionError))
            | retry_if_result(lambda r: _is_server_error(r))
        ),
        stop=stop_after_attempt(cfg["retries"] + 1),
        wait=wait_exponential(
            multiplier=cfg["backoff_base"], exp_base=cfg["backoff_factor"]
        ),
        reraise=True,
    )
    def _attempt() -> requests.Response:
        return sess.request(
            method.upper(), url, timeout=cfg["timeout_seconds"], **kwargs
        )

    try:
        resp = br.call(_attempt)
    except CircuitBreakerError as e:  # pybreaker open
        raise CircuitOpenError(f"Circuit '{service_name}' is OPEN") from e

    # If after retries we still have 5xx, raise
    if _is_server_error(resp):
        resp.raise_for_status()
    return resp


# Convenience wrappers -------------------------------------------------------


def http_get(service_name: str, url: str, **kwargs) -> requests.Response:
    return http_request(service_name, "GET", url, **kwargs)


def http_post(service_name: str, url: str, **kwargs) -> requests.Response:
    return http_request(service_name, "POST", url, **kwargs)


def http_put(service_name: str, url: str, **kwargs) -> requests.Response:
    return http_request(service_name, "PUT", url, **kwargs)


def http_delete(service_name: str, url: str, **kwargs) -> requests.Response:
    return http_request(service_name, "DELETE", url, **kwargs)
