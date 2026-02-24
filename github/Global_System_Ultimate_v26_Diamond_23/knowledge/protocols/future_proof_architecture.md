 (v15.9.8)

**Objective:** Design systems that can evolve, scale, and update without downtime or breaking changes.
**Version:** Global System Ultimate v15.9.8 (See VERSION file)

## 1. Core Principles

### 1.1 Decoupled Services (The "Lego" Philosophy)
*   **Rule:** Never build a monolith unless it's a "Modular Monolith" with strict boundary enforcement.
*   **Implementation:**
    *   **Frontend:** Must be a separate deployable unit (SPA/PWA) served via CDN/Edge.
    *   **Backend:** Must be API-first (REST/GraphQL/gRPC).
    *   **Database:** Must be treated as a shared resource with strict schema migration policies.
    *   **State:** Must be externalized (Redis/Memcached), never stored in-memory within the application container.

### 1.2 The Open/Closed Principle (Plugin Pattern)
*   **Rule:** Software entities should be open for extension, but closed for modification.
*   **Implementation:**
    *   **Hooks & Events:** Core logic should emit events (e.g., `USER_CREATED`) that other modules can listen to.
    *   **Dynamic Loading:** Support loading modules/plugins at runtime or startup without recompiling the core.
    *   **Interface-Based Design:** Define strict interfaces for all major components (Storage, Auth, Notification).

### 1.3 Sidecar Pattern (Non-Intrusive Updates)
*   **Rule:** Cross-cutting concerns (Logging, Monitoring, Security, Proxying) should run alongside the application, not inside it.
*   **Implementation:**
    *   **Service Mesh:** Use Envoy/Istio for traffic management, retries, and circuit breaking.
    *   **Log Shippers:** Run Fluentd/Filebeat as a sidecar to collect logs.
    *   **Security Proxies:** Handle mTLS and AuthN/AuthZ in a sidecar proxy.

### 1.4 API Versioning Strategy (Zero-Breaking Changes)
*   **Rule:** Once an API is public, it is immutable.
*   **Implementation:**
    *   **URI Versioning:** `/api/v1/resource` -> `/api/v2/resource`.
    *   **Header Versioning:** `Accept: application/vnd.myapi.v1+json`.
    *   **Deprecation Policy:** Support at least N-1 versions. Warn users via `Deprecation` headers 6 months before removal.

## 2. Zero-Downtime Deployment Strategies

### 2.1 Blue-Green Deployment
*   **Concept:** Run two identical environments (Blue = Live, Green = New).
*   **Process:** Deploy to Green -> Test Green -> Switch Router to Green -> Decommission Blue.
*   **Benefit:** Instant rollback if issues arise.

### 2.2 Canary Releases
*   **Concept:** Roll out the update to a small subset of users (e.g., 5%) first.
*   **Process:** Deploy v2 to 5% -> Monitor Metrics (Error Rate, Latency) -> If healthy, increase to 20%, 50%, 100%.
*   **Benefit:** Limits the blast radius of bugs.

### 2.3 Rolling Updates
*   **Concept:** Update instances one by one.
*   **Process:** Stop Instance A -> Update Instance A -> Start Instance A -> Repeat for B, C...
*   **Requirement:** Application must be stateless and backward compatible during the transition.

## 3. Database Evolution (The Hardest Part)

### 3.1 Expand-Contract Pattern
*   **Phase 1 (Expand):** Add new column/table. Code writes to BOTH old and new.
*   **Phase 2 (Migrate):** Backfill data from old to new.
*   **Phase 3 (Contract):** Code reads/writes ONLY to new. Remove old column/table.

### 3.2 Schema Versioning
*   All database changes must be versioned migrations (e.g., Flyway, Liquibase, Prisma).
*   Never use `DROP COLUMN` in the same deployment as code changes.

## 4. Infrastructure as Code (IaC)
*   **Rule:** All infrastructure (Servers, Load Balancers, DNS) must be defined in code (Terraform, Pulumi, K8s Manifests).
*   **Benefit:** Reproducible environments and disaster recovery.

---
**Mandate:** All new projects created by the AI Agent MUST adhere to this protocol.
