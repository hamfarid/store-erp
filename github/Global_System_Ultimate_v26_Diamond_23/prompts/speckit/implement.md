 (v15.9.8)
**Verified Feb 2026 Standard**

## 1. Context Loading
*   **Input:** `TASKS.md` (Current Task).
*   **Action:** Load relevant files.
*   **Constraint:** Respect `CONTEXT_LIMIT` (128k).

## 2. Implementation Strategy (EDD)
*   **First Step:** Write the failing eval (`promptfoo`).
*   **Second Step:** Write the code to pass the eval.
*   **Constraint:** Do NOT write code without an eval.

## 3. Anti-Hallucination (FORGE '26)
*   **Check:** Verify imports against `requirements.txt`.
*   **Repair:** Use Deterministic AST Analysis if available.
*   **Forbidden:** "Chain-of-Vibes", "FastAPI 2.0".

## 4. Output
*   **File:** Source Code + Test File.
*   **Commit:** "feat: implement X (pass^k verified)".
