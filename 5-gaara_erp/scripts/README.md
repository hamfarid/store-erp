# Gaara ERP - Scripts Directory

This directory contains utility scripts for development, deployment, and maintenance.

## 🚀 Quick Start Scripts

### Development Setup
```bash
./scripts/setup-dev.sh
```
Complete development environment setup with all prerequisites.

### Git Operations
```bash
# Windows (PowerShell)
.\scripts\git-push.ps1

# Linux/Mac
./scripts/git-setup.sh
./scripts/git-push.sh "Your commit message"
```

## 📋 Available Scripts

### Development
- `setup-dev.sh` - Complete development environment setup
- `seed-database.sh` - Seed database with initial data
- `run-tests.sh` - Run test suite with coverage
- `api-test.sh` - Test API endpoints
- `check-health.sh` - Check service health

### Deployment
- `deploy.sh` - Production deployment automation
- `backup-all.sh` - Complete system backup
- `clean.sh` - Cleanup containers and cache

### Git
- `git-setup.sh` - Initialize git and configure remote
- `git-push.sh` - Quick git push
- `git-push.ps1` - Git push (PowerShell for Windows)

### Utilities
- `generate-secret-key.sh` - Generate secure secret keys

## 📖 Usage

All scripts are executable. Make sure they have execute permissions:

```bash
chmod +x scripts/*.sh
```

For Windows PowerShell scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🔧 Script Details

See individual script files for detailed usage and options.
