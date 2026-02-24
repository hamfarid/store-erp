# Acceptance Testing Prompt (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System v26 Diamond 32
**Status:** MANDATORY

## Purpose
Verify requirements are met using automated acceptance tests, integrated with Speckit.

## Instructions
1.  **Source:** Review requirements from `specs/*.spec.md` and `todo.md`.
2.  **Criteria:** Define Gherkin-style acceptance criteria (Given/When/Then).
3.  **Automation:** Implement tests using Playwright (E2E) or Pytest (Integration).
4.  **Verification:** Run `speckit verify` to execute acceptance tests.
5.  **Logging:** Results are automatically logged by Speckit to `system_log.md`.

## Acceptance Criteria (Speckit Verify)
*   **Functional:** All user stories pass automated tests.
*   **Non-Functional:** Performance and security requirements met (Sentinel).
*   **Business:** Business logic validated against specs.

## Output
*   Automated test report (HTML/JSON).
*   Updated `todo.md` (mark feature as accepted).
