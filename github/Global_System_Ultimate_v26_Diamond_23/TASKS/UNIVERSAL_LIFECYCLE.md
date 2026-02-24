# ♾️ Universal Project Lifecycle

> **Directive**: This Todo List applies to **ANY** project (Backend, Frontend, API, or Hybrid).
> **Standard**: Verified Feb 2026 (Swarm Intelligence, Context Engineering, MCP).

## 🕵️ Phase 1: Discovery & Analysis (The Architect)
- [ ] **Context Loading**: Read `memory-bank/activeContext.md` and `AGENTS.md`.
- [ ] **Inventory Scan**: Run `speckit.py analyze` to map existing files.
- [ ] **Gap Analysis**: Compare current state vs. requirements using RAG.
- [ ] **Tech Stack Verification**: Ensure alignment with 2026 Standards (React 19.2+, FastAPI 0.129+, PG 18).

## 🧠 Phase 2: Planning & Design (The Architect)
- [ ] **Swarm Role Assignment**: Define roles (Architect, Developer, Reviewer, QA) in `memory-bank/coordination.md`.
- [ ] **Interface Design**: Define MCP Tools and API Schemas.
- [ ] **Data Modeling**: Draft PostgreSQL 18 schemas with `pgvector`.
- [ ] **Security Review**: Check for Prompt Injection and Secret Leaks (`preflight_check.py`).
- [ ] **Plan Approval**: Create `memory-bank/plan.md` and get user confirmation.

## 🏗️ Phase 3: Implementation (The Developer)
- [ ] **Environment Setup**: Run `genesis.py` to bootstrap containers and dependencies.
- [ ] **Scaffolding**: Create directory structure using `setup_project.py`.
- [ ] **Core Logic**: Implement business rules using AsyncIO patterns.
- [ ] **Augmentation**: Run `augment.py` to lint and optimize code (Ruff/Prettier).
- [ ] **Documentation**: Update `memory-bank/techContext.md` with new architectural decisions.

## ✅ Phase 4: Verification & Testing (The Reviewer & QA)
- [ ] **Pre-Flight Check**: Run `preflight_check.py` to verify system integrity.
- [ ] **Unit Testing**: Run `pytest` with `pytest-asyncio`.
- [ ] **Integration Testing**: Verify MCP tool interactions and DB connectivity.
- [ ] **Self-Healing**: Run `augment.py heal` on any error logs.
- [ ] **QA Sign-off**: The QA Role must explicitly approve the release candidate in `memory-bank/decisionLog.md`.

## 🚀 Phase 5: Deployment & Handoff (The Publisher)
- [ ] **Final Audit**: Run `speckit.py verify`.
- [ ] **Readme Generation**: Update `README.md` with usage instructions.
- [ ] **Artifact Packaging**: Zip or Dockerize the solution.
- [ ] **System Log**: Update `system_log.md` with release notes.
- [ ] **Handoff**: Deliver final output to user.

---
*Powered by Global System Ultimate (Verified Feb 2026)*
