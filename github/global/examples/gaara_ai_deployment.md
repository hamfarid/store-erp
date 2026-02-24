# Example: GAARA-AI Full Deployment

> **Purpose**: Step-by-step deployment of the complete GAARA-AI ecosystem across 4 servers

## Phase 1: Local Server Setup (100.x.x.4)

### 1.1 Install Tailscale
```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --hostname=local-server --advertise-tags=tag:ai-infra \
  --advertise-routes=192.168.1.0/24 --authkey=tskey-auth-xxxxx
```

### 1.2 Start Infrastructure
```bash
cd /opt/gaara-ai
cp .env.example .env  # Edit with real credentials
docker compose up -d postgres redis qdrant minio
```

### 1.3 Initialize Qdrant Collections
```bash
docker compose exec api-gateway python scripts/init_qdrant_collections.py
```

### 1.4 Start Gateway + Celery
```bash
docker compose up -d api-gateway celery-beat flower
```

### 1.5 Start Cloudflare Tunnel
```bash
docker compose up -d cloudflared
# Verify: curl https://ai.gaara.com/health
```

## Phase 2: GPU PC Setup (100.x.x.1)
```bash
tailscale up --hostname=gpu-pc --advertise-tags=tag:ai-gpu
docker compose up -d ollama plant-doctor image-processor
# Pull LLM model:
docker exec gaara-ollama ollama pull qwen2.5:7b
```

## Phase 3: VPS #1 Setup (100.x.x.2)
```bash
tailscale up --hostname=vps1 --advertise-tags=tag:ai-worker --authkey=tskey-auth-xxxxx
docker compose up -d scraper prometheus grafana celery-worker-scraping
```

## Phase 4: VPS #2 Setup (100.x.x.3)
```bash
tailscale up --hostname=vps2 --advertise-tags=tag:ai-worker --authkey=tskey-auth-xxxxx
docker compose up -d celery-worker-data celery-worker-ai
```

## Verification
```bash
# From any server:
curl http://local-server:8000/health           # Gateway
curl http://gpu-pc:11434/api/tags              # Ollama
curl http://local-server:6333/collections      # Qdrant
curl http://vps1:9090/-/healthy                # Prometheus
curl https://ai.gaara.com/api/v1/monitor/health  # External
```

## Post-Deploy Checklist
- [ ] All 4 servers on Tailscale mesh (100.x.x.x)
- [ ] PostgreSQL, Redis, Qdrant, MinIO running
- [ ] API Gateway responding on :8000
- [ ] Ollama responding with at least 1 model loaded
- [ ] Cloudflare Tunnel active → ai.gaara.com accessible
- [ ] Celery workers connected (check Flower at :5555)
- [ ] Prometheus scraping all targets
- [ ] Grafana dashboards loaded
