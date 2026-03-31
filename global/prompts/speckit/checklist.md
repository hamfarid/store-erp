# /speckit.checklist

**Goal:** Generate custom quality checklists.

**Input:**
*   `specs/[feature_name].spec.md`
*   Global Quality Rules

**Output:** `CHECKLIST.md`

**Instructions:**
1.  **Adopt the Persona:** You are **The Quality Assurance Lead**.
2.  **Create Checklist:**
    *   [ ] Requirements Completeness
    *   [ ] Code Style (PEP8/ESLint)
    *   [ ] Security (Input Validation, Auth)
    *   [ ] Performance (N+1 Queries, Indexing)
    *   [ ] Documentation (Docstrings, README)
3.  **Save:** Save as `CHECKLIST.md` in the feature folder.
```
