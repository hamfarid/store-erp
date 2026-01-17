## Section 64: Interactive Project Setup & State Management

### Overview

This section defines an **interactive project setup system** that collects project information at the start and manages project state throughout development and deployment phases.

---

### 64.1 Initial Project Questions

**When to Ask:**
- At the very beginning of a new project
- When user starts working on a project for the first time
- When project configuration file doesn't exist

**Questions to Ask:**

```
╔════════════════════════════════════════════════════════════════╗
║           PROJECT CONFIGURATION QUESTIONNAIRE                  ║
╚════════════════════════════════════════════════════════════════╝

I need to collect some information about your project to provide 
better assistance. Please answer the following questions:

1. PROJECT PHASE
   ─────────────
   Are you in Development or Production phase?
   
   Options:
   [D] Development - Active development, testing, debugging
   [P] Production  - Live deployment, production environment
   
   Your choice: ___

2. PROJECT NAME
   ────────────
   What is your project/application name?
   
   Example: "MyAwesomeApp", "E-Commerce Platform", "Task Manager"
   
   Project Name: _______________

3. DEPLOYMENT STATUS
   ─────────────────
   Has this project been deployed before?
   
   Options:
   [Y] Yes - Already deployed to production
   [N] No  - First time deployment
   
   Your choice: ___

4. PORT CONFIGURATION
   ──────────────────
   
   a) Frontend Port (if applicable):
      Default: 3000
      Your port: _____ (press Enter for default)
   
   b) Backend/API Port:
      Default: 5000
      Your port: _____ (press Enter for default)
   
   c) Database Port:
      Default: 5432 (PostgreSQL) / 3306 (MySQL) / 27017 (MongoDB)
      Your port: _____ (press Enter for default)

5. DATABASE CONFIGURATION
   ──────────────────────
   
   a) Database Name:
      Example: "myapp_db", "production_db"
      Database Name: _______________
   
   b) Should I preserve existing database data?
      [Y] Yes - Keep existing data (production mode)
      [N] No  - Fresh start, drop and recreate (development mode)
      
      Your choice: ___
   
   c) Add test/sample data? (Development only)
      [Y] Yes - Add sample data for testing
      [N] No  - Empty database
      
      Your choice: ___ (Only if Development phase)

6. ENVIRONMENT
   ───────────
   Where will this run?
   
   Options:
   [L] Local    - localhost, 127.0.0.1
   [E] External - Custom domain, cloud server
   
   Your choice: ___
   
   If External, please provide:
   - Host/Domain: _______________
   - IP Address (optional): _______________

7. ADMIN USER (Production only)
   ─────────────────────────────
   
   a) Admin Username:
      Default: admin
      Username: _____ (press Enter for default)
   
   b) Admin Email:
      Email: _______________
   
   c) Admin Password:
      (Will be generated securely if not provided)
      Password: _____ (optional)

╔════════════════════════════════════════════════════════════════╗
║                    CONFIGURATION SUMMARY                       ║
╚════════════════════════════════════════════════════════════════╝

I will now create a configuration file with your answers.
You can review and modify it at any time.

Configuration file: .global/project_config.json

```

---

### 64.2 Configuration File Structure

**Location:** `.global/project_config.json`

**Structure:**

```json
{
  "project": {
    "name": "{PROJECT_NAME}",
    "phase": "development|production",
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
    "name": "{DATABASE_NAME}",
    "preserve_data": false,
    "add_sample_data": true,
    "type": "postgresql|mysql|mongodb",
    "host": "localhost",
    "port": 5432
  },
  "environment": {
    "type": "local|external",
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

---

### 64.3 State Management

**Project States:**

```
┌─────────────────────────────────────────────────────────────┐
│                      PROJECT STATES                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DEVELOPMENT                                             │
│     ├─ Active development                                   │
│     ├─ Testing enabled                                      │
│     ├─ Debug mode ON                                        │
│     ├─ Sample data available                                │
│     ├─ Hot reload enabled                                   │
│     └─ Detailed logging                                     │
│                                                             │
│  2. STAGING (Optional)                                      │
│     ├─ Pre-production testing                               │
│     ├─ Production-like environment                          │
│     ├─ Performance testing                                  │
│     └─ Final QA                                             │
│                                                             │
│  3. PRODUCTION                                              │
│     ├─ Live deployment                                      │
│     ├─ Debug mode OFF                                       │
│     ├─ Optimized builds                                     │
│     ├─ Data preservation ON                                 │
│     ├─ Security hardened                                    │
│     └─ Monitoring active                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**State Transitions:**

```
Development ──[start deploy]──> Production
     ↑                              │
     │                              │
     └───────[rollback]─────────────┘
```

---

### 64.4 Development Phase Behavior

**When `phase: "development"`:**

1. **Configuration:**
   - Debug mode: ON
   - Hot reload: Enabled
   - Detailed logging: ON
   - CORS: Permissive
   - Sample data: Available

2. **Database:**
   - Can drop/recreate freely
   - Sample data can be added
   - Migrations run automatically
   - Backup optional

3. **Security:**
   - Relaxed (for development only)
   - Test credentials allowed
   - HTTPS optional
   - CSRF optional (for testing)

4. **Monitoring:**
   - Console logging
   - Detailed error messages
   - Stack traces visible
   - Performance profiling

5. **Commands Available:**
   - `reset-db` - Drop and recreate database
   - `seed-data` - Add sample data
   - `clear-cache` - Clear all caches
   - `start deploy` - Begin deployment process

---

### 64.5 Production Phase Behavior

**When `phase: "production"`:**

1. **Configuration:**
   - Debug mode: OFF
   - Hot reload: Disabled
   - Minimal logging: ON
   - CORS: Strict
   - Sample data: NOT available

2. **Database:**
   - Data preservation: MANDATORY
   - Backups: Automatic
   - Migrations: Careful, with backups
   - No destructive operations

3. **Security:**
   - Strict security policies
   - Strong credentials required
   - HTTPS: MANDATORY
   - CSRF protection: ON
   - Rate limiting: ON

4. **Monitoring:**
   - Production logging
   - Error tracking (Sentry, etc.)
   - Performance monitoring
   - Uptime monitoring

5. **Commands Available:**
   - `backup-db` - Create database backup
   - `restore-db` - Restore from backup
   - `rollback` - Rollback to previous version
   - `health-check` - Check system health

---

### 64.6 The `start deploy` Command

**Purpose:** Transition from Development to Production

**Workflow:**

```
┌─────────────────────────────────────────────────────────────┐
│              START DEPLOY WORKFLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Pre-Deployment Checks                              │
│  ─────────────────────────────                              │
│  ✓ All tests passing                                        │
│  ✓ No uncommitted changes                                   │
│  ✓ Database migrations ready                                │
│  ✓ Environment variables set                                │
│  ✓ SSL certificates valid                                   │
│  ✓ Dependencies up to date                                  │
│                                                             │
│  Step 2: Backup Current State                               │
│  ────────────────────────────                               │
│  ✓ Backup database                                          │
│  ✓ Backup configuration files                               │
│  ✓ Backup uploaded files                                    │
│  ✓ Create restore point                                     │
│                                                             │
│  Step 3: Build Production Assets                            │
│  ───────────────────────────────                            │
│  ✓ Build frontend (minified)                                │
│  ✓ Build backend (optimized)                                │
│  ✓ Compile assets                                           │
│  ✓ Generate static files                                    │
│                                                             │
│  Step 4: Database Setup                                     │
│  ─────────────────────                                      │
│  ✓ Run migrations                                           │
│  ✓ Create admin user                                        │
│  ✓ Set up initial data                                      │
│  ✓ Verify database integrity                                │
│                                                             │
│  Step 5: Security Hardening                                 │
│  ──────────────────────                                     │
│  ✓ Enable HTTPS                                             │
│  ✓ Set secure headers                                       │
│  ✓ Configure firewall                                       │
│  ✓ Enable rate limiting                                     │
│  ✓ Set strong passwords                                     │
│                                                             │
│  Step 6: Launch Application                                 │
│  ──────────────────────                                     │
│  ✓ Start services                                           │
│  ✓ Health check                                             │
│  ✓ Open admin panel                                         │
│  ✓ Open setup wizard                                        │
│                                                             │
│  Step 7: Post-Deployment                                    │
│  ──────────────────────                                     │
│  ✓ Update project phase to "production"                     │
│  ✓ Enable monitoring                                        │
│  ✓ Send deployment notification                             │
│  ✓ Create deployment log                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Command Usage:**

```bash
# User types:
start deploy

# Augment responds:
🚀 Starting deployment process...

⚠️  WARNING: This will transition your project to PRODUCTION mode.

Current configuration:
  - Project: {PROJECT_NAME}
  - Database: {DATABASE_NAME}
  - Frontend: http://{HOST}:{FRONTEND_PORT}
  - Backend: http://{HOST}:{BACKEND_PORT}

Are you sure you want to proceed? [Y/n]: _

# If Yes:
✓ Pre-deployment checks passed
✓ Database backed up to: backups/db_20251102_103000.sql
✓ Production build created
✓ Database migrations applied
✓ Admin user created: {ADMIN_USERNAME}
✓ Security hardening applied
✓ Application started

🎉 Deployment successful!

Admin Panel: http://{HOST}:{BACKEND_PORT}/admin
Username: {ADMIN_USERNAME}
Password: {GENERATED_PASSWORD}

Setup Wizard: http://{HOST}:{FRONTEND_PORT}/setup

Next steps:
1. Login to admin panel
2. Complete setup wizard
3. Configure your application
4. Verify everything works

Project phase updated: PRODUCTION ✓
```

---

### 64.7 Admin Panel Auto-Open

**After `start deploy`:**

1. **Create Admin User:**
   ```python
   admin_user = {
       "username": config["admin"]["username"],
       "email": config["admin"]["email"],
       "password": generate_secure_password(),
       "is_superuser": True,
       "is_staff": True
   }
   ```

2. **Open Admin Panel:**
   ```python
   admin_url = f"http://{config['environment']['host']}:{config['ports']['backend']}/admin"
   webbrowser.open(admin_url)
   ```

3. **Open Setup Wizard:**
   ```python
   setup_url = f"http://{config['environment']['host']}:{config['ports']['frontend']}/setup"
   webbrowser.open(setup_url)
   ```

4. **Display Credentials:**
   ```
   ╔════════════════════════════════════════════════════════════╗
   ║                  ADMIN CREDENTIALS                         ║
   ╚════════════════════════════════════════════════════════════╝
   
   Admin Panel: http://{HOST}:{BACKEND_PORT}/admin
   
   Username: {ADMIN_USERNAME}
   Password: {GENERATED_PASSWORD}
   
   ⚠️  IMPORTANT: Save these credentials securely!
   ⚠️  Change the password after first login.
   
   Setup Wizard: http://{HOST}:{FRONTEND_PORT}/setup
   
   Follow the setup wizard to:
   - Configure application settings
   - Set up database connections
   - Configure email settings
   - Set up payment gateways (if applicable)
   - Configure integrations
   ```

---

### 64.8 Setup Wizard Flow

**After deployment, setup wizard guides through:**

```
┌─────────────────────────────────────────────────────────────┐
│                    SETUP WIZARD STEPS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Welcome                                            │
│  ──────────────                                             │
│  - Welcome message                                          │
│  - System requirements check                                │
│  - License agreement (if applicable)                        │
│                                                             │
│  Step 2: Database Configuration                             │
│  ──────────────────────────                                 │
│  - Database connection test                                 │
│  - Run migrations                                           │
│  - Create initial tables                                    │
│  - Verify database setup                                    │
│                                                             │
│  Step 3: Admin Account                                      │
│  ─────────────────────                                      │
│  - Confirm admin credentials                                │
│  - Set up 2FA (optional)                                    │
│  - Configure admin email                                    │
│                                                             │
│  Step 4: Application Settings                               │
│  ────────────────────────────                               │
│  - Site name and description                                │
│  - Timezone and locale                                      │
│  - Currency settings                                        │
│  - Date/time formats                                        │
│                                                             │
│  Step 5: Email Configuration                                │
│  ───────────────────────────                                │
│  - SMTP settings                                            │
│  - Test email sending                                       │
│  - Email templates                                          │
│                                                             │
│  Step 6: Security Settings                                  │
│  ─────────────────────────                                  │
│  - Password policies                                        │
│  - Session timeout                                          │
│  - IP whitelist/blacklist                                   │
│  - Rate limiting                                            │
│                                                             │
│  Step 7: Integrations (Optional)                            │
│  ───────────────────────────────                            │
│  - Payment gateways                                         │
│  - Analytics                                                │
│  - Social login                                             │
│  - Third-party APIs                                         │
│                                                             │
│  Step 8: Final Review                                       │
│  ────────────────────                                       │
│  - Review all settings                                      │
│  - Run final tests                                          │
│  - Complete setup                                           │
│  - Redirect to dashboard                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 64.9 Augment Behavior Guidelines

**At Project Start:**

1. **Check for existing config:**
   ```python
   if not os.path.exists('.global/project_config.json'):
       # Ask all questions
       collect_project_info()
   else:
       # Load existing config
       config = load_config()
       print(f"Loaded config for: {config['project']['name']}")
       print(f"Phase: {config['project']['phase']}")
   ```

2. **Use config throughout:**
   ```python
   # Always use config values
   project_name = config['project']['name']
   db_name = config['database']['name']
   frontend_port = config['ports']['frontend']
   
   # Never hardcode values
   # ❌ APP_NAME = "Gaara ERP"
   # ✓ APP_NAME = config['project']['name']
   ```

3. **Respect project phase:**
   ```python
   if config['project']['phase'] == 'development':
       # Development behavior
       enable_debug_mode()
       allow_sample_data()
       relaxed_security()
   else:
       # Production behavior
       disable_debug_mode()
       strict_security()
       enable_monitoring()
   ```

---

### 64.10 Commands Reference

**Development Phase:**

```bash
# Database
reset-db              # Drop and recreate database
seed-data             # Add sample data
migrate-db            # Run migrations
backup-db             # Create backup

# Development
dev-server            # Start development server
hot-reload            # Enable hot reload
clear-cache           # Clear all caches
run-tests             # Run test suite

# Deployment
start deploy          # Begin deployment process
```

**Production Phase:**

```bash
# Database
backup-db             # Create database backup
restore-db [file]     # Restore from backup
migrate-db            # Run migrations (with backup)

# Monitoring
health-check          # Check system health
view-logs             # View application logs
monitor-stats         # View performance stats

# Management
rollback              # Rollback to previous version
restart-services      # Restart all services
update-config         # Update configuration
```

---

### 64.11 Configuration Update

**To update configuration:**

```bash
# Interactive update
update-config

# Direct edit
nano .global/project_config.json

# Reload config
reload-config
```

**Augment will ask:**

```
Which setting would you like to update?

1. Project name
2. Port configuration
3. Database settings
4. Environment settings
5. Admin settings
6. All settings

Your choice: ___
```

---

### 64.12 Best Practices

**For Augment:**

1. **Always ask questions first** if no config exists
2. **Use config values** throughout the project
3. **Respect project phase** in all operations
4. **Never hardcode** project-specific values
5. **Backup before** destructive operations
6. **Verify** before production deployment
7. **Log** all important operations
8. **Notify user** of phase transitions

**For Users:**

1. **Answer questions carefully** - they affect the entire project
2. **Review config** before deployment
3. **Backup** before `start deploy`
4. **Test thoroughly** in development
5. **Use staging** if available
6. **Monitor** after deployment
7. **Keep credentials** secure

---

### 64.13 Integration with Existing Sections

**This section integrates with:**

- **Section 0-3:** Core directives and constraints
- **Section 40:** Definitions Registry (uses config)
- **Section 63:** Global Repository (tools use config)
- **All sections:** Use config values instead of hardcoded

**Example Integration:**

```python
# Section 40: Definitions Registry
# Before:
APP_NAME = "Gaara ERP"

# After:
from .global.project_config import load_config
config = load_config()
APP_NAME = config['project']['name']
```

---

### 64.14 Summary

**This section provides:**

✅ Interactive project setup questionnaire  
✅ Configuration file management  
✅ State management (Development/Production)  
✅ `start deploy` command workflow  
✅ Admin panel auto-open  
✅ Setup wizard integration  
✅ Phase-specific behavior  
✅ Best practices for Augment and users

**Result:**

- No more hardcoded values
- Project-specific configuration
- Smooth development-to-production transition
- Automated deployment process
- Professional setup experience

---

**End of Section 64**

