# Docker Configuration Guide — Global System v26.0.2 Diamond 32

## Compose Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `docker-compose.yml` | **Main development stack** — backend, frontend, database, Redis | Local development and testing |
| `infrastructure/containers/docker-compose.yml` | **AI containers** — learning, search, Qdrant | When running GAARA-AI services |
| `infrastructure/docker-compose.shared.yml` | **Shared services** — monitoring, logging, networking | Always (imported by other compose files) |
| `infrastructure/docker/docker-compose.ml-pipeline.yml` | **ML training pipeline** — GPU training, model serving | Model training and deployment |

## Dockerfiles

| File | Purpose |
|------|---------|
| `infrastructure/Dockerfile.backend` | Django/FastAPI backend |
| `infrastructure/Dockerfile.frontend` | React/Next.js frontend |
| `infrastructure/Dockerfile.template` | Base template for new services |
| `infrastructure/docker/Dockerfile.ml-training` | ML training with GPU support |
| `infrastructure/docker/Dockerfile.ml-serving` | ONNX/vLLM model serving |
| `infrastructure/docker/Dockerfile.python` | General Python service |
| `infrastructure/docker/Dockerfile.spark` | Apache Spark jobs |
| `infrastructure/containers/learning/Dockerfile` | Self-learning pipeline |
| `infrastructure/containers/search/Dockerfile` | RAG search service |

## Quick Start

```bash
# Development (backend + frontend + DB)
docker compose up -d

# With AI services
docker compose -f docker-compose.yml \
  -f infrastructure/containers/docker-compose.yml up -d

# ML pipeline (requires GPU)
docker compose -f infrastructure/docker/docker-compose.ml-pipeline.yml up -d
```

## Networks
All services share the `gaara-network` bridge defined in `docker-compose.shared.yml`.

## Templates
- `templates/TEMPLATE-docker-compose-service.md` — New service scaffold
