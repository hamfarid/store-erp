# Bug Fix Workflow (Global System v26 Diamond 32 Swarm Intelligence)

This workflow governs how defects are resolved. It prioritizes "Root Cause Analysis" over "Quick Fixes".

## 🔄 The Swarm Relay

### Phase 1: The Planner (Triage & Reproduction)
*   **Input:** Bug Report (e.g., "Login fails with 500 error").
*   **Action:**
    1.  **Reproduce:** Create a reproduction script or test case.
    2.  **Analyze:** Read logs. Identify the exact line of failure.
    3.  **Plan:** Define the fix strategy (e.g., "Add null check in auth.py").
*   **Output:** `BUG_REPORT.md` + `PLAN.md`.

### Phase 2: The Executor (Surgical Fix)
*   **Input:** `PLAN.md`.
*   **Action:**
    1.  **Test First:** Run the reproduction script (it should fail).
    2.  **Fix:** Apply the code change.
    3.  **Verify:** Run the reproduction script (it should pass).
*   **Output:** Fixed Code + Passing Test.

### Phase 3: The Reviewer (Regression Testing)
*   **Input:** Fixed Code.
*   **Action:**
    1.  **Impact Analysis:** Did this fix break anything else?
    2.  **Run Suite:** Run ALL tests, not just the new one.
    3.  **Code Quality:** Is the fix clean, or a "hack"?
*   **Output:** `REVIEW_LOG.md`.

### Phase 4: The Critic (Root Cause Certification)
*   **Input:** Verified Fix.
*   **Action:**
    1.  **Question:** "Why did this happen in the first place?"
    2.  **Prevention:** Update `knowledge/antipatterns/` to prevent recurrence.
    3.  **Approval:** Merge to `main` (Hotfix) or `develop`.
