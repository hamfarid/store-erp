# 🚀 Store ERP - Production Deployment Guide

Complete guide for deploying Store ERP to production server with monitoring.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Configuration](#configuration)
- [Monitoring Setup](#monitoring-setup)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)

---

## 🔧 Prerequisites

### System Requirements

- **OS**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows Server
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 20GB minimum free space
- **CPU**: 2 cores minimum, 4 cores recommended

### Required Software

1. **Docker** (20.10+)
   ```bash
   # Linux
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # macOS
   # Download Docker Desktop from https://www.docker.com/products/docker-desktop
   ```

2. **Docker Compose** (2.0+)
   ```bash
   # Linux
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   
   # Verify
   docker-compose --version
   ```

3. **Git**
   ```bash
   sudo apt-get install git  # Ubuntu/Debian
   brew install git          # macOS
   ```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/hamfarid/Store.git
cd Store

# Checkout the verified branch
git checkout test/ci-cd-verification
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (IMPORTANT!)
nano .env  # or vim .env, or use any text editor
```

**Required Changes in `.env`:**
```bash
# Generate secure keys with:
python -c "import secrets; print(secrets.token_hex(32))"

# Update these values:
DB_PASSWORD=your_secure_database_password_here
REDIS_PASSWORD=your_secure_redis_password_here
SECRET_KEY=generated_secret_key_here
JWT_SECRET_KEY=generated_jwt_secret_here
SECURITY_PASSWORD_SALT=generated_salt_here
GRAFANA_PASSWORD=your_secure_grafana_password
```

### 3. Start All Services

**Linux/macOS:**
```bash
# Make scripts executable
chmod +x start-all.sh stop-all.sh start-dev.sh

# Start production with monitoring
./start-all.sh

# Or start without monitoring
./start-all.sh --no-monitoring
```

**Windows:**
```cmd
REM Start production with monitoring
start-all.bat

REM Or start without monitoring
start-all.bat --no-monitoring
```

### 4. Verify Deployment

Wait 30-60 seconds for services to initialize, then access:

- **Frontend**: http://your-server-ip
- **Backend API**: http://your-server-ip:5001/api
- **Health Check**: http://your-server-ip:5001/health
- **Grafana**: http://your-server-ip:3000 (credentials: admin / your_grafana_password)
- **Prometheus**: http://your-server-ip:9090

---

## 📖 Detailed Setup

### Step 1: Server Preparation

```bash
# Update system (Ubuntu/Debian)
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y \
    curl \
    git \
    ca-certificates \
    gnupg \
    lsb-release

# Set timezone
sudo timedatectl set-timezone Africa/Cairo  # or your timezone
```

### Step 2: Configure Firewall

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 3000/tcp    # Grafana (optional, can restrict)
sudo ufw allow 9090/tcp    # Prometheus (optional, can restrict)
sudo ufw enable

# Verify
sudo ufw status
```

### Step 3: SSL Certificate (Optional but Recommended)

```bash
# Install Certbot
sudo apt-get install certbot

# Get SSL certificate (requires domain)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificates will be at: /etc/letsencrypt/live/yourdomain.com/
```

Update `nginx/nginx.conf` to use SSL certificates.

### Step 4: Deploy Application

Follow [Quick Start](#quick-start) steps 1-4.

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` file for all configuration:

```bash
# === Core Settings ===
FLASK_ENV=production           # production | development
FLASK_DEBUG=0                  # 0 = disabled, 1 = enabled

# === Database ===
DB_NAME=store_production       # Database name
DB_USER=store_user            # Database username
DB_PASSWORD=***               # Strong password (16+ chars)
DB_HOST=database              # Container name or IP
DB_PORT=5432                  # PostgreSQL port

# === Redis Cache ===
REDIS_PASSWORD=***            # Strong password
REDIS_HOST=redis              # Container name or IP
REDIS_PORT=6379               # Redis port

# === Security ===
SECRET_KEY=***                # 64+ character hex string
JWT_SECRET_KEY=***            # 64+ character hex string
SECURITY_PASSWORD_SALT=***    # 32+ character hex string

# === Email (for notifications) ===
MAIL_SERVER=smtp.gmail.com    # SMTP server
MAIL_PORT=587                 # SMTP port
MAIL_USE_TLS=true            # Use TLS
MAIL_USERNAME=***            # Email address
MAIL_PASSWORD=***            # App password (not email password)

# === Monitoring ===
GRAFANA_PASSWORD=***          # Grafana admin password

# === Performance ===
WORKERS=4                     # Gunicorn workers (2-4 × CPU cores)
THREADS=2                     # Threads per worker
TIMEOUT=120                   # Request timeout (seconds)

# === Logging ===
LOG_LEVEL=INFO               # DEBUG | INFO | WARNING | ERROR
LOG_FORMAT=json              # json | text
```

### Docker Compose Files

- **`docker-compose.prod.yml`**: Production services (default)
- **`docker-compose.yml`**: Development services
- **`docker-compose.monitoring.yml`**: Monitoring stack (Prometheus, Grafana, Loki)

---

## 📊 Monitoring Setup

### Access Monitoring Tools

1. **Grafana** (http://your-server:3000)
   - Login: `admin` / `your_grafana_password`
   - Pre-configured dashboards for system and application metrics

2. **Prometheus** (http://your-server:9090)
   - Metrics database and query interface
   - View raw metrics and create custom queries

3. **Loki** (http://your-server:3100)
   - Log aggregation system
   - Access via Grafana Explore

### Default Dashboards

Grafana includes pre-configured dashboards:

- **System Overview**: CPU, RAM, Disk, Network
- **Application Metrics**: Request rates, response times, errors
- **Database Performance**: Query times, connections, cache hit rates
- **Container Health**: Resource usage per container

### Custom Alerts

To set up alerts in Grafana:

1. Navigate to Alerting → Alert rules
2. Create new alert rule
3. Define conditions (e.g., CPU > 80%, Memory > 90%)
4. Configure notification channels (email, Slack, etc.)

---

## 🔄 Maintenance

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 backend

# Since timestamp
docker-compose -f docker-compose.prod.yml logs --since 2024-01-01T00:00:00
```

### Restart Services

```bash
# Restart all
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend

# Restart with rebuild
docker-compose -f docker-compose.prod.yml up -d --build backend
```

### Update Application

```bash
# Pull latest changes
git pull origin test/ci-cd-verification

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Or use script with rebuild flag
./start-all.sh --rebuild
```

### Database Backup

```bash
# Manual backup
docker-compose -f docker-compose.prod.yml exec database pg_dump -U store_user store_production > backup_$(date +%Y%m%d).sql

# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T database psql -U store_user store_production < backup_20250113.sql
```

### Clean Up

```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -a -f

# Remove unused volumes (CAREFUL!)
docker volume prune -f

# Clean everything (VERY CAREFUL!)
docker system prune -a --volumes -f
```

---

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check container status
docker ps -a

# View specific container logs
docker logs store_backend_prod

# Check for port conflicts
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5001

# Restart Docker daemon
sudo systemctl restart docker
```

### Database Connection Issues

```bash
# Check database health
docker-compose -f docker-compose.prod.yml exec database pg_isready -U store_user

# Connect to database
docker-compose -f docker-compose.prod.yml exec database psql -U store_user store_production

# Check connections
SELECT * FROM pg_stat_activity;
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Check disk space
df -h

# Check memory
free -m

# Check CPU
top
htop  # if installed
```

### SSL Certificate Issues

```bash
# Renew Let's Encrypt certificates
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run

# Reload Nginx after renewal
docker-compose -f docker-compose.prod.yml restart nginx
```

### argon2-cffi Not Available

```bash
# Install in virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate.bat  # Windows

pip install argon2-cffi==23.1.0

# Verify installation
python -c "import argon2; print(argon2.__version__)"
```

---

## 🔒 Security Best Practices

### 1. Change Default Passwords

```bash
# Generate strong passwords
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update in .env file
DB_PASSWORD=generated_password
REDIS_PASSWORD=generated_password
GRAFANA_PASSWORD=generated_password
```

### 2. Restrict Network Access

```bash
# Only allow specific IPs to monitoring tools
sudo ufw allow from YOUR_IP_ADDRESS to any port 3000  # Grafana
sudo ufw allow from YOUR_IP_ADDRESS to any port 9090  # Prometheus

# Or use nginx proxy with authentication
```

### 3. Enable HTTPS

- Use Let's Encrypt for free SSL certificates
- Update nginx configuration to redirect HTTP to HTTPS
- Set `SESSION_COOKIE_SECURE=true` in `.env`

### 4. Regular Updates

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Update Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Backup Strategy

- **Database**: Daily automated backups
- **Uploads**: Regular file system backups
- **Configuration**: Keep `.env` and configs in secure location
- **Test restores**: Verify backups work regularly

### 6. Monitor Logs

```bash
# Set up log rotation
sudo nano /etc/logrotate.d/docker-containers

# Check for suspicious activity
docker-compose -f docker-compose.prod.yml logs | grep -i error
docker-compose -f docker-compose.prod.yml logs | grep -i warning
```

---

## 📞 Support & Resources

### Documentation

- **API Documentation**: http://your-server:5001/api
- **GitHub Repository**: https://github.com/hamfarid/Store
- **Issue Tracker**: https://github.com/hamfarid/Store/issues

### Useful Commands Cheat Sheet

```bash
# Start services
./start-all.sh                    # Production + monitoring
./start-all.sh --no-monitoring    # Production only
./start-all.sh --dev              # Development mode
./start-dev.sh                    # Development (no Docker)

# Stop services
./stop-all.sh                     # Stop all services
docker-compose down -v            # Stop and remove volumes

# View logs
docker-compose logs -f [service]  # Follow logs
docker-compose logs --tail=100    # Last 100 lines

# Execute commands in containers
docker-compose exec backend sh    # Backend shell
docker-compose exec database psql # Database shell

# Health checks
curl http://localhost:5001/health # Backend health
docker ps --filter "health=healthy" # Healthy containers
```

### System Information

```bash
# Check versions
docker --version
docker-compose --version
python --version

# Check services
docker-compose ps
docker-compose top

# Check networks
docker network ls
docker network inspect store_network

# Check volumes
docker volume ls
docker volume inspect store_postgres_data
```

---

## ✅ Deployment Checklist

Before going to production, verify:

- [ ] `.env` file configured with secure passwords
- [ ] Firewall rules configured
- [ ] SSL certificate installed (if using domain)
- [ ] Database backup strategy in place
- [ ] Monitoring dashboards accessible
- [ ] Email notifications configured
- [ ] Log rotation configured
- [ ] Health checks passing
- [ ] Performance tested under load
- [ ] Documentation reviewed
- [ ] Team trained on operations

---

## 🎉 Success!

Your Store ERP system is now deployed and running!

**Default Access:**
- Frontend: http://your-server
- Backend: http://your-server:5001
- Monitoring: http://your-server:3000

**Next Steps:**
1. Create admin user
2. Configure system settings
3. Set up automated backups
4. Configure monitoring alerts
5. Train users

---

**Last Updated**: 2025-11-13  
**Version**: 1.0.0  
**Branch**: test/ci-cd-verification
