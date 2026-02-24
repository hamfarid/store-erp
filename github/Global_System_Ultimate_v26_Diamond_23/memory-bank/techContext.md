# Tech Context (v26.0)

> **Purpose**: Document the technology stack, tool versions, and infrastructure decisions
> **Updated**: After any technology change or version upgrade
> **Version**: v26.0.0 (Diamond 9)

## Backend Stack

The primary backend framework is **Django** with **Django REST Framework (DRF)** for API development. **Python 3.11+** is the required runtime. Database is **PostgreSQL 15+** with Django ORM as the primary data access layer. Background task processing uses **Celery** or **Django-Q** with **Redis** as the message broker.

## Frontend Stack

Frontend technology selection is project-dependent. The framework supports **React**, **Next.js**, or **Vue.js**. Build tools: **Vite** (preferred) or Next.js built-in bundler. **TypeScript** is required for all frontend code. Testing: **Vitest** for unit tests, **Playwright** for E2E tests.

## ML/AI Stack (Pinned Versions)

Machine learning pipeline uses pinned tool versions per `rules/ml/RULES-plant-disease-analysis.md`.
-   **PyTorch**: 2.1.0
-   **TorchVision**: 0.16.0
-   **TIMM**: 0.9.10
-   **Albumentations**: 1.3.1 (AGPL license — verify compatibility)
-   **OpenCV**: 4.8.0
-   **DINOv2**: ViT-B/14 is the primary embedding model (768 dimensions).
-   **Vector databases**: ChromaDB (< 500K vectors), Qdrant (500K-5M), Milvus (> 5M).

## Infrastructure

Containerization uses **Docker** with multi-stage builds for production images. CI/CD via **GitHub Actions** with all actions pinned by SHA (not tag) per CVE-2025-30066 lesson. Container security scanning with **Trivy**. Secret management via **HashiCorp Vault** or cloud-native secrets managers. All infrastructure defined as code (**Terraform/Ansible**).

## Development Tools

-   **Code quality**: Ruff (Python linter/formatter), Biome (JS/TS linter).
-   **Type checking**: mypy (Python), tsc (TypeScript).
-   **Security scanning**: Bandit (Python), Semgrep CE (multi-language), Gitleaks (secret detection), pip-audit (dependency vulnerabilities).
-   **Project governance**: Speckit (`analyze`, `verify`, `plan`, `implement` commands).

## Monitoring & Observability

-   **Application monitoring**: Sentry for error tracking and performance monitoring.
-   **Metrics**: Prometheus + Grafana for infrastructure and application metrics.
-   **ML experiment tracking**: MLflow or Weights & Biases for model versioning, metrics logging, and artifact storage.

## Data Storage

-   **Primary database**: PostgreSQL with Django migrations for schema management.
-   **Object storage**: S3-compatible (AWS S3 or MinIO) for images and model artifacts.
-   **Vector storage**: ChromaDB/Qdrant/Milvus based on scale requirements.
-   **Cache layer**: Redis for session data, task queues, and application caching.
