# Gaara ERP - Enterprise Resource Planning System

<div dir="rtl">

# Gaara ERP - نظام إدارة موارد المؤسسات

نظام إدارة موارد المؤسسات الذكي والشامل للمؤسسات الزراعية والتجارية

</div>

## 🚀 Quick Start

### Development

```bash
# Clone repository
git clone <repository-url>
cd Gaara_erp

# Create environment file
cp .env.example .env
# Edit .env with your configuration

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Run migrations
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate

# Create superuser
docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser

# Access application
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin
```

### Production

```bash
# Set environment variables in .env
# Then deploy
./scripts/deploy.sh
```

## 📚 Documentation

- **[Backend Setup Guide](./BACKEND_SETUP.md)** - Complete setup instructions
- **[API Documentation](./API_DOCUMENTATION.md)** - Full API reference
- **[Deployment Guide](./DEPLOYMENT.md)** - Production deployment
- **[Infrastructure Summary](./INFRASTRUCTURE_SUMMARY.md)** - System overview

## 🏗️ Architecture

### Tech Stack

**Backend:**
- Django 4.2+ (Python 3.11+)
- PostgreSQL 15
- Redis 7
- Celery (Background tasks)
- Django REST Framework

**Frontend:**
- React 19
- Vite 6
- TailwindCSS 4
- Radix UI
- shadcn/ui
- Framer Motion
- Recharts

**Infrastructure:**
- Docker & Docker Compose
- Nginx (Reverse proxy)
- Prometheus & Grafana (Monitoring)

## 📦 Modules

- **Core Modules**: Users, Organizations, Permissions, Security
- **Business Modules**: Inventory, Sales, Accounting, Purchasing, Production
- **Agricultural Modules**: Farms, Nurseries, Seed Production, Research
- **Integration Modules**: IoT, AI Analytics, E-commerce
- **Admin Modules**: System Monitoring, Health Monitoring, Database Management

## 🔧 Development

### Running Tests

```bash
# Backend tests
./scripts/run-tests.sh

# API tests
./scripts/api-test.sh

# Health check
./scripts/check-health.sh
```

### Database Management

```bash
# Backup
./docker/database-backup.sh

# Restore
./docker/database-restore.sh backups/backup_file.sql.gz

# Seed data
./scripts/seed-database.sh
```

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| Backend | 8000 | Django API |
| Frontend | 5173 | React Dev Server |
| Database | 5432 | PostgreSQL |
| Redis | 6379 | Cache/Sessions |
| Nginx | 80/443 | Reverse Proxy |
| Prometheus | 9090 | Metrics |
| Grafana | 3001 | Dashboards |

## 🔐 Security

- JWT Authentication
- Role-based Access Control (RBAC)
- CORS Configuration
- Rate Limiting
- SQL Injection Prevention
- XSS Protection
- CSRF Protection

## 📊 Monitoring

```bash
# Start monitoring stack
docker-compose -f monitoring/docker-compose.monitoring.yml up -d

# Access Grafana
# http://localhost:3001 (admin/admin)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

MIT License

## 📞 Support

- **Email**: support@gaara-erp.com
- **Documentation**: See `/docs` directory
- **Issues**: GitHub Issues

---

**Version**: 1.0.0  
**Last Updated**: 2025-01-15
