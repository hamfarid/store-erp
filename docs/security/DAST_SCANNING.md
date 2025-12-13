# DAST Scanning with OWASP ZAP

**Date:** 2025-11-08  
**Task:** T28 - DAST Enhancement  
**Status:** Ready to Execute  
**Version:** 1.0

---

## Overview

This document describes the Dynamic Application Security Testing (DAST) implementation using OWASP ZAP for the Store ERP system.

### What is DAST?

DAST (Dynamic Application Security Testing) is a black-box security testing methodology that analyzes running applications to identify security vulnerabilities. Unlike SAST (Static Application Security Testing), DAST tests the application from the outside, simulating real-world attacks.

### Why OWASP ZAP?

- **Open Source:** Free and actively maintained
- **Comprehensive:** Tests for OWASP Top 10 vulnerabilities
- **Automated:** Integrates with CI/CD pipelines
- **Flexible:** Supports various authentication methods
- **Detailed Reports:** Provides actionable findings

---

## Architecture

### Scan Types

1. **Baseline Scan** (Default)
   - Quick passive scan
   - No active attacks
   - Safe for production
   - Duration: 2-5 minutes

2. **Full Scan**
   - Active + passive scanning
   - Comprehensive testing
   - May impact performance
   - Duration: 15-30 minutes

3. **API Scan**
   - Focused on API endpoints
   - OpenAPI/Swagger support
   - REST API testing
   - Duration: 5-10 minutes

### Vulnerability Detection

ZAP detects:
- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Security Misconfiguration
- Sensitive Data Exposure
- Broken Authentication
- XML External Entities (XXE)
- Insecure Deserialization
- Using Components with Known Vulnerabilities
- Insufficient Logging & Monitoring

---

## Configuration

### ZAP Configuration File

Location: `scripts/dast/zap-config.yaml`

Key sections:
- **Scan Configuration:** URL, depth, threads
- **Authentication:** Form-based login
- **Active Scan:** Custom rules and policies
- **Passive Scan:** Enabled rules
- **Exclusions:** URLs and parameters to skip
- **Custom Rules:** Project-specific checks
- **Alert Filtering:** False positive handling

### Authentication Setup

```yaml
authentication:
  type: "form"
  loginUrl: "http://localhost:5000/api/auth/login"
  username: "admin"
  password: "admin123"
  usernameField: "username"
  passwordField: "password"
  loggedInIndicator: "dashboard|authenticated|token"
  loggedOutIndicator: "login|unauthorized|401"
```

### Custom Rules

1. **Hardcoded Credentials Detection**
   - Pattern: `(password|secret|api_key|token)\s*[=:]\s*['\"]?[a-zA-Z0-9]{8,}['\"]?`
   - Severity: HIGH

2. **Debug Information Disclosure**
   - Pattern: `(debug|trace|stack trace|exception|error at line)`
   - Severity: MEDIUM

3. **SQL Injection Patterns**
   - Pattern: `(union|select|insert|update|delete|drop|create)\s+(from|into|table|database)`
   - Severity: HIGH

4. **XXE Injection Patterns**
   - Pattern: `<!ENTITY|SYSTEM|PUBLIC`
   - Severity: HIGH

---

## Running DAST Scans

### Local Execution

#### Prerequisites
```bash
# Install Docker
docker --version

# Pull ZAP image
docker pull owasp/zap2docker-stable
```

#### Run Baseline Scan
```bash
# Start backend
cd backend
python app.py

# Run ZAP scan (in another terminal)
docker run --network host -t owasp/zap2docker-stable zap-baseline.py \
  -t http://127.0.0.1:5000 \
  -r zap-baseline.html \
  -J zap-baseline.json
```

#### Run Full Scan
```bash
docker run --network host -t owasp/zap2docker-stable zap-full-scan.py \
  -t http://127.0.0.1:5000 \
  -r zap-full.html \
  -J zap-full.json
```

#### Run API Scan
```bash
docker run --network host -t owasp/zap2docker-stable zap-api-scan.py \
  -t http://127.0.0.1:5000/api \
  -f openapi \
  -r zap-api.html \
  -J zap-api.json
```

### CI/CD Execution

The DAST scan runs automatically on:
- **Pull Requests:** To `main` or `development` branches
- **Push:** To `main` branch
- **Schedule:** Daily at 2 AM UTC
- **Manual:** Via workflow dispatch

Workflow file: `.github/workflows/security-enhanced.yml`

---

## Results Analysis

### Severity Levels

| Severity | Risk Code | Action Required |
|----------|-----------|-----------------|
| 🔴 High | 3 | Fix immediately (24h) |
| 🟠 Medium | 2 | Fix in current sprint (1 week) |
| 🟡 Low | 1 | Fix in future sprint (2 weeks) |
| ℹ️ Info | 0 | Review and document |

### Report Files

1. **zap-baseline.html** - Visual HTML report
2. **zap-baseline.json** - Machine-readable JSON
3. **zap-findings.md** - Markdown summary
4. **zap-pr-comment.md** - PR comment

### Parsing Results

```bash
# Parse ZAP JSON output
node scripts/dast/parse-zap-results.js

# Output files:
# - zap-findings.md (detailed findings)
# - zap-pr-comment.md (PR comment)
```

---

## Common Findings & Solutions

### 1. Missing Security Headers

**Finding:** Missing X-Frame-Options, X-Content-Type-Options, CSP

**Solution:**
```python
# backend/src/security_middleware.py
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

### 2. Cookie without Secure Flag

**Finding:** Cookies not marked as Secure

**Solution:**
```python
# Set secure flag on cookies
response.set_cookie('session', value, secure=True, httponly=True, samesite='Strict')
```

### 3. SQL Injection

**Finding:** Potential SQL injection in query

**Solution:**
```python
# Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### 4. XSS Vulnerability

**Finding:** Unescaped user input in HTML

**Solution:**
```javascript
// Escape user input
const escaped = DOMPurify.sanitize(userInput);
```

### 5. CSRF Missing

**Finding:** Missing CSRF protection

**Solution:**
```python
# Use Flask-WTF CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

---

## False Positives

### Handling False Positives

1. **Review Finding:** Verify it's actually a false positive
2. **Document Reason:** Add to `zap-config.yaml`
3. **Ignore Alert:** Add to `alertFiltering.ignoreAlerts`

Example:
```yaml
alertFiltering:
  ignoreAlerts:
    - id: "10010"
      reason: "HttpOnly flag not required for this cookie"
```

---

## Best Practices

### 1. Run Regularly
- **PR Checks:** Every pull request
- **Scheduled:** Daily or weekly
- **Pre-Release:** Before every deployment

### 2. Fix High Severity First
- Address critical issues immediately
- Don't deploy with high-severity findings
- Track medium/low issues in backlog

### 3. Integrate with Development
- Add security tests to unit tests
- Train developers on secure coding
- Review findings in sprint planning

### 4. Monitor Trends
- Track findings over time
- Measure improvement
- Set security KPIs

### 5. Keep Updated
- Update ZAP regularly
- Review new rules
- Update custom rules

---

## Troubleshooting

### Scan Fails to Start

**Issue:** ZAP can't connect to target

**Solution:**
```bash
# Check if backend is running
curl http://localhost:5000/health

# Check Docker network
docker run --network host -t owasp/zap2docker-stable zap-baseline.py -t http://127.0.0.1:5000
```

### Authentication Fails

**Issue:** ZAP can't authenticate

**Solution:**
- Verify credentials in `zap-config.yaml`
- Check login URL
- Verify logged-in indicator regex

### Too Many False Positives

**Issue:** Many irrelevant findings

**Solution:**
- Add exclusions to `zap-config.yaml`
- Tune custom rules
- Update alert filtering

### Scan Takes Too Long

**Issue:** Scan exceeds timeout

**Solution:**
- Use baseline scan instead of full
- Reduce max depth
- Exclude static assets

---

## Resources

### Documentation
- [OWASP ZAP Docs](https://www.zaproxy.org/docs/)
- [ZAP Docker](https://www.zaproxy.org/docs/docker/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Tools
- [ZAP Desktop](https://www.zaproxy.org/download/)
- [ZAP API](https://www.zaproxy.org/docs/api/)
- [ZAP Extensions](https://www.zaproxy.org/addons/)

### Training
- [OWASP Security Training](https://owasp.org/www-project-web-security-testing-guide/)
- [Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

---

## Metrics

### Success Criteria
- ✅ Zero high-severity findings
- ✅ <5 medium-severity findings
- ✅ Scan completes in <5 minutes
- ✅ No false positives

### KPIs
- **Scan Frequency:** Daily
- **Fix Time (High):** <24 hours
- **Fix Time (Medium):** <1 week
- **Coverage:** 100% of API endpoints

---

**Document Version:** 1.0  
**Created:** 2025-11-08  
**Status:** Ready for Use

