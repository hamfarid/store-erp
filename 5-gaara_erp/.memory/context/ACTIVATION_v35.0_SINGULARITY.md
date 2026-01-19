# Global Professional Core Prompt v35.0 Singularity - ACTIVATION COMPLETE

**Activation Date:** 2026-01-17
**Project:** Gaara ERP v12
**Mode:** Adoption (Existing Project Enhancement)

---

## ✅ ACTIVATION CHECKLIST

### 1. Bootstrap Protocol
- [x] Extracted `global_v35.0_singularity.zip` to `global_v35.0_singularity/`
- [x] Verified global system structure (153 files, 133 .md, 5 .py)
- [x] Located core tools in `global_v35.0_singularity/global/tools/`

### 2. Librarian Protocol
- [x] Read `.memory/file_registry.json`
- [x] Updated registry with Global v35.0 reference
- [x] Verified file registry integrity

### 3. Context First Protocol
- [x] Read `global/rules/99_context_first.md`
- [x] Read `.memory/context/current_task.md`
- [x] Read project spec (provided by user)
- [x] Understood project state: Phase 7 - Deployment Readiness (95%)

### 4. Shadow Architect Protocol
- [x] Created critique: `.memory/decisions/SHADOW_CRITIQUE_2026-01-17.md`
- [x] Identified 6 critical risks
- [x] Documented mitigations
- [x] Pre-mortem analysis complete

### 5. Anti-Hallucination Oath
> **[Verification Oath]**
> I have read `.memory/file_registry.json` and verified the project structure.
> I have verified the existing codebase structure in `backend/` and `frontend/`.
> I will NOT hallucinate imports, functions, or file paths.
> All paths use absolute Windows paths (D:\Ai_Project\5-gaara_erp\...).

### 6. Constitution Created
- [x] Created `CONSTITUTION.md` with:
  - Vision & Mission
  - Core Principles (Security First, Zero Errors, Documentation is Code)
  - Architectural Guidelines
  - System Integration (Global v35.0 protocols)
  - Roles & Responsibilities
  - Quality Gates

---

## 📊 PROJECT STATE SUMMARY

### Current Statistics
| Metric | Value |
|--------|-------|
| Total Modules | 94 (94 defined, 123 with sub-modules) |
| Complete Modules | 49 (>80% score) |
| Partial Modules | 74 (40-79% score) |
| Average Score | 78.7% |
| Critical Errors | 154 (to fix) |
| Missing Modules | 19 (to create) |
| Modules Without Frontend | 70 (74.5%) |
| TaskMaster Tasks | 40 defined |

### Tech Stack Verified
- Backend: Django 4.x + DRF
- Frontend: React 18.x
- Database: PostgreSQL 15.x
- Cache: Redis 7.x
- Task Queue: Celery 5.x
- Container: Docker 24.x

### File Counts (Verified)
| Type | Count |
|------|-------|
| Total Files | 14,376 |
| Python Files | 1,236 |
| React Components | 963 |
| Lines of Code | ~500,000+ |

---

## 🎯 IMMEDIATE PRIORITIES (Phase 0)

Based on Shadow Architect critique and project spec:

### Week 1-2: Fix Critical Errors
1. Fix 68 F821 (undefined variables)
2. Fix 24 E9 (syntax errors)
3. Fix 62 F811 (redefinitions)
4. Add pre-commit hooks

### Week 2-3: Security Hardening
1. Implement MFA (Tasks 2, 3, 4)
2. Configure JWT (Task 1)
3. Add Rate Limiting (Task 6)
4. Strong Password Policy (Task 5)

### Week 4-12: Critical Modules
1. Multi-tenant Models (Task 7)
2. Schema Middleware (Task 8)
3. HR Module (Task 26) - 35+ files
4. Projects Module (Task 27)

---

## 🔧 AVAILABLE TOOLS

### Global v35.0 Singularity Tools
| Tool | Path | Purpose |
|------|------|---------|
| Lifecycle | `global_v35.0_singularity/global/tools/lifecycle.py` | Project lifecycle management |
| Code Indexer | `global_v35.0_singularity/global/tools/code_indexer.py` | Codebase analysis |
| Speckit Bridge | `global_v35.0_singularity/global/tools/speckit_bridge.py` | GitHub tool wrapper |
| README Generator | `global_v35.0_singularity/global/tools/readme_generator.py` | Documentation |
| System Logger | `global_v35.0_singularity/global/system_logger.py` | Event logging |

### TaskMaster MCP Tools
| Tool | Description |
|------|-------------|
| `get_tasks` | List tasks with optional filters |
| `get_task` | Get task details by ID |
| `next_task` | Get next available task |
| `set_task_status` | Update task status |
| `add_task` | Add new task with AI |
| `expand_task` | Break down task into subtasks |
| `update_subtask` | Log progress on subtask |

---

## 📋 WORKFLOWS

### Standard Development Workflow
```
1. get_tasks --status=pending     # See what needs doing
2. next_task                      # Get recommended next task
3. get_task <id>                  # Understand requirements
4. expand_task <id>               # Break down if complex
5. [Implement]                    # Write code
6. update_subtask <id> --prompt   # Log findings
7. set_task_status <id> --done    # Mark complete
8. Repeat
```

### Speckit-Driven Development (SDD)
```
1. /speckit.constitution   # Define project principles (✅ Done)
2. /speckit.specify        # Create specification
3. /speckit.clarify        # Resolve ambiguities
4. /speckit.plan           # Technical planning
5. /speckit.tasks          # Generate tasks
6. /speckit.implement      # Write code
7. /speckit.analyze        # Verify consistency
```

---

## 📁 KEY DIRECTORIES

```
D:\Ai_Project\5-gaara_erp\
├── CONSTITUTION.md                    # Project supreme law
├── .memory/                           # AI Memory System
│   ├── file_registry.json             # File tracking (ALWAYS check)
│   ├── context/                       # Current context
│   │   ├── current_task.md            # Active task
│   │   └── ACTIVATION_v35.0_SINGULARITY.md  # This file
│   └── decisions/                     # Architecture decisions
├── .taskmaster/                       # TaskMaster system
│   ├── tasks/tasks.json               # 40 defined tasks
│   └── config.json                    # AI model config
├── global_v35.0_singularity/          # Global system (extracted)
│   └── global/
│       ├── rules/                     # Core protocols
│       ├── tools/                     # Python tools
│       ├── prompts/speckit/           # SDD prompts
│       └── knowledge/                 # Best practices
├── backend/                           # Django backend
│   └── src/                           # Source modules
├── frontend/                          # React frontend
│   └── src/                           # Components (963)
├── gaara-erp-frontend/                # Unified frontend
│   └── src/
│       ├── components/                # UI components
│       └── pages/                     # Page components
└── docs/                              # Documentation (1255 files)
```

---

## 🚨 CRITICAL REMINDERS

1. **NEVER write code without reading context files first**
2. **ALWAYS check file_registry.json before creating files**
3. **ALWAYS swear the Verification Oath before imports**
4. **ALWAYS run Shadow Architect on major decisions**
5. **ALWAYS use absolute paths (D:\Ai_Project\5-gaara_erp\...)**
6. **ALWAYS update documentation with code changes**

---

## ▶️ NEXT STEPS

To continue development, use these commands:

### View Current Tasks
```
TaskMaster: get_tasks --status=pending
```

### Get Recommended Next Task
```
TaskMaster: next_task
```

### Start Implementation
```
TaskMaster: get_task 1  # JWT Configuration (recommended first)
```

### Or Focus on Critical Errors First
Run flake8 to identify and fix 154 critical errors before new features.

---

**Global Professional Core Prompt v35.0 Singularity - ACTIVATED** ✅

*"The System That Plans Before It Builds, and Adopts What Exists"*
