# Environment Separation Examples

## ⚠️ CRITICAL: Keep Environments Separate!

This document provides clear examples of how to keep Global Guidelines environment separate from your project environment.

---

## 📁 Directory Structure

### ✅ CORRECT: Separate Environments

```
/home/user/
├── global/                          # Global Guidelines (instruction manual)
│   ├── prompts/                     # Guidance modules
│   ├── .global/                     # Helper tools environment
│   │   ├── data/
│   │   │   └── memory.db            # For Global Guidelines helpers only
│   │   ├── docker-compose.yml       # For Global Guidelines helpers only
│   │   ├── config/
│   │   │   └── settings.yml         # For Global Guidelines helpers only
│   │   ├── tools/                   # Analysis tools
│   │   ├── scripts/                 # Integration scripts
│   │   └── templates/               # Templates to copy
│   └── GLOBAL_GUIDELINES_UNIFIED_v8.0.0.txt
│
└── my-awesome-project/              # Your actual project
    ├── src/                         # Your source code
    ├── database/
    │   └── app.db                   # Your project database
    ├── docker-compose.yml           # Your project Docker setup
    ├── .env                         # Your project config
    ├── requirements.txt
    └── README.md
```

### ❌ WRONG: Mixed Environments

```
/home/user/
└── global/                          # DON'T DO THIS!
    ├── prompts/
    ├── .global/
    │   └── data/
    │       ├── memory.db            # Helper tools database
    │       └── my_project_data.db   # ❌ WRONG! Project data in .global/
    ├── my-project-code/             # ❌ WRONG! Project inside Global Guidelines
    │   └── src/
    └── docker-compose.yml           # ❌ WRONG! Mixing containers
```

---

## 🗄️ Database Separation

### ✅ CORRECT: Separate Databases

```bash
# Global Guidelines helper tools database
~/global/.global/data/memory.db
Purpose: Store context for Global Guidelines helper tools
Used by: .global/tools/memory_manager.py (optional)
Schema: Helper tool specific

# Your project database
~/my-awesome-project/database/app.db
Purpose: Store your application data
Used by: Your application code
Schema: Your application specific
```

### ❌ WRONG: Shared Database

```bash
# DON'T DO THIS!
~/global/.global/data/memory.db
  ├── helper_tools_table     # Global Guidelines data
  └── my_project_users       # ❌ WRONG! Project data mixed in
```

---

## 🐳 Docker Separation

### ✅ CORRECT: Separate Docker Setups

**Global Guidelines Docker (Optional):**
```yaml
# ~/global/.global/docker-compose.yml
version: '3.8'
services:
  global-helper-db:
    image: postgres:15
    environment:
      POSTGRES_DB: global_helpers
      POSTGRES_USER: global_helper
    volumes:
      - ./data:/var/lib/postgresql/data
    # Only for Global Guidelines helper tools
```

**Your Project Docker:**
```yaml
# ~/my-awesome-project/docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/myapp
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myapp_user
    volumes:
      - ./database:/var/lib/postgresql/data
    # For YOUR application
```

### ❌ WRONG: Mixed Docker Setup

```yaml
# DON'T DO THIS!
# ~/global/.global/docker-compose.yml
version: '3.8'
services:
  global-helper-db:
    # Global Guidelines helper
  
  my-app:              # ❌ WRONG! Your app in Global Guidelines Docker
    build: ../my-project
  
  my-app-db:           # ❌ WRONG! Your database in Global Guidelines Docker
    image: postgres:15
```

---

## ⚙️ Configuration Separation

### ✅ CORRECT: Separate Configs

**Global Guidelines Config (Optional):**
```yaml
# ~/global/.global/config/settings.yml
helper_tools:
  memory_db_path: ./data/memory.db
  log_level: INFO
  # Only for Global Guidelines helpers
```

**Your Project Config:**
```bash
# ~/my-awesome-project/.env
DATABASE_URL=postgresql://localhost/myapp
SECRET_KEY=your-secret-key
DEBUG=True
# Your application configuration
```

### ❌ WRONG: Mixed Config

```bash
# DON'T DO THIS!
# ~/global/.global/config/.env
GLOBAL_HELPER_DB=./data/memory.db    # Global Guidelines
MY_APP_DATABASE=postgres://...       # ❌ WRONG! Your app config mixed in
MY_APP_SECRET_KEY=...                # ❌ WRONG!
```

---

## 🔧 Code Examples

### ✅ CORRECT: AI Behavior

```python
# When user asks: "Create a database for my project"

# AI should do:
project_path = ask_user("Where is your project located?")
# User: "~/my-awesome-project"

# Create database in user's project
db_path = f"{project_path}/database/app.db"
create_database(db_path)  # ✅ CORRECT!

# NOT in Global Guidelines
# ❌ WRONG: db_path = "~/global/.global/data/app.db"
```

### ✅ CORRECT: Using Templates

```bash
# When user asks: "Add authentication to my project"

# AI should do:
# 1. Copy template from Global Guidelines
cp -r ~/global/.global/templates/auth ~/my-awesome-project/src/auth

# 2. Customize for user's project
cd ~/my-awesome-project
# Edit files in ~/my-awesome-project/src/auth

# NOT modify Global Guidelines templates
# ❌ WRONG: Edit ~/global/.global/templates/auth
```

---

## 🎯 Environment Variables

### ✅ CORRECT: Separate Environment Variables

**Global Guidelines (Optional):**
```bash
# ~/global/.global/.env
GLOBAL_HELPER_DB_PATH=./data/memory.db
GLOBAL_LOG_LEVEL=INFO
```

**Your Project:**
```bash
# ~/my-awesome-project/.env
DATABASE_URL=postgresql://localhost/myapp
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
DEBUG=True
```

### ❌ WRONG: Shared Environment

```bash
# DON'T DO THIS!
# ~/global/.global/.env
GLOBAL_HELPER_DB_PATH=./data/memory.db
MY_APP_DATABASE_URL=...              # ❌ WRONG!
MY_APP_SECRET_KEY=...                # ❌ WRONG!
```

---

## 📊 Summary Table

| Aspect | Global Guidelines | Your Project | Separate? |
|--------|------------------|--------------|-----------|
| **Location** | `~/global/` | `~/my-awesome-project/` | ✅ YES |
| **Database** | `.global/data/memory.db` | `database/app.db` | ✅ YES |
| **Docker** | `.global/docker-compose.yml` | `docker-compose.yml` | ✅ YES |
| **Config** | `.global/config/settings.yml` | `.env` or `config/` | ✅ YES |
| **Code** | `prompts/` (guidance) | `src/` (your code) | ✅ YES |
| **Purpose** | Instruction manual | Your application | ✅ YES |

---

## ⚠️ Common Mistakes

### Mistake 1: Using .global/ database for project
```python
# ❌ WRONG!
db = connect("~/global/.global/data/memory.db")
db.create_table("users")  # Your project table

# ✅ CORRECT!
db = connect("~/my-project/database/app.db")
db.create_table("users")  # Your project table
```

### Mistake 2: Putting project code in Global Guidelines
```bash
# ❌ WRONG!
~/global/my-project-code/
~/global/.global/my-app/

# ✅ CORRECT!
~/my-project/
~/projects/my-app/
```

### Mistake 3: Mixing Docker containers
```yaml
# ❌ WRONG! (in ~/global/.global/docker-compose.yml)
services:
  global-helper:
    ...
  my-app:           # ❌ Your app container
    ...

# ✅ CORRECT! (separate files)
# ~/global/.global/docker-compose.yml
services:
  global-helper:
    ...

# ~/my-project/docker-compose.yml
services:
  my-app:
    ...
```

---

## 🎓 Learning Points

1. **Global Guidelines = Instruction Manual**
   - Contains guidance, templates, examples
   - Has optional helper tools in `.global/`
   - NOT your project

2. **Your Project = Actual Application**
   - Your source code, database, config
   - Completely separate from Global Guidelines
   - Applies guidance from Global Guidelines

3. **Environments Must Be Separate**
   - Different databases
   - Different Docker setups
   - Different configurations
   - Different directories

4. **Templates Are Copied, Not Shared**
   - Copy from `.global/templates/` to your project
   - Customize in your project
   - Don't modify Global Guidelines templates

---

## 📝 Checklist for AI

When working on a user's project, verify:

- [ ] Asked user for project path (not assuming Global Guidelines)
- [ ] Creating files in user's project directory
- [ ] Using user's project database (not .global/data/)
- [ ] Using user's project Docker setup (not .global/docker-compose.yml)
- [ ] Using user's project config (not .global/config/)
- [ ] Keeping Global Guidelines separate
- [ ] Only copying templates from .global/ (not modifying them)
- [ ] Applying guidance TO user's project (not TO Global Guidelines)

---

**Remember: Global Guidelines is the cookbook, your project is the meal you're cooking!** 🍳

