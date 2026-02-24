# Feature Development Workflow (Global System v26 Diamond 32 Swarm Intelligence)

This workflow governs how new capabilities are added to the system. It ensures that no feature is built without a plan, and no plan is executed without verification against the **Universal Governance Constitution**.

## 🔄 The Swarm Relay (5-Layer Defense)

### Phase 1: The Planner (Design & Feasibility)
*   **Input:** User Request (e.g., "Add Stripe payments").
*   **Governance Check (Layer 1):** Read `AGENTS.md`. Ensure feature aligns with project structure.
*   **Action:**
    1.  **Research:** Read Stripe API docs (v2025).
    2.  **Gap Analysis:** What files need to change? (`requirements.txt`, `.env`, `controllers/`).
    3.  **Draft Plan:** Create `PLAN.md` with atomic steps.
*   **Output:** `PLAN.md` (Approved).

### Phase 2: The Executor (Implementation)
*   **Input:** `PLAN.md`.
*   **Tool Check (Layer 5):** Ensure Kilo/Kiro/Augment/Windsurf configs are present.
*   **Action:**
    1.  **Step 1:** Install dependencies (`stripe`).
    2.  **Step 2:** Create `StripeService` class.
    3.  **Step 3:** Create API endpoints.
    4.  **Self-Correction:** If API fails, fix it before moving to Step 4.
*   **Output:** Implemented Codebase.

### Phase 3: The Reviewer (Audit)
*   **Input:** Codebase.
*   **Action:**
    1.  **Security Check:** Are API keys hardcoded? (Must use `.env`).
    2.  **Logic Check:** Does it handle failed payments?
    3.  **Test Check:** Are there unit tests for `StripeService`?
    4.  **Agent Compatibility:** Is the code parseable by Augment/Windsurf?
*   **Output:** `REVIEW_LOG.md` (Pass).

### Phase 4: The Critic (Integration Check)
*   **Input:** Verified Code.
*   **Action:**
    1.  **Semantic Check:** Does this actually allow the user to pay?
    2.  **Sentinel Check:** Zero TODOs. `sentinel.py` PASS.
    3.  **Approval:** Merge to `develop`.
