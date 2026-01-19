# ⚡ Quick Start Guide for Developers

**Version:** 1.0.0  
**Last Updated:** 2025-11-18  
**Target:** Development Environment  
**Status:** ✅ Ready to Use

---

## 📋 Overview

Get the Gaara AI application running on your local machine in **under 10 minutes**!

**What You'll Get:**
- ✅ Backend API running on http://localhost:1005
- ✅ Frontend app running on http://localhost:1505
- ✅ Interactive API docs at http://localhost:1005/docs
- ✅ Database with sample data
- ✅ Hot reload for development

---

## 🎯 Prerequisites

### Required Software
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### Optional (Recommended)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)
- **VS Code** - [Download](https://code.visualstudio.com/)
- **Postman** - [Download](https://www.postman.com/)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone Repository (30 seconds)

```bash
git clone https://github.com/your-org/gaara-ai.git
cd gaara-ai
```

### Step 2: Setup Backend (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install additional packages
pip install qrcode[pil] python-jose[cryptography] passlib[bcrypt]
```

### Step 3: Configure Environment (1 minute)

Create `backend/.env`:

```env
# Database (SQLite for quick start)
DATABASE_URL=sqlite:///./gaara_scan_ai.db

# Application
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=dev-jwt-secret-change-in-production
DEBUG=True
APP_PORT=1005

# CORS (allow frontend)
ALLOWED_ORIGINS=http://localhost:1505,http://localhost:5173

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Step 4: Initialize Database (30 seconds)

```bash
# Run migrations
alembic upgrade head

# Create admin user (optional)
python scripts/create_admin.py
```

### Step 5: Start Backend (10 seconds)

```bash
# Start development server
cd src
python main.py
```

**Backend is now running at:** http://localhost:1005
**API Docs:** http://localhost:1005/docs

### Step 6: Setup Frontend (1 minute)

Open a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend is now running at:** http://localhost:1505

---

## ✅ Verify Installation

### Test Backend

```bash
# Health check
curl http://localhost:1005/health

# Expected response:
{
  "status": "healthy",
  "service": "Gaara AI Backend",
  "version": "3.0.0"
}
```

### Test Frontend

Open browser: http://localhost:1505

You should see the Gaara AI login page.

---

## 🎓 First Steps

### 1. Create Your First User

**Via API (Postman or curl):**

```bash
curl -X POST http://localhost:1005/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@gaara.ai",
    "password": "SecureP@ssw0rd123",
    "name": "Developer User"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "developer@gaara.ai",
    "name": "Developer User",
    "role": "USER"
  }
}
```

### 2. Login

```bash
curl -X POST http://localhost:1005/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@gaara.ai",
    "password": "SecureP@ssw0rd123"
  }'
```

### 3. Create Your First Farm

```bash
curl -X POST http://localhost:1005/api/v1/farms \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Test Farm",
    "location": "California, USA",
    "area": 100,
    "crop_type": "wheat"
  }'
```

### 4. Explore API Documentation

Visit: http://localhost:1005/docs

Try out all endpoints interactively!

---

## 📁 Project Structure

```
gaara-ai/
├── backend/                    # Backend API
│   ├── src/
│   │   ├── api/v1/            # API routes
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── farms.py       # Farms CRUD
│   │   │   ├── diagnosis.py   # Diagnosis
│   │   │   └── reports.py     # Reports
│   │   ├── models/            # Database models
│   │   │   ├── user.py
│   │   │   ├── farm.py
│   │   │   ├── diagnosis.py
│   │   │   └── report.py
│   │   ├── utils/             # Utilities
│   │   │   ├── security.py
│   │   │   └── password_policy.py
│   │   ├── modules/           # Feature modules
│   │   │   └── mfa/
│   │   ├── middleware/        # Custom middleware
│   │   └── core/              # Core configuration
│   ├── tests/                 # Tests
│   ├── alembic/               # Database migrations
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
│
├── frontend/                   # Frontend app
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── hooks/             # Custom hooks
│   │   └── utils/             # Utilities
│   ├── package.json           # Node dependencies
│   └── .env                   # Environment variables
│
└── docs/                       # Documentation
    ├── API_DOCUMENTATION.md
    ├── DATABASE_SCHEMA.md
    ├── DEPLOYMENT_GUIDE.md
    └── QUICK_START_GUIDE.md
```

---

## 🛠️ Development Workflow

### Backend Development

```bash
# Activate virtual environment
cd backend
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Start development server (auto-reload enabled)
cd src
python main.py

# Run tests
cd ..
pytest -v

# Run specific test
pytest tests/test_api_quick.py -v

# Check code coverage
pytest --cov=src --cov-report=html

# Run linting
flake8 src/
black src/

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend Development

```bash
cd frontend

# Start development server (hot reload)
npm run dev

# Run tests
npm test

# Run linting
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🧪 Testing

### Run All Tests

```bash
# Backend
cd backend
pytest -v

# Frontend
cd frontend
npm test
```

### Run Specific Tests

```bash
# Backend - Unit tests
pytest tests/unit/ -v

# Backend - Integration tests
pytest tests/integration/ -v

# Backend - API tests
pytest tests/test_api_quick.py -v

# Frontend - Component tests
npm test -- --testPathPattern=components
```

### Test Coverage

```bash
# Backend
pytest --cov=src --cov-report=html
# Open htmlcov/index.html

# Frontend
npm test -- --coverage
# Open coverage/lcov-report/index.html
```

---

## 🐛 Debugging

### Backend Debugging (VS Code)

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": false,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

### Frontend Debugging (VS Code)

Install "Debugger for Chrome" extension, then create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

---

## 📝 Common Tasks

### Add a New API Endpoint

1. Create route in `backend/src/api/v1/your_module.py`
2. Add Pydantic schemas
3. Implement business logic
4. Write tests in `backend/tests/`
5. Update API documentation

### Add a New Database Model

1. Create model in `backend/src/models/your_model.py`
2. Import in `backend/src/models/__init__.py`
3. Create migration: `alembic revision --autogenerate -m "Add your_model"`
4. Apply migration: `alembic upgrade head`
5. Write tests

### Add a New Frontend Page

1. Create component in `frontend/src/pages/YourPage.tsx`
2. Add route in `frontend/src/App.tsx`
3. Create API service in `frontend/src/services/yourService.ts`
4. Write tests

---

## 🔧 Troubleshooting

### Backend Won't Start

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

**Problem:** `Database connection error`

**Solution:**
```bash
# Check .env file exists
cat .env

# For SQLite, ensure database file exists
alembic upgrade head
```

---

**Problem:** `Port 1005 already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :1005
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:1005 | xargs kill -9
```

### Frontend Won't Start

**Problem:** `npm ERR! missing script: dev`

**Solution:**
```bash
cd frontend
npm install
npm run dev
```

---

**Problem:** `CORS error when calling API`

**Solution:**
Check `backend/.env`:
```env
ALLOWED_ORIGINS=http://localhost:1505,http://localhost:5173
```

---

## 📚 Useful Commands

### Backend

```bash
# Install new package
pip install package-name
pip freeze > requirements.txt

# Database
alembic upgrade head          # Apply all migrations
alembic downgrade -1          # Rollback one migration
alembic current               # Show current version
alembic history               # Show migration history

# Testing
pytest -v                     # Run all tests
pytest -k test_name           # Run specific test
pytest --cov=src              # Run with coverage
pytest -x                     # Stop on first failure
pytest --pdb                  # Drop into debugger on failure
```

### Frontend

```bash
# Install new package
npm install package-name
npm install -D package-name   # Dev dependency

# Development
npm run dev                   # Start dev server
npm run build                 # Build for production
npm run preview               # Preview production build
npm run lint                  # Run linter
npm run format                # Format code
```

---

## 🎯 Next Steps

1. **Read the Documentation**
   - API_DOCUMENTATION.md
   - DATABASE_SCHEMA.md
   - Security.md

2. **Explore the Codebase**
   - Start with `backend/src/main.py`
   - Check out `backend/src/api/v1/`
   - Look at `frontend/src/App.tsx`

3. **Make Your First Contribution**
   - Pick an issue from GitHub
   - Create a feature branch
   - Write tests
   - Submit a pull request

4. **Join the Community**
   - Discord: https://discord.gg/gaara-ai
   - GitHub Discussions: https://github.com/your-org/gaara-ai/discussions

---

## 📞 Get Help

**Documentation:** https://docs.gaara-ai.com  
**Issues:** https://github.com/your-org/gaara-ai/issues  
**Discord:** https://discord.gg/gaara-ai  
**Email:** dev@gaara-ai.com

---

**Generated by:** Autonomous AI Agent  
**Framework:** GLOBAL_PROFESSIONAL_CORE_PROMPT v16.0  
**Status:** ✅ Ready to Use

---

