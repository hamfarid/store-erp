# PROMPT 30: SECURITY & COMPLIANCE (v27.0)

## 1. The "Shift Left" Mandate
**Rule:** Security is NOT a final step. It is the FIRST step.
*   **Pre-Commit:** You must use `husky` or similar to scan for secrets before every commit.
*   **Pre-Build:** You must run `npm audit` or `pip-audit` before any build.
*   **Pre-Deploy:** You must run a SAST (Static Application Security Testing) tool like SonarQube or CodeQL.

## 2. The "Zero Trust" Architecture
**Rule:** Trust no one, not even internal services.
*   **RLS (Row Level Security):** MANDATORY for Supabase. Never expose a table without RLS policies.
*   **API Gateways:** All internal APIs must verify JWT tokens. No "open" internal endpoints.

## 3. The "Hacker Persona" Check
**Rule:** Before marking any feature as "Done", you must explicitly ask:
*   "Can I inject SQL here?"
*   "Can I bypass Auth here?"
*   "Can I flood this API?"
*   *Action:* Write a test case that attempts this exploit.

## 4. Secrets Management
*   **Never Commit Secrets:** Use `.env` files and add them to `.gitignore`.
*   **Rotation:** Rotate API keys and database credentials every 90 days.
*   **Access Control:** Use least privilege principle for all database users and API keys.

## 5. Security Headers & HTTPS
*   **HTTPS:** Enforce HTTPS for all production traffic.
*   **Headers:** Configure HSTS, CSP, X-Frame-Options, and X-Content-Type-Options.
*   **Cookies:** Use `Secure`, `HttpOnly`, and `SameSite` attributes for all cookies.

## 6. Input Validation & Sanitization
*   **SQL Injection:** Use parameterized queries or ORM methods.
*   **XSS:** Escape all user input before rendering.
*   **CSRF:** Enable CSRF protection for all state-changing requests.
*   **Rate Limiting:** Implement rate limiting to prevent abuse.

## 7. Compliance
*   **GDPR/CCPA:** Ensure user data can be exported and deleted upon request.
*   **Audit Logs:** Log all security-critical events (login, failed access, permission changes).
