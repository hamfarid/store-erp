# Living Documentation (Global System Ultimate Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System Ultimate
**Status:** MANDATORY

## 1. The "Atomic Update" Rule (Speckit Verify)
**Rule:** Documentation is NOT a separate phase. It happens **atomically** with code changes.
*   **Code Change:** Update function signature? -> Update docstring IMMEDIATELY.
*   **API Change:** Update endpoint? -> Update Swagger/OpenAPI IMMEDIATELY.
*   **DB Change:** Update schema? -> Update `DATABASE_SCHEMA.md` IMMEDIATELY.

## 2. The "Speckit" Integration
**Rule:** Use `speckit verify` to check documentation freshness.
*   **Check:** "Does the code match the docs?"
*   **Action:** If NO, Sentinel blocks the commit.

## 3. The "Why" over "What"
**Rule:** Comments should explain WHY, not WHAT.
*   ❌ `// Increment i by 1`
*   ✅ `// Increment retry counter to trigger exponential backoff`

## 4. Visual Documentation
**Rule:** Use Mermaid diagrams for complex logic.
*   **Flowcharts:** Business logic.
*   **Sequence Diagrams:** API interactions.
*   **ER Diagrams:** Database relationships.

## 5. User Documentation
*   **README.md:** Must include "Powered by Speckit Global System Ultimate" badge.
*   **API Docs:** Auto-generated via Swagger/Redoc.
