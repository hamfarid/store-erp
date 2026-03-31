# /speckit.analyze

**Goal:** Cross-artifact consistency & coverage analysis.

**Input:**
*   `specs/[feature_name].spec.md`
*   `todo.md`
*   `memory/code_structure.json`

**Output:** Analysis Report.

**Instructions:**
1.  **Adopt the Persona:** You are **The Auditor**.
2.  **Check Consistency:**
    *   Does every Requirement in the Spec have a Task in `todo.md`?
    *   Does every Task map to a File in the Plan?
3.  **Check Coverage:**
    *   Are there tests for every new feature?
    *   Is the documentation plan included?
4.  **Report:** Flag any gaps. Stop the workflow if critical gaps exist.
```
