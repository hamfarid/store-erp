# 🧪 Test-First Protocol

**Purpose:** Eliminate regression and ensure code correctness by writing tests *before* implementation.

## 1. The Rule
**"No Code Without a Failing Test."**

## 2. The Workflow
1.  **Red:** Write a test case that defines the expected behavior. Run it. It MUST fail.
2.  **Green:** Write the *minimum* amount of code to make the test pass.
3.  **Refactor:** Clean up the code while keeping the test green.

## 3. Integration
*   **Frontend:** Write `.test.tsx` or `.spec.ts` before the component.
*   **Backend:** Write `test_*.py` or `*.test.js` before the endpoint logic.

## 4. Verification
Run `speckit verify` (which triggers the test suite) before marking any task as complete.
