 (v15.9.8)

**GOAL:** Ensure that updates, features, and fixes are deployed without breaking existing functionality or causing downtime.

## 1. CHANGE MANAGEMENT (Feature Flags)
*   **Principle:** Decouple Deployment from Release.
*   **Mechanism:** Use Feature Flags (e.g., LaunchDarkly, Unleash, or simple env vars) to toggle new features.
*   **Workflow:**
    1.  Deploy code with the feature flag **OFF**.
    2.  Verify in production (can be enabled for internal users only).
    3.  Gradually roll out to 10%, 50%, 100% of users.
    4.  If issues arise, kill the switch instantly (no rollback needed).

## 2. API VERSIONING (Backward Compatibility)
*   **Principle:** Never break existing clients.
*   **Strategy:**
    *   **URI Versioning:** `/api/v1/users` vs `/api/v2/users`.
    *   **Header Versioning:** `Accept: application/vnd.myapi.v2+json`.
*   **Rule:**
    *   **Additive Changes:** Safe to add new fields to JSON responses.
    *   **Breaking Changes:** MUST be in a new API version.
    *   **Deprecation:** Mark old fields as `@deprecated` and support them for at least 6 months.

## 3. CONTAINER UPDATES (Zero-Downtime)
*   **Strategy:**
    *   **Rolling Update:** Replace instances one by one. (K8s default).
    *   **Blue-Green Deployment:**
        *   **Blue:** Current live version.
        *   **Green:** New version (idle).
        *   **Switch:** Route traffic from Blue to Green instantly.
        *   **Rollback:** Route traffic back to Blue if Green fails.
*   **Health Checks:**
    *   **Liveness Probe:** Is the container running?
    *   **Readiness Probe:** Is the container ready to accept traffic? (DB connected, cache warm).

## 4. REGRESSION TESTING
*   **Principle:** New code must not break old features.
*   **Requirement:**
    *   **Unit Tests:** Run on every commit.
    *   **Integration Tests:** Run on every PR.
    *   **E2E Tests:** Run before deployment (Staging).
*   **Golden Rule:** If a bug is found in production, write a test case for it FIRST, then fix it.

## 5. DATABASE MIGRATIONS
*   **Principle:** Database schema changes must be backward compatible.
*   **Workflow:**
    1.  **Expand:** Add new columns/tables (nullable).
    2.  **Migrate:** Copy data/logic to new structure (dual write).
    3.  **Contract:** Remove old columns/tables (after code is fully updated).
*   **Constraint:** Never rename a column in a single deployment. Add new -> Copy -> Deprecate old -> Remove old.

---
*Signed,*
*The Global Professional Engineer*
