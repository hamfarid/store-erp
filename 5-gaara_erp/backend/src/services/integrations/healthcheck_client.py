"""
Thin external integration client using the pybreaker + tenacity HTTP adapter.
"""

from __future__ import annotations

from typing import Any, Dict

from src.resilience.pybreaker_http_client import http_get


def check_external_health(service_name: str, url: str) -> Dict[str, Any]:
    """Call an external service health/status endpoint.

    - service_name: logical name for circuit isolation (e.g., 'sms-gateway')
    - url: full URL to call (e.g., 'https://httpbin.org/status/200')
    """
    resp = http_get(service_name, url, retries=0)
    # Some health endpoints return 204/200 without body; just surface status
    try:
        data = resp.json()
    except Exception:
        data = {"message": resp.text[:200] if resp.text else ""}
    return {"status_code": resp.status_code, "data": data}
