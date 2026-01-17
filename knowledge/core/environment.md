# Knowledge Item: Environment Separation

> **Critical Concept:** Never mix helper tools with user's project!

---

## Use this when

- ✅ Starting ANY new project
- ✅ Setting up databases
- ✅ Configuring Docker
- ✅ Creating configuration files
- ✅ Installing dependencies
- ✅ Organizing project structure
- ✅ ANY time you're unsure where something belongs

## Don't use this when

- ❌ Never! This concept ALWAYS applies!

## Purpose

**Single clear purpose:**  
Ensure complete separation between helper tools (Memory, MCP) and user's actual project to prevent confusion and maintain clean architecture.

## Decision Rule

**Always choose the best solution:**
- If it's for YOU (AI/technical lead) → `~/.global/`
- If it's for USER'S PROJECT → `~/user-project/`
- If unsure → ASK! Don't guess!

**Never choose the easy way:**
- ❌ Don't put everything in one place "for convenience"
- ✅ Maintain strict separation even if it takes more effort

## Environment Structure

### Helper Tools Environment (For YOU)
```
~/.global/                          # All helper tools here!
├── memory/                         # Memory system
│   ├── context.db                  # Your context database
│   ├── summaries/                  # Conversation summaries
│   └── decisions/                  # Decision logs
├── mcp/                            # MCP configuration
│   ├── config.json                 # MCP servers config
│   ├── servers/                    # Installed servers
│   └── logs/                       # MCP logs
├── cache/                          # Temporary cache
└── config/                         # Your configurations
```

### User's Project Environment (For THEIR APP)
```
~/user-project/                     # User's actual project
├── src/                            # Source code
│   ├── api/                        # API endpoints
│   ├── models/                     # Data models
│   └── services/                   # Business logic
├── database/                       # Project database
│   ├── app.db                      # Application data
│   ├── migrations/                 # DB migrations
│   └── seeds/                      # Seed data
├── config/                         # Project configuration
│   ├── .env                        # Environment variables
│   └── settings.py                 # App settings
├── docker/                         # Project Docker
│   ├── Dockerfile                  # App container
│   └── docker-compose.yml          # App services
├── tests/                          # Project tests
├── docs/                           # Project documentation
└── requirements.txt                # Project dependencies
```

## Critical Separations

### Database Separation
```
Helper Tools Database:
  ~/.global/memory/context.db       # YOUR context

User's Project Database:
  ~/user-project/database/app.db    # THEIR data

NEVER MIX THESE!
```

### Docker Separation
```
Helper Tools Docker:
  ~/.global/docker/                 # If you need Docker for tools
    └── docker-compose.yml          # For helper services

User's Project Docker:
  ~/user-project/docker/            # Their application containers
    └── docker-compose.yml          # For their app services

COMPLETELY SEPARATE!
```

### Configuration Separation
```
Helper Tools Config:
  ~/.global/config/                 # Your configurations
    ├── memory.conf
    └── mcp.conf

User's Project Config:
  ~/user-project/config/            # Their app config
    ├── .env
    └── settings.py

DON'T CONFUSE!
```

### Dependencies Separation
```
Helper Tools Dependencies:
  ~/.global/venv/                   # If you need Python env for tools
    └── (memory, mcp packages)

User's Project Dependencies:
  ~/user-project/venv/              # Their application dependencies
    └── (flask, django, etc.)

SEPARATE ENVIRONMENTS!
```

## Example Scenarios

### Scenario 1: Starting New Project ✅
```python
# CORRECT approach

# 1. Initialize YOUR tools
memory.init(location="~/.global/memory/")
mcp.init(location="~/.global/mcp/")

# 2. Create USER'S project
os.makedirs("~/user-project/src")
os.makedirs("~/user-project/database")
os.makedirs("~/user-project/config")

# 3. Save to memory (YOUR tool)
memory.save({
    "type": "project_start",
    "project_path": "~/user-project",  # Note: separate!
    "description": "User's new web application"
})

# 4. Create USER'S database
create_database("~/user-project/database/app.db")

# Clear separation maintained!
```

### Scenario 2: Setting Up Docker ✅
```yaml
# ~/.global/docker/docker-compose.yml
# For YOUR helper tools (if needed)
version: '3.8'
services:
  memory-cache:
    image: redis:latest
    volumes:
      - ~/.global/cache:/data

---

# ~/user-project/docker/docker-compose.yml
# For USER'S application
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:15
    volumes:
      - ~/user-project/database:/var/lib/postgresql/data
```

### Scenario 3: Configuration Files ✅
```python
# ~/.global/config/memory.conf
# YOUR memory configuration
[memory]
database = ~/.global/memory/context.db
max_size = 100MB
retention = 30days

---

# ~/user-project/config/.env
# USER'S application configuration
DATABASE_URL=postgresql://localhost/app_db
SECRET_KEY=user-secret-key
DEBUG=True
```

## Bad Examples (What NOT to Do)

### Bad Example 1: Mixing Databases ❌
```python
# WRONG!
memory.save_to_db("~/user-project/database/app.db")
# This puts YOUR context in THEIR database!

# CORRECT!
memory.save_to_db("~/.global/memory/context.db")
# YOUR context in YOUR database
```

### Bad Example 2: Mixing Docker ❌
```yaml
# WRONG! (in ~/user-project/docker-compose.yml)
services:
  user-app:
    # User's app
  memory-system:  # WRONG! This is YOUR tool!
    # Memory system
```

### Bad Example 3: Mixing Config ❌
```python
# WRONG! (in ~/user-project/config/settings.py)
MEMORY_DB = "~/.global/memory/context.db"  # WRONG!
# Don't put YOUR tool config in THEIR project!
```

## Decision Tree

```
Question: Where does this belong?

Is it for the AI/technical lead to work better?
├─ YES → ~/.global/
│   ├─ Memory? → ~/.global/memory/
│   ├─ MCP? → ~/.global/mcp/
│   └─ Cache? → ~/.global/cache/
│
└─ NO → Is it part of user's application?
    └─ YES → ~/user-project/
        ├─ Source code? → ~/user-project/src/
        ├─ Database? → ~/user-project/database/
        ├─ Config? → ~/user-project/config/
        └─ Docker? → ~/user-project/docker/
```

## Quality Gates

### Before Creating Any File
- [ ] Is this for ME (helper tool) or USER (their project)?
- [ ] Am I putting it in the correct location?
- [ ] Have I maintained separation?
- [ ] Would this confuse the two environments?

### Before Creating Any Database
- [ ] Is this MY context or USER'S data?
- [ ] Correct path: ~/.global/ or ~/user-project/?
- [ ] Separate connection strings?

### Before Creating Any Docker File
- [ ] Is this for MY tools or USER'S app?
- [ ] Separate compose files?
- [ ] No mixing of services?

## Common Mistakes & Fixes

### Mistake 1: "It's easier to put everything together"
```
❌ WRONG: One database for everything
✅ RIGHT: Separate databases, even if more work
Why: Clarity > Convenience
```

### Mistake 2: "Memory is part of the project"
```
❌ WRONG: Memory in ~/user-project/.memory/
✅ RIGHT: Memory in ~/.global/memory/
Why: Memory is YOUR tool, not their feature
```

### Mistake 3: "MCP is a project dependency"
```
❌ WRONG: MCP in ~/user-project/requirements.txt
✅ RIGHT: MCP in ~/.global/ (pre-installed)
Why: MCP is YOUR capability, not their code
```

### Mistake 4: "Shared Docker compose is simpler"
```
❌ WRONG: One docker-compose.yml for everything
✅ RIGHT: Separate compose files
Why: Clear boundaries prevent confusion
```

## Verification Checklist

### After Setup, Verify:
```bash
# Check helper tools
ls ~/.global/memory/     # Should exist
ls ~/.global/mcp/        # Should exist

# Check user's project
ls ~/user-project/src/       # Should exist
ls ~/user-project/database/  # Should exist

# Verify separation
# These should be DIFFERENT:
cat ~/.global/memory/context.db      # Your context
cat ~/user-project/database/app.db   # Their data

# No overlap!
```

## Related Knowledge Items

- **Memory System** - Lives in ~/.global/memory/ (see `knowledge/core/memory.md`)
- **MCP System** - Lives in ~/.global/mcp/ (see `knowledge/core/mcp.md`)
- **Project Structure** - User's project layout (see `knowledge/development/structure.md`)

---

## Summary

**Environment separation is NON-NEGOTIABLE!**

### The Rule:
```
Helper Tools (Memory, MCP) → ~/.global/
User's Project → ~/user-project/

NEVER MIX!
```

### Why It Matters:
- Prevents confusion
- Maintains clean architecture
- Enables proper testing
- Allows independent scaling
- Makes debugging easier

### Remember:
- YOU use helper tools
- USER builds their project
- These are SEPARATE things
- Keep them SEPARATE always!

**Always choose the best solution (separation) not the easiest (mixing)!**

