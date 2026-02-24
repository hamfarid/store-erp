# Memory Management Rules

## Core Principles
1.  **Single Source of Truth**: The `memory-bank/` directory is the authoritative source for all project context.
2.  **Continuous Update**: Every significant action or decision must be reflected in the memory bank immediately.
3.  **Context Integrity**: Do not delete or modify historical context without a clear reason and documentation.
4.  **Pruning**: Regularly archive obsolete information to keep the active context relevant and efficient.

## Specific Rules
1.  **Initialization**:
    *   Always check for the existence of `memory-bank/` at the start of a session.
    *   If missing, initialize it using `init_project.sh`.
2.  **Active Context**:
    *   Read `activeContext.md` before starting any task.
    *   Update `activeContext.md` after completing any task.
3.  **Project Brief**:
    *   Read `projectBrief.md` to understand the project's goals and constraints.
    *   Update `projectBrief.md` if the project scope changes.
4.  **System Patterns**:
    *   Read `systemPatterns.md` to understand the architectural decisions.
    *   Update `systemPatterns.md` if the architecture evolves.
5.  **Tech Context**:
    *   Read `techContext.md` to understand the technical stack and dependencies.
    *   Update `techContext.md` if new technologies are introduced.
6.  **Progress Tracking**:
    *   Read `progress.md` to understand the current status and pending tasks.
    *   Update `progress.md` to reflect completed work and new milestones.
7.  **Lessons Learned**:
    *   Read `lessons_learned.md` to avoid repeating past mistakes.
    *   Log new insights and lessons learned to `lessons_learned.md`.

## Workflow Integration
*   **Pre-Task**: Load context from `memory-bank/`.
*   **During Task**: Reference context as needed.
*   **Post-Task**: Update `memory-bank/` with new information.
