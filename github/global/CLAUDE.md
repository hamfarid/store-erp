# CLAUDE.md — Claude Code Entry Point (v26.0.2 — Diamond 32)

> **Primary Directive**: See `@AGENTS.md` for full governance framework
> **Ecosystem**: GAARA-AI Unified Ecosystem (8 Modules)

## Core Directives

1. **Context First**: Always read `memory-bank/activeContext.md` and `memory-bank/systemContext.md` before acting on any task.
2. **No Hallucinations**: Verify every import, file path, and API call against the actual codebase.
3. **Tool Usage**: Prefer MCP tools for research, database operations, and testing.
4. **Version Compliance**: This project uses Global System v26 Diamond 32 v26.0.2 (Diamond 32 — GAARA-AI Ecosystem Edition).

## Quick Start for New AI Agents

1. Read `AGENTS.md` — the complete AI agent constitution.
2. Read `BOOTSTRAP.md` — initialization guide + GAARA-AI 8-module architecture.
3. Read `rules/00-iron-rules.md` — non-negotiable rules.
4. Run `speckit analyze` — loads project context.
5. Check `memory-bank/activeContext.md` — current project state.

## GAARA-AI Ecosystem Overview

This project implements a distributed AI system for GAARA Group (agricultural conglomerate, Egypt, est. 1881).

### Architecture
- **4 Servers** connected via Tailscale Mesh VPN (100.x.x.x)
- **8 AI Modules** as Docker microservices
- **FastAPI Gateway** as central entry point (port 8000)
- **Django ERP** (60+ modules) for business operations
- **Cloudflare Tunnel** for secure external access

### The 8 Modules
| Module              | Container      | Tech Stack                      |
|:--------------------|:---------------|:--------------------------------|
| AI Agent            | gaara-llm      | Ollama + Qwen2.5                |
| AI Avatar           | gaara-avatar   | Bark TTS + SadTalker            |
| Search & Scraper    | gaara-scraper  | Crawl4AI + Firecrawl + Playwright |
| Image Engine        | gaara-image    | EasyOCR + CLIP + Florence-2     |
| Drift Detection     | (in gateway)   | Evidently AI                    |
| System Monitor      | gaara-prometheus | Prometheus + Grafana           |
| Big Data & Knowledge | gaara-vectordb | Qdrant + LangChain + BGE-M3   |
| Data Learning       | (Celery workers) | Celery 5.6.2 + Beat           |

### Golden Rule
> CPU-First (ONNX Runtime). GPU upgrade added later.

### Key API Endpoints
```
POST /api/v1/llm/generate     — Text generation
POST /api/v1/llm/chat         — Multi-turn conversation
POST /api/v1/plant/diagnose   — Plant disease diagnosis
POST /api/v1/search/web       — Web search
POST /api/v1/search/deep      — Deep research (multi-source)
POST /api/v1/image/ocr        — OCR (Arabic + English)
POST /api/v1/knowledge/ask    — RAG: Question → Answer from KB
POST /api/v1/avatar/generate  — Avatar video generation
GET  /api/v1/monitor/health   — All services health
```

## Relevant Prompts for GAARA-AI

```
prompts/60_gaara_ai_architecture.md — Full system architecture
prompts/61_fastapi_gateway.md       — API Gateway patterns
prompts/62_ollama_llm_integration.md — LLM service
prompts/63_rag_pipeline.md          — RAG + Knowledge Base
prompts/64_celery_task_management.md — Task queue patterns
prompts/65_plant_doctor_ai.md       — Plant disease detection
prompts/66_web_scraping_pipeline.md  — Multi-engine scraping
prompts/67_image_processing_ocr.md   — Image + OCR
prompts/68_avatar_tts.md            — Avatar + TTS
prompts/69_drift_detection.md       — Model monitoring
prompts/70_tailscale_cloudflare.md  — Network infrastructure
```

## Relevant Rules
```
rules/microservices-architecture.md  — Service design patterns
rules/api-gateway-standards.md       — Gateway routing rules
rules/celery-task-queue.md           — Task queue standards
rules/vector-database-qdrant.md      — Qdrant usage rules
rules/container-networking.md        — Tailscale + Cloudflare rules
```

---

## Section 8: Multi-Project Awareness (Diamond 32)

This framework now governs 3 interconnected AI projects:

| Project | Prompts | Status | Stack |
|:--------|:--------|:-------|:------|
| GAARA-AI Ecosystem | 60-70 | Framework ready | FastAPI + Ollama + Qdrant + Celery |
| Gold Price Predictor | 71 | Active (OSF 0.97) | FastAPI + ARIMA/LSTM/Prophet + React + tRPC |
| Gaara Scan AI | 72 | Infra designed | YOLO v8 + CNN + Celery + Self-Learning |
| Settings UI | 73 | Specified | Django + 10 sections |

### When to Load Which Prompts
- Gold Predictor work → Load 71 + rules/ml-ensemble-voting.md + rules/financial-prediction-api.md
- Gaara Scan work → Load 72 + rules/self-learning-pipeline.md
- Settings page work → Load 73
- GAARA-AI Ecosystem → Load 60-70
