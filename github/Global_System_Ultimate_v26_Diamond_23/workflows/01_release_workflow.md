# Release Workflow (Global System Ultimate Synchronized Intelligence Edition)

This workflow defines how the **Swarm of Agents** collaborates to release software. It is not just a list of commands; it is a cognitive relay race.

## 🔄 The Swarm Relay

### Phase 1: The Planner (Strategic Prep)
*   **Goal:** Confirm readiness for release.
*   **Action:**
    1.  Analyze `CHANGELOG.md` vs. `git log`. Are we missing anything?
    2.  Check `PLAN.md` status. Are all tasks marked `[x]`?
    3.  **Decision:** If gaps exist, abort release. If ready, trigger Phase 2.

### Phase 2: The Executor (Build & Package)
*   **Goal:** Create the artifact.
*   **Action:**
    1.  **Bump Version:** `npm version patch` / `bump2version`.
    2.  **Build:** `npm run build` or `docker build`.
    3.  **Self-Correction:** If build fails, fix it immediately (do not pass to Reviewer).

### Phase 3: The Reviewer (Audit & Test)
*   **Goal:** Verify the artifact.
*   **Action:**
    1.  **Automated Checks:** `python3 global_system/tools/speckit.py verify`.
    2.  **Coverage Check:** Ensure test coverage >= 80%.
    3.  **Security Scan:** Run `npm audit` or `safety check`.
    4.  **Output:** `REVIEW_LOG.md` (Pass/Fail).

### Phase 4: The Critic (Final Gate)
*   **Goal:** Zero-Error Approval.
*   **Action:**
    1.  **Sentinel Check:** `python3 global_system/tools/sentinel.py`.
    2.  **Semantic Check:** Does the release match the Planner's intent?
    3.  **The Button:**
        *   **VETO:** Rollback.
        *   **APPROVE:** `git push --tags` & Deploy.

## 🚀 Deployment Commands (Only after Critic Approval)
```bash
# 1. Tag
git tag -a Global System Ultimate -m "Swarm Release Global System Ultimate"

# 2. Push
git push origin Global System Ultimate

# 3. Deploy (Example)
kubectl apply -f k8s/production/
```
