# Security Audit Workflow

This workflow performs a comprehensive security audit of the codebase.

## Steps

1. **Dependency Vulnerability Scan**
   - Run: `npm audit` (Node.js)
   - Run: `safety check` (Python)
   - Run: `bundle audit` (Ruby)

2. **Static Code Analysis**
   - Run: `eslint` with security rules
   - Run: `bandit` (Python)
   - Run: `brakeman` (Ruby on Rails)

3. **Secret Detection**
   - Run: `git-secrets --scan`
   - Run: `trufflehog`
   - Check for hardcoded API keys, passwords

4. **SQL Injection Check**
   - Review all database queries
   - Ensure parameterized queries are used
   - Run: `sqlmap` for automated testing

5. **XSS Vulnerability Check**
   - Review all user input handling
   - Ensure proper sanitization
   - Run: `XSStrike` for automated testing

6. **Authentication & Authorization Review**
   - Verify JWT implementation
   - Check password hashing (bcrypt, Argon2)
   - Review role-based access control

7. **API Security Check**
   - Verify rate limiting is enabled
   - Check CORS configuration
   - Ensure HTTPS is enforced

8. **Generate Security Report**
   - Document all findings
   - Prioritize by severity (Critical, High, Medium, Low)
   - Create remediation plan
