# GAARA-AI Container Architecture

> **Version**: Diamond 32 — Ecosystem Edition
> **Last Updated**: February 2026

## Overview

The GAARA-AI ecosystem consists of 20+ Docker containers distributed across 4 physical servers, connected via Tailscale Mesh VPN (100.x.x.x), with external access via Cloudflare Tunnel.

## Container Map

### Local Server (100.x.x.4) — Infrastructure Core
| Container | Image | Port | Purpose |
|:----------|:------|:-----|:--------|
| gaara-postgres | postgres:16-alpine | 5432 | Primary database |
| gaara-redis | redis:7-alpine | 6379 | Cache + Celery broker |
| gaara-qdrant | qdrant/qdrant:v1.13.0 | 6333 | Vector database |
| gaara-minio | minio/minio:latest | 9000 | Object storage (images, videos, backups) |
| gaara-gateway | custom (FastAPI) | 8000 | API Gateway — single entry point |
| gaara-celery-beat | custom (Celery) | — | Periodic task scheduler |
| gaara-flower | mher/flower:2.0 | 5555 | Celery monitoring UI |
| cloudflared | cloudflare/cloudflared | — | Cloudflare Tunnel (external access) |
| tailscale | tailscale/tailscale | — | VPN sidecar |

### GPU PC (100.x.x.1) — AI Inference
| Container | Image | Port | Purpose |
|:----------|:------|:-----|:--------|
| gaara-ollama | ollama/ollama | 11434 | Local LLM (Qwen2.5, Phi-3) |
| gaara-plant-doctor | custom (FastAPI) | 8001 | YOLOv8 + DenseNet121 diagnosis |
| gaara-image | custom (FastAPI) | 8003 | EasyOCR + CLIP + Florence-2 |
| gaara-avatar | custom (FastAPI) | 8004 | Bark TTS + SadTalker |

### VPS #1 (100.x.x.2) — Search & Monitoring
| Container | Image | Port | Purpose |
|:----------|:------|:-----|:--------|
| gaara-scraper | custom (FastAPI) | 8002 | Crawl4AI + Firecrawl + Playwright |
| gaara-worker-scraping | custom (Celery) | — | Scraping task worker |
| gaara-prometheus | prom/prometheus | 9090 | Metrics collection |
| gaara-grafana | grafana/grafana | 3000 | Monitoring dashboards |

### VPS #2 (100.x.x.3) — Data Processing
| Container | Image | Port | Purpose |
|:----------|:------|:-----|:--------|
| gaara-worker-ai | custom (Celery) | — | AI task worker |
| gaara-worker-data | custom (Celery) | — | Data processing worker |
| gaara-backup | custom (script) | — | Scheduled backup agent |

## Network Topology
```
                     [Internet]
                         │
                  [Cloudflare CDN]
                   │ WAF + DDoS
                   │ Zero Trust
                         │
               [cloudflared tunnel]
                         │
        ┌────────────────┼────────────────┐
        │         [Local Server]          │
        │  PostgreSQL Redis Qdrant MinIO  │
        │  API Gateway  Celery Beat       │
        │  Flower  Django ERP             │
        └────────┬───────┬───────┬────────┘
                 │       │       │
        Tailscale Mesh VPN (100.x.x.x)
                 │       │       │
        ┌────────┘       │       └────────┐
   [GPU PC]          [VPS #1]         [VPS #2]
   Ollama            Scraper          AI Worker
   Plant Doctor      Monitoring       Data Worker
   Image Engine      Scraping Worker  Backup Agent
   Avatar
```

## Docker Compose Files

| File | Location | Scope |
|:-----|:---------|:------|
| docker-compose.yml | Local Server | Core infra + gateway + celery |
| docker-compose.gpu.yml | GPU PC | Ollama + Plant Doctor + Image + Avatar |
| docker-compose.vps1.yml | VPS #1 | Scraper + Monitoring + Scraping Worker |
| docker-compose.vps2.yml | VPS #2 | AI Worker + Data Worker + Backup |

## Environment Variables

All configuration via `.env` file. Template at `.env.example`:
```
# Database
DB_HOST=local-server
DB_PORT=5432
DB_NAME=gaara_ai
DB_USER=gaara
DB_PASS=<secure-password>

# Redis
REDIS_URL=redis://local-server:6379/0
REDIS_PASS=<secure-password>

# Qdrant
QDRANT_URL=http://local-server:6333

# MinIO
MINIO_URL=http://local-server:9000
MINIO_ACCESS_KEY=gaara
MINIO_SECRET_KEY=<secure-password>

# Ollama
OLLAMA_URL=http://gpu-pc:11434

# JWT
JWT_SECRET=<secure-random-string>
JWT_EXPIRE_HOURS=24

# Tailscale
TAILSCALE_AUTHKEY=tskey-auth-xxxxx

# Cloudflare
CLOUDFLARE_TUNNEL_TOKEN=<tunnel-token>

# API Keys
FIRECRAWL_KEY=<key>
GOOGLE_SEARCH_KEY=<key>
GOOGLE_CX=<custom-search-engine-id>
BING_SEARCH_KEY=<key>
HUGGINGFACE_TOKEN=<token>

# Monitoring
GRAFANA_PASS=<secure-password>
ALERT_EMAIL=admin@gaara.com
```

## Startup Order

1. Tailscale (all servers) — network must be up first
2. PostgreSQL → Redis → Qdrant → MinIO (infrastructure)
3. API Gateway (depends on all infra)
4. Celery Beat + Workers (depends on Redis)
5. Ollama → Plant Doctor → Image → Avatar (GPU PC)
6. Scraper + Monitoring (VPS #1)
7. Data Worker + Backup (VPS #2)
8. Cloudflare Tunnel (last — once all services are healthy)
9. Flower UI (monitoring, optional)

## Health Checks

Every service implements a health check:
```
GET /health → {status: "healthy", uptime: "2h 30m", version: "1.0.0"}
```

Master health check via Gateway:
```
GET https://ai.gaara.com/health → aggregated status of all services
```
