# Memory Update Workflow

## Purpose
This workflow ensures that the project's context is kept up-to-date and accurate, preventing information loss and ensuring that lessons learned are applied.

## Steps
1.  **Trigger**: A significant action or decision is made (e.g., code change, architectural decision, new requirement).
2.  **Identify Context**: Determine which files in `memory-bank/` need to be updated.
    *   `activeContext.md`: Current state and next steps.
    *   `projectBrief.md`: Project goals and constraints.
    *   `systemPatterns.md`: Architectural decisions.
    *   `techContext.md`: Technical stack and dependencies.
    *   `progress.md`: Completed work and milestones.
    *   `lessons_learned.md`: New insights and lessons learned.
3.  **Update Files**: Modify the relevant files with the new information.
    *   Use clear and concise language.
    *   Avoid duplication.
    *   Reference related files if necessary.
4.  **Verify**: Check that the updates are accurate and consistent with the rest of the context.
5.  **Commit**: Save the changes to the repository.

## Roles Involved
*   **Memory Guardian**: Responsible for executing the update.
*   **Developer**: Provides the technical details for the update.
*   **Architect**: Provides the architectural context for the update.
