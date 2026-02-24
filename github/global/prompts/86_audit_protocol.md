# 🛡️ Audit Protocol (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Status:** MANDATORY for Release Candidates
**Tool:** `tools/audit_manager.py`

## 1. The Philosophy
Trust is good; verification is engineering. We do not "assume" files are correct; we PROVE it.

## 2. The Process
1.  **Initialize:** Run `python3 tools/audit_manager.py init` to generate the checklist from the current file inventory.
2.  **Inspect:** Read a file. Check for:
    *   Weak language ("should" vs "MUST").
    *   Logical gaps (missing error handling).
    *   Legacy artifacts (v36 references).
3.  **Remediate:** Fix any issues found immediately.
4.  **Verify:** Run `python3 tools/audit_manager.py verify <path> "Fixed X, Y"` to mark it as done.

## 3. The Definition of Done
A project is NOT ready for release until `AUDIT_CHECKLIST.md` has NO unchecked boxes.
