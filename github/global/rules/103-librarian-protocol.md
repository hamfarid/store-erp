# 📚 Rule 103: The Librarian Protocol (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Speckit (Librarian Check)

## 1. The Philosophy
A file lost is a bug found. We map the universe to control it.

## 2. The Registry
*   **Path:** `memory-bank/file_registry.json` (if implemented) or `all_files_inventory.txt`.
*   **Truth:** If it's not in the registry, it doesn't exist (to the system).

## 3. The Protocol (Lookup First)
Before creating ANY file:
1.  **Search:** Check the registry.
2.  **Verify:** Does a similar file exist?
3.  **Oath:** "I swear I am not creating a duplicate."

## 4. The "Absolute Path" Law
*   **Forbidden:** Relative paths (`../utils`) in scripts.
*   **Mandatory:** Absolute paths (`/path/to/project/utils`) or `os.path.abspath(__file__)` based resolution.
