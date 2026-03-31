# PROMPT 84: PROJECT ANALYSIS & CLEANUP

**Objective:** Analyze the entire project, identify and clean up duplicate/unused files, and create a clear map of the codebase.

---

## 🎯 REQUIREMENTS

1.  **Full Code Analysis:** Read the *entire content* of every file, not just the filenames.
2.  **Dependency Mapping:** Create a complete dependency graph of all imports and definitions.
3.  **Duplicate Detection:** Identify files with similar names (e.g., `fix`, `clean`, `unified`) and similar content.
4.  **Usage Analysis:** Determine which files are actively used and which are not.
5.  **Automated Cleanup:** Move unused files to an `unneeded/` directory and merge duplicate functionality.
6.  **Tool Consolidation:** Move all helper scripts to a central `tools/` directory.

---

## 📝 PHASES OF IMPLEMENTATION

### Phase 1: Analysis
1.  **Run Analysis Tool:** Execute the `project_analyzer.py` script to analyze the entire codebase.
2.  **Generate Reports:** The script will generate:
    - `docs/dependency_map.json`: A complete map of all imports and exports.
    - `docs/file_usage.json`: A report of used vs. unused files.
    - `docs/duplicate_files.json`: A list of duplicate and similar files.

### Phase 2: Cleanup
1.  **Run Cleanup Tool:** Execute the `project_cleanup.py` script.
2.  **Automated Actions:** The script will:
    - Move all unused files to `unneeded/`.
    - Propose a plan for merging duplicate files.
    - Move all scripts to `tools/`.

### Phase 3: Verification
1.  **Re-run Analysis:** Re-run the analysis tool to verify that the cleanup was successful.
2.  **Run Tests:** Run all project tests to ensure that the cleanup has not introduced any regressions.

---

## ✅ SUCCESS CRITERIA

- The `unneeded/` directory contains all unused files.
- The `tools/` directory contains all helper scripts.
- The project has no duplicate or similar files.
- All tests pass.
