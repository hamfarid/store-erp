# T28: DAST Enhancement - Execution Guide

**Date:** 2025-11-08  
**Task:** T28 - DAST Scanning Enhancement  
**Status:** 🔄 Ready to Execute  
**Effort:** 2-3 hours  
**Priority:** P1 - High

---

## Quick Summary

**What's Done:**
- ✅ ZAP configuration created
- ✅ Results parser script created
- ✅ Enhanced security workflow created
- ✅ E2E testing workflow created
- ✅ Comprehensive documentation created

**What You Need to Do:**
1. Test DAST scan locally
2. Verify CI/CD integration
3. Review and fix any findings
4. Document results

---

## Files Created

### Configuration
- `scripts/dast/zap-config.yaml` - OWASP ZAP configuration

### Scripts
- `scripts/dast/parse-zap-results.js` - Results parser

### Workflows
- `.github/workflows/security-enhanced.yml` - Enhanced security workflow
- `.github/workflows/e2e-tests.yml` - E2E testing workflow

### Documentation
- `docs/security/DAST_SCANNING.md` - Comprehensive DAST guide
- `docs/T28_EXECUTION_GUIDE.md` - This file

---

## Execution Steps

### Step 1: Install Docker (if not installed)

```bash
# Check if Docker is installed
docker --version

# If not installed, download from:
# https://www.docker.com/products/docker-desktop
```

---

### Step 2: Pull OWASP ZAP Docker Image (10 min)

```bash
# Pull the latest stable ZAP image
docker pull owasp/zap2docker-stable

# Verify installation
docker images | grep zap
```

**Expected Output:**
```
owasp/zap2docker-stable   latest   abc123def456   2 weeks ago   1.2GB
```

---

### Step 3: Start Backend Server (5 min)

```bash
# Terminal 1: Start backend
cd backend
python app.py
```

**Wait for:** `Running on http://localhost:5000`

---

### Step 4: Run DAST Scan Locally (15-20 min)

```bash
# Terminal 2: Run ZAP baseline scan
docker run --network host -t owasp/zap2docker-stable zap-baseline.py \
  -t http://127.0.0.1:5000 \
  -r zap-baseline.html \
  -J zap-baseline.json
```

**Expected Output:**
```
WARN-NEW: X-Frame-Options Header Not Set [10020]
WARN-NEW: X-Content-Type-Options Header Missing [10021]
...
PASS: All Scans Completed
```

---

### Step 5: Parse Results (5 min)

```bash
# Parse ZAP JSON output
node scripts/dast/parse-zap-results.js
```

**Expected Output:**
```
📊 Parsing OWASP ZAP Report...
✅ Report parsed successfully
✅ Markdown report generated: zap-findings.md
✅ PR comment generated: zap-pr-comment.md
✅ Security scan PASSED
```

---

### Step 6: Review Findings (15-30 min)

```bash
# Open HTML report in browser
start zap-baseline.html  # Windows
open zap-baseline.html   # macOS
xdg-open zap-baseline.html  # Linux

# Or view markdown report
cat zap-findings.md
```

**Review:**
- High severity issues (fix immediately)
- Medium severity issues (fix in sprint)
- Low severity issues (backlog)
- False positives (document)

---

### Step 7: Fix High-Severity Issues (30-60 min)

#### Common Fixes

**1. Add Security Headers**

Edit `backend/src/security_middleware.py`:

```python
@app.after_request
def set_security_headers(response):
    """Set security headers on all responses"""
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response
```

**2. Secure Cookies**

```python
# Set secure flags on cookies
response.set_cookie(
    'session',
    value,
    secure=True,
    httponly=True,
    samesite='Strict'
)
```

**3. CSRF Protection**

```python
# Already implemented in security_middleware.py
# Verify it's enabled for all POST/PUT/DELETE routes
```

---

### Step 8: Re-run Scan (10 min)

```bash
# Re-run scan after fixes
docker run --network host -t owasp/zap2docker-stable zap-baseline.py \
  -t http://127.0.0.1:5000 \
  -r zap-baseline-fixed.html \
  -J zap-baseline-fixed.json

# Parse results
node scripts/dast/parse-zap-results.js
```

**Verify:**
- High-severity issues resolved
- Medium-severity issues reduced
- No new issues introduced

---

### Step 9: Commit Changes (10 min)

```bash
# Add all new files
git add scripts/dast/
git add .github/workflows/security-enhanced.yml
git add .github/workflows/e2e-tests.yml
git add docs/security/DAST_SCANNING.md
git add docs/T28_EXECUTION_GUIDE.md

# Commit security fixes
git add backend/src/security_middleware.py
git commit -m "feat(security): enhance DAST scanning with OWASP ZAP

- Add ZAP configuration with custom rules
- Add results parser for automated analysis
- Add enhanced security workflow
- Add E2E testing workflow
- Fix high-severity security findings
- Add comprehensive DAST documentation

Closes #T28"

# Push changes
git push
```

---

### Step 10: Verify CI/CD Integration (15 min)

```bash
# Create a test PR
git checkout -b test/dast-enhancement
git push -u origin test/dast-enhancement

# Create PR on GitHub
# Verify workflows run:
# - security-enhanced.yml
# - e2e-tests.yml

# Check PR comments for security findings
```

---

## Success Criteria

### ✅ Local Testing
- [ ] ZAP scan runs successfully
- [ ] Results parsed correctly
- [ ] High-severity issues fixed
- [ ] Re-scan shows improvement

### ✅ CI/CD Integration
- [ ] Security workflow runs on PR
- [ ] E2E workflow runs on PR
- [ ] Results posted as PR comments
- [ ] Artifacts uploaded

### ✅ Documentation
- [ ] DAST guide complete
- [ ] Execution guide complete
- [ ] Findings documented
- [ ] False positives documented

### ✅ Security Improvements
- [ ] Zero high-severity findings
- [ ] <5 medium-severity findings
- [ ] Security headers added
- [ ] Cookies secured

---

## Timeline

### Phase 1: Setup (15 min)
- [ ] Install Docker
- [ ] Pull ZAP image
- [ ] Start backend

### Phase 2: Initial Scan (20 min)
- [ ] Run ZAP scan
- [ ] Parse results
- [ ] Review findings

### Phase 3: Fix Issues (60 min)
- [ ] Fix high-severity issues
- [ ] Fix medium-severity issues
- [ ] Re-run scan
- [ ] Verify fixes

### Phase 4: Integration (30 min)
- [ ] Commit changes
- [ ] Create PR
- [ ] Verify CI/CD
- [ ] Document results

**Total: 2-3 hours**

---

## Troubleshooting

### Docker Issues

**Problem:** Docker not installed

**Solution:**
```bash
# Download Docker Desktop
# Windows/Mac: https://www.docker.com/products/docker-desktop
# Linux: sudo apt-get install docker.io
```

**Problem:** Permission denied

**Solution:**
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Scan Issues

**Problem:** Can't connect to backend

**Solution:**
```bash
# Verify backend is running
curl http://localhost:5000/health

# Use --network host for Docker
docker run --network host -t owasp/zap2docker-stable ...
```

**Problem:** Scan takes too long

**Solution:**
```bash
# Use baseline scan instead of full scan
# Reduce max depth in zap-config.yaml
# Exclude static assets
```

### Parser Issues

**Problem:** Node.js not found

**Solution:**
```bash
# Install Node.js
# Download from: https://nodejs.org/
```

**Problem:** JSON parse error

**Solution:**
```bash
# Verify JSON file exists
ls -la zap-baseline.json

# Check JSON is valid
cat zap-baseline.json | jq .
```

---

## Next Steps

After T28 is complete:

1. ✅ T28: DAST Enhancement - COMPLETE
2. ⏳ T29: Deployment Automation (3-4h)
3. ⏳ T32: Documentation Finalization (2-3h)
4. ⏳ T33: Final Testing & Verification (2-3h)

---

## Resources

### Documentation
- **DAST Guide:** `docs/security/DAST_SCANNING.md`
- **ZAP Config:** `scripts/dast/zap-config.yaml`
- **Parser Script:** `scripts/dast/parse-zap-results.js`

### External Resources
- **OWASP ZAP:** https://www.zaproxy.org/
- **ZAP Docker:** https://www.zaproxy.org/docs/docker/
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/

---

## Quick Commands

```bash
# Pull ZAP image
docker pull owasp/zap2docker-stable

# Run baseline scan
docker run --network host -t owasp/zap2docker-stable zap-baseline.py \
  -t http://127.0.0.1:5000 \
  -r zap-baseline.html \
  -J zap-baseline.json

# Parse results
node scripts/dast/parse-zap-results.js

# View report
start zap-baseline.html

# Commit changes
git add .
git commit -m "feat(security): enhance DAST scanning"
git push
```

---

**Document Version:** 1.0  
**Created:** 2025-11-08  
**Status:** Ready for Execution

