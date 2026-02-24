# Production Deployment Checklist

## Pre-Deployment Verification

### Code Quality & Testing
- [ ] All unit tests passing locally
- [ ] Code coverage meets minimum threshold (80%)
- [ ] No linting errors (Flake8 for Python, ESLint for JavaScript)
- [ ] Code formatting verified (Black for Python)
- [ ] Security scan completed (Trivy)
- [ ] No critical vulnerabilities detected
- [ ] All CI/CD pipeline checks passing on GitHub Actions

### Backend Verification
- [ ] Database migrations validated
- [ ] All new endpoints documented in API documentation
- [ ] Authentication/authorization tests passing
- [ ] API response format standardized
- [ ] Error handling properly implemented
- [ ] Logging configured for production
- [ ] Environment variables documented
- [ ] Database backups scheduled

### Frontend Verification
- [ ] Build completes without errors
- [ ] All pages render correctly
- [ ] Navigation flows working as expected
- [ ] Form validations working
- [ ] Mobile responsiveness tested
- [ ] Cross-browser testing completed
- [ ] Performance metrics acceptable

### Security Checklist
- [ ] All secrets properly configured in GitHub
- [ ] No hardcoded credentials in code
- [ ] SSL/TLS certificates valid
- [ ] CORS policies properly configured
- [ ] Rate limiting enabled
- [ ] CSRF protection enabled
- [ ] Security headers configured
- [ ] Input validation implemented
- [ ] SQL injection prevention verified

## Production Configuration

### GitHub Secrets Setup
Before deploying to production, configure these secrets in GitHub:

```
Production Backend Secrets:
- PROD_DATABASE_URL          # Production database connection
- PROD_SECRET_KEY            # Flask secret key
- PROD_JWT_SECRET            # JWT signing key
- PROD_MAIL_SERVER           # Email server address
- PROD_MAIL_USERNAME         # Email credentials
- PROD_MAIL_PASSWORD         # Email password
- PROD_AWS_ACCESS_KEY_ID     # AWS credentials (if using S3)
- PROD_AWS_SECRET_ACCESS_KEY # AWS secret key
- PROD_SENTRY_DSN            # Error tracking (optional)

Production Frontend Secrets:
- PROD_API_URL               # Production API endpoint
- PROD_AUTH_DOMAIN           # Authentication domain
- PROD_STRIPE_PUBLIC_KEY     # Stripe public key (if applicable)

Deployment Secrets:
- PROD_DEPLOY_KEY            # SSH key for deployment
- PROD_REGISTRY_USERNAME     # Container registry username
- PROD_REGISTRY_PASSWORD     # Container registry password
```

### Environment Configuration
- [ ] Update `.env.production` with production values
- [ ] Database connection string verified
- [ ] API endpoints pointing to production servers
- [ ] Logging level set to INFO or higher
- [ ] Debug mode disabled
- [ ] CORS origins properly restricted

## Deployment Process

### Pre-Deployment Tasks
1. **Backup Existing Data**
   ```bash
   python create_backup.py --backup-dir backups --manifest
   # Upload backup to secure storage
   ```

2. **Database Backup**
   ```bash
   # Create database dump
   pg_dump production_db > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

3. **Tag Release**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

### Deployment Steps
1. **Docker Image Build & Push**
   - Triggered automatically via CI/CD pipeline
   - Wait for all tests to pass
   - Verify images are pushed to registry

2. **Database Migrations**
   ```bash
   # Run migrations on production database
   flask db upgrade
   ```

3. **Deploy Backend**
   ```bash
   # Pull latest image and restart
   docker pull ghcr.io/hamfarid/store-erp/backend:main
   docker-compose -f docker-compose.prod.yml up -d backend
   ```

4. **Deploy Frontend**
   ```bash
   # Pull latest image and restart
   docker pull ghcr.io/hamfarid/store-erp/frontend:main
   docker-compose -f docker-compose.prod.yml up -d frontend
   ```

5. **Health Checks**
   ```bash
   # Verify backend health
   curl https://api.production.com/health
   
   # Verify frontend is loading
   curl https://production.com
   ```

## Post-Deployment Verification

### Smoke Tests
- [ ] Frontend loads without errors
- [ ] Login functionality working
- [ ] User can navigate to main pages
- [ ] Backend API responding
- [ ] Database queries executing
- [ ] Authentication tokens valid

### Performance Monitoring
- [ ] API response times within SLA
- [ ] Database query performance acceptable
- [ ] Memory usage normal
- [ ] CPU usage normal
- [ ] Disk space available
- [ ] No error spikes in logs

### Monitoring & Alerts
- [ ] Prometheus scraping metrics
- [ ] Grafana dashboards displaying data
- [ ] Alert rules configured and active
- [ ] Error notifications being sent
- [ ] Performance notifications being sent
- [ ] Uptime monitoring active

## Rollback Procedure

If critical issues are detected:

### Quick Rollback Steps
1. **Identify Issue**
   ```bash
   # Check logs
   docker logs backend_container
   docker logs frontend_container
   ```

2. **Rollback Backend**
   ```bash
   # Use previous image tag
   docker pull ghcr.io/hamfarid/store-erp/backend:previous-tag
   docker-compose -f docker-compose.prod.yml up -d backend
   ```

3. **Rollback Frontend**
   ```bash
   docker pull ghcr.io/hamfarid/store-erp/frontend:previous-tag
   docker-compose -f docker-compose.prod.yml up -d frontend
   ```

4. **Rollback Database** (if needed)
   ```bash
   # Restore from backup if migrations caused issues
   psql production_db < backup_file.sql
   ```

5. **Verify Rollback**
   ```bash
   curl https://api.production.com/health
   curl https://production.com
   ```

## Post-Deployment Documentation

- [ ] Release notes updated
- [ ] Deployment summary documented
- [ ] Any issues logged as GitHub issues
- [ ] Performance impact assessed
- [ ] Changes documented in wiki/docs
- [ ] Team notified of deployment
- [ ] Stakeholders notified if relevant

## Scheduled Maintenance

### Daily Tasks
- [ ] Monitor error logs
- [ ] Check backup completion
- [ ] Verify uptime
- [ ] Monitor resource usage

### Weekly Tasks
- [ ] Review performance metrics
- [ ] Check security logs
- [ ] Test backup restore procedure
- [ ] Review and update runbooks

### Monthly Tasks
- [ ] Update dependencies
- [ ] Security audit
- [ ] Database optimization
- [ ] Performance analysis
- [ ] Capacity planning

## Emergency Contacts

- **DevOps Lead**: [Name & Contact]
- **Security Team**: [Name & Contact]
- **Database Admin**: [Name & Contact]
- **On-call Support**: [Contact Info]

## Useful Commands

```bash
# View deployment status
kubectl rollout status deployment/backend
kubectl rollout status deployment/frontend

# View logs
kubectl logs -f deployment/backend
kubectl logs -f deployment/frontend

# Scale replicas
kubectl scale deployment backend --replicas=3

# Force restart
kubectl rollout restart deployment/backend

# Get pod information
kubectl get pods -n production
kubectl describe pod <pod-name> -n production
```

---

Last Updated: [Date]
Updated By: [Name]
