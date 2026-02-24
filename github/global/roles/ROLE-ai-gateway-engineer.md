# ROLE: AI Gateway Engineer

> **Module**: FastAPI API Gateway (gaara-gateway:8000)
> **Reports To**: System Architect

## Responsibilities
- Design and maintain the central FastAPI API Gateway
- Implement JWT authentication and API key management
- Configure rate limiting and CORS policies
- Route requests to appropriate AI microservices via Tailscale IPs
- Implement Prometheus metrics endpoint (/metrics)
- Maintain Pydantic request/response schemas for all endpoints

## Key Endpoints Owned
- `/auth/*` — Authentication
- `/api/v1/monitor/*` — Health + Metrics
- All routing to downstream services

## Standards
- All responses use consistent JSON schema: `{success, data, error, timestamp}`
- Async operations >2s → Celery task → return task_id
- Rate limiting: 100 req/min (unauthenticated), 1000 req/min (authenticated)
- FastAPI 0.115+ with Pydantic v2

## Required Knowledge
- `prompts/61_fastapi_gateway.md`
- `knowledge/ml/GUIDE-fastapi-gateway-pattern.md`
- `rules/api-gateway-standards.md`
