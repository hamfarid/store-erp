# Store ERP - Scripts Guide

**Version:** 2.0.0  
**Last Updated:** 2025-12-13

---

## Overview

This guide explains how to use the automation scripts provided with Store ERP for easy setup, deployment, and management.

---

## Available Scripts

### 1. `setup.sh` - Complete Setup

**Purpose:** Automated installation and setup of the entire project.

**What it does:**
- ✅ Checks system requirements (Python 3.11, Node.js 22, pnpm)
- ✅ Creates Python virtual environment
- ✅ Installs all Python dependencies
- ✅ Installs all Node.js dependencies
- ✅ Sets up database
- ✅ Creates environment files (.env)
- ✅ Creates required directories
- ✅ Runs tests
- ✅ Optionally builds frontend

**Usage:**
```bash
./setup.sh
```

**First-time setup:**
```bash
# 1. Clone the repository
git clone https://github.com/hamfarid/store-erp.git
cd store-erp

# 2. Run setup
./setup.sh

# 3. Update environment variables
nano backend/.env
# Change SECRET_KEY and JWT_SECRET_KEY

# 4. Start the application
./start.sh
```

**Requirements:**
- Python 3.11+
- Node.js 22+
- Git (recommended)

**Time:** 5-10 minutes (depending on internet speed)

---

### 2. `start.sh` - Start Servers

**Purpose:** Start both backend and frontend servers.

**What it does:**
- ✅ Checks if servers are already running
- ✅ Starts Flask backend server (port 8000)
- ✅ Starts Vite frontend server (port 5502)
- ✅ Saves process IDs to PID files
- ✅ Waits for servers to be ready
- ✅ Displays access URLs and information

**Usage:**
```bash
./start.sh
```

**Output:**
```
========================================
Store ERP Started Successfully!
========================================

✓ Both servers are running!

Access the application:
  Frontend: http://localhost:5502
  Backend API: http://localhost:8000

Default login:
  Username: admin
  Password: admin123

Process IDs:
  Backend: 12345
  Frontend: 12346

Logs:
  Backend: /path/to/logs/backend.log
  Frontend: /path/to/logs/frontend.log
```

**Ports used:**
- Backend: 8000 (configurable in backend/.env)
- Frontend: 5502 (default Vite port)

**Logs:**
- Backend: `logs/backend.log`
- Frontend: `logs/frontend.log`
- Application: `logs/application/app.log`

---

### 3. `stop.sh` - Stop Servers

**Purpose:** Stop both backend and frontend servers.

**What it does:**
- ✅ Stops backend server gracefully
- ✅ Stops frontend server gracefully
- ✅ Force kills if not responding
- ✅ Cleans up PID files
- ✅ Kills any remaining processes on ports

**Usage:**
```bash
./stop.sh
```

**Output:**
```
========================================
Stopping Store ERP Servers
========================================

ℹ Stopping backend (PID: 12345)...
✓ Backend stopped
ℹ Stopping frontend (PID: 12346)...
✓ Frontend stopped

========================================
Store ERP Stopped
========================================

✓ Stopped 2 server(s)
```

**Safe shutdown:**
- Waits 10 seconds for graceful shutdown
- Force kills if process doesn't respond
- Cleans up all resources

---

### 4. `restart.sh` - Restart Servers

**Purpose:** Restart both servers (stop + start).

**What it does:**
- ✅ Stops all servers
- ✅ Waits 2 seconds
- ✅ Starts all servers

**Usage:**
```bash
./restart.sh
```

**When to use:**
- After code changes
- After configuration changes
- After dependency updates
- When servers are unresponsive

**Equivalent to:**
```bash
./stop.sh && sleep 2 && ./start.sh
```

---

### 5. `status.sh` - Check Status

**Purpose:** Check the status of all services.

**What it does:**
- ✅ Checks if backend is running
- ✅ Checks if frontend is running
- ✅ Checks if ports are listening
- ✅ Shows process information
- ✅ Checks database status
- ✅ Shows recent logs
- ✅ Displays overall status

**Usage:**
```bash
./status.sh
```

**Output:**
```
========================================
Store ERP Status
========================================

Backend Server:
✓ Running (PID: 12345)
  Process: 12345  1234  2.5  1.2  00:15:23 python src/app.py
✓ Port 8000: Listening
  URL: http://localhost:8000

Frontend Server:
✓ Running (PID: 12346)
  Process: 12346  1234  1.5  2.1  00:15:20 node vite
✓ Port 5502: Listening
  URL: http://localhost:5502

Database:
✓ Database exists (Size: 2.5M)
  Location: /path/to/backend/store_erp.db

Recent Logs:
✓ Application log exists (Size: 1.2M)
  Last 5 lines:
    [INFO] Server started
    [INFO] Database connected
    ...

========================================
Overall Status
========================================

✓ All services are running

Access the application:
  Frontend: http://localhost:5502
  Backend API: http://localhost:8000
```

---

## Common Workflows

### First-Time Setup

```bash
# 1. Clone repository
git clone https://github.com/hamfarid/store-erp.git
cd store-erp

# 2. Run setup
./setup.sh

# 3. Update secrets
nano backend/.env
# Change SECRET_KEY and JWT_SECRET_KEY

# 4. Start application
./start.sh

# 5. Open browser
# http://localhost:5502
```

### Daily Development

```bash
# Morning - Start servers
./start.sh

# Check status anytime
./status.sh

# After code changes - Restart
./restart.sh

# Evening - Stop servers
./stop.sh
```

### After Updates

```bash
# 1. Stop servers
./stop.sh

# 2. Pull latest code
git pull

# 3. Update dependencies
cd backend && source venv/bin/activate && pip install -r requirements.txt
cd ../frontend && pnpm install

# 4. Run migrations (if any)
cd ../backend && flask db upgrade

# 5. Restart servers
cd .. && ./restart.sh
```

### Troubleshooting

```bash
# Check status
./status.sh

# View logs
tail -f logs/backend.log
tail -f logs/frontend.log
tail -f logs/application/app.log

# Restart if issues
./restart.sh

# Full reset
./stop.sh
rm -rf backend/venv frontend/node_modules
./setup.sh
./start.sh
```

---

## Environment Variables

### Backend (.env)

```bash
# Flask Configuration
FLASK_APP=src/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# Database
DATABASE_URL=sqlite:///store_erp.db

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=http://localhost:5502,http://localhost:3004

# Logging
LOG_LEVEL=INFO
LOG_DIR=../logs

# 2FA
TOTP_ISSUER=Store ERP
```

### Frontend (.env)

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# App Configuration
VITE_APP_NAME=Store ERP
VITE_APP_VERSION=2.0.0

# Features
VITE_ENABLE_2FA=true
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_RTL=true
```

---

## Port Configuration

### Default Ports

| Service | Port | Configurable |
|---------|------|--------------|
| Backend | 8000 | Yes (backend/.env) |
| Frontend | 5502 | Yes (vite.config.js) |

### Change Backend Port

Edit `backend/.env`:
```bash
PORT=9000
```

Restart:
```bash
./restart.sh
```

### Change Frontend Port

Edit `frontend/vite.config.js`:
```javascript
export default defineConfig({
  server: {
    port: 3000
  }
})
```

Update `backend/.env` CORS:
```bash
CORS_ORIGINS=http://localhost:3000
```

Restart:
```bash
./restart.sh
```

---

## Logs

### Log Locations

| Log Type | Location | Purpose |
|----------|----------|---------|
| Backend | `logs/backend.log` | Backend server output |
| Frontend | `logs/frontend.log` | Frontend server output |
| Application | `logs/application/app.log` | Application events |
| Security | `logs/security/security.log` | Security events |
| Performance | `logs/performance/performance.log` | Performance metrics |
| Errors | `logs/errors/errors.log` | Error logs only |

### View Logs

```bash
# Real-time backend logs
tail -f logs/backend.log

# Real-time frontend logs
tail -f logs/frontend.log

# Real-time application logs
tail -f logs/application/app.log

# All logs together
tail -f logs/backend.log logs/frontend.log logs/application/app.log

# Last 100 lines
tail -100 logs/application/app.log

# Search logs
grep "ERROR" logs/application/app.log
grep "login" logs/security/security.log
```

---

## Process Management

### PID Files

Scripts use PID files to track running processes:
- Backend: `.backend.pid`
- Frontend: `.frontend.pid`

### Manual Process Management

```bash
# Find processes
ps aux | grep "python src/app.py"
ps aux | grep "vite"

# Kill by port
lsof -ti:8000 | xargs kill
lsof -ti:5502 | xargs kill

# Kill by PID
kill 12345
kill -9 12345  # Force kill
```

---

## Troubleshooting

### Issue 1: Port Already in Use

**Error:**
```
✗ Port 8000 is already in use
```

**Solution:**
```bash
# Find process using port
lsof -i :8000

# Kill process
lsof -ti:8000 | xargs kill

# Or change port in backend/.env
PORT=9000
```

### Issue 2: Virtual Environment Not Found

**Error:**
```
✗ Virtual environment not found
```

**Solution:**
```bash
# Run setup again
./setup.sh
```

### Issue 3: Dependencies Not Installed

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 4: Database Not Found

**Error:**
```
✗ Database not found
```

**Solution:**
```bash
cd backend
source venv/bin/activate
python database_setup.py
```

### Issue 5: Permission Denied

**Error:**
```
bash: ./setup.sh: Permission denied
```

**Solution:**
```bash
chmod +x setup.sh start.sh stop.sh restart.sh status.sh
```

---

## Advanced Usage

### Run in Background (Production)

For production, use systemd services instead of these scripts.

**Create systemd service:**
```bash
sudo nano /etc/systemd/system/store-erp-backend.service
```

```ini
[Unit]
Description=Store ERP Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/store-erp/backend
Environment="PATH=/path/to/store-erp/backend/venv/bin"
ExecStart=/path/to/store-erp/backend/venv/bin/python src/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable store-erp-backend
sudo systemctl start store-erp-backend
sudo systemctl status store-erp-backend
```

### Docker Deployment

For Docker deployment, see `docs/DEVELOPER_GUIDE.md`.

### Nginx Deployment

For Nginx deployment, see `deployment/nginx/store-erp.conf`.

---

## Best Practices

### Development

1. **Always use scripts** - Don't run servers manually
2. **Check status** - Use `./status.sh` before starting
3. **View logs** - Monitor logs for errors
4. **Restart after changes** - Use `./restart.sh` after code changes

### Production

1. **Use systemd** - Don't use these scripts in production
2. **Use Nginx** - Reverse proxy for both servers
3. **Use SSL** - Always use HTTPS
4. **Monitor logs** - Set up log monitoring
5. **Backup database** - Regular backups

---

## Quick Reference

```bash
# Setup (first time only)
./setup.sh

# Start servers
./start.sh

# Stop servers
./stop.sh

# Restart servers
./restart.sh

# Check status
./status.sh

# View logs
tail -f logs/backend.log logs/frontend.log

# Update dependencies
cd backend && source venv/bin/activate && pip install -r requirements.txt
cd ../frontend && pnpm install

# Run tests
cd backend && source venv/bin/activate && pytest

# Build frontend
cd frontend && pnpm build
```

---

## Support

For issues or questions:
- **Documentation:** `docs/DEVELOPER_GUIDE.md`
- **GitHub Issues:** https://github.com/hamfarid/store-erp/issues
- **Email:** support@store-erp.com

---

**Version:** 2.0.0  
**Last Updated:** 2025-12-13
