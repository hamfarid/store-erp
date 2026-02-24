# Task AI & Planning (Global System Ultimate 2026)

**Version:** Global System Ultimate v8 - Agentic Swarm Edition
**Engine:** Speckit Global System Ultimate
**Status:** MANDATORY

## 1. The "Context First" Plan Structure (Speckit Plan)
**Rule:** Every task plan MUST start with a "Context Loading" phase.
*   **Phase 0:** Read Context Files (`memory-bank/`, `specs/`).
*   **Phase 1:** Visual Architecture (Mermaid).

## 2. Hierarchical Management (Swarm-Based)
*   **Level 1: Epics** (Big Picture) -> `plan.md` (Managed by Architect Agent)
*   **Level 2: Stories** (User Value) -> `plan.md` (Managed by Product Agent)
*   **Level 3: Tasks** (Dev Work) -> `todo.md` (Managed by Developer Agent)

## 3. The "Atomic Execution" (Speckit Implement)
**Rule:** Break tasks into atomic units that include documentation.
*   *Bad:* "Implement Auth"
*   *Good:* "Implement Login API + Update Routes.md + Add Tests"

## 4. The "Definition of Done" (Speckit Verify)
A task is ONLY done when:
1.  Code is written.
2.  Tests pass (Unit/E2E).
3.  Documentation is updated.
4.  Sentinel checks pass.
5.  `todo.md` is updated.
6.  **Self-Correction:** If errors occur, the agent must attempt to fix them autonomously (up to 3 times) before escalating.

## 5. Error Recovery Protocol (2026)
If a task fails:
1.  **Diagnose:** Analyze the error log.
2.  **Hypothesize:** Generate 3 potential fixes.
3.  **Test:** Apply the most likely fix and run tests.
4.  **Verify:** Confirm the fix works.
5.  **Document:** Record the error and fix in `memory-bank/lessons.md`.
