# 🔧 Backend Development Rules (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel & CodeRabbit

## 1. The Philosophy
Backend code is the engine of truth. It must be robust, secure, and efficient.

## 2. Core Principles
*   **Validation:** Trust NO input. Validate everything at the controller level.
*   **Idempotency:** APIs MUST be idempotent where possible.
*   **Statelessness:** Servers MUST be stateless. Use Redis/Database for state.

## 3. Architecture
*   **Layered Design:** Controller -> Service -> Model. No skipping layers.
*   **Dependency Injection:** Use DI for testability.
*   **Async/Await:** MUST use async/await for all I/O operations.

## 4. Security (Sentinel Enforced)
*   **SQL Injection:** MUST use parameterized queries (ORM or Prepared Statements).
*   **Secrets:** NEVER hardcode secrets. Use `.env`.
*   **Auth:** Validate JWT on every protected route.

## 5. Error Handling
*   **Centralized:** Use a global error handler middleware.
*   **Logging:** Log errors with stack traces (internal only) and request IDs.
*   **Response:** Return standard error JSON structure (Code, Message, Details).

## 6. Testing
*   **Unit Tests:** Mock external dependencies.
*   **Integration Tests:** Test API endpoints with a test database.
*   **Coverage:** Minimum 80% required.
