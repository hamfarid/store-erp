# Nx Monorepo Guidelines

## Overview
Nx is a smart, fast, and extensible build system with first-class monorepo support and powerful integrations. We use Nx to manage our project structure, ensuring scalability and code sharing.

## Core Structure
- **apps/**: Contains the deployable applications (e.g., `frontend`, `backend`).
- **libs/**: Contains shared libraries (e.g., `ui-components`, `data-access`, `utils`).
- **tools/**: Custom scripts and tooling for the workspace.

## Best Practices
1.  **Library Types:**
    -   `feature-*`: Smart components and business logic for a specific feature.
    -   `ui-*`: Dumb/Presentational components.
    -   `data-access-*`: State management and API services.
    -   `util-*`: Pure utility functions and helpers.
2.  **Boundaries:** Enforce module boundaries using `eslint-plugin-nx` to prevent circular dependencies and ensure architectural integrity.
3.  **Caching:** Leverage Nx computation caching to speed up builds and tests.
4.  **Generators:** Use Nx generators (`nx g ...`) to create new apps and libs to ensure consistency.

## Workflow
-   **Creating a Lib:** `npx nx g @nx/react:lib libs/ui-header`
-   **Running Tasks:** `npx nx run-many --target=test --all`
-   **Graph:** Use `npx nx graph` to visualize dependencies.
