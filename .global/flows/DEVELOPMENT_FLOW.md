# Development Flow - سير عمل التطوير

## نظرة عامة / Overview

هذا المستند يحدد سير العمل الكامل لتطوير المشاريع باستخدام Global Guidelines.

This document defines the complete workflow for developing projects using Global Guidelines.

---

## المراحل الرئيسية / Main Phases

### Phase 1: Project Initialization (تهيئة المشروع)

#### 1.1 تحميل Global Guidelines

```bash
# Option A: Clone full repository (للمساهمين)
git clone https://github.com/hamfarid/global.git

# Option B: Download as standalone (للمشاريع القائمة)
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash
```

#### 1.2 تطبيق البنية الأساسية

```bash
# Navigate to project
cd /path/to/your/project

# Apply global structure
.global/scripts/apply_structure.sh
```

#### 1.3 إعداد البيئة

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### Phase 2: Development Setup (إعداد التطوير)

#### 2.1 إنشاء config/

```bash
# Create config structure
mkdir -p config/definitions
touch config/__init__.py
touch config/ports.py
touch config/definitions/{__init__.py,common.py,core.py,custom.py}
```

#### 2.2 تطبيق Templates

```bash
# Copy templates from global
cp .global/templates/config/definitions/*.py config/definitions/
cp .global/templates/config/ports.py config/
```

#### 2.3 إعداد Tools

```bash
# Create tools directory
mkdir -p tools
cp .global/tools/*.py tools/
```

---

### Phase 3: Development Workflow (سير عمل التطوير)

#### 3.1 Feature Development

```
1. Create feature branch
   └─> git checkout -b feature/feature-name

2. Develop feature
   ├─> Write code following Global Guidelines
   ├─> Use config/definitions for types
   ├─> Follow naming conventions
   └─> Add docstrings

3. Test feature
   ├─> Unit tests
   ├─> Integration tests
   └─> Manual testing

4. Code quality check
   ├─> flake8 .
   ├─> mypy .
   └─> Run tools/analyze_dependencies.py

5. Commit changes
   └─> git commit -m "feat: description"
```

#### 3.2 Code Review Process

```
1. Push branch
   └─> git push origin feature/feature-name

2. Create Pull Request
   ├─> Add description
   ├─> Link related issues
   └─> Request reviewers

3. Review checklist
   ├─> [ ] Follows Global Guidelines
   ├─> [ ] Has tests
   ├─> [ ] Documentation updated
   ├─> [ ] No code duplication
   └─> [ ] Passes quality checks

4. Address feedback
   └─> Make requested changes

5. Merge
   └─> Squash and merge to main
```

---

### Phase 4: Quality Assurance (ضمان الجودة)

#### 4.1 Automated Checks

```bash
# Run all quality checks
.global/scripts/quality_check.sh

# Individual checks
flake8 . --config=.flake8
mypy . --config-file=pyproject.toml
python tools/detect_code_duplication.py .
python tools/analyze_dependencies.py .
```

#### 4.2 Manual Review

```
Checklist:
├─> [ ] Code follows PEP 8
├─> [ ] All functions have docstrings
├─> [ ] Type hints are complete
├─> [ ] No unused imports
├─> [ ] No code duplication
├─> [ ] Config/definitions used properly
├─> [ ] Error handling is robust
└─> [ ] Performance is acceptable
```

---

### Phase 5: Documentation (التوثيق)

#### 5.1 Code Documentation

```python
# Every module must have:
"""
File: path/to/module.py
Module: package.module
Created: YYYY-MM-DD
Author: Your Name
Description: What this module does
"""

# Every class must have:
class MyClass:
    """
    Brief description
    
    Attributes:
        attr1: Description
        attr2: Description
    
    Example:
        >>> obj = MyClass()
        >>> obj.method()
    """

# Every function must have:
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When...
    """
```

#### 5.2 Project Documentation

```
docs/
├── README.md          # Project overview
├── SETUP.md           # Setup instructions
├── API.md             # API documentation
├── ARCHITECTURE.md    # Architecture overview
└── CHANGELOG.md       # Version history
```

---

### Phase 6: Testing (الاختبار)

#### 6.1 Test Structure

```
tests/
├── __init__.py
├── conftest.py        # Pytest fixtures
├── unit/              # Unit tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/       # Integration tests
│   ├── test_api.py
│   └── test_database.py
└── e2e/              # End-to-end tests
    └── test_workflows.py
```

#### 6.2 Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test
pytest tests/unit/test_models.py

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

---

### Phase 7: Deployment (النشر)

#### 7.1 Pre-deployment Checklist

```
├─> [ ] All tests pass
├─> [ ] Documentation updated
├─> [ ] CHANGELOG updated
├─> [ ] Version bumped
├─> [ ] Dependencies locked
├─> [ ] Environment variables documented
└─> [ ] Backup plan ready
```

#### 7.2 Deployment Steps

```bash
# 1. Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. Build
python -m build

# 3. Deploy (example for web app)
docker build -t myapp:v1.0.0 .
docker push myapp:v1.0.0

# 4. Update production
kubectl apply -f k8s/deployment.yaml
```

---

## Best Practices / أفضل الممارسات

### 1. Git Workflow

```
main (protected)
  ├─> develop
  │     ├─> feature/feature-1
  │     ├─> feature/feature-2
  │     └─> bugfix/bug-1
  └─> hotfix/critical-fix
```

### 2. Commit Messages

```
Format: <type>(<scope>): <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

Examples:
- feat(auth): add JWT authentication
- fix(api): resolve timeout issue
- docs(readme): update setup instructions
```

### 3. Branch Naming

```
feature/feature-name
bugfix/bug-description
hotfix/critical-issue
release/v1.0.0
```

### 4. Code Organization

```
project/
├── config/           # Configuration
├── src/             # Source code
│   ├── models/      # Data models
│   ├── services/    # Business logic
│   ├── api/         # API endpoints
│   └── utils/       # Utilities
├── tests/           # Tests
├── tools/           # Development tools
└── docs/            # Documentation
```

---

## Tools Integration / تكامل الأدوات

### 1. analyze_dependencies.py

```bash
# Analyze project dependencies
python tools/analyze_dependencies.py .

# Generate dependency graph
python tools/analyze_dependencies.py . --format graphviz > deps.dot
dot -Tpng deps.dot -o deps.png
```

### 2. detect_code_duplication.py

```bash
# Detect code duplication
python tools/detect_code_duplication.py .

# With threshold
python tools/detect_code_duplication.py . --threshold 0.9
```

### 3. smart_merge.py

```bash
# Dry run
python tools/smart_merge.py --config merge_config.json --dry-run

# Execute merge
python tools/smart_merge.py --config merge_config.json
```

### 4. update_imports.py

```bash
# Update imports
python tools/update_imports.py old_module new_module .
```

---

## Continuous Integration / التكامل المستمر

### GitHub Actions Example

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install flake8 mypy pytest
      
      - name: Quality checks
        run: |
          flake8 .
          mypy .
      
      - name: Run tests
        run: pytest --cov=.
```

---

## Troubleshooting / حل المشاكل

### Common Issues

#### Issue 1: Circular Imports

```python
# Problem
# models/user.py
from models.post import Post

# models/post.py
from models.user import User

# Solution: Use TYPE_CHECKING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.post import Post
```

#### Issue 2: Import Errors

```bash
# Check Python path
echo $PYTHONPATH

# Add project root to path
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

#### Issue 3: Dependency Conflicts

```bash
# Check dependencies
pip list

# Create clean environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Monitoring & Maintenance / المراقبة والصيانة

### 1. Regular Tasks

```
Daily:
├─> Review pull requests
├─> Check CI/CD status
└─> Monitor error logs

Weekly:
├─> Update dependencies
├─> Review code quality metrics
└─> Update documentation

Monthly:
├─> Security audit
├─> Performance review
└─> Refactoring session
```

### 2. Metrics to Track

```
Code Quality:
├─> Test coverage (target: >80%)
├─> Code duplication (target: <5%)
├─> Complexity (target: <10 per function)
└─> Technical debt (track and reduce)

Performance:
├─> Response time
├─> Error rate
├─> Resource usage
└─> Uptime
```

---

## References / المراجع

- [Global Guidelines](../GLOBAL_GUIDELINES_v3.7.txt)
- [OSF Framework](../OSF_FRAMEWORK.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Quick Start](../QUICK_START.md)

---

**Last Updated:** 2025-11-02  
**Version:** 1.0.0  
**Status:** ✅ Active

