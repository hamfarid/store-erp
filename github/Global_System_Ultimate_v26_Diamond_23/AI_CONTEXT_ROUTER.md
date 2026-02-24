# AI Context Router

**Version:** Dynamic (Verified Feb 2026)
**Engine:** Speckit Swarm Intelligence
**Status:** MANDATORY

## 🗺️ Purpose
This file acts as the **Central Nervous System** for the Autonomous Engineer. It directs the AI to the exact set of files required for a specific domain or task type, preventing context overload and ensuring no critical rule is missed.

## 🚦 Routing Logic

### 1. 🖥️ Frontend Development (React 19.2+)
**Trigger:** Task involves UI, Components, CSS, State Management, Client-side Logic.
**Mandatory Context:**
*   `prompts/43_ui_ux_testing.md` (Testing Standards)
*   `prompts/65_internationalization.md` (i18n Rules)
*   `prompts/68_pwa.md` (PWA Standards)
*   `rules/frontend.md` (General Frontend Rules)
*   `memory-bank/techContext.md` (Tech Stack)

### 2. ⚙️ Backend Development (FastAPI 0.129+)
**Trigger:** Task involves API, Database, Server Logic, Authentication, Background Jobs.
**Mandatory Context:**
*   `prompts/23_api.md` (API Design)
*   `prompts/30_security.md` (Security Hardening)
*   `prompts/44_database_testing.md` (DB Tests)
*   `prompts/53_rate_limiting.md` (Throttling)
*   `prompts/81_error_handling.md` (Exception Handling)
*   `rules/backend.md` (General Backend Rules)

### 3. 🗄️ Database Engineering (PostgreSQL 18.2)
**Trigger:** Task involves Schema Design, Migrations, Queries, Indexing.
**Mandatory Context:**
*   `prompts/77_database_migrations.md` (Migration Safety)
*   `prompts/76_performance_optimization.md` (Query Tuning)
*   `rules/database.md` (General DB Rules)

### 4. 🧪 Quality Assurance (Pytest-AsyncIO)
**Trigger:** Task involves Writing Tests, Debugging, QA, Verification.
**Mandatory Context:**
*   `prompts/49_acceptance_testing.md` (E2E)
*   `prompts/48_regression_testing.md` (Regression)
*   `prompts/37_penetration_testing.md` (Security Tests)
*   `rules/testing.md` (General Testing Rules)

### 5. 🚀 DevOps & Deployment (Docker/MCP)
**Trigger:** Task involves CI/CD, Docker, Cloud, Release.
**Mandatory Context:**
*   `prompts/78_ci_cd_pipeline.md` (Pipeline Config)
*   `prompts/26_docker.md` (Containerization)

## 🔄 Universal Context (ALWAYS LOAD)
Regardless of the task, the following MUST be loaded:
1.  `AGENTS.md` (The Constitution)
2.  `memory-bank/activeContext.md` (The Current Focus)
3.  `TASKS/UNIVERSAL_LIFECYCLE.md` (The Plan)
4.  `rules/99_anti_hallucination.md` (The Law)

## 🤖 Execution Protocol
1.  **Identify Domain:** Determine if the task is Frontend, Backend, DB, QA, or DevOps.
2.  **Load Universal Context:** Read the "Universal Context" files.
3.  **Load Domain Context:** Read the "Mandatory Context" files for the identified domain.
4.  **Execute:** Proceed with `speckit.py swarm --goal "..."`.
