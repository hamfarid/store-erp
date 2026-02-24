# INITIAL_TODO.md — Mandatory Launch Checklist

> **Version**: v26.0.2 (Diamond 32)
> **Status**: Required for ALL new projects
> **Governance**: Global System v26 Diamond 32 — Multi-Project Edition
> **Date**: February 2026

---

## The One Command to Rule Them All

```bash
python3 setup_project.py
```

This script handles Python verification, directory creation, virtual environment, dependencies, and environment variables automatically.

---

## Phase 1: Identity & Governance (Read First — ~5 min)

- [ ] Read `VERSION` — confirm v26.0.2 Diamond 32
- [ ] Read `BOOTSTRAP.md` — system orientation + project portfolio
- [ ] Read `AGENTS.md` — AI agent governance constitution
- [ ] Read `rules/00-iron-rules.md` — non-negotiable rules
- [ ] Read `GLOBAL_PROFESSIONAL_CORE_PROMPT_v35.0.md` — behavior + tech stack
- [ ] Read `prompts/00_MASTER.md` — prompt index (118+ prompts)
- [ ] Read `prompts/00_PRIORITY_ORDER.md` — tiered loading strategy

## Phase 2: Project Selection (Identify Your Target)

Determine which project you're working on and load its specific prompts:

- [ ] **GAARA-AI Ecosystem** → Load prompts 60-70
  - Entry: `prompts/60_gaara_ai_architecture.md`
  - 8 microservices, 4 servers, Tailscale + Cloudflare
  
- [ ] **Gold Price Predictor** → Load prompt 71
  - Entry: `prompts/71_gold_price_predictor.md`
  - Also read: `knowledge/ml/GUIDE-gold-predictor-architecture.md`
  - Also read: `rules/ml-ensemble-voting.md`, `rules/financial-prediction-api.md`
  - Also read: `workflows/15_gold_predictor_pipeline.md`
  
- [ ] **Gaara Scan AI** → Load prompt 72
  - Entry: `prompts/72_gaara_scan_plant_disease.md`
  - Also read: `knowledge/ml/GUIDE-gaara-scan-infrastructure.md`
  - Also read: `rules/self-learning-pipeline.md`
  - Also read: `workflows/16_gaara_scan_diagnosis.md`, `workflows/17_gaara_scan_auto_training.md`

- [ ] **Settings Page** → Load prompt 73
  - Entry: `prompts/73_gaara_ai_settings_page.md`

## Phase 3: Environment Setup (Run Once — ~2 min)

- [ ] Run `python3 setup_project.py` — creates venv, installs deps, sets up .env
- [ ] Verify: `python3 tools/final_verify_functional.py` — system health check
- [ ] Verify: `python3 gap_analysis_check.py` — no missing files

## Phase 4: Directory Structure Verification

Confirm these directories exist (setup script creates them automatically):

```
prompts/          — 118+ governance prompts
roles/            — Agent role definitions
rules/            — Coding standards + ML rules
rules/ml/         — ML-specific policies (YAML + MD)
workflows/        — Step-by-step process guides
templates/        — File templates for new components
examples/         — Working code examples
knowledge/        — Technical guides + best practices
knowledge/ml/     — ML infrastructure guides
tools/            — Verification + utility scripts
infrastructure/   — Docker, K8s, networking configs
memory-bank/      — Active project context
docs/             — Generated project documentation
errors/           — Error catalogs + lessons learned
tests/            — Test templates
data/raw/         — Raw data (git-ignored)
data/processed/   — Processed data (git-ignored)
models/           — Trained models (git-ignored)
logs/             — Application logs (git-ignored)
```

## Phase 5: Anti-Hallucination Verification

- [ ] Confirm you know which project you're targeting (Phase 2)
- [ ] Confirm database version: Gold Predictor = PG 14, Others = PG 16
- [ ] Confirm you will NOT mix code between projects
- [ ] Confirm you will verify file existence before referencing
- [ ] Confirm you will check service health before calling endpoints

## Phase 6: First Commit

- [ ] Create `PLAN.md` with project-specific tasks
- [ ] Commit: `git commit -m "feat: Initialize with Global System v26.0.2 Diamond 32"`
- [ ] Push to GitHub (use `python3 upload_to_github.py` for guided setup)

---

## Cross-Project Isolation Rules

| Attribute | Gold Predictor | Gaara Scan | GAARA-AI |
|:----------|:--------------|:-----------|:---------|
| Database | PostgreSQL 14 | PostgreSQL 16 | PostgreSQL 16 |
| ML Domain | Time-series (ARIMA/LSTM/Prophet) | Computer Vision (YOLO/CNN) | NLP + RAG |
| Docker | Standalone | 10 services | 8 modules |
| Security | AWS Secrets + JWT + MFA | Standard | Standard |
| Drift | PSI 0.20 threshold | mAP50 comparison | Evidently AI |

**NEVER cross-pollinate** code, configs, or database schemas between projects without explicit verification.

---

**Signed**: The Global Professional Engineer
**System**: Global System v26 Diamond 32 v26.0.2 Diamond 32
