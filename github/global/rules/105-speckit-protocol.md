# Rule 105: The Speckit Protocol (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by `tools/speckit.py`

## 1. The Prime Directive
**"No Code Without a Plan. No Plan Without Analysis."**

Every task MUST follow the **Speckit Cycle**:
1.  **Analyze:** `python3 tools/speckit.py analyze` (Understand the context).
2.  **Plan:** `python3 tools/speckit.py plan` (Create the blueprint).
3.  **Task:** `python3 tools/speckit.py tasks` (Break it down).
4.  **Implement:** `python3 tools/speckit.py implement` (Build it).
5.  **Verify:** `python3 tools/speckit.py verify` (Test and secure it).

## 2. The Zero-Error Policy
*   **No TODOs:** Code must be complete or not committed.
*   **No Secrets:** API keys must be in `.env`.
*   **No Broken Tests:** Green light is required for every step.

## 3. The Memory Imperative
*   Every change must be indexed immediately using `tools/code_indexer.py` (if available).
*   The `memory-bank/activeContext.md` must be updated after every major phase.

## 4. The Sentinel's Watch
*   The Sentinel (`tools/preflight_check.py`) has the final say.
*   If Sentinel says "BLOCK", you STOP and FIX. No exceptions.

## 5. Adoption Mode (Legacy Support)
*   **Respect the Legacy:** Do not delete existing files unless they violate the Constitution.
*   **Gradual Refactoring:** Refactor one module at a time using Speckit.
*   **Backfill Specs:** Create specs for existing features before modifying them.
