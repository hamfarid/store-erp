# Security Audit Workflow (Global System v26 Diamond 32 Synchronized Intelligence Edition)

Security is not a step; it is a mindset. In the Swarm, **The Reviewer** and **The Critic** are the primary guardians, but **The Executor** must build securely from the start.

## 🛡️ The Swarm Defense Protocol

### Phase 1: The Planner (Threat Modeling)
*   **Action:** Identify the "Crown Jewels" (Database, API Keys, User Data).
*   **Question:** "How would I hack this?"
*   **Output:** `THREAT_MODEL.md` (List of potential attack vectors).

### Phase 2: The Executor (Secure Implementation)
*   **Action:**
    *   Use `python-dotenv` for secrets (NEVER hardcode).
    *   Use `bcrypt` or `Argon2` for passwords.
    *   Use Parameterized Queries for SQL.
*   **Self-Check:** Run `bandit` or `npm audit` locally before committing.

### Phase 3: The Reviewer (Vulnerability Scanning)
*   **Action:**
    1.  **Static Analysis (SAST):** Run `bandit -r .` and `eslint-plugin-security`.
    2.  **Dependency Check:** Run `pip-audit` or `npm audit`.
    3.  **Secret Scanning:** Run `trufflehog` or `git-secrets` (simulated via Sentinel).
*   **Output:** `SECURITY_LOG.md`.

### Phase 4: The Critic (Penetration Simulation)
*   **Action:**
    1.  **The "Red Team" Mindset:** Attempt to bypass the logic.
    2.  **Sentinel Check:** `python3 global_system/tools/sentinel.py` (Final Gate).
    3.  **VETO Power:** If *any* High/Critical vulnerability exists, the release is blocked.

## 🚨 Emergency Response (If Breach Detected)
1.  **Isolate:** Take the container/service offline.
2.  **Analyze:** Planner identifies the breach point.
3.  **Patch:** Executor fixes the hole.
4.  **Verify:** Reviewer confirms the patch works.
5.  **Restore:** Critic approves re-deployment.
