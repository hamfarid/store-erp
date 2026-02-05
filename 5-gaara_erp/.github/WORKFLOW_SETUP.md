# GitHub Workflow Setup Guide

This document explains the remaining setup needed to make all workflows fully functional.

## ✅ Fixed Issues

1. **dependabot.yml** - Removed unsupported `reviewers` property and fixed duplicate keys
2. **Environment names** - Updated to match GitHub's environment naming (e.g., `staging-env`, `production-env`)

## ⚠️ Remaining Setup (Required)

### 1. Create GitHub Environments

Navigate to your repository's **Settings → Environments** and create these three environments:

#### Development Environment
- **Name**: `development-env`
- **URL** (optional): `https://dev.gaaragroup.com`
- **Deployment branches**: All branches can deploy

#### Staging Environment
- **Name**: `staging-env`
- **URL** (optional): `https://staging.gaaragroup.com`
- **Deployment branches**: Only `develop`, `release/*` branches

#### Production Environment
- **Name**: `production-env`
- **URL** (optional): `https://gaaragroup.com`
- **Deployment branches**: Only `main` branch
- **Required reviewers** (recommended): Add team members
- **Deployment timeout**: 30 minutes

### 2. Add Repository Secrets

Navigate to **Settings → Secrets and variables → Actions** and add:

#### Deployment Secrets
```
STAGING_SSH_KEY          # SSH private key for staging server
STAGING_HOST            # Staging server hostname/IP
STAGING_USER            # SSH user for staging
STAGING_API_KEY         # API authentication token for staging
STAGING_DB_URL          # Database connection string for staging

PRODUCTION_SSH_KEY      # SSH private key for production server
PRODUCTION_HOST         # Production server hostname/IP
PRODUCTION_USER         # SSH user for production
PRODUCTION_API_KEY      # API authentication token for production
PRODUCTION_DB_URL       # Database connection string for production
```

#### Notification Secrets
```
SLACK_WEBHOOK_URL       # Slack webhook for deployment notifications
```

#### Build & Deployment
```
DOCKER_REGISTRY_URL     # Docker registry (e.g., docker.io, ghcr.io)
DOCKER_USERNAME         # Registry authentication username
DOCKER_PASSWORD         # Registry authentication token/password
```

### 3. Branch Protection Rules

Navigate to **Settings → Branches** and protect `main` and `develop`:

#### For `main` branch:
- ✅ Require pull request reviews before merging (2 reviewers recommended)
- ✅ Require status checks to pass (select all CI workflows)
- ✅ Require branches to be up to date
- ✅ Dismiss stale pull request approvals
- ✅ Require code owner reviews
- ✅ Restrict who can push to matching branches (admin only)

#### For `develop` branch:
- ✅ Require pull request reviews before merging (1 reviewer)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Dismiss stale pull request approvals

### 4. GitHub Actions Configuration

#### Enable Workflows
Go to **Actions** tab → verify all workflows are enabled:
- ✅ Build & Test (`ci.yml`)
- ✅ Deploy Staging (`deploy-staging.yml`)
- ✅ Deploy Production (`deploy.yml`)
- ✅ Hotfix (`hotfix.yml`)
- ✅ Release (`release.yml`)

#### Workflow Permissions
Navigate to **Settings → Actions → General**:
- ✅ Allow all actions and reusable workflows (or restrict to specific)
- ✅ Workflow permissions: Read and write permissions
- ✅ Allow GitHub Actions to create and approve pull requests

## 📋 Workflow Environment Variables

These are set in workflows but require corresponding GitHub Secrets or should be added as repository variables:

```yaml
# Environment URLs
STAGING_URL: https://staging.gaaragroup.com
PRODUCTION_URL: https://gaaragroup.com

# Version Management
SEMANTIC_RELEASE_VERSION: latest
NPM_REGISTRY: https://registry.npmjs.org

# Build Configuration
NODE_ENV: production
PYTHON_VERSION: 3.11
```

## 🔄 Testing the Workflows

After setup, test each workflow:

### Test CI Workflow
```bash
git checkout develop
git commit --allow-empty -m "test: workflow trigger"
git push origin develop
```
Visit Actions tab to verify build succeeds.

### Test Hotfix Workflow
Trigger manually:
```
GitHub UI → Actions → Hotfix → Run workflow
```

### Test Release Workflow
Push semantic commit to `develop`:
```bash
git checkout develop
git commit --allow-empty -m "feat: test feature"
git push origin develop
```

## 📚 Related Documentation

- [Git Workflow Guide](.github/instructions/git_workflow.instructions.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Conventional Commits](https://www.conventionalcommits.org/)

## ✨ Verification Checklist

- [ ] All 3 environments created in GitHub
- [ ] All required secrets added (14 total)
- [ ] Branch protection rules configured for `main` and `develop`
- [ ] Workflow permissions set to read+write
- [ ] CI workflow runs on every PR
- [ ] All workflows accessible in Actions tab
- [ ] Test workflows triggered successfully
- [ ] Slack notifications working (if configured)

---

**Status**: Setup guide v1.0 | Last Updated: 2026-02-05
