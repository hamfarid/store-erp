================================================================================
MODULE 16: MCP INTEGRATION LAYER
================================================================================

⚠️ NOTE: This module is part of Global Guidelines (instruction manual).
Apply this guidance to THE USER'S PROJECT, not to Global Guidelines itself.
Global Guidelines is in: ~/global/ or similar
User's project is in: A separate directory (ask user for project path)



OVERVIEW
--------
هذا المودول يوفر طبقة ذكية للتكامل مع Model Context Protocol (MCP) servers،
تمكّن الذكاء الاصطناعي من اتخاذ قرارات ذكية، تنسيق الأدوات، وأتمتة سير العمل
بناءً على السياق والأهداف.

CORE PHILOSOPHY
---------------
"من دليل سلبي إلى مساعد ذكي نشط"

بدلاً من انتظار المطور لاختيار الأدوات، البرومبت:
- يحلل السياق تلقائياً
- يختار الأدوات المناسبة
- ينسق سير العمل
- يتخذ القرارات الذكية
- يتعلم ويتحسن

================================================================================
SECTION 1: MANDATORY PROJECT MAPPING
================================================================================

OVERVIEW
--------
**إلزامي:** قبل البدء في أي مشروع، يجب على الذكاء الاصطناعي رسم خريطة شاملة
للبرنامج توثق جميع الأركان والمكونات.

REQUIRED MAPPING COMPONENTS
---------------------------

### 1. PROJECT STRUCTURE MAP

**Format:** Mermaid Diagram

```mermaid
graph TB
    Root[Project Root]
    
    Root --> Frontend[Frontend]
    Root --> Backend[Backend]
    Root --> Database[Database]
    Root --> Config[Configuration]
    Root --> Tests[Tests]
    Root --> Docs[Documentation]
    
    Frontend --> Components[Components]
    Frontend --> Pages[Pages]
    Frontend --> Hooks[Hooks]
    Frontend --> Utils[Utils]
    Frontend --> Assets[Assets]
    
    Backend --> Routes[Routes]
    Backend --> Controllers[Controllers]
    Backend --> Models[Models]
    Backend --> Services[Services]
    Backend --> Middleware[Middleware]
    
    Database --> Schemas[Schemas]
    Database --> Migrations[Migrations]
    Database --> Seeds[Seeds]
    
    Config --> Env[Environment]
    Config --> Settings[Settings]
    Config --> Secrets[Secrets]
```

**Tool:** `mermaid.generate_diagram`

```bash
# إنشاء خريطة البنية
manus-render-diagram project_structure.mmd project_structure.png
```

---

### 2. IMPORTS & EXPORTS MAP

**Purpose:** توثيق جميع الاستيرادات والتصديرات في المشروع

**Format:** JSON + Diagram

```json
{
  "project": "my-app",
  "modules": [
    {
      "file": "src/main.py",
      "imports": [
        {"module": "flask", "items": ["Flask", "request", "jsonify"]},
        {"module": "sqlalchemy", "items": ["create_engine", "Column", "Integer"]},
        {"module": "./models", "items": ["User", "Post"]},
        {"module": "./utils", "items": ["validate_email", "hash_password"]}
      ],
      "exports": [
        {"name": "app", "type": "Flask", "description": "Main Flask application"},
        {"name": "db", "type": "SQLAlchemy", "description": "Database instance"}
      ]
    },
    {
      "file": "src/models/user.py",
      "imports": [
        {"module": "sqlalchemy", "items": ["Column", "Integer", "String"]},
        {"module": "../database", "items": ["Base"]}
      ],
      "exports": [
        {"name": "User", "type": "class", "description": "User model"}
      ]
    }
  ],
  "dependency_graph": {
    "main.py": ["models/user.py", "utils/validation.py"],
    "models/user.py": ["database.py"],
    "utils/validation.py": []
  }
}
```

**Mermaid Diagram:**

```mermaid
graph LR
    main[main.py] --> models[models/user.py]
    main --> utils[utils/validation.py]
    models --> db[database.py]
    
    main -.import.-> flask[flask]
    main -.import.-> sqlalchemy[sqlalchemy]
    models -.import.-> sqlalchemy
```

**Tool:** `code-analysis.map_imports_exports`

```bash
# تحليل الاستيرادات والتصديرات
python3 << 'ANALYZE_IMPORTS'
import ast
import json
from pathlib import Path

def analyze_python_file(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
    
    imports = []
    exports = []
    
    for node in ast.walk(tree):
        # Analyze imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "module": alias.name,
                    "items": [alias.asname or alias.name]
                })
        elif isinstance(node, ast.ImportFrom):
            imports.append({
                "module": node.module,
                "items": [alias.name for alias in node.names]
            })
        
        # Analyze exports (functions, classes)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not node.name.startswith('_'):
                exports.append({
                    "name": node.name,
                    "type": "function" if isinstance(node, ast.FunctionDef) else "class"
                })
    
    return {"imports": imports, "exports": exports}

# Analyze all Python files
project_map = {}
for py_file in Path('src').rglob('*.py'):
    project_map[str(py_file)] = analyze_python_file(py_file)

print(json.dumps(project_map, indent=2))
ANALYZE_IMPORTS
```

---

### 3. CLASS DEFINITIONS MAP

**Purpose:** توثيق جميع الـ Classes في المشروع

**Format:** UML Class Diagram

```mermaid
classDiagram
    class User {
        +int id
        +string username
        +string email
        +string password_hash
        +datetime created_at
        +validate_email() bool
        +check_password(password) bool
        +to_dict() dict
    }
    
    class Post {
        +int id
        +string title
        +string content
        +int user_id
        +datetime created_at
        +User author
        +get_author() User
        +to_dict() dict
    }
    
    class Comment {
        +int id
        +string content
        +int post_id
        +int user_id
        +datetime created_at
        +Post post
        +User author
        +to_dict() dict
    }
    
    User "1" --> "*" Post : writes
    User "1" --> "*" Comment : writes
    Post "1" --> "*" Comment : has
```

**Tool:** `code-analysis.generate_class_diagram`

```python
# تحليل Classes
import ast
import inspect

def analyze_class(cls):
    return {
        "name": cls.__name__,
        "bases": [base.__name__ for base in cls.__bases__],
        "attributes": [
            {
                "name": name,
                "type": type(value).__name__
            }
            for name, value in vars(cls).items()
            if not name.startswith('_')
        ],
        "methods": [
            {
                "name": name,
                "signature": str(inspect.signature(method)),
                "docstring": method.__doc__
            }
            for name, method in inspect.getmembers(cls, predicate=inspect.isfunction)
            if not name.startswith('_')
        ]
    }

# Example usage
from models import User, Post, Comment

classes_map = {
    "User": analyze_class(User),
    "Post": analyze_class(Post),
    "Comment": analyze_class(Comment)
}
```

---

### 4. LIBRARIES & DEPENDENCIES MAP

**Purpose:** توثيق جميع المكتبات المستخدمة

**Format:** JSON + Dependency Tree

```json
{
  "project": "my-app",
  "dependencies": {
    "production": [
      {
        "name": "flask",
        "version": "3.0.0",
        "purpose": "Web framework",
        "used_in": ["main.py", "routes/*.py"],
        "critical": true
      },
      {
        "name": "sqlalchemy",
        "version": "2.0.23",
        "purpose": "ORM for database",
        "used_in": ["models/*.py", "database.py"],
        "critical": true
      },
      {
        "name": "pydantic",
        "version": "2.5.0",
        "purpose": "Data validation",
        "used_in": ["schemas/*.py"],
        "critical": false
      }
    ],
    "development": [
      {
        "name": "pytest",
        "version": "7.4.3",
        "purpose": "Testing framework",
        "used_in": ["tests/*.py"],
        "critical": false
      },
      {
        "name": "ruff",
        "version": "0.1.6",
        "purpose": "Linting and formatting",
        "used_in": ["CI/CD"],
        "critical": false
      }
    ]
  },
  "dependency_tree": {
    "flask": ["werkzeug", "jinja2", "click"],
    "sqlalchemy": ["greenlet", "typing-extensions"],
    "pydantic": ["typing-extensions", "annotated-types"]
  },
  "security_vulnerabilities": [],
  "outdated_packages": [
    {
      "name": "flask",
      "current": "3.0.0",
      "latest": "3.0.1",
      "severity": "low"
    }
  ]
}
```

**Mermaid Diagram:**

```mermaid
graph TD
    App[My App]
    
    App --> Flask[flask 3.0.0]
    App --> SQLAlchemy[sqlalchemy 2.0.23]
    App --> Pydantic[pydantic 2.5.0]
    
    Flask --> Werkzeug[werkzeug]
    Flask --> Jinja2[jinja2]
    Flask --> Click[click]
    
    SQLAlchemy --> Greenlet[greenlet]
    SQLAlchemy --> TypingExt1[typing-extensions]
    
    Pydantic --> TypingExt2[typing-extensions]
    Pydantic --> AnnotatedTypes[annotated-types]
```

**Tool:** `code-analysis.analyze_dependencies`

```bash
# Python dependencies
pip list --format=json > dependencies.json
pip-audit --format=json > security_audit.json

# JavaScript dependencies
npm list --json > dependencies.json
npm audit --json > security_audit.json

# Analyze with MCP
{
  "tool": "code-analysis.analyze_dependencies",
  "arguments": {
    "project_dir": ".",
    "include_dev": true,
    "check_security": true,
    "check_updates": true
  }
}
```

---

### 5. API ENDPOINTS MAP

**Purpose:** توثيق جميع API endpoints

**Format:** OpenAPI/Swagger + Diagram

```yaml
openapi: 3.0.0
info:
  title: My App API
  version: 1.0.0

paths:
  /api/users:
    get:
      summary: List all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    
    post:
      summary: Create new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: Created

  /api/users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Success
        '404':
          description: Not found

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        username:
          type: string
        email:
          type: string
```

**Mermaid Diagram:**

```mermaid
graph LR
    Client[Client]
    
    Client -->|GET| ListUsers[/api/users]
    Client -->|POST| CreateUser[/api/users]
    Client -->|GET| GetUser[/api/users/:id]
    Client -->|PUT| UpdateUser[/api/users/:id]
    Client -->|DELETE| DeleteUser[/api/users/:id]
    
    ListUsers --> DB[(Database)]
    CreateUser --> DB
    GetUser --> DB
    UpdateUser --> DB
    DeleteUser --> DB
```

**Tool:** `code-analysis.generate_api_docs`

```python
# تحليل API endpoints (Flask example)
from flask import Flask
import json

def analyze_flask_routes(app: Flask):
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods - {'HEAD', 'OPTIONS'}),
            "path": str(rule),
            "parameters": [
                {
                    "name": arg,
                    "type": "path",
                    "required": True
                }
                for arg in rule.arguments
            ]
        })
    return routes

# Usage
from main import app
api_map = analyze_flask_routes(app)
print(json.dumps(api_map, indent=2))
```

---

### 6. DATABASE SCHEMA MAP

**Purpose:** توثيق بنية قاعدة البيانات

**Format:** ERD (Entity Relationship Diagram)

```mermaid
erDiagram
    USER ||--o{ POST : writes
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has
    POST }o--|| CATEGORY : belongs_to
    
    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
    }
    
    POST {
        int id PK
        string title
        text content
        int user_id FK
        int category_id FK
        datetime created_at
        datetime updated_at
    }
    
    COMMENT {
        int id PK
        text content
        int post_id FK
        int user_id FK
        datetime created_at
    }
    
    CATEGORY {
        int id PK
        string name UK
        string description
    }
```

**Tool:** `code-analysis.generate_erd`

```python
# تحليل Database schema (SQLAlchemy example)
from sqlalchemy import inspect
from sqlalchemy.orm import Session

def analyze_database_schema(engine):
    inspector = inspect(engine)
    schema = {}
    
    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append({
                "name": column['name'],
                "type": str(column['type']),
                "nullable": column['nullable'],
                "primary_key": column.get('primary_key', False)
            })
        
        foreign_keys = []
        for fk in inspector.get_foreign_keys(table_name):
            foreign_keys.append({
                "column": fk['constrained_columns'][0],
                "references": f"{fk['referred_table']}.{fk['referred_columns'][0]}"
            })
        
        schema[table_name] = {
            "columns": columns,
            "foreign_keys": foreign_keys
        }
    
    return schema

# Usage
from database import engine
db_schema = analyze_database_schema(engine)
```

---

### 7. CONFIGURATION MAP

**Purpose:** توثيق جميع الإعدادات والمتغيرات

**Format:** JSON + Diagram

```json
{
  "configuration": {
    "environment_variables": [
      {
        "name": "DATABASE_URL",
        "required": true,
        "default": null,
        "description": "PostgreSQL connection string",
        "example": "postgresql://user:pass@localhost/db"
      },
      {
        "name": "SECRET_KEY",
        "required": true,
        "default": null,
        "description": "Flask secret key for sessions",
        "example": "your-secret-key-here"
      },
      {
        "name": "DEBUG",
        "required": false,
        "default": "False",
        "description": "Enable debug mode",
        "example": "True"
      }
    ],
    "config_files": [
      {
        "path": "config/settings.py",
        "format": "python",
        "variables": ["DATABASE_URL", "SECRET_KEY", "DEBUG"]
      },
      {
        "path": ".env.example",
        "format": "env",
        "variables": ["DATABASE_URL", "SECRET_KEY"]
      }
    ],
    "secrets": [
      {
        "name": "API_KEY",
        "storage": "environment",
        "required": true
      },
      {
        "name": "JWT_SECRET",
        "storage": "secrets_manager",
        "required": true
      }
    ]
  }
}
```

---

## MANDATORY DOCUMENTATION WORKFLOW

### Step 1: Initial Project Scan

```typescript
{
  "workflow": "project_mapping",
  "steps": [
    {
      "step": 1,
      "action": "Scan project structure",
      "tool": "code-analysis.scan_directory",
      "output": "project_structure.json"
    },
    {
      "step": 2,
      "action": "Analyze imports/exports",
      "tool": "code-analysis.map_imports_exports",
      "output": "imports_exports.json"
    },
    {
      "step": 3,
      "action": "Extract class definitions",
      "tool": "code-analysis.extract_classes",
      "output": "classes.json"
    },
    {
      "step": 4,
      "action": "Analyze dependencies",
      "tool": "code-analysis.analyze_dependencies",
      "output": "dependencies.json"
    },
    {
      "step": 5,
      "action": "Map API endpoints",
      "tool": "code-analysis.generate_api_docs",
      "output": "api_docs.json"
    },
    {
      "step": 6,
      "action": "Generate database ERD",
      "tool": "code-analysis.generate_erd",
      "output": "database_erd.mmd"
    },
    {
      "step": 7,
      "action": "Document configuration",
      "tool": "code-analysis.extract_config",
      "output": "configuration.json"
    }
  ]
}
```

### Step 2: Generate Visual Diagrams

```bash
# Generate all diagrams
manus-render-diagram project_structure.mmd project_structure.png
manus-render-diagram imports_exports.mmd imports_exports.png
manus-render-diagram class_diagram.mmd class_diagram.png
manus-render-diagram api_endpoints.mmd api_endpoints.png
manus-render-diagram database_erd.mmd database_erd.png
```

### Step 3: Create Documentation

```markdown
# Project Documentation

## 1. Project Structure
![Project Structure](project_structure.png)

## 2. Imports & Exports
![Imports & Exports](imports_exports.png)

## 3. Class Diagram
![Class Diagram](class_diagram.png)

## 4. API Endpoints
![API Endpoints](api_endpoints.png)

## 5. Database Schema
![Database ERD](database_erd.png)

## 6. Dependencies
[See dependencies.json]

## 7. Configuration
[See configuration.json]
```

### Step 4: Store in Project

```bash
# Create docs directory
mkdir -p docs/architecture

# Move all documentation
mv *.png docs/architecture/
mv *.json docs/architecture/
mv *.mmd docs/architecture/

# Create README
cat > docs/architecture/README.md << 'EOF'
# Architecture Documentation

This directory contains comprehensive project documentation:

- **project_structure.png** - Project directory structure
- **imports_exports.png** - Module dependencies
- **class_diagram.png** - Class relationships
- **api_endpoints.png** - API routes
- **database_erd.png** - Database schema
- **dependencies.json** - Library dependencies
- **configuration.json** - Configuration variables

Generated: $(date)
EOF
```

---

## ENFORCEMENT RULES

### Rule 1: Before Starting Any Task

```typescript
{
  "rule": "mandatory_project_mapping",
  "trigger": "new_project || first_interaction",
  "actions": [
    "scan_project_structure",
    "analyze_imports_exports",
    "extract_classes",
    "analyze_dependencies",
    "map_api_endpoints",
    "generate_database_erd",
    "document_configuration"
  ],
  "output": "docs/architecture/",
  "required": true,
  "skip_allowed": false
}
```

### Rule 2: Update Documentation on Changes

```typescript
{
  "rule": "update_documentation",
  "trigger": "code_change || new_file || dependency_change",
  "actions": [
    "update_affected_diagrams",
    "regenerate_documentation",
    "commit_to_git"
  ],
  "auto": true
}
```

### Rule 3: Validate Documentation

```typescript
{
  "rule": "validate_documentation",
  "trigger": "before_commit || before_deploy",
  "checks": [
    "all_diagrams_exist",
    "all_classes_documented",
    "all_apis_documented",
    "all_dependencies_listed",
    "no_missing_imports"
  ],
  "fail_on_error": true
}
```

================================================================================
SECTION 2: CONTEXT ANALYZER
================================================================================

OVERVIEW
--------
Context Analyzer يحلل سياق المشروع تلقائياً ويحدد الأدوات والإجراءات المناسبة.

CONTEXT LAYERS
--------------

### 1. Project Context

```typescript
{
  "project_context": {
    "type": "web_app | mobile_app | api | library | cli_tool",
    "stack": {
      "frontend": ["react", "nextjs", "tailwind"],
      "backend": ["flask", "fastapi", "express"],
      "database": ["postgresql", "mongodb", "redis"],
      "infrastructure": ["docker", "kubernetes", "cloudflare"]
    },
    "phase": "planning | development | testing | deployment | maintenance",
    "size": "small | medium | large | enterprise",
    "team_size": 5,
    "methodology": "agile | waterfall | kanban"
  }
}
```

**Tool:** `context-analyzer.analyze_project`

```python
# تحليل سياق المشروع
def analyze_project_context(project_dir):
    context = {
        "type": detect_project_type(project_dir),
        "stack": detect_tech_stack(project_dir),
        "phase": determine_current_phase(project_dir),
        "size": estimate_project_size(project_dir)
    }
    return context

def detect_project_type(project_dir):
    # Check for indicators
    if Path(project_dir / "package.json").exists():
        pkg = json.load(open(project_dir / "package.json"))
        if "react" in pkg.get("dependencies", {}):
            return "web_app"
    elif Path(project_dir / "requirements.txt").exists():
        reqs = open(project_dir / "requirements.txt").read()
        if "flask" in reqs or "fastapi" in reqs:
            return "api"
    return "unknown"
```

---

### 2. Code Context

```typescript
{
  "code_context": {
    "languages": ["python", "javascript", "typescript"],
    "frameworks": ["flask", "react", "nextjs"],
    "quality_metrics": {
      "test_coverage": 85,
      "code_complexity": "medium",
      "technical_debt": "low",
      "security_score": 92
    },
    "recent_changes": [
      {
        "file": "src/main.py",
        "type": "modification",
        "lines_changed": 45,
        "timestamp": "2025-01-03T10:30:00Z"
      }
    ],
    "issues": [
      {
        "type": "code_smell",
        "severity": "medium",
        "file": "src/legacy.py",
        "line": 123
      }
    ]
  }
}
```

**Tool:** `context-analyzer.analyze_code`

```bash
# تحليل جودة الكود
{
  "tool": "code-analysis.analyze_codebase",
  "arguments": {
    "directory": "src/",
    "metrics": ["complexity", "coverage", "debt", "security"]
  }
}
```

---

### 3. Task Context

```typescript
{
  "task_context": {
    "current_task": {
      "id": "TASK-123",
      "title": "Fix login bug",
      "type": "bug_fix",
      "priority": "high",
      "assigned_to": "developer@example.com",
      "status": "in_progress"
    },
    "related_tasks": [
      {
        "id": "TASK-120",
        "title": "Improve authentication",
        "relation": "parent"
      }
    ],
    "blockers": [],
    "dependencies": ["TASK-115"]
  }
}
```

**Tool:** `taskqueue.get_context`

---

### 4. Environment Context

```typescript
{
  "environment_context": {
    "current_env": "development | staging | production",
    "available_tools": [
      "ruff", "eslint", "playwright", "sentry", "cloudflare"
    ],
    "mcp_servers": [
      {"name": "playwright", "status": "active"},
      {"name": "github", "status": "active"},
      {"name": "sentry", "status": "active"}
    ],
    "resources": {
      "cpu": "available",
      "memory": "available",
      "disk": "available"
    }
  }
}
```

---

## CONTEXT-BASED DECISION MAKING

### Decision Rules

```typescript
{
  "decision_rules": [
    {
      "condition": {
        "phase": "development",
        "code_quality": {"$lt": 80}
      },
      "action": "run_linters_and_fix",
      "tools": ["ruff", "eslint"],
      "priority": "high",
      "auto_execute": true
    },
    {
      "condition": {
        "task_type": "bug_fix",
        "error_rate": {"$gt": 5}
      },
      "action": "investigate_errors",
      "tools": ["sentry", "code-analysis"],
      "priority": "critical",
      "auto_execute": true
    },
    {
      "condition": {
        "phase": "testing",
        "test_coverage": {"$lt": 80}
      },
      "action": "increase_test_coverage",
      "tools": ["playwright", "pytest"],
      "priority": "medium",
      "auto_execute": false
    },
    {
      "condition": {
        "phase": "deployment",
        "environment": "production"
      },
      "action": "deploy_and_monitor",
      "tools": ["cloudflare", "sentry", "github"],
      "priority": "high",
      "auto_execute": false
    }
  ]
}
```

### Implementation

```python
# Context-based decision engine
def make_decision(context):
    for rule in decision_rules:
        if evaluate_condition(rule['condition'], context):
            return {
                "action": rule['action'],
                "tools": rule['tools'],
                "priority": rule['priority'],
                "auto_execute": rule['auto_execute']
            }
    return None

def evaluate_condition(condition, context):
    for key, value in condition.items():
        if key not in context:
            return False
        
        if isinstance(value, dict):
            # Handle operators like $lt, $gt
            for op, threshold in value.items():
                if op == "$lt" and context[key] >= threshold:
                    return False
                elif op == "$gt" and context[key] <= threshold:
                    return False
        elif context[key] != value:
            return False
    
    return True
```

================================================================================
SECTION 3: TOOL ORCHESTRATOR
================================================================================

OVERVIEW
--------
Tool Orchestrator ينسق عدة MCP servers لتنفيذ مهام معقدة.

ORCHESTRATION PATTERNS
----------------------

### 1. Sequential Execution

```typescript
{
  "pattern": "sequential",
  "workflow": [
    {
      "step": 1,
      "tool": "context7.get_documentation",
      "input": {"library": "flask"},
      "output_var": "flask_docs"
    },
    {
      "step": 2,
      "tool": "code-analysis.analyze_codebase",
      "input": {"directory": "src/"},
      "output_var": "analysis_results"
    },
    {
      "step": 3,
      "tool": "ruff.lint_code",
      "input": {"file": "src/main.py", "fix": true},
      "output_var": "lint_results"
    },
    {
      "step": 4,
      "tool": "github.create_issue",
      "input": {
        "title": "Code quality improvements",
        "body": "{{analysis_results}} + {{lint_results}}"
      },
      "output_var": "issue_url"
    }
  ]
}
```

---

### 2. Parallel Execution

```typescript
{
  "pattern": "parallel",
  "workflow": [
    {
      "parallel_tasks": [
        {
          "tool": "ruff.check_project",
          "input": {"directory": "src/"},
          "output_var": "python_lint"
        },
        {
          "tool": "eslint.lint_directory",
          "input": {"directory": "frontend/"},
          "output_var": "js_lint"
        },
        {
          "tool": "code-analysis.security_scan",
          "input": {"directory": "."},
          "output_var": "security_scan"
        }
      ]
    },
    {
      "step": 2,
      "tool": "aggregate_results",
      "input": {
        "results": ["{{python_lint}}", "{{js_lint}}", "{{security_scan}}"]
      },
      "output_var": "combined_report"
    }
  ]
}
```

---

### 3. Conditional Execution

```typescript
{
  "pattern": "conditional",
  "workflow": [
    {
      "step": 1,
      "tool": "sentry.list_issues",
      "input": {"status": "unresolved"},
      "output_var": "issues"
    },
    {
      "step": 2,
      "condition": "{{issues.length}} > 0",
      "then": [
        {
          "tool": "sentry.get_issue_details",
          "input": {"issue_id": "{{issues[0].id}}"},
          "output_var": "issue_details"
        },
        {
          "tool": "taskqueue.add_task",
          "input": {
            "title": "Fix Sentry issue {{issues[0].id}}",
            "priority": "high"
          }
        }
      ],
      "else": [
        {
          "tool": "notify",
          "input": {"message": "No issues found!"}
        }
      ]
    }
  ]
}
```

---

### 4. Loop Execution

```typescript
{
  "pattern": "loop",
  "workflow": [
    {
      "step": 1,
      "tool": "github.list_pull_requests",
      "input": {"state": "open"},
      "output_var": "pull_requests"
    },
    {
      "step": 2,
      "loop": "{{pull_requests}}",
      "loop_var": "pr",
      "actions": [
        {
          "tool": "github.get_pull_request_diff",
          "input": {"pull_number": "{{pr.number}}"},
          "output_var": "diff"
        },
        {
          "tool": "ruff.lint_code",
          "input": {"content": "{{diff}}"},
          "output_var": "lint_results"
        },
        {
          "tool": "github.add_issue_comment",
          "input": {
            "issue_number": "{{pr.number}}",
            "body": "Lint results: {{lint_results}}"
          }
        }
      ]
    }
  ]
}
```

---

## ERROR HANDLING & RECOVERY

### Retry Strategy

```typescript
{
  "error_handling": {
    "retry": {
      "max_attempts": 3,
      "backoff": "exponential",
      "backoff_factor": 2,
      "retry_on": ["timeout", "rate_limit", "server_error"]
    },
    "fallback": {
      "primary_tool": "ruff",
      "fallback_tools": ["pylint", "flake8"],
      "fallback_on": ["tool_unavailable", "tool_error"]
    },
    "recovery": {
      "on_error": [
        {
          "action": "log_error",
          "tool": "sentry.capture_exception"
        },
        {
          "action": "create_task",
          "tool": "taskqueue.add_task",
          "input": {
            "title": "Tool execution failed",
            "priority": "high"
          }
        },
        {
          "action": "notify_team",
          "tool": "slack.send_message"
        }
      ]
    }
  }
}
```

### Implementation

```python
# Error handling implementation
import time
from typing import Callable, Any

def execute_with_retry(
    func: Callable,
    max_attempts: int = 3,
    backoff_factor: int = 2,
    retry_on: list = None
):
    retry_on = retry_on or ["timeout", "rate_limit"]
    
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            error_type = type(e).__name__.lower()
            
            if error_type not in retry_on:
                raise
            
            if attempt < max_attempts - 1:
                wait_time = backoff_factor ** attempt
                print(f"Retry {attempt + 1}/{max_attempts} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

def execute_with_fallback(
    primary_func: Callable,
    fallback_funcs: list[Callable]
):
    try:
        return primary_func()
    except Exception as e:
        print(f"Primary tool failed: {e}")
        
        for i, fallback_func in enumerate(fallback_funcs):
            try:
                print(f"Trying fallback {i + 1}...")
                return fallback_func()
            except Exception as fallback_error:
                print(f"Fallback {i + 1} failed: {fallback_error}")
                continue
        
        raise Exception("All tools failed")
```

================================================================================
SECTION 4: INTELLIGENT WORKFLOWS
================================================================================

OVERVIEW
--------
مجموعة من سير العمل الذكية المحددة مسبقاً للمهام الشائعة.

WORKFLOW TEMPLATES
------------------

### 1. Complete Bug Fix Workflow

```typescript
{
  "workflow": "bug_fix_complete",
  "trigger": "error_detected || issue_reported",
  "mandatory_mapping": true,
  "steps": [
    {
      "phase": "Documentation",
      "mandatory": true,
      "actions": [
        {
          "action": "Generate project map",
          "tools": ["code-analysis.scan_directory"],
          "output": "docs/architecture/"
        },
        {
          "action": "Map affected components",
          "tools": ["code-analysis.map_imports_exports"],
          "output": "affected_components.json"
        }
      ]
    },
    {
      "phase": "Detection",
      "actions": [
        {
          "tool": "sentry.get_issue_details",
          "input": {"issue_id": "{{issue_id}}"},
          "output_var": "error_details"
        },
        {
          "tool": "code-analysis.find_root_cause",
          "input": {"error": "{{error_details}}"},
          "output_var": "root_cause"
        }
      ]
    },
    {
      "phase": "Analysis",
      "actions": [
        {
          "tool": "code-analysis.analyze_codebase",
          "input": {"focus": "{{root_cause.file}}"},
          "output_var": "code_analysis"
        },
        {
          "tool": "github.search_similar_issues",
          "input": {"query": "{{error_details.message}}"},
          "output_var": "similar_issues"
        }
      ]
    },
    {
      "phase": "Planning",
      "actions": [
        {
          "tool": "sequential-thinking.decompose_problem",
          "input": {"problem": "{{root_cause}}"},
          "output_var": "solution_steps"
        },
        {
          "tool": "taskqueue.add_task",
          "input": {
            "title": "Fix: {{error_details.title}}",
            "description": "{{solution_steps}}",
            "priority": "high"
          },
          "output_var": "task_id"
        },
        {
          "tool": "github.create_issue",
          "input": {
            "title": "Bug: {{error_details.title}}",
            "body": "Root cause: {{root_cause}}\nSolution: {{solution_steps}}",
            "labels": ["bug", "high-priority"]
          },
          "output_var": "github_issue"
        }
      ]
    },
    {
      "phase": "Implementation",
      "manual": true,
      "guidance": [
        "Review solution steps",
        "Implement fix",
        "Add tests",
        "Run linters"
      ],
      "auto_actions": [
        {
          "tool": "ruff.lint_code",
          "input": {"file": "{{root_cause.file}}", "fix": true}
        },
        {
          "tool": "playwright.test",
          "input": {"test_file": "tests/test_{{root_cause.module}}.py"}
        }
      ]
    },
    {
      "phase": "Review",
      "actions": [
        {
          "tool": "code-analysis.review_changes",
          "input": {"files": "{{changed_files}}"},
          "output_var": "review_results"
        },
        {
          "tool": "github.create_pull_request",
          "input": {
            "title": "Fix: {{error_details.title}}",
            "body": "Fixes #{{github_issue.number}}",
            "labels": ["bug-fix"]
          },
          "output_var": "pull_request"
        }
      ]
    },
    {
      "phase": "Deployment",
      "manual": true,
      "actions": [
        {
          "tool": "cloudflare.deploy",
          "input": {"environment": "staging"}
        },
        {
          "tool": "playwright.test_all",
          "input": {"environment": "staging"}
        },
        {
          "condition": "{{tests_passed}}",
          "tool": "cloudflare.deploy",
          "input": {"environment": "production"}
        }
      ]
    },
    {
      "phase": "Monitoring",
      "actions": [
        {
          "tool": "sentry.monitor_issue",
          "input": {"issue_id": "{{issue_id}}"},
          "duration": "24h"
        },
        {
          "tool": "sentry.resolve_issue",
          "input": {"issue_id": "{{issue_id}}"},
          "condition": "{{no_new_errors}}"
        },
        {
          "tool": "taskqueue.complete_task",
          "input": {"task_id": "{{task_id}}"}
        },
        {
          "tool": "github.close_issue",
          "input": {"issue_number": "{{github_issue.number}}"}
        }
      ]
    },
    {
      "phase": "Documentation Update",
      "mandatory": true,
      "actions": [
        {
          "action": "Update architecture docs",
          "tools": ["code-analysis.regenerate_diagrams"],
          "output": "docs/architecture/"
        },
        {
          "action": "Document fix",
          "tools": ["notion.create_page"],
          "input": {
            "title": "Bug Fix: {{error_details.title}}",
            "content": "{{solution_steps}}"
          }
        }
      ]
    }
  ]
}
```

---

### 2. Feature Development Workflow

```typescript
{
  "workflow": "feature_development",
  "trigger": "feature_request",
  "mandatory_mapping": true,
  "steps": [
    {
      "phase": "Initial Documentation",
      "mandatory": true,
      "actions": [
        {
          "action": "Generate complete project map",
          "tools": [
            "code-analysis.scan_directory",
            "code-analysis.map_imports_exports",
            "code-analysis.extract_classes",
            "code-analysis.analyze_dependencies",
            "code-analysis.generate_api_docs",
            "code-analysis.generate_erd"
          ],
          "output": "docs/architecture/"
        }
      ]
    },
    {
      "phase": "Research",
      "actions": [
        {
          "tool": "context7.search",
          "input": {"query": "{{feature_description}}"},
          "output_var": "research_results"
        },
        {
          "tool": "github.search_code",
          "input": {"query": "{{feature_keywords}}"},
          "output_var": "similar_implementations"
        }
      ]
    },
    {
      "phase": "Design",
      "actions": [
        {
          "tool": "sequential-thinking.design_solution",
          "input": {"requirements": "{{feature_description}}"},
          "output_var": "design_doc"
        },
        {
          "tool": "notion.create_page",
          "input": {
            "title": "Feature Design: {{feature_name}}",
            "content": "{{design_doc}}"
          }
        },
        {
          "action": "Generate architecture diagrams",
          "tools": ["mermaid.generate_diagram"],
          "input": {"design": "{{design_doc}}"},
          "output": "docs/features/{{feature_name}}/"
        }
      ]
    },
    {
      "phase": "Planning",
      "actions": [
        {
          "tool": "sequential-thinking.decompose",
          "input": {"feature": "{{design_doc}}"},
          "output_var": "task_breakdown"
        },
        {
          "tool": "taskqueue.bulk_add_tasks",
          "input": {"tasks": "{{task_breakdown}}"},
          "output_var": "task_ids"
        },
        {
          "tool": "github.create_milestone",
          "input": {
            "title": "Feature: {{feature_name}}",
            "description": "{{design_doc}}"
          }
        }
      ]
    },
    {
      "phase": "Implementation",
      "manual": true,
      "guidance": [
        "Follow design document",
        "Write tests first (TDD)",
        "Implement feature",
        "Run linters continuously"
      ],
      "auto_actions": [
        {
          "trigger": "on_file_save",
          "tool": "ruff.lint_code",
          "input": {"fix": true}
        },
        {
          "trigger": "on_commit",
          "tool": "playwright.test_affected",
          "input": {"changed_files": "{{git_diff}}"}
        }
      ]
    },
    {
      "phase": "Testing",
      "actions": [
        {
          "tool": "playwright.test_all",
          "input": {"suite": "feature_{{feature_name}}"}
        },
        {
          "tool": "code-analysis.check_coverage",
          "input": {"target": 80}
        },
        {
          "tool": "sentry.check_errors",
          "input": {"environment": "staging"}
        }
      ]
    },
    {
      "phase": "Review",
      "actions": [
        {
          "tool": "code-analysis.review_changes",
          "input": {"feature": "{{feature_name}}"}
        },
        {
          "tool": "github.create_pull_request",
          "input": {
            "title": "Feature: {{feature_name}}",
            "body": "Implements {{design_doc}}",
            "labels": ["feature", "needs-review"]
          }
        }
      ]
    },
    {
      "phase": "Deployment",
      "actions": [
        {
          "tool": "cloudflare.deploy",
          "input": {"environment": "production"}
        },
        {
          "tool": "github.create_release",
          "input": {
            "tag": "v{{version}}",
            "name": "Release {{version}} - {{feature_name}}"
          }
        }
      ]
    },
    {
      "phase": "Monitoring",
      "actions": [
        {
          "tool": "sentry.monitor",
          "input": {"feature": "{{feature_name}}"},
          "duration": "7d"
        },
        {
          "tool": "cloudflare.get_metrics",
          "input": {"feature": "{{feature_name}}"}
        }
      ]
    },
    {
      "phase": "Final Documentation",
      "mandatory": true,
      "actions": [
        {
          "action": "Update all architecture docs",
          "tools": [
            "code-analysis.regenerate_all_diagrams",
            "code-analysis.update_api_docs",
            "code-analysis.update_erd"
          ],
          "output": "docs/architecture/"
        },
        {
          "action": "Create feature documentation",
          "tools": ["notion.create_page"],
          "input": {
            "title": "Feature: {{feature_name}}",
            "content": "Complete documentation with diagrams"
          }
        },
        {
          "action": "Update README",
          "tools": ["github.update_file"],
          "input": {
            "file": "README.md",
            "content": "Add {{feature_name}} to features list"
          }
        }
      ]
    }
  ]
}
```

---

### 3. Code Quality Workflow

```typescript
{
  "workflow": "code_quality_check",
  "trigger": "scheduled || on_commit || manual",
  "mandatory_mapping": true,
  "steps": [
    {
      "phase": "Documentation Check",
      "mandatory": true,
      "actions": [
        {
          "action": "Verify architecture docs exist",
          "check": [
            "docs/architecture/project_structure.png",
            "docs/architecture/imports_exports.json",
            "docs/architecture/classes.json",
            "docs/architecture/dependencies.json",
            "docs/architecture/api_docs.json",
            "docs/architecture/database_erd.mmd"
          ]
        },
        {
          "action": "Regenerate if missing",
          "condition": "{{any_missing}}",
          "tools": ["code-analysis.generate_all_docs"]
        }
      ]
    },
    {
      "phase": "Linting",
      "parallel": true,
      "actions": [
        {
          "tool": "ruff.check_project",
          "input": {"directory": "src/", "fix": true},
          "output_var": "python_lint"
        },
        {
          "tool": "eslint.lint_directory",
          "input": {"directory": "frontend/", "fix": true},
          "output_var": "js_lint"
        }
      ]
    },
    {
      "phase": "Analysis",
      "parallel": true,
      "actions": [
        {
          "tool": "code-analysis.analyze_codebase",
          "input": {"depth": "deep"},
          "output_var": "code_analysis"
        },
        {
          "tool": "code-analysis.security_scan",
          "input": {"owasp_check": true},
          "output_var": "security_scan"
        },
        {
          "tool": "code-analysis.find_dead_code",
          "input": {"min_confidence": 80},
          "output_var": "dead_code"
        }
      ]
    },
    {
      "phase": "Reporting",
      "actions": [
        {
          "tool": "aggregate_results",
          "input": {
            "results": [
              "{{python_lint}}",
              "{{js_lint}}",
              "{{code_analysis}}",
              "{{security_scan}}",
              "{{dead_code}}"
            ]
          },
          "output_var": "quality_report"
        },
        {
          "tool": "github.create_issue",
          "input": {
            "title": "Code Quality Report - {{date}}",
            "body": "{{quality_report}}",
            "labels": ["code-quality", "automated"]
          }
        },
        {
          "tool": "notion.create_page",
          "input": {
            "title": "Code Quality Report",
            "content": "{{quality_report}}"
          }
        }
      ]
    },
    {
      "phase": "Task Creation",
      "actions": [
        {
          "tool": "taskqueue.bulk_add_tasks",
          "input": {
            "tasks": "{{quality_report.issues}}",
            "auto_prioritize": true
          }
        }
      ]
    }
  ]
}
```

================================================================================
SECTION 5: BEST PRACTICES & GUIDELINES
================================================================================

## MANDATORY PRACTICES

### 1. Always Map Before Starting

```typescript
{
  "rule": "map_before_start",
  "enforcement": "strict",
  "applies_to": "all_projects",
  "actions": [
    "Generate project structure diagram",
    "Map all imports and exports",
    "Document all classes",
    "List all dependencies",
    "Map all API endpoints",
    "Generate database ERD",
    "Document configuration"
  ],
  "output_location": "docs/architecture/",
  "update_frequency": "on_change"
}
```

### 2. Keep Documentation Updated

```typescript
{
  "rule": "update_docs_on_change",
  "enforcement": "strict",
  "triggers": [
    "new_file_created",
    "class_added",
    "api_endpoint_added",
    "dependency_added",
    "database_schema_changed"
  ],
  "actions": [
    "Regenerate affected diagrams",
    "Update documentation",
    "Commit to git"
  ]
}
```

### 3. Use Context-Aware Tool Selection

```typescript
{
  "rule": "context_aware_tools",
  "guidance": [
    "Analyze context before choosing tools",
    "Consider project phase",
    "Check available resources",
    "Evaluate task requirements",
    "Select optimal tool combination"
  ]
}
```

### 4. Automate Repetitive Tasks

```typescript
{
  "rule": "automate_repetitive",
  "examples": [
    "Linting on save",
    "Testing on commit",
    "Documentation on change",
    "Deployment on merge",
    "Monitoring on deploy"
  ]
}
```

### 5. Monitor and Learn

```typescript
{
  "rule": "monitor_and_learn",
  "actions": [
    "Track tool effectiveness",
    "Measure workflow efficiency",
    "Collect feedback",
    "Adjust strategies",
    "Improve continuously"
  ]
}
```

================================================================================
RESOURCES
================================================================================

### Documentation Tools
- **Mermaid:** https://mermaid.js.org/
- **PlantUML:** https://plantuml.com/
- **Swagger/OpenAPI:** https://swagger.io/

### Code Analysis Tools
- **Ruff:** https://github.com/astral-sh/ruff
- **ESLint:** https://eslint.org/
- **SonarQube:** https://www.sonarqube.org/

### MCP Resources
- **MCP Protocol:** https://modelcontextprotocol.io/
- **MCP Servers:** https://github.com/punkpeye/awesome-mcp-servers

================================================================================
END OF MODULE 16: MCP INTEGRATION LAYER
================================================================================

