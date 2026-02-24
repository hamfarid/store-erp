# Project Lifecycle Knowledge Base
 (v26.0.2 Diamond 32 GAARA AI)

**FRAMEWORK: 2026 AI Coding Agent Governance**
**STATUS: MANDATORY**

This document defines the **Standard Operating Procedure (SOP)** for the entire lifecycle of any project built under the Global System v26 Diamond 32.

## 1. 🏁 Project Lifecycle: Phases Overview

### Phase 1: Inception & Analysis (The "Why")
**Goal:** Define the problem, scope, and success metrics.

*   **Step 1.1: Context Loading:**
    *   Read `AGENTS.md` and `memory-bank/activeContext.md`.
    *   Run `python3 global_system/scripts/preflight_check.py`.
*   **Step 1.2: Requirement Analysis:**
    *   Use `python3 global_system/tools/speckit.py analyze`.
    *   Identify stakeholders, constraints, and "Zero-Error" criteria.
*   **Step 1.3: Architecture Design:**
    *   Consult `knowledge/protocols/future_proof_architecture.md`.
    *   Draft `ARCHITECTURE.md` (C4 Model).
*   **Output:** `PLAN.md`, `ARCHITECTURE.md`.

### Phase 2: Planning & Scaffolding (The "How")
**Goal:** Create a detailed roadmap and set up the environment.

*   **Step 2.1: Task Breakdown:**
    *   Break down `PLAN.md` into atomic tasks (max 4 hours each).
    *   Assign roles (Architect, Developer, Reviewer) per `global_system/workflows/05_bug_fix_workflow.md`.
*   **Step 2.2: Environment Setup:**
    *   Initialize `uv` (Python) and `pnpm` (Node.js).
    *   Configure `pre-commit` hooks (Ruff, Biome, Gitleaks).
*   **Step 2.3: Eval Definition (EDD):**
    *   Write Evals **BEFORE** code. Define `pass@1` criteria.
    *   Create `tools/evals/project_eval.py`.
*   **Output:** `tasks.json`, `tools/evals/`, Initial Repo Structure.

### Phase 3: Implementation (The "What")
**Goal:** Write clean, secure, and tested code.

*   **Step 3.1: The Loop (Red-Green-Refactor):**
    *   **Red:** Write a failing test/eval.
    *   **Green:** Write minimal code to pass.
    *   **Refactor:** Optimize and clean up.
*   **Step 3.2: Security First:**
    *   Check against `knowledge/technical/owasp_llm_2025.md`.
    *   Run `python3 global_system/tools/security_scan.py`.
*   **Step 3.3: Documentation:**
    *   Update `README.md` and `docs/` in real-time.
*   **Output:** Source Code, Tests, Updated Docs.

### Phase 4: Verification & Audit (The "Check")
**Goal:** Ensure Zero-Error quality.

*   **Step 4.1: Automated Verification:**
    *   Run `python3 global_system/tools/speckit.py verify`.
    *   Run full test suite (Pytest/Playwright).
*   **Step 4.2: Security Audit:**
    *   Run `trivy fs .` (Filesystem).
    *   Run `trivy config .` (IaC).
*   **Step 4.3: Sentinel Check:**
    *   Run `python3 global_system/tools/sentinel.py`.
    *   **VETO:** If Sentinel fails, go back to Phase 3.
*   **Output:** `REVIEW_LOG.md`, Audit Reports.

### Phase 5: Deployment & Observability (The "Live")
**Goal:** Safe, zero-downtime release.

*   **Step 5.1: Containerization:**
    *   Build Docker image (distroless, signed with Cosign).
*   **Step 5.2: Infrastructure:**
    *   Apply OpenTofu config (`infrastructure/iac/`).
*   **Step 5.3: Rolling Update:**
    *   Deploy to K8s with `maxUnavailable: 0`.
    *   Monitor metrics (OpenLLMetry).
*   **Output:** Live System, Monitoring Dashboards.

### Phase 6: Retrospective & Memory (The "Learn")
**Goal:** Improve the system for next time.

*   **Step 6.1: Memory Consolidation:**
    *   Update `memory-bank/project_history.md`.
    *   Extract reusable patterns to `global_system/examples/`.
*   **Step 6.2: Post-Mortem (if needed):**
    *   Analyze any incidents or near-misses.
*   **Output:** Updated Memory Bank.

---
*Signed,*
*The Global Professional Engineer (Global System v26 Diamond 32 v26.0 Diamond 32 GAARA AI)*
