# Store ERP - System Startup Guide

## 🚀 Quick Start

### Option 1: Start Everything (Recommended)
```bash
# Windows
.\start-all.bat

# PowerShell
.\start-system.ps1

# Linux/Mac
./start-all.sh
```

This will:
- ✅ Initialize Python virtual environment
- ✅ Install all backend dependencies
- ✅ Initialize and migrate database
- ✅ Create default admin user
- ✅ Install frontend dependencies
- ✅ Start Docker services (optional)
- ✅ Start backend on port 5002
- ✅ Start frontend on port 5502

---

## 📋 Command Options

### Windows Batch File (`start-all.bat`)

```bash
# Start with browser auto-open
.\start-all.bat --browser

# Start without Docker services
.\start-all.bat --no-docker

# Clean install (remove existing dependencies)
.\start-all.bat --clean

# Backend only
.\start-all.bat --backend-only

# Frontend only
.\start-all.bat --frontend-only

# Show help
.\start-all.bat --help
```

### PowerShell Script (`start-system.ps1`)

```powershell
# Development mode (default)
.\start-system.ps1

# With browser auto-open
.\start-system.ps1 -OpenBrowser

# Production mode (Docker)
.\start-system.ps1 -Mode prod

# Skip database migrations
.\start-system.ps1 -SkipMigration

# Skip Docker services
.\start-system.ps1 -SkipDocker

# Backend only
.\start-system.ps1 -SkipFrontend

# Frontend only
.\start-system.ps1 -SkipBackend

# Clean installation
.\start-system.ps1 -Clean

# Combined options
.\start-system.ps1 -OpenBrowser -SkipDocker
```

---

## 🌐 Access URLs

After successful startup, you can access:

### Main Application
- **Frontend**: http://localhost:5502
- **Backend API**: http://localhost:5002
- **API Documentation**: http://localhost:5002/api/docs
- **Health Check**: http://localhost:5002/health

### Docker Services (if started)
- **Redis**: localhost:6379
- **PostgreSQL**: localhost:5432
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090

---

## 🔐 Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

⚠️ **Important**: Change these credentials after first login!

---

## 📦 What Gets Installed/Initialized

### Backend (Python/Flask)
1. **Virtual Environment**: `.venv` directory
2. **Dependencies**: All packages from `requirements.txt`
3. **Database**: SQLite at `backend/instance/inventory.db`
4. **Migrations**: Alembic migration files
5. **Default Data**: Admin user, roles, categories, warehouses

### Frontend (React/Vite)
1. **Dependencies**: All packages from `package.json`
2. **Node Modules**: `frontend/node_modules` directory

### Docker Services (Optional)
1. **Redis**: For caching and sessions
2. **PostgreSQL**: For production database
3. **Grafana**: For monitoring and analytics
4. **Prometheus**: For metrics collection
5. **Loki**: For log aggregation

---

## 🛠️ Troubleshooting

### Port Already in Use

If you see "port already in use" errors:

```bash
# Check what's using port 5002 (backend)
netstat -ano | findstr :5002

# Check what's using port 5502 (frontend)
netstat -ano | findstr :5502

# Kill process by PID
taskkill /PID <PID> /F
```

### Docker Not Starting

```bash
# Check Docker status
docker ps

# Start Docker Desktop manually
# Or restart Docker service
net stop com.docker.service
net start com.docker.service
```

### Database Errors

```bash
# Recreate database from scratch
cd backend
Remove-Item instance\inventory.db
python database_setup.py
```

### Dependency Errors

```bash
# Backend - Reinstall dependencies
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt --force-reinstall

# Frontend - Reinstall dependencies
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Clean Restart

```bash
# Stop all services
.\stop-all.bat

# Clean start
.\start-all.bat --clean
```

---

## 🔄 System Management

### Viewing Logs

**Backend**: Check the terminal window where backend is running

**Frontend**: Check the terminal window where frontend is running

**Docker Services**:
```bash
docker-compose logs -f
docker-compose logs -f redis
docker-compose logs -f postgres
```

### Stopping Services

**Option 1**: Press `Ctrl+C` in each terminal window

**Option 2**: Use stop script
```bash
.\stop-all.bat
```

**Option 3**: Stop Docker only
```bash
docker-compose down
```

### Restarting Services

**Full Restart**:
```bash
.\stop-all.bat
.\start-all.bat
```

**Docker Only**:
```bash
docker-compose restart
```

**Individual Service**:
```bash
docker-compose restart redis
```

---

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Linux, macOS
- **RAM**: 4GB (8GB recommended)
- **Disk**: 2GB free space
- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher
- **Docker**: 20.x or higher (optional)

### Software Dependencies
- Python 3.8+
- Node.js 16+
- npm 8+
- PowerShell 5.1+ (Windows)
- Docker Desktop (optional)
- Docker Compose (optional)

---

## 🎯 Development vs Production

### Development Mode (Default)
- Uses SQLite database
- Flask development server
- Vite dev server with HMR
- Debug logging enabled
- CORS enabled for localhost
- No SSL/TLS

### Production Mode
- Uses PostgreSQL database
- Gunicorn WSGI server
- Nginx reverse proxy
- Production logging
- SSL/TLS enabled
- Docker containerized

To start in production mode:
```bash
.\start-system.ps1 -Mode prod
```

---

## 📝 Configuration Files

### Environment Variables
Create `.env` file in project root:
```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database
DATABASE_URL=sqlite:///instance/inventory.db
# or for PostgreSQL:
# DATABASE_URL=postgresql://user:pass@localhost:5432/store_db

# Server
BACKEND_PORT=5002
FRONTEND_PORT=5502

# Docker
COMPOSE_PROJECT_NAME=store_erp
```

### Frontend Configuration
Edit `frontend/.env`:
```env
VITE_API_URL=http://localhost:5002
VITE_APP_NAME=Store ERP
```

---

## 🔧 Advanced Usage

### Custom Ports
```powershell
# Edit start-system.ps1
$BACKEND_PORT = 8000  # Change backend port
$FRONTEND_PORT = 3000  # Change frontend port
```

### Skip Specific Components
```bash
# Backend only (for API development)
.\start-system.ps1 -SkipFrontend

# Frontend only (mock backend)
.\start-system.ps1 -SkipBackend

# No Docker (lightweight)
.\start-system.ps1 -SkipDocker

# Skip migrations (faster startup)
.\start-system.ps1 -SkipMigration
```

### Clean Installation
When dependencies are broken or outdated:
```bash
.\start-system.ps1 -Clean
```

This will:
- Delete `.venv` directory
- Delete `node_modules` directory
- Reinstall all dependencies fresh

---

## 📚 Additional Resources

### Documentation
- [API Documentation](./API_DOCUMENTATION.md)
- [Technical Documentation](./TECHNICAL_DOCUMENTATION.md)
- [User Guide](./USER_GUIDE.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)

### Support
- GitHub Issues: https://github.com/hamfarid/Store/issues
- Email: support@store-erp.example

---

## ✅ Verification Checklist

After startup, verify:

- [ ] Backend responds at http://localhost:5002/health
- [ ] Frontend loads at http://localhost:5502
- [ ] Can login with admin/admin123
- [ ] Database file exists at `backend/instance/inventory.db`
- [ ] Docker containers running (if using Docker): `docker-compose ps`
- [ ] No error messages in terminal windows

---

## 🎉 Success!

If all services are running, you should see:
- ✅ Backend server running on http://localhost:5002
- ✅ Frontend server running on http://localhost:5502
- ✅ Database initialized with default data
- ✅ Docker services running (if applicable)

**Next Steps:**
1. Open http://localhost:5502 in your browser
2. Login with admin/admin123
3. Change default password in settings
4. Start using the system!

---

*Last Updated: November 17, 2025*
