 (v15.9.8)
**Verified Feb 2026 Standard**

## 1. Python (Ruff + Bandit)
*   **Linter:** `ruff check .` (v0.15.1).
*   **Security:** `bandit -r .` (1.9.3).
*   **Docstrings:** Google Style (Mandatory).
*   **Type Hints:** Mandatory for all functions.

## 2. TypeScript/JS (Biome)
*   **Linter:** `biome check src/` (v2.3.15).
*   **Strict Mode:** Enabled.
*   **No Any:** Avoid `any` type at all costs.

## 3. Testing (EDD)
*   **Evals:** `promptfoo` for logic.
*   **Unit:** `pytest` / `vitest`.
*   **E2E:** `playwright`.

## 4. Documentation
*   **README:** Every folder must have one.
*   **Comments:** Explain "Why", not "What".
