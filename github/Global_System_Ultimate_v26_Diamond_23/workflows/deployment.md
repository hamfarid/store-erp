# 🚀 Deployment Workflow (Global System Ultimate Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System Ultimate + Sentinel
**Status:** MANDATORY

## Workflow

```
Verify (Sentinel) → Build → Deploy → Monitor
```

## Phase 1: Pre-Flight Check (Sentinel)
1.  **Run Verification:**
    ```bash
    python3 global/tools/speckit.py verify
    ```
    *   **STOP** if any test fails.
    *   **STOP** if Sentinel finds secrets or TODOs.
    *   **STOP** if CodeRabbit finds critical issues.

2.  **Environment Check:**
    *   Ensure all secrets are in the deployment environment (NOT in code).
    *   Verify database migrations are ready.

## Phase 2: Build
1.  **Docker:** Build and tag image.
2.  **Assets:** Compile static assets.
3.  **Artifacts:** Package the release.

## Phase 3: Deploy
1.  **Strategy:** Blue/Green or Rolling Update.
2.  **Database:** Run migrations *before* switching traffic.
3.  **Traffic:** Switch traffic to new version.

## Phase 4: Post-Deploy Monitor
1.  **Health Check:** Verify `/health` endpoint.
2.  **Logs:** Monitor for errors (Sentry).
3.  **Rollback:** Be ready to revert if metrics degrade.

## Remember
**Deployment is not the end. It is the beginning of reality.**
