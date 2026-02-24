# PROMPT 79 — Logging Strategy (v26.0.2 Diamond 32)

## Purpose
Standardized logging across all services for debugging, auditing, and observability.

## Logging Levels
- **CRITICAL**: System failures, data loss, security breaches
- **ERROR**: Operation failures requiring attention
- **WARNING**: Degraded performance, approaching limits
- **INFO**: Normal operations, state changes, deployments
- **DEBUG**: Detailed diagnostic (dev/staging only)

## Standards
1. Use structured JSON logging (not plain text)
2. Include: timestamp, level, service_name, correlation_id, message, context
3. Never log secrets, passwords, tokens, or PII
4. Log at function entry/exit for critical paths
5. Use correlation IDs across microservices for distributed tracing

## Implementation
- Python: `structlog` or `python-json-logger`
- Django: Override `LOGGING` settings in `settings.py`
- FastAPI: Middleware for request/response logging
- Celery: Task-level logging with task_id as correlation_id

## Retention
- Production: 90 days hot, 1 year cold storage
- Staging: 30 days
- Development: 7 days

## Integration
- Ship to centralized logging (ELK/Grafana Loki)
- Alert on ERROR/CRITICAL via `rules/ml/POLICY-alerting-escalation.yaml`
