# Store ERP - Production Deployment Guide

**Version:** 1.0.0  
**Last Updated:** 2025-11-08  
**Status:** Production Ready

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Architecture](#architecture)
4. [Deployment Methods](#deployment-methods)
5. [Configuration](#configuration)
6. [Deployment Steps](#deployment-steps)
7. [Post-Deployment](#post-deployment)
8. [Monitoring](#monitoring)
9. [Backup & Recovery](#backup--recovery)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This guide provides comprehensive instructions for deploying the Store ERP system to production. The deployment uses Docker containers orchestrated with Docker Compose for a reliable, scalable, and maintainable production environment.

### Key Features

- ✅ **Multi-stage Docker builds** for optimized images
- ✅ **Health checks** for all services
- ✅ **Resource limits** to prevent resource exhaustion
- ✅ **Automated backups** before deployment
- ✅ **Rollback capability** for failed deployments
- ✅ **CI/CD integration** with GitHub Actions
- ✅ **Security scanning** with Trivy
- ✅ **Monitoring** with Prometheus and Grafana

---

## 📦 Prerequisites

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8 GB
- Disk: 50 GB SSD
- OS: Ubuntu 20.04+ / Debian 11+ / CentOS 8+

**Recommended:**
- CPU: 8 cores
- RAM: 16 GB
- Disk: 100 GB SSD
- OS: Ubuntu 22.04 LTS

### Software Requirements

1. **Docker** (v24.0+)
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

2. **Docker Compose** (v2.20+)
   ```bash
   sudo apt-get update
   sudo apt-get install docker-compose-plugin
   ```

3. **Git** (v2.30+)
   ```bash
   sudo apt-get install git
   ```

4. **curl** (for health checks)
   ```bash
   sudo apt-get install curl
   ```

### Network Requirements

- **Ports to open:**
  - 80 (HTTP)
  - 443 (HTTPS)
  - 5000 (Backend API - optional, can be internal only)
  - 5432 (PostgreSQL - internal only)
  - 6379 (Redis - internal only)

- **Firewall configuration:**
  ```bash
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw enable
  ```

---

## 🏗️ Architecture

### Production Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Internet                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  Nginx Proxy   │ (Port 80/443)
            │  (SSL/TLS)     │
            └────────┬───────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Nginx)       │    │    (Flask)      │
│   Port 80       │    │    Port 5000    │
└─────────────────┘    └────────┬────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
           ┌─────────────────┐    ┌─────────────────┐
           │   PostgreSQL    │    │     Redis       │
           │   Port 5432     │    │    Port 6379    │
           └─────────────────┘    └─────────────────┘
```

### Container Services

1. **Frontend** (Nginx + React)
   - Serves static files
   - Handles client-side routing
   - Proxies API requests to backend

2. **Backend** (Flask + Gunicorn)
   - REST API endpoints
   - Business logic
   - Database operations

3. **PostgreSQL**
   - Primary database
   - Persistent data storage

4. **Redis**
   - Session storage
   - Caching layer
   - Task queue

5. **Nginx Proxy**
   - SSL/TLS termination
   - Load balancing
   - Reverse proxy

---

## 🚀 Deployment Methods

### Method 1: Manual Deployment (Recommended for first deployment)

**Step-by-step deployment using scripts**

### Method 2: CI/CD Deployment (Recommended for updates)

**Automated deployment via GitHub Actions**

### Method 3: Docker Compose Only

**Direct Docker Compose deployment**

---

## ⚙️ Configuration

### 1. Environment Variables

Copy the example environment file:

```bash
cp .env.production.example .env.production
```

Edit `.env.production` and set the following **required** variables:

```bash
# Database
POSTGRES_PASSWORD=your-strong-password-here
POSTGRES_USER=store_user
POSTGRES_DB=store_db

# Redis
REDIS_PASSWORD=your-strong-redis-password

# Backend
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-min-32-chars
CORS_ORIGINS=https://yourdomain.com

# Frontend
VITE_API_URL=https://api.yourdomain.com

# Domain
DOMAIN=yourdomain.com
SSL_EMAIL=admin@yourdomain.com
```

### 2. SSL/TLS Certificates

**Option A: Let's Encrypt (Recommended)**

```bash
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

**Option B: Self-signed (Development only)**

```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/private.key \
  -out nginx/ssl/certificate.crt
```

### 3. Nginx Configuration

Update `nginx/nginx.conf` with your domain:

```nginx
server_name yourdomain.com www.yourdomain.com;
ssl_certificate /etc/nginx/ssl/certificate.crt;
ssl_certificate_key /etc/nginx/ssl/private.key;
```

---

## 📝 Deployment Steps

### Method 1: Manual Deployment

#### Step 1: Clone Repository

```bash
git clone https://github.com/hamfarid/store.git
cd store
```

#### Step 2: Configure Environment

```bash
cp .env.production.example .env.production
nano .env.production  # Edit with your values
```

#### Step 3: Make Scripts Executable

```bash
chmod +x scripts/deploy-production.sh
chmod +x scripts/rollback.sh
chmod +x scripts/health-check.sh
```

#### Step 4: Run Deployment

```bash
./scripts/deploy-production.sh
```

**What this does:**
1. ✅ Checks prerequisites
2. ✅ Loads environment variables
3. ✅ Creates database backup
4. ✅ Builds Docker images
5. ✅ Deploys containers
6. ✅ Runs database migrations
7. ✅ Performs health checks
8. ✅ Shows deployment summary

#### Step 5: Verify Deployment

```bash
./scripts/health-check.sh --verbose
```

---

### Method 2: CI/CD Deployment

#### Step 1: Configure GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

```
SERVER_HOST=your-server-ip
SERVER_USER=deploy
SSH_PRIVATE_KEY=your-ssh-private-key
DOMAIN=yourdomain.com
VITE_API_URL=https://api.yourdomain.com
SLACK_WEBHOOK=your-slack-webhook-url (optional)
```

#### Step 2: Push to Main Branch

```bash
git add .
git commit -m "feat: deploy to production"
git push origin main
```

The GitHub Actions workflow will automatically:
1. Build Docker images
2. Run security scans
3. Deploy to production
4. Run health checks
5. Send notifications

---

## ✅ Post-Deployment

### 1. Verify Services

```bash
# Check all services
docker-compose -f docker-compose.production.yml ps

# Check logs
docker-compose -f docker-compose.production.yml logs -f
```

### 2. Create Admin User

```bash
docker-compose -f docker-compose.production.yml exec backend \
  flask create-admin --username admin --email admin@yourdomain.com
```

### 3. Test Application

1. **Frontend:** https://yourdomain.com
2. **Backend API:** https://api.yourdomain.com/health
3. **API Docs:** https://api.yourdomain.com/api/docs

### 4. Configure Monitoring

See [MONITORING.md](./MONITORING.md) for Prometheus and Grafana setup.

---

## 📊 Monitoring

### Health Checks

Run automated health checks:

```bash
./scripts/health-check.sh --verbose
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.production.yml logs -f

# Specific service
docker-compose -f docker-compose.production.yml logs -f backend

# Last 100 lines
docker-compose -f docker-compose.production.yml logs --tail=100 backend
```

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df
```

---

## 💾 Backup & Recovery

### Automated Backups

Backups are automatically created before each deployment in:
```
backups/deployment_YYYYMMDD_HHMMSS/
```

### Manual Backup

```bash
# Create backup
docker-compose -f docker-compose.production.yml exec postgres pg_dump \
  -U store_user -d store_db > backup_$(date +%Y%m%d).sql

# Compress backup
gzip backup_$(date +%Y%m%d).sql
```

### Restore from Backup

```bash
# List available backups
ls -lh backups/

# Rollback to specific backup
./scripts/rollback.sh backups/deployment_20251108_120000
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Container Won't Start

**Check logs:**
```bash
docker-compose -f docker-compose.production.yml logs backend
```

**Check container status:**
```bash
docker ps -a
```

#### 2. Database Connection Failed

**Check PostgreSQL:**
```bash
docker-compose -f docker-compose.production.yml exec postgres \
  pg_isready -U store_user -d store_db
```

**Check environment variables:**
```bash
docker-compose -f docker-compose.production.yml exec backend env | grep DATABASE
```

#### 3. Frontend Not Loading

**Check Nginx logs:**
```bash
docker-compose -f docker-compose.production.yml logs frontend
```

**Verify build:**
```bash
docker-compose -f docker-compose.production.yml exec frontend ls -la /usr/share/nginx/html
```

#### 4. High Memory Usage

**Check container stats:**
```bash
docker stats
```

**Restart specific service:**
```bash
docker-compose -f docker-compose.production.yml restart backend
```

### Emergency Procedures

#### Complete Rollback

```bash
./scripts/rollback.sh
```

#### Force Rebuild

```bash
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d
```

#### Clean Docker System

```bash
docker system prune -a --volumes
```

---

## 📞 Support

For issues or questions:
- **GitHub Issues:** https://github.com/hamfarid/store/issues
- **Documentation:** https://github.com/hamfarid/store/docs

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-11-08  
**Status:** Production Ready

