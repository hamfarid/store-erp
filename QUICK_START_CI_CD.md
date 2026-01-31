# Quick Start Guide - CI/CD & Monitoring

## 🚀 5-Minute Setup

### Step 1: Verify Workflows are Running
1. Go to [GitHub Actions](https://github.com/hamfarid/store-erp/actions)
2. You should see:
   - ✅ `CI/CD Pipeline` workflow
   - ✅ `Automated Backups` workflow
   - ✅ `Setup & Monitoring` workflow

### Step 2: Configure Secrets (5 minutes)
```
Settings → Secrets and variables → Actions → New repository secret
```

**Minimum secrets needed:**
```
PROD_DATABASE_URL=postgresql://user:password@localhost:5432/store
PROD_SECRET_KEY=<random-32-char-string>
PROD_JWT_SECRET=<random-32-char-string>
```

**Generate random secrets:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Test the Setup
```bash
# Create a test PR to trigger CI
git checkout -b test/ci-setup
git commit --allow-empty -m "Test CI pipeline"
git push origin test/ci-setup
# Open PR on GitHub
```

Watch the workflow run in the Actions tab!

---

## 📊 Monitoring Dashboard

### Quick Access Links
```
Local Monitoring (when deployed):
- Prometheus:   http://localhost:9090
- Grafana:      http://localhost:3000
- AlertManager: http://localhost:9093
```

### Login Credentials
```
Grafana:
  Username: admin
  Password: admin (change after first login!)
```

---

## 💾 Backup Management

### Automatic Backups
- **When**: Daily at 2:00 AM UTC
- **Where**: GitHub Actions Artifacts (30-day retention)
- **Manual Trigger**: Go to Actions → Automated Backups → Run workflow

### Create Manual Backup
```bash
cd project_root
python create_backup.py --backup-dir backups --manifest
# Creates: backups/backup_YYYYMMDD_HHMMSS.zip
```

---

## 🔍 Checking Workflow Status

### Dashboard View
```
https://github.com/hamfarid/store-erp/actions
```

### Test Results
When a workflow runs, you'll see:
- ✅ Backend Tests: Python tests, linting, coverage
- ✅ Frontend Tests: Node.js tests, build verification  
- ✅ Security: Vulnerability scanning
- ✅ Docker: Image build & push to registry

### Reading Logs
1. Click on a workflow run
2. Click the job name (e.g., "Backend Tests")
3. Expand any failed step to see error details

---

## 📝 Common Tasks

### Push Code Changes
```bash
git add .
git commit -m "Your message"
git push origin your-branch
# Creates a PR → Triggers CI tests
```

### Deploy to Production
```bash
# 1. Create release tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. Workflow automatically:
#    - Runs all tests
#    - Builds Docker images
#    - Creates backup
#    - Uploads to releases

# 3. Follow DEPLOYMENT_CHECKLIST.md
```

### Monitor Errors
```
Go to: Actions → [Workflow] → [Job] → [Failed Step]
Read error message
Fix locally
Push new commit (re-runs tests)
```

### Rollback Deployment
```bash
# If deployment fails:
git reset --hard HEAD~1  # Undo last commit
git push origin -f main  # Force push (if needed)

# OR use previous Docker image tag
docker pull previous-tag
docker compose up
```

---

## 🔐 Secrets Quick Reference

### Where to Find Secret Names
See: `PRODUCTION_SECRETS_GUIDE.md`

### Update a Secret
1. Settings → Secrets and variables → Actions
2. Find the secret
3. Click "Update secret"
4. Enter new value
5. Click "Update secret"

### Common Secret Updates
```
After setting secret → commit code → workflow uses it
No restart needed! GitHub Actions automatically uses new values
```

---

## 🚨 Troubleshooting

### Workflow Failed?
1. Click on the failed workflow run
2. Click the failed job
3. Read the error message
4. Check the logs for details
5. Fix locally and push new commit

### Test Failures
```bash
# Run tests locally first:
cd backend && python -m pytest -v
cd frontend && npm test
```

### Docker Build Failed
```bash
# Check Dockerfile syntax
docker build -f backend/Dockerfile -t test:latest backend/
```

### Backup Failed
```bash
# Test backup locally:
python create_backup.py --backup-dir test
# Check disk space: df -h
```

### Secret Not Found
```
- Check spelling (case-sensitive!)
- Verify it exists in Settings → Secrets
- Ensure correct repository (not org-level)
- Workflow needs 'contents: read' permission
```

---

## 📞 Quick Help

### Check Current Status
```bash
git status              # Local changes
git log --oneline -5    # Recent commits
git branch -v           # Current branch
```

### Review Changes
```bash
git diff                # Unstaged changes
git diff --cached       # Staged changes
git show HEAD           # Latest commit
```

### Revert Changes
```bash
git checkout .          # Discard all changes
git reset HEAD~1        # Undo last commit (keep changes)
git reset --hard HEAD~1 # Undo and discard changes
```

---

## 📚 More Information

For detailed documentation, see:
- `CI_CD_SETUP_SUMMARY.md` - Complete overview
- `DEPLOYMENT_CHECKLIST.md` - Pre/post deployment
- `PRODUCTION_SECRETS_GUIDE.md` - Secrets management
- `MONITORING_SETUP.md` - Monitoring setup
- `create_backup.py` - Backup script documentation

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Workflows visible in Actions tab
- [ ] Secrets configured
- [ ] Test PR triggers CI
- [ ] Backup runs without errors
- [ ] Monitoring dashboard loads
- [ ] Team has access to documentation

---

**Still need help?** Check the documentation files or review workflow logs in GitHub Actions!
