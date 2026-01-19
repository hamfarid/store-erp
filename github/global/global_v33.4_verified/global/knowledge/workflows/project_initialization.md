# Project Initialization Workflow

> **How to properly initialize a new project**

---

## Use This When

**Use this workflow when:**
- ✅ Starting a brand new project
- ✅ Need to set up project structure
- ✅ Need to initialize tracking and documentation
- ✅ First interaction on a new project

**Don't use this when:**
- ❌ Project already initialized
- ❌ Just adding a feature to existing project
- ❌ Working on a quick script or tool

---

## Purpose

Properly initialize a project with:
- Clean project structure
- Tracking files for AI
- Memory context
- MCP tools ready
- Best practices from start

---

## Decision Rule

```
If starting new project:
  → Use THIS workflow
  
If project exists:
  → Skip to relevant workflow (API, Bug Fix, etc.)
```

---

## Initialization Steps

### Step 1: Verify Environment Separation

**CRITICAL: Understand the separation!**

```
YOUR Tools (Helper):
  ~/.global/memory/    # Your context storage
  ~/.global/mcp/       # Your capabilities

USER'S Project:
  ~/user-project/      # Their code and data

NEVER MIX THESE!
```

**Verify:**
- [ ] I understand Memory/MCP are MY tools
- [ ] I understand user's project is separate
- [ ] I will NOT put Memory/MCP in user's project
- [ ] I will NOT put project code in ~/.global/

---

### Step 2: Initialize Helper Tools

**Initialize Memory:**
```python
# Initialize memory system
memory.init(location="~/.global/memory/")

# Save project initialization
memory.save({
    "type": "project_init",
    "project_name": "[project-name]",
    "project_path": "~/user-project/",
    "date": "[current-date]",
    "description": "[brief-description]"
})
```

**Initialize MCP:**
```python
# Check available MCP servers
servers = mcp.list_servers()
print(f"Available servers: {servers}")

# List all available tools
tools = mcp.list_all_tools()
print(f"Total tools available: {len(tools)}")

# Save to memory
memory.save({
    "type": "mcp_init",
    "servers": servers,
    "tools_count": len(tools)
})
```

**Location:** `~/.global/` (YOUR tools!)

---

### Step 3: Get Project Information

**Ask user:**
1. Project name?
2. Project type? (Web app, API, Full-stack, etc.)
3. Main requirements?
4. Preferred technologies? (or let me choose best)
5. Timeline/constraints?

**Save to memory:**
```python
memory.save({
    "type": "project_requirements",
    "name": "[name]",
    "type": "[type]",
    "requirements": [...],
    "technologies": [...],
    "timeline": "[timeline]"
})
```

---

### Step 4: Create Project Structure

**Navigate to project location:**
```bash
cd ~/user-project/
```

**Create .ai/ folder for tracking:**
```bash
mkdir -p .ai
```

**Copy templates:**
```bash
# From Global Guidelines templates
cp ~/.../global/knowledge/templates/PROJECT_PLAN.md .ai/
cp ~/.../global/knowledge/templates/PROGRESS_TRACKER.md .ai/
cp ~/.../global/knowledge/templates/DECISIONS_LOG.md .ai/
cp ~/.../global/knowledge/templates/ARCHITECTURE.md .ai/
```

**Create project structure based on type:**

#### Web Application
```bash
mkdir -p src tests docs config deploy
touch README.md
touch .gitignore
touch requirements.txt  # or package.json
```

#### API Service
```bash
mkdir -p api models services tests docs
touch README.md
touch .gitignore
touch requirements.txt
```

#### Full-Stack
```bash
mkdir -p backend frontend database tests docs
touch README.md
touch .gitignore
touch docker-compose.yml
```

**Location:** `~/user-project/` (USER'S project!)

---

### Step 5: Initialize Version Control

```bash
cd ~/user-project/

# Initialize git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
*.egg-info/

# Testing
.coverage
.pytest_cache/
htmlcov/

# AI tracking (optional - can commit if desired)
# .ai/
EOF

# Initial commit
git add .
git commit -m "Initial project structure"
```

---

### Step 6: Fill Project Plan

**Edit `.ai/PROJECT_PLAN.md`:**

```markdown
# Project Plan

## Project Overview
**Project Name:** [Name]
**Start Date:** [Date]
**Expected Duration:** [Duration]
**Status:** 🔄 In Progress

## Requirements
[Fill from user requirements]

## Architecture
[Design based on requirements]

## Project Phases
[Break down into phases]

## Timeline
[Create realistic timeline]
```

**Save decisions to memory:**
```python
memory.save({
    "type": "architecture_decision",
    "component": "[component]",
    "choice": "[technology]",
    "rationale": "[why-best-choice]",
    "alternatives": [...],
    "trade_offs": "[pros-cons]"
})
```

---

### Step 7: Create Initial Documentation

**README.md:**
```markdown
# [Project Name]

> [Brief description]

## Features
- [Feature 1]
- [Feature 2]

## Tech Stack
- [Technology 1]
- [Technology 2]

## Getting Started
[To be filled as project develops]

## Documentation
See `docs/` folder for detailed documentation.

## Project Tracking
See `.ai/` folder for project plan, progress, and decisions.
```

**docs/README.md:**
```markdown
# Documentation

## Available Documentation
- [INSTALL.md](INSTALL.md) - Installation guide
- [API.md](API.md) - API documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

[To be created as needed]
```

---

### Step 8: Set Up Development Environment

**Based on project type:**

#### Python Project
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Create requirements.txt
cat > requirements.txt << 'EOF'
# Core
flask==3.0.0  # or django, fastapi, etc.

# Database
sqlalchemy==2.0.0
psycopg2-binary==2.9.0

# Testing
pytest==7.4.0
pytest-cov==4.1.0

# Development
black==23.0.0
flake8==6.0.0
EOF

# Install dependencies
pip install -r requirements.txt
```

#### Node.js Project
```bash
# Initialize package.json
npm init -y

# Install dependencies
npm install express
npm install --save-dev jest eslint prettier

# Update package.json scripts
# (Add test, lint, format scripts)
```

---

### Step 9: Initialize Progress Tracker

**Edit `.ai/PROGRESS_TRACKER.md`:**

```markdown
# Progress Tracker

## Overall Progress
**Phase:** Planning
**Overall Completion:** 0%
**Status:** 🔄 Just Started

## Phase 1: Planning
**Status:** 🔄 In Progress
**Started:** [Date]

### Tasks
#### Task 1: Project Initialization
- **Status:** ✅ Complete
- **Duration:** [time]
- **Notes:** Project structure created, tracking files initialized
```

---

### Step 10: Verify Initialization

**Checklist:**
- [ ] Helper tools initialized (Memory + MCP)
- [ ] Environment separation understood
- [ ] Project structure created
- [ ] .ai/ folder with templates
- [ ] Git initialized
- [ ] .gitignore created
- [ ] README.md created
- [ ] Development environment set up
- [ ] PROJECT_PLAN.md filled
- [ ] PROGRESS_TRACKER.md started
- [ ] All saved to memory

**If all checked:**
```python
memory.save({
    "type": "project_initialized",
    "project_name": "[name]",
    "project_path": "~/user-project/",
    "date": "[date]",
    "status": "ready_to_start"
})
```

---

## What You Should Have Now

### In ~/.global/ (YOUR tools)
```
~/.global/
├── memory/
│   └── [project-name]-context.json
└── mcp/
    └── [configured servers]
```

### In ~/user-project/ (USER'S project)
```
~/user-project/
├── .ai/
│   ├── PROJECT_PLAN.md
│   ├── PROGRESS_TRACKER.md
│   ├── DECISIONS_LOG.md
│   └── ARCHITECTURE.md
├── src/ (or api/, backend/, etc.)
├── tests/
├── docs/
│   └── README.md
├── .git/
├── .gitignore
├── README.md
└── requirements.txt (or package.json)
```

---

## Next Steps

**After initialization:**
1. Review PROJECT_PLAN.md with user
2. Get approval to proceed
3. Start Phase 1 of development
4. Follow full_project.md workflow

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Mixing Environments
```
DON'T:
~/user-project/memory/  # ❌ Memory in project!
~/user-project/.global/ # ❌ Global tools in project!

DO:
~/.global/memory/       # ✅ Memory in global
~/user-project/.ai/     # ✅ Tracking in project
```

### ❌ Mistake 2: Skipping Memory Initialization
```
DON'T:
Start coding without initializing memory

DO:
1. Initialize memory FIRST
2. Save project context
3. Then start coding
```

### ❌ Mistake 3: Not Documenting Decisions
```
DON'T:
Choose technology without documenting why

DO:
1. Evaluate options
2. Choose best (not easiest!)
3. Document rationale
4. Save to memory
```

### ❌ Mistake 4: Poor Project Structure
```
DON'T:
Put everything in root folder

DO:
Create proper structure:
- src/ for code
- tests/ for tests
- docs/ for documentation
- .ai/ for tracking
```

---

## Example: Initializing a Blog Platform

```
Step 1: Verify Separation ✅
  - Understood: Memory/MCP are MY tools
  - Understood: Project is separate

Step 2: Initialize Helper Tools ✅
  - memory.init() → ~/.global/memory/
  - mcp.list_servers() → 5 servers available
  - Saved to memory

Step 3: Get Project Info ✅
  - Name: "Blog Platform"
  - Type: Full-stack web app
  - Requirements: Auth, posts, comments
  - Technologies: Flask + React + PostgreSQL
  - Timeline: 2 weeks

Step 4: Create Structure ✅
  ~/blog-platform/
  ├── .ai/
  ├── backend/
  ├── frontend/
  ├── database/
  ├── tests/
  └── docs/

Step 5: Initialize Git ✅
  - git init
  - .gitignore created
  - Initial commit

Step 6: Fill Project Plan ✅
  - Requirements documented
  - Architecture designed
  - 3 phases planned
  - All decisions saved to memory

Step 7: Create Documentation ✅
  - README.md created
  - docs/ structure ready

Step 8: Set Up Environment ✅
  - Backend: Python venv + requirements.txt
  - Frontend: npm init + dependencies
  - Database: PostgreSQL schema planned

Step 9: Initialize Tracker ✅
  - PROGRESS_TRACKER.md started
  - First task logged

Step 10: Verify ✅
  - All checklist items complete
  - Saved to memory
  - Ready to start Phase 1!

Duration: 45 minutes
Status: ✅ Ready to build!
```

---

## Related

- `knowledge/workflows/full_project.md` - Complete project workflow
- `knowledge/templates/` - All templates
- `knowledge/core/memory.md` - Memory system
- `knowledge/core/mcp.md` - MCP system
- `knowledge/core/environment.md` - Environment separation

---

**Remember: Proper initialization saves hours later. Take time to do it right!**

