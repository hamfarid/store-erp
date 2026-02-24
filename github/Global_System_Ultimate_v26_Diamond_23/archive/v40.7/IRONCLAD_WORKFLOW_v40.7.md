# The Ironclad Workflow (Global System Ultimate Synchronized Intelligence Edition)
**Status:** ENFORCED BY CODE
**Philosophy:** "Trust is good, Automation is better."

## 1. The Single Entry Point
The AI (and the Developer) is **forbidden** from running raw commands like `git commit` or `python main.py` directly for lifecycle events.
**ALL** actions must go through `speckit`.

*   ❌ `git commit -m "fix"`
*   ✅ `speckit commit -m "fix"` (Runs Sentinel -> Tests -> Commit)

## 2. The Enforcement Chain

### Step 1: Analysis (Auto-Context)
*   **Trigger:** `speckit analyze`
*   **Enforcement:**
    *   Speckit checks if `memory-bank/context.json` exists.
    *   If not, it runs `project_analyzer.py` **automatically**.
    *   It loads the context into the environment variables.

### Step 2: Planning (The Blueprint)
*   **Trigger:** `speckit plan <feature>`
*   **Enforcement:**
    *   Speckit checks `AI_CONTEXT_ROUTER.md`.
    *   It **refuses** to proceed if the Plan Template is not followed.
    *   It saves the plan to `plans/<feature>.plan.md`.
    *   **Swarm Check:** It assigns the plan to the **Architect** role.

### Step 3: Implementation (The Build)
*   **Trigger:** `speckit implement <feature>`
*   **Enforcement:**
    *   Speckit reads `plans/<feature>.plan.md`.
    *   It verifies that the plan exists.
    *   **Swarm Check:** It assigns the task to the **Developer** role.

### Step 4: Verification (The Gatekeeper)
*   **Trigger:** `speckit verify`
*   **Enforcement:**
    *   **Sentinel:** Runs first. If it finds TODOs or Secrets -> **ABORT**.
    *   **CodeRabbit:** Runs second. If it finds Critical Issues -> **ABORT**.
    *   **Tests:** Runs third. If tests fail -> **ABORT**.
    *   **Swarm Check:** It assigns the review to the **Reviewer** and **QA** roles.

### Step 5: Committing (The Seal)
*   **Trigger:** `speckit commit`
*   **Enforcement:**
    *   Only runs if `speckit verify` passed in the last 5 minutes.
    *   Automatically formats the commit message.

## 3. The "No Bypass" Rule
The `setup_project.py` script will install a `pre-commit` hook that runs `sentinel.py`.
Even if the user tries to bypass Speckit and use `git commit`, the hook will catch them.
