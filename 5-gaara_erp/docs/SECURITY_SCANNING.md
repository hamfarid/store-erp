# Security Scanning Guide - Gaara ERP v12

**Last Updated**: 2025-11-29  
**Version**: 12.0.0

---

## Overview

Gaara ERP implements a comprehensive security scanning strategy using multiple tools:

| Tool | Purpose | Integration |
|------|---------|-------------|
| **Trivy** | Container, filesystem, IaC, secrets | GitHub Actions |
| **CodeQL** | SAST (Static Application Security Testing) | GitHub Actions |
| **Bandit** | Python security linting | GitHub Actions |
| **Safety/pip-audit** | Python dependency vulnerabilities | GitHub Actions |
| **npm audit** | Node.js dependency vulnerabilities | GitHub Actions |

---

## Trivy Security Scanner

### What Trivy Scans

Trivy is our primary security scanner, providing:

1. **Container Image Scanning**
   - OS packages (Alpine, Debian, etc.)
   - Application dependencies (Python, Node.js)
   - Embedded secrets

2. **Filesystem Scanning**
   - `requirements.txt` / `pyproject.toml`
   - `package.json` / `package-lock.json`
   - Application source code

3. **Infrastructure as Code (IaC)**
   - Dockerfile misconfigurations
   - docker-compose.yml issues
   - Kubernetes manifests
   - Terraform files (if present)

4. **Secret Detection**
   - API keys
   - Passwords
   - Private keys
   - Tokens

### GitHub Actions Workflows

#### 1. Main CI Pipeline (`ci.yml`)

```yaml
# Runs on every push/PR
- Trivy filesystem scan (Python & Node.js)
- Trivy secret scan
- Trivy container scan (after Docker build)
- SBOM generation (CycloneDX)
- Results uploaded to GitHub Security tab
```

#### 2. Dedicated Security Workflow (`trivy-security.yml`)

```yaml
# Runs daily at 6 AM UTC + on push/PR
- Full filesystem scan
- Comprehensive secret detection
- IaC configuration scan
- Container image scan
- SBOM in CycloneDX & SPDX formats
- Vulnerability reports as artifacts
```

### Running Locally

#### Installation

```bash
# macOS
brew install trivy

# Ubuntu/Debian
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# Docker
docker pull aquasec/trivy
```

#### Commands

```bash
# Scan filesystem (dependencies)
trivy fs --scanners vuln gaara_erp/

# Scan for secrets
trivy fs --scanners secret .

# Scan Docker image
docker build -t gaara-erp:local .
trivy image gaara-erp:local

# Scan IaC configurations
trivy config .

# Full scan with all scanners
trivy fs --scanners vuln,secret,misconfig .

# Generate SBOM
trivy image --format cyclonedx -o sbom.json gaara-erp:local

# Scan with specific severity
trivy image --severity HIGH,CRITICAL gaara-erp:local

# Scan ignoring unfixed vulnerabilities
trivy image --ignore-unfixed gaara-erp:local
```

### Severity Levels

| Severity | Description | SLA |
|----------|-------------|-----|
| **CRITICAL** | Exploitable remotely, high impact | Fix immediately |
| **HIGH** | Significant security risk | Fix within 7 days |
| **MEDIUM** | Moderate security risk | Fix within 30 days |
| **LOW** | Minor security concern | Fix as time permits |
| **UNKNOWN** | Unscored vulnerability | Assess manually |

### Managing False Positives

Create/edit `.trivyignore` in project root:

```
# Ignore specific CVE
CVE-2023-12345

# Ignore by package (PURL format)
pkg:pypi/example-package@1.0.0
pkg:npm/lodash

# Ignore with expiration (Trivy 0.45+)
CVE-2023-12345 exp:2024-12-31
```

### Integration with GitHub Security Tab

All Trivy findings are uploaded as SARIF to GitHub's Security tab:

1. Navigate to repository → **Security** → **Code scanning alerts**
2. Filter by tool: `trivy-backend`, `trivy-frontend`, `trivy-container`, `trivy-iac`
3. View, dismiss, or create issues for each finding

---

## SBOM (Software Bill of Materials)

### What is SBOM?

A Software Bill of Materials is a complete list of all components, libraries, and dependencies in the software.

### Generated Formats

| Format | Use Case | Standard |
|--------|----------|----------|
| **CycloneDX** | Vulnerability management | OWASP |
| **SPDX** | License compliance | Linux Foundation |

### Accessing SBOMs

1. Go to GitHub Actions run
2. Download from **Artifacts** section
3. Files: `sbom-cyclonedx.json`, `sbom-spdx.json`

### Using SBOMs

```bash
# Scan SBOM for vulnerabilities
trivy sbom sbom-cyclonedx.json

# Import into Dependency-Track
curl -X POST "https://dependency-track.example.com/api/v1/bom" \
  -H "X-Api-Key: $API_KEY" \
  -F "bom=@sbom-cyclonedx.json"
```

---

## CodeQL Analysis

CodeQL provides deep SAST scanning for Python and JavaScript:

```yaml
# .github/workflows/codeql.yml
- Runs on push to main/develop
- Weekly scheduled scan
- Security-extended query suite
```

---

## Pre-commit Hooks

Consider adding local security checks:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-ll', '-q']

  - repo: local
    hooks:
      - id: trivy-secrets
        name: Trivy Secret Scan
        entry: trivy fs --scanners secret --exit-code 1 .
        language: system
        pass_filenames: false

# Install hooks
pre-commit install
```

---

## Security Checklist

### Before Every Release

- [ ] Run Trivy scan on final Docker image
- [ ] Review all HIGH/CRITICAL findings
- [ ] Generate fresh SBOM
- [ ] Check GitHub Security tab for new alerts
- [ ] Update `.trivyignore` if needed
- [ ] Document any accepted risks

### Monthly Security Review

- [ ] Review scheduled scan results
- [ ] Update dependencies with known vulnerabilities
- [ ] Audit dismissed findings
- [ ] Review SBOM changes
- [ ] Update security documentation

---

## Resources

- [Trivy Documentation](https://trivy.dev)
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [CycloneDX Specification](https://cyclonedx.org)
- [SPDX Specification](https://spdx.dev)
- [OWASP Dependency-Track](https://dependencytrack.org)

---

**Last Reviewed**: 2025-11-29  
**Next Review**: 2025-12-29

