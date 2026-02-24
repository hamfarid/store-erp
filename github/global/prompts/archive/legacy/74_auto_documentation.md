# Auto Documentation (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System v26 Diamond 32
**Status:** MANDATORY

## Purpose
Automate the generation and maintenance of documentation using Speckit and CI/CD tools.

## Instructions
1.  **API Docs:** Use Swagger/OpenAPI (FastAPI) or Redoc (Node.js) to auto-generate API references.
2.  **Code Docs:** Use `pdoc` (Python) or `TypeDoc` (TS) to generate code references.
3.  **Readme:** Use `global/tools/readme_generator.py` to update the README with the latest stats.
4.  **Verification:** `speckit verify` checks if docs are up-to-date with code.

## Tools
*   **Python:** `pdoc`, `mkdocs`
*   **TypeScript:** `typedoc`
*   **API:** `swagger-ui`, `redoc`
