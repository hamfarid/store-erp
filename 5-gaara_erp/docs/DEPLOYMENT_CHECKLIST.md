# Gaara ERP Production Deployment Checklist

**Version**: 12.0
**Date**: 2025-12-01
**Environment**: Production

---

## Pre-Deployment Checks

### 1. Security Configuration ✅
- [x] SECRET_KEY set from environment (no hardcoded defaults)
- [x] DEBUG = False in production
- [x] ALLOWED_HOSTS configured
- [x] CSRF protection enabled
- [x] JWT access token TTL = 15 minutes
- [x] JWT refresh token rotation enabled
- [x] Account lockout configured (5 attempts/15 min)
- [x] Rate limiting enabled
- [x] Secure cookie flags (SECURE, HTTPONLY, SAMESITE)
- [x] HTTPS redirect enabled (SECURE_SSL_REDIRECT)
- [x] CSP headers configured
- [x] SQL injection protection (parameterized queries)
- [x] Input validation on all API endpoints

### 2. Environment Variables Required
```bash
# Django
SECRET_KEY=<strong-random-key>
DJANGO_SETTINGS_MODULE=gaara_erp.production_settings

# Database
DB_NAME=gaara_erp_prod
DB_USER=<db_username>
DB_PASSWORD=<db_password>
DB_HOST=<db_host>
DB_PORT=5432

# Redis (Cache/Sessions)
REDIS_HOST=<redis_host>
REDIS_PORT=6379

# Email
EMAIL_HOST=<smtp_host>
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<password>

# AI (Optional)
OPENAI_API_KEY=<key>
LANGFUSE_SECRET_KEY=<key>
LANGFUSE_PUBLIC_KEY=<key>

# Secrets Manager (Choose one)
SECRETS_BACKEND=vault|aws|azure|gcp
VAULT_ADDR=<vault_url>
VAULT_TOKEN=<token>
```

### 3. Database Migration
- [ ] Backup existing database
- [ ] Run `python manage.py migrate --check` (dry run)
- [ ] Run `python manage.py migrate`
- [ ] Verify all migrations applied: `python manage.py showmigrations`
- [ ] Create superuser if needed: `python manage.py createsuperuser`
- [ ] Load initial data if needed: `python manage.py loaddata initial_data.json`

### 4. Static Files
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Verify static files directory exists and is served
- [ ] Configure CDN if applicable

### 5. Cache & Session
- [ ] Redis server running and accessible
- [ ] Cache connection verified
- [ ] Session backend configured

---

## Infrastructure Checklist

### 6. Server Requirements
- [ ] Python 3.11+ installed
- [ ] PostgreSQL 14+ running
- [ ] Redis 6+ running
- [ ] Nginx/Apache configured as reverse proxy
- [ ] SSL certificate installed (Let's Encrypt/commercial)
- [ ] Firewall rules configured

### 7. Docker Deployment (If using Docker)
```bash
# Build images
docker build -t gaara-erp:latest .
docker build -t gaara-erp-api-gateway:latest ./api_gateway

# Run with security flags
docker run --read-only \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  --user 1000:1000 \
  -p 8000:8000 \
  gaara-erp:latest
```

- [ ] Docker images built successfully
- [ ] Non-root user configured
- [ ] Health checks passing
- [ ] Volume mounts configured for logs/media

### 8. Process Manager
- [ ] Gunicorn/uWSGI configured
- [ ] Worker count set appropriately
- [ ] Supervisor/systemd service created
- [ ] Auto-restart on failure enabled

---

## Application Verification

### 9. Health Checks
```bash
# Basic health
curl -f http://localhost:8000/api/health/

# Detailed health
curl -f http://localhost:8000/api/health/detailed/

# Database connectivity
curl -f http://localhost:8000/api/health/db/
```

- [ ] Health endpoint returns 200 OK
- [ ] Database connection verified
- [ ] Redis connection verified
- [ ] External API connections verified (if any)

### 10. Functional Tests
- [ ] Login flow works
- [ ] Create/Read/Update/Delete operations work
- [ ] File upload/download works
- [ ] Email sending works (if configured)
- [ ] AI features work (if configured)

### 11. Performance Baseline
- [ ] Response time < 500ms for common endpoints
- [ ] Database queries optimized (check for N+1)
- [ ] Static files served efficiently
- [ ] Memory usage within limits

---

## Monitoring & Logging

### 12. Logging Configuration
- [ ] Log level set to INFO (or WARNING for production)
- [ ] Log rotation configured
- [ ] Error notifications enabled
- [ ] Audit logging enabled

### 13. Monitoring Setup
- [ ] Application metrics exposed
- [ ] Database metrics monitored
- [ ] Error tracking (Sentry/similar) configured
- [ ] Uptime monitoring configured
- [ ] Alerts configured for critical issues

---

## Backup & Recovery

### 14. Backup Configuration
- [ ] Database backup schedule configured
- [ ] Media files backup configured
- [ ] Backup retention policy set
- [ ] Backup restoration tested
- [ ] Offsite backup enabled

### 15. Disaster Recovery
- [ ] Recovery procedure documented
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined
- [ ] Failover procedure tested (if applicable)

---

## Final Verification

### 16. Pre-Go-Live
- [ ] All tests passing
- [ ] Security scan passed
- [ ] Performance testing completed
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Team trained on deployment procedures

### 17. Go-Live
- [ ] DNS configured/updated
- [ ] SSL certificate verified
- [ ] Application accessible via domain
- [ ] All features working
- [ ] Monitoring active
- [ ] Support team notified

### 18. Post-Deployment
- [ ] Monitor error rates for 24-48 hours
- [ ] Monitor performance metrics
- [ ] Gather user feedback
- [ ] Document any issues found
- [ ] Plan hotfix release if needed

---

## Rollback Procedure

If issues are found post-deployment:

1. **Assess severity** - Can it wait for a hotfix?
2. **Stop traffic** - Put site in maintenance mode
3. **Rollback code** - Deploy previous version
4. **Rollback database** - If migrations were run, restore backup
5. **Verify** - Test basic functionality
6. **Resume traffic** - Remove maintenance mode
7. **Post-mortem** - Document what went wrong

---

## Emergency Contacts

| Role | Contact |
|------|---------|
| DevOps Lead | [Name] |
| Backend Lead | [Name] |
| Database Admin | [Name] |
| Security Team | [Name] |

---

**Deployment Approved By**: _________________ Date: _________

**Deployed By**: _________________ Date: _________

**Verified By**: _________________ Date: _________

