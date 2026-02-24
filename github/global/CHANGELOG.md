# Changelog — Global System v26 Diamond 32

## [v26.0.2] — Diamond 32: Multi-Project Edition (2026-02-19)

### Context — 4 New Source Documents Integrated
- **GOLD_PREDICTOR_WHAT_TO_SAY.pdf**: Complete spec for Gold Price Predictor + Asset Predictor UI dual system
- **gaara-scan-infra.tar**: 13 infrastructure files (Docker, DB schema, Model Manager, Celery Pipeline, Crawler, Monitoring)
- **gaara_ai_settings.pdf**: 10-section settings page UI specification
- **gaara_ai_research.pdf**: Complete tools & architecture research (21 pages)

### Added — New Prompts (3)
- **71_gold_price_predictor.md**: Full spec for dual ML+UI system (4 models, 5 assets, OSF 0.97→0.99)
- **72_gaara_scan_plant_disease.md**: Self-learning plant disease detection (YOLO+CNN, 14 tables, 4 quality gates)
- **73_gaara_ai_settings_page.md**: 10-section Django settings page (learning, LLM, scraping, images, servers, avatar, monitoring, backup, ERP, API keys)

### Added — New Roles (3)
- **ROLE-ml-financial-engineer.md**: Gold Predictor ML models, ensemble optimization, drift detection
- **ROLE-plant-disease-self-learning-engineer.md**: Gaara Scan self-learning loop, crawler, training
- **ROLE-ai-assistant-engineer.md**: Goldy + Free AI assistants, integration with predictions + news

### Added — New Rules (3)
- **ml-ensemble-voting.md**: Weighted voting standards, weight optimization, drift detection protocol
- **self-learning-pipeline.md**: Autonomous learning (trigger → crawl → validate → train → promote/reject)
- **financial-prediction-api.md**: FastAPI standards, security (AWS Secrets + MFA), cache strategy, news service

### Added — New Workflows (3)
- **15_gold_predictor_pipeline.md**: ML training + prediction (data → train 4 models → ensemble → store → drift)
- **16_gaara_scan_diagnosis.md**: 4-quality-gate plant diagnosis (upload → YOLO → CNN → cross-validate → treatment)
- **17_gaara_scan_auto_training.md**: Self-learning loop (threshold → lock → train → compare → promote/reject)

### Added — New Templates (2)
- **TEMPLATE-ml-prediction-model.md**: Adding new prediction models to any time-series system
- **TEMPLATE-gaara-scan-disease-class.md**: Adding new plant diseases to Gaara Scan

### Added — New Examples (2)
- **gaara_scan_self_learning.md**: Full self-learning loop walkthrough
- **gold_predictor_ml_pipeline.md**: Full ML pipeline from data collection to trading signals

### Added — New Knowledge Guides (2)
- **GUIDE-gaara-scan-infrastructure.md**: Complete Docker setup (10 services, GPU auto-detect, Celery config)
- **GUIDE-gold-predictor-architecture.md**: Full architecture + known issues + improvement roadmap

### Updated — Governance Files (7)
- **BOOTSTRAP.md**: Added Section 7 (3-project portfolio)
- **CLAUDE.md**: Added Section 8 (multi-project awareness + prompt loading guide)
- **AGENTS.md**: Added Section 8 (project-specific agent assignments)
- **GLOBAL_PROFESSIONAL_CORE_PROMPT_v35.0.md**: Added Sections 8+9 (multi-project portfolio + cross-project anti-hallucination)
- **CONSTITUTION.md**: Added Article VII (multi-project governance)
- **00_MASTER.md**: Added prompts 71-73 section
- **00_PRIORITY_ORDER.md**: Added Tier 3b for project-specific prompts
- **VERSION**: Updated to v26.0.2

### Summary
- **18 new files** added
- **7 existing files** updated
- Framework now governs 3 AI projects: GAARA-AI Ecosystem, Gold Price Predictor, Gaara Scan AI

---

## [v26.0.1] — Diamond 32: GAARA-AI Ecosystem Edition (2026-02-19)

### Added — New Files
- **11 GAARA-AI Prompts** (60-70): Architecture, Gateway, Ollama, RAG, Celery, Plant Doctor, Scraping, Image/OCR, Avatar/TTS, Drift Detection, Tailscale/Cloudflare
- **5 New Roles**: AI Gateway Engineer, RAG Pipeline Engineer, Plant Doctor Engineer, Scraping Engineer, Network Infrastructure Engineer
- **5 New Rules**: Microservices Architecture, API Gateway Standards, Celery Task Queue, Vector Database Qdrant, Container Networking
- **3 New Templates**: FastAPI Service, Celery Task, Docker Compose Service
- **5 New Workflows**: Smart Search→Knowledge (10), Plant Diagnosis (11), Learning Session (12), Avatar Presentation (13), Market Intelligence (14)
- **2 New Examples**: Full Deployment, Django ERP Integration
- **5 New Knowledge Guides**: Celery Workers 2026, FastAPI Gateway Pattern, RAG Qdrant LangChain 2026, Plant Disease YOLOv8 ONNX, Tailscale+Cloudflare Networking

### Updated — Existing Files
- **BOOTSTRAP.md**: Rewritten — added GAARA-AI 8-module architecture, tech stack, prompt loading strategy
- **CLAUDE.md**: Updated to Diamond 32 — added ecosystem overview, API endpoints, module map
- **AGENTS.md**: Added Section 7: GAARA-AI Ecosystem Awareness (module map, network, agent rules)
- **CONSTITUTION.md**: Full rewrite — added GAARA-AI articles, Arabic-first principle, network sovereignty
- **GLOBAL_PROFESSIONAL_CORE_PROMPT_v35.0.md**: Updated to v35.1 — added ecosystem awareness, anti-hallucination rules
- **00_MASTER.md**: Updated index — added GAARA-AI section (60-70), renamed old 60-70 to 80-90
- **00_PRIORITY_ORDER.md**: Rewritten with 5-tier priority system, GAARA-AI prompts in Tier 2-3
- **VERSION**: Updated to v26.0.1

### Updated — Knowledge Guides (from GAARA_Updated_Files_Feb2026.zip)
- GUIDE-scraping-tool-selection.md → Crawl4AI primary
- GUIDE-ml-tool-versions.md → All versions Feb 2026
- GUIDE-drift-detection-tools.md → Evidently 0.6+
- GUIDE-web-scraping-tools.md → Added Crawl4AI, Firecrawl, ScrapeGraphAI
- GUIDE-vector-database-selection.md → Qdrant production standard
- AI_RAG_WORKFLOW.md → Full rewrite with LangChain 0.3 LCEL
- GUIDE-gpu-container-setup.md → Updated

### Renamed — Prompt Numbering
- Prompts 60-70 (old generic) → renumbered to 80-90 (no content changed)
  - 60_templates → 80_templates
  - 61_microservices → 81_microservices
  - 62_graphql → 82_graphql
  - 63_message_queue → 83_message_queue
  - 64_data_migration → 84_data_migration
  - 65_internationalization → 85_internationalization
  - 66_accessibility → 86_accessibility
  - 67_seo → 87_seo
  - 68_pwa → 88_pwa
  - 69_machine_learning → 89_machine_learning
  - 70_documentation → 90_documentation

### Summary
- **36 new files** added
- **8 existing files** updated
- **11 files** renumbered (no content loss)
- Framework now fully aligned with GAARA-AI 8-module distributed architecture

---

## [v26.0.0] — Diamond 32 (2026-02-19)
### Added
- Mandatory Logging: Centralized logging across all agents
- Strict Mode: Iron Rules enforced by default
- Audit Trail: Comprehensive AI decision logging
- New Roles: Enhanced Financial Analyst, System Architect, ML Engineer

### Changed
- Constitution: Replaced test spec with Governance Constitution
- Bootstrap: Merged legacy D22 instructions into main guide
- Cleanup: Removed 50%+ repository waste

---

## [v26.0.0] — Diamond 28 (2026-01-15)
### Added
- ML Workflows: Specialized ML pipeline workflows
- Error Catalogs: `errors/ml/` for model-specific issues

---

## [v26.0.0] — Diamond 22 (2025-12-01)
### Added
- Initial Release: Base framework for Global System v26 Diamond 32 v26
- Core Prompts: 111-prompt library

## [v26.0.2-r7] — Diamond 32: Directory Completion Edition (2026-02-20)

### Round 7 — Full Directory Completion
- Re-applied all Round 5-6 fixes (badge, AGENTS, OOP, empty files, .gitkeep)
- Created 39 missing subdirectory README.md files across all nested directories
- Fixed 19 infrastructure README headers (broken shell substitution)
- Added README to: infrastructure/* (19 subdirs), errors/ml, errors/critical-resolved (5)
- Added README to: examples/ml, templates/ml, templates/ide_configs
- Added README to: knowledge/core,ml,protocols,templates,workflows
- Added README to: workflows/ml, roles/ml, rules/ml
- Added README to: .github/workflows, audit_diamond_32/tools, backend/app
- Added README to: docs/api, docs/user_guides, frontend/src
- Added README to: memory-bank/knowledge/antipatterns,patterns
- Added README to: prompts/speckit, skills/* (5 subdirs), tests/e2e,integration,unit
- Added README to: tools/evals
- Replaced TODO placeholders in docs/TESTING_STRATEGY.md
- Final state: 0 dirs with content but no README, 0 empty files, 0 TODOs, 0 stale refs
