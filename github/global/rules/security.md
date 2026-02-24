# 🔒 Security Rules (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by `tools/preflight_check.py`

## Mindset
**You are paranoid. Everything is a threat until proven safe.**

## Core Principles
- **Trust No Input:** Validate everything.
- **Zero Secrets:** No API keys in code. Ever.
- **Automated Defense:** Sentinel watches everything.

## The Sentinel Protocol
1.  **Secret Scanning:** Sentinel blocks any commit with regex patterns matching API keys, passwords, or tokens.
2.  **TODO Scanning:** Sentinel blocks "TODO" comments in security-critical files.
3.  **Dependency Check:** CodeRabbit (if active) flags vulnerable dependencies.

## Input Validation
- **SQL Injection:** MUST use parameterized queries. Sentinel blocks `f"SELECT...`.
- **XSS:** MUST use framework auto-escaping.
- **Validation:** Use Pydantic/Zod for strict schema validation.

## Authentication & Authorization
- **Passwords:** Use bcrypt/Argon2.
- **Sessions:** Secure, HTTPOnly cookies.
- **RBAC:** Check permissions on EVERY request.

## Data Protection
- **Encryption:** Encrypt sensitive data at rest and in transit.
- **HTTPS:** Enforce HTTPS everywhere.
- **Logs:** Never log PII or secrets.

## Remember
**Security is not a feature. It is the foundation.**
**If Sentinel blocks you, thank it.**

## Related Prompts
- `prompts/31_authentication.md` — Authentication implementation
