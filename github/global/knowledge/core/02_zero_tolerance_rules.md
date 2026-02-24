# Zero-Tolerance Rules (Global System v26 Diamond 32)

These rules are **NON-NEGOTIABLE** and must be enforced at all times by all agents and developers working within the Global System. Violations are considered critical failures.

## 1. Security
*   **No Hardcoded Secrets:** API keys, passwords, and tokens MUST be in `.env` files, never in code.
*   **No SQL Injection:** ALWAYS use parameterized queries or ORMs. NEVER concatenate strings into SQL.
*   **No XSS Vulnerabilities:** ALWAYS escape user input. Use framework-provided sanitization.
*   **No CSRF Vulnerabilities:** Ensure CSRF protection is enabled on all state-changing endpoints.

## 2. Code Quality
*   **No Unhandled Errors:** Every Promise must have a `.catch()` or `try/catch` block. No silent failures.
*   **No Missing Tests:** Minimum **95%** code coverage is required for core logic.
*   **No Undocumented Code:** All public functions and classes MUST have docstrings/JSDoc.
*   **No Duplicate Code (DRY):** If logic is repeated 3 times, refactor it into a utility or component.
*   **No Magic Numbers:** Use named constants for all numeric or string literals.

## 3. Architecture
*   **No Direct DOM Manipulation:** In React/Vue/Angular, never touch the DOM directly (e.g., `document.getElementById`). Use refs.
*   **No Circular Dependencies:** Modules must not import each other in a loop.
*   **No God Objects:** Classes/Components should have a single responsibility (SRP).

## 4. Workflow
*   **No Uncommitted Changes:** Always commit work before switching contexts or finishing a task.
*   **No Bypassing Validation:** Frontend validation is for UX; Backend validation is for Security. BOTH are mandatory.
*   **No "Fix Later":** If you see a bug or code smell, fix it NOW or log it in `memory-bank/lessons.md`.
