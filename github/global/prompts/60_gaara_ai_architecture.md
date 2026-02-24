# Prompt 60: GAARA-AI Unified Ecosystem Architecture

> **Scope**: Full system architecture for GAARA-AI — 8 modules, 4 servers, Tailscale mesh
> **When to Load**: Any GAARA-AI development work

## System Identity
You are building GAARA-AI — an integrated AI ecosystem for GAARA Group, a 144-year-old Egyptian agricultural conglomerate and exclusive Sakata seed distributor for 55+ years.

## Architecture Overview

### The 8 Modules
1. **AI Agent** (gaara-llm:11434) — Ollama LLM inference, chat, summarize, embeddings
2. **AI Avatar** (gaara-avatar:8004) — Bark/Coqui TTS, SadTalker talking avatar, Wav2Lip lip sync
3. **Search & Scraper** (gaara-scraper:8002) — Crawl4AI (primary), Firecrawl (complex sites), ScrapeGraphAI (NLP), Playwright (fallback)
4. **Image Engine** (gaara-image:8003) — EasyOCR (Arabic+English), CLIP/Florence-2 analysis, Playwright screenshots
5. **Drift Detection** (in API Gateway) — Evidently AI data drift + model drift monitoring
6. **System Monitor** (gaara-prometheus:9090 + gaara-grafana:3000) — Health checks, metrics, alerting
7. **Big Data & Knowledge** (gaara-vectordb:6333) — Qdrant VectorDB, RAG pipeline with LangChain + BGE-M3
8. **Data Learning & Backup** (Celery workers) — Self-learning sessions, scheduled backup

### 4-Server Distribution
```
GPU PC (gpu-pc / 100.x.x.1):
  → Ollama LLM, Plant Doctor, Avatar, Image AI, Training

VPS #1 (vps1 / 100.x.x.2):
  → Scraper, Search APIs, Monitoring, Celery Worker, Flower UI

VPS #2 (vps2 / 100.x.x.3):
  → Data Processing, Batch Inference, Learning Worker, Celery Worker, Backup Agent

Local Server (local-server / 100.x.x.4):
  → PostgreSQL 16, Redis 7, Qdrant, MinIO, Django ERP, FastAPI Gateway, cloudflared
```

### Network Layers
- **Layer 1 — Tailscale Mesh VPN**: Internal 100.x.x.x network, WireGuard-based, MagicDNS, P2P, ACLs per tag
- **Layer 2 — Cloudflare Tunnel**: External access via cloudflared container, Zero Trust auth, auto HTTPS, DDoS/WAF

### Golden Rule
> CPU-First (ONNX Runtime): All models run on CPU initially. GPU support via docker-compose.gpu.yml override.

## Key Design Decisions
1. CPU-First (ONNX) — portability, no GPU dependency
2. Service per Function — one container per AI capability
3. Celery for Async — any operation >2 seconds becomes a task
4. Qdrant (not ChromaDB) — production-grade, Hybrid Search (Dense + BM25)
5. FastAPI Gateway — single entry point, JWT + rate limiting
6. Django for UI — ERP already has 60+ modules, add ai_integration app
7. Redis (Broker + Cache) — Celery broker + result backend + caching
8. ONNX Runtime — 2-5x speedup on CPU vs PyTorch
9. Tailscale + Cloudflare — zero-config internal mesh + secure external access
10. Arabic-First — OCR Arabic, TTS Arabic, LLM supports Arabic (Qwen 2.5)
11. LangChain + Qdrant — RAG pipeline with Hybrid Search
12. Evidently AI — free, open-source drift monitoring
13. BGE-M3 Embeddings — multilingual Arabic+English, 768 dimensions
