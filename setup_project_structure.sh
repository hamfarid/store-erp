#!/bin/bash
# FILE: setup_project_structure.sh
# PURPOSE: إنشاء هيكل المجلدات والملفات الأساسية لأي مشروع جديد
# OWNER: Global Team
# LAST-AUDITED: 2025-10-21

set -e

PROJECT_NAME="${1:-my_project}"
PROJECT_ROOT="${2:-./$PROJECT_NAME}"

echo "=========================================="
echo "إنشاء هيكل المشروع: $PROJECT_NAME"
echo "المسار: $PROJECT_ROOT"
echo "=========================================="

# إنشاء المجلد الرئيسي
mkdir -p "$PROJECT_ROOT"
cd "$PROJECT_ROOT"

# إنشاء مجلدات docs
echo "📁 إنشاء مجلدات التوثيق..."
mkdir -p docs/{api,db,security,ui,architecture}

# إنشاء ملفات التوثيق الأساسية
echo "📝 إنشاء ملفات التوثيق الأساسية..."

# ملفات docs الرئيسية
cat > docs/Inventory.md << 'EOF'
# Inventory

## Project Overview
- **Project Name:** 
- **Version:** 
- **Last Updated:** 

## Directory Structure
```
/
├── docs/
├── src/
└── tests/
```

## Modules List
| Module | Path | Status | Owner | Dependencies |
|--------|------|--------|-------|--------------|
|        |      |        |       |              |
EOF

cat > docs/TODO.md << 'EOF'
# TODO (APPEND-ONLY)

## High Priority (P0)
- [ ] 

## Medium Priority (P1)
- [ ] 

## Low Priority (P2)
- [ ] 

## Completed Tasks
<!-- Move completed tasks here with date and commit -->
EOF

cat > docs/DONT_DO_THIS_AGAIN.md << 'EOF'
# Don't Do This Again (APPEND-ONLY)

## Template
```markdown
### [YYYY-MM-DD] Error/Mistake Title
**Context:** <What was being done>
**Error:** <What went wrong>
**Root Cause:** <Why it happened>
**Language/Framework:** <Relevant tech>
**Prevention Rule:** <How to avoid in future>
**Related Files:** <File paths>
```

---

## Log Entries
<!-- Add entries below -->
EOF

cat > docs/TechStack.md << 'EOF'
# Technology Stack

## Frontend
- Framework: 
- UI Library: 
- State Management: 

## Backend
- Language: 
- Framework: 
- Database: 

## DevOps
- CI/CD: 
- Hosting: 
- Monitoring: 

## Development Tools
- Version Control: Git
- Package Manager: 
- Testing Framework: 
EOF

cat > docs/API_Contracts.md << 'EOF'
# API Contracts

## Endpoints

### Example Endpoint
- **Method:** GET
- **Path:** `/api/example`
- **Auth Required:** Yes/No
- **Request:**
  ```json
  {}
  ```
- **Response:**
  ```json
  {
    "code": 200,
    "message": "Success",
    "data": {}
  }
  ```
EOF

cat > docs/DB_Schema.md << 'EOF'
# Database Schema

## Tables

### Example Table
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id     | INT  | PRIMARY KEY | Unique ID   |

## Relationships
```mermaid
erDiagram
    TABLE1 ||--o{ TABLE2 : has
```
EOF

cat > docs/Security.md << 'EOF'
# Security Documentation

## Authentication
- Method: 
- Token Type: 
- TTL: 

## Authorization
- Model: RBAC
- Permissions: 

## Security Measures
- [ ] HTTPS enforced
- [ ] CSRF protection
- [ ] XSS prevention
- [ ] SQL injection prevention
- [ ] Rate limiting
- [ ] Input validation
EOF

cat > docs/Permissions_Model.md << 'EOF'
# Permissions Model

## Permission Types
- **ADMIN:** Full system access
- **MODIFY:** Create, update, delete
- **READ:** Full details access
- **VIEW_LIGHT:** Limited details
- **APPROVE:** Workflow approval

## Role × Permission Matrix
| Role  | Module A | Module B | Module C |
|-------|----------|----------|----------|
| Admin | ADMIN    | ADMIN    | ADMIN    |
| User  | READ     | MODIFY   | VIEW     |
EOF

cat > docs/Routes_FE.md << 'EOF'
# Frontend Routes

| Route | Component | Auth Required | Permissions | Description |
|-------|-----------|---------------|-------------|-------------|
| /     | Home      | No            | -           | Landing page|
EOF

cat > docs/Routes_BE.md << 'EOF'
# Backend Routes

| Method | Path | Handler | Auth | Permissions | Description |
|--------|------|---------|------|-------------|-------------|
| GET    | /api/health | healthCheck | No | - | Health check |
EOF

# إنشاء ملف Solution_Tradeoff_Log
cp -n "$(dirname "$0")/Solution_Tradeoff_Log.md" docs/ 2>/dev/null || cat > docs/Solution_Tradeoff_Log.md << 'EOF'
# Solution Trade-off Log (APPEND-ONLY)

> Record alternatives, OSF_Score, and final decision per significant change.

## [YYYY-MM-DD] Feature/Module: <name> | PR: <#> | Owner: <team>
**Context:**
**Options & OSF_Score:**
| Option | Security | Correctness | Reliability | Maintainability | Perf | Speed | OSF_Score |
|-------:|---------:|------------:|------------:|----------------:|-----:|------:|----------:|
| A      | 0.9      | 0.9         | 0.8         | 0.8             | 0.7  | 0.5   | 0.84      |
**Decision:** <Option>
**Rationale:**
**Rollback:** <how/when>
**Evidence:** <links>
EOF

cat > docs/fix_this_error.md << 'EOF'
# Fix This Error (APPEND-ONLY)

## Template
```markdown
### [YYYY-MM-DD] Error Title
**Status:** OPEN | IN_PROGRESS | FIXED
**Priority:** P0 | P1 | P2 | P3
**Description:** 
**Steps to Reproduce:** 
**Expected Behavior:** 
**Actual Behavior:** 
**Files Affected:** 
**Fix Applied:** (after fixing)
**Commit:** (after fixing)
```

---

## Errors
<!-- Add entries below -->
EOF

cat > docs/To_ReActivated_again.md << 'EOF'
# To Be Re-Activated (APPEND-ONLY)

## Template
```markdown
### [YYYY-MM-DD] Feature/Code Temporarily Disabled
**What:** 
**Why Disabled:** 
**Re-enable When:** 
**Re-enable Steps:** 
**Related Files:** 
```

---

## Entries
<!-- Add entries below -->
EOF

cat > docs/Class_Registry.md << 'EOF'
# Class & Type Canonical Registry (APPEND-ONLY)

## Template
```markdown
### CanonicalName: <Name>
- **Location:** `path/to/file.ext`
- **Domain Context:** <e.g., User Management, Inventory>
- **Purpose:** 
- **Fields:** 
- **Relations:** 
- **Invariants:** 
- **Visibility:** Public | Internal | Private
- **Lifecycle:** Active | Deprecated
- **DTO/API Mapping:** 
- **FE Mapping:** 
- **DB Mapping:** 
- **Tests:** 
- **Aliases/Synonyms:** 
- **Migration Notes:** 
```

---

## Registry
<!-- Add entries below -->
EOF

# إنشاء مجلد function_reference
cat > function_reference.md << 'EOF'
# Function Reference (APPEND-ONLY)

## Shared Functions and Definitions

### Template
```markdown
#### Function: `functionName(params)`
- **Location:** `path/to/file.ext`
- **Purpose:** 
- **Parameters:** 
  - `param1` (type): description
- **Returns:** type - description
- **Example:**
  ```language
  example code
  ```
- **Related:** 
```

---

## Functions
<!-- Add entries below -->
EOF

# إنشاء مجلدات المصدر
echo "📁 إنشاء مجلدات المصدر..."
mkdir -p src/{frontend,backend,shared}
mkdir -p tests/{unit,integration,e2e}

# إنشاء مجلدات todo
echo "📁 إنشاء مجلدات المهام..."
mkdir -p todo/{errors,fixes,development,integration,inspection}

# إنشاء .gitignore
echo "📝 إنشاء .gitignore..."
cat > .gitignore << 'EOF'
# Environment
.env
.env.local
.venv/
venv/
env/

# Dependencies
node_modules/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/

# Build outputs
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp
EOF

# إنشاء README
echo "📝 إنشاء README.md..."
cat > README.md << EOF
# $PROJECT_NAME

## Description
<!-- Add project description here -->

## Setup
\`\`\`bash
# Add setup instructions
\`\`\`

## Documentation
See [docs/](./docs/) for detailed documentation.

## License
<!-- Add license information -->
EOF

echo ""
echo "✅ تم إنشاء هيكل المشروع بنجاح!"
echo ""
echo "📋 الملفات والمجلدات المُنشأة:"
echo "   - docs/ (مع جميع ملفات التوثيق)"
echo "   - src/ (frontend, backend, shared)"
echo "   - tests/ (unit, integration, e2e)"
echo "   - todo/ (errors, fixes, development, integration, inspection)"
echo "   - function_reference.md"
echo "   - README.md"
echo "   - .gitignore"
echo ""
echo "🎯 الخطوات التالية:"
echo "   1. راجع ملف docs/TODO.md وأضف المهام"
echo "   2. حدّث docs/TechStack.md بالتقنيات المستخدمة"
echo "   3. ابدأ بتطوير الوحدات الأقل اعتمادية"
echo ""

