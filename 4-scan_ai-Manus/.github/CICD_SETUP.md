# CI/CD Setup Guide 🚀

## Overview

This repository includes a comprehensive CI/CD pipeline powered by GitHub Actions for automated testing, building, and deployment of the Gaara Scan AI system.

## 📋 Workflows

### 1. Main CI Pipeline (`ci.yml`)

**Triggers:** Push to `main`/`develop`, Pull Requests

**Jobs:**
- **Backend Testing**
  - Python 3.11 environment
  - PostgreSQL 15 + Redis services
  - Runs pytest with coverage reporting
  - Black code formatting check
  - Flake8 linting
  - Uploads coverage to Codecov

- **Frontend Testing**
  - Node.js 18 environment
  - ESLint code quality checks
  - Vitest unit tests
  - Production build verification

- **Security Scanning**
  - Trivy vulnerability scanner
  - Python Safety check for dependencies
  - SARIF reports to GitHub Security tab

- **Docker Build**
  - Builds backend and frontend images
  - Uses GitHub Actions cache for faster builds
  - Validates Docker configurations

- **Code Quality Analysis**
  - SonarCloud integration (optional)
  - Comprehensive code metrics

- **Deployment**
  - Automatic deployment on `main` branch pushes
  - Customize based on your infrastructure

### 2. Docker Publishing (`docker-publish.yml`)

**Triggers:** Push to `main`, version tags (`v*.*.*`)

**Features:**
- Builds and pushes to GitHub Container Registry (GHCR)
- Automatic tagging with:
  - Branch names
  - Semantic versions
  - Git SHA
- Multi-architecture support ready
- Layer caching for faster builds

**Published Images:**
```
ghcr.io/hamfarid/gaara-scan-system-backend:latest
ghcr.io/hamfarid/gaara-scan-system-frontend:latest
```

### 3. Database Migrations (`database-migrations.yml`)

**Triggers:** Changes to `backend/alembic/**` or `backend/src/models/**`

**Validations:**
- Migration script syntax check
- Test database upgrade
- Rollback testing
- Ensures migrations are reversible

### 4. Dependabot (`dependabot.yml`)

**Automated Updates:**
- Python dependencies (weekly)
- JavaScript dependencies (weekly)
- Docker base images (weekly)
- GitHub Actions versions (weekly)

## 🔧 Setup Instructions

### 1. Enable GitHub Actions

Actions are enabled by default. Visit:
```
https://github.com/hamfarid/gaara-Scan-system/actions
```

### 2. Configure Secrets

Go to **Settings → Secrets and variables → Actions** and add:

#### Required Secrets:
```bash
# For Codecov (optional)
CODECOV_TOKEN=<your-codecov-token>

# For SonarCloud (optional)
SONAR_TOKEN=<your-sonar-token>

# For deployment (customize based on your needs)
DEPLOY_SSH_KEY=<ssh-private-key>
DEPLOY_HOST=<your-server-ip>
DEPLOY_USER=<deployment-user>
```

#### Docker Registry (GHCR):
- Uses `GITHUB_TOKEN` (automatically provided)
- No additional setup required

### 3. Branch Protection Rules

Set up branch protection for `main`:

1. Go to **Settings → Branches → Branch protection rules**
2. Add rule for `main`:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass before merging
     - backend-test
     - frontend-test
     - docker-build
   - ✅ Require branches to be up to date
   - ✅ Include administrators

### 4. Environment Variables

Add repository variables (Settings → Secrets and variables → Actions → Variables):

```bash
# Database Configuration
DATABASE_URL=<production-db-url>
REDIS_HOST=<redis-host>

# Application Settings
SECRET_KEY=<your-secret-key>
JWT_SECRET_KEY=<your-jwt-secret>
FRONTEND_URL=<your-frontend-url>

# Optional: SonarCloud
SONAR_ORGANIZATION=hamfarid
SONAR_PROJECT_KEY=hamfarid_gaara-Scan-system
```

## 📊 Status Badges

Add to your README.md:

```markdown
![CI Status](https://github.com/hamfarid/gaara-Scan-system/workflows/CI%2FCD%20Pipeline/badge.svg)
![Docker](https://github.com/hamfarid/gaara-Scan-system/workflows/Docker%20Build%20and%20Publish/badge.svg)
[![codecov](https://codecov.io/gh/hamfarid/gaara-Scan-system/branch/main/graph/badge.svg)](https://codecov.io/gh/hamfarid/gaara-Scan-system)
```

## 🐳 Using Published Docker Images

Pull and run the latest images:

```bash
# Pull images
docker pull ghcr.io/hamfarid/gaara-scan-system-backend:latest
docker pull ghcr.io/hamfarid/gaara-scan-system-frontend:latest

# Run with docker-compose
docker compose up -d
```

### Authentication for Private Packages:

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

## 🔄 Manual Workflow Triggers

Trigger workflows manually:

```bash
# Using GitHub CLI
gh workflow run "CI/CD Pipeline"
gh workflow run "Docker Build and Publish"
gh workflow run "Database Migrations"

# Or via GitHub UI: Actions → Select workflow → Run workflow
```

## 📝 Local Testing

### Backend Tests:
```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v --cov=src
```

### Frontend Tests:
```bash
cd frontend
npm install
npm test
npm run build
```

### Docker Build:
```bash
docker compose build
docker compose up -d
```

## 🎯 Continuous Deployment

### Automatic Deployment (main branch)

When code is pushed to `main` and all tests pass, the deployment job runs automatically.

**Customize deployment in `.github/workflows/ci.yml`:**

```yaml
- name: Deploy to server
  run: |
    # Add your deployment commands
    # Examples:
    # - Deploy to AWS ECS
    # - Deploy to Kubernetes
    # - Deploy to DigitalOcean
    # - SSH to server and update
```

### Popular Deployment Options:

#### Option 1: Docker Swarm
```yaml
- name: Deploy to Docker Swarm
  run: |
    docker stack deploy -c docker-compose.yml gaara-scan
```

#### Option 2: Kubernetes
```yaml
- name: Deploy to Kubernetes
  run: |
    kubectl apply -f k8s/
    kubectl rollout restart deployment/backend
    kubectl rollout restart deployment/frontend
```

#### Option 3: SSH to Server
```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USER }}
    key: ${{ secrets.DEPLOY_SSH_KEY }}
    script: |
      cd /opt/gaara-scan-system
      git pull
      docker compose pull
      docker compose up -d
```

## 🔒 Security Best Practices

1. **Never commit secrets** - Use GitHub Secrets
2. **Review Dependabot PRs** - Update dependencies regularly
3. **Monitor Security Advisories** - Check GitHub Security tab
4. **Scan Docker images** - Trivy runs automatically
5. **Enable 2FA** - On your GitHub account

## 📈 Monitoring

### GitHub Actions Dashboard
- View workflow runs: `https://github.com/hamfarid/gaara-Scan-system/actions`
- Check job logs for failures
- Review security alerts

### Codecov (Optional)
- Coverage reports: `https://codecov.io/gh/hamfarid/gaara-Scan-system`

### SonarCloud (Optional)
- Code quality: `https://sonarcloud.io/dashboard?id=hamfarid_gaara-Scan-system`

## 🐛 Troubleshooting

### Tests Failing?
1. Check logs in Actions tab
2. Run tests locally
3. Ensure dependencies are up to date

### Docker Build Failed?
1. Check Dockerfile syntax
2. Verify base image availability
3. Review build context

### Deployment Issues?
1. Check secrets are configured
2. Verify server connectivity
3. Review deployment logs

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Semantic Versioning](https://semver.org/)

## 💡 Tips

- **Use caching** - Workflows use layer caching for faster builds
- **Parallel jobs** - Tests run in parallel for speed
- **Manual triggers** - Use `workflow_dispatch` for manual runs
- **Environment-specific secrets** - Use GitHub Environments for staging/prod

## 🔄 Backup System

Run backup script locally:

```bash
python create_backup.py
```

Creates timestamped ZIP archive excluding:
- `node_modules/`
- `__pycache__/`
- `.pytest_cache/`
- `.venv/`, `venv/`, `env/`
- `.git/`
- Build artifacts

**Output location:** `../gaara_scan_ai_backup_YYYYMMDD_HHMMSS.zip`

---

**Need help?** Open an issue or check workflow logs in the Actions tab.
