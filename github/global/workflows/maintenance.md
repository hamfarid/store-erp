# 🔧 Maintenance Workflow (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System v26 Diamond 32
**Status:** MANDATORY

## Workflow

```
Monitor → Analyze (Speckit) → Fix (Speckit) → Verify (Sentinel)
```

## Phase 1: Monitor & Detect
1.  **Logs:** Watch Sentry/CloudWatch.
2.  **Feedback:** User reports.
3.  **Alerts:** Automated system alerts.

## Phase 2: Analyze (Speckit)
1.  **Run Analysis:**
    ```bash
    python3 global/tools/speckit.py analyze
    ```
2.  **Root Cause:** Use Sequential Thinking to find the *real* problem, not just the symptom.
3.  **Plan Fix:** Create a `fix.plan.md`.

## Phase 3: Fix (Speckit)
1.  **Implement:**
    ```bash
    python3 global/tools/speckit.py implement
    ```
2.  **Test:** Write a regression test that *fails* without the fix and *passes* with it.

## Phase 4: Verify (Sentinel)
1.  **Run Verification:**
    ```bash
    python3 global/tools/speckit.py verify
    ```
2.  **Prevention:** Update `global/helpers/Errors_Log_Template.md` to prevent recurrence.

## Regular Maintenance
*   **Weekly:** Run `speckit.py verify` on the whole codebase.
*   **Monthly:** Update dependencies and run Sentinel Check.

## Remember
**Maintenance is not a chore. It is hygiene.**
