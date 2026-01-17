# Interactive Project Setup System - User Guide

## Overview

The Interactive Project Setup System is a comprehensive solution that:
- Collects project information at the start
- Manages project state (Development/Production)
- Automates deployment process
- Provides phase-specific behavior

---

## Quick Start

### 1. Initial Setup

When starting a new project with Augment:

```bash
# Augment will automatically detect no configuration and ask:
"I notice this is a new project. Let me collect some information..."

# Or manually run:
python3 tools/project_config_manager.py setup
```

### 2. Answer Questions

Augment will ask you about:
1. **Project Phase** - Development or Production?
2. **Project Name** - What's your app called?
3. **Deployment Status** - First time or already deployed?
4. **Port Configuration** - Frontend, Backend, Database ports
5. **Database Configuration** - Name, preserve data, sample data
6. **Environment** - Local or External (domain)
7. **Admin User** - Username, email, password (Production only)

### 3. Configuration Saved

Your answers are saved to `.global/project_config.json`

Augment will use this configuration throughout the project.

---

## Usage Examples

### Example 1: New Development Project

```
User: "I want to create a new e-commerce platform"

Augment: "Great! Let me collect some information first..."

[Questionnaire]
1. Project Phase: [D] Development
2. Project Name: E-Commerce Platform
3. Deployed: [N] No
4. Frontend Port: 3000
5. Backend Port: 5000
6. Database Port: 5432
7. Database Name: ecommerce_db
8. Preserve Data: [N] No
9. Sample Data: [Y] Yes
10. Environment: [L] Local

✓ Configuration saved!

Augment: "Perfect! I've set up your development environment.
I'll use these settings throughout the project.

Your app will run at:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Database: ecommerce_db

I'll add sample data for testing. Ready to start?"
```

### Example 2: Existing Production Project

```
User: "I need to work on my existing production app"

Augment: "I notice there's no configuration. Let me collect info..."

[Questionnaire]
1. Project Phase: [P] Production
2. Project Name: MyApp
3. Deployed: [Y] Yes
4. Frontend Port: 80
5. Backend Port: 8000
6. Database Port: 5432
7. Database Name: myapp_production
8. Preserve Data: [Y] Yes
9. Environment: [E] External
10. Domain: myapp.com
11. Admin Username: admin
12. Admin Email: admin@myapp.com

✓ Configuration saved!

Augment: "Configuration loaded. I'll be extra careful with your
production database and won't make any destructive changes
without your explicit confirmation."
```

### Example 3: Deploying to Production

```
User: "start deploy"

Augment: "🚀 Starting deployment process...

⚠️  WARNING: This will transition your project to PRODUCTION mode.

Current configuration:
  - Project: E-Commerce Platform
  - Database: ecommerce_db
  - Frontend: http://localhost:3000
  - Backend: http://localhost:5000

Are you sure you want to proceed? [Y/n]:"

User: "Y"

Augment: "
✓ Pre-deployment checks passed
✓ Database backed up to: backups/deploy_20251102_103000/
✓ Production build created
✓ Database migrations applied
✓ Admin user created: admin
✓ Security hardening applied
✓ Application started

🎉 Deployment successful!

Admin Panel: http://localhost:5000/admin
Username: admin
Password: Xy9#mK2$pL4@

Setup Wizard: http://localhost:3000/setup

⚠️  IMPORTANT: Save these credentials securely!

Opening admin panel and setup wizard..."
```

---

## Configuration File

### Location

`.global/project_config.json`

### Structure

```json
{
  "project": {
    "name": "E-Commerce Platform",
    "phase": "development",
    "deployed": false,
    "created_at": "2025-11-02T10:30:00Z",
    "updated_at": "2025-11-02T10:30:00Z"
  },
  "ports": {
    "frontend": 3000,
    "backend": 5000,
    "database": 5432
  },
  "database": {
    "name": "ecommerce_db",
    "preserve_data": false,
    "add_sample_data": true,
    "type": "postgresql",
    "host": "localhost",
    "port": 5432
  },
  "environment": {
    "type": "local",
    "host": "localhost",
    "domain": null,
    "ip_address": null
  },
  "admin": {
    "username": "admin",
    "email": "admin@example.com",
    "password_hash": null,
    "created": false
  },
  "features": {
    "auto_backup": true,
    "logging": true,
    "monitoring": true
  }
}
```

### Manual Editing

You can edit this file manually:

```bash
nano .global/project_config.json
```

After editing, tell Augment to reload:

```
User: "reload configuration"

Augment: "✓ Configuration reloaded from .global/project_config.json"
```

---

## Commands

### Configuration Management

```bash
# Interactive setup
python3 tools/project_config_manager.py setup

# Show current configuration
python3 tools/project_config_manager.py show

# Generate .env file from configuration
python3 tools/project_config_manager.py env

# Deploy to production
python3 tools/project_config_manager.py deploy
```

### Deployment

```bash
# Start deployment process
./scripts/start_deploy.sh

# Or tell Augment:
User: "start deploy"
```

### Development Commands

```bash
# Reset database (Development only)
User: "reset database"

# Add sample data (Development only)
User: "seed database"

# Clear caches
User: "clear cache"
```

### Production Commands

```bash
# Backup database
User: "backup database"

# Check system health
User: "health check"

# View logs
User: "show logs"
```

---

## Phase-Specific Behavior

### Development Phase

**Augment will:**
- ✅ Allow destructive database operations
- ✅ Add sample/test data
- ✅ Enable debug mode
- ✅ Show detailed error messages
- ✅ Allow quick iterations

**Example:**
```
User: "drop the database and start fresh"

Augment: "Sure! Since we're in development mode, I'll:
1. Drop the database 'ecommerce_db'
2. Recreate it
3. Run migrations
4. Add sample data

Proceeding..."
```

### Production Phase

**Augment will:**
- ❌ Refuse destructive operations
- ✅ Require confirmation for changes
- ✅ Create backups automatically
- ✅ Use production-safe settings
- ✅ Preserve all data

**Example:**
```
User: "drop the database"

Augment: "⚠️  DANGER: You're in PRODUCTION mode!

I cannot drop the production database without explicit confirmation.

This will:
- Delete ALL data in 'myapp_production'
- Affect live users
- Require restoration from backup

Are you ABSOLUTELY sure? Type 'DELETE PRODUCTION DATABASE' to confirm:"
```

---

## Best Practices

### 1. Always Run Setup First

```bash
# First thing when starting a project
python3 tools/project_config_manager.py setup
```

### 2. Use Correct Phase

- **Development:** For active development, testing, experiments
- **Production:** For live, deployed applications

### 3. Backup Before Deployment

```bash
# Automatic backup is created, but you can also:
User: "backup database before deployment"
```

### 4. Review Configuration

```bash
# Before deployment, review:
python3 tools/project_config_manager.py show
```

### 5. Test in Development

- Always test thoroughly in development
- Use sample data to simulate production
- Run all tests before deploying

### 6. Secure Production

- Use strong passwords
- Enable HTTPS
- Configure firewall
- Set up monitoring

---

## Troubleshooting

### Configuration Not Found

```
Error: No configuration found!

Solution:
python3 tools/project_config_manager.py setup
```

### Wrong Phase

```
User: "I'm in the wrong phase, how do I change?"

Augment: "You can either:

1. Edit manually:
   nano .global/project_config.json
   Change: "phase": "development" or "production"

2. Run setup again:
   python3 tools/project_config_manager.py setup

3. For deployment:
   ./scripts/start_deploy.sh
"
```

### Lost Admin Password

```
User: "I forgot my admin password"

Augment: "For security, passwords are hashed. You can:

1. Reset via Django:
   python manage.py changepassword admin

2. Or recreate admin user:
   python manage.py createsuperuser
"
```

### Deployment Failed

```
User: "deployment failed, how do I rollback?"

Augment: "I created a backup before deployment:

Backup location: backups/deploy_20251102_103000/

To restore:
1. Restore database:
   psql myapp_db < backups/deploy_20251102_103000/database.sql

2. Restore configuration:
   cp backups/deploy_20251102_103000/.global/project_config.json .global/

3. Restart services
"
```

---

## Integration with Augment

### How Augment Uses Configuration

1. **At Start:**
   - Checks for `.global/project_config.json`
   - If not found, runs interactive setup
   - Loads configuration into memory

2. **During Development:**
   - Uses config values instead of hardcoded
   - Respects project phase
   - Adjusts behavior accordingly

3. **For Deployment:**
   - Runs pre-deployment checks
   - Creates backups
   - Transitions to production
   - Opens admin panel and setup wizard

### Example Augment Behavior

```python
# Augment's internal logic

# Load configuration
config = load_config()

# Use throughout
if config['project']['phase'] == 'development':
    # Development mode
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    DATABASE_PRESERVE = False
else:
    # Production mode
    DEBUG = False
    ALLOWED_HOSTS = [config['environment']['host']]
    DATABASE_PRESERVE = True

# Use config values
APP_NAME = config['project']['name']
DATABASE_NAME = config['database']['name']
FRONTEND_PORT = config['ports']['frontend']
```

---

## Advanced Usage

### Multiple Environments

You can have different configurations:

```bash
# Development
cp .global/project_config.json .global/config.dev.json

# Staging
cp .global/project_config.json .global/config.staging.json

# Production
cp .global/project_config.json .global/config.prod.json

# Switch between them
cp .global/config.prod.json .global/project_config.json
```

### Custom Scripts

Create custom scripts that use the configuration:

```python
#!/usr/bin/env python3
import json

# Load configuration
with open('.global/project_config.json') as f:
    config = json.load(f)

# Use it
print(f"Project: {config['project']['name']}")
print(f"Phase: {config['project']['phase']}")
```

### CI/CD Integration

Use configuration in CI/CD:

```yaml
# .github/workflows/deploy.yml
- name: Deploy
  run: |
    python3 tools/project_config_manager.py deploy
    ./scripts/start_deploy.sh
```

---

## Summary

The Interactive Project Setup System:

✅ **Eliminates hardcoded values**  
✅ **Provides project-specific configuration**  
✅ **Manages development/production phases**  
✅ **Automates deployment**  
✅ **Ensures data safety**  
✅ **Integrates with Augment**

**Result:** Professional, safe, automated project management from development to production.

---

## Support

For issues or questions:
- Check Section 64 in GLOBAL_GUIDELINES
- Review this guide
- Check configuration file
- Run: `python3 tools/project_config_manager.py show`

