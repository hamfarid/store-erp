# Code Style Rules (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel & Linter

## 1. The Philosophy
Code style is not a suggestion; it is a law. Inconsistent code is a security risk.

## 2. General Rules
*   **Indentation:**
    *   **JavaScript/TypeScript:** MUST use 2 spaces.
    *   **Python:** MUST use 4 spaces.
*   **Line Length:** MUST NOT exceed 100 characters.
*   **Quotes:** MUST use single quotes `'` for strings (unless interpolation is needed).

## 3. JavaScript/TypeScript
*   **Variables:** MUST use `const` by default. `let` is allowed only if reassignment is proven necessary. `var` is FORBIDDEN.
*   **Functions:** MUST use arrow functions for callbacks.
*   **Strings:** MUST use template literals for interpolation.
*   **Semicolons:** MUST be used at the end of every statement.

## 4. Python
*   **Style Guide:** MUST strictly follow PEP 8.
*   **Type Hints:** MUST be present for all function signatures.
*   **Docstrings:** MUST be present for all public functions and classes (Google Style).
*   **Naming:**
    *   Variables/Functions: `snake_case`
    *   Classes: `PascalCase`
    *   Constants: `UPPER_CASE`

## 5. Enforcement
*   **Pre-Commit:** The Sentinel Hook WILL block any commit that fails linting.
*   **Commands:**
    *   JS/TS: `npm run lint`
    *   Python: `flake8`
