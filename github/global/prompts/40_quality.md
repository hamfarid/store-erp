# Code Quality & Best Practices (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System v26 Diamond 32 + Sentinel
**Status:** MANDATORY

## 1. Code Style (Speckit Verify)
*   **Python:** PEP 8 (Enforced by `flake8`, `black`).
*   **TypeScript:** ESLint + Prettier.
*   **Rule:** No style violations allowed. Sentinel blocks commits.

## 2. Type Safety
*   **Python:** `mypy --strict`. No `Any` allowed without explicit justification.
*   **TypeScript:** `strict: true`. No `any` allowed.

## 3. Complexity Limits
*   **Function:** Max 50 lines.
*   **File:** Max 300 lines.
*   **Cyclomatic Complexity:** Max 10.

## 4. Code Review Checklist (Sentinel)
*   [ ] Tests pass?
*   [ ] Coverage > 90%?
*   [ ] No secrets?
*   [ ] No TODOs?
*   [ ] Docs updated?

## 5. Refactoring
*   **Rule:** Refactor *before* adding features.
*   **Boy Scout Rule:** Leave the code cleaner than you found it.
