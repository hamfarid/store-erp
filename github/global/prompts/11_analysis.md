# Prompt 11: Project Analysis

=================================================================================
PROJECT ANALYSIS - Existing Project Analysis Global System v26 Diamond 32 (Synchronized Intelligence Edition)
=================================================================================

Version: Dynamic
Type: Core - Analysis
Roles: Architect, Sequential Thinker, Agentic Engine

This prompt guides the deep analysis of existing projects, leveraging **Speckit Global System v26 Diamond 32**, **Sequential Thinking**, and the **Architect Role**.

=================================================================================
OVERVIEW
=================================================================================

When a user provides an existing project, this prompt helps you:
1.  **Deconstruct** the project structure using the Architect's mindset.
2.  **Analyze** the technology stack and dependencies.
3.  **Evaluate** code quality and architectural integrity.
4.  **Plan** the migration or upgrade path using Sequential Thinking.

=================================================================================
ANALYSIS WORKFLOW
=================================================================================

## Step 1: The Agentic Scan (Initial Assessment)

**Role:** The Architect
**Tool:** `speckit.py analyze`

1.  **Run the Agentic Engine:**
    ```bash
    python3 global/tools/speckit.py analyze
    ```
    *   This automatically runs `project_analyzer.py` and `memory_service.py`.
    *   It maps the territory and recalls past context.

2.  **Identify the Core:**
    *   Is it Monolithic or Microservices?
    *   What is the primary design pattern (MVC, MVVM, Clean Arch)?
    *   Where are the architectural bottlenecks?

## Step 2: Sequential Deep Dive (Logic & Flow)

**Role:** Sequential Thinker
**Tool:** `sequential_thinking.py` (Mental Model)

1.  **Trace the Data Flow:**
    *   From Entry Point (API/UI) -> Controller -> Service -> Database.
    *   Identify where data is transformed and where it is validated.

2.  **Map the Dependencies:**
    *   Frontend: React/Vue/Angular? State Management?
    *   Backend: Django/FastAPI/Express? ORM?
    *   Infrastructure: Docker? K8s? Cloud?

## Step 3: Technology Detection (Detailed)

### Frontend Detection
*   **React:** Look for `package.json` ("react"), `src/App.tsx`, JSX/TSX.
*   **Vue:** Look for `package.json` ("vue"), `src/App.vue`, `.vue` files.
*   **Angular:** Look for `angular.json`, `src/app/app.component.ts`.

### Backend Detection
*   **Django:** Look for `manage.py`, `settings.py`, `urls.py`.
*   **FastAPI:** Look for `main.py` (FastAPI instance), `pydantic` models.
*   **Express:** Look for `app.js`, `server.js`, `express` dependency.

### Database Detection
*   **PostgreSQL:** `psycopg2`, `pg`, connection strings.
*   **MongoDB:** `pymongo`, `mongoose`.
*   **Redis:** `redis-py`, `ioredis`.

## Step 4: Code Quality & Security Audit

**Role:** The Critic
**Tools:** `speckit.py verify` (CodeRabbit + Sentinel)

1.  **Run Verification:**
    ```bash
    python3 global/tools/speckit.py verify
    ```
    *   **Sentinel:** Checks for secrets and TODOs.
    *   **CodeRabbit:** Checks for complexity, coverage, and vulnerabilities.

2.  **Analyze Metrics:**
    *   Cyclomatic Complexity.
    *   Test Coverage (pytest/jest).
    *   Security Vulnerabilities (OWASP Top 10).

## Step 5: The Migration Plan (Sequential Output)

Generate a step-by-step plan to upgrade or integrate this project into the Global System:

1.  **Phase 1: Stabilization** (Fix critical bugs, add tests).
2.  **Phase 2: Standardization** (Apply Global Rules, formatting).
3.  **Phase 3: Optimization** (Refactor architecture, improve performance).

=================================================================================
ANALYSIS OUTPUT
=================================================================================

Generate a **Project Analysis Report** containing:
1.  **Executive Summary:** High-level overview for stakeholders.
2.  **Architectural Diagram:** Mermaid chart of the system.
3.  **Tech Stack Matrix:** Detailed list of all technologies.
4.  **Risk Assessment:** Critical, High, Medium, Low risks.
5.  **Action Plan:** The roadmap for the future.
