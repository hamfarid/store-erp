# FILE: USAGE_GUIDE.md | PURPOSE: GitHub Actions workflows and scripts usage guide | OWNER: DevOps | RELATED: .github/workflows/, scripts/ | LAST-AUDITED: 2025-10-21

# Usage Guide — نظام إدارة المخزون العربي

**Version**: 1.0  
**Last Updated**: 2025-10-21  
**Audience**: Developers, DevOps Engineers

---

## 1. Overview

This guide documents how to use the GitHub Actions workflows and automation scripts in this repository.

**Key Components**:
- 4 GitHub Actions workflows (`.github/workflows/`)
- 3 automation scripts (`scripts/`)
- Environment validation
- Deployment procedures

---

## 2. GitHub Actions Workflows

### 2.1 Deployment Workflow (`deploy.yml`)

**Purpose**: Automated deployment pipeline with environment promotion (dev → staging → production)

**Trigger**:
- Push to `main` branch (auto-deploy to dev)
- Manual workflow dispatch (for staging/production)

**Environments**:
1. **Development** — Auto-deployed on every push to `main`
2. **Staging** — Manual approval required
3. **Production** — Manual approval required

**Usage**:

```bash
# Automatic deployment to dev
git push origin main

# Manual deployment to staging
# 1. Go to GitHub Actions tab
# 2. Select "Deploy" workflow
# 3. Click "Run workflow"
# 4. Select "staging" environment
# 5. Approve deployment

# Manual deployment to production
# Same as staging, but select "production" environment
```

**Workflow Steps**:
1. **Build** — Install dependencies, run tests, build frontend
2. **Deploy to Dev** — Deploy to development environment
3. **Health Check** — Verify deployment health
4. **Deploy to Staging** (manual approval)
5. **Deploy to Production** (manual approval)

**Required Secrets** (configure in GitHub Settings → Secrets):
- `DEPLOY_SSH_KEY` — SSH key for deployment server
- `DEPLOY_HOST` — Deployment server hostname
- `DEPLOY_USER` — Deployment server username
- `DEPLOY_PATH` — Deployment directory path
- `SECRET_KEY` — Flask secret key (from KMS/Vault)
- `JWT_SECRET_KEY` — JWT secret key (from KMS/Vault)
- `DATABASE_URL` — Production database URL (from KMS/Vault)

**Health Check**:
```bash
# After deployment, verify:
curl -f https://app.gaaragroup.com/api/health
```

---

### 2.2 Audit Workflow (`audit.yml`)

**Purpose**: Full system audit with compliance checks and PR comments

**Trigger**:
- Pull request to `main` branch
- Weekly schedule (every Monday at 2 AM UTC)
- Manual workflow dispatch

**Usage**:

```bash
# Automatic on PR
git checkout -b feature/my-feature
git push origin feature/my-feature
# Create PR → Audit runs automatically

# Manual audit
# 1. Go to GitHub Actions tab
# 2. Select "Audit Repository" workflow
# 3. Click "Run workflow"
```

**Audit Checks**:
1. **File Headers** — Verify required header line in all files
2. **Environment Files** — Detect `.env` files in repository
3. **Frontend Coverage** — Count pages, buttons, components
4. **Backend Coverage** — Count routes, models, blueprints
5. **Database Schema** — Count tables, columns, constraints
6. **Security Files** — Verify presence of security docs
7. **Documentation** — Check for missing docs

**Outputs**:
- `docs/Status_Report.md` — Markdown report
- `docs/Status_Report.json` — JSON report
- PR comment with summary

**Example PR Comment**:
```markdown
## 📊 Audit Report

**Overall Health**: 🟡 Yellow

| Category | Status | Score |
|----------|--------|-------|
| Security | 🔴 Red | 0.0/1.0 |
| Backend | 🟡 Yellow | 0.6/1.0 |
| Frontend | 🟡 Yellow | 0.5/1.0 |

**Critical Issues**:
- 18 critical security vulnerabilities
- 12/18 frontend pages incomplete
- 3 .env files found in repository

[View Full Report](../docs/Status_Report.md)
```

---

### 2.3 Issues Workflow (`issues.yml`)

**Purpose**: Auto-create GitHub Issues from `docs/Task_List.md`

**Trigger**:
- Manual workflow dispatch
- Push to `main` branch (if `docs/Task_List.md` changed)

**Usage**:

```bash
# Dry-run mode (preview without creating issues)
# 1. Go to GitHub Actions tab
# 2. Select "Create Issues from Task List" workflow
# 3. Click "Run workflow"
# 4. Check "Dry Run" option
# 5. Click "Run workflow"

# Create issues
# Same as above, but uncheck "Dry Run"
```

**Task List Format** (`docs/Task_List.md`):
```markdown
- [P0][Backend] Fix SQL injection vulnerabilities @backend-team (16h)
- [P1][Frontend] Implement Product Detail page @frontend-team (4h)
- [P2][DevOps] Set up Redis for caching @devops-team (8h)
```

**Generated Issues**:
- **Title**: Task description
- **Labels**: Priority (P0/P1/P2/P3), Area (Backend/Frontend/DevOps/etc.)
- **Assignee**: Extracted from `@username` (if exists)
- **Body**: Includes estimate, dependencies, acceptance criteria

**Duplicate Detection**:
- Checks for existing issues with same title
- Skips creation if duplicate found

---

### 2.4 Pages Workflow (`pages.yml`)

**Purpose**: Publish documentation to GitHub Pages

**Trigger**:
- Push to `main` branch (if `docs/` changed)
- Manual workflow dispatch

**Usage**:

```bash
# Automatic on docs update
git add docs/
git commit -m "docs: update documentation"
git push origin main
# Pages deploy automatically

# Manual deployment
# 1. Go to GitHub Actions tab
# 2. Select "Deploy Docs to GitHub Pages" workflow
# 3. Click "Run workflow"
```

**Published Docs**:
- URL: `https://<username>.github.io/<repo-name>/`
- Auto-generated index with navigation
- Organized by sections:
  - Security (Security.md, Threat_Model.md, CSP.md, Permissions_Model.md)
  - Architecture (TechStack.md, DB_Schema.md, Class_Registry.md)
  - API (API_Contracts.md, Routes_BE.md, Routes_FE.md)
  - Operations (Runbook.md, Remediation_Plan.md, Status_Report.md, Env.md)

**Setup** (one-time):
1. Go to GitHub Settings → Pages
2. Source: GitHub Actions
3. Save

---

## 3. Automation Scripts

### 3.1 Repository Audit Script (`scripts/audit_repo.py`)

**Purpose**: Scan repository for compliance violations and generate reports

**Usage**:

```bash
# Run audit
python scripts/audit_repo.py

# Output:
# - docs/Status_Report.md (Markdown)
# - docs/Status_Report.json (JSON)
```

**Checks**:
- File headers (required format)
- Environment files in repository
- Frontend pages/buttons count
- Backend routes/models count
- Database tables/columns count
- Security documentation presence

**Example Output**:
```json
{
  "timestamp": "2025-10-21T12:00:00Z",
  "overall_health": "yellow",
  "security_score": 0.0,
  "backend_score": 0.6,
  "frontend_score": 0.5,
  "critical_issues": [
    "18 critical security vulnerabilities",
    "12/18 frontend pages incomplete"
  ],
  "file_header_violations": [
    "backend/src/models/product.py",
    "frontend/src/pages/Dashboard.jsx"
  ],
  "env_files_found": [
    "backend/.env"
  ]
}
```

---

### 3.2 Issues from Task List Script (`scripts/issues_from_tasklist.py`)

**Purpose**: Convert `docs/Task_List.md` to GitHub Issues

**Usage**:

```bash
# Dry-run (preview without creating)
python scripts/issues_from_tasklist.py --dry-run

# Create issues
python scripts/issues_from_tasklist.py

# Specify custom task list file
python scripts/issues_from_tasklist.py --file custom_tasks.md
```

**Options**:
- `--dry-run` — Preview issues without creating
- `--file <path>` — Custom task list file (default: `docs/Task_List.md`)
- `--token <token>` — GitHub personal access token (or use `GITHUB_TOKEN` env var)

**Required Environment Variables**:
```bash
export GITHUB_TOKEN=ghp_your_personal_access_token
export GITHUB_REPOSITORY=username/repo-name
```

**Example Output**:
```
✅ Created issue #42: Fix SQL injection vulnerabilities
✅ Created issue #43: Implement Product Detail page
⚠️  Skipped (duplicate): Set up Redis for caching
```

---

### 3.3 Backup Script (`scripts/backup.sh`)

**Purpose**: Create clean backup archive excluding secrets and caches

**Usage**:

```bash
# Create backup
bash scripts/backup.sh

# Output: backups/backup_YYYYMMDD_HHMMSS.tar.gz
```

**Excluded**:
- `.env` files
- `.venv`, `node_modules`
- `__pycache__`, `.pytest_cache`, `.mypy_cache`
- `dist`, `build`, `.next`
- `*.log`, `*.db` files
- `encryption_keys`, `backups`, `tmp`

**Included**:
- All source code (`.py`, `.js`, `.jsx`)
- Configuration files (`.json`, `.yaml`, `.toml`)
- Documentation (`.md`)
- Scripts (`.sh`, `.ps1`)
- Templates

**Restore**:
```bash
tar -xzf backups/backup_20251021_120000.tar.gz -C /restore/path
```

---

## 4. Environment Validation

### 4.1 Validate Environment Script (`scripts/validate_env.py`)

**Purpose**: Validate `.env` file against schema

**Usage**:

```bash
# Validate backend/.env
cd backend
python ../scripts/validate_env.py

# Output:
# ✅ Environment validation passed
# OR
# ❌ Environment validation failed:
#   - SECRET_KEY must be at least 32 characters
#   - JWT_ACCESS_TOKEN_EXPIRES must be ≤900 (15 minutes)
```

**Checks**:
- Required variables present
- Secret key length (≥32 characters)
- JWT TTL limits (access ≤900s, refresh ≤604800s)
- Flask environment valid (development/production/testing)
- Production-specific checks (FLASK_DEBUG=False, PostgreSQL database)

---

## 5. Common Workflows

### 5.1 Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes
# ... edit files ...

# 3. Run local tests
cd backend
pytest
cd ../frontend
npm test

# 4. Validate environment
python scripts/validate_env.py

# 5. Commit changes
git add .
git commit -m "feat: add new feature"

# 6. Push and create PR
git push origin feature/my-feature
# Create PR on GitHub

# 7. Audit runs automatically on PR
# Review audit report in PR comments

# 8. Merge PR
# Auto-deploy to dev environment
```

---

### 5.2 Release Workflow

```bash
# 1. Ensure all tests pass
cd backend && pytest && cd ..
cd frontend && npm test && cd ..

# 2. Update version
# Edit package.json, __init__.py, etc.

# 3. Create release tag
git tag -a v1.6.0 -m "Release v1.6.0"
git push origin v1.6.0

# 4. Deploy to staging
# Go to GitHub Actions → Deploy → Run workflow → staging

# 5. Test staging
curl -f https://staging.gaaragroup.com/api/health

# 6. Deploy to production
# Go to GitHub Actions → Deploy → Run workflow → production

# 7. Verify production
curl -f https://app.gaaragroup.com/api/health
```

---

### 5.3 Hotfix Workflow

```bash
# 1. Create hotfix branch from main
git checkout -b hotfix/critical-bug main

# 2. Fix bug
# ... edit files ...

# 3. Test locally
pytest tests/test_critical_bug.py

# 4. Commit and push
git commit -m "fix: critical bug"
git push origin hotfix/critical-bug

# 5. Create PR with "hotfix" label
# Audit runs automatically

# 6. Merge PR (requires approval)
# Auto-deploy to dev

# 7. Deploy to production immediately
# Go to GitHub Actions → Deploy → Run workflow → production
```

---

## 6. Troubleshooting

### 6.1 Workflow Fails

**Symptom**: GitHub Actions workflow fails

**Diagnosis**:
1. Check workflow logs in GitHub Actions tab
2. Look for error messages in failed step
3. Verify secrets are configured correctly

**Common Issues**:
- **Missing secrets**: Configure in GitHub Settings → Secrets
- **SSH key invalid**: Regenerate and update `DEPLOY_SSH_KEY`
- **Tests fail**: Fix tests locally before pushing
- **Build fails**: Check dependencies in `requirements.txt` / `package.json`

---

### 6.2 Audit Script Fails

**Symptom**: `python scripts/audit_repo.py` fails

**Diagnosis**:
```bash
# Check Python version
python --version  # Must be 3.11+

# Check dependencies
pip list | grep -E "pathlib|json"

# Run with verbose output
python scripts/audit_repo.py --verbose
```

**Common Issues**:
- **File not found**: Run from repository root
- **Permission denied**: Check file permissions
- **Import error**: Install missing dependencies

---

### 6.3 Issues Script Fails

**Symptom**: `python scripts/issues_from_tasklist.py` fails

**Diagnosis**:
```bash
# Check GitHub token
echo $GITHUB_TOKEN

# Check repository
echo $GITHUB_REPOSITORY

# Test API access
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GITHUB_REPOSITORY/issues
```

**Common Issues**:
- **401 Unauthorized**: Invalid or expired GitHub token
- **404 Not Found**: Invalid repository name
- **403 Forbidden**: Token lacks required permissions (needs `repo` scope)

---

## 7. Best Practices

### 7.1 Workflow Best Practices

1. **Always run audit before merging PR**
2. **Test in staging before production**
3. **Use dry-run mode for issues script**
4. **Review deployment logs after each deploy**
5. **Keep secrets in GitHub Secrets, not code**

---

### 7.2 Script Best Practices

1. **Run audit weekly** (automated via workflow)
2. **Backup before major changes**
3. **Validate environment after updates**
4. **Use version control for task lists**
5. **Document custom workflows**

---

## 8. References

- GitHub Actions Docs: https://docs.github.com/en/actions
- GitHub Pages Docs: https://docs.github.com/en/pages
- Deployment Guide: `/docs/Runbook.md`
- Environment Variables: `/docs/Env.md`
- Security Procedures: `/docs/Security.md`

