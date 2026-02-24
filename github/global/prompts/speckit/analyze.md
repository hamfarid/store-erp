# /speckit.analyze (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Goal:** Deep analysis of the codebase, requirements, and project state using the **Agentic Engine** and **5-Layer Defense**.

**Input:**
*   `specs/[feature_name].spec.md` (if applicable)
*   `todo.md`
*   `global/system_log.md`
*   **MANDATORY:** `global/AI_CONTEXT_ROUTER.md`
*   **MANDATORY:** `AGENTS.md`

**Output:** `project_memory.md` (or equivalent analysis report).

**Instructions:**
1.  **Governance Check (Layer 1):**
    *   **Action:** Read `AGENTS.md`.
    *   **Constraint:** Ensure analysis aligns with the Universal Governance Constitution.

2.  **Context Routing (Layer 3):**
    *   **Action:** Read `global/AI_CONTEXT_ROUTER.md`.
    *   **Action:** Determine the scope of analysis (Frontend/Backend/etc.).
    *   **Action:** Load the relevant context files BEFORE starting analysis.

3.  **Sequential Thinking (Layer 1):** Apply `global/tools/sequential_thinking.py` logic.

4.  **Check Consistency:**
    *   Does every Requirement in the Spec have a Task in `todo.md`?
    *   Does every Task map to a File in the Plan?

5.  **Check Coverage:**
    *   Are there tests for every new feature?
    *   Is the documentation plan included?

6.  **Sentinel Check (Layer 5):**
    *   Scan for recurring errors from `Errors_Log_Template.md`.
    *   Ensure no "Won't Fix" issues are blocking progress.
    *   **Verify:** Are Kilo/Kiro/Augment/Windsurf configurations valid?

7.  **Report:** Flag any gaps. Stop the workflow if critical gaps exist.
