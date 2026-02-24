# AGENTS.md - Global AI Agent Constitution (v26.0.2 Diamond 32)
> **Canonical Source of Truth**: This file is the single entry point for all AI agents operating within the Global System v26 Diamond 32 framework. All other configuration files (`CLAUDE.md`, `.cursorrules`, etc.) must reference this file.

## 1. Core Directives (The “Prime Directives”)

1.  **No File Loss**: You are FORBIDDEN from deleting or overwriting files without explicit user confirmation and a backup.
2.  **Latest Wins**: When merging or updating, the most recent valid version of a file always takes precedence.
3.  **Context First**: Before executing ANY task, you MUST read `memory-bank/activeContext.md` and `memory-bank/systemContext.md`.
4.  **Tool Use**: You MUST use the provided tools (`speckit.py`, `manus-mcp-cli`) for all operations. Manual shell commands are a fallback only.
5.  **Code is Law**: Adhere strictly to the technology stack defined in `BOOTSTRAP.md`.

## 2. 5-Layer Defense Protocol (Immune System)

This system implements a 5-layer defense strategy to ensure code quality and security:

1.  **Layer 1: Static Analysis (Pre-Commit)**
    - Tools: `ruff`, `mypy`, `eslint`, `prettier`
    - Action: Blocks commits that violate syntax or style rules.

2.  **Layer 2: Unit Testing (CI/CD)**
    - Tools: `pytest`, `jest`
    - Action: Verifies individual components function correctly.

3.  **Layer 3: Integration Testing (CI/CD)**
    - Tools: `cypress`, `playwright`
    - Action: Ensures modules work together as expected.

4.  **Layer 4: Security Scanning (Pipeline)**
    - Tools: `bandit`, `safety`, `trivy`
    - Action: Detects vulnerabilities and dependencies issues.

5.  **Layer 5: AI Review (Post-Merge)**
    - Tools: `CodeRabbit`, `Reviewer Agent`
    - Action: Provides semantic analysis and architectural feedback.

## 3. Role Registry (Swarm Intelligence)

The following roles are recognized and authorized within the system. Agents must adopt the persona and constraints of the assigned role.

| Role | Description | Key Responsibilities | Configuration File |
| :--- | :--- | :--- | :--- |
| **Architect** | System Design & Standards | High-level design, technology selection, standard enforcement | `roles/ROLE-swarm-intelligence-coordinator.md` |
| **Developer** | Implementation & Coding | Writing code, unit tests, adherence to style guides | `roles/ROLE-developer.md` |
| **Reviewer** | Code Review & Audit | Security checks, performance analysis, compliance verification | `roles/ROLE-reviewer.md` |
| **QA Engineer** | Testing & Validation | E2E testing, regression testing, bug reporting | `roles/ROLE-qa-engineer.md` |
| **ML Engineer** | Machine Learning Ops | Model training, deployment, monitoring, pipeline management | `roles/ml/ROLE-ml-engineer.md` |
| **Data Scientist** | Data Analysis & Modeling | Feature engineering, experimentation, statistical analysis | `roles/ml/ROLE-data-scientist.md` |
| **Big Data Architect** | Data Infrastructure | Spark/Hadoop clusters, ETL pipelines, data lakes | `roles/ml/ROLE-big-data-architect.md` |
| **Governance Agent** | Policy Compliance | Monitoring adherence to EU AI Act, GDPR, and internal policies | `roles/ml/ROLE-governance-agent.md` |
| **Security Agent** | Threat Detection | Real-time anomaly detection, vulnerability scanning | `roles/ml/ROLE-security-agent.md` |

## 4. Operational Workflows

Agents must follow these defined workflows for specific tasks:

*   **General Development**: `workflows/04_feature_development_workflow.md`
*   **Bug Fixing**: `workflows/05_bug_fix_workflow.md`
*   **ML Development**: `workflows/ml/ml_ai_development.md`
*   **Security Audit**: `workflows/02_security_audit_workflow.md`
*   **Release Management**: `workflows/01_release_workflow.md`

## 5. Technology Stack (Verified Feb 2026)

*   **Frontend**: React 19.2.4 (Server Components), Tailwind v4
*   **Backend**: FastAPI >= 0.129 (Python) or Bun v1.3.8 (Node.js)
*   **Database**: PostgreSQL 18.2 + pgvector v0.8.1
*   **ML/AI**: PyTorch 2.10.0, MLflow 3.9.0, DeepSeek-V3.2
*   **Infrastructure**: Docker (Multi-stage), Kubernetes (HPA enabled)

## 6. Error Handling & Recovery

*   **The Two-Strike Rule**: If a task fails twice with the same error, STOP, analyze, and update `memory-bank/lessons.md`.
*   **Error Catalog**: Consult `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` before asking for human help.

## 7. Platform Configuration

This file (`AGENTS.md`) is the master configuration. Platform-specific files (e.g., `.cursor/rules/*.mdc`, `CLAUDE.md`) inherit from here.

*   **Cursor**: `.cursor/rules/` (Specific coding patterns)
*   **Claude**: `CLAUDE.md` (Conversation style & memory)
*   **VS Code**: `.vscode/settings.json` (Formatters & linters)

## 8. Emergency Procedures

If you are lost or confused:
1.  Read `memory-bank/activeContext.md`.
2.  Read `memory-bank/systemContext.md`.
3.  Run `python3 tools/preflight_check.py`.

## 9. GAARA-AI Ecosystem Awareness

All agents operating within this framework must be aware of the GAARA-AI distributed architecture:

### System Context
- **Company**: GAARA Group — Agricultural Conglomerate (Egypt, Est. 1881)
- **Distribution**: Exclusive Sakata seed distributor in Egypt for 55+ years
- **Architecture**: 8 Docker microservices across 4 servers via Tailscale Mesh VPN
- **Gateway**: FastAPI (port 8000) — central entry point for all AI services
- **ERP**: Django 5.x with 60+ modules (existing system)
- **Golden Rule**: CPU-first (ONNX Runtime) → GPU upgrade later

### Module Map
| Module | Container | Port | Responsible For |
|:-------|:----------|:-----|:----------------|
| AI Agent | gaara-llm | 11434 | LLM inference, chat, embeddings |
| AI Avatar | gaara-avatar | 8004 | TTS, talking avatar, lip sync |
| Search & Scraper | gaara-scraper | 8002 | Web search, multi-engine scraping |
| Image Engine | gaara-image | 8003 | OCR (Arabic+English), image analysis |
| Drift Detection | (in gateway) | — | Model monitoring, data drift |
| System Monitor | gaara-prometheus | 9090 | Health checks, metrics, alerting |
| Big Data & Knowledge | gaara-vectordb | 6333 | RAG pipeline, vector search |
| Data Learning & Backup | (Celery workers) | — | Self-learning, scheduled backup |

### Network Architecture
- **Tailscale** (100.x.x.x) — internal mesh VPN between servers
- **Cloudflare Tunnel** — external access with Zero Trust, HTTPS auto, DDoS/WAF
- **MagicDNS** — auto DNS (gpu-pc, vps1, vps2, local-server)

### Agent Rules for GAARA-AI
1. Any async operation >2 seconds → Celery task (never block the API)
2. All inter-service communication → via httpx async through internal Tailscale IPs
3. All models → ONNX format for CPU inference (2-5x speedup)
4. All embeddings → BGE-M3 (768 dimensions, multilingual Arabic+English)
5. All knowledge storage → Qdrant collections (7 categories)
6. All monitoring → expose /metrics endpoint (Prometheus format)

---

## Section 8: Multi-Project Agent Assignments (Diamond 32)

### Gold Price Predictor Agents
- **ML Financial Engineer**: Model training, ensemble optimization, drift detection
- **AI Assistant Engineer**: Goldy + Free integration, news + sentiment + predictions

### Gaara Scan AI Agents
- **Plant Disease Self-Learning Engineer**: YOLO/CNN training, self-learning loop, crawler pipeline
- **Network Infrastructure Engineer**: Docker services (10), GPU auto-detection

### Cross-Project Rules
- All ML projects follow rules in `rules/ml/`
- Drift detection required for all prediction models
- Self-learning pipelines must use training locks (Redis)
- All Docker services must have health checks
- Financial prediction models require MFA for admin operations
