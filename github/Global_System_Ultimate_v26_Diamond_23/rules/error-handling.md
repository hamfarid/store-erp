# 🔧 Error Handling Rules (Global System Ultimate)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel & CodeRabbit

## 1. The Philosophy
Errors are not accidents; they are unhandled states. We do not "try" to fix them; we "engineer" them away.

## 2. The Protocol (3-Strike Rule)
1.  **Strike 1 (Internal Fix):** Analyze the stack trace. Fix the logic.
2.  **Strike 2 (Context Check):** Read `rules/` and `memory-bank/lessons.md`. Did you miss a pattern?
3.  **Strike 3 (External Search):** Use `search` tool. Find the definitive solution.
4.  **Strike 4 (Escalation):** Ask the user. Do NOT hallucinate a fix.

## 3. Mandatory Practices
*   **No Silent Failures:** `try/catch` blocks MUST log the error or rethrow it. Empty catch blocks are FORBIDDEN.
*   **Specific Exceptions:** Catch specific exceptions (e.g., `ValueError`), not generic `Exception`.
*   **User-Facing Messages:** Errors shown to users MUST be sanitized (no stack traces).

## 4. The "Don't Make This Error Again" Protocol
*   **Log It:** Every fixed error MUST be logged in `memory-bank/lessons.md`.
*   **Learn It:** Update `rules/` if the error was caused by a missing rule.
*   **Prevent It:** Add a test case that reproduces the error, then fix it.
