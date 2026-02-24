# Rule: API Gateway Standards

> **Applies To**: FastAPI Gateway (gaara-gateway:8000)

## Authentication
- JWT tokens for all protected endpoints
- Token expiry: 24 hours (access), 7 days (refresh)
- API keys for service-to-service communication
- Endpoints `/health` and `/auth/token` are public

## Rate Limiting
- Unauthenticated: 100 requests/minute per IP
- Authenticated: 1000 requests/minute per user
- Burst: 2x limit for 10 seconds
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Response Schema (Mandatory)
```json
{
  "success": true,
  "data": {},
  "error": null,
  "timestamp": "2026-02-19T12:00:00Z",
  "request_id": "uuid"
}
```

## Routing Rules
- All AI endpoints prefixed: `/api/v1/{module}/`
- Gateway proxies to downstream service via Tailscale IP
- Timeout: 30 seconds for sync, 300 seconds for async
- Async operations return: `{task_id}` → poll via `GET /api/v1/tasks/{id}`

## CORS
- Origins: configurable via `CORS_ORIGINS` env var
- Methods: GET, POST, PUT, DELETE
- Headers: Authorization, Content-Type, X-Request-ID
