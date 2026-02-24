# System Patterns (v26.0)

> **Purpose**: Document recurring architectural and design patterns used across the project
> **Updated**: Automatically by agents after significant architectural decisions
> **Version**: v26.0.2 (Diamond 32)

## Architecture Pattern (Dual-System & Microservices)

The system has evolved into a **Distributed Microservices Architecture** (Gaara-AI Ecosystem) running on a **Tailscale Mesh VPN**.

### 1. The Core Monolith (Legacy ERP)
*   **Framework:** Django (60+ Modules).
*   **Role:** Core business logic, data persistence, legacy workflows.
*   **Pattern:** Modular Monolith with strict boundary enforcement.

### 2. The AI Microservices (New Intelligence)
*   **Framework:** FastAPI (Python) + Node.js (Avatar/Scraper).
*   **Communication:** REST APIs via Cloudflare Tunnel & Tailscale.
*   **Containerization:** Docker with Multi-Stage Builds (Builder -> Runtime).

### 3. The Dual-System Financial Engine
*   **Backend:** FastAPI ML Service (Prediction Engine).
*   **Frontend:** React/Express (Visualization Dashboard).
*   **Pattern:** Decoupled Frontend/Backend with shared data contracts.

## Service Layer Pattern

All business logic resides in **service classes**, not in views or serializers. Views are thin (request parsing + response formatting only). Services handle validation, business rules, database operations, and external API calls. This pattern enables unit testing of business logic without HTTP overhead.

## Error Handling Pattern

All errors follow a structured response format: `{ "error": { "code": "ERR_XXX", "message": "...", "details": [...] } }`. Error codes are cataloged in `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` and domain-specific catalogs in `errors/ml/`. Every external call, file operation, and database query has explicit error handling with meaningful messages.

## Authentication Pattern

*   **User Auth:** JWT-based authentication with token refresh.
*   **Service Auth:** Zero Trust via Cloudflare Access & Tailscale ACLs.
*   **API Keys:** Managed via `secrets` module, never hardcoded.

## ML Pipeline Pattern (Dual-System)

### Plant Disease Detection
`Image → Quality Gate → Binarization (5 views) → Multi-Crop (10 views) → Feature Extraction → Embedding → Classification → GradCAM → Similarity Search → Report`.

### Financial Forecasting (New)
`Data Ingestion (Daily) → Feature Engineering → Model Training (ARIMA/LSTM/Prophet) → Ensemble Weighting → Inference API → React Dashboard`.

## Drift-Adapter Pattern

When embedding drift is detected (centroid shift > 0.05), the system follows: `Alert → Accuracy Check → Collect 50 samples → Fine-tune (80% new + 20% original via Experience Replay) → Validate all classes (no class drops > 3%) → Deploy or Rollback → Log event`. Maximum one retraining per month to prevent thrashing.

## Agent Coordination Pattern

Multi-agent workflows follow the sequential chain: Architect (01) → Developer (02) → Reviewer (03) → QA (04). Swarm Intelligence Coordinator manages parallel execution and conflict resolution. Role boundaries are strictly enforced — agents cannot perform tasks outside their defined scope.

## Memory Bank Pattern

Project state is persisted across sessions in `memory-bank/`. `activeContext.md` holds current task state. `systemPatterns.md` (this file) holds recurring patterns. `techContext.md` holds technology stack details. `projectBrief.md` holds project mission and objectives. Agents must read relevant memory bank files before acting on any task.
