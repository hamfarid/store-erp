# 🚀 Store ERP System - Implementation Guide

**Version:** 1.0  
**Date:** 2025-11-05  
**For:** Development Team

---

## 📋 Quick Start

### 1. Environment Setup

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- Git

**Backend Setup:**
```bash
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

# Generate secure secrets
python scripts/generate_secrets.py

# Update .env with generated secrets

# Initialize database
python init_db.py

# Run tests
pytest --cov=src --cov-report=html

# Start server
python src/main.py
```

**Frontend Setup:**
```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev

# Run tests
npm run test

# Build for production
npm run build
```

---

## 🔐 Security Setup

### Generate Secure Secrets

**Method 1: Python**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Method 2: OpenSSL**
```bash
openssl rand -hex 32
```

**Method 3: Use provided script**
```bash
python backend/scripts/generate_secrets.py
```

### Update .env File

```bash
# Edit backend/.env
SECRET_KEY=<generated-secret-1>
JWT_SECRET_KEY=<generated-secret-2>
```

### Verify Security

```bash
# Run security tests
pytest tests/test_security*.py -v

# Check for hardcoded secrets
grep -r "SECRET_KEY\|JWT_SECRET" backend/src/ --exclude-dir=__pycache__
```

---

## 🧪 Testing

### Run All Tests

```bash
cd backend

# Run all tests with coverage
pytest --cov=src --cov-report=term-missing --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run tests by marker
pytest -m security -v
pytest -m integration -v

# Generate coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Run tests in UI mode
npm run test:ui
```

---

## 📦 Dependencies

### Backend Dependencies

**Core:**
- Flask 3.0.0 - Web framework
- SQLAlchemy 2.0.23 - ORM
- Flask-CORS 4.0.1 - CORS support

**Security:**
- argon2-cffi 23.1.0 - Password hashing (OWASP recommended)
- PyJWT 2.8.0 - JWT tokens
- cryptography 46.0.3 - Encryption
- pyotp 2.9.0 - MFA/TOTP
- bleach 6.1.0 - XSS prevention

**Testing:**
- pytest 7.4.3 - Testing framework
- pytest-cov 4.1.0 - Coverage reporting

**See:** `backend/requirements.txt` for complete list

### Frontend Dependencies

**Core:**
- React 18.3.1
- React Router DOM 7.6.1
- Vite 7.0.4

**Testing:**
- Vitest 3.2.4
- @testing-library/react 16.1.0

**See:** `frontend/package.json` for complete list

---

## 🗄️ Database

### Development (SQLite)

```bash
# Database location
backend/instance/inventory.db

# Initialize database
python backend/init_db.py

# Create admin user
python backend/create_admin_user.py

# Backup database
cp backend/instance/inventory.db backend/backups/inventory_$(date +%Y%m%d).db
```

### Production (PostgreSQL Recommended)

```bash
# Install PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb store_erp

# Create user
sudo -u postgres createuser -P store_user

# Grant privileges
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE store_erp TO store_user;

# Update .env
DATABASE_URL=postgresql://store_user:password@localhost:5432/store_erp
```

---

## 🚀 Deployment

### Development

```bash
# Backend
cd backend
python src/main.py

# Frontend
cd frontend
npm run dev
```

### Production

**Backend (Gunicorn):**
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:8000 src.main:app
```

**Frontend (Build):**
```bash
cd frontend
npm run build
# Serve dist/ folder with nginx or similar
```

**Docker:**
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📊 Monitoring

### Logs

```bash
# Backend logs
tail -f backend/logs/app.log

# Error logs
tail -f backend/logs/errors.log

# Access logs
tail -f backend/logs/access.log
```

### Health Check

```bash
# Backend health
curl http://localhost:8000/api/health

# System status
curl http://localhost:8000/api/system/status
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Import errors in tests**
```bash
# Solution: Fix Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend/src"
```

**Issue: Database locked**
```bash
# Solution: Close all connections
# Check for running processes
ps aux | grep python
# Kill if necessary
kill <pid>
```

**Issue: Port already in use**
```bash
# Solution: Find and kill process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Linux/Mac:
lsof -i :8000
kill -9 <pid>
```

**Issue: Missing dependencies**
```bash
# Solution: Reinstall
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Documentation

### Available Documentation

- `README.md` - Project overview
- `COMPREHENSIVE_ANALYSIS_REPORT.md` - Analysis findings
- `REFACTORING_PLAN.md` - Detailed refactoring plan
- `docs/Security.md` - Security documentation
- `docs/JWT_Token_Rotation.md` - JWT implementation
- `P0_SECURITY_SETUP.md` - Security setup guide
- `API_DOCUMENTATION.md` - API reference
- `TECHNICAL_DOCUMENTATION.md` - Technical details

### Generate API Documentation

```bash
# Start server
python backend/src/main.py

# Access OpenAPI spec
curl http://localhost:8000/api/openapi.json

# View in browser
http://localhost:8000/api/docs
```

---

## 🎯 Next Steps

### Immediate (This Week)

1. **Review Analysis Report**
   - Read `COMPREHENSIVE_ANALYSIS_REPORT.md`
   - Understand critical issues
   - Approve refactoring plan

2. **Set Up Development Environment**
   - Install dependencies
   - Create .env file
   - Generate secure secrets
   - Run tests

3. **Start Phase 1 (Critical Security)**
   - Remove hardcoded secrets
   - Remove insecure password fallback
   - Implement authorization checks

### Short Term (Next 2 Weeks)

4. **Phase 2: Testing**
   - Fix test import errors
   - Add comprehensive tests
   - Achieve 80%+ coverage
   - Set up CI/CD

5. **Phase 3: Important Fixes**
   - Fix CORS configuration
   - Consolidate server entry points
   - Remove linting suppression
   - Optimize database

### Long Term (Next Month)

6. **Phase 4: Code Organization**
   - Clean up route files
   - Reorganize by domain
   - Update documentation

7. **Phase 5: Nice-to-Have**
   - Add architecture diagrams
   - Internationalize comments
   - Optimize frontend bundle

---

## 🆘 Support

### Getting Help

**Documentation:**
- Check `docs/` directory
- Read analysis reports
- Review refactoring plan

**Issues:**
- Check troubleshooting section
- Review logs
- Run tests to identify problems

**Questions:**
- Consult technical lead
- Review code comments
- Check commit history

---

## ✅ Checklist

### Before Starting Development

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Git configured
- [ ] Dependencies installed (backend)
- [ ] Dependencies installed (frontend)
- [ ] .env file created and configured
- [ ] Secure secrets generated
- [ ] Database initialized
- [ ] Tests passing
- [ ] Development server running

### Before Deploying to Production

- [ ] All tests passing (80%+ coverage)
- [ ] Security audit complete
- [ ] No hardcoded secrets
- [ ] HTTPS configured
- [ ] PostgreSQL database set up
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Staging environment tested
- [ ] Rollback plan ready

---

**Last Updated:** 2025-11-05  
**Version:** 1.0  
**Maintainer:** Development Team

