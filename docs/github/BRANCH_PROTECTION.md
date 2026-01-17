# Branch Protection Rules

This document describes the recommended branch protection rules for the Store ERP repository.

## Overview

Branch protection rules ensure code quality and prevent accidental changes to critical branches.

---

## Quick Start

### Automated Configuration (Recommended)

We provide scripts to automatically configure branch protection:

**PowerShell (Windows):**
```powershell
# Set your GitHub token
$env:GITHUB_TOKEN = "your_token_here"

# Run the script
.\scripts\configure_branch_protection.ps1
```

**Bash (Linux/Mac):**
```bash
# Set your GitHub token
export GITHUB_TOKEN="your_token_here"

# Run the script
chmod +x scripts/configure_branch_protection.sh
./scripts/configure_branch_protection.sh
```

**What the scripts do:**
- ✅ Configure main branch protection with strict rules
- ✅ Configure development branch protection (if exists)
- ✅ Set required status checks
- ✅ Set PR review requirements
- ✅ Prevent force pushes and deletions
- ✅ Require conversation resolution

---

## Main Branch Protection

### Branch: `main`

#### Required Status Checks

**Must pass before merging:**

1. **backend-tests** (`.github/workflows/backend-tests.yml`)
   - ✅ Linting (black, isort, flake8)
   - ✅ Type checking (mypy)
   - ✅ Security scan (bandit)
   - ✅ Unit tests (all must pass)
   - ✅ Integration tests (all must pass)
   - ✅ API drift tests (all must pass)
   - ✅ Enhanced validation tests (all must pass)
   - ✅ Performance tests (all must pass)
   - ✅ Coverage threshold (≥80%)
   - ✅ OpenAPI spec validation

2. **pr-checks** (`.github/workflows/pr-checks.yml`)
   - ✅ Code formatting
   - ✅ Import sorting
   - ✅ Linting
   - ✅ Security scan
   - ✅ All tests
   - ✅ Coverage check

3. **load-testing** (`.github/workflows/load-testing.yml`) - Optional
   - ⚠️ Load test (failure rate < 5%)

4. **dast_zap** (`.github/workflows/dast_zap.yml`) - Optional
   - ⚠️ OWASP ZAP baseline scan

#### Pull Request Requirements

- ✅ **Require pull request reviews before merging**
  - Required approving reviews: **1**
  - Dismiss stale pull request approvals when new commits are pushed: **Yes**
  - Require review from Code Owners: **No** (optional)

- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date before merging: **Yes**
  - Status checks that are required:
    - `backend-tests / test`
    - `pr-quality-gate / pr-quality-gate`

- ✅ **Require conversation resolution before merging**
  - All conversations must be resolved: **Yes**

- ✅ **Require signed commits** - Optional
  - Require signed commits: **No** (can be enabled for higher security)

- ✅ **Require linear history**
  - Require linear history: **No** (allows merge commits)

- ✅ **Include administrators**
  - Enforce all configured restrictions for administrators: **Yes**

#### Additional Settings

- ✅ **Allow force pushes**
  - Allow force pushes: **No**

- ✅ **Allow deletions**
  - Allow deletions: **No**

---

## Development Branch Protection

### Branch: `develop` (if used)

#### Required Status Checks

**Must pass before merging:**

1. **backend-tests**
   - ✅ All tests must pass
   - ✅ Coverage ≥70% (lower threshold for development)

2. **pr-checks**
   - ✅ Code formatting
   - ✅ Linting

#### Pull Request Requirements

- ✅ **Require pull request reviews before merging**
  - Required approving reviews: **1**

- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date before merging: **No** (more flexible)

---

## Feature Branch Protection

### Branch Pattern: `feature/*`

#### Recommendations

- ⚠️ No strict protection rules
- ✅ Developers can force push to their own feature branches
- ✅ Developers can delete their own feature branches after merge

---

## Release Branch Protection

### Branch Pattern: `release/*`

#### Required Status Checks

**Must pass before merging:**

1. **backend-tests** (all checks)
2. **load-testing** (required for releases)
3. **dast_zap** (required for releases)
4. **lighthouse_ci** (required for releases)

#### Pull Request Requirements

- ✅ **Require pull request reviews before merging**
  - Required approving reviews: **2** (higher for releases)
  - Require review from Code Owners: **Yes**

- ✅ **Require status checks to pass before merging**
  - All status checks must pass

---

## Hotfix Branch Protection

### Branch Pattern: `hotfix/*`

#### Required Status Checks

**Must pass before merging:**

1. **backend-tests** (critical tests only)
2. **pr-checks**

#### Pull Request Requirements

- ✅ **Require pull request reviews before merging**
  - Required approving reviews: **1** (can be expedited)

---

## How to Configure

### Via GitHub Web UI

1. Go to **Settings** → **Branches**
2. Click **Add rule** or edit existing rule
3. Enter branch name pattern (e.g., `main`)
4. Configure protection settings as described above
5. Click **Create** or **Save changes**

### Via GitHub API

```bash
# Example: Protect main branch
curl -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/hamfarid/store/branches/main/protection \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": [
        "backend-tests / test",
        "pr-quality-gate / pr-quality-gate"
      ]
    },
    "enforce_admins": true,
    "required_pull_request_reviews": {
      "dismissal_restrictions": {},
      "dismiss_stale_reviews": true,
      "require_code_owner_reviews": false,
      "required_approving_review_count": 1
    },
    "restrictions": null,
    "allow_force_pushes": false,
    "allow_deletions": false,
    "required_conversation_resolution": true
  }'
```

### Via GitHub CLI

```bash
# Install GitHub CLI
# https://cli.github.com/

# Protect main branch
gh api repos/hamfarid/store/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=backend-tests \
  --field required_status_checks[contexts][]=pr-quality-gate \
  --field enforce_admins=true \
  --field required_pull_request_reviews[required_approving_review_count]=1 \
  --field required_pull_request_reviews[dismiss_stale_reviews]=true \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field required_conversation_resolution=true
```

---

## Workflow

### For Developers

1. **Create feature branch** from `main`
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/my-feature
   ```

2. **Make changes and commit**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. **Push to remote**
   ```bash
   git push origin feature/my-feature
   ```

4. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Select `main` as base branch
   - Select `feature/my-feature` as compare branch
   - Fill in PR template
   - Click "Create Pull Request"

5. **Wait for CI/CD checks**
   - All required checks must pass
   - Fix any failures
   - Push new commits to update PR

6. **Request review**
   - Request review from team member
   - Address review comments
   - Resolve all conversations

7. **Merge**
   - Once approved and all checks pass
   - Click "Merge Pull Request"
   - Delete feature branch

---

## Status Check Details

### backend-tests

**What it checks:**
- Code formatting (black, isort)
- Linting (flake8)
- Type checking (mypy)
- Security (bandit, safety)
- Unit tests (109+ tests)
- Integration tests
- API drift tests
- Coverage (≥80%)
- OpenAPI spec validation

**How to fix failures:**
```bash
# Format code
black backend
isort backend

# Run tests locally
cd backend
pytest tests/ -v --cov=src

# Check coverage
python scripts/generate_coverage_report.py
```

### pr-checks

**What it checks:**
- All quality gates
- Comprehensive test suite
- Code complexity
- Dead code detection

**How to fix failures:**
- Follow error messages in workflow logs
- Run checks locally before pushing
- Use pre-commit hooks (recommended)

---

## Pre-commit Hooks (Recommended)

Install pre-commit hooks to catch issues before pushing:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

---

## Troubleshooting

### "Required status check is failing"

1. Check workflow logs in GitHub Actions
2. Run tests locally to reproduce
3. Fix the issue
4. Push new commit to update PR

### "Branch is out of date"

1. Update your branch:
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/my-feature
   git merge main
   git push origin feature/my-feature
   ```

### "Coverage below threshold"

1. Add tests for uncovered code
2. Run coverage report locally:
   ```bash
   cd backend
   python scripts/generate_coverage_report.py
   open htmlcov/index.html
   ```
3. Identify uncovered lines
4. Write tests
5. Push new commit

---

**Last Updated:** 2025-11-06  
**Next Review:** 2025-12-01

