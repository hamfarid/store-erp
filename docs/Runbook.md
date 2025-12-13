# Operations Runbook

**Last Updated:** 2025-11-04  
**Owner:** DevOps/Operations Team  
**Status:** ✅ Current

---

## Overview

Operational procedures for deployment, monitoring, troubleshooting, and incident response.

## Deployment

### Pre-Deployment Checklist

- [ ] All tests passing (CI green)
- [ ] Security scans passed (no critical/high findings)
- [ ] SBOM generated and reviewed
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Secrets rotated (if needed)
- [ ] Backup created
- [ ] Rollback plan documented

### Deployment Process

#### Development

```bash
# 1. Merge PR to main
# 2. CI/CD automatically deploys to dev
# 3. Verify deployment
curl https://dev-api.example.com/health
```

#### Staging

```bash
# 1. Tag release: git tag v1.0.0
# 2. Push tag: git push origin v1.0.0
# 3. CI/CD automatically deploys to staging
# 4. Run smoke tests
pytest tests/smoke/
# 5. Verify in staging environment
```

#### Production

```bash
# 1. Create release PR
# 2. Get approval from 2 reviewers
# 3. Merge to main
# 4. Tag release: git tag v1.0.0
# 5. CI/CD automatically deploys to production
# 6. Monitor for errors
# 7. Verify health checks
```

### Rollback Procedure

```bash
# 1. Identify issue
# 2. Revert to previous version
git revert <commit-hash>
git push origin main

# 3. CI/CD automatically deploys previous version
# 4. Verify rollback successful
curl https://api.example.com/health

# 5. Post-incident review
```

## Monitoring

### Health Checks

```bash
# API health
curl https://api.example.com/health

# Database health
curl https://api.example.com/api/health

# Frontend health
curl https://example.com/
```

### Metrics to Monitor

| Metric | Threshold | Action |
|--------|-----------|--------|
| API Response Time (p95) | > 1000ms | Investigate |
| Error Rate | > 1% | Alert |
| CPU Usage | > 80% | Scale up |
| Memory Usage | > 85% | Scale up |
| Database Connections | > 80% of pool | Investigate |
| Disk Usage | > 90% | Clean up / expand |

### Logging

```bash
# View recent logs
docker logs <container-id> --tail 100 -f

# Search logs
docker logs <container-id> | grep "ERROR"

# Export logs
docker logs <container-id> > logs.txt
```

### Alerts

- **Slack:** #alerts channel
- **Email:** <ops-team@example.com>
- **PagerDuty:** On-call rotation

## Troubleshooting

### API Not Responding

```bash
# 1. Check if service is running
docker ps | grep api

# 2. Check logs for errors
docker logs <container-id> --tail 50

# 3. Check database connection
curl https://api.example.com/api/health

# 4. Restart service
docker restart <container-id>

# 5. If still failing, rollback
```

### Database Connection Issues

```bash
# 1. Check database status
psql -h db.prod.internal -U user -d inventory -c "SELECT 1"

# 2. Check connection pool
# Look for "too many connections" error

# 3. Increase pool size in .env
DATABASE_POOL_SIZE=20

# 4. Restart API service
docker restart <container-id>
```

### High Memory Usage

```bash
# 1. Check memory usage
docker stats <container-id>

# 2. Check for memory leaks
# Review recent code changes

# 3. Restart service
docker restart <container-id>

# 4. Scale up if needed
docker-compose up -d --scale api=2
```

### Slow Queries

```bash
# 1. Enable slow query log
# In PostgreSQL: log_min_duration_statement = 1000

# 2. Analyze slow queries
EXPLAIN ANALYZE SELECT ...;

# 3. Add indexes if needed
CREATE INDEX idx_name ON table(column);

# 4. Restart database
docker restart <db-container-id>
```

## Maintenance

### Database Maintenance

```bash
# Backup database
pg_dump -h db.prod.internal -U user inventory > backup.sql

# Restore database
psql -h db.prod.internal -U user inventory < backup.sql

# Vacuum (cleanup)
VACUUM ANALYZE;

# Reindex
REINDEX DATABASE inventory;
```

### Log Rotation

```bash
# Logs are rotated daily
# Retention: 30 days
# Location: /var/log/app/

# Manual rotation
logrotate -f /etc/logrotate.d/app
```

### Certificate Renewal

```bash
# Let's Encrypt certificates auto-renew
# Renewal happens 30 days before expiry

# Manual renewal
certbot renew --force-renewal

# Verify certificate
openssl s_client -connect api.example.com:443
```

## Incident Response

### Severity Levels

| Level | Response Time | Escalation |
|-------|---------------|------------|
| Critical | 15 min | VP Eng + CTO |
| High | 1 hour | Engineering Lead |
| Medium | 4 hours | Team Lead |
| Low | 24 hours | Backlog |

### Incident Process

1. **Detection:** Alert triggered
2. **Triage:** Assess severity
3. **Mitigation:** Stop the bleeding (rollback, scale, etc.)
4. **Resolution:** Fix root cause
5. **Communication:** Update status page
6. **Post-Incident:** RCA + improvements

### Communication Template

```
🚨 INCIDENT: [Service] - [Brief Description]

Status: INVESTIGATING
Severity: [CRITICAL/HIGH/MEDIUM/LOW]
Impact: [Number] users affected
ETA: [Time estimate]

Updates:
- [Time] Initial alert received
- [Time] Root cause identified
- [Time] Mitigation in progress
- [Time] Service restored
```

## Disaster Recovery

### RTO/RPO Targets

| Component | RTO | RPO |
|-----------|-----|-----|
| API | 15 min | 5 min |
| Database | 30 min | 1 min |
| Frontend | 5 min | 0 min |

### Backup Verification

```bash
# Weekly restore test
# 1. Restore to staging
# 2. Run smoke tests
# 3. Verify data integrity
# 4. Document results
```

### Failover Procedure

```bash
# 1. Detect primary failure
# 2. Promote read replica to primary
# 3. Update DNS to point to new primary
# 4. Verify all services working
# 5. Investigate root cause
```

## Performance Tuning

### Database Optimization

```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT ...;

-- Add missing indexes
CREATE INDEX idx_name ON table(column);

-- Update statistics
ANALYZE table_name;
```

### API Optimization

- Enable caching (Redis)
- Use connection pooling
- Optimize database queries
- Implement pagination
- Use CDN for static assets

### Frontend Optimization

- Minify CSS/JS
- Compress images
- Lazy load components
- Use service workers
- Enable gzip compression

## Security Maintenance

### Secret Rotation

```bash
# Rotate JWT secret
# 1. Generate new secret
# 2. Update in KMS/Vault
# 3. Restart API service
# 4. Monitor for issues

# Rotate database password
# 1. Generate new password
# 2. Update in KMS/Vault
# 3. Update database user
# 4. Restart API service
```

### Security Patches

```bash
# Check for vulnerabilities
npm audit
pip check

# Update dependencies
npm update
pip install --upgrade -r requirements.txt

# Run security scans
bandit -r backend/
eslint frontend/
```

---

**Next Steps:**

- [ ] Create detailed runbook for each service
- [ ] Document disaster recovery procedures
- [ ] Create on-call rotation schedule
- [ ] Conduct disaster recovery drill
