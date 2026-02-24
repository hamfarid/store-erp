# Testing Strategy (Global System v26 Diamond 32)

## Core Philosophy
**"Test First, Fix Never."** We believe that robust automated testing is the only way to ensure long-term velocity and reliability. We adhere to the **Test Pyramid** principle.

## The Test Pyramid

### 1. Unit Tests (60%)
*   **Scope:** Individual functions, classes, and components in isolation.
*   **Speed:** Extremely fast (milliseconds).
*   **Tools:** Jest, Vitest (JS/TS), PyTest (Python), JUnit (Java).
*   **Mocking:** Heavy use of mocks/stubs for external dependencies.

### 2. Integration Tests (30%)
*   **Scope:** Interaction between modules (e.g., Service + Database, Controller + Service).
*   **Speed:** Moderate (seconds).
*   **Tools:** Supertest, TestContainers, React Testing Library.
*   **Environment:** Uses real or containerized databases/services.

### 3. End-to-End (E2E) Tests (10%)
*   **Scope:** Full user flows from UI to Database and back.
*   **Speed:** Slow (minutes).
*   **Tools:** Playwright (Preferred), Cypress, Selenium.
*   **Environment:** Staging-like environment.

## Coverage Requirements

*   **Critical Core Logic:** 100% Branch Coverage.
*   **General Business Logic:** 95% Line Coverage.
*   **UI Components:** 80% Component Coverage.
*   **Overall Project Target:** **95%+**

## Testing Workflow

1.  **Red:** Write a failing test that defines the desired behavior.
2.  **Green:** Write the minimum code necessary to pass the test.
3.  **Refactor:** Clean up the code while keeping the test passing.
4.  **Commit:** Never commit code without passing tests.

## Continuous Integration (CI)

*   All tests must run automatically on every Pull Request.
*   Builds must fail if tests fail or coverage drops below the threshold.
*   Linting and static analysis should run before tests.
