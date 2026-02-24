# Template: FastAPI AI Microservice

> **Use For**: Creating new GAARA-AI Docker microservices

## Directory Structure
```
services/{service-name}/
├── Dockerfile
├── requirements.txt
├── main.py                  # FastAPI app entry point
├── core/
│   ├── config.py            # Pydantic BaseSettings
│   └── logging.py           # Structured logging
├── api/
│   └── routes.py            # API endpoints
├── services/
│   └── {service}_service.py # Business logic
└── models/
    └── schemas.py           # Pydantic request/response schemas
```

## Dockerfile Template
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE {PORT}
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:{PORT}/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{PORT}"]
```

## Mandatory Endpoints
```python
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "{name}", "version": "1.0.0", "timestamp": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics():
    # Prometheus format metrics
    ...
```

## Response Schema (All Endpoints)
```python
class APIResponse(BaseModel):
    success: bool
    data: Any = None
    error: Optional[dict] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    request_id: str = Field(default_factory=lambda: str(uuid4()))
```

## Checklist Before Deploy
- [ ] /health endpoint returns 200
- [ ] /metrics endpoint returns Prometheus format
- [ ] Pydantic v2 schemas for all request/response
- [ ] Structured logging (JSON format)
- [ ] Environment variables via Pydantic BaseSettings
- [ ] Docker health check defined
- [ ] requirements.txt pinned versions
