# 🐝 Swarm Protocol: Multi-Agent Orchestration

> **Framework**: Chain-of-Vibes / Swarm Intelligence
> **Goal**: Coordinate specialized agents to solve complex tasks.

## 1. The Huddle (Planning Phase)
*   **Participants**: Architect, User.
*   **Output**: `PLAN.md` with clear task breakdown.
*   **Process**:
    1.  User provides intent.
    2.  Architect decomposes intent into atomic tasks.
    3.  Architect assigns tasks to Developer/QA.

## 2. The Sprint (Execution Phase)
*   **Participants**: Developer, QA.
*   **Output**: Code, Tests, Documentation.
*   **Process**:
    1.  **Developer** picks a task.
    2.  **Developer** writes tests (EDD).
    3.  **Developer** implements code.
    4.  **QA** verifies implementation.

## 3. The Review (Verification Phase)
*   **Participants**: Reviewer, Architect.
*   **Output**: Merged PR or Feedback.
*   **Process**:
    1.  **Reviewer** runs `tools/security_scan.py`.
    2.  **Reviewer** checks against `AGENTS.md`.
    3.  **Architect** validates alignment with system design.

## 4. Conflict Resolution
*   If agents disagree, **Architect** has the final vote.
*   If Architect is unsure, **User** is consulted (Human-in-the-Loop).
