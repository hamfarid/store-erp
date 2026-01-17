# Deployment Flow - سير عمل النشر

## نظرة عامة / Overview

دليل شامل لنشر المشاريع المبنية باستخدام Global Guidelines.

Comprehensive guide for deploying projects built using Global Guidelines.

---

## Pre-Deployment Checklist / قائمة ما قبل النشر

### 1. Code Quality ✅

```bash
# Run all quality checks
flake8 .
mypy .
python .global/tools/analyze_dependencies.py .
python .global/tools/detect_code_duplication.py .
```

- [ ] No flake8 errors
- [ ] No mypy errors
- [ ] No circular dependencies
- [ ] Code duplication < 5%

### 2. Testing ✅

```bash
# Run all tests
pytest --cov=. --cov-report=html

# Check coverage
open htmlcov/index.html
```

- [ ] All tests pass
- [ ] Coverage > 80%
- [ ] Integration tests pass
- [ ] E2E tests pass

### 3. Documentation ✅

- [ ] README updated
- [ ] CHANGELOG updated
- [ ] API docs updated
- [ ] Environment variables documented

### 4. Security ✅

```bash
# Security audit
pip-audit
bandit -r .
safety check
```

- [ ] No security vulnerabilities
- [ ] Secrets not in code
- [ ] Dependencies up to date
- [ ] SSL/TLS configured

### 5. Performance ✅

- [ ] Load testing done
- [ ] Database optimized
- [ ] Caching configured
- [ ] CDN configured (if applicable)

---

## Deployment Strategies / استراتيجيات النشر

### Strategy 1: Blue-Green Deployment

**الوصف:** نشر الإصدار الجديد بجانب القديم ثم التبديل

```
┌─────────────┐     ┌─────────────┐
│   Blue      │     │   Green     │
│  (Current)  │────▶│    (New)    │
│   v1.0.0    │     │   v1.1.0    │
└─────────────┘     └─────────────┘
       │                   │
       └────────┬──────────┘
                │
          Load Balancer
```

**Steps:**
```bash
# 1. Deploy new version (Green)
deploy_green_environment v1.1.0

# 2. Test Green
run_smoke_tests green

# 3. Switch traffic
switch_traffic_to_green

# 4. Monitor
monitor_metrics --duration 30m

# 5. If OK, decommission Blue
# If issues, rollback to Blue
```

---

### Strategy 2: Canary Deployment

**الوصف:** نشر تدريجي لنسبة صغيرة من المستخدمين

```
v1.0.0 (90%) ────┐
                 ├──▶ Users
v1.1.0 (10%) ────┘
```

**Steps:**
```bash
# 1. Deploy canary (10% traffic)
deploy_canary v1.1.0 --traffic 10

# 2. Monitor metrics
monitor_canary --duration 1h

# 3. If OK, increase gradually
update_canary_traffic 25
update_canary_traffic 50
update_canary_traffic 100

# 4. Complete deployment
finalize_canary_deployment
```

---

### Strategy 3: Rolling Deployment

**الوصف:** تحديث تدريجي للخوادم واحدة تلو الأخرى

```
Server 1: v1.0.0 → v1.1.0 ✓
Server 2: v1.0.0 → v1.1.0 ✓
Server 3: v1.0.0 → v1.1.0 ✓
Server 4: v1.0.0 → v1.1.0 ✓
```

**Steps:**
```bash
# Kubernetes rolling update
kubectl set image deployment/myapp myapp=myapp:v1.1.0

# Monitor rollout
kubectl rollout status deployment/myapp

# If issues, rollback
kubectl rollout undo deployment/myapp
```

---

## Deployment Environments / بيئات النشر

### 1. Development

```yaml
# config/environments/development.yml
environment: development
debug: true
database:
  host: localhost
  name: myapp_dev
cache:
  enabled: false
logging:
  level: DEBUG
```

### 2. Staging

```yaml
# config/environments/staging.yml
environment: staging
debug: false
database:
  host: staging-db.internal
  name: myapp_staging
cache:
  enabled: true
  backend: redis
logging:
  level: INFO
```

### 3. Production

```yaml
# config/environments/production.yml
environment: production
debug: false
database:
  host: prod-db.internal
  name: myapp_prod
  pool_size: 20
cache:
  enabled: true
  backend: redis
  cluster: true
logging:
  level: WARNING
monitoring:
  enabled: true
```

---

## Deployment Process / عملية النشر

### Step 1: Preparation

```bash
# 1. Create release branch
git checkout -b release/v1.1.0

# 2. Update version
echo "1.1.0" > VERSION

# 3. Update CHANGELOG
cat >> CHANGELOG.md << EOF
## [1.1.0] - $(date +%Y-%m-%d)

### Added
- Feature X
- Feature Y

### Fixed
- Bug Z
EOF

# 4. Commit changes
git add VERSION CHANGELOG.md
git commit -m "chore: bump version to 1.1.0"

# 5. Create tag
git tag -a v1.1.0 -m "Release v1.1.0"

# 6. Push
git push origin release/v1.1.0
git push origin v1.1.0
```

---

### Step 2: Build

```bash
# Python package
python -m build
twine check dist/*

# Docker image
docker build -t myapp:v1.1.0 .
docker tag myapp:v1.1.0 myapp:latest

# Push to registry
docker push myapp:v1.1.0
docker push myapp:latest
```

---

### Step 3: Deploy to Staging

```bash
# Deploy to staging
deploy_to_staging v1.1.0

# Run smoke tests
pytest tests/smoke/ --env=staging

# Run integration tests
pytest tests/integration/ --env=staging

# Manual QA testing
# ...
```

---

### Step 4: Deploy to Production

```bash
# Backup database
backup_production_database

# Deploy
deploy_to_production v1.1.0

# Run smoke tests
pytest tests/smoke/ --env=production

# Monitor
monitor_production --duration 1h
```

---

### Step 5: Post-Deployment

```bash
# Verify deployment
curl https://api.myapp.com/health

# Check logs
kubectl logs -f deployment/myapp

# Monitor metrics
open https://grafana.myapp.com

# Notify team
send_deployment_notification v1.1.0 success
```

---

## Docker Deployment / نشر Docker

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Copy Global Guidelines
COPY .global/ .global/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    image: myapp:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## Kubernetes Deployment / نشر Kubernetes

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1.1.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## CI/CD Pipeline / خط أنابيب CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest flake8 mypy
      
      - name: Run tests
        run: pytest --cov=.
      
      - name: Quality checks
        run: |
          flake8 .
          mypy .

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.ref_name }} .
          docker tag myapp:${{ github.ref_name }} myapp:latest
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push myapp:${{ github.ref_name }}
          docker push myapp:latest

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.ref_name }}
          kubectl rollout status deployment/myapp

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.ref_name }}
          kubectl rollout status deployment/myapp
      
      - name: Notify team
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"Deployed ${{ github.ref_name }} to production"}'
```

---

## Monitoring & Alerting / المراقبة والتنبيهات

### Health Checks

```python
# app/health.py
from fastapi import APIRouter
from config.definitions import APIResponse

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return APIResponse(
        success=True,
        message="Service is healthy",
        data={"status": "ok"}
    )

@router.get("/ready")
async def readiness_check():
    """Readiness check - includes dependencies"""
    # Check database
    db_ok = await check_database()
    # Check Redis
    redis_ok = await check_redis()
    
    if db_ok and redis_ok:
        return APIResponse(
            success=True,
            message="Service is ready",
            data={"status": "ready"}
        )
    else:
        return APIResponse(
            success=False,
            message="Service not ready",
            data={"database": db_ok, "redis": redis_ok}
        ), 503
```

### Metrics

```python
# app/metrics.py
from prometheus_client import Counter, Histogram

# Request counter
requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Response time
response_time = Histogram(
    'http_response_time_seconds',
    'HTTP response time in seconds',
    ['method', 'endpoint']
)
```

---

## Rollback Procedures / إجراءات التراجع

### Quick Rollback

```bash
# Kubernetes
kubectl rollout undo deployment/myapp

# Docker Compose
docker-compose down
docker-compose up -d --build --force-recreate
```

### Database Rollback

```bash
# Restore from backup
restore_database_backup latest

# Run down migrations
alembic downgrade -1
```

---

## Post-Deployment Tasks / مهام ما بعد النشر

### 1. Monitoring (First Hour)

```
✓ Check error rates
✓ Check response times
✓ Check resource usage
✓ Check logs for errors
✓ Verify all endpoints work
```

### 2. Communication

```
✓ Notify team of successful deployment
✓ Update status page
✓ Announce new features (if any)
✓ Document any issues encountered
```

### 3. Cleanup

```bash
# Remove old Docker images
docker image prune -a --filter "until=24h"

# Clean up old deployments
kubectl delete deployment myapp-old
```

---

## References / المراجع

- [Development Flow](./DEVELOPMENT_FLOW.md)
- [Integration Flow](./INTEGRATION_FLOW.md)
- [Global Guidelines](../GLOBAL_GUIDELINES_v3.7.txt)

---

**Last Updated:** 2025-11-02  
**Version:** 1.0.0  
**Status:** ✅ Active

