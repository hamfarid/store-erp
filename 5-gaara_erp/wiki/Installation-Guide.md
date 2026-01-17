# 📦 Installation Guide

This guide walks you through setting up the Store Management System on your local machine or server.

---

## Prerequisites

### Required Software

| Software | Minimum Version | Recommended |
|----------|-----------------|-------------|
| Python | 3.10 | 3.11+ |
| Node.js | 18.x | 20.x LTS |
| npm | 9.x | 10.x |
| Git | 2.30 | Latest |
| Docker | 20.10 | Latest |

### Optional (for production)

- PostgreSQL 14+
- Redis 7+
- Nginx

---

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hamfarid/Store.git
cd Store
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
flask db upgrade

# Create admin user
python scripts/create_admin.py
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local
```

### 4. Start Development Servers

**Backend:**
```bash
cd backend
flask run --debug
```

**Frontend:**
```bash
cd frontend
npm run dev
```

---

## Docker Installation

### Using Docker Compose

```bash
# Clone repository
git clone https://github.com/hamfarid/Store.git
cd Store

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Services

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 5000 | http://localhost:5000/api |
| API Docs | 5000 | http://localhost:5000/api/docs |

---

## Configuration

### Backend Environment Variables

```ini
# .env file
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///store.db

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Email (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Frontend Environment Variables

```ini
# .env.local file
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=Store Management System
```

---

## Database Setup

### SQLite (Development)

SQLite is used by default for development. No additional setup required.

### PostgreSQL (Production)

```bash
# Create database
createdb store_db

# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/store_db

# Run migrations
flask db upgrade
```

---

## Verify Installation

### Check Backend

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Check Frontend

Visit http://localhost:3000 in your browser.

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Database migration errors:**
```bash
# Reset migrations
flask db downgrade base
flask db upgrade
```

---

## Next Steps

- [[Configuration]] - Detailed configuration options
- [[Quick Start Tutorial]] - Build your first feature
- [[API Reference]] - Explore the API

---

*Last updated: 2025-12-01*

