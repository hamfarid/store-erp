# Gaara Scan AI - Project Roles & Operational Framework

**Version:** 2.0  
**Last Updated:** December 13, 2025  
**Scope:** Defines roles, responsibilities, and the mandatory operational framework for all contributors to the Gaara Scan AI project.

---

## I. CORE DIRECTIVE & GUIDING PRINCIPLES

All development activities on this project must adhere to the principles outlined in the `GLOBAL_PROFESSIONAL_CORE_PROMPT.md`. The primary goal is to build a **secure, reliable, and high-quality** agricultural management platform.

### Guiding Principles
1.  **Quality First**: Never compromise on code quality, security, or testing.
2.  **User-Centric**: Prioritize features and fixes that deliver tangible value to the end-user.
3.  **Professional Standards**: Maintain production-grade code and documentation at all times.
4.  **Systematic Approach**: Follow the mandatory OPERATIONAL_FRAMEWORK for all significant tasks.
5.  **Transparency**: Document decisions, trade-offs, and technical rationale clearly.

---

## II. PROJECT ROLES & RESPONSIBILITIES

This project is developed by a team of expert engineers. While collaboration is encouraged, each role has primary ownership over its domain.

| Role | Primary Responsibilities | Key Skills & Technologies |
|---|---|---|
| **Backend Engineer** | - API development & maintenance<br>- Database design & migrations<br>- Business logic implementation<br>- Server-side security & performance | FastAPI, SQLAlchemy, PostgreSQL, Redis, Pytest, Docker |
| **Frontend Engineer** | - UI/UX implementation<br>- Component architecture<br>- State management<br>- Client-side performance & accessibility | React, Vite, Tailwind CSS, Radix UI, Vitest |
| **QA Engineer** | - Test planning & execution<br>- Automated testing (Unit, Integration, E2E)<br>- Code quality enforcement<br>- CI/CD pipeline management | Pytest, Vitest, Playwright, GitHub Actions, Codecov |
| **DevOps Engineer** | - Infrastructure as Code (IaC)<br>- Production deployment & monitoring<br>- Database backups & disaster recovery<br>- Security hardening of infrastructure | Docker, Nginx, GitHub Actions, Prometheus, Grafana, AWS/Azure/GCP |

---

## III. MANDATORY OPERATIONAL_FRAMEWORK (Phases 0-8)

This framework, derived from the `GLOBAL_PROFESSIONAL_CORE_PROMPT.md`, **must be executed in order** for every significant feature, refactor, or fix. The output of each phase should be documented in the corresponding Pull Request or task ticket.

### Phase 0: Deep Chain of Thought (DCoT)
- **Action**: Create a detailed, numbered roadmap for the task.
- **Deliverable**: A checklist covering all affected components (FE, BE, DB, etc.), risks, and success metrics.

### Phase 1: First-Principles Analysis
- **Action**: Gather verifiable facts about the current state of the system.
- **Deliverable**: A list of findings with file paths and line numbers.

### Phase 2: System & Forces Analysis
- **Action**: Map the system components and their interactions.
- **Deliverable**: A dependency graph and a list of leverage points.

### Phase 3: Probabilistic Behavior Modeling
- **Action**: Predict the likely outcomes and behaviors of the system and its users.
- **Deliverable**: A summary of expected user patterns, edge cases, and potential failure modes.

### Phase 4: Strategy Generation (≥3 Options)
- **Action**: Develop at least three distinct implementation strategies (e.g., quick fix, balanced approach, full refactor).
- **Deliverable**: A table comparing the strategies based on scope, cost, risk, and impact.

### Phase 5: Stress-Test & Forecast
- **Action**: Analyze the best-case, worst-case, and most-probable outcomes for the chosen strategy.
- **Deliverable**: A brief report including a rollback plan.

### Phase 6: Self-Correction Loop
- **Action**: Refine the chosen strategy by combining the best elements and challenging assumptions.
- **Deliverable**: A final, scored implementation plan (Reward Metric: 0.0-1.0).

### Phase 7: Operational Principle Extraction
- **Action**: Abstract the core lesson learned from the task into a reusable principle.
- **Deliverable**: A documented principle explaining what was learned and when to apply it.

### Phase 8: Final Review
- **Action**: Confirm 100% adherence to all framework phases and project standards.
- **Deliverable**: A final checklist confirming that all code is tested, documented, and meets quality standards before merging.

---

## IV. OUTPUT & DOCUMENTATION PROTOCOL

For every task, the final output must be structured and transparent.

### Decision Log (`<decision_trace>`)
- A concise, public log documenting the execution of Phases 0-8.
- **Must include**: Facts, findings, decisions, and evidence (file paths, metrics).
- **Must NOT include**: Private chain-of-thought or speculative comments.

### Implementation (`<result>`)
- The final code, configuration, or documentation changes.
- Must be accompanied by a clear implementation plan.

### Summary (`<summary>`)
- A brief, 1-3 sentence wrap-up of what was accomplished and the next steps.
