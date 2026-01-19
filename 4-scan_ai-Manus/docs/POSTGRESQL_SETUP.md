# 🐘 PostgreSQL Setup Guide

**Version:** 1.0.0  
**Last Updated:** 2025-11-18  
**Status:** ✅ Ready to Use

---

## 📋 Overview

This guide will help you switch from SQLite to PostgreSQL for production use.

**Why PostgreSQL?**
- ✅ Better performance for production
- ✅ Concurrent connections support
- ✅ Advanced features (JSON, full-text search)
- ✅ Better data integrity
- ✅ Scalability

---

## 🎯 Prerequisites

### Option 1: Install PostgreSQL Locally (Recommended for Development)

**Windows:**
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the `postgres` user
4. Default port: 5432

**macOS:**
```bash
# Using Homebrew
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Option 2: Use Docker (Quick Start)

```bash
docker run --name gaara-postgres \
  -e POSTGRES_DB=gaara_scan_ai \
  -e POSTGRES_USER=gaara_user \
  -e POSTGRES_PASSWORD=GaaraSecure2024!@# \
  -p 5432:5432 \
  -v gaara_postgres_data:/var/lib/postgresql/data \
  -d postgres:15-alpine
```

---

## 🚀 Setup Steps

### Step 1: Create Database and User

**Method 1: Using psql (Command Line)**

```bash
# Connect to PostgreSQL as postgres user
psql -U postgres

# In psql prompt:
CREATE DATABASE gaara_scan_ai;
CREATE USER gaara_user WITH PASSWORD 'GaaraSecure2024!@#';
GRANT ALL PRIVILEGES ON DATABASE gaara_scan_ai TO gaara_user;

# For PostgreSQL 15+, also grant schema privileges
\c gaara_scan_ai
GRANT ALL ON SCHEMA public TO gaara_user;

# Exit
\q
```

**Method 2: Using pgAdmin (GUI)**

1. Open pgAdmin
2. Right-click "Databases" → "Create" → "Database"
   - Name: `gaara_scan_ai`
   - Owner: `postgres`
3. Right-click "Login/Group Roles" → "Create" → "Login/Group Role"
   - Name: `gaara_user`
   - Password: `GaaraSecure2024!@#`
   - Privileges: Can login
4. Right-click `gaara_scan_ai` → "Properties" → "Security"
   - Add `gaara_user` with all privileges

**Method 3: Using SQL Script**

Save this as `setup_database.sql`:

```sql
-- Create database
CREATE DATABASE gaara_scan_ai
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Create user
CREATE USER gaara_user WITH PASSWORD 'GaaraSecure2024!@#';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE gaara_scan_ai TO gaara_user;

-- Connect to database and grant schema privileges
\c gaara_scan_ai
GRANT ALL ON SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gaara_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gaara_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gaara_user;
```

Run it:
```bash
psql -U postgres -f setup_database.sql
```

---

### Step 2: Install PostgreSQL Driver

```bash
cd backend
.\venv\Scripts\Activate.ps1
pip install psycopg2-binary
```

---

### Step 3: Update Configuration

**The `.env` file has already been updated with:**

```env
POSTGRES_DB=gaara_scan_ai
POSTGRES_USER=gaara_user
POSTGRES_PASSWORD=GaaraSecure2024!@#
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://gaara_user:GaaraSecure2024!@#@localhost:5432/gaara_scan_ai
```

**⚠️ IMPORTANT:** Change the password in production!

---

### Step 4: Run Database Migrations

```bash
cd backend

# Drop existing SQLite migrations (if any)
# rm -rf alembic/versions/*  # Optional: if you want to start fresh

# Create new migration for PostgreSQL
.\venv\Scripts\python.exe -m alembic revision --autogenerate -m "PostgreSQL migration"

# Apply migrations
.\venv\Scripts\python.exe -m alembic upgrade head
```

---

### Step 5: Create Admin User

```bash
.\venv\Scripts\python.exe scripts/create_default_admin.py
```

**Expected Output:**
```
============================================================
🚀 Gaara AI - Create Default Admin User
============================================================

Initializing database...
✅ Database initialized

Creating default admin user...
Email: admin@gaara.ai
Name: Admin User

============================================================
✅ Default admin user created successfully!
============================================================

ID:    1
Email: admin@gaara.ai
Name:  Admin User
Role:  ADMIN

Login Credentials:
  Email:    admin@gaara.ai
  Password: Admin@Gaara123
```

---

### Step 6: Restart Application

```bash
# Stop the current application (Ctrl+C in the terminal)

# Start with PostgreSQL
cd src
python main.py
```

---

## ✅ Verify PostgreSQL Connection

### Method 1: Check Application Logs

When you start the application, you should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Method 2: Test Database Connection

```bash
# Using psql
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

### Method 3: Test via API

```bash
curl http://localhost:8000/health
```

---

## 🔧 Troubleshooting

### Error: "could not connect to server"

**Solution:**
```bash
# Check if PostgreSQL is running
# Windows:
services.msc  # Look for "postgresql-x64-15"

# macOS:
brew services list

# Linux:
sudo systemctl status postgresql
```

### Error: "password authentication failed"

**Solution:**
```bash
# Reset password
psql -U postgres
ALTER USER gaara_user WITH PASSWORD 'GaaraSecure2024!@#';
\q
```

### Error: "database does not exist"

**Solution:**
```bash
psql -U postgres
CREATE DATABASE gaara_scan_ai;
GRANT ALL PRIVILEGES ON DATABASE gaara_scan_ai TO gaara_user;
\q
```

### Error: "permission denied for schema public"

**Solution:**
```bash
psql -U postgres -d gaara_scan_ai
GRANT ALL ON SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gaara_user;
\q
```

---

## 📊 PostgreSQL vs SQLite Comparison

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Concurrent Writes** | ❌ Limited | ✅ Excellent |
| **Performance** | ✅ Good for small apps | ✅ Excellent for large apps |
| **Data Types** | ⚠️ Limited | ✅ Rich (JSON, Arrays, etc.) |
| **Full-Text Search** | ⚠️ Basic | ✅ Advanced |
| **Scalability** | ❌ Limited | ✅ Excellent |
| **Setup** | ✅ Zero config | ⚠️ Requires installation |
| **Production Ready** | ⚠️ Small apps only | ✅ Yes |

---

## 🔒 Security Best Practices

### 1. Change Default Password

```bash
psql -U postgres
ALTER USER gaara_user WITH PASSWORD 'YOUR_STRONG_PASSWORD_HERE';
\q
```

Update `.env`:
```env
POSTGRES_PASSWORD=YOUR_STRONG_PASSWORD_HERE
DATABASE_URL=postgresql://gaara_user:YOUR_STRONG_PASSWORD_HERE@localhost:5432/gaara_scan_ai
```

### 2. Restrict Network Access

Edit `postgresql.conf`:
```
listen_addresses = 'localhost'  # Only local connections
```

Edit `pg_hba.conf`:
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   gaara_scan_ai   gaara_user                              md5
host    gaara_scan_ai   gaara_user      127.0.0.1/32            md5
```

### 3. Enable SSL (Production)

```bash
# Generate SSL certificate
openssl req -new -x509 -days 365 -nodes -text -out server.crt -keyout server.key

# Update postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

---

## 📈 Performance Tuning

### Basic Tuning (postgresql.conf)

```conf
# Memory
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB

# Connections
max_connections = 100

# Logging
log_statement = 'all'  # Development only
log_duration = on
```

---

## 🔄 Migration from SQLite

If you have existing data in SQLite:

```bash
# Export from SQLite
sqlite3 gaara_scan_ai.db .dump > sqlite_dump.sql

# Convert to PostgreSQL format (manual editing required)
# Then import:
psql -U gaara_user -d gaara_scan_ai -f postgres_dump.sql
```

---

## 📞 Support

**PostgreSQL Documentation:** https://www.postgresql.org/docs/  
**pgAdmin Download:** https://www.pgadmin.org/download/  
**Docker PostgreSQL:** https://hub.docker.com/_/postgres

---

**Generated by:** Autonomous AI Agent  
**Framework:** GLOBAL_PROFESSIONAL_CORE_PROMPT v16.0  
**Status:** ✅ Ready to Use

---

