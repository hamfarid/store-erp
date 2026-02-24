# Speckit Verify
 (v26.0.2 Diamond 32 GAARA AI)
**Verified Feb 2026 Standard**

## 1. Static Analysis
*   **Python:** Run `ruff check .` (v0.15.1).
*   **JS/TS:** Run `biome check src/` (v2.3.15).
*   **Security:** Run `bandit -r .` (1.9.3).

## 2. Dynamic Evaluation (EDD)
*   **Tool:** `promptfoo eval`.
*   **Metric:** `pass^k` (Reliability).
*   **Threshold:** Must be > 0.9 (90% success).

## 3. Context Health
*   **Check:** Run `speckit.py verify`.
*   **Action:** If context > 128k, trigger compaction.

## 4. Output
*   **Report:** `SYSTEM_ASSURANCE_REPORT.md`.
*   **Status:** ✅ Verified or ❌ Failed.
