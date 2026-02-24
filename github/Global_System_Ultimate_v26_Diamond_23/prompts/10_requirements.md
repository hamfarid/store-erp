=================================================================================
REQUIREMENTS GATHERING - Interactive Project Setup
=================================================================================

Version: 5.0.0
Type: Core - Requirements

This prompt guides interactive project requirements gathering.
Based on Section 64 of the original prompt.

=================================================================================
INTERACTIVE QUESTIONS
=================================================================================

When starting a new project, ask these questions in order:

1. **Project Name**
   Q: "What is the name of your project?"
   Store as: {{PROJECT_NAME}}

2. **Project Type**
   Q: "What type of project is this?"
   Options:
   - Web Application
   - API Service
   - Desktop Application
   - Mobile App
   - Data Science/ML Project
   - Other
   Store as: {{PROJECT_TYPE}}

3. **Environment**
   Q: "Is this for development or production?"
   Options: development, production
   Store as: {{ENVIRONMENT}}
   
4. **Tech Stack - Backend**
   Q: "Which backend framework?"
   Options: Django, FastAPI, Flask, Node.js/Express, None
   Store as: {{BACKEND_FRAMEWORK}}

5. **Tech Stack - Frontend**
   Q: "Which frontend framework?"
   Options: React, Vue, Angular, Plain HTML/CSS/JS, None
   Store as: {{FRONTEND_FRAMEWORK}}

6. **Database**
   Q: "Which database?"
   Options: PostgreSQL, MySQL, MongoDB, SQLite, None
   Store as: {{DATABASE_TYPE}}
   
7. **Database Name**
   Q: "Database name? (default: {{PROJECT_SLUG}}_db)"
   Store as: {{DATABASE_NAME}}

8. **Ports**
   Q: "Frontend port? (default: 3000)"
   Store as: {{FRONTEND_PORT}}
   
   Q: "Backend port? (default: 5000)"
   Store as: {{BACKEND_PORT}}
   
   Q: "Database port? (default: 5432 for PostgreSQL)"
   Store as: {{DB_PORT}}

9. **Deployment**
   Q: "Will this be deployed? (yes/no)"
   Store as: {{DEPLOY}}
   
   If yes:
   Q: "Deployment target?"
   Options: AWS, Google Cloud, Azure, Heroku, DigitalOcean, On-premise
   Store as: {{DEPLOY_TARGET}}

10. **Sample Data**
    Q: "Add sample data for development? (yes/no)"
    Store as: {{SAMPLE_DATA}}

11. **Authentication**
    Q: "Does this need user authentication? (yes/no)"
    Store as: {{NEEDS_AUTH}}

=================================================================================
CONFIGURATION FILE
=================================================================================

After collecting answers, create `.global/project.json`:

```json
{
  "project_name": "{{PROJECT_NAME}}",
  "project_slug": "{{PROJECT_SLUG}}",
  "project_type": "{{PROJECT_TYPE}}",
  "environment": "{{ENVIRONMENT}}",
  "tech_stack": {
    "backend": "{{BACKEND_FRAMEWORK}}",
    "frontend": "{{FRONTEND_FRAMEWORK}}",
    "database": "{{DATABASE_TYPE}}"
  },
  "database": {
    "name": "{{DATABASE_NAME}}",
    "user": "{{DATABASE_USER}}",
    "port": {{DB_PORT}}
  },
  "ports": {
    "frontend": {{FRONTEND_PORT}},
    "backend": {{BACKEND_PORT}},
    "database": {{DB_PORT}}
  },
  "deployment": {
    "enabled": {{DEPLOY}},
    "target": "{{DEPLOY_TARGET}}"
  },
  "features": {
    "authentication": {{NEEDS_AUTH}},
    "sample_data": {{SAMPLE_DATA}}
  }
}
```

=================================================================================
NEXT STEPS
=================================================================================

After requirements gathering:
1. Save configuration
2. Load 03_planning.txt for project planning
3. Load relevant architecture prompts based on tech stack
4. Check 50_templates.txt for matching template

=================================================================================


================================================================================
ADDITIONAL CONTENT FROM Global System Ultimate
================================================================================

39. PORT CONFIGURATION MANAGEMENT

--------------------------------------------------------------------------------

45. IMPORT/EXPORT DOCUMENTATION

--------------------------------------------------------------------------------

## 61. Import Update Automation

--------------------------------------------------------------------------------

# Section 65: Automatic Project Analysis

## Overview

When working with **existing projects**, Augment should automatically analyze the project structure, detect technologies, and generate project-specific configuration and prompts.

This eliminates the need for manual configuration and ensures accurate, context-aware assistance.

---

## When to Trigger Auto-Analysis

### Trigger Conditions

Auto-analysis should be triggered when:

1. **User opens an existing project** in Augment
2. **No `.global/project_config.json` exists** in the project
3. **User explicitly requests** analysis: "analyze this project"
4. **User asks about project** without configuration

### Skip Conditions

Skip auto-analysis when:

1. **`.global/project_config.json` already exists**
2. **User is creating a new project** (use interactive setup instead)
3. **User explicitly skips** analysis

---

## Analysis Process

### Step 1: Detect Project Root

```python
# Find project root by looking for:
- .git/ directory
- package.json
- requirements.txt
- pyproject.toml
- Cargo.toml
- go.mod
```

### Step 2: Run Project Analyzer

```bash
python3 /path/to/global/tools/project_analyzer.py /path/to/project
```

**This will:**
- Analyze project structure
- Detect technologies (frontend, backend, database)
- Find dependencies
- Detect API endpoints
- Analyze frontend components
- Analyze backend models/views
- Generate recommendations

### Step 3: Generate Files

The analyzer creates 3 files in `.global/`:

1. **`project_analysis.json`** - Full analysis results
2. **`project_config.json`** - Project configuration
3. **`project_prompt_additions.txt`** - Project-specific prompt

### Step 4: Load Configuration

Augment loads the generated configuration and uses it for all subsequent operations.

---

## Auto-Detected Information

### Project Information

- **Name** - From package.json, setup.py, or directory name
- **Description** - From package.json or README
- **Version** - From package.json or setup.py

### Technologies

#### Frontend
- React
- Vue
- Angular
- Next.js
- Svelte

#### Backend
- Django
- Flask
- FastAPI
- Express.js
- NestJS

#### Database
- PostgreSQL
- MySQL
- MongoDB
- SQLite
- Redis

#### Tools
- Docker
- Docker Compose
- Git
- CI/CD (GitHub Actions, GitLab CI)

### Project Structure

- Frontend directory detected
- Backend directory detected
- Tests directory detected
- Documentation directory detected
- Number of components/pages
- Number of models/views

### Dependencies

- Frontend dependencies (from package.json)
- Backend dependencies (from requirements.txt, Pipfile, etc.)
- Total dependency count

### API Endpoints

- Route files detected
- API structure

### Database Configuration

- Database type
- Config files
- Connection settings

---

## Generated Configuration

### Example: `project_config.json`

```json
{
  "project": {
    "name": "E-Commerce Platform",
    "phase": "development",
    "deployed": false,
    "created_at": "2025-11-02T20:00:00Z",
    "updated_at": "2025-11-02T20:00:00Z"
  },
  "ports": {
    "frontend": 3000,
    "backend": 5000,
    "database": 5432
  },
  "database": {
    "name": "ecommerce_platform_db",
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
    "email": "",
    "password_hash": null,
    "created": false
  },
  "features": {
    "auto_backup": true,
    "logging": true,
    "monitoring": true
  },
  "detected": {
    "frontend_framework": "React",
    "backend_framework": "Django",
    "database_type": "PostgreSQL",
    "has_tests": true,
    "has_docs": false
  }
}
```

### Example: `project_prompt_additions.txt`

```
## Project-Specific Configuration

### Project: E-Commerce Platform

**Auto-detected information:**

#### Technologies
- **Frontend:** React
- **Backend:** Django
- **Database:** PostgreSQL
- **Tools:** Docker, Docker Compose, Git

#### Structure
- Frontend detected: Yes
- Backend detected: Yes
- Tests found: Yes
- Documentation found: No

#### Frontend
- Framework: React
- Components: 45 found
- Pages: 12 found

#### Backend
- Framework: Django
- Models: 15 found
- Views: 23 found

#### Database
- Type: PostgreSQL
- Config files: config/database.py, settings.py

#### Dependencies
- Total: 87
- Frontend: 42
- Backend: 45

#### Recommendations

- [HIGH] No documentation directory found. Consider adding docs/
- [MEDIUM] No Docker configuration found. Consider adding Dockerfile

**Use this information to provide context-aware assistance.**
```

---

## Augment Behavior After Analysis

### Context-Aware Assistance

Augment should use the detected information to:

1. **Understand project structure** - Know where files belong
2. **Use correct technologies** - Don't suggest Vue for a React project
3. **Respect existing patterns** - Follow project conventions
4. **Avoid conflicts** - Don't create duplicate files
5. **Provide relevant suggestions** - Based on detected stack

### Example Interactions

#### User: "Add a new user model"

**Without analysis:**
```
Augment: "Which framework are you using?"
```

**With analysis:**
```
Augment: "I'll add a new User model to your Django backend.

Based on your existing models in backend/models/, I'll create:
- backend/models/user.py
- Migration file
- Admin registration

Following your project's pattern."
```

#### User: "Create a dashboard page"

**Without analysis:**
```
Augment: "Which frontend framework?"
```

**With analysis:**
```
Augment: "I'll create a Dashboard page in React.

Based on your existing pages in src/pages/, I'll create:
- src/pages/Dashboard.jsx
- src/components/DashboardStats.jsx
- src/components/DashboardChart.jsx

Using your existing component patterns and styling."
```

---

## Recommendations System

### Priority Levels

1. **HIGH** - Critical issues that should be addressed
2. **MEDIUM** - Important improvements
3. **LOW** - Nice-to-have enhancements

### Common Recommendations

#### Documentation
- No README.md found
- No documentation directory
- No API documentation

#### Testing
- No tests directory found
- Low test coverage
- No E2E tests

#### Deployment
- No Docker configuration
- No CI/CD pipeline
- No environment variables template

#### Security
- No .gitignore found
- Secrets in code
- No security headers

#### Code Quality
- No linting configuration
- No formatting configuration
- No pre-commit hooks

---

## Usage Examples

### Example 1: Analyze Existing Project

```bash
# User opens project in Augment
# Augment detects no .global/project_config.json

Augment: "I notice this is an existing project without configuration.
Would you like me to analyze it automatically? [Y/n]"

User: "yes"

Augment: "🔍 Analyzing project...
  📋 Detecting project info...
  📁 Analyzing structure...
  🔧 Detecting technologies...
  📦 Analyzing dependencies...
  🗄️  Detecting database...
  🌐 Detecting API endpoints...
  🎨 Analyzing frontend...
  ⚙️  Analyzing backend...
  💡 Generating recommendations...

✅ Analysis complete!

Detected:
- Frontend: React
- Backend: Django
- Database: PostgreSQL
- 45 components, 12 pages
- 15 models, 23 views

Generated:
- .global/project_analysis.json
- .global/project_config.json
- .global/project_prompt_additions.txt

I'm now ready to assist with context-aware suggestions!"
```

### Example 2: Manual Analysis Request

```
User: "analyze this project"

Augment: [Runs analysis]

"✅ Analysis complete!

Your project: E-Commerce Platform
- Frontend: React (45 components)
- Backend: Django (15 models)
- Database: PostgreSQL
- Tests: Yes (87 test files)
- Docs: No

Recommendations:
- [HIGH] Add documentation directory
- [MEDIUM] Add Docker configuration

Ready to help!"
```

### Example 3: Update Existing Configuration

```
User: "re-analyze the project"

Augment: "I'll update the analysis...

Changes detected:
- New components: 5
- New models: 2
- New dependencies: 3

Configuration updated!"
```

---

## Integration with Interactive Setup

### Decision Tree

```
User starts working on project
    |
    ├─ New project?
    │   └─> Use Interactive Setup (Section 64)
    │
    └─ Existing project?
        |
        ├─ Has .global/project_config.json?
        │   └─> Load configuration
        │
        └─ No configuration?
            └─> Run Auto-Analysis (Section 65)
```

### Hybrid Approach

For existing projects, Augment can:

1. **Auto-analyze** to detect current state
2. **Ask questions** to fill in missing information
3. **Combine** detected + user-provided data

**Example:**

```
Augment: "I've analyzed your project and detected:
- Frontend: React
- Backend: Django
- Database: PostgreSQL

I have a few questions:

1. Are you in Development or Production? [D/P]: _
2. Preserve existing data? [Y/N]: _
3. Admin email: _

This will complete the configuration."
```

---

## File Structure After Analysis

```
your-project/
├── .global/
│   ├── project_analysis.json       # Full analysis
│   ├── project_config.json         # Configuration
│   ├── project_prompt_additions.txt # Prompt additions
│   ├── tools/                      # Copied from global
│   └── scripts/                    # Copied from global
├── [existing project files]
└── ...
```

---

## Best Practices

### 1. Always Analyze First

Before making changes to an existing project, **always run analysis** to understand:
- Current structure
- Existing patterns
- Technology stack
- Dependencies

### 2. Respect Existing Patterns

Use detected patterns for:
- File naming
- Directory structure
- Code style
- Import patterns

### 3. Avoid Duplication

Check analysis results before creating:
- New models (check existing models)
- New components (check existing components)
- New routes (check existing routes)

### 4. Update Configuration

When project changes significantly:
- Re-run analysis
- Update configuration
- Regenerate prompt additions

### 5. Combine with Interactive Setup

For missing information:
- Use auto-analysis for detection
- Use interactive questions for user preferences
- Combine both for complete configuration

---

## Troubleshooting

### Issue: Analysis Fails

**Cause:** Invalid project structure or permissions

**Solution:**
```bash
# Check project path
ls -la /path/to/project

# Run with verbose output
python3 tools/project_analyzer.py /path/to/project --verbose
```

### Issue: Wrong Technology Detected

**Cause:** Multiple frameworks or ambiguous files

**Solution:**
```bash
# Manually specify in config
{
  "detected": {
    "frontend_framework": "React",  # Override
    "backend_framework": "Django"   # Override
  }
}
```

### Issue: Missing Dependencies

**Cause:** Dependencies not in standard files

**Solution:**
- Add to `requirements.txt` or `package.json`
- Or manually add to configuration

---

## Commands

### Analyze Project

```bash
# From command line
python3 /path/to/global/tools/project_analyzer.py /path/to/project

# From Augment
User: "analyze this project"
User: "re-analyze"
User: "update project analysis"
```

### View Analysis

```bash
# View full analysis
cat .global/project_analysis.json | jq

# View configuration
cat .global/project_config.json | jq

# View prompt additions
cat .global/project_prompt_additions.txt
```

### Update Configuration

```bash
# Re-run analysis
python3 tools/project_analyzer.py .

# Or in Augment
User: "update configuration"
```

---

## Summary

### Key Points

1. **Auto-analysis** detects project structure and technologies
2. **Generates configuration** automatically
3. **Creates project-specific prompts** for context-aware assistance
4. **Combines with interactive setup** for complete configuration
5. **Respects existing patterns** and conventions

### Benefits

✅ **No manual configuration** - Everything detected automatically  
✅ **Context-aware assistance** - Augment knows your project  
✅ **Accurate suggestions** - Based on actual project structure  
✅ **Faster onboarding** - Start working immediately  
✅ **Consistent patterns** - Follow existing conventions

### When to Use

- **Existing projects** without configuration
- **Inherited projects** you're unfamiliar with
- **Large projects** with complex structure
- **Multi-technology projects** (full-stack)
- **Before major changes** to understand current state

---

**Auto-analysis makes Augment truly intelligent about your project!** 🎯

--------------------------------------------------------------------------------



================================================================================
RECOVERED CONTENT FROM Global System Ultimate (Phase 2)
================================================================================

GLOBAL DESIGN & EXECUTION PROMPT Global System Ultimate — COMPLETE EDITION

Guidelines: LOADED Global System Ultimate — GLOBAL policy active.
Universal, production-ready rules for designing, building, auditing, repairing, and validating any project.

⸻

VERSION HISTORY:
- Global System Ultimate: Initial release with OSF framework
- Global System Ultimate: Added KMS/Vault, OIDC, AWS Secrets
- Global System Ultimate: Added Resilience & Circuit Breakers
- Global System Ultimate: Expanded Frontend & Visual Design (13 sections)
- Global System Ultimate: Added Integration Guides (Docker, Kubernetes, Maturity Model)
- Global System Ultimate: Added CI/CD Integration Guide
- Global System Ultimate: COMPLETE EDITION - Backend, Database, Security, DevOps, Testing expanded


⸻

PLACEHOLDER VARIABLES:
This prompt uses placeholder variables that should be replaced with your actual values:

Configuration Variables:
• {YOUR_PROJECT_NAME}    - Replace with your project/application name
• {your_database_name}   - Replace with your database name
• {HOST}                 - Replace with your host (e.g., localhost, your-domain.com)
• {FRONTEND_PORT}        - Replace
 with your frontend port (e.g., 3000, 8080)
• {BACKEND_PORT}         - Replace with your backend port (e.g., 5000, 8000)
• {DB_PORT}              - Replace with your database port (e.g., 5432 for PostgreSQL, 3306 for MySQL)
• {DB_USER}              - Replace with your database username
• {DB_PASSWORD}          - Replace with your database password
• {database_name}        - Replace with your specific database name

Example Replacements:
Before: APP_NAME="{YOUR_PROJECT_NAME}"
After:  APP_NAME="MyAwesomeApp"

Before: DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:{DB_PORT}/{your_database_name}
After:  DATABASE_URL=postgresql://admin:secret123@localhost:5432/myapp_db

Note: These are placeholders for examples and should be customized for your specific project.

⸻

⸻

0) Scope • Precedence • Safety
•Scope: Applies to all projects (new/existing, small/large, startup/enterprise)
•Precedence: System Policies → Global Guidelines → Project Policies → Conversation → Turn-level
•Safety:
/NestJS), Go, Rust
- Frameworks: FastAPI (async, type-safe), Django (batteries-included), NestJS (enterprise)
- ORMs: SQLAlchemy, Prisma, TypeORM
- API Protocols: REST, GraphQL, gRPC, WebSocket

B) API Design Principles
- RESTful conventions (GET/POST/PUT/PATCH/DELETE)
- GraphQL for complex queries
- gRPC for microservices
- WebSocket for real-time
- Versioning: /api/v1/, /api/v2/
- Pagination: cursor-based preferred
- Rate limiting: per-user, per-IP
- CORS: whitelist only

C) Request/Response Standards
- Unified error envelope:
  {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {...},
    "traceId": "uuid",
    "timestamp": "ISO8601"
  }
- Success response:
  {
    "data": {...},
    "meta": {
      "page": 1,
      "total": 100,
      "traceId": "uuid"
    }
  }

D) Authentication & Authorization
- JWT with rotation (TTL: 15min access, 7d refresh)
- OAuth 2.0 / OIDC for SSO
- MFA support (TOTP, SMS, email)
- RBAC with granular permissions
- Session 
ts
- Timeout: 5 seconds
- Reset timeout: 30 seconds

C) Patterns
- Retry: exponential backoff (max 3 attempts)
- Timeout: per-request, per-operation
- Fallback: cached data, default response
- Bulkhead: isolate resources
- Idempotency: safe retries

⸻

15) CI/CD INTEGRATION (from Global System Ultimate)

[Full CI/CD guide - GitHub Actions, GitLab CI, Security Scanning, Quality Gates, Deployment Strategies]

⸻

16) INTEGRATION GUIDES (from Global System Ultimate)

A) Docker Integration
- Multi-stage builds
- Security hardening
- Performance optimization
- Production deployment

B) Kubernetes Integration
- Manifests (Deployment, Service, StatefulSet)
- ConfigMaps & Secrets
- Ingress & Load Balancing
- Auto-Scaling

C) Maturity Model
- 5 levels (0-4)
- 8 assessment criteria
- OSF Score calculator
- Roadmap for improvement

⸻

17) OUTPUT PROTOCOL

Structure:
<decision_trace>
  Concise, public decision log for Phases 0–8 (facts, findings, decisions, evidence with file paths/lines, metrics).
</decision_trace>

<result>
{
  "re
source": "Task description",
  "plan": [...],
  "task_list": [...],
  "osf_scores": {...},
  "maturity_level": "Level X",
  "docs_updated": [...]
}
</result>

<summary>
  Brief wrap-up and next steps (1–3 sentences).
</summary>

⸻

18) CLEAN CODE & BEST PRACTICES

A) Naming
- Variables: camelCase (JS), snake_case (Python)
- Functions: verb + noun (getUserById)
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case.ts, snake_case.py

B) Functions
- Single responsibility
- Max 50 lines
- Max 3 parameters (use object for more)
- Pure functions preferred
- Early returns

C) Comments
- Why, not what
- TODO with owner and date
- Complex logic explained
- No commented-out code

D) Error Handling
- Try-catch for exceptions
- Specific error types
- Logged with context
- User-friendly messages
- Never swallow errors

E) Code Organization
- Modular: feature-based folders
- DRY: no duplication
- SOLID principles
- Dependency injection
- Testable code

⸻

19) CRISIS PROTOCOL

A) In
e Identification
- Unique device ID per installation
- Hardware fingerprinting (when available)
- Persistent across app updates
- Privacy-preserving (hashed)

B) Use Cases
- Multi-device session management
- Device-specific settings
- Security: detect unauthorized devices
- Analytics: device usage patterns

C) Implementation
- Generate on first launch
- Store securely (Keychain/KeyStore)
- Include in API requests (X-Device-ID header)
- Backend: track device_id per user

D) Security
- Rotate on security events
- Revoke compromised devices
- Audit log: device access history
- MFA: trusted devices

⸻

22) SDUI (SERVER-DRIVEN UI) (NEW in Global System Ultimate)

A) Concept
- UI structure defined by server responses
- Client renders based on JSON schema
- Dynamic UI without app updates
- A/B testing, personalization

B) Schema Example
```json
{
  "screen": "dashboard",
  "version": "1.2.0",
  "layout": {
    "type": "grid",
    "columns": 2,
    "components": [
      {
        "id": "stats-card",
        "ty
pe": "card",
        "title": "إحصائيات اليوم",
        "data_source": "/api/stats/today",
        "refresh_interval": 60
      },
      {
        "id": "quick-actions",
        "type": "button-group",
        "buttons": [
          {
            "label": "إضافة منتج",
            "action": "navigate",
            "target": "/products/new",
            "permission": "products.create"
          }
        ]
      }
    ]
  }
}
```

C) Benefits
- Rapid iteration without releases
- Personalized UX per user/role
- Feature flags via UI config
- Consistent cross-platform

D) Implementation
- Component registry: map types to React components
- Schema validation: Zod/JSON Schema
- Caching: cache UI configs
- Fallback: default UI if fetch fails
- Versioning: schema version compatibility

E) Security
- Validate schema server-side
- Permission checks in UI config
- Rate limit UI config endpoints
- Audit: log UI config changes

⸻

23) FILE HEADER POLICY (Enhanced in Global System Ultimate)

A) Mandatory Header (Line
l
3. If new: add entry to registry
4. CI: block PRs without registry update

E) Benefits
- No duplicate classes
- Clear ownership
- Easy refactoring
- Documentation

⸻

25) ROUTE OBFUSCATION (Enhanced in Global System Ultimate)

A) Purpose
- Hide internal route structure
- Prevent enumeration attacks
- Anti-scraping

B) Techniques
- HMAC-signed route tokens
- Short TTL (1-5 minutes)
- Rotating secrets
- Contenthash chunk names

C) Implementation
```python
# Backend
def generate_route_token(route: str, user_id: str, ttl: int = 300) -> str:
    """Generate HMAC-signed route token"""
    expires = int(time.time()) + ttl
    payload = f"{route}:{user_id}:{expires}"
    signature = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()[:16]
    return f"{signature}.{expires}"

def verify_route_token(token: str, route: str, user_id: str) -> bool:
    """Verify route token"""
    try:
        signature, expires_str = token.split('.')
        expires = int(expi
low, Kubeflow, Prefect

⸻

28) ADDITIONAL BEST PRACTICES (Global System Ultimate)

A) Conventional Commits
- Format: `<type>(<scope>): <subject>`
- Types: feat, fix, docs, style, refactor, test, chore
- Example: `feat(auth): add MFA support`

B) Branch Naming
- Feature: `feature/user-auth`
- Bugfix: `bugfix/login-error`
- Hotfix: `hotfix/security-patch`
- Release: `release/Global System Ultimate`

C) Structured Logging
```json
{
  "timestamp": "2025-10-28T15:30:00Z",
  "level": "INFO",
  "traceId": "abc-123",
  "userId": "user-456",
  "tenantId": "tenant-789",
  "route": "/api/users",
  "action": "CREATE",
  "severity": "normal",
  "timed_ms": 45,
  "outcome": "success"
}
```

D) Accessibility
- Keyboard navigation (Tab, Enter, Esc)
- Focus-visible styles
- ARIA labels and roles
- AA contrast (4.5:1 for text)
- Screen reader testing

E) Repository Privacy
- All repositories Private by default
- Explicit approval for Public
- Secret scanning enabled
- Branch protection rules

⸻

END OF GLOBAL_GUIDELINES Global System Ultimate

New in v3.
/components/UserProfile.tsx` - User profile component
  - Exports: UserProfile (default)
  - Dependencies: api/user, hooks/useAuth
  - Last Modified: 2025-10-25
  - Owner: Frontend Team
```

C) SEMANTIC DUPLICATION DETECTION

Use AST (Abstract Syntax Tree) analysis to detect semantic duplicates:

```python
# Example: detect_duplicates.py
import ast
import difflib

def get_function_signatures(file_path):
    """Extract function signatures from Python file"""
    with open(file_path) as f:
        tree = ast.parse(f.read())
    
    signatures = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            signatures.append({
                'name': node.name,
                'args': args,
                'lineno': node.lineno
            })
    return signatures

def find_duplicate_functions(dir_path):
    """Find functions with similar signatures across files"""
    # Implementation...
    pass
```

D
find existing code  
✅ Prevents wasted effort  
✅ Maintains codebase sanity

⸻

30) ENVIRONMENT DETECTION & CONFIGURATION (CRITICAL - NEW in Global System Ultimate)

**PURPOSE:** Ensure correct behavior for Development vs Production environments

A) MANDATORY ENVIRONMENT VARIABLE

**`.env` MUST include:**
```bash
APP_ENV=development  # or 'production' or 'staging'
```

**Validation on startup:**
```python
import os
import sys

APP_ENV = os.getenv('APP_ENV')
if not APP_ENV:
    print("❌ ERROR: APP_ENV not set in .env!")
    print("Set APP_ENV=development or APP_ENV=production")
    sys.exit(1)

if APP_ENV not in ['development', 'staging', 'production']:
    print(f"❌ ERROR: Invalid APP_ENV='{APP_ENV}'")
    print("Must be: development, staging, or production")
    sys.exit(1)

print(f"✅ Running in {APP_ENV.upper()} mode")
```

B) ENVIRONMENT-SPECIFIC BEHAVIOR

### Development Mode (`APP_ENV=development`)

**Characteristics:**
- ✅ Detailed error messages with stack traces
- ✅ Hot reload enabled
- ✅ Debug 
toolbar visible
- ✅ Automatic seed data generation
- ✅ CORS允许 all origins (for local dev)
- ✅ SQL query logging
- ✅ No caching (or minimal)

**Example:**
```python
if APP_ENV == 'development':
    # Detailed errors
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['DEBUG'] = True
    
    # Seed data
    if not User.query.first():
        create_test_users()
        create_test_products()
        print("✅ Test data created")
    
    # CORS
    CORS(app, origins="*")
```

### Production Mode (`APP_ENV=production`)

**Characteristics:**
- ✅ Generic error messages only
- ✅ No stack traces to clients
- ✅ Optimized builds
- ✅ Setup Wizard on first run
- ✅ Strict CORS
- ✅ Aggressive caching
- ✅ No debug info

**Example:**
```python
if APP_ENV == 'production':
    # Generic errors only
    @app.errorhandler(Exception)
    def handle_error(e):
        # Log detailed error internally
        logger.error(f"Error: {e}", exc_info=True)
        
        # Return generic message to clie
nt
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "INTERNAL_ERROR",
            "traceId": generate_trace_id()
        }), 500
    
    # Check if first run
    if not SystemConfig.query.filter_by(key='setup_complete').first():
        # Redirect to Setup Wizard
        return redirect('/setup/wizard')
```

C) FIRST-RUN DETECTION

```python
def is_first_run():
    """Check if this is the first time running in production"""
    if APP_ENV != 'production':
        return False
    
    # Check for setup completion marker
    setup_complete = SystemConfig.query.filter_by(
        key='setup_complete'
    ).first()
    
    return setup_complete is None or not setup_complete.value

def mark_setup_complete():
    """Mark setup as complete"""
    config = SystemConfig(key='setup_complete', value=True)
    db.session.add(config)
    db.session.commit()
```

D) CONFIGURATION FILES PER ENVIRONMENT

```
config/
├── development.py    # Dev-specif
ic config
├── staging.py        # Staging config
├── production.py     # Production config
└── base.py          # Shared config
```

**Load config based on environment:**
```python
if APP_ENV == 'development':
    app.config.from_object('config.development')
elif APP_ENV == 'staging':
    app.config.from_object('config.staging')
elif APP_ENV == 'production':
    app.config.from_object('config.production')
```

E) FRONTEND ENVIRONMENT DETECTION

```typescript
// frontend/src/config/environment.ts
export const APP_ENV = import.meta.env.VITE_APP_ENV || 'development';

export const config = {
  isDevelopment: APP_ENV === 'development',
  isProduction: APP_ENV === 'production',
  apiUrl: APP_ENV === 'production' 
    ? 'https://api.example.com'
    : 'http://{HOST}:{BACKEND_PORT}',
  enableDebug: APP_ENV === 'development',
  showErrorDetails: APP_ENV === 'development',
};
```

F) BENEFITS

✅ Appropriate behavior per environment  
✅ No test data in production  
✅ Detailed errors in dev, gene
ric in prod  
✅ Setup wizard only in production  
✅ Security: no debug info leaks

⸻

31) PRODUCTION SETUP WIZARD (CRITICAL - NEW in Global System Ultimate)

**PURPOSE:** Guide production deployment with interactive setup

A) WIZARD ACTIVATION

Trigger on first production run:
```python
@app.before_first_request
def check_setup():
    if APP_ENV == 'production' and is_first_run():
        # Redirect all requests to setup wizard
        session['needs_setup'] = True

@app.before_request
def enforce_setup():
    if session.get('needs_setup') and request.endpoint != 'setup_wizard':
        return redirect(url_for('setup_wizard'))
```

B) SETUP WIZARD STEPS

### Step 1: Welcome & Requirements Check
```
┌─────────────────────────────────────────┐
│  Welcome to Production Setup            │
│                                         │
│  Checking system requirements...       │
│  ✅ Python 3.11+                        │
│  ✅ PostgreSQL 14+                      │
│  ✅ Redis 6+                            │
│  ✅ D

│  Database: [{your_database_name}___]               │
│  Username: [postgres____]               │
│  Password: [____________]               │
│                                         │
│  [Test Connection]                      │
│  Status: ✅ Connected successfully      │
│                                         │
│  [Back] [Continue]                      │
└─────────────────────────────────────────┘
```

### Step 4: Email Configuration (SMTP)
```
┌─────────────────────────────────────────┐
│  Email Configuration                    │
│                                         │
│  SMTP Host:   [smtp.gmail.com]          │
│  SMTP Port:   [587__________]           │
│  Username:    [_______________]         │
│  Password:    [_______________]         │
│  From Email:  [_______________]         │
│  From Name:   [{YOUR_PROJECT_NAME}_____]          │
│                                         │
│  [Send Test Email]                      │
│                                         │
│  [Ski
ord']
            
            if validate_admin_user(email, password):
                create_admin_user(email, password)
                return redirect('/setup/wizard?step=3')
            else:
                return render_template('setup/step2.html', error="Invalid input")
        
        elif step == '3':
            # Database config
            db_config = {
                'host': request.form['host'],
                'port': request.form['port'],
                'database': request.form['database'],
                'username': request.form['username'],
                'password': request.form['password'],
            }
            
            if validate_db_config(db_config):
                save_db_config(db_config)
                return redirect('/setup/wizard?step=4')
            else:
                return render_template('setup/step3.html', error="Connection failed")
        
        # ... more steps ...
        
        elif step == '6':
            # Complete setup

            mark_setup_complete()
            session.pop('needs_setup', None)
            return redirect('/login')
    
    return render_template(f'setup/step{step}.html')
```

D) POST-SETUP CONFIGURATION

After setup wizard, provide GUI settings screens:

**Settings Menu in Admin Panel:**
```
Settings
├── General
│   ├── Company Info
│   ├── Localization
│   └── Time Zone
├── Users & Permissions
│   ├── User Management
│   ├── Roles
│   └── Permissions
├── Email
│   ├── SMTP Settings
│   └── Email Templates
├── Security
│   ├── Password Policy
│   ├── MFA Settings
│   └── Session Management
├── Integrations
│   ├── Payment Gateways
│   ├── SMS Providers
│   └── Third-party APIs
└── Advanced
    ├── Database
    ├── Cache
    └── Backup
```

E) BENEFITS

✅ Guided production setup  
✅ No manual .env editing  
✅ Validation at each step  
✅ Test connections before saving  
✅ Secure credential handling  
✅ GUI for post-setup changes

⸻

(Continuing with remaining sections...)

32) CROS
S-BROWSER TESTING (CRITICAL - NEW in Global System Ultimate)

**PURPOSE:** Ensure application works correctly across all major browsers and devices

A) MANDATORY BROWSER SUPPORT

**Desktop:**
- Chrome 90+ (primary)
- Firefox 88+
- Safari 14+
- Edge 90+

**Mobile:**
- Chrome Mobile (Android)
- Safari Mobile (iOS)
- Samsung Internet

B) AUTOMATED TESTING WITH PLAYWRIGHT

```javascript
// tests/e2e/cross-browser.spec.ts
import { test, expect, devices } from '@playwright/test';

// Test on multiple browsers
test.describe('Cross-browser compatibility', () => {
  test.use({ ...devices['Desktop Chrome'] });
  
  test('Login page renders correctly', async ({ page }) => {
    await page.goto('/login');
    
    // Check critical elements
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
    
    // Check styling
    const loginButton = page.locator('but
ton[type="submit"]');
    const bgColor = await loginButton.evaluate(el => 
      getComputedStyle(el).backgroundColor
    );
    expect(bgColor).toBe('rgb(59, 130, 246)'); // Primary color
  });
  
  test('Dashboard loads on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.goto('/dashboard');
    
    // Mobile menu should be visible
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
    
    // Desktop sidebar should be hidden
    await expect(page.locator('[data-testid="desktop-sidebar"]')).toBeHidden();
  });
});

// Run on all browsers
const browsers = ['chromium', 'firefox', 'webkit'];
browsers.forEach(browserName => {
  test.describe(`${browserName} specific tests`, () => {
    test.use({ browserName });
    
    test('All pages load', async ({ page }) => {
      const pages = ['/login', '/dashboard', '/products', '/sales'];
      for (const url of pages) {
        await page.goto(ur
l);
        await expect(page).not.toHaveTitle(/Error/);
      }
    });
  });
});
```

C) CSS COMPATIBILITY

**Use Autoprefixer:**
```javascript
// postcss.config.js
module.exports = {
  plugins: {
    autoprefixer: {
      browsers: ['last 2 versions', '> 1%', 'not dead']
    }
  }
};
```

**CSS Feature Detection:**
```css
/* Use @supports for modern features */
@supports (display: grid) {
  .container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

/* Fallback for older browsers */
@supports not (display: grid) {
  .container {
    display: flex;
    flex-wrap: wrap;
  }
}
```

D) JAVASCRIPT POLYFILLS

```javascript
// src/polyfills.ts
// For older browsers
import 'core-js/stable';
import 'regenerator-runtime/runtime';

// Fetch API polyfill
if (!window.fetch) {
  import('whatwg-fetch');
}

// IntersectionObserver polyfill
if (!('IntersectionObserver' in window)) {
  import('intersection-observer');
}
```

E) RESPONSIVE DESIGN TESTING

``
`javascript
// Test on various screen sizes
const viewports = [
  { name: 'Mobile', width: 375, height: 667 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Desktop', width: 1920, height: 1080 },
];

viewports.forEach(({ name, width, height }) => {
  test(`Layout works on ${name}`, async ({ page }) => {
    await page.setViewportSize({ width, height });
    await page.goto('/dashboard');
    
    // Take screenshot for visual regression
    await page.screenshot({ 
      path: `screenshots/${name}-dashboard.png`,
      fullPage: true 
    });
    
    // Check no horizontal scroll
    const hasHorizontalScroll = await page.evaluate(() => 
      document.documentElement.scrollWidth > window.innerWidth
    );
    expect(hasHorizontalScroll).toBe(false);
  });
});
```

F) CI INTEGRATION

```yaml
# .github/workflows/cross-browser-tests.yml
name: Cross-Browser Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: 
[chromium, firefox, webkit]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps ${{ matrix.browser }}
      - name: Run tests
        run: npx playwright test --project=${{ matrix.browser }}
      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.browser }}
          path: test-results/
```

G) BENEFITS

✅ Works on all major browsers  
✅ Automated testing  
✅ Early detection of issues  
✅ Better user experience  
✅ Professional quality

⸻

33) UI ASSET MANAGEMENT (CRITICAL - NEW in Global System Ultimate)

**PURPOSE:** Ensure all UI assets (fonts, icons, images, CSS) load correctly

A) ASSET LOADING VERIFICATION

```typescript
// frontend/src/utils/assetChecker.ts
export async function checkAssets(): Promise<{
  fonts: boolean;
  icons: boolean;
  
images: boolean;
  css: boolean;
}> {
  const results = {
    fonts: await checkFonts(),
    icons: await checkIcons(),
    images: await checkImages(),
    css: await checkCSS(),
  };
  
  const allLoaded = Object.values(results).every(v => v);
  if (!allLoaded) {
    console.error('❌ Some assets failed to load:', results);
  }
  
  return results;
}

async function checkFonts(): Promise<boolean> {
  try {
    // Check if custom fonts are loaded
    await document.fonts.ready;
    const fonts = ['Cairo', 'Inter']; // Your custom fonts
    
    for (const font of fonts) {
      const loaded = document.fonts.check(`16px ${font}`);
      if (!loaded) {
        console.error(`❌ Font not loaded: ${font}`);
        return false;
      }
    }
    return true;
  } catch (error) {
    console.error('❌ Font check failed:', error);
    return false;
  }
}

async function checkIcons(): Promise<boolean> {
  // Check if icon font/library is loaded
  const testIcon = document.createElement('i');
  
testIcon.className = 'icon-test'; // Your icon class
  document.body.appendChild(testIcon);
  
  const computed = getComputedStyle(testIcon);
  const hasIconFont = computed.fontFamily.includes('your-icon-font');
  
  document.body.removeChild(testIcon);
  return hasIconFont;
}

async function checkImages(): Promise<boolean> {
  // Check critical images
  const criticalImages = [
    '/logo.png',
    '/favicon.ico',
  ];
  
  const promises = criticalImages.map(src => 
    new Promise((resolve) => {
      const img = new Image();
      img.onload = () => resolve(true);
      img.onerror = () => {
        console.error(`❌ Image failed to load: ${src}`);
        resolve(false);
      };
      img.src = src;
    })
  );
  
  const results = await Promise.all(promises);
  return results.every(v => v);
}

async function checkCSS(): Promise<boolean> {
  // Check if main CSS is loaded
  const stylesheets = Array.from(document.styleSheets);
  const hasMainCSS = stylesheets.some(sheet => 
    sh
eet.href && sheet.href.includes('main.css')
  );
  
  if (!hasMainCSS) {
    console.error('❌ Main CSS not loaded');
  }
  
  return hasMainCSS;
}
```

B) FALLBACK ASSETS

```typescript
// frontend/src/config/assets.ts
export const ASSET_FALLBACKS = {
  logo: '/assets/fallback-logo.png',
  avatar: '/assets/default-avatar.png',
  icon: '/assets/default-icon.svg',
};

export function getImageWithFallback(src: string, fallback: string) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve(src);
    img.onerror = () => {
      console.warn(`Image failed, using fallback: ${src} -> ${fallback}`);
      resolve(fallback);
    };
    img.src = src;
  });
}

// Usage in React
function UserAvatar({ src }: { src: string }) {
  const [imgSrc, setImgSrc] = useState(src);
  
  useEffect(() => {
    getImageWithFallback(src, ASSET_FALLBACKS.avatar)
      .then(setImgSrc);
  }, [src]);
  
  return <img src={imgSrc} alt="Avatar" />;
}
```

C) ASSET PRELOADING


```html
<!-- index.html -->
<head>
  <!-- Preload critical assets -->
  <link rel="preload" href="/fonts/Cairo-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/Inter-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/logo.png" as="image">
  <link rel="preload" href="/main.css" as="style">
  
  <!-- DNS prefetch for external resources -->
  <link rel="dns-prefetch" href="https://fonts.googleapis.com">
  <link rel="dns-prefetch" href="https://cdn.example.com">
</head>
```

D) CDN CONFIGURATION

```typescript
// frontend/src/config/cdn.ts
const CDN_URL = import.meta.env.VITE_CDN_URL || '';

export function getCDNUrl(path: string): string {
  if (!CDN_URL) return path;
  return `${CDN_URL}${path}`;
}

// Usage
<img src={getCDNUrl('/images/product.jpg')} />
```

E) ASSET LOADING MONITORING

```typescript
// Monitor asset loading performance
window.addEventListener('load', () => {
  const resources = performance.ge
tEntriesByType('resource');
  
  const slowAssets = resources.filter(resource => 
    resource.duration > 1000 // > 1 second
  );
  
  if (slowAssets.length > 0) {
    console.warn('⚠️ Slow assets detected:', slowAssets.map(r => ({
      name: r.name,
      duration: r.duration,
      size: r.transferSize,
    })));
  }
  
  // Report to monitoring service
  if (window.analytics) {
    window.analytics.track('Asset Loading', {
      totalAssets: resources.length,
      slowAssets: slowAssets.length,
      totalDuration: resources.reduce((sum, r) => sum + r.duration, 0),
    });
  }
});
```

F) BENEFITS

✅ All assets load correctly  
✅ Fallbacks for failures  
✅ Performance monitoring  
✅ Better user experience  
✅ Professional appearance

⸻

34) PRODUCTION ERROR HANDLING (CRITICAL - NEW in Global System Ultimate)

**PURPOSE:** Prevent error/stack trace leaks in production

A) GENERIC ERROR RESPONSES

**Backend (Python/Flask):**
```python
# backend/src/error_handlers.py
from flask import jsonify
import l
ogging
import traceback
import uuid

logger = logging.getLogger(__name__)

def generate_trace_id():
    """Generate unique trace ID for error tracking"""
    return str(uuid.uuid4())

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions"""
    trace_id = generate_trace_id()
    
    # Log detailed error internally
    logger.error(
        f"Unhandled exception [TraceID: {trace_id}]",
        exc_info=True,
        extra={
            'trace_id': trace_id,
            'error_type': type(e).__name__,
            'error_message': str(e),
            'stack_trace': traceback.format_exc(),
        }
    )
    
    # Return generic error to client
    if app.config['ENV'] == 'production':
        return jsonify({
            'error': 'An unexpected error occurred',
            'code': 'INTERNAL_ERROR',
            'traceId': trace_id,
            'message': 'Please contact support if the problem persists'
        }), 500
    else:
        # In develop
ment, return detailed error
        return jsonify({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc().split('\n'),
            'traceId': trace_id
        }), 500

@app.errorhandler(404)
def handle_not_found(e):
    """Handle 404 errors"""
    # Don't reveal route structure
    return jsonify({
        'error': 'Resource not found',
        'code': 'NOT_FOUND'
    }), 404

@app.errorhandler(403)
def handle_forbidden(e):
    """Handle 403 errors"""
    # Don't reveal permission structure
    return jsonify({
        'error': 'Access denied',
        'code': 'FORBIDDEN'
    }), 403
```

B) FRONTEND ERROR BOUNDARY

```typescript
// frontend/src/components/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
  traceId?: string;
}

class ErrorBoundary extends Component<Prop
s, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    const traceId = this.generateTraceId();
    
    // Log to monitoring service
    console.error('React Error Boundary caught:', {
      error: error.message,
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
  return (
    <ErrorBoundary>
      <Router>
        <Routes>
          {/* Your routes */}
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}
```

C) API ERROR STANDARDIZATION

```typescript
// frontend/src/api/client.ts
export interface APIError {
  error: string;
  code: string;
  traceId?: string;
  message?: string;
  details?: any;
}

export async function apiCall<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await fetch(url
, options);
    
    if (!response.ok) {
      const error: APIError = await response.json();
      
      // Log error (but don't expose to user in production)
      console.error('API Error:', {
        url,
        status: response.status,
        error,
      });
      
      // Throw user-friendly error
      throw new Error(error.message || error.error || 'حدث خطأ');
    }
    
    return await response.json();
  } catch (error) {
    // Network error or JSON parse error
    console.error('Request failed:', error);
    throw new Error('فشل الاتصال بالخادم');
  }
}
```

D) ERROR LOGGING SERVICE

```python
# backend/src/services/error_logger.py
import logging
from datetime import datetime
from models import ErrorLog

class ErrorLogger:
    @staticmethod
    def log_error(
        trace_id: str,
        error_type: str,
        error_message: str,
        stack_trace: str,
        user_id: int = None,
        request_data: dict = None
    ):
        """Log error to database for anal
ysis"""
        error_log = ErrorLog(
            trace_id=trace_id,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            user_id=user_id,
            request_data=request_data,
            timestamp=datetime.utcnow()
        )
        db.session.add(error_log)
        db.session.commit()
        
        # Also log to file
        logging.error(
            f"[{trace_id}] {error_type}: {error_message}",
            extra={'stack_trace': stack_trace}
        )
        
        # Send alert if critical
        if error_type in ['DatabaseError', 'SecurityError']:
            send_alert_to_admin(trace_id, error_type, error_message)
```

E) BENEFITS

✅ No stack traces leaked to clients  
✅ Detailed logging internally  
✅ Trace IDs for debugging  
✅ User-friendly error messages  
✅ Security: no information disclosure

⸻

(Continuing with sections 35-38...)

35) .ENV VALIDATION & MANAGEMENT (CRITICAL - NEW in Global System Ultimate)

**PU
RPOSE:** Ensure .env is correctly configured with all required variables

A) COMPREHENSIVE .env.example

```bash
# .env.example - Complete template with documentation

# ============================================
# ENVIRONMENT
# ============================================
APP_ENV=development  # development, staging, or production (REQUIRED)
DEBUG=True           # Enable debug mode (development only)

# ============================================
# APPLICATION
# ============================================
APP_NAME="{YOUR_PROJECT_NAME}"
APP_URL=http://{HOST}:{BACKEND_PORT}
FRONTEND_URL=http://{HOST}:{FRONTEND_PORT}

# ============================================
# DATABASE
# ============================================
DB_HOST=localhost
DB_PORT=5432
DB_NAME={your_database_name}
DB_USER=postgres
DB_PASSWORD=your_secure_password_here  # CHANGE THIS!

# Full connection string (alternative to above)
# DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:{DB_PORT}/{your_database_name
}

# ============================================
# SECURITY
# ============================================
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
ENABLE_MFA=True
ENABLE_API_DOCS=True  # Swagger/OpenAPI docs
ENABLE_REGISTRATION=False  # Allow user self-registration

# ============================================
# PERFORMANCE
# ============================================
WORKERS=4  # Gunicorn workers
THREADS=2  # Threads per worker
CACHE_TTL=3600  # Cache time-to-live in seconds
```

B) VALIDATION SCRIPT

```python
# scripts/validate_env.py
import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Define required variables
REQUIRED_VARS = {
    'APP_ENV': {
        'required': True,
        'allowed_values': ['development', 'staging', 'production'],
        'description': 'Application environment'
    },
    'SECRET_KEY': {
        'required': True,
        'min_length': 32,
  
      'description': 'Application secret key'
    },
    'JWT_SECRET_KEY': {
        'required': True,
        'min_length': 32,
        'description': 'JWT secret key'
    },
    'DB_HOST': {
        'required': True,
        'description': 'Database host'
    },
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
        return 0
    else:
        print(f"❌ Validation failed with {len(result['errors'])} error(s)")
        print()
        print("Please fix the errors above and run validation again.")
        print("See .env.example for reference.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

C) AUTO-GENERATION OF .env

```python
# scripts/generate_env.py
import secrets

def generate_secret_key(length=32):
    """Generate secure random key"""
    return secrets.token_hex(length)

def generate_env_file():
    """Generate .env file with secure defaults"""
    template = f"""# Generated .env file - {datetime.now().isoformat()
}

# IMPORTANT: Review and update all values before use!

APP_ENV=development
SECRET_KEY={generate_secret_key()}
JWT_SECRET_KEY={generate_secret_key()}

DB_HOST=localhost
DB_PORT=5432
DB_NAME={your_database_name}
DB_USER=postgres
DB_PASSWORD={generate_secret_key(16)}

# Add other variables from .env.example
"""
    
    with open('.env', 'w') as f:
        f.write(template)
    
    print("✅ .env file generated!")
    print("⚠️ Please review and update the values before running the application.")

if __name__ == '__main__':
    generate_env_file()
```

D) RUNTIME VALIDATION

```python
# backend/src/app.py
from scripts.validate_env import validate_env

# Validate on startup
result = validate_env()
if not result['valid']:
    print("❌ Environment validation failed!")
    for error in result['errors']:
        print(f"  {error}")
    sys.exit(1)

if result['warnings']:
    for warning in result['warnings']:
        print(f"  {warning}")
```

E) DOCUMENTATION

Create `/docs/Env.md`:
```mar
kdown
# Environment Variables Documentation

## Required Variables

### APP_ENV
- **Description**: Application environment
- **Required**: Yes
- **Allowed Values**: `development`, `staging`, `production`
- **Example**: `APP_ENV=production`

### SECRET_KEY
- **Description**: Secret key for session encryption
- **Required**: Yes
- **Min Length**: 32 characters
- **Generation**: `python -c "import secrets; print(secrets.token_hex(32))"`
- **Example**: `SECRET_KEY=a1b2c3d4...`

(Continue for all variables...)
```

F) BENEFITS

✅ All required variables documented  
✅ Validation before startup  
✅ Secure defaults  
✅ Clear error messages  
✅ Production safety

⸻

36) IMPORT/EXPORT DOCUMENTATION (CRITICAL - NEW in Global System Ultimate)

**PURPOSE:** Track all imports/exports to prevent circular dependencies and duplication

A) IMPORTS MAP

Create `/docs/Imports_Map.md`:
```markdown
# Imports Map - Generated: 2025-10-28

## Backend Imports

### models/user.py
```python
from sqlalchemy import Column, Integer, 
String
from database import db
from services.auth import hash_password
```

**Imports:**
- `sqlalchemy` (external)
- `database.db` (internal - database.py)
- `services.auth.hash_password` (internal - services/auth.py)

**Imported By:**
- `services/auth_service.py`
- `routes/user_routes.py`
- `routes/auth_routes.py`

---

### services/auth_service.py
```python
from models.user import User
from utils.jwt import generate_token
```

**Imports:**
- `models.user.User` (internal - models/user.py)
- `utils.jwt.generate_token` (internal - utils/jwt.py)

**Imported By:**
- `routes/auth_routes.py`

---

## Frontend Imports

### components/UserProfile.tsx
```typescript
import { User } from '../types/user';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/client';
```

**Imports:**
- `../types/user.User` (internal)
- `../hooks/useAuth` (internal)
- `../api/client.api` (internal)

**Imported By:**
- `pages/Dashboard.tsx`
- `pages/Profile.tsx`

---

## Circular Dependencies Det
ected

⚠️ **NONE** (Good!)

---

## Unused Imports Detected

⚠️ `utils/deprecated.py` - Not imported anywhere (consider removing)

---

## External Dependencies

### Python
- `sqlalchemy==2.0.23`
- `flask==3.0.0`
- `pydantic==2.5.0`

### JavaScript/TypeScript
- `react@18.2.0`
- `axios@1.6.0`
- `react-router-dom@6.20.0`
```

B) EXPORTS MAP

Create `/docs/Exports_Map.md`:
```markdown
# Exports Map - Generated: 2025-10-28

## Backend Exports

### models/user.py
**Exports:**
- `User` (class) - User model
- `create_user()` (function) - Create new user
- `get_user_by_email()` (function) - Find user by email

**Usage Count:** 15 imports across 8 files

---

### services/auth_service.py
**Exports:**
- `AuthService` (class) - Authentication service
- `login()` (function) - User login
- `logout()` (function) - User logout
- `verify_token()` (function) - Verify JWT token

**Usage Count:** 8 imports across 5 files

---

## Frontend Exports

### types/user.ts
**Exports:**
- `User` (interface) - Use
e, ast.Import):
            for alias in node.names:
                imports.append({
                    'module': alias.name,
                    'alias': alias.asname,
                    'type': 'import'
                })
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append({
                    'module': node.module,
                    'name': alias.name,
                    'alias': alias.asname,
                    'type': 'from'
                })
    
    return imports

def find_circular_dependencies(import_graph: Dict) -> List:
    """Detect circular dependencies"""
    # Implementation using DFS
    pass

def generate_imports_map(root_dir: str):
    """Generate complete imports map"""
    # Scan all Python files
    # Analyze imports
    # Detect circular dependencies
    # Generate markdown report
    pass

if __name__ == '__main__':
    generate_imports_map('./backend')
    generate_imports_map('./frontend')

rity threshold
    
    def get_function_signature(self, func_node: ast.FunctionDef) -> str:
        """Extract normalized function signature"""
        args = [arg.arg for arg in func_node.args.args]
        return f"{func_node.name}({', '.join(args)})"
    
    def get_class_signature(self, class_node: ast.ClassDef) -> str:
        """Extract class signature"""
        methods = []
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                methods.append(node.name)
        return f"{class_node.name}: {', '.join(sorted(methods))}"
    
    def normalize_code(self, code: str) -> str:
        """Normalize code for comparison"""
        # Remove comments, whitespace, docstrings
        tree = ast.parse(code)
        return ast.unparse(tree)
    
    def find_similar_files(self, dir_path: str) -> List[Dict]:
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
    
    if file_duplicates or func_duplicates:
  
 1. Check .env
    print("1. Checking environment...")
    env_result = validate_env()
    if not env_result['valid']:
        errors.extend(env_result['errors'])
    
    # 2. Check documentation exists
    print("2. Checking documentation...")
    required_docs = [
        'docs/File_Map.md',
        'docs/Class_Registry.md',
        'docs/Imports_Map.md',
        'docs/TODO.md',
    ]
    for doc in required_docs:
        if not Path(doc).exists():
            errors.append(f"❌ Missing required documentation: {doc}")
    
    # 3. Check for uncommitted changes
    print("3. Checking git status...")
    import subprocess
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True)
    if result.stdout:
        errors.append("⚠️ You have uncommitted changes. Commit or stash them first.")
    
    # Summary
    if errors:
        print("\n❌ Pre-development checks failed:")
        for error in errors:
            print(f"  {error}")
        print("\nPlease fix the
7):**
- File duplication check
- .env validation
- Import/Export consistency
- Cross-browser tests
- Asset loading tests
- Error handling tests
- Class Registry sync

Version: 3.2.0
Date: 2025-10-28
Status: Production Ready - Critical Fixes Applied
License: Proprietary

Total Sections: 38 (was 28 in Global System Ultimate)
Total Lines: 3000+ (was 1147 in Global System Ultimate)
New Content: +1853 lines (+162%)

⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻

================================================================================
39. PORT CONFIGURATION MANAGEMENT
================================================================================

## Problem
- Applications use inconsistent ports (8000 vs 3000)
- Hard-coded ports in code
- Port conflicts between services
- .env values ignored

## Solution: Single Source of Truth

### config/ports.py
```python
import os
import sys

def get_port(env_var: str, default: int) -> int:
    """Get port from environment with validation"""
    try:
        port = int(os.getenv(env_va
r, default))
    except ValueError:
        print(f"ERROR: Invalid {env_var}. Must be integer.")
        sys.exit(1)
    
    if not (1024 <= port <= 65535):
        print(f"ERROR: {env_var}={port} invalid. Must be 1024-65535.")
        sys.exit(1)
    
    return port

BACKEND_PORT = get_port('BACKEND_PORT', 8000)
FRONTEND_PORT = get_port('FRONTEND_PORT', 3000)
DATABASE_PORT = get_port('DATABASE_PORT', 5432)
REDIS_PORT = get_port('REDIS_PORT', 6379)

# Conflict detection
ports = {
    'BACKEND': BACKEND_PORT,
    'FRONTEND': FRONTEND_PORT,
    'DATABASE': DATABASE_PORT,
    'REDIS': REDIS_PORT,
}

if len(set(ports.values())) != len(ports):
    print("ERROR: Port conflicts detected")
    sys.exit(1)
```

### Usage
```python
# main.py
from config.ports import BACKEND_PORT, FRONTEND_PORT

# FastAPI
app = FastAPI()
uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)

# React/Next.js - package.json
{
  "scripts": {
    "dev": "next dev -p $FRONTEND_PORT"
  }
}
```

### .env Template
```bas
h
# Port Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
DATABASE_PORT=5432
REDIS_PORT=6379
```

### CI Check
```yaml
- name: Validate Ports
  run: python -c "from config.ports import *"
```

## Rules
1. ✅ NEVER hard-code ports
2. ✅ Import from config.ports only
3. ✅ Validate on startup
4. ✅ Check for conflicts
5. ✅ Document in .env.example

================================================================================
40. ORGANIZED DEFINITIONS STRUCTURE
================================================================================

## Problem
- Classes undefined or duplicated
- Import errors
- No central registry
- Inconsistent types

## Solution: Three-Tier Definition System

### Structure
```
config/
├── ports.py                    # Port configuration
└── definitions/
    ├── __init__.py             # Central registry
    ├── common.py               # General-purpose definitions
    ├── core.py                 # Base models & mixins
    └── custom.py               # Project-
specific definitions
```

### common.py - General Purpose
```python
"""Common definitions used across entire project"""

from enum import Enum
from typing import TypedDict, Literal, Any

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class APIResponse(TypedDict):
    success: bool
    message: str
    data: dict[str, Any] | None
    errors: list[str] | None

# Constants
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MIN_PASSWORD_LENGTH = 8
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

### core.py - Base Models
```python
"""Core base models and mixins"""

from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, Field

class BaseModel(PydanticBa
 __init__.py:F401
```

### pyproject.toml
```toml
[tool.autopep8]
max_line_length = 120
aggressive = 2

[tool.black]
line-length = 120
target-version = ['py310', 'py311', 'py312']

[tool.isort]
profile = "black"
line_length = 120
```

### Pre-commit Hook (.git/hooks/pre-commit)
```bash
#!/bin/bash

echo "Checking line length..."

# Check Python files
find . -name "*.py" -not -path "*/venv/*" -not -path "*/.venv/*" | \
  xargs grep -n ".\{121,\}" | \
  grep -v "^#" | \
  grep -v "http" | \
  grep -v '"""' && {
    echo "❌ Lines exceed 120 characters"
    exit 1
  }

echo "✅ All lines ≤ 120 characters"
```

### Auto-fix Script
```bash
#!/bin/bash
# scripts/fix_line_length.sh

echo "Fixing line length..."

# Install tools
pip install autopep8 black isort

# Fix Python files
autopep8 --in-place --aggressive --aggressive \
  --max-line-length=120 \
  --recursive \
  --exclude=venv,.venv,migrations \
  .

black --line-length=120 .
isort --profile=black --line-length=120 .

echo "✅ Line lengt


### middleware/error_handler.py
```python
"""Environment-based error handling middleware"""

import os
import uuid
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime

APP_ENV = os.getenv('APP_ENV', 'development')

async def error_handler_middleware(request: Request, call_next):
    """Handle errors based on environment"""
    try:
        return await call_next(request)
    
    except Exception as e:
        error_id = str(uuid.uuid4())
        
        # Log error (always)
        log_error(error_id, e, request)
        
        if APP_ENV == 'production':
            # Production: Generic error
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "An error occurred. Please contact support.",
                    "error_id": error_id,
                    "timestamp": datetime.utcnow().isoformat()
              
  }
            )
        else:
            # Development: Detailed error
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": str(e),
                    "error_type": type(e).__name__,
                    "error_id": error_id,
                    "traceback": traceback.format_exc(),
                    "request": {
                        "method": request.method,
                        "url": str(request.url),
                        "headers": dict(request.headers)
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

def log_error(error_id: str, error: Exception, request: Request):
    """Log error to file/service"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.error(
        f"Error ID: {error_id}\n"
        f"Type: {type(error).__name__}\n"
        f"Message: {str(error)}\n"
  
      f"URL: {request.url}\n"
        f"Method: {request.method}\n"
        f"Traceback:\n{traceback.format_exc()}"
    )
```

### Frontend Error Display

#### Development
```typescript
// Show detailed errors
if (process.env.NODE_ENV === 'development') {
  console.error('Error:', error);
  toast.error(
    <div>
      <strong>{error.error_type}</strong>
      <p>{error.message}</p>
      <code>{error.traceback}</code>
    </div>
  );
}
```

#### Production
```typescript
// Show generic error
if (process.env.NODE_ENV === 'production') {
  toast.error(
    'An error occurred. Please try again or contact support.'
  );
  // Send to error tracking service
  Sentry.captureException(error);
}
```

### Usage
```python
# main.py
from middleware.error_handler import error_handler_middleware

app = FastAPI()
app.middleware("http")(error_handler_middleware)
```

## Rules
1. ✅ NO stack traces in production
2. ✅ Generic messages in production
3. ✅ Detailed errors in development
4. ✅ Always log wit
h error_id
5. ✅ Track errors in production


================================================================================
43. UNUSED CODE REMOVAL
================================================================================

## Problem
- Unused imports
- Unused variables/functions
- Dead code
- Causes errors and bloat

## Solution: Automated Cleanup

### scripts/remove_unused.sh
```bash
#!/bin/bash

echo "Removing unused code..."

# Install tools
pip install autoflake

# Remove unused imports and variables
autoflake --in-place \
  --remove-all-unused-imports \
  --remove-unused-variables \
  --remove-duplicate-keys \
  --recursive \
  --exclude=venv,.venv,migrations,node_modules \
  .

echo "✅ Unused code removed"
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for unused imports
autoflake --check \
  --remove-all-unused-imports \
  --recursive \
  --exclude=venv,.venv \
  . || {
    echo "❌ Unused imports found. Run: ./scripts/remove_unused.sh"
   
 develop]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

### .github/workflows/deploy.yml
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    environme
nt: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run production checks
        run: |
          python scripts/validate_env.py
          python scripts/map_files.py . docs/File_Map.md
      
      - name: Deploy
        run: |
          # Your deployment script
          echo "Deploying to production..."
```

## Rules
1. ✅ Test on multiple Python versions
2. ✅ Install system dependencies
3. ✅ Cache pip packages
4. ✅ Run all checks
5. ✅ Generate reports

================================================================================
45. IMPORT/EXPORT DOCUMENTATION
================================================================================

## Problem
- No documentation of imports/exports
- Circular dependencies
- Unclear module r
elationships

## Solution: Auto-Generated Documentation

### scripts/document_imports.py
```python
"""
File: scripts/document_imports.py
Generate import/export documentation
"""

import ast
import os
from pathlib import Path
from collections import defaultdict

def analyze_file(filepath: Path) -> dict:
    """Analyze Python file for imports and exports"""
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except:
            return {}
    
    imports = []
    exports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")
        
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if is
instance(target, ast.Name) and target.id == '__all__':
                    if isinstance(node.value, ast.List):
                        exports = [
                            elt.s for elt in node.value.elts
                            if isinstance(elt, ast.Str)
                        ]
    
    return {
        'imports': imports,
        'exports': exports
    }

def generate_documentation(root_dir: str, output_file: str):
    """Generate import/export documentation"""
    
    modules = {}
    
    for filepath in Path(root_dir).rglob('*.py'):
        if 'venv' in str(filepath) or '.venv' in str(filepath):
            continue
        
        rel_path = filepath.relative_to(root_dir)
        analysis = analyze_file(filepath)
        
        if analysis:
            modules[str(rel_path)] = analysis
    
    # Write documentation
    with open(output_file, 'w') as f:
        f.write("# Import/Export Documentation\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\
n")
        
        for module, data in sorted(modules.items()):
            f.write(f"## {module}\n\n")
            
            if data.get('exports'):
                f.write("### Exports\n")
                for exp in data['exports']:
                    f.write(f"- `{exp}`\n")
                f.write("\n")
            
            if data.get('imports'):
                f.write("### Imports\n")
                for imp in data['imports']:
                    f.write(f"- `{imp}`\n")
                f.write("\n")
            
            f.write("---\n\n")

if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    output = sys.argv[2] if len(sys.argv) > 2 else "docs/Imports_Exports.md"
    
    generate_documentation(root, output)
    print(f"✅ Documentation generated: {output}")
```

### Usage
```bash
# Generate documentation
python scripts/document_imports.py . docs/Imports_Exports.md

# Add to CI
- na
**Raises:**
- `ExceptionType`: When this happens

**Example:**
```python
from module_name import function_name

result = function_name(arg1, arg2=value)
print(result)
```

**Dependencies:**
- `dependency1`
- `dependency2`

**Used By:**
- `module_a.py`
- `module_b.py`

---
```

### 47.2 Documentation Standards

**Every shared function MUST have:**
1. ✅ Docstring (Google or Sphinx style)
2. ✅ Type hints
3. ✅ Entry in `function_reference.md`
4. ✅ Unit tests
5. ✅ Usage examples

**Docstring Example (Google Style):**
```python
def calculate_total(items: List[Dict], tax_rate: float = 0.15) -> Decimal:
    """
    Calculate total price including tax.
    
    Args:
        items: List of item dictionaries with 'price' and 'quantity'
        tax_rate: Tax rate as decimal (default: 0.15 for 15%)
    
    Returns:
        Total price including tax as Decimal
    
    Raises:
        ValueError: If items list is empty or tax_rate is negative
    
    Example:
        >>> items = [{'price': 10.0, 
documented = []
    for file_path, func_name in functions:
        if f"`{func_name}`" not in content:
            undocumented.append(f"{file_path}::{func_name}")
    
    if undocumented:
        print("❌ Undocumented functions found:")
        for func in undocumented:
            print(f"  - {func}")
        print("\nPlease add them to docs/function_reference.md")
        return False
    
    print("✅ All shared functions are documented")
    return True

if __name__ == '__main__':
    functions = find_shared_functions()
    if not check_documented(functions):
        sys.exit(1)
```

---

## 48. Error Tracking System

### 48.1 Error Log File (APPEND-ONLY)

**Location:** `docs/errors/Dont_make_this_error_again.md`

**Rules:**
- **APPEND-ONLY** - Never delete entries
- Document every significant error
- Include root cause and solution
- Add prevention measures

**Template:**
```markdown
## Error #XXX: [Brief Title]

**Date:** YYYY-MM-DD
**Severity:** Critical / High / Medium / Low

   patterns = []
    with open(error_file) as f:
        content = f.read()
    
    # Extract code patterns that caused errors
    # This is a simplified example
    pattern_blocks = re.findall(r'```python\n# WRONG:(.*?)```', content, re.DOTALL)
    for block in pattern_blocks:
        patterns.append(block.strip())
    
    return patterns

def check_files_for_patterns(patterns):
    """Check Python files for error patterns."""
    issues_found = False
    
    for py_file in Path('.').rglob('*.py'):
        if 'test_' in str(py_file) or '__pycache__' in str(py_file):
            continue
        
        with open(py_file) as f:
            content = f.read()
        
        for pattern in patterns:
            if pattern in content:
                print(f"⚠️  Known error pattern found in {py_file}")
                print(f"   Pattern: {pattern[:50]}...")
                issues_found = True
    
    return issues_found

if __name__ == '__main__':
    patterns = load_error_patterns
ort ast
from pathlib import Path
from collections import defaultdict

def analyze_module(file_path):
    """Analyze a Python module."""
    with open(file_path) as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return None
    
    info = {
        'classes': [],
        'functions': [],
        'imports': [],
        'dependencies': set()
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            info['classes'].append(node.name)
        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):
                info['functions'].append(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom) and node.module:
                info['dependencies'].add(node.module.split('.')[0])
    
    return info

def generate_map():
    """Generate module map."""
    modules = defaultdict(dict)
    
    for py_file in Path('.')
.rglob('*.py'):
        if '__pycache__' in str(py_file) or 'venv' in str(py_file):
            continue
        
        info = analyze_module(py_file)
        if info:
            modules[str(py_file)] = info
    
    # Write to markdown
    with open('docs/Module_Map.md', 'w') as f:
        f.write("# Module Map\n\n")
        f.write("**Generated:** Auto-generated\n\n")
        f.write("## Modules by Directory\n\n")
        
        # Group by directory
        by_dir = defaultdict(list)
        for path in sorted(modules.keys()):
            dir_name = str(Path(path).parent)
            by_dir[dir_name].append(path)
        
        for dir_name in sorted(by_dir.keys()):
            f.write(f"### `{dir_name}/`\n\n")
            for path in sorted(by_dir[dir_name]):
                info = modules[path]
                f.write(f"#### `{Path(path).name}`\n\n")
                
                if info['classes']:
                    f.write("**Classes:**\n")
                    for cls
 in info['classes']:
                        f.write(f"- `{cls}`\n")
                    f.write("\n")
                
                if info['functions']:
                    f.write("**Functions:**\n")
                    for func in info['functions']:
                        f.write(f"- `{func}()`\n")
                    f.write("\n")
                
                if info['dependencies']:
                    f.write("**Dependencies:**\n")
                    for dep in sorted(info['dependencies']):
                        f.write(f"- `{dep}`\n")
                    f.write("\n")
        
        # Dependency graph
        f.write("## Dependency Graph\n\n")
        f.write("```mermaid\n")
        f.write("graph TD\n")
        for path, info in modules.items():
            module_name = Path(path).stem
            for dep in info['dependencies']:
                f.write(f"  {module_name} --> {dep}\n")
        f.write("```\n")

if __name__ == '__main__':
    generate_map()
    pri
startswith(('django', 'flask', 'fastapi')):
                    deps.add(node.module.split('.')[0])
    
    return deps

def topological_sort(modules):
    """Sort modules by dependency order."""
    # Build dependency graph
    graph = {}
    in_degree = defaultdict(int)
    
    for module, deps in modules.items():
        graph[module] = deps
        for dep in deps:
            in_degree[dep] += 1
    
    # Find modules with no dependencies
    queue = [m for m in graph if in_degree[m] == 0]
    result = []
    
    while queue:
        module = queue.pop(0)
        result.append(module)
        
        for dep in graph.get(module, []):
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)
    
    return result

def main():
    """Analyze and print dependency order."""
    modules = {}
    
    for py_file in Path('.').rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        module_name = str(
py_file).replace('/', '.').replace('.py', '')
        deps = get_dependencies(py_file)
        modules[module_name] = deps
    
    order = topological_sort(modules)
    
    print("📊 Module Build Order (Least Dependent First):\n")
    for i, module in enumerate(order, 1):
        deps = modules.get(module, set())
        print(f"{i:3d}. {module}")
        if deps:
            print(f"     Dependencies: {', '.join(sorted(deps))}")
    
    print(f"\n✅ Total modules: {len(order)}")
    print(f"✅ Start with: {order[0] if order else 'None'}")

if __name__ == '__main__':
    main()
```

**Usage:**
```bash
python scripts/analyze_dependencies.py
```

### 49.4 Reusability Guidelines

**Before Creating New Code:**
1. ✅ Search existing modules
2. ✅ Check function reference
3. ✅ Review module map
4. ✅ Analyze dependencies
5. ✅ Reuse if possible
6. ✅ Extend if needed
7. ✅ Create only if necessary

**When Reusing:**
- Import, don't copy
- Extend via inheritance
- Compose via delegation
- Document 
functions
- Extract class into separate file
- Split file into multiple files
- Create submodules

### 51.2 Single Responsibility Principle (SRP)

**Each function/class should do ONE thing.**

**Bad Example:**
```python
def process_order(order_data):
    # Validates, calculates, saves, sends email - TOO MUCH!
    if not order_data.get('customer_id'):
        raise ValueError("Missing customer")
    
    total = sum(item['price'] * item['qty'] for item in order_data['items'])
    tax = total * 0.15
    final_total = total + tax
    
    order = Order.objects.create(
        customer_id=order_data['customer_id'],
        total=final_total
    )
    
    send_email(order.customer.email, f"Order {order.id} confirmed")
    
    return order
```

**Good Example:**
```python
def validate_order_data(order_data: Dict) -> None:
    """Validate order data."""
    if not order_data.get('customer_id'):
        raise ValueError("Missing customer")

def calculate_order_total(items: List[Dict]) -> Dec
imal:
    """Calculate order total with tax."""
    subtotal = sum(Decimal(str(item['price'])) * item['qty'] for item in items)
    tax = subtotal * Decimal('0.15')
    return subtotal + tax

def create_order(customer_id: int, total: Decimal) -> Order:
    """Create order in database."""
    return Order.objects.create(customer_id=customer_id, total=total)

def send_order_confirmation(order: Order) -> None:
    """Send order confirmation email."""
    send_email(order.customer.email, f"Order {order.id} confirmed")

def process_order(order_data: Dict) -> Order:
    """Process complete order workflow."""
    validate_order_data(order_data)
    total = calculate_order_total(order_data['items'])
    order = create_order(order_data['customer_id'], total)
    send_order_confirmation(order)
    return order
```

### 51.3 DRY (Don't Repeat Yourself)

**If code appears 3+ times, extract it.**

**Bad Example:**
```python
# In multiple files
def view1(request):
    if not request.user.is_authenti
cated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    # ...

def view2(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    # ...
```

**Good Example:**
```python
# utils/auth.py
def require_auth(view_func):
    """Decorator to require authentication."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

# views.py
@require_auth
def view1(request):
    # ...

@require_auth
def view2(request):
    # ...
```

### 51.4 Refactoring Large Files

**Script:** `scripts/suggest_refactoring.py`
```python
#!/usr/bin/env python3
"""Suggest refactoring for large files/functions."""

import ast
from pathlib import Path

def analyze_file(file_path):
    """Analyze file for refactoring opportunities."""
    wit
h open(file_path) as f:
        content = f.read()
        lines = content.split('\n')
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return None
    
    issues = []
    
    # Check file length
    if len(lines) > 500:
        issues.append(f"File too long: {len(lines)} lines (max 500)")
    
    # Check function lengths
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_lines = node.end_lineno - node.lineno
            if func_lines > 50:
                issues.append(
                    f"Function '{node.name}' too long: {func_lines} lines (max 50)"
                )
        
        elif isinstance(node, ast.ClassDef):
            class_lines = node.end_lineno - node.lineno
            if class_lines > 300:
                issues.append(
                    f"Class '{node.name}' too long: {class_lines} lines (max 300)"
                )
    
    return issues

def main():
    """Check all Python files.""
"
    all_issues = {}
    
    for py_file in Path('.').rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        issues = analyze_file(py_file)
        if issues:
            all_issues[str(py_file)] = issues
    
    if all_issues:
        print("🔧 Refactoring Suggestions:\n")
        for file_path, issues in all_issues.items():
            print(f"📄 {file_path}")
            for issue in issues:
                print(f"   ⚠️  {issue}")
            print()
        
        print(f"Total files needing refactoring: {len(all_issues)}")
    else:
        print("✅ All files are well-modularized!")

if __name__ == '__main__':
    main()
```

**Usage:**
```bash
python scripts/suggest_refactoring.py
```

---

## 52. Enhanced File Header Policy

### 52.1 Mandatory File Header

**Every file MUST start with:**

**Python:**
```python
"""
File: path/to/file.py
Module: module_name
Created: YYYY-MM-DD
Last Modified: YYYY-MM-DD
Author: author_name
Description: Br
k Python file header."""
    with open(file_path) as f:
        content = f.read(500)  # First 500 chars
    
    if not content.startswith('"""'):
        return False, "Missing docstring header"
    
    for field in REQUIRED_FIELDS:
        if field not in content:
            return False, f"Missing field: {field}"
    
    return True, "OK"

def check_ts_header(file_path):
    """Check TypeScript/JavaScript file header."""
    with open(file_path) as f:
        content = f.read(500)
    
    if not content.startswith('/**'):
        return False, "Missing JSDoc header"
    
    for field in REQUIRED_FIELDS:
        if field not in content:
            return False, f"Missing field: {field}"
    
    return True, "OK"

def main():
    """Check all files."""
    issues = []
    
    for file_path in Path('.').rglob('*'):
        if file_path.suffix == '.py' and '__pycache__' not in str(file_path):
            ok, msg = check_python_header(file_path)
            if not ok:
          
      issues.append(f"{file_path}: {msg}")
        
        elif file_path.suffix in ('.ts', '.tsx', '.js', '.jsx'):
            ok, msg = check_ts_header(file_path)
            if not ok:
                issues.append(f"{file_path}: {msg}")
    
    if issues:
        print("❌ File header issues found:\n")
        for issue in issues:
            print(f"  {issue}")
        sys.exit(1)
    
    print("✅ All file headers are correct")

if __name__ == '__main__':
    main()
```

### 52.3 Auto-generate Headers

**Script:** `scripts/add_file_headers.py`
```python
#!/usr/bin/env python3
"""Add headers to files missing them."""

from pathlib import Path
from datetime import date

PYTHON_TEMPLATE = '''"""
File: {path}
Module: {module}
Created: {date}
Last Modified: {date}
Author: {author}
Description: TODO: Add description

Dependencies:
- TODO: List dependencies

Related Files:
- TODO: List related files
"""

'''

def add_python_header(file_path, author="Team"):
    """Add header to Python 
file."""
    with open(file_path) as f:
        content = f.read()
    
    if content.startswith('"""'):
        print(f"⏭️  {file_path} already has header")
        return
    
    module = str(file_path).replace('/', '.').replace('.py', '')
    header = PYTHON_TEMPLATE.format(
        path=file_path,
        module=module,
        date=date.today().isoformat(),
        author=author
    )
    
    with open(file_path, 'w') as f:
        f.write(header + content)
    
    print(f"✅ Added header to {file_path}")

def main():
    """Add headers to all Python files."""
    for py_file in Path('.').rglob('*.py'):
        if '__pycache__' not in str(py_file):
            add_python_header(py_file)

if __name__ == '__main__':
    main()
```


---

## 53. Frontend/Backend Testing Strategy

### 53.1 Backend Testing (Python)

**Tools:**
```bash
pip install pytest pytest-cov pytest-django pytest-mock
pip install flake8 autopep8 pylint mypy
```

**Test Structure:**
```
tests/
├── unit/         
f):
        """Create OrderService instance."""
        return OrderService()
    
    @pytest.fixture
    def sample_order_data(self):
        """Sample order data."""
        return {
            'customer_id': 1,
            'items': [
                {'price': '10.00', 'qty': 2},
                {'price': '5.00', 'qty': 3}
            ]
        }
    
    def test_calculate_total_success(self, order_service, sample_order_data):
        """Test successful total calculation."""
        total = order_service.calculate_total(sample_order_data['items'])
        expected = Decimal('35.00') * Decimal('1.15')  # With 15% tax
        assert total == expected
    
    def test_calculate_total_empty_items(self, order_service):
        """Test calculation with empty items."""
        with pytest.raises(ValueError, match="Items list cannot be empty"):
            order_service.calculate_total([])
    
    @patch('services.order_service.Order.objects.create')
    def test_create_order(self, mock
-manager

# Playwright
pip install playwright
playwright install
```

**Test Structure:**
```
tests/frontend/
├── test_login.py
├── test_dashboard.py
├── test_orders.py
└── conftest.py
```

**Playwright Example:**
```python
"""
File: tests/frontend/test_login.py
Module: tests.frontend.test_login
Created: 2025-01-15
Author: Team
Description: Frontend tests for login functionality
"""

import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page(browser):
    """Create new page for each test."""
    page = browser.new_page()
    yield page
    page.close()

def test_login_success(page: Page):
    """Test successful login."""
    # Navigate
    page.goto("http://{HOST}:{FRONTEND_PORT}/login")
    
    # Fill form
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password"]', 'testpass123')
    
    # Submit
    page.click('button[type="submit"]')
    
    # Verify redirect
    expect(page).to_have_url("http://{HOST}:{F
RONTEND_PORT}/dashboard")
    
    # Verify welcome message
    expect(page.locator('text=Welcome, testuser')).to_be_visible()

def test_login_invalid_credentials(page: Page):
    """Test login with invalid credentials."""
    page.goto("http://{HOST}:{FRONTEND_PORT}/login")
    
    page.fill('input[name="username"]', 'invalid')
    page.fill('input[name="password"]', 'wrong')
    page.click('button[type="submit"]')
    
    # Should show error
    expect(page.locator('text=Invalid credentials')).to_be_visible()
    
    # Should stay on login page
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/login")

def test_login_validation(page: Page):
    """Test form validation."""
    page.goto("http://{HOST}:{FRONTEND_PORT}/login")
    
    # Try to submit empty form
    page.click('button[type="submit"]')
    
    # Should show validation errors
    expect(page.locator('text=Username is required')).to_be_visible()
    expect(page.locator('text=Password is required')).to_be_visi
ble()
```

**Selenium Example:**
```python
"""
File: tests/frontend/test_dashboard_selenium.py
Module: tests.frontend.test_dashboard_selenium
Created: 2025-01-15
Author: Team
Description: Selenium tests for dashboard
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    """Create WebDriver instance."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_dashboard_loads(driver):
    """Test dashboard page loads correctly."""
    driver.get("http://{HOST}:{FRONTEND_PORT}/dashboard")
    
    # Wait for page load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
    )
    
    # Check title
    assert "Dashboard" in driver.title
    
    # Check key elements
    assert driver.find_eleme
nt(By.ID, "user-menu")
    assert driver.find_element(By.CLASS_NAME, "stats-widget")

def test_dashboard_navigation(driver):
    """Test navigation from dashboard."""
    driver.get("http://{HOST}:{FRONTEND_PORT}/dashboard")
    
    # Click on Orders link
    orders_link = driver.find_element(By.LINK_TEXT, "Orders")
    orders_link.click()
    
    # Should navigate to orders page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/orders")
    )
    
    assert "/orders" in driver.current_url
```

**Running Frontend Tests:**
```bash
# Playwright
pytest tests/frontend/ --headed  # With browser UI
pytest tests/frontend/ --browser=firefox

# Selenium
pytest tests/frontend/test_dashboard_selenium.py
```

### 53.3 Integration Tests

**Example:**
```python
"""
File: tests/integration/test_order_api.py
Module: tests.integration.test_order_api
Created: 2025-01-15
Author: Team
Description: Integration tests for order API
"""

import pytest
from django.test import Client
from decima
l import Decimal
from models import Order, Customer

@pytest.fixture
def client():
    """Create test client."""
    return Client()

@pytest.fixture
def customer(db):
    """Create test customer."""
    return Customer.objects.create(
        name="Test Customer",
        email="test@example.com"
    )

@pytest.mark.django_db
def test_create_order_api(client, customer):
    """Test order creation via API."""
    data = {
        'customer_id': customer.id,
        'items': [
            {'product_id': 1, 'quantity': 2, 'price': '10.00'},
            {'product_id': 2, 'quantity': 1, 'price': '15.00'}
        ]
    }
    
    response = client.post('/api/orders/', data, content_type='application/json')
    
    assert response.status_code == 201
    assert 'id' in response.json()
    
    # Verify in database
    order = Order.objects.get(id=response.json()['id'])
    assert order.customer == customer
    assert order.total == Decimal('40.25')  # (20 + 15) * 1.15 tax
```

### 53.4 E2E T
ests

**Example:**
```python
"""
File: tests/e2e/test_order_workflow.py
Module: tests.e2e.test_order_workflow
Created: 2025-01-15
Author: Team
Description: End-to-end test for complete order workflow
"""

import pytest
from playwright.sync_api import Page, expect

def test_complete_order_workflow(page: Page):
    """Test complete order creation workflow."""
    # 1. Login
    page.goto("http://{HOST}:{FRONTEND_PORT}/login")
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password"]', 'testpass123')
    page.click('button[type="submit"]')
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/dashboard")
    
    # 2. Navigate to orders
    page.click('text=Orders')
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/orders")
    
    # 3. Create new order
    page.click('button:has-text("New Order")')
    expect(page.locator('h1:has-text("Create Order")')).to_be_visible()
    
    # 4. Fill order form
    page.select_option('select[name="cust
omer"]', label='Test Customer')
    page.click('button:has-text("Add Item")')
    page.select_option('select[name="items[0].product"]', label='Product A')
    page.fill('input[name="items[0].quantity"]', '2')
    
    # 5. Submit order
    page.click('button[type="submit"]:has-text("Create Order")')
    
    # 6. Verify success
    expect(page.locator('text=Order created successfully')).to_be_visible()
    expect(page).to_have_url("http://{HOST}:{FRONTEND_PORT}/orders")
    
    # 7. Verify order appears in list
    expect(page.locator('table tbody tr').first).to_contain_text('Test Customer')
```

---

## 54. Module Quality Standards

### 54.1 Follow 'sales' Module Standards

**The 'sales' module is the gold standard. All modules should match its quality.**

**Key Characteristics:**
1. **Professional Organization**
   - Separate folders for models, views, services, tests
   - Clear separation of concerns
   - Logical file structure

2. **Advanced Models**
   - Comprehensive relationshi
 للنموذج."""
        return f"{self.code} - {self.name}"
    
    def confirm(self):
        """
        تأكيد النموذج.
        
        يقوم بتغيير الحالة إلى مؤكد وحفظ تاريخ التأكيد.
        
        Raises:
            ValueError: إذا كان النموذج ليس في حالة مسودة
        """
        if self.state != self.STATE_DRAFT:
            raise ValueError("لا يمكن تأكيد نموذج غير مسودة")
        
        from django.utils import timezone
        self.state = self.STATE_CONFIRMED
        self.confirmed_at = timezone.now()
        self.save()
    
    def cancel(self):
        """
        إلغاء النموذج.
        
        يقوم بتغيير الحالة إلى ملغي.
        
        Raises:
            ValueError: إذا كان النموذج ملغي بالفعل
        """
        if self.state == self.STATE_CANCELLED:
            raise ValueError("النموذج ملغي بالفعل")
        
        self.state = self.STATE_CANCELLED
        self.save()
    
    def compute_total(self):
        """
        حساب الإجمالي.
        
        يقوم ب
stants and definitions

Dependencies: None
"""

from decimal import Decimal

# Application
APP_NAME = "{YOUR_PROJECT_NAME}"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Enterprise Resource Planning System"

# Ports (SINGLE SOURCE OF TRUTH)
BACKEND_PORT = 8000
FRONTEND_PORT = 3000
API_PORT = 8000

# URLs
BACKEND_URL = f"http://{HOST}:{BACKEND_PORT}"
FRONTEND_URL = f"http://{HOST}:{FRONTEND_PORT}"
API_BASE_URL = f"{BACKEND_URL}/api"

# Database
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Business Rules
DEFAULT_TAX_RATE = Decimal('0.15')  # 15%
DEFAULT_CURRENCY = 'SAR'
DEFAULT_LANGUAGE = 'ar'

# File Upload
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
ALLOWED_DOCUMENT_TYPES = ['application/pdf', 'application/msword']

# Validation
MIN_PASSWORD_LENGTH = 8
MAX_USERNAME_LENGTH = 50
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# States
STATE_DRAFT = 'draft'
STATE_CONFIRMED = 'confirmed'
STATE_CANCELLED = 'cancelled
'
STATE_DONE = 'done'

COMMON_STATES = [
    (STATE_DRAFT, 'مسودة'),
    (STATE_CONFIRMED, 'مؤكد'),
    (STATE_CANCELLED, 'ملغي'),
    (STATE_DONE, 'منتهي'),
]

# Permissions
PERM_VIEW = 'view'
PERM_CREATE = 'create'
PERM_EDIT = 'edit'
PERM_DELETE = 'delete'
PERM_ADMIN = 'admin'

ALL_PERMISSIONS = [PERM_VIEW, PERM_CREATE, PERM_EDIT, PERM_DELETE, PERM_ADMIN]

# Error Messages
ERROR_REQUIRED_FIELD = "هذا الحقل مطلوب"
ERROR_INVALID_EMAIL = "البريد الإلكتروني غير صحيح"
ERROR_PASSWORD_TOO_SHORT = f"كلمة المرور يجب أن تكون {MIN_PASSWORD_LENGTH} أحرف على الأقل"
ERROR_UNAUTHORIZED = "غير مصرح"
ERROR_NOT_FOUND = "غير موجود"
ERROR_INTERNAL_SERVER = "خطأ في الخادم"

# Success Messages
SUCCESS_CREATED = "تم الإنشاء بنجاح"
SUCCESS_UPDATED = "تم التحديث بنجاح"
SUCCESS_DELETED = "تم الحذف بنجاح"
SUCCESS_CONFIRMED = "تم التأكيد بنجاح"
```

### 55.2 Type Definitions

**Location:** `config/definitions/types.py`

```python
"""
File: config/definitions/types.py
Module: config.definitions.types
Created: 20
ubtotal: Decimal
    tax: Decimal
    total: Decimal
    state: StateType
    created_at: datetime
```

### 55.3 Environment-Specific Configs

**Location:** `config/environments/`

```python
# config/environments/development.py
"""Development environment configuration."""

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASE_URL = 'sqlite:///db.sqlite3'
LOG_LEVEL = 'DEBUG'
SHOW_ERRORS_IN_FRONTEND = True

# config/environments/production.py
"""Production environment configuration."""

DEBUG = False
ALLOWED_HOSTS = ['example.com', 'www.example.com']
DATABASE_URL = 'postgresql://user:pass@localhost/{database_name}'
LOG_LEVEL = 'WARNING'
SHOW_ERRORS_IN_FRONTEND = False
REQUIRE_HTTPS = True
```

### 55.4 Usage

**Import constants:**
```python
from config.constants import (
    BACKEND_PORT,
    DEFAULT_TAX_RATE,
    STATE_CONFIRMED,
    ERROR_REQUIRED_FIELD
)

# Use in code
app.run(port=BACKEND_PORT)
tax = subtotal * DEFAULT_TAX_RATE
if order.state == STATE_CONFIRMED:
    # ...

```

**No magic numbers/strings:**
```python
# ❌ BAD
if order.state == 'confirmed':
    tax = total * 0.15

# ✅ GOOD
from config.constants import STATE_CONFIRMED, DEFAULT_TAX_RATE

if order.state == STATE_CONFIRMED:
    tax = total * DEFAULT_TAX_RATE
```


---

## 56. Dependency Management

### 56.1 Using pipreqs

**Install:**
```bash
pip install pipreqs
```

**Generate requirements AFTER finishing modules:**
```bash
# Generate from actual imports
pipreqs . --force

# For specific directory
pipreqs ./module_name --force

# Save to specific file
pipreqs . --savepath requirements-new.txt
```

**Why pipreqs?**
- Only includes actually used packages
- Avoids bloat from `pip freeze`
- Scans imports, not installed packages

### 56.2 Requirements Files Structure

```
requirements/
├── base.txt          # Core dependencies (always needed)
├── development.txt   # Dev tools (testing, linting)
├── production.txt    # Production-only (gunicorn, etc.)
└── testing.txt       # Testing-only (pytest, c
use ~= for minor updates
django~=4.2.0  # Allows 4.2.x, not 4.3.0
```

### 56.4 Security Updates

**Check for vulnerabilities:**
```bash
# Install safety
pip install safety

# Check dependencies
safety check

# Check specific file
safety check -r requirements.txt

# Auto-fix (with caution)
safety check --auto-update
```

**Update dependencies:**
```bash
# Check outdated
pip list --outdated

# Update specific package
pip install --upgrade package_name

# Regenerate requirements
pipreqs . --force
```

### 56.5 Workflow

**Development:**
```bash
# Install dev dependencies
pip install -r requirements/development.txt

# Work on code...

# Before committing
pipreqs . --force  # Regenerate base requirements
safety check       # Check security
```

**Production:**
```bash
# Install only production dependencies
pip install -r requirements/production.txt
```

**Testing:**
```bash
# Install test dependencies
pip install -r requirements/testing.txt

# Run tests
pytest
```

---

## 57. Design vs Im
                 models.add(node.name)
    
    return models

def load_design_spec(spec_file: str) -> Dict:
    """Load design specification."""
    with open(spec_file) as f:
        return json.load(f)

def analyze_gaps(spec_file: str = 'docs/design_spec.json'):
    """Analyze gaps between design and implementation."""
    print("🔍 Analyzing Design vs Implementation Gaps\n")
    
    # Load design spec
    try:
        spec = load_design_spec(spec_file)
    except FileNotFoundError:
        print(f"⚠️  Design spec not found: {spec_file}")
        print("   Create docs/design_spec.json with your design")
        return
    
    # Find implementation
    api_endpoints = find_api_endpoints()
    frontend_routes = find_frontend_routes()
    db_models = find_database_models()
    
    # Compare
    gaps = []
    
    # Check API endpoints
    if 'api_endpoints' in spec:
        for endpoint in spec['api_endpoints']:
            if endpoint not in api_endpoints:
                gaps.appen
d(f"Missing API endpoint: {endpoint}")
    
    # Check frontend routes
    if 'frontend_routes' in spec:
        for route in spec['frontend_routes']:
            if route not in frontend_routes:
                gaps.append(f"Missing frontend route: {route}")
    
    # Check database models
    if 'models' in spec:
        for model in spec['models']:
            if model not in db_models:
                gaps.append(f"Missing database model: {model}")
    
    # Report
    if gaps:
        print("❌ Gaps Found:\n")
        for gap in gaps:
            print(f"  • {gap}")
        print(f"\nTotal gaps: {len(gaps)}")
    else:
        print("✅ No gaps found! Design matches implementation.")
    
    # Summary
    print("\n📊 Summary:")
    print(f"  API Endpoints: {len(api_endpoints)} implemented")
    print(f"  Frontend Routes: {len(frontend_routes)} implemented")
    print(f"  Database Models: {len(db_models)} implemented")

if __name__ == '__main__':
    analyze_gaps()
```

### 57.3 D
esign Specification Template

**Location:** `docs/design_spec.json`

```json
{
  "module_name": "orders",
  "version": "1.0.0",
  "api_endpoints": [
    "/api/orders/",
    "/api/orders/<id>/",
    "/api/orders/<id>/confirm/",
    "/api/orders/<id>/cancel/"
  ],
  "frontend_routes": [
    "/orders",
    "/orders/new",
    "/orders/:id",
    "/orders/:id/edit"
  ],
  "models": [
    "Order",
    "OrderItem",
    "Customer"
  ],
  "relationships": [
    {
      "from": "Order",
      "to": "Customer",
      "type": "ForeignKey"
    },
    {
      "from": "OrderItem",
      "to": "Order",
      "type": "ForeignKey"
    }
  ],
  "features": [
    "Create order",
    "Edit order",
    "Confirm order",
    "Cancel order",
    "View order list",
    "Search orders",
    "Filter by status",
    "Export to PDF"
  ]
}
```

### 57.4 Integration Testing

**Test that design features work end-to-end:**

```python
"""
File: tests/integration/test_order_integration.py
Module: tests.integration.test_or
der_integration
Created: 2025-01-15
Author: Team
Description: Integration tests for complete order workflow
"""

import pytest
from django.test import Client
from models import Order, Customer

@pytest.mark.django_db
class TestOrderIntegration:
    """Test complete order integration."""
    
    def test_order_workflow(self, client: Client):
        """Test complete order workflow from design spec."""
        # 1. Create customer
        customer = Customer.objects.create(name="Test", email="test@example.com")
        
        # 2. Create order via API
        response = client.post('/api/orders/', {
            'customer_id': customer.id,
            'items': [{'product_id': 1, 'quantity': 2}]
        }, content_type='application/json')
        assert response.status_code == 201
        order_id = response.json()['id']
        
        # 3. Retrieve order
        response = client.get(f'/api/orders/{order_id}/')
        assert response.status_code == 200
        assert response.json()
['state'] == 'draft'
        
        # 4. Confirm order
        response = client.post(f'/api/orders/{order_id}/confirm/')
        assert response.status_code == 200
        
        # 5. Verify state changed
        order = Order.objects.get(id=order_id)
        assert order.state == 'confirmed'
        
        # 6. Cancel order
        response = client.post(f'/api/orders/{order_id}/cancel/')
        assert response.status_code == 200
        
        # 7. Verify cancelled
        order.refresh_from_db()
        assert order.state == 'cancelled'
```

---

## Summary: Global System Ultimate Additions

### New Sections (46-57)

**🔴 Critical (46-49):**
- 46. Comprehensive Verification System
- 47. Function Reference System
- 48. Error Tracking System
- 49. Module Discovery & Reuse

**🟡 High Priority (50-55):**
- 50. Task Management System
- 51. Code Modularization
- 52. Enhanced File Header Policy
- 53. Frontend/Backend Testing Strategy
- 54. Module Quality Standards
- 55. Constants & Definitions Reg
e updated automatically
module_name = "models.user_unified"
mod = __import__(module_name)
```
**Action:** Manual review required

**2. String References**
```python
# Cannot be updated automatically
MODELS = ["models.user_unified", "models.product"]
```
**Action:** Manual review required

**3. Comments**
```python
# See models.user_unified for details
```
**Action:** Update comments manually or with separate tool

### 61.7 Integration with Smart Merge

```bash
# Smart merge automatically calls update_imports
python scripts/smart_merge.py

# Internally calls:
# python scripts/update_imports.py old_module new_module
```

### 61.8 CI/CD Integration

```yaml
- name: Verify Imports
  run: |
    python -c "import sys; import importlib; \
    [importlib.import_module(m) for m in sys.argv[1:]]" \
    $(find . -name "*.py" -exec grep -l "^import\|^from" {} \;)
```

### 61.9 Post-Update Checklist

- [ ] All imports updated
- [ ] No syntax errors
- [ ] No import errors
- [ ] All tests pass
- [ ] 
ages:
    - core: Core functionality
    - models: Data models
    - services: Business logic
    - api: API endpoints
    - utils: Utility functions
"""

# Import commonly used items from subpackages
from .core import App, Config
from .models import User, Session
from .services import UserService, AuthService

# Version info
from .version import __version__, __version_info__

# Public API
__all__ = [
    # Core
    'App',
    'Config',
    # Models
    'User',
    'Session',
    # Services
    'UserService',
    'AuthService',
    # Version
    '__version__',
    '__version_info__',
]

# Subpackage references (for documentation)
__subpackages__ = [
    'core',
    'models',
    'services',
    'api',
    'utils',
]
```

### Pattern 6: Plugin System

```python
# plugins/__init__.py
"""
Plugin system with dynamic discovery
"""

import importlib
import pkgutil
from typing import Dict, Type

# Plugin registry
_plugins: Dict[str, Type] = {}


def discover_plugins():
    """Automatically di
scover and register plugins"""
    package = __package__
    for _, name, _ in pkgutil.iter_modules([package.replace('.', '/')]):
        module = importlib.import_module(f'{package}.{name}')
        if hasattr(module, 'register_plugin'):
            plugin = module.register_plugin()
            _plugins[plugin.name] = plugin


def get_plugin(name: str):
    """Get plugin by name"""
    if not _plugins:
        discover_plugins()
    return _plugins.get(name)


__all__ = [
    'discover_plugins',
    'get_plugin',
]
```

### Pattern 7: Conditional Imports

```python
# compat/__init__.py
"""
Compatibility layer for different Python versions
"""

import sys

# Version-specific imports
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

# Platform-specific imports
if sys.platform == 'win32':
    from .windows import WindowsSpecific as PlatformSpecific
else:
    from .unix import UnixSpecific as PlatformSpecific

__all__ = [
 
m typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .post import Post

class User:
    def get_posts(self) -> List['Post']:  # String annotation
        from .post import Post
        return Post.query.filter_by(user_id=self.id).all()

# ✅ SOLUTION 3: Restructure - create base module
# models/base.py - common base classes
# models/user.py - imports from base
# models/post.py - imports from base
# models/__init__.py - imports both
```

### Problem 2: Import Order Issues

```python
# ✅ CORRECT ORDER in __init__.py

# 1. Standard library imports
import os
import sys
from typing import Dict, List

# 2. Third-party imports
import requests
from sqlalchemy import create_engine

# 3. Local imports - order matters!
from .exceptions import ConfigError  # No dependencies
from .constants import DEFAULT_CONFIG  # Uses exceptions
from .validators import validate  # Uses constants and exceptions
from .config import Config  # Uses all above

# 4. __all__ definition
__all__ = [
    'Config'
,
    'ConfigError',
    'DEFAULT_CONFIG',
    'validate',
]
```

### Problem 3: Namespace Pollution

```python
# ❌ BAD: Pollutes namespace
# utils/__init__.py
from .helpers import *
from .validators import *
from .formatters import *
# Now namespace has 50+ items!

# ✅ GOOD: Clean namespace
# utils/__init__.py
"""Utilities package - import submodules as needed"""

# Only export the most commonly used
from .helpers import format_date, parse_json
from .validators import is_valid_email

__all__ = [
    'format_date',
    'parse_json',
    'is_valid_email',
    # For less common items, use: from utils.helpers import ...
]

# Make submodules accessible
from . import helpers
from . import validators
from . import formatters
```

---

## 5. أمثلة حسب حجم المشروع / Examples by Project Size

### Small Project (< 10 modules)

```python
# mysmallapp/__init__.py
"""Small application - simple structure"""

from .main import run_app
from .config import Config
from .utils import helper_function

__v


import mypackage


def test_public_api_available():
    """Test that public API is accessible"""
    assert hasattr(mypackage, 'PublicClass')
    assert hasattr(mypackage, 'public_function')


def test_private_not_exposed():
    """Test that private items are not in public API"""
    assert not hasattr(mypackage, '_private_helper')


def test_all_defined():
    """Test that __all__ is properly defined"""
    assert hasattr(mypackage, '__all__')
    assert isinstance(mypackage.__all__, list)
    assert len(mypackage.__all__) > 0


def test_all_items_exist():
    """Test that all items in __all__ actually exist"""
    for item in mypackage.__all__:
        assert hasattr(mypackage, item), f"{item} in __all__ but not found"


def test_version_available():
    """Test that version info is available"""
    assert hasattr(mypackage, '__version__')
    assert isinstance(mypackage.__version__, str)


def test_no_import_side_effects():
    """Test that importing doesn't have side effects"""
 
 جديدة

### Testing
- [ ] يوجد tests للـ public API
- [ ] tests تتحقق من `__all__`
- [ ] tests تتحقق من عدم وجود side effects

---

## 8. أدوات مساعدة / Helper Tools

### Script للتحقق من __init__.py

```python
#!/usr/bin/env python3
"""
Script: check_init_py.py
Check __init__.py files for common issues
"""

import ast
import sys
from pathlib import Path


def check_init_file(filepath: Path) -> list[str]:
    """Check __init__.py for issues"""
    issues = []
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return [f"Syntax error: {e}"]
    
    # Check for docstring
    if not ast.get_docstring(tree):
        issues.append("Missing module docstring")
    
    # Check for __all__
    has_all = any(
        isinstance(node, ast.Assign) and
        any(isinstance(t, ast.Name) and t.id == '__all__' for t in node.targets)
        for node in tree.body
    )
    
    # Check for star impor
ts
    has_star_import = any(
        isinstance(node, ast.ImportFrom) and
        any(isinstance(alias, ast.alias) and alias.name == '*' for alias in node.names)
        for node in tree.body
    )
    
    if has_star_import and not has_all:
        issues.append("Star import without __all__ definition")
    
    # Check for heavy initialization
    function_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    ]
    
    if len(function_calls) > 5:
        issues.append(f"Many function calls ({len(function_calls)}) - possible heavy initialization")
    
    return issues


def main():
    """Check all __init__.py files in project"""
    project_root = Path.cwd()
    init_files = list(project_root.rglob('__init__.py'))
    
    print(f"Checking {len(init_files)} __init__.py files...\n")
    
    total_issues = 0
    for init_file in init_files:
        issues = check_init_file(init_file)
        if issues:
    
        print(f"❌ {init_file.relative_to(project_root)}")
            for issue in issues:
                print(f"   - {issue}")
            print()
            total_issues += len(issues)
    
    if total_issues == 0:
        print("✅ All __init__.py files look good!")
    else:
        print(f"Found {total_issues} issues in {len(init_files)} files")
        sys.exit(1)


if __name__ == '__main__':
    main()
```

---

## 9. القواعد الذهبية / Golden Rules

### 🥇 Rule 1: Keep It Simple
**أبسط __init__.py هو الأفضل**
- لا تضع logic معقد
- لا تقم بـ initialization ثقيل
- اجعله سهل القراءة والفهم

### 🥈 Rule 2: Be Explicit
**الوضوح أفضل من الإيجاز**
- استخدم explicit imports
- حدد `__all__` بوضوح
- وثق القرارات المهمة

### 🥉 Rule 3: Think About Users
**فكر في من سيستخدم الـ package**
- اجعل الـ public API واضح
- أخفِ التفاصيل الداخلية
- وفر واجهة سهلة الاستخدام

### 🏅 Rule 4: Performance Matters
**لا تبطئ الـ import time**
- استخدم lazy imports للـ heavy modules
- تجنب الـ initializatio
lar):
  File 1: src/services/user_service.py (lines 45-62)
  File 2: src/services/admin_service.py (lines 78-95)
  
  Suggestion: Extract to common function in src/utils/auth.py

Duplication #2 (89% similar):
  File 1: src/models/user.py (lines 12-25)
  File 2: src/models/admin.py (lines 15-28)
  
  Suggestion: Create base model in src/models/base.py
```

**الخيارات:**
```bash
# تحديد حد التشابه
python tools/detect_code_duplication.py . --threshold 0.85

# تحديد الحد الأدنى لعدد الأسطر
python tools/detect_code_duplication.py . --min-lines 10

# تجاهل ملفات معينة
python tools/detect_code_duplication.py . --ignore tests/,migrations/
```

---

### 1.3 smart_merge.py

**الوظيفة:** دمج ذكي للملفات مع حل التعارضات

**الاستخدام:**
```bash
python tools/smart_merge.py --config merge_config.json
```

**الميزات:**
- ✅ دمج تلقائي للملفات
- ✅ كشف التعارضات
- ✅ حل ذكي للتعارضات
- ✅ نسخ احتياطي تلقائي
- ✅ Rollback عند الفشل

**ملف التكوين (merge_config.json):**
```json
{
  "source": "feature_branch/"
,
  "target": "main_branch/",
  "strategy": "smart",
  "backup": true,
  "auto_resolve": true,
  "conflict_resolution": {
    "imports": "merge",
    "functions": "prefer_target",
    "classes": "prefer_source"
  }
}
```

**مثال الإخراج:**
```
=== Smart Merge Report ===

Files to merge: 15
Conflicts detected: 3
Auto-resolved: 2
Manual intervention needed: 1

✅ Merged successfully:
  - src/models/user.py
  - src/services/auth.py
  - src/utils/helpers.py

⚠️ Conflicts (auto-resolved):
  - src/config/settings.py (imports merged)
  - src/api/routes.py (functions merged)

❌ Manual intervention needed:
  - src/core/engine.py (conflicting logic)
    Please review and resolve manually
```

**الخيارات:**
```bash
# تشغيل تجريبي (dry run)
python tools/smart_merge.py --config merge_config.json --dry-run

# تجاهل النسخ الاحتياطي
python tools/smart_merge.py --config merge_config.json --no-backup

# وضع تفاعلي
python tools/smart_merge.py --config merge_config.json --interactive
```

---

### 1.4 upda
onse     # استجابة خطأ موحدة
)
```

#### core.py
**التعريفات الأساسية للنماذج:**
```python
from config.definitions import (
    BaseModel,        # نموذج أساسي
    TimestampMixin,   # created_at, updated_at
    SoftDeleteMixin,  # deleted_at, is_deleted
    AuditMixin        # created_by, updated_by
)
```

#### custom.py
**تعريفات مخصصة للمشروع:**
```python
from config.definitions import (
    ProjectStatus,    # PLANNING, IN_PROGRESS, COMPLETED
    Priority,         # LOW, MEDIUM, HIGH, CRITICAL
    TaskType          # BUG, FEATURE, ENHANCEMENT
)
```

---

## 3. Examples / الأمثلة 💡

### 3.1 simple-api/

**الوصف:** مثال كامل لـ API بسيط باستخدام FastAPI

**المحتوى:**
```
simple-api/
├── main.py              # نقطة الدخول
├── models.py            # النماذج
├── routes.py            # المسارات
├── config.py            # التكوين
└── README.md            # الدليل
```

**الاستخدام:**
```bash
cd examples/simple-api/
pip install -r requirements.txt
uvicorn main:app --reload
```

**الميزات:**


    raise AttributeError(f"module has no attribute '{name}'")
```

#### Pattern 3: Plugin System
```python
# من 03_plugin_system/__init__.py
def discover_plugins():
    # Auto-discover plugins
    pass

def get_plugin(name):
    # Get plugin by name
    pass
```

---

## 4. Scripts / السكريبتات 🔧

### 4.1 integrate.sh ⭐⭐⭐

**الوظيفة:** تثبيت Global Guidelines في مشروع قائم

**الاستخدام:**
```bash
# Remote installation
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# Local installation
./scripts/integrate.sh
```

**ما يفعله:**
1. ينشئ `.global/` directory
2. يحمل جميع الملفات من GitHub
3. يحدث `.gitignore`
4. ينشئ shortcuts
5. يجعل السكريبتات قابلة للتنفيذ

**لا يؤثر على:**
- `.git/` directory
- ملفات المشروع الموجودة
- Git history

---

### 4.2 configure.sh

**الوظيفة:** اختيار المكونات المطلوبة

**الاستخدام:**
```bash
.global/scripts/configure.sh
```

**المكونات:**
1. config/definitions
2. tools/
3. templates/
4. examples/
5. scripts/
6.
يوضح نمط معين
   - طبق النمط المناسب لحالتك

---

## 8. Integration with AI Tools / التكامل مع أدوات AI

### مع Augment:

```python
# في Augment، يمكنك:
# 1. تحميل البرومبت كـ system prompt
# 2. الإشارة للأدوات عند الحاجة
# 3. استخدام الأمثلة كـ context

# مثال:
augment.load_prompt("GLOBAL_GUIDELINES_Global System Ultimate.txt")
augment.add_tool("tools/analyze_dependencies.py")
augment.add_context("examples/simple-api/")
```

### مع GitHub Copilot:

```python
# في .github/copilot-instructions.md
# أضف:
"""
Use Global Guidelines from:
- Prompt: GLOBAL_GUIDELINES_Global System Ultimate.txt
- Tools: tools/
- Examples: examples/
- Templates: templates/
"""
```

### مع Cursor:

```json
// في .cursor/settings.json
{
  "cursor.rules": [
    "Follow GLOBAL_GUIDELINES_Global System Ultimate.txt",
    "Use tools/ for analysis",
    "Reference examples/ for patterns"
  ]
}
```

---

## 9. Troubleshooting / حل المشاكل

### Issue 1: الأدوات لا تعمل

```bash
# تأكد من Python version
python --version  # يجب أن يكون >= 3.8

# ثبت المتطلبات
pip install -r
 requirements.txt

# شغل مع verbose
python tools/analyze_dependencies.py . --verbose
```

### Issue 2: Templates لا تعمل

```bash
# تأكد من البنية
ls -la templates/config/definitions/

# تأكد من __init__.py
cat templates/config/definitions/__init__.py
```

### Issue 3: Examples لا تشتغل

```bash
# تأكد من المتطلبات
cd examples/simple-api/
pip install -r requirements.txt

# شغل مع debug
python main.py --debug
```

---

## 10. References / المراجع

### الوثائق الرئيسية:
- [GLOBAL_GUIDELINES_Global System Ultimate.txt](../GLOBAL_GUIDELINES_Global System Ultimate.txt)
- [INIT_PY_BEST_PRACTICES.md](../INIT_PY_BEST_PRACTICES.md)
- [OSF_FRAMEWORK.md](../OSF_FRAMEWORK.md)

### Workflows:
- [DEVELOPMENT_FLOW.md](../flows/DEVELOPMENT_FLOW.md)
- [INTEGRATION_FLOW.md](../flows/INTEGRATION_FLOW.md)
- [DEPLOYMENT_FLOW.md](../flows/DEPLOYMENT_FLOW.md)

### Tools Documentation:
- [tools/README.md](../tools/README.md)

### Scripts Documentation:
- [scripts/README.md](../scripts/README.md)

---

## Summary / الملخص

مستودع Global Guidelin
rst time
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
   [N] No  - First 
time deployment
   
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
   ──────
─────
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

**Loca
tion:** `.global/project_config.json`

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
│  
              │
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
Username: {ADM
IN_USERNAME}
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
   ╔═══════════════════════════════════════════
═════════════════╗
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
│  Step 
1: Welcome                                            │
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
│  - Confirm admin credentials                  
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
   db_nam
tput ~/projects/my-erp

# Short form
python3 tools/template_generator.py -t web_page_with_login -o ~/my-app
```

### Features

✅ **Interactive mode** - Asks questions for each variable  
✅ **Batch mode** - Uses default values  
✅ **Variable substitution** - Replaces placeholders  
✅ **Validation** - Checks requirements  
✅ **Post-generation** - Runs setup scripts

---

## Template Structure

Each template includes:

```
template_name/
├── README.md              # Template-specific guide
├── frontend/              # Frontend code (if applicable)
├── backend/               # Backend code (if applicable)
├── database/              # Database schemas
├── docker/                # Docker configuration
├── tests/                 # Test files
├── docs/                  # Documentation
├── .env.example           # Environment variables
├── .gitignore             # Git ignore
└── config.json            # Template configuration
```

---

## Configuration System

### config.json

Each template has
 a `config.json`:

```json
{
  "template_name": "erp_system",
  "version": "1.0.0",
  "description": "Complete ERP system",
  "variables": {
    "PROJECT_NAME": "{{PROJECT_NAME}}",
    "DATABASE_NAME": "{{DATABASE_NAME}}",
    "FRONTEND_PORT": "{{FRONTEND_PORT}}",
    "BACKEND_PORT": "{{BACKEND_PORT}}"
  },
  "defaults": {
    "PROJECT_NAME": "My ERP System",
    "DATABASE_NAME": "erp_db",
    "FRONTEND_PORT": "3000",
    "BACKEND_PORT": "5000"
  },
  "modules": [...],
  "features": {...},
  "tech_stack": {...}
}
```

### Variable Substitution

Placeholders in files are automatically replaced:

**Before:**
```python
PROJECT_NAME = "{{PROJECT_NAME}}"
DATABASE_NAME = "{{DATABASE_NAME}}"
```

**After:**
```python
PROJECT_NAME = "My ERP System"
DATABASE_NAME = "erp_db"
```

---

## Augment Integration

### When to Use Templates

Augment should suggest templates when:

1. **User starts new project**
   ```
   User: "I want to create an ERP system"
   Augment: "I can generate a complete ERP 