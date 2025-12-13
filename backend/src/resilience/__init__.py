"""
Resilience utilities package.
"""

from .circuit_breaker import (
    CircuitBreaker,
    CircuitOpenError,
    get_circuit_breaker,
)
from .http_client import http_request, http_get, http_post, http_put, http_delete

# Optional: pybreaker + tenacity adapter
try:  # pragma: no cover - optional dependency may be absent in some environments
    from .pybreaker_http_client import (
        http_request as pb_http_request,
        http_get as pb_http_get,
        http_post as pb_http_post,
        http_put as pb_http_put,
        http_delete as pb_http_delete,
    )

    _PB_AVAILABLE = True
except Exception:  # pragma: no cover
    pb_http_request = None  # type: ignore
    pb_http_get = None  # type: ignore
    pb_http_post = None  # type: ignore
    pb_http_put = None  # type: ignore
    pb_http_delete = None  # type: ignore
    _PB_AVAILABLE = False

__all__ = [
    "CircuitBreaker",
    "CircuitOpenError",
    "get_circuit_breaker",
    "http_request",
    "http_get",
    "http_post",
    "http_put",
    "http_delete",
]

if _PB_AVAILABLE:
    __all__ += [
        # pybreaker + tenacity variants
        "pb_http_request",
        "pb_http_get",
        "pb_http_post",
        "pb_http_put",
        "pb_http_delete",
    ]
