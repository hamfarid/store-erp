 (v15.9.8)
**Verified Feb 2026 Standard**

## 1. Task Breakdown
*   **Input:** `memory-bank/activeContext.md` (The Plan).
*   **Action:** Convert plan steps into executable tasks.
*   **Constraint:** Each task must be < 200 LOC.

## 2. Task Metadata (EDD)
*   **Eval:** Define the `promptfoo` test case for this task.
*   **Example:** "Task: Implement Login -> Eval: `test_login_success`"

## 3. Task Metadata (BATS)
*   **Model:** Suggest the optimal model (Haiku/Sonnet/Opus).
*   **Cost:** Estimated token usage.

## 4. Output
*   **File:** `TASKS.md`
*   **Format:** Checklist with [ ] and metadata.
