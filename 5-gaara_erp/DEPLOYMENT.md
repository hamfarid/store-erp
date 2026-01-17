# Gaara ERP - Deployment Guide

## 🚀 Production Deployment

### Prerequisites

- Docker & Docker Compose installed
- Domain name configured (for production)
- SSL certificates (for HTTPS)
- Backup strategy in place
- Monitoring setup

### Pre-Deployment Checklist

- [ ] All environment variables configured in `.env`
- [ ] Database backups created
- [ ] SSL certificates obtained
- [ ] Domain DNS configured
- [ ] Firewall rules configured
- [ ] Monitoring tools set up
- [ ] Backup scripts tested

### Deployment Steps

#### 1. Prepare Environment

```bash
# Clone repository
git clone <repository-url>
cd Gaara_erp

# Create .env file
cp .env.example .env
# Edit .env with production values

# Generate secure keys
openssl rand -hex 32  # For SECRET_KEY
openssl rand -hex 32  # For ENCRYPTION_KEY
```

#### 2. Run Deployment Script

```bash
# Make script executable
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh
```

Or manually:

```bash
# Build and start
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

#### 3. Verify Deployment

```bash
# Check health
curl http://localhost:8000/health/

# Check logs
docker-compose logs -f backend

# Check all services
docker-compose ps
```

### Post-Deployment

#### 1. Create Admin User

```bash
docker-compose exec backend python manage.py createsuperuser
```

#### 2. Configure Nginx (if not using Docker)

Update nginx configuration with your domain and SSL certificates.

#### 3. Set Up Monitoring

```bash
# Start monitoring stack
docker-compose -f monitoring/docker-compose.monitoring.yml up -d

# Access Grafana
# http://your-domain:3001
# Default credentials: admin/admin
```

#### 4. Set Up Backups

```bash
# Create backup
./scripts/backup-all.sh

# Schedule automated backups (crontab)
0 2 * * * /path/to/scripts/backup-all.sh
```

### Backup & Restore

#### Backup

```bash
# Complete backup (database + media + config)
./scripts/backup-all.sh

# Database only
./docker/database-backup.sh
```

#### Restore

```bash
# Restore database
./docker/database-restore.sh backups/backup_file.sql.gz

# Restore from complete backup
tar -xzf backups/gaara_erp_backup_YYYYMMDD_HHMMSS.tar.gz
# Follow restore instructions in manifest.txt
```

### Monitoring

#### Prometheus

- **URL**: http://your-domain:9090
- **Metrics**: System, application, and database metrics

#### Grafana

- **URL**: http://your-domain:3001
- **Default Login**: admin/admin
- **Dashboards**: Pre-configured for Gaara ERP

### Scaling

#### Horizontal Scaling

```bash
# Scale backend workers
docker-compose up -d --scale backend=3

# Scale Celery workers
docker-compose up -d --scale celery=4
```

#### Load Balancer

Configure Nginx as load balancer:

```nginx
upstream backend {
    least_conn;
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

### Maintenance

#### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate
```

#### Database Maintenance

```bash
# Vacuum database
docker-compose exec db psql -U gaara_admin -d gaara_erp -c "VACUUM ANALYZE;"

# Check database size
docker-compose exec db psql -U gaara_admin -d gaara_erp -c "\l+"
```

### Troubleshooting

#### Service Won't Start

```bash
# Check logs
docker-compose logs backend

# Check database connection
docker-compose exec backend python manage.py dbshell

# Check environment variables
docker-compose exec backend env | grep -E "DATABASE|SECRET"
```

#### Performance Issues

```bash
# Check resource usage
docker stats

# Check database queries
docker-compose exec backend python manage.py shell
# Then use Django debug toolbar or query logging
```

#### Backup Issues

```bash
# Test backup script
./docker/database-backup.sh

# Check disk space
df -h

# Check backup directory permissions
ls -la backups/
```

### Security Checklist

- [ ] All default passwords changed
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` configured
- [ ] SSL/TLS enabled
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Database backups encrypted
- [ ] Access logs monitored
- [ ] Regular security updates applied
- [ ] Firewall rules configured

### Rollback Procedure

```bash
# Stop current deployment
docker-compose down

# Restore from backup
./docker/database-restore.sh backups/backup_before_update.sql.gz

# Start previous version
git checkout <previous-commit>
docker-compose build
docker-compose up -d
```

---

**Last Updated**: 2025-01-15  
**Version**: 1.0.0
