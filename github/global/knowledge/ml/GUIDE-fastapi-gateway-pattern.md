# GUIDE-fastapi-gateway-pattern.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. Why FastAPI as API Gateway?

FastAPI 0.115+ is the standard for AI/ML microservices in 2026:
- **Async I/O**: High throughput for I/O-bound tasks (HTTP calls to services)
- **Type Safety**: Pydantic 2.10+ for request/response validation
- **Auto Docs**: OpenAPI/Swagger generated automatically
- **Performance**: Near Go/Rust speeds for I/O workloads
- **Ecosystem**: httpx, SQLAlchemy async, Celery integration

## 2. Gateway Architecture

```
Client (Django/Mobile/API)
    │
    ▼
┌─────────────────────────┐
│   FastAPI API Gateway    │  ← Single entry point
│   (port 8000)            │
│                          │
│  • JWT Authentication    │
│  • Rate Limiting         │
│  • Request Logging       │
│  • CORS Middleware       │
│  • Prometheus Metrics    │
│                          │
│  /api/v1/llm/*       ───┼──► Ollama (11434)
│  /api/v1/plant/*     ───┼──► Plant Doctor (8001)
│  /api/v1/search/*    ───┼──► Scraper (8002)
│  /api/v1/image/*     ───┼──► Image Processor (8003)
│  /api/v1/avatar/*    ───┼──► Avatar (8004)
│  /api/v1/knowledge/* ───┼──► Qdrant (6333) + LLM
│  /api/v1/learn/*     ───┼──► Celery Tasks
│  /api/v1/monitor/*   ───┼──► Prometheus (9090)
└─────────────────────────┘
```

## 3. Implementation

### 3.1 Main App
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.middleware import LoggingMiddleware, MetricsMiddleware
from api.v1.router import api_router

app = FastAPI(
    title="GAARA AI Gateway",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware (order matters — outermost first)
app.add_middleware(MetricsMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}
```

### 3.2 Router Organization
```python
# api/v1/router.py
from fastapi import APIRouter
from api.v1 import llm, plant, search, image, avatar, knowledge, learn, monitor

api_router = APIRouter()
api_router.include_router(llm.router, prefix="/llm", tags=["LLM"])
api_router.include_router(plant.router, prefix="/plant", tags=["Plant Doctor"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(image.router, prefix="/image", tags=["Image"])
api_router.include_router(avatar.router, prefix="/avatar", tags=["Avatar"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge"])
api_router.include_router(learn.router, prefix="/learn", tags=["Learning"])
api_router.include_router(monitor.router, prefix="/monitor", tags=["Monitor"])
```

### 3.3 Service Communication (httpx async)
```python
# services/cluster_client.py
import httpx
from core.config import settings

class ClusterClient:
    def __init__(self):
        self.timeout = httpx.Timeout(30.0, connect=5.0)

    async def call_service(self, service_url, endpoint, data=None, files=None):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if files:
                response = await client.post(f"{service_url}{endpoint}", files=files)
            else:
                response = await client.post(f"{service_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()

    async def call_llm(self, prompt, model="qwen2.5:7b"):
        return await self.call_service(
            settings.LLM_URL, "/api/generate",
            data={"model": model, "prompt": prompt, "stream": False}
        )

    async def call_plant_doctor(self, image_bytes):
        return await self.call_service(
            settings.PLANT_URL, "/diagnose",
            files={"image": ("plant.jpg", image_bytes, "image/jpeg")}
        )
```

### 3.4 JWT Authentication
```python
# core/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 3.5 Pydantic Settings
```python
# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Service URLs (Tailscale MagicDNS or Docker network)
    LLM_URL: str = "http://ollama:11434"
    PLANT_URL: str = "http://plant-doctor:8001"
    SCRAPER_URL: str = "http://scraper:8002"
    IMAGE_URL: str = "http://image-processor:8003"
    AVATAR_URL: str = "http://avatar:8004"

    # Infrastructure
    REDIS_URL: str = "redis://redis:6379/0"
    QDRANT_URL: str = "http://qdrant:6333"
    DB_URL: str = "postgresql+asyncpg://gaara:pass@postgres:5432/gaara_ai"

    # Security
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
```

## 4. Deployment

### Production Stack:
```bash
# Gunicorn + Uvicorn workers
gunicorn main:app \
  -k uvicorn.workers.UvicornWorker \
  -w 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Docker:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "--bind", "0.0.0.0:8000"]
```

## 5. Monitoring Integration

```python
# core/middleware.py
from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Request duration')

class MetricsMiddleware:
    async def __call__(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
        REQUEST_DURATION.observe(duration)
        return response
```
