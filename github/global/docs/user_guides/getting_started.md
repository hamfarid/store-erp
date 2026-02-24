# Getting Started Guide (Global System v26 Diamond 32 Synchronized Intelligence Edition)

## Prerequisites
*   Docker
*   Python 3.11+
*   Node.js 20+
*   **AI Agent:** Cursor, Cline, Claude Code, Kilo, Kiro, Augment, or Windsurf.

## Installation
1.  Clone the repository.
2.  Run `./setup.sh`.
3.  **Governance Check:**
    *   Read `AGENTS.md`.
    *   Ensure your agent is configured correctly (e.g., `.cursor/rules`, `.augment/rules`).

## Agent Setup
*   **Cursor:** Enable "Always On" mode for rules.
*   **Cline:** Point to `.clinerules/01-governance.md`.
*   **Augment:** Verify `.augment/rules/coding-standards.md` is active.
*   **Windsurf:** Ensure `.windsurf/rules` are loaded.
*   **Kilo/Kiro:** Check `kilo.json` / `kiro.yaml`.

## Workflow
1.  **Plan:** Use `speckit analyze` to start.
2.  **Execute:** Follow the `PLAN.md`.
3.  **Verify:** Run `speckit verify` before committing.
