# Roles — Global System v26.0.2 Diamond 32

> Role definitions for all system agents and team members.

## Core Roles (Numbered)
- `ROLE-01-architect.md` — System architect
- `ROLE-02-developer.md` — Core developer
- `ROLE-03-reviewer.md` — Code reviewer
- `ROLE-04-qa.md` — Quality assurance

## Specialist Roles
- `ROLE-architect.md` — Architecture decisions
- `ROLE-developer.md` — Feature development
- `ROLE-reviewer.md` — Peer review
- `ROLE-qa-engineer.md` — Testing & QA
- `ROLE-backend-specialist.md` — Backend services
- `ROLE-frontend-specialist.md` — Frontend UI
- `ROLE-database-architect.md` — Database design
- `ROLE-security-auditor.md` — Security review
- `ROLE-api-designer.md` / `ROLE-API_Designer.md` — API design
- `ROLE-documentation-writer.md` — Documentation
- `ROLE-performance-engineer.md` — Performance optimization
- `ROLE-code-reviewer.md` — Detailed code review
- `ROLE-network-infrastructure-engineer.md` — Network & infra

## AI & ML Roles
- `ROLE-ai-assistant-engineer.md` — AI assistant integration
- `ROLE-ai-gateway-engineer.md` — AI gateway management
- `ROLE-rag-pipeline-engineer.md` — RAG pipeline
- `ROLE-swarm-intelligence-coordinator.md` — Multi-agent coordination
- `ROLE-ml-financial-engineer.md` — Financial ML models
- `ROLE-scraping-engineer.md` — Data scraping

## GAARA-Specific Roles
- `ROLE-gaara-scan-engineer.md` — Plant disease scanning
- `ROLE-plant-disease-self-learning-engineer.md` — Self-learning pipeline
- `ROLE-plant-doctor-engineer.md` — Diagnosis system
- `ROLE-celery-task-engineer.md` — Async task management

## ML Roles (in `ml/`)
$(ls roles/ml/*.md 2>/dev/null | while read f; do echo "- \`ml/$(basename $f)\`"; done)

## Role ↔ Prompt Mapping
| Role | Related Prompt |
|------|---------------|
| architect | `prompts/09_architecture.md` |
| developer | `prompts/07_code_generation.md` |
| reviewer | `prompts/06_task_ai.md` |
| backend-specialist | `prompts/20_backend.md` |
| frontend-specialist | `prompts/30_frontend.md` |
| database-architect | `prompts/22_database.md` |
| security-auditor | `prompts/31_authentication.md` |
| gaara-scan-engineer | `prompts/72_gaara_scan_plant_disease.md` |
| ml-financial-engineer | `prompts/71_gold_price_predictor.md` |
| ai-assistant-engineer | `prompts/73_gaara_ai_settings_page.md` |
| rag-pipeline-engineer | `prompts/03_mcp_integration.md` |
