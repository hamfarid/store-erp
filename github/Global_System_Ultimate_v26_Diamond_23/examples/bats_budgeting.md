 (v15.9.8)
**Verified Feb 2026 Standard**

## Scenario: Implement a "Summarize PDF" Feature

### 1. Estimate Token Cost
*   **Input:** 10-page PDF (~5000 tokens).
*   **Output:** 1-page summary (~500 tokens).
*   **Model:** Claude 3.5 Sonnet ($3/M input, $15/M output).

### 2. Calculate Budget
*   **Input Cost:** (5000 / 1M) * $3 = $0.015
*   **Output Cost:** (500 / 1M) * $15 = $0.0075
*   **Total:** $0.0225 per run.

### 3. Optimize (Model Cascading)
*   **Can we use Haiku?** Yes, summarization is simple.
*   **Haiku Cost:** ($0.25/M input, $1.25/M output).
*   **New Total:** $0.00125 + $0.000625 = $0.001875 (~12x cheaper!).

### 4. Decision
*   **Action:** Use `model: claude-3-haiku-20240307` in `speckit.py`.
