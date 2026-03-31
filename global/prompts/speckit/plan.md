# /speckit.plan (Hybrid Engine v35.0)

**Goal:** Convert the Spec into a **Bulletproof Technical Blueprint**.
**Constraint:** "Code is Memory" - Every decision must be indexed.

**Input:**
*   `specs/[feature_name].spec.md`
*   `.memory/code_structure.json` (Existing Architecture)

**Output:** `plans/[feature_name].plan.md`

**The Hybrid Protocol:**

1.  **Predictive Engineering (Mandatory):**
    *   Before planning, ask: "Where will this break?"
    *   Add a section: "## Risk Analysis & Mitigation".

2.  **Data Structure First:**
    *   Define the JSON schemas, Database Models, or Class Attributes *before* logic.
    *   Use `class` definitions in Python/Pseudo-code to show structure.

3.  **Integration Strategy:**
    *   Explicitly list which *existing* files will be modified.
    *   Explicitly list which *new* files will be created.

**Template (Strict Enforcement):**

```markdown
# Plan: [Feature Name]
**Architect:** [AI Name]
**Risk Level:** [Low/Medium/High]

## 1. Predictive Engineering (Risk Analysis)
*   **Risk:** [Potential Failure Point] -> **Mitigation:** [Solution]

## 2. Data Structures (The Backbone)
```python
class FeatureName:
    def __init__(self):
        # Define attributes here
        pass
```

## 3. File Operations
*   **Create:** `path/to/new_file.py`
*   **Modify:** `path/to/existing_file.py` (Method: `update_function_X`)

## 4. Step-by-Step Implementation Strategy
1.  [Step 1 Description]
2.  [Step 2 Description]
```
