# Gaara ERP v12 - Deployment Guide

**Last Updated**: 2025-11-28  
**Version**: 12.0.0

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Docker Deployment](#docker-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Security Scanning (Trivy)](#security-scanning-trivy)
8. [Monitoring & Health Checks](#monitoring--health-checks)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Storage | 20 GB | 50+ GB SSD |
| Python | 3.11+ | 3.11.x |
| Node.js | 18+ | 20.x LTS |
| PostgreSQL | 14+ | 15+ |
| Redis | 6+ | 7+ |

### Required Tools

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Install kubectl (for K8s)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/gaara-erp.git
cd gaara-erp
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit with your values
nano .env
```

### Required Environment Variables

```bash
# Django
SECRET_KEY=<generate-with-python>
DEBUG=false
ALLOWED_HOSTS=gaara-erp.com,api.gaara-erp.com

# Database
DATABASE_URL=postgres://user:pass@host:5432/gaara_erp
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=gaara_erp
POSTGRES_USER=gaara_admin
POSTGRES_PASSWORD=<secure-password>

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
ENCRYPTION_KEY=<generate-with-openssl>
BACKUP_ENCRYPTION_KEY=<generate-with-openssl>

# External Services (optional)
ANTHROPIC_API_KEY=<for-ai-features>
OPENAI_API_KEY=<for-ai-features>

# CORS
CORS_ALLOWED_ORIGINS=https://gaara-erp.com,https://app.gaara-erp.com
```

### Generate Secure Keys

```bash
# Generate Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate encryption keys
openssl rand -base64 32
```

---

## Database Setup

### 1. Create Database

```bash
# PostgreSQL
sudo -u postgres psql

CREATE USER gaara_admin WITH PASSWORD 'your_password';
CREATE DATABASE gaara_erp OWNER gaara_admin;
GRANT ALL PRIVILEGES ON DATABASE gaara_erp TO gaara_admin;

# Enable required extensions
\c gaara_erp
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
\q
```

### 2. Run Migrations

```bash
cd gaara_erp
python manage.py migrate
python manage.py createsuperuser
```

### 3. Load Initial Data (Optional)

```bash
python manage.py loaddata fixtures/initial_data.json
```

---

## Docker Deployment

### Quick Start

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: gaara_erp
      POSTGRES_USER: gaara_admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gaara_admin -d gaara_erp"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgres://gaara_admin:${POSTGRES_PASSWORD}@db:5432/gaara_erp
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      DEBUG: 'false'
    ports:
      - "8000:8000"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./gaara-erp-frontend
      dockerfile: Dockerfile
    depends_on:
      - backend
    ports:
      - "3000:80"
    environment:
      VITE_API_URL: http://backend:8000/api

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - static_volume:/var/www/static:ro
      - media_volume:/var/www/media:ro
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
```

### Production Build

```bash
# Build production images
docker build -t gaara-erp:latest .
docker build -t gaara-erp-frontend:latest ./gaara-erp-frontend

# Push to registry
docker push your-registry.com/gaara-erp:latest
docker push your-registry.com/gaara-erp-frontend:latest
```

---

## Kubernetes Deployment

### 1. Create Namespace

```bash
kubectl create namespace gaara-erp
```

### 2. Create Secrets

```bash
kubectl create secret generic gaara-erp-secrets \
  --from-literal=SECRET_KEY="your-secret-key" \
  --from-literal=DATABASE_PASSWORD="your-db-password" \
  --from-literal=ENCRYPTION_KEY="your-encryption-key" \
  -n gaara-erp
```

### 3. Deploy Application

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gaara-erp
  namespace: gaara-erp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gaara-erp
  template:
    metadata:
      labels:
        app: gaara-erp
    spec:
      containers:
        - name: gaara-erp
          image: your-registry.com/gaara-erp:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: gaara-erp-secrets
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "1Gi"
              cpu: "1000m"
          livenessProbe:
            httpGet:
              path: /health/
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

```bash
kubectl apply -f k8s/
```

---

## CI/CD Pipeline

### GitHub Actions

The CI/CD pipeline is configured in `.github/workflows/ci.yml` and includes:

1. **Code Quality**: Linting, formatting checks
2. **Security**: Dependency scanning, SAST
3. **Testing**: Unit tests, integration tests
4. **E2E Testing**: Playwright browser tests
5. **Docker Build**: Multi-stage builds
6. **Deployment**: Staging and production

### Workflow Triggers

- **Push to main**: Full pipeline + production deploy
- **Push to develop**: Full pipeline + staging deploy
- **Pull Request**: Tests only, no deploy

---

## Security Scanning (Trivy)

Gaara ERP uses **Trivy** for comprehensive security scanning integrated into GitHub Actions.

### What Trivy Scans

| Scan Type | Description |
|-----------|-------------|
| **Container Image** | OS packages & application dependencies in Docker images |
| **Filesystem** | Python & Node.js dependencies in source code |
| **IaC (Infrastructure as Code)** | Dockerfile, docker-compose.yml, K8s manifests |
| **Secrets** | Hardcoded API keys, passwords, tokens in code |

### Workflows

1. **`ci.yml`** - Runs Trivy on every push/PR:
   - Container image scan after Docker build
   - SBOM generation (CycloneDX format)
   - Results uploaded to GitHub Security tab

2. **`trivy-security.yml`** - Dedicated security workflow:
   - Scheduled daily at 6 AM UTC
   - Full filesystem, secret, IaC, and container scans
   - SBOM in both CycloneDX and SPDX formats
   - Vulnerability reports as artifacts

### Running Trivy Locally

```bash
# Install Trivy
brew install trivy  # macOS
# or
sudo apt-get install trivy  # Ubuntu

# Scan Docker image
docker build -t gaara-erp:local .
trivy image gaara-erp:local

# Scan filesystem
trivy fs --scanners vuln,secret gaara_erp/

# Scan for secrets
trivy fs --scanners secret .

# Scan IaC (Dockerfile, docker-compose, K8s)
trivy config .

# Generate SBOM
trivy image --format cyclonedx -o sbom.json gaara-erp:local
```

### Severity Levels

| Level | Action |
|-------|--------|
| **CRITICAL** | Must fix before deployment |
| **HIGH** | Fix within 7 days |
| **MEDIUM** | Fix within 30 days |
| **LOW** | Fix when convenient |

### Ignoring False Positives

Create `.trivyignore` in project root:

```
# Ignore specific CVEs
CVE-2023-XXXXX

# Ignore by package
pkg:pypi/example-package
```

### SBOM (Software Bill of Materials)

SBOMs are automatically generated on every build in two formats:

- **CycloneDX** (`sbom-cyclonedx.json`) - For vulnerability management tools
- **SPDX** (`sbom-spdx.json`) - For license compliance

Download from GitHub Actions artifacts.

### Security Tab Integration

All Trivy findings are uploaded to GitHub's Security tab:
1. Go to repository → **Security** tab
2. Click **Code scanning alerts**
3. Filter by tool: `trivy-*`

---

## Monitoring & Health Checks

### Health Check Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/health/` | Basic health status |
| `/health/detailed/` | Detailed health with dependencies |

### Prometheus Metrics

```bash
# Expose metrics endpoint
pip install django-prometheus
```

### Logging

Logs are written to:
- `/app/logs/django.log` - Application logs
- `/app/logs/error.log` - Error logs
- stdout/stderr - For container log aggregation

---

## Troubleshooting

### Common Issues

#### Database Connection Failed

```bash
# Check database is running
docker-compose ps db

# Check connectivity
docker exec -it gaara-erp_backend_1 python -c "import psycopg2; print('OK')"
```

#### Static Files Not Loading

```bash
# Collect static files
docker exec -it gaara-erp_backend_1 python manage.py collectstatic --noinput
```

#### Migrations Failed

```bash
# Check migration status
python manage.py showmigrations

# Reset specific app migrations
python manage.py migrate app_name zero
python manage.py migrate app_name
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend

# Kubernetes logs
kubectl logs -f deployment/gaara-erp -n gaara-erp
```

---

## Security Checklist

Before deploying to production:

- [ ] All secrets stored in environment/vault
- [ ] HTTPS enabled with valid certificates
- [ ] DEBUG=false
- [ ] ALLOWED_HOSTS configured
- [ ] CORS origins restricted
- [ ] Database connections encrypted
- [ ] Firewall rules configured
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Audit logging enabled

---

**Last Reviewed**: 2025-11-28  
**Next Review**: 2026-02-28

