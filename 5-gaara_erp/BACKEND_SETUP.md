# Gaara ERP - Backend Setup Guide

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Git
- 8GB+ RAM recommended
- 20GB+ free disk space

### Development Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Gaara_erp
   ```

2. **Create environment file**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start development environment**

   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. **Run migrations**

   ```bash
   docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser
   ```

6. **Access the application**
   - Frontend: <http://localhost:5173> (Vite dev server)
   - Frontend Preview: <http://localhost:4173>
   - Backend API: <http://localhost:8000>
   - API Docs: <http://localhost:8000/api/docs/>
   - Admin Panel: <http://localhost:8000/admin>

### Production Setup

1. **Set environment variables**

   ```bash
   # Generate secure keys
   openssl rand -hex 32  # For SECRET_KEY
   openssl rand -hex 32  # For ENCRYPTION_KEY
   ```

2. **Update .env file**

   ```bash
   SECRET_KEY=<generated-secret-key>
   ENCRYPTION_KEY=<generated-encryption-key>
   POSTGRES_PASSWORD=<strong-password>
   DEBUG=false
   ```

3. **Start production environment**

   ```bash
   docker-compose up -d
   ```

4. **Run migrations**

   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Collect static files**

   ```bash
   docker-compose exec backend python manage.py collectstatic --noinput
   ```

## 📁 Project Structure

```
Gaara_erp/
├── gaara_erp/              # Django backend
│   ├── gaara_erp/          # Main project settings
│   ├── core_modules/       # Core functionality
│   ├── business_modules/   # Business logic
│   ├── agricultural_modules/ # Agricultural features
│   ├── integration_modules/ # Third-party integrations
│   └── manage.py
├── gaara-erp-frontend/     # React frontend
├── docker/                 # Docker scripts
│   ├── init-db.sql
│   ├── docker-entrypoint.sh
│   ├── database-backup.sh
│   └── database-restore.sh
├── docker-compose.yml      # Production
├── docker-compose.dev.yml  # Development
├── Dockerfile              # Backend Dockerfile
└── .env.example           # Environment template
```

## 🗄️ Database

### PostgreSQL Configuration

- **Default Database**: `gaara_erp`
- **Default User**: `gaara_admin`
- **Port**: `5432`
- **Timezone**: `Asia/Riyadh`
- **Encoding**: `UTF8`

### Database Backup

```bash
# Manual backup
docker-compose exec db pg_dump -U gaara_admin gaara_erp > backup.sql

# Using backup script
./docker/database-backup.sh
```

### Database Restore

```bash
# Using restore script
./docker/database-restore.sh backups/gaara_erp_backup_20240101_120000.sql.gz
```

## 🔧 Development Commands

### Django Management

```bash
# Run migrations
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate

# Create migrations
docker-compose -f docker-compose.dev.yml exec backend python manage.py makemigrations

# Create superuser
docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser

# Django shell
docker-compose -f docker-compose.dev.yml exec backend python manage.py shell

# Run tests
docker-compose -f docker-compose.dev.yml exec backend python manage.py test
```

### Docker Commands

```bash
# View logs
docker-compose -f docker-compose.dev.yml logs -f backend

# Restart service
docker-compose -f docker-compose.dev.yml restart backend

# Stop all services
docker-compose -f docker-compose.dev.yml down

# Remove volumes (⚠️ deletes data)
docker-compose -f docker-compose.dev.yml down -v
```

## 🔐 Security

### Environment Variables

Never commit `.env` file. Always use `.env.example` as template.

### Required Secrets

- `SECRET_KEY`: Django secret key (generate with `openssl rand -hex 32`)
- `ENCRYPTION_KEY`: For encrypting sensitive data
- `POSTGRES_PASSWORD`: Strong database password

### Production Checklist

- [ ] Change all default passwords
- [ ] Set `DEBUG=false`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL/TLS certificates
- [ ] Configure secure cookies
- [ ] Set up proper backup strategy
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set up monitoring and logging

## 📊 Services

### Backend (Django)

- **Port**: 8000
- **Health Check**: <http://localhost:8000/health/>
- **Admin**: <http://localhost:8000/admin>

### Frontend (React/Vite)

- **Port**: 5173 (dev) / 80 (prod)
- **Preview Port**: 4173 (dev preview)
- **Health Check**: <http://localhost/health>

### Database (PostgreSQL)

- **Port**: 5432
- **User**: gaara_admin
- **Database**: gaara_erp

### Cache (Redis)

- **Port**: 6379
- **Purpose**: Session storage, caching, Celery broker

### Celery Worker

- **Purpose**: Background task processing
- **Concurrency**: 4 workers (production)

### Celery Beat

- **Purpose**: Scheduled tasks
- **Frequency**: Configurable via Django settings

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check database status
docker-compose ps db

# View database logs
docker-compose logs db

# Test connection
docker-compose exec backend python manage.py dbshell
```

### Migration Issues

```bash
# Reset migrations (⚠️ use with caution)
docker-compose exec backend python manage.py migrate --fake-initial

# Show migration status
docker-compose exec backend python manage.py showmigrations
```

### Port Conflicts

If ports are already in use:

```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x docker/*.sh
```

## 📚 API Documentation

API documentation is available at:

- **Swagger UI**: <http://localhost:8000/api/docs/>
- **ReDoc**: <http://localhost:8000/api/redoc/>
- **Full API Docs**: See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## 🔄 Updates

### Update Dependencies

```bash
# Backend
docker-compose exec backend pip install --upgrade -r requirements.txt

# Frontend
cd gaara-erp-frontend
npm update
```

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose build

# Restart services
docker-compose up -d
```

## 📞 Support

For issues and questions:

- Check logs: `docker-compose logs`
- Review documentation in `/docs`
- Open an issue on GitHub

---

**Last Updated**: 2025-01-15
**Version**: 1.0.0
