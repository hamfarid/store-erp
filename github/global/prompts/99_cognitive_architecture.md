# 🧠 Cognitive Architecture & Autonomous Reasoning (Level 12)

> **Core Philosophy**: "Do not just answer. Think. Plan. Verify. Remember."

## 1. The Cognitive Loop
All AI agents in the Global System v26 Diamond 32 system MUST follow this loop for complex tasks:

1.  **Hydrate (Memory Load)**:
    *   Query ChromaDB for relevant context (`rag_engine.py --query`).
    *   Load `memory-bank/working/current_state.json`.
2.  **Reason (Plan)**:
    *   Break down the task.
    *   Check `OSF_Score` for proposed solutions.
3.  **Act (Execute)**:
    *   Write code/files.
    *   Use tools (`container_manager.py`, `speckit.py`).
4.  **Verify (Self-Correction)**:
    *   Run tests.
    *   If failure -> **Self-Heal** (Analyze error, propose fix, retry).
5.  **Memorize (Commit)**:
    *   Store new findings in ChromaDB (`rag_engine.py --ingest`).
    *   Update `memory-bank/long_term/knowledge_graph.json`.

## 2. Memory Structure
*   **Short-Term**: Current session context (RAM).
*   **Working**: Active task state (`memory-bank/working/`).
*   **Long-Term**: Vector Database (ChromaDB) + Knowledge Graph.

## 3. Self-Healing Protocol
When a test fails:
1.  **Capture**: Get stdout/stderr.
2.  **Analyze**: Match against `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md`.
3.  **Hypothesize**: Generate 3 potential fixes.
4.  **Test**: Apply Fix #1 -> Run Test. If fail, Fix #2.
5.  **Escalate**: If all fail, ask human.

## 4. The "Why" Check
Before committing any code, ask:
*   *Why* did I choose this architecture?
*   *Why* is this secure?
*   *Why* is this performant?

(If you cannot answer, **DO NOT COMMIT**).
