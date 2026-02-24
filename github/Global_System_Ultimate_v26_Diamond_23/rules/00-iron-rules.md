 (v26.0 Diamond 30)
**Verified Feb 2026 Standard**

## 1. The Golden Rule: EDD
*   **Rule:** No code shall be written without a failing eval (`promptfoo`).
*   **Penalty:** Code without evals will be rejected by `CrossCheck`.

## 2. The Silver Rule: BATS
*   **Rule:** Every plan must estimate token cost.
*   **Action:** Use `speckit.py plan` to calculate budget.

## 3. The Bronze Rule: Context
*   **Rule:** No file shall exceed 200 LOC.
*   **Action:** Refactor large files immediately.
*   **Limit:** Total context must stay under 128k tokens.

## 4. The Iron Rule: Ports
*   **Rule:** NEVER hardcode ports (e.g., 8000, 3000).
*   **Action:** Use `genesis.py` or environment variables.

## 5. The Steel Rule: Hallucinations
*   **Rule:** Verify every import against `requirements.txt`.
*   **Action:** Use `FORGE` logic to repair broken imports.
