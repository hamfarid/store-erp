# Plan: Comprehensive System Test
**Version:** 1.0
**Visual Hash:** 9a8b7c6d (Matches Spec)

## 1. Architecture & Design
This plan focuses on a non-invasive, discovery-based testing approach. We will use a "Probe & Report" architecture.
*   **Probe:** Scripts that check for file existence and configuration validity.
*   **Executor:** Wrappers around standard test runners (`npm test`, `pytest`).
*   **Reporter:** A centralized aggregator that compiles results into Markdown.

## 2. Component Analysis (Predictive)
*   **Frontend:** Expect `package.json`. Will use `npm` commands.
    *   *Risk:* Missing dependencies. *Mitigation:* Run `npm install` if needed (ask user first? No, Constitution says non-destructive, but install is usually safe. We will check `node_modules` first).
*   **Backend:** Expect `requirements.txt` or `pyproject.toml`.
    *   *Risk:* Virtual environment missing. *Mitigation:* Use `python3` directly if venv not found, or warn.
*   **Database:** Expect `.env` or `docker-compose.yml`.
    *   *Risk:* DB not running. *Mitigation:* Check port connectivity (e.g., 5432) before trying to connect.

## 3. Step-by-Step Implementation Strategy
1.  **Audit Phase:** Create `scripts/audit_system.py` to scan and identify components.
2.  **Frontend Test Phase:** If Frontend detected, run `npm run lint` and `npm run build`. Capture stdout/stderr.
3.  **Backend Test Phase:** If Backend detected, run `pytest`. Capture stdout/stderr.
4.  **Reporting Phase:** Create `scripts/generate_report.py` to parse logs and write `reports/test_summary.md`.

## 4. Verification Plan
*   **Success:** `reports/test_summary.md` is generated and contains sections for all detected components.
*   **Failure:** Script crashes or fails to detect obvious components.
