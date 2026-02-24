# 🧠 Memory Management Rules (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Speckit (Analyze Phase)

## 1. The Philosophy
Amnesia is a bug. You MUST remember.

## 2. The Protocol (The Librarian)
1.  **Initialization:** At the start of EVERY task, you MUST read `memory-bank/activeContext.md` and `memory-bank/systemContext.md`.
2.  **Persistence:** You MUST save key decisions to `memory-bank/decisionLog.md` immediately.
3.  **Registry:** Every new file created MUST be added to `memory-bank/file_registry.json` (if implemented).

## 3. Mandatory Memory Structures
*   **`memory-bank/activeContext.md`:** The current state of the universe.
*   **`memory-bank/decisionLog.md`:** The history of decisions.
*   **`memory-bank/projectBrief.md`:** The goal of the universe.

## 4. The "No Duplication" Rule
*   **Check First:** Before creating a file, check `all_files_inventory.txt`.
*   **Reuse:** If a utility exists, import it. Do NOT recreate it.
