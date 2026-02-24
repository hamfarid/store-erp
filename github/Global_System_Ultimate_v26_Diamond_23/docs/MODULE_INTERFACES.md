# Module Interfaces Documentation (v26.0)

> **Scope**: Cross-Module Communication Contracts
> **Audience**: All Agents — Architect, Developer, Reviewer
> **Version**: v26.0.0 (Diamond 9)

## Purpose

This document defines the interfaces between major system modules to ensure clean boundaries, prevent tight coupling, and enable independent development and testing of each module.

## Interface Principles

All module interfaces must follow these principles:
-   Contracts defined before implementation.
-   Backward compatibility maintained across versions.
-   Changes require Architect approval and Reviewer validation.
-   All interfaces documented with input/output types.

## Core Module Interfaces

### Authentication Module → All Modules
**Interface**: JWT Token Validation.
**Contract**: Every protected endpoint receives a JWT token in the `Authorization: Bearer <token>` header. The token payload contains `user_id`, `role`, `permissions[]`, and `exp` (expiration). All modules must validate the token before processing any request.

### API Gateway → Backend Services
**Interface**: RESTful HTTP with JSON payloads.
**Contract**: All requests include `Content-Type: application/json`. Rate limiting headers included in all responses (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`). Error responses follow standard format: `{ "error": { "code": "ERR_XXX", "message": "...", "details": [...] } }`.

### Backend Services → Database
**Interface**: Django ORM (preferred) or raw SQL (Architect-approved exceptions only).
**Contract**: All queries use parameterized statements (no string interpolation for SQL). Read operations use `select_related()` / `prefetch_related()` to prevent N+1 queries. Write operations use database transactions for multi-table updates.

### Backend Services → ML Pipeline
**Interface**: Async task queue (Celery/Django-Q).
**Contract**: Image submitted as task with `image_id`, `image_path`, `analysis_type`, `priority`. Pipeline returns result as structured JSON with `prediction`, `confidence`, `embedding_id`, `heatmap_path`, `similar_images[]`. Timeout: 30 seconds for standard, 120 seconds for high-accuracy mode.

### ML Pipeline → Vector Database
**Interface**: Vector DB client SDK (ChromaDB/Qdrant/Milvus per scale).
**Contract**: All embeddings are 768-dimensional, L2-normalized float32 vectors. Metadata schema defined in `rules/ml/RULES-embedding-storage.md` Section 4.2. Insertion batch size ≤ 1000 (ChromaDB) or ≤ 10000 (Qdrant/Milvus).

### Notification Module → External Services
**Interface**: Event-driven (message queue or webhook).
**Contract**: Critical disease alerts (e.g., Late Blight) trigger SMS and email notifications. Notification payload: `{ "alert_type", "disease", "confidence", "image_id", "timestamp", "location" }`. Delivery confirmation required within 60 seconds.

## Interface Change Management

Any interface change requires:
1.  Architect approval with ADR documenting the change rationale.
2.  Backward-compatible implementation (old interface supported for minimum 1 release cycle).
3.  Reviewer validation that all consuming modules are updated.
4.  QA regression testing on all affected integration points.

## Cross-References

-   **API Design**: `roles/ROLE-api-designer.md`
-   **Backend Implementation**: `roles/ROLE-backend-specialist.md`
-   **ML Pipeline Workflow**: `workflows/ml/ML_MULTI_VIEW_WORKFLOW.md`
-   **Embedding Storage**: `rules/ml/RULES-embedding-storage.md`
