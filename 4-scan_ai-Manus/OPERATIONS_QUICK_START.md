# 🚀 Production Operations Quick Reference

## Immediate Actions Required

### 1️⃣ Configure GitHub Secrets (CRITICAL - Do First)
```bash
# Open GitHub Secrets page
https://github.com/hamfarid/gaara-Scan-system/settings/secrets/actions

# Or use GitHub CLI to add secrets quickly:
gh secret set PROD_DB_HOST -b "your-db-host"
gh secret set PROD_DB_PORT -b "5432"
gh secret set PROD_DB_NAME -b "gaara_scan_ai"
gh secret set PROD_DB_USER -b "gaara_user"
gh secret set PROD_DB_PASSWORD -b "$(openssl rand -base64 32)"

gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set AWS_REGION
gh secret set BACKUP_S3_BUCKET

# See .github/PRODUCTION_SECRETS.md for complete list
```

### 2️⃣ Deploy Monitoring Stack (Before First Release)
```bash
# Start all monitoring services (Prometheus, Grafana, AlertManager, Loki, Jaeger)
docker-compose -f docker-compose.monitoring.yml up -d

# Verify all services are running
docker ps | grep -E "prometheus|grafana|alertmanager|loki|jaeger"

# Access dashboards
# - Grafana: http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9090
# - Jaeger: http://localhost:16686
```

### 3️⃣ Test Automated Backups
```bash
# Trigger manual backup via GitHub Actions UI
https://github.com/hamfarid/gaara-Scan-system/actions/workflows/automated-backup.yml
# Click "Run workflow" → Select backup_type=full

# Or via CLI
gh workflow run automated-backup.yml -f backup_type=full

# Verify backup in S3
aws s3 ls s3://your-bucket-name/database-backups/
aws s3 ls s3://your-bucket-name/application-backups/
```

### 4️⃣ Test Rollback Procedure
```bash
# First test in STAGING environment (not production!)
gh workflow run rollback.yml \
  -f environment=staging \
  -f version=latest \
  -f reason="Testing rollback procedure"

# Monitor rollback progress
https://github.com/hamfarid/gaara-Scan-system/actions/workflows/rollback.yml

# Check created GitHub issue for audit trail
https://github.com/hamfarid/gaara-Scan-system/issues
```

---

## Daily Operations

### Check System Health
```bash
# View all workflow runs
gh workflow list
gh run list

# Check if any alerts are firing
curl http://localhost:9093/api/v1/alerts

# View Prometheus metrics
curl http://localhost:9090/api/v1/query?query=up

# Check application logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### View Metrics
```bash
# CPU usage across all services
curl 'http://localhost:9090/api/v1/query?query=100-((avg(rate(node_cpu_seconds_total%7Bmode=%22idle%22%7D%5B5m%5D))*100))'

# Memory usage
curl 'http://localhost:9090/api/v1/query?query=(1-(node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes))*100'

# Request rate
curl 'http://localhost:9090/api/v1/query?query=rate(http_requests_total%5B5m%5D)'

# Error rate
curl 'http://localhost:9090/api/v1/query?query=rate(http_requests_total%7Bstatus=%225xx%22%7D%5B5m%5D)'
```

### Deploy New Release
```bash
# Follow deployment checklist
cat DEPLOYMENT_CHECKLIST.md

# Create git tag
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1

# Docker build & publish triggered automatically
# Check Actions tab for progress
https://github.com/hamfarid/gaara-Scan-system/actions/workflows/docker-publish.yml

# View deployed version in production
# (Check pod/container labels or app version endpoint)
```

---

## Emergency Procedures

### 🚨 Quick Rollback (60 seconds)
```bash
# Immediate rollback to previous version
gh workflow run rollback.yml \
  -f environment=production \
  -f version=v1.0.0 \
  -f reason="Emergency: Critical bug affecting users"

# Monitor rollback
gh run list --workflow=rollback.yml --limit=1

# Verify health
curl -s http://your-app/health | jq .
```

### 🚨 Database Recovery
```bash
# List available backups
aws s3 ls s3://your-bucket/database-backups/ --recursive | sort

# Download latest backup
aws s3 cp s3://your-bucket/database-backups/gaara_db_backup_*.sql.gz ./

# Restore database
gunzip gaara_db_backup_*.sql.gz
psql postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME < gaara_db_backup_*.sql

# Verify recovery
psql postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME -c "SELECT COUNT(*) FROM users;"
```

### 🚨 Redis Cache Recovery
```bash
# List Redis backups
aws s3 ls s3://your-bucket/redis-backups/ --recursive

# Download latest dump
aws s3 cp s3://your-bucket/redis-backups/redis_backup_*.rdb.gz ./

# Restore Redis
gunzip redis_backup_*.rdb.gz
redis-cli --pipe < redis_backup_*.rdb  # Or restore using docker volume

# Clear problematic keys if needed
redis-cli FLUSHDB  # ⚠️ Be careful with this!
```

### 🚨 Out-of-Disk-Space Recovery
```bash
# Check disk usage
df -h

# Check backup S3 for cleanup opportunity
aws s3 ls s3://your-bucket/database-backups/ --recursive --human-readable --summarize

# Clear old backups (keep last 30 days)
# Note: Backup cleanup runs automatically per backup workflow
# Manual cleanup:
aws s3 rm s3://your-bucket/database-backups/ \
  --recursive \
  --exclude "*" \
  --include "gaara_db_backup_*.sql.gz" \
  # Remove files older than 30 days manually or via lifecycle policy
```

---

## Monitoring & Alerting

### Configure Alert Receivers
```bash
# Edit AlertManager configuration
vim monitoring/alertmanager/alertmanager.yml

# Update with your Slack webhook
# Update with your email server
# Update with your PagerDuty key

# Reload AlertManager
docker-compose -f docker-compose.monitoring.yml restart alertmanager
```

### View Alert Status
```bash
# All active alerts
curl http://localhost:9093/api/v1/alerts?active=true | jq '.data[]'

# Alerts by severity
curl http://localhost:9093/api/v1/alerts | jq '.data[] | select(.labels.severity=="critical")'

# Alert history
https://localhost:9093/  # UI shows all alerts
```

### Test Alert Delivery
```bash
# Trigger test alert in Prometheus
cat >> monitoring/prometheus/rules/test-alerts.yml <<EOF
groups:
  - name: test
    rules:
      - alert: TestAlert
        expr: vector(1)
        annotations:
          summary: "Test Alert"
EOF

# Reload Prometheus
docker-compose -f docker-compose.monitoring.yml restart prometheus

# Wait 30 seconds for alert to fire
# Check Slack/Email for notification
```

---

## Useful Commands

### Backend
```bash
# Run backend tests
python -m pytest tests/ -v

# Format code
python -m black backend/

# Lint code
python -m flake8 backend/

# Check migrations
alembic current
alembic heads

# Create new migration
alembic revision --autogenerate -m "Add new column"
```

### Frontend
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Format code
npm run format
```

### Docker
```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Clean up (remove volumes too!)
docker-compose down -v
```

### Database
```bash
# Connect to database
psql postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME

# List databases
\l

# Connect to database
\c gaara_scan_ai

# List tables
\dt

# View table structure
\d users

# Run SQL file
\i backup.sql
```

### Git
```bash
# Check status
git status

# Add all changes
git add -A

# Commit with message
git commit -m "feat: Add new feature"

# Push to main
git push origin main

# Create new tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# View commit history
git log --oneline -10

# View file changes
git diff backend/src/main.py
```

---

## Troubleshooting

### Workflows Not Triggering
```bash
# Check workflow syntax
gh workflow view automated-backup.yml

# Enable workflow if disabled
gh workflow enable automated-backup.yml

# Check if secrets are configured
gh secret list

# View workflow runs
gh run list --workflow=automated-backup.yml
```

### Monitoring Services Down
```bash
# Check service status
docker-compose -f docker-compose.monitoring.yml ps

# Restart specific service
docker-compose -f docker-compose.monitoring.yml restart prometheus

# View service logs
docker-compose -f docker-compose.monitoring.yml logs prometheus

# Rebuild and restart
docker-compose -f docker-compose.monitoring.yml up -d --force-recreate prometheus
```

### Backup Not Completing
```bash
# Check backup workflow logs
gh run view <run-id> -j backup-database

# Check S3 permissions
aws s3 ls s3://your-bucket/ --region us-east-1

# Check database connectivity
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT version();"

# Check disk space
df -h

# Manual backup test
pg_dump -h localhost -U gaara_user -d gaara_scan_ai > /tmp/test_backup.sql
gzip /tmp/test_backup.sql
aws s3 cp /tmp/test_backup.sql.gz s3://your-bucket/test-backup.sql.gz
```

### Alerts Not Firing
```bash
# Check alert rules syntax
curl http://localhost:9090/api/v1/rules | jq '.data'

# Verify metrics are being scraped
curl 'http://localhost:9090/api/v1/query?query=up'

# Test alert condition manually
curl 'http://localhost:9090/api/v1/query?query=node_memory_MemAvailable_bytes'

# Check AlertManager configuration
docker-compose -f docker-compose.monitoring.yml logs alertmanager
```

---

## Documentation Links

- **Production Readiness:** [PRODUCTION_READINESS.md](PRODUCTION_READINESS.md)
- **Deployment Checklist:** [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- **Production Secrets:** [.github/PRODUCTION_SECRETS.md](.github/PRODUCTION_SECRETS.md)
- **Monitoring Guide:** [monitoring/MONITORING_GUIDE.md](monitoring/MONITORING_GUIDE.md)
- **CI/CD Setup:** [.github/CICD_SETUP.md](.github/CICD_SETUP.md)
- **Quick CI/CD Ref:** [CICD_QUICK_REFERENCE.md](CICD_QUICK_REFERENCE.md)

---

## Important Reminders

✅ **Before Every Release:**
- Run full test suite
- Create database backup
- Check all metrics in Grafana
- Review deployment checklist
- Get approval from team lead

✅ **During Deployment:**
- Monitor error rates in real-time
- Check Prometheus dashboards
- Watch application logs
- Be ready to rollback

✅ **After Deployment:**
- Run smoke tests
- Monitor for 1 hour
- Check user feedback
- Update documentation

⚠️ **Emergency Contacts:** See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for on-call procedures

---

**Last Updated:** 2026-01-31  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
