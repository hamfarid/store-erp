# 🚀 Deployment Checklist

## Pre-Deployment

### Code Quality
- [ ] All tests passing (backend & frontend)
- [ ] Code review completed and approved
- [ ] No merge conflicts with main branch
- [ ] Linting passes without errors
- [ ] Security scan completed (no critical vulnerabilities)
- [ ] Code coverage meets threshold (>80%)

### Documentation
- [ ] CHANGELOG.md updated with new features/fixes
- [ ] API documentation updated (if API changes)
- [ ] README.md updated (if setup changed)
- [ ] Migration guides written (for breaking changes)

### Database
- [ ] Database migrations created and tested
- [ ] Migration rollback tested successfully
- [ ] Database backup completed
- [ ] Migration scripts reviewed for performance impact
- [ ] Indexes added for new queries
- [ ] Data validation scripts prepared

### Configuration
- [ ] Environment variables documented
- [ ] Secrets rotated (if needed)
- [ ] Feature flags configured
- [ ] Rate limits reviewed and adjusted
- [ ] CORS settings verified
- [ ] SSL certificates valid (>30 days)

### Dependencies
- [ ] All dependencies up to date
- [ ] No known security vulnerabilities
- [ ] License compliance checked
- [ ] Third-party service status verified

## Deployment Phase

### Backup & Safety
- [ ] Full database backup created
- [ ] Application files backed up
- [ ] Redis data backed up (if applicable)
- [ ] Previous deployment tagged in git
- [ ] Rollback plan documented and ready

### Infrastructure
- [ ] Server resources sufficient (CPU, RAM, Disk)
- [ ] Load balancer configured correctly
- [ ] CDN cache cleared (if needed)
- [ ] DNS records verified
- [ ] Firewall rules updated (if needed)

### Deployment Execution
- [ ] Maintenance mode enabled (if needed)
- [ ] Traffic redirected to staging
- [ ] Database migrations executed
- [ ] Docker images built and pushed
- [ ] Containers deployed to production
- [ ] Configuration files updated
- [ ] Static assets deployed to CDN

### Monitoring Setup
- [ ] Prometheus scraping targets updated
- [ ] Grafana dashboards verified
- [ ] Alert rules enabled
- [ ] Log aggregation working
- [ ] APM/Tracing configured
- [ ] Error tracking service connected

## Post-Deployment

### Verification (First 5 minutes)
- [ ] Health check endpoints responding
- [ ] Application accessible via URL
- [ ] Login/authentication working
- [ ] Database connectivity verified
- [ ] Redis connectivity verified
- [ ] File uploads working
- [ ] Email notifications working

### Smoke Tests (First 15 minutes)
- [ ] Critical user flows tested
  - [ ] User registration
  - [ ] User login
  - [ ] Farm creation
  - [ ] Diagnosis submission
  - [ ] Report generation
  - [ ] Image upload
  - [ ] Data export
- [ ] API endpoints responding correctly
- [ ] Scheduled tasks running
- [ ] Background jobs processing

### Monitoring (First Hour)
- [ ] Error rates normal (<1%)
- [ ] Response times acceptable (<500ms p95)
- [ ] CPU usage normal (<70%)
- [ ] Memory usage stable
- [ ] Database queries performing well
- [ ] No unexpected 500 errors
- [ ] No memory leaks detected
- [ ] Cache hit rates acceptable

### Performance Checks
- [ ] Page load times <3 seconds
- [ ] API response times <500ms
- [ ] Database query times optimized
- [ ] CDN delivery working
- [ ] Image optimization working
- [ ] Compression enabled

### Security Verification
- [ ] HTTPS enforced
- [ ] Security headers present
- [ ] CSRF protection active
- [ ] XSS protection enabled
- [ ] SQL injection protection working
- [ ] Rate limiting functional
- [ ] Authentication tokens valid

## Communication

### Team Notification
- [ ] Deploy notification sent to team
- [ ] Release notes shared
- [ ] Known issues documented
- [ ] Support team briefed
- [ ] Stakeholders informed

### User Communication (if needed)
- [ ] Maintenance window communicated
- [ ] New features announced
- [ ] Known issues disclosed
- [ ] Help documentation updated

## Rollback Criteria

Rollback immediately if:
- [ ] Error rate >5% for 5 minutes
- [ ] Response time p95 >2 seconds
- [ ] Critical functionality broken
- [ ] Database corruption detected
- [ ] Security vulnerability discovered
- [ ] Data loss occurring

## Post-Deployment Tasks (Within 24 hours)

### Monitoring Review
- [ ] Review all metrics dashboards
- [ ] Check error logs for patterns
- [ ] Analyze performance metrics
- [ ] Review user feedback/complaints
- [ ] Check third-party service usage

### Optimization
- [ ] Identify performance bottlenecks
- [ ] Review database query performance
- [ ] Check cache effectiveness
- [ ] Analyze CDN usage
- [ ] Review API usage patterns

### Documentation
- [ ] Update deployment log
- [ ] Document any issues encountered
- [ ] Note any manual interventions
- [ ] Update runbook if needed
- [ ] Share lessons learned

## Long-term Monitoring (First Week)

- [ ] Daily error rate review
- [ ] User adoption metrics
- [ ] Performance trend analysis
- [ ] Resource utilization review
- [ ] Cost impact assessment
- [ ] User feedback collection

## Cleanup (After Successful Deployment)

- [ ] Remove old Docker images
- [ ] Clean up old logs
- [ ] Archive old backups
- [ ] Update documentation
- [ ] Close related issues/tickets

---

## Emergency Contacts

| Role | Name | Contact |
|------|------|---------|
| Lead Developer | - | - |
| DevOps Engineer | - | - |
| Database Admin | - | - |
| Security Lead | - | - |
| Product Manager | - | - |

## Useful Commands

### Quick Rollback
```bash
# Using workflow
gh workflow run rollback.yml -f environment=production -f version=<TAG>

# Manual rollback
kubectl rollout undo deployment/backend
kubectl rollout undo deployment/frontend
```

### Check Status
```bash
# Kubernetes
kubectl get pods
kubectl logs -f deployment/backend

# Docker
docker ps
docker logs -f gaara_backend

# Database
psql $DATABASE_URL -c "SELECT version();"
```

### Health Checks
```bash
curl https://api.example.com/health
curl https://example.com
```

---

**Last Updated:** 2026-01-31  
**Template Version:** 2.0
