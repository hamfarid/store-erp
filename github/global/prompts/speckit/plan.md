# Speckit Plan
 (v26.0.2 Diamond 32 GAARA AI)
**Verified Feb 2026 Standard**

## 1. Goal Analysis
*   **Input:** User Goal.
*   **Action:** Decompose into atomic requirements.
*   **Constraint:** Check `memory-bank/systemContext.md` for conflicts.

## 2. Evaluation Strategy (EDD)
*   **Mandatory:** Define success criteria using `pass^k` (Reliability).
*   **Action:** Create a `promptfoo` config for this plan.
*   **Example:** "Login must succeed 10/10 times with valid creds."

## 3. Cost Estimation (BATS)
*   **Budget:** Estimate token usage for this plan.
*   **Optimization:** Can we use a smaller model (Haiku) for parts of this?
*   **Alert:** If estimated cost > $5, flag for user approval.

## 4. Architecture & Ports
*   **Smart Ports:** Do NOT assign static ports. Use `genesis.py` logic.
*   **Containers:** Check `docker-compose.shared.yml` for existing services.

## 5. Output
*   **File:** `memory-bank/activeContext.md`
*   **Format:** Markdown with clear "Next Steps".
