# Deployment Workflow

**Version:** 2.0.0  
**Last Updated:** 2026-01-16

---

## Environments

| Environment | Purpose | URL |
|-------------|---------|-----|
| Development | Local dev | localhost:6501 |
| Staging | Testing | staging.store-erp.local |
| Production | Live | store-erp.com |

---

## Deployment Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Develop   │────▶│   Staging   │────▶│ Production  │
│   Branch    │     │   Deploy    │     │   Deploy    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
   Unit Tests         E2E Tests          Smoke Tests
   Lint Check         QA Review          Monitoring
   Build Check        Load Test          Alerting
```

---

## Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing
- [ ] No linting errors
- [ ] Code reviewed
- [ ] Security scan passed

### Database
- [ ] Migrations tested
- [ ] Rollback plan ready
- [ ] Backup created

### Configuration
- [ ] Environment variables set
- [ ] Secrets updated
- [ ] SSL certificates valid

### Documentation
- [ ] Release notes written
- [ ] Changelog updated
- [ ] API docs current

---

## Deployment Steps

### 1. Staging Deployment

```bash
# Automatic on merge to develop
# Or manual:
./scripts/deploy.sh staging
```

### 2. Production Deployment

```bash
# Requires approval
./scripts/deploy.sh production --force

# Or via Docker
docker-compose -f docker-compose.prod.yml up -d
```

---

## Rollback Procedure

### Quick Rollback

```bash
# Revert to previous version
git revert HEAD
./scripts/deploy.sh production --force
```

### Database Rollback

```bash
# Restore from backup
./scripts/restore-backup.sh backup_YYYYMMDD_HHMMSS.sql
```

---

## Monitoring

### Health Checks
- `/api/health` - Backend health
- `/health` - Nginx health

### Metrics to Watch
- Response time < 1s
- Error rate < 0.1%
- CPU usage < 80%
- Memory usage < 80%

### Alerting
- Slack notifications
- Email alerts
- PagerDuty (critical)

---

## Post-Deployment

### Verification
- [ ] Health checks passing
- [ ] Smoke tests passing
- [ ] No error spikes
- [ ] Performance normal

### Communication
- [ ] Team notified
- [ ] Stakeholders updated
- [ ] Release notes published
