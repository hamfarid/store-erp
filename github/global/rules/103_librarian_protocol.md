# RULE 103: THE LIBRARIAN PROTOCOL (v32.0)

## 📚 The Concept
**Rule:** You are NOT allowed to create a file without checking if it exists.
**Mandate:** You must maintain a `file_registry.json` and consult it before every `write` action.

## 1. The Registry
*   **File:** `.memory/file_registry.json`
*   **Content:** A map of all critical files and their paths.
*   **Update:** Every time you create a file, you MUST add it to the registry.

## 2. The "Lookup First" Mandate
**Trigger:** Before creating ANY file (e.g., `utils.py`).
**Action:**
1.  Read `.memory/file_registry.json`.
2.  Search for `utils.py`.
3.  **If Found:** USE THE EXISTING FILE. Do not create a duplicate (e.g., `utils_new.py`).
4.  **If Not Found:** Create the file and ADD it to the registry.

## 3. The "Absolute Path" Law
**Rule:** Relative paths (e.g., `../config`) are FORBIDDEN in critical commands.
**Reason:** They cause "File Not Found" errors when the CWD changes.
**Mandate:** Always use full paths: `/home/ubuntu/project/...`
