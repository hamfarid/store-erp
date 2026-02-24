# Global Professional Development System

**Version:** Latest (No version numbers)  
**Status:** ✅ Production Ready  
**Last Updated:** 2025-11-15

---

## 🚀 Overview

This repository contains a **comprehensive, professional global development system** designed for AI agents to autonomously develop, improve, and maintain software projects with **zero hallucinations** and **100% completeness**.

The system provides a complete framework with:
- **Clear guidelines** for every phase
- **Zero-tolerance constraints** for quality
- **Security-first approach** (OSF Framework)
- **Mandatory verification** at every step
- **Complete task tracking** with TODO system

Built to handle both **new projects from scratch** and **improvement of existing projects**.

---

## ✨ Key Features

### 🎯 Core System
- **7 Autonomous Phases:** From initialization to handoff
- **87 Specialized Prompts:** Covering all aspects of development
- **15 Strict Rules:** Non-negotiable quality standards
- **14 AI Roles:** Specialized agent configurations
- **10 Workflows:** Predefined execution patterns

### 🆕 New Features (2025-11-15)

#### 🧪 RORLOC Testing Methodology ⭐ **LATEST**
- **6-phase comprehensive testing** (Record → Organize → Refactor → Locate → Optimize → Confirm)
- **Playwright + MCP + Chrome DevTools** integration
- **100% coverage:** UI + API + DB + Security + A11y + Performance
- **Automated test runner** with colored reports
- **Final QA Report** with GO/NO-GO recommendation
- **Mandatory in Phase 4**

#### 📋 TODO Task Management System
- **3 synchronized files** for complete task tracking
- **TODO.md** - Permanent record (NEVER delete)
- **COMPLETE_TASKS.md** - Done tasks with timestamps
- **INCOMPLETE_TASKS.md** - Pending tasks by priority
- **130+ ready-to-use tasks** in templates
- **Mandatory in Phase 1 & Phase 3**

#### 🗺️ Module Mapping System
- **Automatic project mapping** tool
- **Track all files** (Frontend, Backend, Database)
- **Document relationships** and data flow
- **Visual diagrams** generation
- **Mandatory in Phase 1**

#### 🔄 Duplicate Files Detection
- **Automatic detection** of similar files
- **Deep code analysis** with normalization
- **Safe merging** with backups
- **Progress bar** for each file
- **Mandatory in Phase 3**

#### 🔍 Complete System Verification
- **Verify all pages** (List, Create, Edit, View)
- **Verify all buttons** (Add, Edit, Delete, Save, Cancel)
- **Verify Backend** (Routes, Controllers, Services, Models)
- **Verify Database** (Tables, Migrations, Relationships)
- **100% completeness report**
- **Mandatory before Phase 7**

### 🛠️ Advanced Tools

**8 Professional Tools in `.global/tools/`:**
1. `module_mapper.py` - Generate project module map
2. `duplicate_files_detector.py` - Find similar files
3. `code_deduplicator.py` - Merge duplicate code safely
4. `complete_system_checker.py` - Verify system completeness
5. **`rorloc_test_runner.py`** ⭐ **NEW** - Run RORLOC testing phases
6. `fix_paths.py` - Fix import paths
7. `project_analyzer.py` - Analyze project structure
8. `project_cleanup.py` - Clean up project files

### 📚 Comprehensive Documentation
- **OSF Framework:** Security-first decision making
- **Memory System:** 6 types for context management
- **Error Tracking:** 4 severity levels
- **Complete directory structure:** 48 folders documented

---

## 📁 Project Structure

```
global/
├── GLOBAL_PROFESSIONAL_CORE_PROMPT.md  # Main system prompt (~1900 lines)
├── README.md                           # This file
├── system_logger.py                    # System logger
│
├── prompts/                            # 91 specialized prompts
│   ├── 00_MASTER.md                   # Master blueprint
│   ├── 00_PRIORITY_ORDER.md           # Read order (CRITICAL)
│   ├── 01-14_*.md                     # Foundation prompts
│   ├── 20-29_*.md                     # Architecture prompts
│   ├── 30-46_*.md                     # Implementation prompts
│   ├── 50-59_*.md                     # Security prompts
│   ├── 60-79_*.md                     # Quality prompts
│   ├── 75_rorloc_testing_methodology.md  # RORLOC Testing ⭐ NEW
│   ├── 80-89_*.md                     # Verification prompts
│   └── 90-99_*.md                     # Handoff prompts
│
├── rules/                              # 15 strict rules
│   ├── 00_PRIORITY_ORDER.md           # Rules priority (CRITICAL)
│   ├── memory.md                      # Memory usage (MANDATORY)
│   ├── mcp.md                         # MCP tools (MANDATORY)
│   ├── thinking.md                    # Thinking framework (MANDATORY)
│   ├── 14_no_duplicate_files.md       # Zero tolerance
│   └── *.md                           # Other rules
│
├── roles/                              # 14 AI agent roles
│   ├── lead_developer.md
│   ├── code_reviewer.md
│   ├── security_expert.md
│   └── *.md
│
├── helpers/                            # 9 reusable templates
│   ├── TODO_Template.md               # TODO template
│   ├── COMPLETE_TASKS_Template.md     # Complete tasks
│   ├── INCOMPLETE_TASKS_Template.md   # Incomplete tasks
│   ├── RORLOC_Test_Plan_Template.md   # RORLOC test plan ⭐ NEW
│   ├── Task_List_Template.md
│   ├── Project_Plan_Template.md
│   └── *.md
│
├── .global/                            # Global tools & config
│   ├── tools/                         # 8 professional tools
│   │   ├── module_mapper.py
│   │   ├── duplicate_files_detector.py
│   │   ├── code_deduplicator.py
│   │   ├── complete_system_checker.py
│   │   ├── rorloc_test_runner.py      # ⭐ NEW
│   │   └── *.py
│   ├── config/                        # Configuration files
│   └── backups/                       # Backup storage
│
├── docs/                               # Project documentation
│   ├── COMPLETE_DIRECTORY_STRUCTURE.md # ⭐ NEW
│   ├── MODULE_MAP.md                  # Auto-generated
│   ├── TODO.md                        # Master task list ⭐ NEW
│   ├── COMPLETE_TASKS.md              # Done tasks ⭐ NEW
│   ├── INCOMPLETE_TASKS.md            # Pending tasks ⭐ NEW
│   └── *.md
│
├── .memory/                            # Memory system
│   ├── context/                       # Current context
│   ├── knowledge/                     # Long-term knowledge
│   ├── decisions/                     # Decision history
│   ├── errors/                        # Error tracking
│   └── state/                         # System state
│
├── knowledge/                          # Knowledge base
│   ├── templates/                     # Code templates
│   └── *.md                           # Knowledge files
│
├── examples/                           # Example projects
│   ├── fullstack_app/
│   ├── api_backend/
│   └── *.md
│
├── workflows/                          # 10 workflow definitions
│   └── *.md
│
└── errors/                             # Error logs
    ├── critical/
    └── logs/
```

---

## 🚀 Quick Start

### For AI Agents

**Step 1: Read Core Files (MANDATORY)**
```bash
1. GLOBAL_PROFESSIONAL_CORE_PROMPT.md  # Main system (~60 min read)
2. prompts/00_PRIORITY_ORDER.md        # Read order (CRITICAL)
3. rules/00_PRIORITY_ORDER.md          # Rules priority (CRITICAL)
```

**Step 2: Create TODO Files (Phase 1 - MANDATORY)**
```bash
cp helpers/TODO_Template.md docs/TODO.md
cp helpers/INCOMPLETE_TASKS_Template.md docs/INCOMPLETE_TASKS.md
cp helpers/COMPLETE_TASKS_Template.md docs/COMPLETE_TASKS.md
```

**Step 3: Follow the 7 Phases**
1. **Phase 1:** Initialize & Understand
2. **Phase 2:** Plan & Design
3. **Phase 3:** Implementation
4. **Phase 4:** Testing
5. **Phase 5:** Security
6. **Phase 6:** Deployment
7. **Phase 7:** Documentation & Handoff

**Step 4: Use Verification Tools**
```bash
# Generate module map
python .global/tools/module_mapper.py /path/to/project

# Check for duplicates
python .global/tools/duplicate_files_detector.py /path/to/project

# Verify completeness
python .global/tools/complete_system_checker.py /path/to/project
```

### For Developers

**Clone the repository:**
```bash
git clone https://github.com/hamfarid/global.git
cd global
```

**Read the documentation:**
```bash
cat GLOBAL_PROFESSIONAL_CORE_PROMPT.md
cat prompts/00_PRIORITY_ORDER.md
cat rules/00_PRIORITY_ORDER.md
```

**Start a new project:**
```bash
# Copy TODO templates
cp helpers/TODO_Template.md docs/TODO.md
cp helpers/INCOMPLETE_TASKS_Template.md docs/INCOMPLETE_TASKS.md
cp helpers/COMPLETE_TASKS_Template.md docs/COMPLETE_TASKS.md

# Customize TODO.md for your project
# Follow the 7 phases
```

---

## 📋 TODO System Workflow

### The Three Files

**1. `docs/TODO.md` - The Master Plan**
- Permanent record of ALL tasks
- NEVER delete anything (only mark with [x])
- Single source of truth
- Updated continuously

**2. `docs/COMPLETE_TASKS.md` - Done Tasks**
- Tasks moved here when completed
- Includes timestamps
- Organized by date
- Celebration of progress

**3. `docs/INCOMPLETE_TASKS.md` - Pending Tasks**
- Only incomplete tasks
- Organized by priority (4 levels)
- Updated frequently
- Quick view of what's left

### Workflow

**When you complete a task:**
1. Mark with [x] in `TODO.md`
2. Move to `COMPLETE_TASKS.md` with timestamp
3. Remove from `INCOMPLETE_TASKS.md`

**When you discover a new task:**
1. Add to `TODO.md`
2. Add to `INCOMPLETE_TASKS.md` under appropriate priority
3. Update task counts

**At phase end:**
1. Review all three files
2. Ensure synchronization
3. Update statistics

---

## 🔍 Verification System

### Module Mapping (Phase 1 - MANDATORY)

**Create module map:**
```bash
python .global/tools/module_mapper.py /path/to/project
```

**Output:** `docs/MODULE_MAP.md` with:
- Project overview
- File structure
- Frontend components
- Backend services
- Database schema
- Data flow diagrams
- Missing files checklist

### Duplicate Detection (Phase 3 - MANDATORY)

**Find duplicates:**
```bash
python .global/tools/duplicate_files_detector.py /path/to/project
```

**Analyze and merge:**
```bash
python .global/tools/code_deduplicator.py /path/to/project --threshold 0.85
```

**Auto-merge safe duplicates:**
```bash
python .global/tools/code_deduplicator.py /path/to/project --auto-merge --threshold 0.95
```

### System Verification (Before Phase 7 - MANDATORY)

**Verify completeness:**
```bash
python .global/tools/complete_system_checker.py /path/to/project
```

**Checks:**
- ✅ All pages exist (List, Create, Edit, View)
- ✅ All buttons work (Add, Edit, Delete, Save, Cancel)
- ✅ Backend complete (Routes, Controllers, Services, Models)
- ✅ Database ready (Tables, Migrations, Relationships)

**Output:** Completion score (must be 100% to proceed)

---

## 🎯 Core Principles

### OSF Framework (Observe, Strategize, Fix)
1. **Observe:** Analyze the situation thoroughly
2. **Strategize:** Plan with security-first approach (35% weight)
3. **Fix:** Implement with verification

### Zero-Tolerance Rules (15 Rules)

**LEVEL 1: Critical (9 rules)**
1. Memory usage (MANDATORY)
2. MCP tools (MANDATORY)
3. Thinking framework (MANDATORY)
4. Context engineering (MANDATORY)
5. **TODO System (MANDATORY)** ⭐ NEW
6. No duplicate files (ZERO TOLERANCE)
7. Code style standards
8. Naming conventions
9. Error handling standards

**LEVEL 2: High Priority (4 rules)**
- Frontend development rules
- Backend development rules
- Database rules
- Git commit message format

**LEVEL 3: Best Practices (2 rules)**
- Security best practices
- Testing standards

### Mandatory Checkpoints

**Phase 1 (Initialize):**
- ✅ Read prompts 1-7 (Foundation)
- ✅ Read prompts 8-11 (Analysis)
- ✅ **Create TODO files (15-17)** ⭐ MANDATORY
- ✅ Create MODULE_MAP.md

**Phase 3 (Implementation):**
- ✅ Read prompts 23-26 (Code Quality)
- ✅ Read prompt 27 (Path Management) - CRITICAL
- ✅ Read prompts 28-29 (Verification) - MANDATORY
- ✅ **Update TODO files (30-32)** ⭐ MANDATORY
- ✅ Run duplicate detection
- ✅ Merge safe duplicates

**Phase 7 (Handoff):**
- ✅ All tasks in TODO.md marked [x]
- ✅ INCOMPLETE_TASKS.md is empty
- ✅ System verification passed (100%)
- ✅ All documentation complete

---

## 🛠️ Tools Reference

### Module Mapper
```bash
python .global/tools/module_mapper.py <project_path>
```
Generates comprehensive module map in `docs/MODULE_MAP.md`

### Duplicate Detector
```bash
python .global/tools/duplicate_files_detector.py <project_path>
```
Finds files with similar names or identical content

### Code Deduplicator
```bash
python .global/tools/code_deduplicator.py <project_path> [--auto-merge] [--threshold 0.85]
```
Analyzes and merges duplicate code safely

### System Checker
```bash
python .global/tools/complete_system_checker.py <project_path>
```
Verifies 100% system completeness

---

## 📊 Statistics

| Metric | Count |
|--------|-------|
| Total Folders | 48 |
| Total Files | 252 |
| Prompts | 87 |
| Rules | 15 |
| Roles | 14 |
| Workflows | 10 |
| Tools | 7 |
| Templates | 8 |

---

## 🆕 Recent Updates (2025-11-15)

### Added
- ✅ TODO Task Management System (3 files + templates)
- ✅ Module Mapping System (tool + prompt)
- ✅ Duplicate Files Detection (2 tools + prompt)
- ✅ Complete System Verification (tool + prompt)
- ✅ Complete Directory Structure documentation
- ✅ Updated priority orders (prompts & rules)

### Changed
- ✅ GLOBAL_PROFESSIONAL_CORE_PROMPT.md (~1800 lines now)
- ✅ prompts/00_PRIORITY_ORDER.md (includes TODO system)
- ✅ rules/00_PRIORITY_ORDER.md (15 rules now)

### Total Additions
- 4 new prompts (85, 86, TODO sections)
- 4 new tools (mapper, detector, deduplicator, checker)
- 3 new templates (TODO, COMPLETE, INCOMPLETE)
- 1 new rule (TODO System - LEVEL 1)

---

## 🤝 Contributing

This is a professional system for AI-driven development. Contributions should:
- Follow the OSF Framework
- Respect all 15 rules
- Include complete documentation
- Pass all verification checks

---

## 📄 License

MIT License - See repository for details

---

## 🔗 Links

**Repository:** https://github.com/hamfarid/global  
**Issues:** https://github.com/hamfarid/global/issues  
**Documentation:** See `docs/` folder

---

## ✅ Quick Checklist

**Before starting any project:**
- [ ] Read GLOBAL_PROFESSIONAL_CORE_PROMPT.md
- [ ] Read prompts/00_PRIORITY_ORDER.md
- [ ] Read rules/00_PRIORITY_ORDER.md
- [ ] Create TODO files from templates
- [ ] Generate MODULE_MAP.md
- [ ] Follow the 7 phases

**During development:**
- [ ] Update TODO files after each task
- [ ] Check for duplicate files regularly
- [ ] Update MODULE_MAP.md when adding files
- [ ] Follow all 15 rules strictly

**Before completion:**
- [ ] All tasks marked [x] in TODO.md
- [ ] INCOMPLETE_TASKS.md is empty
- [ ] No duplicate files
- [ ] RORLOC testing completed (Phase 4) ⭐ NEW
- [ ] System verification: 100%
- [ ] Final QA Report: GO recommendation
- [ ] All documentation complete

---

**Version:** Latest  
**Status:** ✅ Production Ready  
**Last Updated:** 2025-11-15

**Ready for immediate production use!** 🚀

