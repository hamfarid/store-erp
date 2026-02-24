# 00. PRIORITY ORDER (THE PRIME DIRECTIVE)

**This file dictates the absolute hierarchy of your decision-making process.**

## 1. SECURITY (Highest Priority)
-   **Zero Trust:** Assume all inputs are malicious.
-   **Authentication/Authorization:** Never bypass auth checks.
-   **Data Protection:** Encrypt sensitive data.
-   **Dependencies:** No vulnerable packages.

## 2. CORRECTNESS & RELIABILITY
-   **Functionality:** The code must do exactly what is requested.
-   **Testing:** Minimum 80% coverage. No untested code.
-   **Idempotency:** All mutations must be idempotent.
-   **Error Handling:** No unhandled exceptions.

## 3. ARCHITECTURAL INTEGRITY (Nx & Supabase)
-   **Structure:** Adhere to Nx Monorepo structure.
-   **Database:** Follow Supabase/PostgreSQL best practices (RLS, Normalization).
-   **Separation of Concerns:** Strict boundary between UI, Logic, and Data.

## 4. MAINTAINABILITY & DOCUMENTATION
-   **Readability:** Clean, self-documenting code.
-   **Documentation:** Speckit-style JIT docs.
-   **Logging:** Structured JSON logs for everything.

## 5. PERFORMANCE
-   **Optimization:** Efficient queries, caching, and lazy loading.
-   **Scalability:** Design for growth.

## 6. USER EXPERIENCE
-   **Responsiveness:** Fast UI feedback.
-   **Accessibility:** WCAG compliance.

**Conflict Resolution:**
If a lower priority conflicts with a higher priority, the **HIGHER PRIORITY WINS**.
*Example: If a performance optimization (5) compromises security (1), you MUST reject the optimization.*
