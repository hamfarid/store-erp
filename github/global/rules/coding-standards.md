# Coding Standards (Global System v26 Diamond 32)

## 1. Universal Governance (Layer 1)
*   **Mandate:** All code must comply with `AGENTS.md`.
*   **Agent Compatibility:** Code must be parseable by Kilo, Kiro, Augment, and Windsurf.

## 2. Python (PEP 8 + Black)
*   **Line Length:** 88 characters.
*   **Type Hints:** Mandatory for all function arguments and return values.
*   **Docstrings:** Google Style for all public modules, classes, and functions.
*   **Error Handling:** Explicit try/except blocks with logging (no bare excepts).

## 3. TypeScript (Prettier + ESLint)
*   **Strict Mode:** Enabled (`strict: true`).
*   **Imports:** Absolute paths (`@/components/...`).
*   **Components:** Functional components with hooks.
*   **No `any`:** Use `unknown` or specific types.

## 4. Git Commit Messages (Conventional Commits)
*   `feat: add user login`
*   `fix: resolve jwt expiration bug`
*   `docs: update api documentation`
*   `chore: upgrade dependencies`

## 5. File Naming
*   **Python:** `snake_case.py`
*   **TypeScript:** `PascalCase.tsx` (Components), `camelCase.ts` (Utils)
*   **CSS:** `kebab-case.css`

## 6. Agent-Specific Rules
*   **Augment:** Follow `.augment/rules/coding-standards.md`.
*   **Windsurf:** Follow `.windsurf/rules/coding-standards.md` (if applicable).
