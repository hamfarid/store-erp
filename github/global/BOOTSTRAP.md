# Global System v26.0.2 (Diamond 32) — Bootstrap Guide

> **Version**: v26.0.2 | **Edition**: Diamond 32 — Multi-Project GAARA AI
> **Last Updated**: February 2026
> **Maintainer**: GAARA Group — CEO Office

---

## 1. Quick Start (3 Commands)

```bash
git clone <repo_url> && cd <project_name>
python3 setup_project.py
python3 tools/final_verify_functional.py
```

## 2. AI Agent Onboarding Sequence

When an AI agent enters this project for the **first time**, follow this exact reading order:

| Step | File | Purpose | Tokens |
|:-----|:-----|:--------|:-------|
| 1 | `VERSION` | Confirm v26.0.2 Diamond 32 | ~10 |
| 2 | `BOOTSTRAP.md` | This file — full system orientation | ~3K |
| 3 | `AGENTS.md` | Governance constitution + agent roles | ~2K |
| 4 | `rules/00-iron-rules.md` | Non-negotiable rules | ~1K |
| 5 | `GLOBAL_PROFESSIONAL_CORE_PROMPT_v35.0.md` | AI behavior + tech stack | ~2K |
| 6 | `prompts/00_MASTER.md` | Prompt index (118+ prompts) | ~2K |
| 7 | `prompts/00_PRIORITY_ORDER.md` | What to load and when | ~1K |

**After onboarding**, load project-specific prompts per Section 6 below.

## 3. System Identity

**Organization**: GAARA Group — 144-year-old Egyptian agricultural conglomerate, exclusive Sakata seeds distributor for 55+ years.

**This Framework** (`Global System v26 Diamond 32 v26`) is the governance layer for ALL AI-powered projects under GAARA Group. It provides prompts, roles, rules, workflows, templates, examples, and knowledge guides that any AI agent must follow.

**What This Is NOT**: This is NOT code. This is a framework of `.md` governance files that instructs AI agents how to build, review, and maintain code across 3 projects.

## 4. Technology Stack

### Core Platform
| Layer | Technology | Version |
|:------|:-----------|:--------|
| Language | Python | 3.12+ |
| Backend | Django (ERP) + FastAPI (AI services) | 5.x / 0.115+ |
| Database | PostgreSQL | 14 (Gold Predictor) / 16 (GAARA-AI, Gaara Scan) |
| Cache & Broker | Redis | 7 Alpine |
| Vector DB | Qdrant | 1.13+ |
| Task Queue | Celery + Flower + Beat | 5.6.2+ |
| Monitoring | Prometheus + Grafana | Latest |
| Containers | Docker Compose v2 | 27+ |

### AI/ML Stack
| Component | Technology | Used By |
|:----------|:-----------|:--------|
| LLM (Local) | Ollama (Qwen2.5 / Phi-3) | GAARA-AI |
| LLM (Cloud) | Claude API + Gemini API | Gold Predictor |
| Embeddings | BGE-M3 (768 dims, multilingual) | GAARA-AI |
| RAG Pipeline | LangChain 0.3+ LCEL + Qdrant | GAARA-AI |
| Disease Detection | YOLOv8n + CNN (ONNX) | Gaara Scan |
| Self-Learning | Celery + Image Crawler + OpenAI Vision | Gaara Scan |
| Price Prediction | ARIMA + LSTM + Prophet + Ensemble Voting | Gold Predictor |
| OCR | EasyOCR (Arabic + English) | GAARA-AI |
| Image Analysis | CLIP / Florence-2 / GradCAM | GAARA-AI, Gaara Scan |
| TTS | Bark + Coqui TTS | GAARA-AI |
| Scraping | Crawl4AI → Firecrawl → Playwright | GAARA-AI |
| Drift Detection | Evidently AI | GAARA-AI, Gold Predictor |
| Inference | ONNX Runtime (CPU-first) | ALL |

### Networking & Infrastructure
| Component | Technology | Purpose |
|:----------|:-----------|:--------|
| Internal VPN | Tailscale (WireGuard mesh) | Server-to-server (100.x.x.x) |
| External Access | Cloudflare Tunnel | Zero-trust HTTPS |
| CI/CD | GitHub Actions | Automated testing |
| IaC | Terraform + Ansible | Server provisioning |

## 5. Project Portfolio (3 Active Systems)

### Project 1: GAARA-AI Unified Ecosystem
| Attribute | Value |
|:----------|:------|
| **Status** | Framework documented, code NOT started |
| **Scope** | 8 AI microservices across 4 servers |
| **Prompts** | 60-70 (11 prompts) |
| **Entry Point** | `prompts/60_gaara_ai_architecture.md` |
| **Stack** | FastAPI + Ollama + Qdrant + Celery + Tailscale |
| **Architecture** | CPU-first ONNX, Arabic-first, 4-server mesh |

**Server Layout:**
```
GPU PC (100.x.x.1)       → Ollama LLM, Plant Doctor, Avatar, Image AI
VPS #1 (100.x.x.2)       → Scraper, Search APIs, Monitoring, Celery Worker
VPS #2 (100.x.x.3)       → Data Processing, Batch Inference, Learning, Backup
Local Server (100.x.x.4)  → PostgreSQL, Redis, Qdrant, MinIO, Django ERP, Gateway
```

**8 Modules:**
| # | Module | Container | Port | Server |
|:--|:-------|:----------|:-----|:-------|
| 1 | AI Agent | gaara-llm | 11434 | GPU PC |
| 2 | AI Avatar | gaara-avatar | 8004 | GPU PC |
| 3 | Search & Scraper | gaara-scraper | 8002 | VPS #1 |
| 4 | Image Engine | gaara-image | 8003 | GPU PC |
| 5 | Drift Detection | (in gateway) | — | Local Server |
| 6 | System Monitor | gaara-prometheus | 9090 | VPS #1 |
| 7 | Big Data & Knowledge | gaara-vectordb | 6333 | Local Server |
| 8 | Data Learning & Backup | (Celery workers) | — | VPS #2 |

### Project 2: Gold Price Predictor + Asset Predictor UI
| Attribute | Value |
|:----------|:------|
| **Status** | Active — OSF 0.97, target 0.99 |
| **Scope** | System 1 (Backend ML) + System 2 (React Frontend) |
| **Prompt** | 71 |
| **Entry Point** | `prompts/71_gold_price_predictor.md` |
| **Stack** | FastAPI + PostgreSQL 14 + Redis 7 + React 19 + tRPC 11 |
| **Models** | ARIMA + LSTM + Prophet + Ensemble (Weighted Voting) |
| **Assets** | Gold, Bitcoin, Ethereum, EGP/USD, TRY/USD |
| **AI Assistants** | Goldy (Claude, unlimited) + Free (Gemini, 10/day) |
| **Security** | AWS Secrets + JWT + MFA/TOTP + SOC 2 + PCI DSS |

### Project 3: Gaara Scan AI (Plant Disease Self-Learning)
| Attribute | Value |
|:----------|:------|
| **Status** | Infrastructure designed, 10 Docker services |
| **Scope** | Autonomous plant disease detection + self-learning |
| **Prompt** | 72 |
| **Entry Point** | `prompts/72_gaara_scan_plant_disease.md` |
| **Stack** | FastAPI + YOLO v8 + CNN + Celery + PostgreSQL 16 |
| **Self-Learning** | Low confidence → Crawl → OpenAI Validate → Retrain → Promote |
| **IoT** | Sensor data → disease risk alerts every 30 minutes |
| **Infrastructure** | `infrastructure/gaara-scan/` (Docker, schema, configs) |

### Shared: GAARA AI Settings Page
| Attribute | Value |
|:----------|:------|
| **Prompt** | 73 |
| **Entry Point** | `prompts/73_gaara_ai_settings_page.md` |
| **Scope** | 10-section Django settings UI for the AI ecosystem |

## 6. Prompt Loading Strategy

The framework contains **118+ prompts**. Load strategically based on context window:

### Tier 1: Always Load (~5K tokens)
```
rules/00-iron-rules.md
AGENTS.md (Sections 1-3)
BOOTSTRAP.md (this file — Sections 4-5)
```

### Tier 2: Load per Project
```
GAARA-AI Ecosystem  → prompts/60_gaara_ai_architecture.md + 61 + 64
Gold Price Predictor → prompts/71_gold_price_predictor.md
Gaara Scan AI       → prompts/72_gaara_scan_plant_disease.md
Settings Page       → prompts/73_gaara_ai_settings_page.md
```

### Tier 3: Load per Module (~3-5K each)
```
LLM work       → prompts/62_ollama_llm_integration.md
RAG/KB work    → prompts/63_rag_pipeline.md
Plant Doctor   → prompts/65_plant_doctor_ai.md
Scraping       → prompts/66_web_scraping_pipeline.md
Image/OCR      → prompts/67_image_processing_ocr.md
Avatar/TTS     → prompts/68_avatar_tts.md
Monitoring     → prompts/69_drift_detection.md
Networking     → prompts/70_tailscale_cloudflare.md
```

### Tier 4: General Development
```
prompts/07_code_generation.md, 09_code_review.md, 26_docker.md, 27_monitoring.md
```

### Tier 5: As Needed
All remaining prompts (01-59, 74-95) loaded only when relevant.

## 7. Key Configuration Files

| File | Purpose |
|:-----|:--------|
| `infrastructure/containers/gaara-ai/docker-compose.yml` | GAARA-AI 8-module Docker Compose |
| `infrastructure/containers/gaara-ai/.env.example` | GAARA-AI environment template |
| `infrastructure/gaara-scan/docker-compose.yml` | Gaara Scan 10-service Docker Compose |
| `infrastructure/gaara-scan/schema.sql` | Gaara Scan 14-table database schema |
| `infrastructure/networking/GUIDE-tailscale-cloudflare-networking.md` | VPN & tunnel setup |
| `knowledge/ml/GUIDE-gaara-scan-infrastructure.md` | Gaara Scan full infra reference |
| `knowledge/ml/GUIDE-gold-predictor-architecture.md` | Gold Predictor architecture + known issues |

## 8. File Naming Conventions

| Directory | Convention | Example |
|:----------|:-----------|:--------|
| prompts/ | `NN_snake_case.md` | `71_gold_price_predictor.md` |
| rules/ | `kebab-case.md` | `ml-ensemble-voting.md` |
| rules/ml/ | `RULES-kebab.md` / `POLICY-kebab.yaml` | `RULES-plant-disease-analysis.md` |
| roles/ | `ROLE-kebab-case.md` | `ROLE-ml-financial-engineer.md` |
| knowledge/ | `GUIDE-kebab-case.md` | `GUIDE-gaara-scan-infrastructure.md` |
| workflows/ | `NN_snake_case.md` | `15_gold_predictor_pipeline.md` |
| templates/ | `TEMPLATE-kebab-case.md` | `TEMPLATE-ml-prediction-model.md` |
| examples/ | `snake_case.md` | `gold_predictor_ml_pipeline.md` |

## 9. Golden Rules

1. **CPU-First**: All models run ONNX on CPU. GPU is optional overlay.
2. **Arabic-First**: OCR, TTS, LLM — Arabic support is mandatory.
3. **Celery for Async**: Any operation >2 seconds → background task.
4. **Qdrant for Knowledge**: Never ChromaDB in production.
5. **Tailscale Internal**: All inter-service traffic via WireGuard mesh.
6. **Cloudflare External**: Zero Trust, no open ports to internet.
7. **Verify Before Acting**: Never assume a file exists or a service is running.
8. **Project Isolation**: Gold Predictor (PG 14), Gaara Scan (PG 16), GAARA-AI (PG 16) — don't mix.
