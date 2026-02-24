# Complete Inventory Management System - Docker Setup

## 🚀 Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd complete_inventory_system/backend
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Build and Run
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Check status
docker-compose ps
```

### 4. Access the Application
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health
- **Database**: localhost:5432
- **Redis**: localhost:6379

## 📁 File Structure

```
backend/
├── Dockerfile                 # Multi-stage production Dockerfile
├── docker-compose.yml         # Complete service orchestration
├── requirements_final.txt     # Consolidated dependencies
├── app.py                     # Main application entry point
├── .dockerignore              # Docker build optimization
├── src/                       # Source code
├── logs/                      # Application logs
├── uploads/                   # File uploads
├── reports/                   # Generated reports
└── backups/                   # Database backups
```

## 🔧 Configuration

### Environment Variables
```bash
# Application
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database
DATABASE_URL=postgresql://inventory_user:inventory_pass@postgres:5432/inventory_db

# Redis
REDIS_URL=redis://redis:6379/0

# Build Arguments
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
VERSION=1.0.0
VCS_REF=$(git rev-parse --short HEAD)
```

## 🐳 Docker Commands

### Development
```bash
# Start development environment
docker-compose -f docker-compose.yml up backend_dev

# Run tests
docker-compose run --rm backend pytest

# Access container shell
docker-compose exec backend sh

# View real-time logs
docker-compose logs -f backend
```

### Production
```bash
# Build production image
docker build -t inventory-backend:latest .

# Run production container
docker run -d \
  --name inventory-backend \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  inventory-backend:latest

# Scale services
docker-compose up -d --scale backend=3
```

### Maintenance
```bash
# Update services
docker-compose pull
docker-compose up -d

# Backup database
docker-compose exec postgres pg_dump -U inventory_user inventory_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U inventory_user inventory_db < backup.sql

# Clean up
docker-compose down -v
docker system prune -a
```

## 📊 Monitoring

### Health Checks
```bash
# Check application health
curl http://localhost:5000/api/health

# Check all services
docker-compose ps
```

### Logs
```bash
# Application logs
docker-compose logs backend

# Database logs
docker-compose logs postgres

# All services
docker-compose logs
```

## 🔒 Security

### Production Checklist
- [ ] Change default passwords
- [ ] Use environment variables for secrets
- [ ] Enable SSL/TLS
- [ ] Configure firewall rules
- [ ] Set up log monitoring
- [ ] Enable backup automation

### SSL Configuration
```bash
# Generate SSL certificates
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/nginx.key \
  -out nginx/ssl/nginx.crt
```

## 🚨 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find process using port
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Database Connection Failed**
```bash
# Check database status
docker-compose logs postgres
# Restart database
docker-compose restart postgres
```

**Build Failures**
```bash
# Clean build cache
docker builder prune -a
# Rebuild without cache
docker-compose build --no-cache
```

**Permission Issues**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod -R 755 .
```

## 📈 Performance Optimization

### Production Tuning
```bash
# Increase worker processes
docker-compose up -d --scale backend=4

# Optimize database
docker-compose exec postgres psql -U inventory_user -d inventory_db -c "VACUUM ANALYZE;"

# Monitor resources
docker stats
```

### Memory Limits
```yaml
# In docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

## 🔄 Updates

### Application Updates
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose build backend
docker-compose up -d backend
```

### Dependency Updates
```bash
# Update requirements
pip-compile requirements_final.txt

# Rebuild image
docker-compose build --no-cache backend
```

## 📞 Support

For issues and questions:
- Check logs: `docker-compose logs`
- Review health status: `curl http://localhost:5000/api/health`
- Restart services: `docker-compose restart`
