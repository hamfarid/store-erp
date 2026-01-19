# 🔄 SQLite to PostgreSQL Migration Guide

**Version:** 1.0.0  
**Last Updated:** 2025-11-18  
**Status:** ✅ Ready to Execute

---

## 📋 Overview

This guide covers the complete migration from SQLite to PostgreSQL for the Gaara AI application.

**What's Changed:**
- ✅ `.env` file updated with PostgreSQL credentials
- ✅ `alembic.ini` updated with PostgreSQL connection
- ✅ Setup scripts created for automated installation

---

## 🚀 Quick Migration (3 Steps)

### Step 1: Install PostgreSQL (Choose One)

**Option A: Windows Installer (Recommended)**
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer (remember the postgres password!)
3. Default port: 5432

**Option B: Docker (Quick Start)**
```bash
docker run --name gaara-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15-alpine
```

**Option C: Package Manager**
```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Linux
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

### Step 2: Setup Database (Choose One)

**Option A: Automated Script (Windows)**
```bash
cd backend
.\scripts\setup_postgresql.ps1
```

**Option B: SQL Script (All Platforms)**
```bash
cd backend
psql -U postgres -f scripts/setup_postgresql.sql
```

**Option C: Manual Setup**
```bash
# Connect to PostgreSQL
psql -U postgres

# Run these commands:
CREATE DATABASE gaara_scan_ai;
CREATE USER gaara_user WITH PASSWORD 'GaaraSecure2024!@#';
GRANT ALL PRIVILEGES ON DATABASE gaara_scan_ai TO gaara_user;
\c gaara_scan_ai
GRANT ALL ON SCHEMA public TO gaara_user;
\q
```

---

### Step 3: Install Driver & Run Migrations

```bash
cd backend
.\venv\Scripts\Activate.ps1

# Install PostgreSQL driver
pip install psycopg2-binary

# Run migrations
alembic upgrade head

# Create admin user
python scripts/create_default_admin.py

# Start application
cd src
python main.py
```

---

## ✅ Verification

### Check Database Connection

```bash
# Test connection
psql -U gaara_user -d gaara_scan_ai -h localhost

# List tables
\dt

# Expected output:
#  Schema |    Name    | Type  |   Owner    
# --------+------------+-------+------------
#  public | diagnoses  | table | gaara_user
#  public | farms      | table | gaara_user
#  public | reports    | table | gaara_user
#  public | users      | table | gaara_user

# Exit
\q
```

### Test Application

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gaara.ai","password":"Admin@Gaara123"}'
```

---

## 📊 Configuration Changes

### `.env` File (Updated)

**Before (SQLite):**
```env
DATABASE_URL=sqlite:///./gaara_scan_ai.db
```

**After (PostgreSQL):**
```env
POSTGRES_DB=gaara_scan_ai
POSTGRES_USER=gaara_user
POSTGRES_PASSWORD=GaaraSecure2024!@#
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://gaara_user:GaaraSecure2024!@#@localhost:5432/gaara_scan_ai
```

### `alembic.ini` (Updated)

**Before:**
```ini
sqlalchemy.url = sqlite:///./gaara_scan_ai.db
```

**After:**
```ini
sqlalchemy.url = postgresql://gaara_user:GaaraSecure2024!@#@localhost:5432/gaara_scan_ai
```

---

## 🔄 Data Migration (If You Have Existing Data)

### Export from SQLite

```bash
# Export all data
sqlite3 gaara_scan_ai.db .dump > sqlite_dump.sql
```

### Convert to PostgreSQL Format

The dump needs manual editing:
1. Remove SQLite-specific syntax
2. Convert data types
3. Fix sequences

**Or use a tool:**
```bash
# Using pgloader (recommended)
pgloader sqlite_dump.sql postgresql://gaara_user:GaaraSecure2024!@#@localhost/gaara_scan_ai
```

---

## 🔧 Troubleshooting

### Error: "psql: command not found"

**Solution:**
Add PostgreSQL to PATH:
```bash
# Windows (add to System Environment Variables)
C:\Program Files\PostgreSQL\15\bin

# macOS
export PATH="/usr/local/opt/postgresql@15/bin:$PATH"

# Linux
export PATH="/usr/lib/postgresql/15/bin:$PATH"
```

### Error: "password authentication failed"

**Solution:**
```bash
# Reset password
psql -U postgres
ALTER USER gaara_user WITH PASSWORD 'GaaraSecure2024!@#';
\q

# Update .env file with new password
```

### Error: "could not connect to server"

**Solution:**
```bash
# Check if PostgreSQL is running
# Windows:
services.msc  # Look for postgresql-x64-15

# macOS:
brew services list

# Linux:
sudo systemctl status postgresql

# Start if not running:
# Windows: Start from services.msc
# macOS: brew services start postgresql@15
# Linux: sudo systemctl start postgresql
```

### Error: "database does not exist"

**Solution:**
```bash
# Create database
psql -U postgres
CREATE DATABASE gaara_scan_ai;
\q

# Or run setup script again
psql -U postgres -f scripts/setup_postgresql.sql
```

---

## 📈 Performance Comparison

| Metric | SQLite | PostgreSQL |
|--------|--------|------------|
| **Concurrent Writes** | 1 | Unlimited |
| **Read Performance** | Fast | Very Fast |
| **Write Performance** | Good | Excellent |
| **Max Database Size** | 281 TB | Unlimited |
| **Concurrent Connections** | Limited | 100+ |
| **Production Ready** | Small apps | ✅ Yes |

---

## 🔒 Security Recommendations

### 1. Change Default Password

```bash
psql -U postgres
ALTER USER gaara_user WITH PASSWORD 'YOUR_STRONG_PASSWORD';
\q
```

Update `.env` and `alembic.ini` with new password.

### 2. Restrict Network Access

Edit `postgresql.conf`:
```conf
listen_addresses = 'localhost'
```

Edit `pg_hba.conf`:
```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   gaara_scan_ai   gaara_user                              md5
host    gaara_scan_ai   gaara_user      127.0.0.1/32            md5
```

### 3. Enable SSL (Production)

```conf
# postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

---

## 📚 Additional Resources

**Documentation:**
- PostgreSQL Setup Guide: `docs/POSTGRESQL_SETUP.md`
- Deployment Guide: `docs/DEPLOYMENT_GUIDE.md`
- Quick Start Guide: `docs/QUICK_START_GUIDE.md`

**Scripts:**
- SQL Setup: `backend/scripts/setup_postgresql.sql`
- PowerShell Setup: `backend/scripts/setup_postgresql.ps1`
- Admin User: `backend/scripts/create_default_admin.py`

**Official Docs:**
- PostgreSQL: https://www.postgresql.org/docs/
- Alembic: https://alembic.sqlalchemy.org/
- SQLAlchemy: https://www.sqlalchemy.org/

---

## ✅ Migration Checklist

- [ ] PostgreSQL installed
- [ ] Database created (`gaara_scan_ai`)
- [ ] User created (`gaara_user`)
- [ ] Privileges granted
- [ ] `.env` file updated
- [ ] `alembic.ini` updated
- [ ] `psycopg2-binary` installed
- [ ] Migrations run (`alembic upgrade head`)
- [ ] Admin user created
- [ ] Application tested
- [ ] Password changed (production)

---

**Generated by:** Autonomous AI Agent  
**Framework:** GLOBAL_PROFESSIONAL_CORE_PROMPT v16.0  
**Status:** ✅ Ready to Execute

---

