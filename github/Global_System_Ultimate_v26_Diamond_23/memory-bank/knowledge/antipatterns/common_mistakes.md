# Common Anti-Patterns (Global System Ultimate Synchronized Intelligence Edition)

## 1. The God Object
*   **Description:** A single class that does everything (e.g., `SystemManager`).
*   **Why it's bad:** Impossible to test, maintain, or extend.
*   **Fix:** Break it down using Single Responsibility Principle (SRP).

## 2. Hardcoded Secrets
*   **Description:** `API_KEY = "sk-12345"` inside the code.
*   **Why it's bad:** Security risk if committed to Git.
*   **Fix:** Use Environment Variables (`os.getenv("API_KEY")`).

## 3. Spaghetti Code
*   **Description:** Unstructured, tangled control flow (GOTO statements, deep nesting).
*   **Why it's bad:** Unreadable and fragile.
*   **Fix:** Refactor into small, named functions.

## 4. Magic Numbers
*   **Description:** `if status == 4:`
*   **Why it's bad:** What does `4` mean?
*   **Fix:** Use named constants (`STATUS_COMPLETED = 4`).
