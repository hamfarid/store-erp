# 🚫 No Duplicate Files (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Speckit (Librarian Check)

## 1. The Philosophy
Duplication is the root of all evil (and bugs). One Source of Truth (SSOT).

## 2. The Protocol
Before creating ANY file, you MUST:
1.  **Search:** Check `memory-bank/file_registry.json` (if exists) and `all_files_inventory.txt`.
2.  **Verify:** Does a file with a similar purpose exist?
3.  **Justify:** If yes, why do you need a new one? Can you refactor the existing one?

## 3. Forbidden Patterns
*   **Suffixes:** `_v2`, `_final`, `_new`, `_fix` are STRICTLY FORBIDDEN.
*   **Shadowing:** Creating `utils.py` when `common/utils.py` exists.

## 4. Resolution
If you find a duplicate:
1.  **Merge:** Combine the logic into the superior file.
2.  **Delete:** Remove the inferior file.
3.  **Update:** Update all references to point to the merged file.
