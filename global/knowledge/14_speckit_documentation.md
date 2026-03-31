# Speckit Documentation Methodology

## Overview
We adopt Speckit's philosophy of "Just-in-Time" learning and documentation. Documentation should be accessible, context-aware, and integrated into the workflow.

## Principles
1.  **Contextual:** Documentation should be available where the user (or developer) needs it.
2.  **Bite-sized:** Information should be digestible and focused on a specific task or concept.
3.  **Up-to-date:** Documentation must evolve with the product.

## Implementation
1.  **API Planning:**
    -   Before writing code, document the API contract (endpoints, request/response bodies).
    -   Use tools like Swagger/OpenAPI or simple Markdown tables in `docs/API_DOCUMENTATION.md`.
2.  **Code Comments:**
    -   Use JSDoc/TSDoc for all public functions and components.
    -   Explain *why*, not just *what*.
3.  **User Guides:**
    -   Create short, focused guides for key features in `docs/user_guides/`.
    -   Link to these guides from the UI (e.g., tooltips, help links).

## Workflow
-   **Phase 1 (Planning):** Draft API docs and data models.
-   **Phase 2 (Dev):** Update docs as implementation details change.
-   **Phase 3 (Review):** Verify docs match the code.
