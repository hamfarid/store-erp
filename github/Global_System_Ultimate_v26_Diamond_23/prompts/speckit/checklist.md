# /speckit.checklist (Global System Ultimate Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System Ultimate
**Status:** MANDATORY

## Goal
Generate custom quality checklists for features, integrated with Sentinel.

## Input
*   `specs/[feature_name].spec.md`
*   `global/rules/`

## Output
`CHECKLIST.md`

## Instructions
1.  **Adopt the Persona:** You are **The Quality Assurance Lead**.
2.  **Create Checklist:**
    *   [ ] **Sentinel Check:** No secrets, no TODOs.
    *   [ ] **Speckit Verify:** All tests pass.
    *   [ ] **Requirements:** All spec items implemented.
    *   [ ] **Security:** Input validation, Auth, RLS.
    *   [ ] **Performance:** No N+1 queries, proper indexing.
    *   [ ] **Documentation:** Docstrings, updated `system_log.md`.
3.  **Save:** Save as `CHECKLIST.md` in the feature folder.
