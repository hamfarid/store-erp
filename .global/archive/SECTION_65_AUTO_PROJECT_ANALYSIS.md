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

