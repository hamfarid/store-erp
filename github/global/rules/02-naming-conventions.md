# 🏷️ Naming Conventions (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel (Linter)

## 1. The Philosophy
Names are the first documentation. If the name is ambiguous, the code is broken.

## 2. Universal Rules
*   **Descriptive:** `user_email` ✅, `ue` ❌.
*   **English:** All names MUST be in English.
*   **No Hungarians:** No type prefixes (`strName` ❌).

## 3. Language Specifics
### Python
*   **Variables/Functions:** `snake_case` (e.g., `calculate_total`).
*   **Classes:** `PascalCase` (e.g., `OrderProcessor`).
*   **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`).

### JavaScript/TypeScript
*   **Variables/Functions:** `camelCase` (e.g., `calculateTotal`).
*   **Classes/Components:** `PascalCase` (e.g., `UserProfile`).
*   **Constants:** `UPPER_SNAKE_CASE` (e.g., `API_ENDPOINT`).

## 4. File Naming
*   **Python:** `snake_case.py` (e.g., `order_service.py`).
*   **JavaScript/React:** `PascalCase.jsx` for components, `camelCase.js` for utilities.
*   **CSS/Assets:** `kebab-case` (e.g., `main-style.css`).
