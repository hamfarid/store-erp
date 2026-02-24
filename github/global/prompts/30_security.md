# Security & Compliance (Global System v26 Diamond 32 Synchronized Intelligence Edition)

**Version:** 37.0
**Engine:** Speckit Global System v26 Diamond 32 + Sentinel
**Status:** MANDATORY

## 1. The "Shift Left" Mandate (Sentinel)
**Rule:** Security is NOT a final step. It is the FIRST step.
*   **Pre-Commit:** Sentinel checks for secrets and TODOs.
*   **Pre-Build:** `speckit verify` runs SAST checks.
*   **Pre-Deploy:** Automated penetration testing.

## 2. The "Zero Trust" Architecture
**Rule:** Trust no one, not even internal services.
*   **RLS:** MANDATORY for Supabase.
*   **JWT:** Verify tokens on EVERY request.
*   **Least Privilege:** Minimal database permissions.

## 3. The "Hacker Persona" Check (Speckit Verify)
**Rule:** Before marking any feature as "Done", run `speckit verify` to simulate attacks:
*   SQL Injection
*   XSS (Cross-Site Scripting)
*   IDOR (Insecure Direct Object References)

## 4. Secrets Management (Sentinel)
*   **NEVER** commit secrets. Sentinel will block you.
*   **Use** `.env` for local development.
*   **Use** Secret Managers (AWS Secrets Manager, Vault) for production.

## 5. Compliance
*   **GDPR:** Data export/deletion capabilities.
*   **Audit Logs:** Log all sensitive actions to `system_log.md` and DB.
