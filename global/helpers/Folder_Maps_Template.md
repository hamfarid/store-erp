# Folder Maps - Project Structure

> **Purpose:** Complete map of project structure with purpose of each folder and file.

**Last Updated:** [DATE]  
**Project:** Store Management System

---

## Project Root Structure

```
store-erp/
├── backend/                # Backend Flask application
├── frontend/               # Frontend React application
├── docs/                   # Documentation
├── global/                 # Global development framework
├── .memory/                # Memory and context storage
├── config/                 # Configuration files
├── migrations/             # Database migrations
├── scripts/                # Utility scripts
├── tests/                  # Test files
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── docker-compose.yml      # Docker configuration
├── README.md               # Project overview
└── CHANGELOG.md            # Version history
```

---

## /backend - Backend Application

**Purpose:** Flask backend API server

```
backend/
├── src/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── utils/           # Utility functions
│   └── decorators/      # Custom decorators
├── migrations/          # Alembic migrations
├── instance/            # Instance-specific files
├── tests/               # Backend tests
├── requirements.txt     # Python dependencies
└── app.py              # Application entry point
```

---

## /frontend - Frontend Application

**Purpose:** React frontend SPA

```
frontend/
├── src/
│   ├── pages/           # Page components
│   ├── components/      # Reusable components
│   ├── services/        # API services
│   ├── contexts/        # React contexts
│   ├── hooks/           # Custom hooks
│   ├── lib/             # Utilities
│   └── App.jsx          # Main app component
├── public/              # Static assets
├── package.json         # Node dependencies
└── vite.config.js       # Vite configuration
```

---

## /docs - Documentation

**Purpose:** All project documentation

```
docs/
├── TODO.md                 # Task tracking (NEVER DELETE)
├── COMPLETE_TASKS.md       # Completed tasks log
├── INCOMPLETE_TASKS.md     # Remaining tasks
├── ARCHITECTURE.md         # System architecture
├── API_DOCUMENTATION.md    # API reference
├── DATABASE_SCHEMA.md      # Data model
├── SECURITY_GUIDELINES.md  # Security practices
├── DEPLOYMENT_GUIDE.md     # Deployment steps
└── DEDUPLICATION_LOG.md    # Duplicate tracking
```

---

## /global - Development Framework

**Purpose:** Global Professional Core Prompt implementation

```
global/
├── tools/
│   ├── lifecycle.py       # Lifecycle Maestro
│   ├── librarian.py       # File Registry Manager
│   └── speckit_bridge.py  # Spec File Manager
├── rules/
│   ├── 99_context_first.md   # Context First rule
│   └── 100_evolution_engine.md  # Evolution Engine
├── helpers/
│   ├── Task_List_Template.md
│   ├── Class_Registry_Template.md
│   ├── Folder_Maps_Template.md
│   ├── Import_Export_Map_Template.md
│   └── Errors_Log_Template.md
└── README.md
```

---

## /.memory - Memory Storage

**Purpose:** Context and memory for AI development

```
.memory/
├── file_registry.json      # File tracking
├── context/
│   └── current_task.md     # Current task context
├── checkpoints/            # Phase checkpoints
├── decisions/              # Decision logs
├── knowledge/              # Learned patterns
└── conversations/          # Session history
```

---

## Folder Naming Conventions

**General Rules:**
- Use lowercase
- Use underscores for spaces
- Be descriptive but concise
- Plural for collections
- Singular for single items

**Python Packages:**
- Must have `__init__.py`
- Use relative imports within package

**Test Files:**
- Prefix with `test_`
- Mirror source structure

---

## Adding New Folders/Files

**Checklist:**
1. [ ] Choose appropriate location
2. [ ] Follow naming conventions
3. [ ] Add to this map
4. [ ] Update Import_Export_Map.md (if code file)
5. [ ] Add tests (if code file)
6. [ ] Document purpose
