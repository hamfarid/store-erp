# Prompt 61: FastAPI API Gateway Pattern

> **Scope**: Central API Gateway design for GAARA-AI
> **When to Load**: Building or modifying the API Gateway service

## Gateway Architecture

The API Gateway (gaara-gateway:8000) is the single entry point for all AI services. Built with FastAPI 0.115+.

### Core Structure
```
services/gateway/
├── Dockerfile
├── requirements.txt
├── main.py                  # FastAPI app entry
├── core/
│   ├── config.py            # Pydantic BaseSettings
│   ├── celery_app.py        # Celery config + task routing + beat schedule
│   ├── security.py          # JWT auth + API key validation
│   ├── middleware.py         # Logging, CORS, rate limiting, metrics
│   └── database.py          # AsyncSession + SQLAlchemy engine
├── api/v1/
│   ├── router.py            # Include all sub-routers
│   ├── llm.py               # /generate, /embed, /chat, /summarize
│   ├── plant.py             # /diagnose, /disease, /nutrient, /batch
│   ├── search.py            # /web, /images, /scrape, /deep
│   ├── image.py             # /ocr, /analyze, /screenshot, /edit
│   ├── avatar.py            # /generate, /tts, /present
│   ├── knowledge.py         # /search, /add, /ask, /categories
│   ├── learn.py             # /session, /sessions, /schedule
│   └── monitor.py           # /health, /metrics, /tasks, /drift, /servers
├── tasks/                   # Celery task definitions
├── models/                  # Pydantic schemas + SQLAlchemy ORM
└── services/                # Service clients (Ollama, Qdrant, RAG, Drift)
```

### API Endpoints
```
# Auth
POST /auth/token              — Get JWT token
POST /auth/refresh            — Refresh token

# LLM (/api/v1/llm)
POST /api/v1/llm/generate     — Text generation
POST /api/v1/llm/embed        — Generate embeddings
POST /api/v1/llm/chat         — Multi-turn conversation
POST /api/v1/llm/summarize    — Summarize text/document
GET  /api/v1/llm/models       — Available models

# Plant Doctor (/api/v1/plant)
POST /api/v1/plant/diagnose   — Full diagnosis (disease + nutrients)
POST /api/v1/plant/batch      — Batch (multiple images)
GET  /api/v1/plant/treatments — Treatment database

# Search (/api/v1/search)
POST /api/v1/search/web       — Web search
POST /api/v1/search/scrape    — Scrape URL
POST /api/v1/search/deep      — Deep research (multi-source)

# Image (/api/v1/image)
POST /api/v1/image/ocr        — OCR (Arabic + English)
POST /api/v1/image/analyze    — AI image analysis
POST /api/v1/image/screenshot — Website screenshot

# Knowledge (/api/v1/knowledge)
POST /api/v1/knowledge/add    — Add to knowledge base
GET  /api/v1/knowledge/search — Semantic search
POST /api/v1/knowledge/ask    — RAG: Question → Answer from KB

# Learning (/api/v1/learn)
POST /api/v1/learn/session    — Start learning session
POST /api/v1/learn/schedule   — Schedule periodic learning

# Avatar (/api/v1/avatar)
POST /api/v1/avatar/tts       — Text-to-speech
POST /api/v1/avatar/generate  — Full avatar video

# Monitor (/api/v1/monitor)
GET  /api/v1/monitor/health   — All services health
GET  /api/v1/monitor/metrics  — Prometheus metrics
GET  /api/v1/monitor/drift    — Model drift reports
```

### Rules
- Every endpoint returns JSON with consistent schema: `{success, data, error, timestamp}`
- All async operations >2s → Celery task → return task_id → poll via GET /tasks/{id}
- JWT required for all endpoints except /health and /auth/token
- Rate limiting: 100 req/min per IP for free tier, 1000 for authenticated
- CORS: configurable via environment variables
- Prometheus metrics exposed at /api/v1/monitor/metrics
