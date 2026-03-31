# 105_speckit_protocol.md - v33.2 (Adoption Edition)

## 1. The Two Paths
The System now recognizes two states of existence:
1.  **Genesis (Greenfield):** Creating a project from nothing.
2.  **Adoption (Brownfield):** Taking control of an existing chaotic project.

## 2. The Adoption Workflow
When `lifecycle.py` detects existing files:
1.  **Reverse Engineering:** It reads the existing code to draft a "Legacy Constitution".
2.  **Librarian Registration:** It scans every existing file and registers it in `file_registry.json` to prevent overwriting or duplication.
3.  **Spec-Backfilling:** It uses Speckit to generate specs for existing critical modules (gradually).

## 3. The Rules of Adoption
*   **Respect the Legacy:** Do not delete existing files unless they violate the "Constitution".
*   **Gradual Refactoring:** Refactor one module at a time.
*   **No Ghost Files:** If a file exists on disk but not in the Registry, REGISTER IT IMMEDIATELY.

## 4. Speckit Integration
*   **New Features:** Must have a `.spec.md` before coding.
*   **Existing Features:** Must have a `.spec.md` created before *modifying* code.

## 5. The Tooling
*   **Core Tool:** `specify` (The real CLI from GitHub).
*   **Bridge:** `python3 global/tools/speckit_bridge.py` (Our system wrapper).

## 6. The Workflow (Standard)
**Phase A: Inception (The Spec)**
1.  **Init:** Run `python3 global/tools/speckit_bridge.py init <project_name>` to scaffold the spec structure.
2.  **Define:** Create/Edit `.spec.md` files to describe features in natural language.
3.  **Verify:** Ensure the spec aligns with `project_memory.md`.

**Phase B: Implementation (The Code)**
1.  **Read Spec:** You MUST read the relevant `.spec.md` file before writing code.
2.  **Implement:** Write code that satisfies the spec.
3.  **Update:** If code changes, update the spec. **Keep them in sync.**

## 7. Integration with Anti-Amnesia
*   **Librarian Check:** The bridge ensures we don't overwrite existing specs without checking.
*   **Verification Oath:** You must swear: "I have read the Spec for Feature X before coding it."

**Rule:** NEVER write code without a corresponding Spec.
