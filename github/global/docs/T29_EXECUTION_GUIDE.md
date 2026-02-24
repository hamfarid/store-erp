# T29: Deployment Automation - Execution Guide

**Task:** T29 - Deployment Automation  
**Effort:** 3-4 hours  
**Status:** ✅ Ready for Execution  
**Created:** 2025-11-08

---

## 📋 Overview

This guide provides step-by-step instructions for executing **T29: Deployment Automation**. All files have been created and are ready for testing and deployment.

---

## 📁 Files Created

### Docker Files (3 files)
```
✅ Dockerfile.backend              - Production-optimized backend image
✅ Dockerfile.frontend             - Production-optimized frontend image
✅ docker-compose.production.yml   - Production orchestration
```

### Configuration Files (1 file)
```
✅ .env.production.example         - Environment variables template
```

### Deployment Scripts (3 files)
```
✅ scripts/deploy-production.sh    - Main deployment script
✅ scripts/rollback.sh             - Rollback script
✅ scripts/health-check.sh         - Health check script
```

### CI/CD Workflow (1 file)
```
✅ .github/workflows/deploy-production.yml  - GitHub Actions deployment
```

### Documentation (1 file)
```
✅ docs/deployment/DEPLOYMENT_GUIDE.md      - Comprehensive deployment guide
```

**Total: 9 files created**

---

## 🚀 Execution Steps

### Phase 1: Local Testing (1-1.5 hours)

#### Step 1: Configure Environment

```bash
# Copy environment template
cp .env.production.example .env.production

# Edit with your values
nano .env.production
```

**Required variables:**
```bash
POSTGRES_PASSWORD=your-strong-password
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-min-32-chars
```

#### Step 2: Make Scripts Executable

```bash
chmod +x scripts/deploy-production.sh
chmod +x scripts/rollback.sh
chmod +x scripts/health-check.sh
```

#### Step 3: Build Docker Images

```bash
# Build backend image
docker build -f Dockerfile.backend -t store-backend:test .

# Build frontend image
docker build -f Dockerfile.frontend -t store-frontend:test .
```

**Expected output:**
```
✓ Backend image built successfully
✓ Frontend image built successfully
```

#### Step 4: Test Docker Compose

```bash
# Start services
docker-compose -f docker-compose.production.yml up -d

# Check status
docker-compose -f docker-compose.production.yml ps
```

**Expected output:**
```
NAME                    STATUS
store_postgres_prod     Up (healthy)
store_redis_prod        Up (healthy)
store_backend_prod      Up (healthy)
store_frontend_prod     Up (healthy)
store_nginx_prod        Up (healthy)
```

#### Step 5: Run Health Checks

```bash
./scripts/health-check.sh --verbose
```

**Expected output:**
```
✓ All health checks passed!
✓ PostgreSQL is accepting connections
✓ Redis is responding to PING
✓ Backend health endpoint is responding (HTTP 200)
✓ Frontend is responding (HTTP 200)
```

#### Step 6: Test Application

1. **Frontend:** http://localhost:80
2. **Backend:** http://localhost:5000/health
3. **API Docs:** http://localhost:5000/api/docs

#### Step 7: Test Rollback

```bash
# Create a test backup
mkdir -p backups/test_backup
docker-compose -f docker-compose.production.yml exec postgres pg_dump \
  -U store_user -d store_db > backups/test_backup/database_backup.sql

# Test rollback script
./scripts/rollback.sh backups/test_backup
```

**Expected output:**
```
✓ Rollback completed successfully!
✓ Database restored successfully
✓ Application restarted successfully
```

#### Step 8: Clean Up

```bash
# Stop services
docker-compose -f docker-compose.production.yml down

# Remove test volumes (optional)
docker volume prune
```

---

### Phase 2: CI/CD Setup (0.5-1 hour)

#### Step 1: Configure GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SERVER_HOST` | Production server IP/domain | `192.168.1.100` |
| `SERVER_USER` | SSH user for deployment | `deploy` |
| `SSH_PRIVATE_KEY` | SSH private key | `-----BEGIN RSA PRIVATE KEY-----...` |
| `DOMAIN` | Production domain | `yourdomain.com` |
| `VITE_API_URL` | Backend API URL | `https://api.yourdomain.com` |
| `SLACK_WEBHOOK` | Slack webhook (optional) | `https://hooks.slack.com/...` |

#### Step 2: Test Workflow Locally

```bash
# Install act (GitHub Actions local runner)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Test workflow
act -j build
```

#### Step 3: Commit and Push

```bash
git add .
git commit -m "feat(deployment): add production deployment automation (T29)"
git push origin main
```

#### Step 4: Monitor Workflow

1. Go to **Actions** tab in GitHub
2. Watch the deployment workflow
3. Verify all jobs pass:
   - ✅ Build
   - ✅ Security Scan
   - ✅ Deploy
   - ✅ Notify

---

### Phase 3: Production Deployment (1-1.5 hours)

#### Step 1: Prepare Production Server

```bash
# SSH to server
ssh user@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Create deployment directory
sudo mkdir -p /opt/store-erp
sudo chown $USER:$USER /opt/store-erp
```

#### Step 2: Copy Files to Server

```bash
# From local machine
scp docker-compose.production.yml user@server:/opt/store-erp/
scp .env.production user@server:/opt/store-erp/
scp -r scripts user@server:/opt/store-erp/
```

#### Step 3: Deploy to Production

```bash
# SSH to server
ssh user@your-server-ip

# Navigate to deployment directory
cd /opt/store-erp

# Run deployment
chmod +x scripts/deploy-production.sh
./scripts/deploy-production.sh
```

**Expected output:**
```
========================================
Checking Prerequisites
========================================
✓ Docker is installed
✓ Docker Compose is installed
✓ .env.production file exists

========================================
Building Docker Images
========================================
✓ Docker images built successfully

========================================
Deploying Application
========================================
✓ Application deployed successfully

========================================
Running Health Checks
========================================
✓ Backend is healthy
✓ Frontend is healthy
✓ Database is healthy

========================================
Deployment Summary
========================================
✓ Deployment completed successfully!
```

#### Step 4: Configure SSL/TLS

```bash
# Install Certbot
sudo apt-get install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Update Nginx configuration
sudo nano /opt/store-erp/nginx/nginx.conf
```

#### Step 5: Restart with SSL

```bash
docker-compose -f docker-compose.production.yml restart nginx
```

---

## ✅ Success Criteria

### Local Testing
- [ ] Backend Docker image builds successfully
- [ ] Frontend Docker image builds successfully
- [ ] All services start and pass health checks
- [ ] Application is accessible locally
- [ ] Rollback script works correctly

### CI/CD
- [ ] GitHub Actions workflow runs successfully
- [ ] Docker images are pushed to registry
- [ ] Security scans pass
- [ ] Deployment completes without errors

### Production
- [ ] Application is accessible via domain
- [ ] SSL/TLS is configured correctly
- [ ] All health checks pass
- [ ] Monitoring is active
- [ ] Backups are created automatically

---

## 📊 Timeline

| Phase | Task | Duration |
|-------|------|----------|
| **Phase 1** | Local Testing | 1-1.5h |
| **Phase 2** | CI/CD Setup | 0.5-1h |
| **Phase 3** | Production Deployment | 1-1.5h |
| **Total** | | **3-4 hours** |

---

## 🔧 Troubleshooting

### Issue: Docker build fails

**Solution:**
```bash
# Check Docker version
docker --version

# Clean Docker cache
docker system prune -a

# Rebuild with no cache
docker build --no-cache -f Dockerfile.backend -t store-backend:test .
```

### Issue: Health checks fail

**Solution:**
```bash
# Check logs
docker-compose -f docker-compose.production.yml logs backend

# Check environment variables
docker-compose -f docker-compose.production.yml exec backend env

# Restart service
docker-compose -f docker-compose.production.yml restart backend
```

### Issue: Database connection error

**Solution:**
```bash
# Check PostgreSQL
docker-compose -f docker-compose.production.yml exec postgres \
  pg_isready -U store_user -d store_db

# Check DATABASE_URL
docker-compose -f docker-compose.production.yml exec backend \
  env | grep DATABASE_URL
```

### Issue: Frontend not loading

**Solution:**
```bash
# Check Nginx logs
docker-compose -f docker-compose.production.yml logs frontend

# Verify build files
docker-compose -f docker-compose.production.yml exec frontend \
  ls -la /usr/share/nginx/html
```

---

## 📚 Additional Resources

### Documentation
- **Deployment Guide:** `docs/deployment/DEPLOYMENT_GUIDE.md`
- **Docker Documentation:** https://docs.docker.com/
- **Docker Compose:** https://docs.docker.com/compose/

### Scripts
- **Deploy:** `scripts/deploy-production.sh`
- **Rollback:** `scripts/rollback.sh`
- **Health Check:** `scripts/health-check.sh`

### Workflows
- **CI/CD:** `.github/workflows/deploy-production.yml`

---

## 🎯 Next Steps

After completing T29:

1. **T32: Documentation Finalization** (2-3 hours)
   - Complete all 21 required documentation files
   - Update README.md
   - Create troubleshooting guide

2. **T33: Final Testing & Verification** (2-3 hours)
   - Run full test suite
   - Performance validation
   - Security validation
   - Create final report

---

**Document Version:** 1.0.0  
**Created:** 2025-11-08  
**Status:** Ready for Execution

