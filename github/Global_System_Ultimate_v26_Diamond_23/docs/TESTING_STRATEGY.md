# Testing Strategy (Global System Ultimate Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System Ultimate
**Status:** MANDATORY

## 1. Overview
This document outlines the testing strategy for the Global System Ultimate, ensuring we meet our quality standards, including a minimum of 80% code coverage, enforced by `speckit verify`.

## 2. Testing Levels (The Pyramid)

### 2.1. Unit Tests (60%)
-   **Purpose:** Test individual functions/components in isolation.
-   **Framework:** PyTest (Python), Jest (JS/TS).
-   **Execution:** `speckit verify --unit`

### 2.2. Integration Tests (30%)
-   **Purpose:** Test interactions (API <-> DB).
-   **Framework:** PyTest, Supertest.
-   **Execution:** `speckit verify --integration`

### 2.3. End-to-End (E2E) Tests (10%)
-   **Purpose:** Test complete user flows.
-   **Framework:** Playwright (Mandatory).
-   **Execution:** `speckit verify --e2e`

## 3. Code Coverage
-   **Target:** 80% minimum.
-   **Enforcement:** `speckit verify` fails if coverage < 80%.

## 4. The "Sentinel" Check
Before any code is merged, `sentinel.py` runs to ensure:
1.  No TODOs.
2.  No Secrets.
3.  Tests Pass.
4.  Coverage Met.

## 5. Bug Triage
-   **Critical:** Fix immediately (Stop the Line).
-   **High:** Fix within 24h.
-   **Medium:** Fix in next sprint.
-   **Low:** Backlog.
