# PROMPT: Path & Import Tracing and Correction

**Objective:** Analyze the entire codebase, identify all incorrect paths and imports, and automatically correct them.

**Context:** The project has many incorrect paths in imports, file references, and configuration files. Your task is to fix them systematically.

---

## Phase 1: Analysis & Mapping (Read-Only)

1.  **Map Project Structure:**
    -   Recursively list all files and directories in the project.
    -   Create a file `docs/PROJECT_STRUCTURE.md` with the complete tree.

2.  **Extract All Paths & Imports:**
    -   Use `grep` or a similar tool to find all instances of `import`, `require`, `from`, `src=`, `href=`, and `url()` in all project files (`.js`, `.jsx`, `.ts`, `.tsx`, `.css`, `.scss`, `.html`, `.json`).
    -   For each match, extract the path and the file where it was found.
    -   Store this information in a structured format (e.g., JSON) in `docs/Path_Analysis.json`.

    ```json
    [
      {
        "file": "src/components/Header.jsx",
        "line": 3,
        "path": "../utils/auth",
        "type": "import"
      },
      {
        "file": "public/index.html",
        "line": 10,
        "path": "/static/logo.png",
        "type": "src"
      }
    ]
    ```

3.  **Validate Each Path:**
    -   For each entry in `docs/Path_Analysis.json`:
        -   Resolve the absolute path based on the file's location.
        -   Check if the resolved path actually exists.
        -   If it does not exist, mark it as `"status": "broken"`.

    ```json
    {
      "file": "src/components/Header.jsx",
      "line": 3,
      "path": "../utils/auth",
      "type": "import",
      "resolved_path": "/home/ubuntu/my-project/src/utils/auth.js",
      "status": "broken" // Because auth.js doesn't exist
    }
    ```

## Phase 2: Correction (Write)

1.  **Find Correct Path:**
    -   For each broken path, search the project for the correct file.
    -   For example, if `../utils/auth` is broken, search for `auth.js` in the entire project.
    -   Once found, calculate the correct relative path from the original file.

2.  **Generate Corrections:**
    -   Create a `docs/Path_Corrections.json` file with the proposed changes.

    ```json
    [
      {
        "file": "src/components/Header.jsx",
        "line": 3,
        "old_path": "../utils/auth",
        "new_path": "../../core/auth/auth.js",
        "status": "correction_proposed"
      }
    ]
    ```

3.  **Apply Corrections:**
    -   Read the `docs/Path_Corrections.json` file.
    -   For each entry, open the file and replace the `old_path` with the `new_path`.
    -   **Use a script for this to avoid manual errors.**

## Phase 3: Verification

1.  **Re-run Analysis:** Repeat Phase 1.
2.  **Verify:** Check `docs/Path_Analysis.json` again. There should be **zero** broken paths.
3.  **Run Tests:** Run all unit and integration tests to ensure the changes have not broken any functionality.

---

## Automation Script (`.global/tools/fix_paths.py`)

You should create a Python script to automate this entire process. The script should:

1.  Take the project root as an argument.
2.  Perform the analysis and generate `Path_Analysis.json`.
3.  Perform the correction and generate `Path_Corrections.json`.
4.  Prompt the user for confirmation before applying the changes.
5.  Apply the changes.
6.  Re-run the analysis for verification.

---

## Example Commands

**To start the process, you would say:**

> "I will now begin a full analysis of all paths and imports in the project located at `/home/ubuntu/my-project`. I will use the `13_path_and_import_tracing.md` prompt and the associated automation script to identify and correct all broken paths."

**Then, you would execute the script:**

```bash
python3 .global/tools/fix_paths.py --project-root /home/ubuntu/my-project
```

---

**Success Criteria:**
- ✅ `docs/PROJECT_STRUCTURE.md` is created.
- ✅ `docs/Path_Analysis.json` is created and shows broken paths.
- ✅ `docs/Path_Corrections.json` is created with proposed fixes.
- ✅ All broken paths are corrected in the codebase.
- ✅ The final `Path_Analysis.json` shows zero broken paths.
- ✅ All tests pass after-correction tests pass.

