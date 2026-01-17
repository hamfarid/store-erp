# Dependency Management Guide

**Version:** 2.0  
**Last Updated:** 2025-12-13  
**Maintainer:** DevOps Team

---

## Overview

This guide provides comprehensive instructions for managing dependencies in Store ERP, including updating, auditing, and maintaining both Python and Node.js packages.

---

## Table of Contents

1. [Current Dependencies](#current-dependencies)
2. [Update Strategy](#update-strategy)
3. [Automated Updates](#automated-updates)
4. [Security Audits](#security-audits)
5. [Version Pinning](#version-pinning)
6. [Testing After Updates](#testing-after-updates)
7. [Rollback Procedures](#rollback-procedures)
8. [Best Practices](#best-practices)

---

## Current Dependencies

### Backend (Python 3.11)

**Total Packages:** 99

**Core Dependencies:**
```
Flask==3.0.3
Flask-CORS==4.0.1
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.7
Flask-JWT-Extended==4.6.0
Flask-Login==0.6.3
SQLAlchemy==2.0.23
bcrypt==4.1.2
PyJWT==2.8.0
cryptography==46.0.3
pyotp==2.9.0
qrcode==7.4.2
pytest==8.0.0
```

**File:** `backend/requirements.txt`

### Frontend (Node.js 22)

**Total Packages:** 50+ dependencies

**Core Dependencies:**
```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "react-router-dom": "^7.1.3",
  "axios": "^1.7.9",
  "vite": "^6.0.7",
  "@radix-ui/*": "latest",
  "tailwindcss": "^4.1.7"
}
```

**File:** `frontend/package.json`

---

## Update Strategy

### 1. Scheduled Updates

**Frequency:**
- **Security Updates:** Immediately (within 24 hours)
- **Minor Updates:** Monthly (first week of month)
- **Major Updates:** Quarterly (after thorough testing)

**Schedule:**
```
Week 1 of Month:
  - Monday: Check for updates
  - Tuesday: Review changelogs
  - Wednesday: Update dev environment
  - Thursday: Run tests
  - Friday: Deploy to staging

Week 2 of Month:
  - Monday: Monitor staging
  - Tuesday-Thursday: Fix issues
  - Friday: Deploy to production (if stable)
```

### 2. Update Process

#### Step 1: Backup
```bash
# Create backup before any updates
./scripts/update_dependencies.sh
# This automatically creates backup in .backups/
```

#### Step 2: Check for Updates
```bash
# Backend
cd backend
pip list --outdated

# Frontend
cd frontend
pnpm outdated
```

#### Step 3: Review Changelogs
- Check GitHub releases for breaking changes
- Review migration guides
- Check compatibility matrix

#### Step 4: Update
```bash
# Backend (selective update)
pip install --upgrade package_name

# Frontend (selective update)
pnpm update package_name

# Or use automated script
./scripts/update_dependencies.sh
```

#### Step 5: Test
```bash
# Run all tests
cd backend
pytest --cov

# Test frontend build
cd frontend
pnpm build
```

#### Step 6: Commit
```bash
git add requirements.txt package.json pnpm-lock.yaml
git commit -m "chore: update dependencies (YYYY-MM-DD)"
git push
```

---

## Automated Updates

### Using Dependabot (GitHub)

**Configuration:** `.github/dependabot.yml`

```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    reviewers:
      - "hamfarid"
    labels:
      - "dependencies"
      - "python"
    
  # JavaScript dependencies
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    reviewers:
      - "hamfarid"
    labels:
      - "dependencies"
      - "javascript"
    versioning-strategy: increase
```

### Using Renovate Bot (Alternative)

**Configuration:** `renovate.json`

```json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["breaking-change"]
    }
  ],
  "schedule": ["before 10am on monday"],
  "timezone": "Asia/Riyadh"
}
```

### Manual Automated Script

**Already Created:** `scripts/update_dependencies.sh`

**Usage:**
```bash
# Run update script
./scripts/update_dependencies.sh

# Review changes
git diff requirements.txt package.json

# Test
pytest && pnpm build

# Commit if successful
git add -A
git commit -m "chore: automated dependency update"
git push
```

---

## Security Audits

### Python Security Audit

**Tool:** pip-audit

**Installation:**
```bash
pip install pip-audit
```

**Usage:**
```bash
cd backend
pip-audit

# Fix vulnerabilities
pip-audit --fix

# Generate report
pip-audit --format json > security-audit.json
```

**Automated Check:**
```bash
# Add to CI/CD pipeline
pip-audit --require-hashes --strict
```

### Node.js Security Audit

**Tool:** pnpm audit

**Usage:**
```bash
cd frontend
pnpm audit

# Fix vulnerabilities
pnpm audit --fix

# Generate report
pnpm audit --json > security-audit.json
```

**Automated Check:**
```bash
# Add to CI/CD pipeline
pnpm audit --audit-level moderate
```

### GitHub Security Alerts

**Enable:**
1. Go to repository settings
2. Security & analysis
3. Enable Dependabot alerts
4. Enable Dependabot security updates

---

## Version Pinning

### Python Version Pinning

**Strategy:** Pin exact versions for production

**requirements.txt:**
```
# Exact versions (production)
Flask==3.0.3
SQLAlchemy==2.0.23

# Compatible versions (development)
# Flask>=3.0,<4.0
# SQLAlchemy>=2.0,<3.0
```

**Best Practice:**
- Use exact versions (`==`) in production
- Use compatible versions (`>=`, `<`) in development
- Use `requirements-dev.txt` for development dependencies

### Node.js Version Pinning

**Strategy:** Use caret (`^`) for minor updates

**package.json:**
```json
{
  "dependencies": {
    "react": "^18.3.1",      // Allow 18.x.x
    "axios": "~1.7.9"        // Allow 1.7.x only
  }
}
```

**Lock Files:**
- **Python:** Not standard (consider `pip-tools`)
- **Node.js:** `pnpm-lock.yaml` (automatically managed)

**Best Practice:**
- Always commit lock files
- Use `pnpm install --frozen-lockfile` in CI/CD

---

## Testing After Updates

### Automated Testing

**Backend:**
```bash
cd backend

# Run all tests
pytest --cov --cov-report=html

# Run specific test suites
pytest tests/test_logger.py -v
pytest tests/integration/ -v

# Check coverage
coverage report
```

**Frontend:**
```bash
cd frontend

# Build test
pnpm build

# Unit tests (if configured)
pnpm test

# E2E tests (if configured)
pnpm test:e2e
```

### Manual Testing Checklist

After updating dependencies, manually test:

- [ ] Login/Logout
- [ ] Dashboard loads
- [ ] Create product
- [ ] Create sale (POS)
- [ ] Create purchase
- [ ] Generate report
- [ ] User permissions
- [ ] 2FA functionality
- [ ] API endpoints
- [ ] Database operations

### Integration Testing

```bash
# Run integration tests
cd backend
pytest tests/integration/test_frontend_backend.py -v

# Test with real database
pytest --db=postgresql
```

---

## Rollback Procedures

### Quick Rollback

**If update fails:**

```bash
# Restore from backup (created by update script)
BACKUP_DIR=".backups/dependencies-YYYYMMDD-HHMMSS"

# Restore Python
cp $BACKUP_DIR/requirements.txt.bak backend/requirements.txt
cd backend
pip install -r requirements.txt

# Restore Node.js
cp $BACKUP_DIR/package.json.bak frontend/package.json
cp $BACKUP_DIR/pnpm-lock.yaml.bak frontend/pnpm-lock.yaml
cd frontend
pnpm install --frozen-lockfile
```

### Git Rollback

```bash
# Revert last commit
git revert HEAD

# Or reset to previous commit
git reset --hard HEAD~1

# Reinstall dependencies
cd backend && pip install -r requirements.txt
cd frontend && pnpm install
```

### Docker Rollback (if using Docker)

```bash
# Use previous image
docker pull store-erp:previous-version
docker-compose up -d
```

---

## Best Practices

### 1. Always Backup First

**Before any update:**
```bash
./scripts/update_dependencies.sh
# This creates automatic backup
```

### 2. Update One at a Time

**Don't update all at once:**
```bash
# Good: Update one package
pip install --upgrade Flask

# Bad: Update everything
# pip install --upgrade -r requirements.txt
```

### 3. Read Changelogs

**Before updating:**
- Check GitHub releases
- Read migration guides
- Check for breaking changes

### 4. Test Thoroughly

**After updating:**
- Run automated tests
- Manual testing
- Check logs for errors

### 5. Update Development First

**Environment order:**
1. Local development
2. Staging environment
3. Production environment

### 6. Use Lock Files

**Always commit:**
- `pnpm-lock.yaml` (Node.js)
- Consider `requirements.lock` (Python with pip-tools)

### 7. Monitor After Deployment

**After updating production:**
- Monitor error logs
- Check performance metrics
- Watch for user reports

### 8. Document Changes

**In commit message:**
```bash
git commit -m "chore: update Flask 3.0.2 -> 3.0.3

- Security fix for CVE-2024-XXXXX
- Improved performance
- No breaking changes

Tested:
- All unit tests pass
- Integration tests pass
- Manual testing complete"
```

---

## Dependency Management Tools

### Python Tools

#### pip-tools
```bash
# Install
pip install pip-tools

# Generate requirements.txt from requirements.in
pip-compile requirements.in

# Sync environment
pip-sync requirements.txt
```

#### Poetry (Alternative)
```bash
# Install
pip install poetry

# Initialize
poetry init

# Add dependency
poetry add flask

# Update
poetry update
```

### Node.js Tools

#### pnpm (Current)
```bash
# Update pnpm itself
pnpm add -g pnpm

# Update all dependencies
pnpm update

# Update specific package
pnpm update react

# Interactive update
pnpm update --interactive
```

#### npm-check-updates
```bash
# Install
pnpm add -g npm-check-updates

# Check for updates
ncu

# Update package.json
ncu -u

# Install updates
pnpm install
```

---

## CI/CD Integration

### GitHub Actions

**Workflow:** `.github/workflows/dependency-check.yml`

```yaml
name: Dependency Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  check-dependencies:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '22'
      
      - name: Check Python dependencies
        run: |
          cd backend
          pip install pip-audit
          pip-audit
      
      - name: Check Node.js dependencies
        run: |
          cd frontend
          corepack enable
          pnpm install
          pnpm audit
      
      - name: Create issue if vulnerabilities found
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Security vulnerabilities found in dependencies',
              body: 'Automated dependency check found vulnerabilities. Please review and update.',
              labels: ['security', 'dependencies']
            })
```

---

## Monitoring & Alerts

### Set Up Alerts

**GitHub:**
- Enable Dependabot alerts
- Enable security advisories
- Set up email notifications

**External Services:**
- Snyk (https://snyk.io/)
- WhiteSource (https://www.whitesourcesoftware.com/)
- Sonatype (https://www.sonatype.com/)

### Dashboard

**Create monitoring dashboard:**
- Number of outdated packages
- Security vulnerabilities
- Last update date
- Test coverage after updates

---

## Troubleshooting

### Common Issues

#### Issue 1: Dependency Conflicts

**Symptom:** Package A requires version X, Package B requires version Y

**Solution:**
```bash
# Check dependency tree
pip show package_name
pnpm why package_name

# Try updating conflicting packages together
pip install --upgrade package_a package_b
```

#### Issue 2: Breaking Changes

**Symptom:** Tests fail after update

**Solution:**
1. Read migration guide
2. Update code to match new API
3. Or rollback and wait for stable release

#### Issue 3: Lock File Conflicts

**Symptom:** Git merge conflicts in lock files

**Solution:**
```bash
# Regenerate lock file
cd frontend
rm pnpm-lock.yaml
pnpm install
```

---

## Recommended Update Schedule

### Weekly
- [ ] Check security alerts
- [ ] Review Dependabot PRs
- [ ] Update critical security patches

### Monthly
- [ ] Check for outdated packages
- [ ] Review changelogs
- [ ] Update minor versions
- [ ] Run full test suite

### Quarterly
- [ ] Review major version updates
- [ ] Plan migration for breaking changes
- [ ] Update documentation
- [ ] Audit all dependencies

### Yearly
- [ ] Review all dependencies
- [ ] Remove unused packages
- [ ] Update Node.js/Python versions
- [ ] Refactor deprecated code

---

## Resources

### Documentation
- **Python:** https://pip.pypa.io/
- **pnpm:** https://pnpm.io/
- **Dependabot:** https://docs.github.com/en/code-security/dependabot

### Tools
- **pip-audit:** https://pypi.org/project/pip-audit/
- **npm-check-updates:** https://www.npmjs.com/package/npm-check-updates
- **Snyk:** https://snyk.io/

### Security
- **CVE Database:** https://cve.mitre.org/
- **GitHub Advisory:** https://github.com/advisories
- **Python Security:** https://pyup.io/

---

## Conclusion

Proper dependency management is crucial for:
- **Security:** Patch vulnerabilities quickly
- **Stability:** Avoid breaking changes
- **Performance:** Benefit from improvements
- **Maintainability:** Keep codebase modern

**Follow this guide to ensure Store ERP dependencies are always up-to-date and secure!**

---

**Version:** 2.0  
**Last Updated:** 2025-12-13  
**Next Review:** 2025-01-13
