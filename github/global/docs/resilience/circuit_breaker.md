# Circuit Breaker (T8)

This module introduces a dependency-free Circuit Breaker and an HTTP client adapter.

- Package: `src/resilience/`
  - `circuit_breaker.py` – CLOSED/OPEN/HALF_OPEN states, rolling failure window, half-open probes.
  - `http_client.py` – Wraps `requests` with retries + backoff + jitter and circuit breaker.
- Config keys (ProductionConfig):
  - `CIRCUIT_BREAKER_ENABLED: bool`
  - `CIRCUIT_BREAKER_DEFAULTS: dict` (thresholds, windows, retries, timeout)
  - `CIRCUIT_BREAKER_SERVICES: dict` (per-service overrides, optional)

Usage example:

```python
from src.resilience.http_client import http_get
resp = http_get("crm-api", "https://crm/api/customers/42", timeout=5)
resp.raise_for_status()
```

Testing strategy:
- Unit tests for state transitions and HTTP behavior using `responses`.
- Fast thresholds for tests; production uses safer defaults.

Notes:
- No behavior is changed until you adopt the adapter in integration code.
- For DB, keep `pool_pre_ping` and sensible timeouts; circuit breaking databases is usually not recommended.

## Optional: pybreaker + tenacity adapter

For production, you can opt into a library-backed adapter that leverages:
- pybreaker (consecutive-failure circuit breaker)
- tenacity (robust retry with exponential backoff)

Usage example:

```python
from src.resilience.pybreaker_http_client import http_get
resp = http_get("crm-api", "https://crm/api/health", retries=1, fail_max=3, reset_timeout=30)
```

A demo route is available once the app starts:
- GET /api/integration/external/health?url=https://httpbin.org/status/200&service=httpbin

