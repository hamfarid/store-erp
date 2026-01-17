# FILE: backend/src/routes/external_integration.py | PURPOSE: Demo
# external integration wired to circuit breaker adapter
# (pybreaker+tenacity)
from __future__ import annotations

from flask import Blueprint, request

from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from src.resilience.circuit_breaker import CircuitOpenError
from src.services.integrations.healthcheck_client import check_external_health

ext_bp = Blueprint("external_integration", __name__)


@ext_bp.route("/api/integration/external/health", methods=["GET"])
def external_health():
    """Call an external health/status endpoint using the resilient HTTP client.

    Query params:
    - url: full URL to call (default: https://httpbin.org/status/200)
    - service: logical service name for circuit isolation (default: httpbin)
    """
    url = request.args.get("url", "https://httpbin.org/status/200")
    service = request.args.get("service", "httpbin")

    try:
        result = check_external_health(service, url)
        return success_response({"service": service, "url": url, **result})
    except CircuitOpenError:
        return error_response(
            "Circuit is open for external service",
            ErrorCodes.SYS_INTERNAL_ERROR,
            503,
            details={"service": service},
        )
    except Exception as e:  # noqa: BLE001 - surface envelope only
        return error_response(str(e), ErrorCodes.SYS_INTERNAL_ERROR, 502)
