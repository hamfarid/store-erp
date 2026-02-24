# Code Review Prompt Global System v26 Diamond 32 (Synchronized Intelligence Edition)

## Purpose
Perform comprehensive, AI-assisted code review before merging, leveraging **CodeRabbit**, **Sentinel**, and the **Critic Role**.

## Roles & Responsibilities
*   **The Critic (Primary):** Leads the review, challenges assumptions, and demands perfection.
*   **CodeRabbit (Tool):** Performs automated static analysis, security scanning, and logic verification.
*   **Sentinel (Tool):** Enforces the Zero-Error Policy (No TODOs, No Secrets).

## Instructions
1.  **Activate the Critic Role:**
    *   Adopt a skeptical, rigorous mindset.
    *   Assume the code is broken until proven otherwise.

2.  **Run Automated Analysis (Speckit Verify):**
    *   **Command:** `python3 global/tools/speckit.py verify`
    *   **Action:** This runs both `coderabbit_reviewer.py` and `sentinel.py`.
    *   **Analyze Output:**
        *   **Sentinel:** MUST be clean (No TODOs, No Secrets).
        *   **CodeRabbit:** MUST have 0 High/Critical issues.

3.  **Manual Deep Dive (The Critic's Eye):**
    *   **Check against Rules:** Verify compliance with `global/rules/`.
    *   **Test Coverage:** Ensure coverage >= 80% (reject if lower).
    *   **Documentation:** Verify docstrings exist for every function and class.
    *   **Complexity:** Reject functions with Cyclomatic Complexity > 10.

4.  **Security Audit:**
    *   Check for hardcoded secrets (Sentinel does this, but double-check).
    *   Verify input validation.
    *   Ensure proper error handling (no silent failures).

5.  **Log Results:**
    *   Record findings in `system_log.md`.
    *   Update `docs/review_report.md`.

## Review Checklist
- [ ] **Sentinel Scan:** Passed (No TODOs, No Secrets).
- [ ] **CodeRabbit Scan:** Passed with 0 High/Critical issues.
- [ ] **Test Coverage:** >= 80%.
- [ ] **Linting:** Clean (flake8/eslint).
- [ ] **Documentation:** Complete and accurate.

## Output
- **Review Report:** Detailed markdown report in `docs/`.
- **Fix List:** Prioritized list of required changes.
- **Decision:** APPROVE / REQUEST CHANGES / REJECT.
