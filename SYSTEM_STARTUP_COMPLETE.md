# System Startup Configuration - Complete ✅

**Date**: November 17, 2025  
**Status**: All startup scripts configured and tested  
**Components**: Backend, Frontend, Docker, Database

---

## 🎯 What Was Implemented

### 1. Enhanced PowerShell Startup Script (`start-system.ps1`)

**New Features Added:**
- ✅ Automatic Docker services startup (Redis, PostgreSQL, Monitoring)
- ✅ Comprehensive database initialization with migrations
- ✅ Default data creation (admin user, roles, categories)
- ✅ Browser auto-open option (`-OpenBrowser`)
- ✅ Skip Docker option (`-SkipDocker`)
- ✅ Clean installation support (`-Clean`)
- ✅ Enhanced error handling and status reporting
- ✅ Health checks for all services
- ✅ Colored console output for better visibility

**New Parameters:**
```powershell
-Mode [dev|prod]        # Development or production mode
-OpenBrowser           # Open browser automatically after startup
-SkipDocker           # Skip Docker services
-SkipMigration        # Skip database migrations
-SkipFrontend         # Backend only
-SkipBackend          # Frontend only
-Clean                # Clean install (remove dependencies)
```

**Usage Examples:**
```powershell
# Standard startup
.\start-system.ps1

# With browser and skip Docker
.\start-system.ps1 -OpenBrowser -SkipDocker

# Clean installation
.\start-system.ps1 -Clean

# Production mode
.\start-system.ps1 -Mode prod
```

### 2. Updated Windows Batch Launcher (`start-all.bat`)

**Features:**
- ✅ Simplified command-line interface
- ✅ Calls PowerShell script with appropriate arguments
- ✅ User-friendly help system
- ✅ Error handling and status reporting
- ✅ ASCII art banner for professional look

**Command-Line Options:**
```bash
--browser          # Open browser after startup
--no-docker        # Skip Docker services
--clean            # Clean installation
--backend-only     # Start backend only
--frontend-only    # Start frontend only
--help             # Show help message
```

**Usage Examples:**
```bash
# Quick start with browser
.\start-all.bat --browser

# Without Docker
.\start-all.bat --no-docker

# Clean install
.\start-all.bat --clean

# Backend only
.\start-all.bat --backend-only
```

### 3. Docker Services Integration

**Automatic Services:**
- Redis (caching and sessions)
- PostgreSQL (production database)
- Grafana (monitoring dashboards)
- Prometheus (metrics collection)
- Loki (log aggregation)

**Features:**
- ✅ Automatic Docker Compose startup
- ✅ Health check verification
- ✅ Service status reporting
- ✅ Graceful error handling if Docker unavailable
- ✅ Optional (system works without Docker)

### 4. Database Initialization Enhancement

**Comprehensive Setup:**
- ✅ Instance directory creation
- ✅ Database file initialization
- ✅ Alembic migrations setup
- ✅ Migration version detection
- ✅ Automatic upgrade execution
- ✅ Default data population
- ✅ Integrity verification

**Scripts Integrated:**
- `database_setup.py` - Main setup
- `check_tables.py` - Verification
- `ensure_tables.py` - Data population
- `create_admin_user.py` - Admin creation

### 5. Comprehensive Documentation

**Created Files:**
- ✅ `STARTUP_GUIDE.md` - Complete startup documentation
- ✅ `SYSTEM_STARTUP_COMPLETE.md` - This file
- ✅ Updated `README.md` with quick start section

**Documentation Includes:**
- Quick start commands
- All command-line options
- Troubleshooting guide
- Port configuration
- System requirements
- Access URLs
- Default credentials
- Development vs production modes

---

## 📦 What Gets Installed/Initialized

### Backend Components
1. **Python Virtual Environment** (`.venv`)
   - Location: `backend/.venv`
   - Python packages from `requirements.txt`

2. **Database** (SQLite)
   - Location: `backend/instance/inventory.db`
   - Tables: All models initialized
   - Migrations: Alembic versions applied

3. **Default Data**
   - Admin user: admin/admin123
   - Default roles: Admin, Manager, Employee, Viewer
   - Sample categories
   - Default warehouse

### Frontend Components
1. **Node Modules**
   - Location: `frontend/node_modules`
   - All dependencies from `package.json`

2. **Development Server**
   - Vite dev server with HMR
   - Port: 5502
   - Network accessible

### Docker Services (Optional)
1. **Redis** - Port 6379
2. **PostgreSQL** - Port 5432
3. **Grafana** - Port 3000
4. **Prometheus** - Port 9090
5. **Loki** - Port 3100

---

## 🌐 System Access Points

### Primary URLs
| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5502 | Main application interface |
| Backend API | http://localhost:5002 | REST API endpoints |
| API Health | http://localhost:5002/health | Health check endpoint |
| API Docs | http://localhost:5002/api/docs | API documentation |

### Docker Services (if enabled)
| Service | URL | Credentials |
|---------|-----|-------------|
| Grafana | http://localhost:3000 | admin/admin123 |
| Prometheus | http://localhost:9090 | None |
| Redis | localhost:6379 | None |
| PostgreSQL | localhost:5432 | See .env |

---

## ✅ Verification Steps

After running the startup script, verify:

### 1. Backend Status
```bash
# Check health endpoint
curl http://localhost:5002/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "blueprints": 38
}
```

### 2. Frontend Status
```bash
# Open in browser
http://localhost:5502

# Should see login page with:
- Store ERP logo
- Username/Password fields
- Language selector (Arabic/English)
```

### 3. Database Status
```bash
cd backend
.\.venv\Scripts\Activate.ps1
python check_tables.py

# Should show all tables created
```

### 4. Docker Status (if using Docker)
```bash
docker-compose ps

# Should show running containers:
- redis
- postgres
- grafana
- prometheus
```

---

## 🎯 Next Steps After Startup

### 1. First Login
- Navigate to http://localhost:5502
- Login with: admin / admin123
- **Important**: Change password immediately!

### 2. System Configuration
- Go to Settings > Company Settings
- Configure company information
- Set currency preferences
- Configure tax settings

### 3. User Management
- Go to Users > User Management
- Create additional user accounts
- Assign appropriate roles
- Set permissions

### 4. Data Setup
- Add product categories
- Create products
- Set up customers/suppliers
- Configure warehouses

### 5. Start Using
- Create sales invoices
- Record purchases
- Track inventory
- Generate reports

---

## 🛠️ Troubleshooting

### Issue: Port Already in Use

**Solution 1**: Stop conflicting processes
```powershell
# Find process using port 5002
Get-NetTCPConnection -LocalPort 5002 | Select-Object -ExpandProperty OwningProcess
Stop-Process -Id <PID> -Force

# Or for port 5502
Get-NetTCPConnection -LocalPort 5502 | Select-Object -ExpandProperty OwningProcess
Stop-Process -Id <PID> -Force
```

**Solution 2**: Change ports in `start-system.ps1`
```powershell
$BACKEND_PORT = 8000   # Change from 5002
$FRONTEND_PORT = 3000  # Change from 5502
```

### Issue: Docker Not Starting

**Check Docker Status:**
```bash
docker ps
docker-compose ps
```

**Start Docker Desktop:**
- Windows: Launch Docker Desktop application
- Ensure Docker daemon is running

**Skip Docker if not needed:**
```bash
.\start-all.bat --no-docker
```

### Issue: Database Errors

**Recreate Database:**
```powershell
cd backend
Remove-Item instance\inventory.db
python database_setup.py
```

**Check Migrations:**
```powershell
python -m flask db current
python -m flask db upgrade
```

### Issue: Dependency Installation Failed

**Backend Dependencies:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt --force-reinstall
```

**Frontend Dependencies:**
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### Issue: Clean Restart Needed

```bash
# Windows
.\stop-all.bat
.\start-all.bat --clean

# PowerShell
.\start-system.ps1 -Clean
```

---

## 📊 System Monitoring

### View Logs

**Backend Logs:**
- Check terminal window where backend is running
- Or check `backend/logs/` directory

**Frontend Logs:**
- Check terminal window where frontend is running
- Or browser console (F12)

**Docker Logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f redis
docker-compose logs -f postgres
```

### Monitor Performance

**Grafana Dashboards:**
1. Open http://localhost:3000
2. Login: admin/admin123
3. Navigate to dashboards
4. View system metrics

**Prometheus Metrics:**
1. Open http://localhost:9090
2. Query system metrics
3. View graphs

---

## 🔄 Maintenance Commands

### Stop System
```bash
# Stop all services
.\stop-all.bat

# Stop backend only (Ctrl+C in terminal)
# Stop frontend only (Ctrl+C in terminal)

# Stop Docker services
docker-compose down
```

### Restart System
```bash
# Full restart
.\stop-all.bat
.\start-all.bat

# Restart Docker only
docker-compose restart
```

### Update Dependencies
```bash
# Backend
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
```

### Backup Database
```bash
# Copy database file
Copy-Item backend\instance\inventory.db backups\inventory_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db
```

---

## 📈 Performance Optimization

### Development Mode
- Uses SQLite (single file database)
- Flask development server
- Vite HMR for fast refresh
- Debug logging enabled

### Production Mode
- Uses PostgreSQL (multi-user)
- Gunicorn WSGI server
- Nginx reverse proxy
- Production logging
- SSL/TLS encryption
- Docker containerization

**Switch to Production:**
```powershell
.\start-system.ps1 -Mode prod
```

---

## 🎉 Success Indicators

After successful startup, you should see:

### Terminal Output
```
╔════════════════════════════════════════════════════════════════╗
║              Store ERP - System Startup Script                 ║
║  Mode: DEV                                                     ║
╚════════════════════════════════════════════════════════════════╝

✅ All prerequisites satisfied
✅ Virtual environment activated
✅ Backend dependencies installed
✅ Database initialized
✅ Backend server is running on http://localhost:5002
✅ Frontend dependencies installed
✅ Frontend server is running on http://localhost:5502

🎉 Development System Started Successfully!
```

### Browser
- Frontend loads at http://localhost:5502
- Login page displays correctly
- No console errors (F12)

### API
- Health check responds: http://localhost:5002/health
- Returns JSON with status: "healthy"

### Docker (if enabled)
```bash
$ docker-compose ps
NAME                STATUS
redis              Up
postgres           Up
grafana            Up
prometheus         Up
```

---

## 📞 Support

### Documentation
- [STARTUP_GUIDE.md](./STARTUP_GUIDE.md) - Complete startup guide
- [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md) - Technical details
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - API reference
- [USER_GUIDE.md](./USER_GUIDE.md) - User manual

### Troubleshooting
- Check logs in `backend/logs/`
- Check browser console (F12)
- Review terminal output
- See troubleshooting section above

### Contact
- GitHub Issues: https://github.com/hamfarid/Store/issues
- Documentation: https://github.com/hamfarid/Store/wiki

---

## ✨ Summary

**Completed Enhancements:**
1. ✅ Enhanced PowerShell startup script with Docker support
2. ✅ Updated Windows batch launcher
3. ✅ Integrated Docker services
4. ✅ Enhanced database initialization
5. ✅ Created comprehensive documentation
6. ✅ Added browser auto-open feature
7. ✅ Implemented health checks
8. ✅ Added clean installation support
9. ✅ Created troubleshooting guide
10. ✅ Updated README with quick start

**Ready to Use:**
- Run `.\start-all.bat` to start everything
- Access http://localhost:5502
- Login with admin/admin123
- Start managing your store!

---

*System startup configuration completed successfully on November 17, 2025*
