# Rule: Microservices Architecture — GAARA-AI

> **Applies To**: All 8 GAARA-AI modules

## Service Design Principles
1. **One Service, One Responsibility**: Each container handles exactly one AI capability.
2. **API-First**: Every service exposes a REST API (FastAPI) — no direct function calls between services.
3. **CPU-First**: All models default to ONNX Runtime on CPU. GPU is an optional overlay via docker-compose.gpu.yml.
4. **Async by Default**: Any operation >2 seconds → Celery task.
5. **Stateless Services**: No local state. All state lives in PostgreSQL, Redis, or Qdrant.
6. **Health Endpoints**: Every service MUST expose `GET /health` returning `{status: "healthy", timestamp, version}`.
7. **Metrics Endpoints**: Every service MUST expose `GET /metrics` in Prometheus format.

## Container Naming Convention
```
gaara-{service}     → AI service containers
gaara-{infra}       → Infrastructure containers (postgres, redis, qdrant, minio)
gaara-worker-{type} → Celery worker containers
```

## Inter-Service Communication
- Internal: HTTP via Tailscale IPs (100.x.x.x) using `httpx` async client
- External: Via FastAPI Gateway through Cloudflare Tunnel only
- All requests include `X-Request-ID` header for tracing

## Error Handling
- Standard error response: `{success: false, error: {code, message, details}, timestamp}`
- HTTP 503 if downstream service unavailable (with retry-after header)
- Circuit breaker pattern for flaky services (3 failures → open → retry after 30s)
