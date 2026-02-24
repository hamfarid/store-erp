# AI Handbook

> **CRITICAL INSTRUCTION**: This handbook MUST be read and activated at the start of every session. It overrides all previous procedural defaults.

## 🛑 1. The "Two-Strike" Rule (Error Handling)
*   **Directive**: If an error occurs **twice** during the execution of a task (same error or related cascade):
    1.  **STOP** immediately. Do not retry blindly.
    2.  **ANALYZE** the root cause using `tools/log_analyzer.py`.
    3.  **DOCUMENT** the error in `memory-bank/lessons.md`.
    4.  **ASK** the user for guidance if the path forward is ambiguous.
*   **Prohibition**: Never loop endlessly on the same error.

## 🧹 2. Hygiene & Cleanup Protocol
*   **Mandate**: Before ANY build, test, or commit, you MUST run the cleanup routine.
*   **Targets**:
    *   `__pycache__` directories (Recursive delete)
    *   `.pytest_cache` directories
    *   `.DS_Store` files
    *   Temporary `.tmp` or `.bak` files
*   **Command**: `python3 tools/file_cleanup.py --aggressive`

## 🔍 3. Pre-Flight Verification (Pre-Build)
*   **Mandate**: Never run code or build a project without a pre-flight check.
*   **Checklist**:
    1.  **Imports**: Verify all imports are valid and installed (`tools/verify_all_imports.py`).
    2.  **Syntax**: Check for syntax errors (`flake8` or `python -m py_compile`).
    3.  **Structure**: Ensure file paths in code match the actual `INVENTORY.md`.
    4.  **Ports**: Verify calculated ports are free (`tools/preflight_check.py`).
*   **Command**: `python3 tools/preflight_check.py`

## 🗺️ 4. Context Awareness (Inventory & Workflows)
*   **Mandate**: You must maintain an up-to-date mental map of the project.
*   **Action**:
    *   Read `INVENTORY.md` to know where files are.
    *   Read `memory-bank/systemContext.md` to understand how modules interact.
    *   **NEVER** guess file paths. Always look them up.

## 🧠 5. Memory Persistence
*   **Directive**: All architectural decisions, workflow maps, and error patterns must be saved to the `memory-bank/` directory.
*   **Goal**: "Amnesia" is not an excuse. Use the file system as your long-term memory.

## 6. Smart Port Orchestration
*   **Mandate**: Do NOT hardcode ports. Always use the calculated values from `genesis.py`.
*   **Formula**:
    *   Redis = Backend + Frontend
    *   DB = Backend + 100
    *   AI = Backend + 200
    *   ML = Frontend + 100
*   **Networking**: Use `global_neural_net` (Docker) or `localhost` (Host).

---
*Signed: Global System v26 Diamond 32 Synchronized Intelligence Governance*
