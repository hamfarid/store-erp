# Security Best Practices (Global System Ultimate)

## Core Philosophy
**"Security by Design."** Security is not an afterthought; it is integrated into every layer of the application stack. We follow the **OWASP Top 10** guidelines and the **OWASP Top 10 for LLM Applications**.

## 1. Authentication & Identity
*   **Password Storage:** NEVER store plain text passwords. Use **Argon2id** or **bcrypt** with a work factor of at least 12.
*   **MFA:** Enforce Multi-Factor Authentication for sensitive accounts.
*   **Tokens:** Use **JWT** (JSON Web Tokens) for stateless auth.
    *   Short-lived Access Tokens (15-30 mins).
    *   Secure, HttpOnly Cookies for Refresh Tokens.
*   **OAuth:** Use standard libraries (e.g., Passport, NextAuth) for social login.

## 2. Authorization & Access Control
*   **Principle of Least Privilege:** Users/Services should only have the permissions necessary for their function.
*   **RBAC/ABAC:** Implement Role-Based or Attribute-Based Access Control.
*   **IDOR Prevention:** Always verify that the authenticated user owns the resource they are trying to access (e.g., `/api/orders/123`).

## 3. Data Protection
*   **Encryption at Rest:** Encrypt sensitive data in the database (PII, secrets).
*   **Encryption in Transit:** Enforce **TLS 1.2+ (HTTPS)** everywhere. No HTTP allowed.
*   **Secrets Management:** Use environment variables (`.env`) or secret managers (Vault, AWS Secrets Manager). NEVER commit secrets to Git.

## 4. Input Validation & Sanitization
*   **Validate Everything:** Trust no one. Validate all incoming data (body, query, params) against strict schemas (Zod, Pydantic, Joi).
*   **Sanitize Output:** Escape all user-generated content to prevent XSS.
*   **SQL Injection:** ALWAYS use parameterized queries or ORMs. NEVER concatenate strings into SQL.

## 5. API Security
*   **Rate Limiting:** Implement rate limiting (e.g., Redis-based) to prevent abuse and DDoS.
*   **CORS:** Configure Cross-Origin Resource Sharing strictly. Allow only trusted domains.
*   **Security Headers:** Use Helmet (Node.js) or similar to set headers:
    *   `Content-Security-Policy` (CSP)
    *   `Strict-Transport-Security` (HSTS)
    *   `X-Content-Type-Options: nosniff`
    *   `X-Frame-Options: DENY`

## 6. Infrastructure Security
*   **Updates:** Keep dependencies and OS patched and up-to-date.
*   **Logging:** Log security events (failed logins, access denied) but NEVER log sensitive data (passwords, tokens).
*   **Firewalls:** Use WAF (Web Application Firewall) and restrict port access.

## 7. AI & LLM Security (New for 2025)
*   **Prompt Injection Defense:**
    *   **Input Filtering:** Sanitize user inputs to remove potential injection vectors (e.g., "Ignore previous instructions").
    *   **Output Validation:** Validate LLM outputs against expected formats (JSON schema) to prevent data exfiltration.
    *   **Instruction Hierarchy:** Use system prompts to explicitly prioritize core instructions over user inputs.
*   **Data Privacy in RAG:**
    *   **Access Control:** Ensure the retrieval system respects user permissions (ACLs) when fetching documents.
    *   **PII Redaction:** Automatically redact Personally Identifiable Information (PII) before sending context to the LLM.
*   **Model Denial of Service (DoS):**
    *   **Token Limits:** Enforce strict token limits on user inputs to prevent resource exhaustion.
    *   **Cost Controls:** Monitor API usage and implement budget caps to prevent financial DoS attacks.
*   **Supply Chain Security:**
    *   **Model Provenance:** Verify the source and integrity of any open-source models or weights used.
    *   **Dependency Scanning:** Regularly scan Python/Node.js dependencies for vulnerabilities using tools like `pip-audit` or `npm audit`.
