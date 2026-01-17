# 🔒 Security Scanning Automation

**Priority:** HIGH  
**Phase:** 5 (Security) & 6 (Deployment)  
**Status:** Production Ready

---

## 🎯 Purpose

Automate security scanning to detect vulnerabilities, secrets, and compliance issues using **SAST**, **Dependency Scanning**, **Secret Detection**, and **License Compliance** tools.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Scanning Types](#scanning-types)
3. [Tools](#tools)
4. [Implementation](#implementation)
5. [CI/CD Integration](#cicd-integration)
6. [Reporting](#reporting)
7. [Best Practices](#best-practices)

---

## 1. Overview

### What is Security Scanning?

Automated analysis of code, dependencies, and configurations to identify security vulnerabilities before they reach production.

### Why It Matters

**Security Impact:**
- 60% of breaches involve unpatched vulnerabilities
- Average cost of data breach: $4.35M
- 43% of cyber attacks target small businesses

**Business Impact:**
- Prevent data breaches
- Protect customer trust
- Ensure compliance
- Reduce remediation costs

---

## 2. Scanning Types

### 1. Dependency Vulnerability Scanning
**Scans:** Third-party packages for known vulnerabilities  
**Tools:** npm audit, Snyk, OWASP Dependency-Check  
**Frequency:** Every commit + daily

### 2. SAST (Static Application Security Testing)
**Scans:** Source code for security flaws  
**Tools:** SonarQube, Semgrep, CodeQL  
**Frequency:** Every pull request

### 3. Secret Detection
**Scans:** Hardcoded secrets, API keys, passwords  
**Tools:** GitGuardian, TruffleHog, detect-secrets  
**Frequency:** Every commit

### 4. License Compliance
**Scans:** License compatibility and violations  
**Tools:** FOSSA, LicenseFinder, license-checker  
**Frequency:** Weekly + before release

---

## 3. Tools

### 1. npm audit (Built-in)

**Usage:**
```bash
# Check for vulnerabilities
npm audit

# Fix automatically
npm audit fix

# Force fix (may break things)
npm audit fix --force

# Get JSON report
npm audit --json > audit-report.json
```

**Configuration:**
```json
// .npmrc
audit-level=moderate
```

---

### 2. Snyk

**Installation:**
```bash
npm install -g snyk
snyk auth
```

**Usage:**
```bash
# Test for vulnerabilities
snyk test

# Monitor project
snyk monitor

# Fix vulnerabilities
snyk fix

# Test Docker images
snyk container test myimage:latest

# Test Infrastructure as Code
snyk iac test terraform/
```

**Configuration:**
```yaml
# .snyk
version: v1.22.0
ignore:
  'SNYK-JS-LODASH-590103':
    - '*':
        reason: 'Not exploitable in our use case'
        expires: '2025-12-31'
patch: {}
```

---

### 3. SonarQube

**Installation:**
```bash
# Using Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
```

**Scanner Installation:**
```bash
npm install -g sonarqube-scanner
```

**Configuration:**
```properties
# sonar-project.properties
sonar.projectKey=my-project
sonar.projectName=My Project
sonar.projectVersion=1.0
sonar.sources=src
sonar.tests=tests
sonar.exclusions=**/node_modules/**,**/*.test.js
sonar.javascript.lcov.reportPaths=coverage/lcov.info
```

**Usage:**
```bash
# Run scanner
sonar-scanner

# With custom config
sonar-scanner -Dsonar.projectKey=my-project
```

---

### 4. Semgrep

**Installation:**
```bash
pip install semgrep
```

**Usage:**
```bash
# Scan with default rules
semgrep --config=auto .

# Scan for specific patterns
semgrep --config=p/security-audit .
semgrep --config=p/owasp-top-ten .
semgrep --config=p/jwt .

# Custom rules
semgrep --config=rules/custom.yml .

# Output JSON
semgrep --json --config=auto . > semgrep-report.json
```

**Custom Rules:**
```yaml
# rules/no-hardcoded-secrets.yml
rules:
  - id: hardcoded-api-key
    pattern: |
      const API_KEY = "..."
    message: "Hardcoded API key detected"
    severity: ERROR
    languages: [javascript, typescript]
  
  - id: hardcoded-password
    pattern: |
      password = "..."
    message: "Hardcoded password detected"
    severity: ERROR
    languages: [python, javascript]
```

---

### 5. TruffleHog (Secret Detection)

**Installation:**
```bash
pip install trufflehog
```

**Usage:**
```bash
# Scan repository
trufflehog git https://github.com/user/repo

# Scan local directory
trufflehog filesystem ./

# Scan with regex
trufflehog --regex --entropy=False git https://github.com/user/repo

# Output JSON
trufflehog --json git https://github.com/user/repo > secrets-report.json
```

---

### 6. GitGuardian

**Installation:**
```bash
pip install ggshield
```

**Configuration:**
```yaml
# .gitguardian.yml
version: 2
paths-ignore:
  - '**/tests/**'
  - '**/*.test.js'
matches-ignore:
  - name: 'Test API Key'
    match: 'test_api_key_12345'
```

**Usage:**
```bash
# Scan current directory
ggshield secret scan path .

# Scan git history
ggshield secret scan repo .

# Pre-commit hook
ggshield secret scan pre-commit
```

---

### 7. OWASP Dependency-Check

**Installation:**
```bash
# Using Docker
docker pull owasp/dependency-check
```

**Usage:**
```bash
# Scan project
docker run --rm \
  -v $(pwd):/src \
  owasp/dependency-check \
  --scan /src \
  --format HTML \
  --out /src/dependency-check-report.html
```

---

## 4. Implementation

### Step 1: Setup Dependency Scanning

```bash
# Install Snyk
npm install -g snyk
snyk auth

# Test project
snyk test

# Add to package.json
npm pkg set scripts.security:deps="snyk test"
npm pkg set scripts.security:fix="snyk fix"
```

---

### Step 2: Setup SAST

```bash
# Install Semgrep
pip install semgrep

# Create script
cat > scripts/sast-scan.sh << 'EOF'
#!/bin/bash
echo "Running SAST scan..."
semgrep --config=auto --json . > reports/sast-report.json
echo "SAST scan complete. Report: reports/sast-report.json"
EOF

chmod +x scripts/sast-scan.sh

# Add to package.json
npm pkg set scripts.security:sast="./scripts/sast-scan.sh"
```

---

### Step 3: Setup Secret Detection

```bash
# Install TruffleHog
pip install trufflehog

# Create script
cat > scripts/secret-scan.sh << 'EOF'
#!/bin/bash
echo "Scanning for secrets..."
trufflehog --json filesystem . > reports/secrets-report.json
if [ $? -eq 0 ]; then
  echo "✅ No secrets found"
else
  echo "❌ Secrets detected! Check reports/secrets-report.json"
  exit 1
fi
EOF

chmod +x scripts/secret-scan.sh

# Add to package.json
npm pkg set scripts.security:secrets="./scripts/secret-scan.sh"
```

---

### Step 4: Setup License Compliance

```bash
# Install license-checker
npm install --save-dev license-checker

# Create script
cat > scripts/license-check.sh << 'EOF'
#!/bin/bash
echo "Checking licenses..."
npx license-checker --json --out reports/licenses.json

# Check for forbidden licenses
npx license-checker --failOn "GPL;AGPL;LGPL"
EOF

chmod +x scripts/license-check.sh

# Add to package.json
npm pkg set scripts.security:licenses="./scripts/license-check.sh"
```

---

### Step 5: Create Master Security Script

```bash
# scripts/security-scan-all.sh
#!/bin/bash

echo "🔒 Running comprehensive security scan..."
echo ""

# Create reports directory
mkdir -p reports

# 1. Dependency scanning
echo "1️⃣  Dependency Vulnerability Scan"
npm audit --json > reports/npm-audit.json
snyk test --json > reports/snyk-report.json || true
echo "✅ Dependency scan complete"
echo ""

# 2. SAST
echo "2️⃣  Static Application Security Testing (SAST)"
semgrep --config=auto --json . > reports/sast-report.json || true
echo "✅ SAST complete"
echo ""

# 3. Secret detection
echo "3️⃣  Secret Detection"
trufflehog --json filesystem . > reports/secrets-report.json || true
echo "✅ Secret detection complete"
echo ""

# 4. License compliance
echo "4️⃣  License Compliance Check"
npx license-checker --json --out reports/licenses.json
echo "✅ License check complete"
echo ""

# Generate summary
echo "📊 Generating summary report..."
node scripts/generate-security-summary.js

echo ""
echo "✅ Security scan complete!"
echo "📁 Reports available in: reports/"
```

---

### Step 6: Create Summary Generator

```javascript
// scripts/generate-security-summary.js
const fs = require('fs');

function generateSummary() {
  const reports = {
    npm: JSON.parse(fs.readFileSync('reports/npm-audit.json', 'utf8')),
    snyk: JSON.parse(fs.readFileSync('reports/snyk-report.json', 'utf8')),
    sast: JSON.parse(fs.readFileSync('reports/sast-report.json', 'utf8')),
    secrets: JSON.parse(fs.readFileSync('reports/secrets-report.json', 'utf8')),
    licenses: JSON.parse(fs.readFileSync('reports/licenses.json', 'utf8'))
  };

  const summary = {
    timestamp: new Date().toISOString(),
    vulnerabilities: {
      critical: 0,
      high: 0,
      medium: 0,
      low: 0
    },
    secrets: {
      found: reports.secrets.length || 0
    },
    licenses: {
      total: Object.keys(reports.licenses).length,
      issues: []
    },
    passed: true
  };

  // Count npm audit vulnerabilities
  if (reports.npm.metadata) {
    summary.vulnerabilities.critical += reports.npm.metadata.vulnerabilities.critical;
    summary.vulnerabilities.high += reports.npm.metadata.vulnerabilities.high;
    summary.vulnerabilities.medium += reports.npm.metadata.vulnerabilities.moderate;
    summary.vulnerabilities.low += reports.npm.metadata.vulnerabilities.low;
  }

  // Check if passed
  if (summary.vulnerabilities.critical > 0 || summary.vulnerabilities.high > 0) {
    summary.passed = false;
  }
  if (summary.secrets.found > 0) {
    summary.passed = false;
  }

  // Generate markdown report
  const markdown = `# Security Scan Summary

**Date:** ${summary.timestamp}  
**Status:** ${summary.passed ? '✅ PASSED' : '❌ FAILED'}

---

## Vulnerabilities

| Severity | Count |
|----------|-------|
| Critical | ${summary.vulnerabilities.critical} |
| High | ${summary.vulnerabilities.high} |
| Medium | ${summary.vulnerabilities.medium} |
| Low | ${summary.vulnerabilities.low} |

---

## Secrets

**Found:** ${summary.secrets.found}

${summary.secrets.found > 0 ? '⚠️ **ACTION REQUIRED:** Remove secrets from code!' : '✅ No secrets detected'}

---

## Licenses

**Total Dependencies:** ${summary.licenses.total}

---

## Recommendations

${summary.vulnerabilities.critical > 0 ? '🚨 **CRITICAL:** Fix critical vulnerabilities immediately!' : ''}
${summary.vulnerabilities.high > 0 ? '⚠️ **HIGH:** Address high-severity vulnerabilities soon' : ''}
${summary.secrets.found > 0 ? '🔐 **SECRETS:** Remove hardcoded secrets and use environment variables' : ''}

---

## Next Steps

1. Review detailed reports in \`reports/\` directory
2. Fix critical and high-severity issues
3. Remove any detected secrets
4. Re-run security scan
5. Update dependencies regularly

---

**Generated by:** Global Professional Development System  
**Version:** 1.0
`;

  fs.writeFileSync('reports/SECURITY_SUMMARY.md', markdown);
  fs.writeFileSync('reports/security-summary.json', JSON.stringify(summary, null, 2));

  console.log('\n📊 Summary Report:');
  console.log('-------------------');
  console.log(`Status: ${summary.passed ? '✅ PASSED' : '❌ FAILED'}`);
  console.log(`Critical: ${summary.vulnerabilities.critical}`);
  console.log(`High: ${summary.vulnerabilities.high}`);
  console.log(`Medium: ${summary.vulnerabilities.medium}`);
  console.log(`Low: ${summary.vulnerabilities.low}`);
  console.log(`Secrets: ${summary.secrets.found}`);
  console.log('\n📁 Full report: reports/SECURITY_SUMMARY.md');

  // Exit with error if failed
  if (!summary.passed) {
    process.exit(1);
  }
}

generateSummary();
```

---

## 5. CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for secret scanning
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          npm ci
          pip install semgrep trufflehog
      
      - name: Run npm audit
        run: npm audit --json > reports/npm-audit.json || true
      
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --json-file-output=reports/snyk-report.json
      
      - name: Run Semgrep
        run: semgrep --config=auto --json . > reports/sast-report.json
      
      - name: Run TruffleHog
        run: trufflehog --json filesystem . > reports/secrets-report.json || true
      
      - name: Check licenses
        run: npx license-checker --json --out reports/licenses.json
      
      - name: Generate summary
        run: node scripts/generate-security-summary.js
      
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: reports/
      
      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const summary = fs.readFileSync('reports/SECURITY_SUMMARY.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: summary
            });
```

---

### Pre-commit Hook

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "🔒 Running security checks..."

# Quick secret scan
echo "Checking for secrets..."
trufflehog filesystem . --only-verified
if [ $? -ne 0 ]; then
  echo "❌ Secrets detected! Commit blocked."
  exit 1
fi

# Quick dependency check
echo "Checking dependencies..."
npm audit --audit-level=high
if [ $? -ne 0 ]; then
  echo "⚠️  High/Critical vulnerabilities found. Consider fixing before committing."
  read -p "Continue anyway? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

echo "✅ Security checks passed"
```

---

## 6. Reporting

### Dashboard (HTML)

```html
<!-- reports/security-dashboard.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Security Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .metric { display: inline-block; margin: 10px; padding: 20px; border-radius: 5px; }
    .critical { background: #ff4444; color: white; }
    .high { background: #ff8800; color: white; }
    .medium { background: #ffaa00; }
    .low { background: #88ff88; }
    .passed { background: #44ff44; }
  </style>
</head>
<body>
  <h1>🔒 Security Dashboard</h1>
  <div id="metrics"></div>
  <script>
    fetch('security-summary.json')
      .then(r => r.json())
      .then(data => {
        document.getElementById('metrics').innerHTML = `
          <div class="metric critical">
            <h2>${data.vulnerabilities.critical}</h2>
            <p>Critical</p>
          </div>
          <div class="metric high">
            <h2>${data.vulnerabilities.high}</h2>
            <p>High</p>
          </div>
          <div class="metric medium">
            <h2>${data.vulnerabilities.medium}</h2>
            <p>Medium</p>
          </div>
          <div class="metric low">
            <h2>${data.vulnerabilities.low}</h2>
            <p>Low</p>
          </div>
          <div class="metric ${data.passed ? 'passed' : 'critical'}">
            <h2>${data.passed ? '✅' : '❌'}</h2>
            <p>${data.passed ? 'Passed' : 'Failed'}</p>
          </div>
        `;
      });
  </script>
</body>
</html>
```

---

## 7. Best Practices

### DO ✅

1. **Scan on every commit** - Catch issues early
2. **Fix critical/high immediately** - Don't ignore
3. **Use multiple tools** - Different tools find different issues
4. **Scan dependencies regularly** - New vulnerabilities discovered daily
5. **Never commit secrets** - Use environment variables
6. **Keep dependencies updated** - Use Dependabot/Renovate
7. **Review licenses** - Avoid legal issues
8. **Automate everything** - CI/CD integration
9. **Monitor continuously** - Not just once
10. **Educate team** - Security is everyone's responsibility

### DON'T ❌

1. **Don't ignore warnings** - They become vulnerabilities
2. **Don't use outdated dependencies** - Update regularly
3. **Don't commit API keys** - Ever
4. **Don't skip scans** - "Just this once" becomes habit
5. **Don't use vulnerable packages** - Find alternatives
6. **Don't disable security checks** - To "save time"
7. **Don't trust user input** - Always validate
8. **Don't hardcode secrets** - Use secrets management
9. **Don't ignore license issues** - Legal problems are expensive
10. **Don't assume you're safe** - Always verify

---

## 🎯 Integration with Our System

### Phase 5: Security
- Run all security scans
- Fix critical/high vulnerabilities
- Remove any secrets
- Verify license compliance
- Generate security report

### Phase 6: Deployment
- Setup continuous security monitoring
- Configure automated dependency updates
- Enable security alerts
- Schedule regular scans

### Checkpoints
- ✅ Zero critical vulnerabilities
- ✅ Zero high vulnerabilities
- ✅ No secrets in code
- ✅ All licenses compliant
- ✅ Security report generated
- ✅ No security regressions

---

## 📚 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Snyk](https://snyk.io/)
- [Semgrep](https://semgrep.dev/)
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit)
- [TruffleHog](https://github.com/trufflesecurity/trufflehog)

---

**Status:** ✅ Production Ready  
**Last Updated:** 2025-11-17  
**Version:** 1.0

