================================================================================
BLUEPRINT PATTERNS - Project Templates and Scaffolding
================================================================================

Version: 5.3.0
Module: 14_blueprint.txt
Purpose: Blueprint patterns for rapid project scaffolding and code generation
Status: Production Ready

================================================================================
OVERVIEW
================================================================================

Blueprint is a powerful pattern for creating reusable project templates and code
scaffolding. This module covers:

1. Blueprint Concept and Architecture
2. VS Code Blueprint Extension (johh/blueprint-templates)
3. Python Blueprint Repository (Limych/py-blueprint)
4. Best Practices for Template Creation
5. Integration with Development Workflows

================================================================================
1. BLUEPRINT CONCEPT
================================================================================

## What is a Blueprint?

A Blueprint is a **template-based code generation pattern** that allows developers
to quickly scaffold new projects, components, or modules with consistent structure
and best practices.

### Core Principles

✅ **Consistency** - Enforce project structure and coding standards
✅ **Reusability** - Create once, use many times
✅ **Maintainability** - Centralized template management
✅ **Productivity** - Reduce boilerplate code writing
✅ **Best Practices** - Embed proven patterns in templates

### Blueprint vs Traditional Templates

| Aspect | Traditional | Blueprint |
|--------|-------------|-----------|
| **Flexibility** | Static | Dynamic with variables |
| **Customization** | Manual editing | Interactive prompts |
| **Updates** | Manual | Centralized updates |
| **Complexity** | Simple | Supports complex structures |
| **Integration** | Standalone | IDE/Editor integrated |

### Use Cases

1. **Project Initialization** - Create new projects with complete structure
2. **Component Generation** - Add new features/modules consistently
3. **Boilerplate Reduction** - Eliminate repetitive code writing
4. **Team Standardization** - Ensure all team members follow same patterns
5. **Documentation** - Include documentation templates
6. **Testing** - Generate test files automatically

================================================================================
2. VS CODE BLUEPRINT EXTENSION
================================================================================

Based on: johh/blueprint-templates
Repository: https://github.com/johh/blueprint-templates

## Overview

VS Code Blueprint extension allows creating file templates with variable
substitution and interactive prompts.

## Installation

```bash
# Install Blueprint extension from VS Code Marketplace
# Extension ID: teamchilla.blueprint

# Clone template repository
git clone https://github.com/johh/blueprint-templates.git
cd blueprint-templates
```

## Configuration

Add to VS Code `settings.json`:

```json
{
  "blueprint.templatesPath": [
    "~/git/blueprint-templates/templates"
  ]
}
```

## Template Structure

### Basic Template Example

```
templates/
└── react-component/
    └── __pascalCase_name__/
        ├── __pascalCase_name__.tsx
        ├── __pascalCase_name__.module.css
        └── __pascalCase_name__.test.tsx
```

### Variable Naming Conventions

| Pattern | Example Input | Output |
|---------|---------------|--------|
| `__name__` | my component | my component |
| `__camelCase_name__` | my component | myComponent |
| `__pascalCase_name__` | my component | MyComponent |
| `__kebabCase_name__` | my component | my-component |
| `__snakeCase_name__` | my component | my_component |
| `__upperCase_name__` | my component | MY COMPONENT |
| `__lowerCase_name__` | my component | my component |

### React Component Template

**File:** `templates/react-fc/__pascalCase_name__.tsx`

```typescript
import React from 'react';
import styles from './__pascalCase_name__.module.css';

interface __pascalCase_name__Props {
  // Define props here
}

export const __pascalCase_name__: React.FC<__pascalCase_name__Props> = (props) => {
  return (
    <div className={styles.container}>
      <h1>__pascalCase_name__</h1>
    </div>
  );
};
```

**File:** `templates/react-fc/__pascalCase_name__.module.css`

```css
.container {
  padding: 20px;
}
```

**File:** `templates/react-fc/__pascalCase_name__.test.tsx`

```typescript
import { render, screen } from '@testing-library/react';
import { __pascalCase_name__ } from './__pascalCase_name__';

describe('__pascalCase_name__', () => {
  it('renders correctly', () => {
    render(<__pascalCase_name__ />);
    expect(screen.getByText('__pascalCase_name__')).toBeInTheDocument();
  });
});
```

### Three.js Object Template

**File:** `templates/three-object/__pascalCase_name__/__pascalCase_name__.ts`

```typescript
import * as THREE from 'three';
import { __pascalCase_name__Material } from './__pascalCase_name__Material';

export class __pascalCase_name__ extends THREE.Mesh {
  constructor() {
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new __pascalCase_name__Material();
    
    super(geometry, material);
    
    this.name = '__pascalCase_name__';
  }
  
  update(time: number): void {
    // Update logic here
    this.rotation.y = time * 0.001;
  }
}
```

### Usage

```bash
# In VS Code Command Palette (Ctrl+Shift+P)
> Blueprint: Create New File from Template

# Select template: react-fc
# Enter name: UserProfile
# Creates: UserProfile/UserProfile.tsx, UserProfile.module.css, UserProfile.test.tsx
```

## Advanced Features

### Multiple File Templates

Create complex structures with multiple files:

```
templates/
└── full-feature/
    ├── __kebabCase_name__/
    │   ├── components/
    │   │   └── __pascalCase_name__.tsx
    │   ├── hooks/
    │   │   └── use__pascalCase_name__.ts
    │   ├── types/
    │   │   └── __pascalCase_name__.types.ts
    │   ├── utils/
    │   │   └── __camelCase_name__Utils.ts
    │   └── index.ts
```

### Conditional Content

Use comments to include conditional sections:

```typescript
// __IF_TYPESCRIPT__
interface Props {
  name: string;
}
// __ENDIF__

export const Component = (/* __IF_TYPESCRIPT__ props: Props __ENDIF__ */) => {
  // Component logic
};
```

================================================================================
3. PYTHON BLUEPRINT REPOSITORY
================================================================================

Based on: Limych/py-blueprint
Repository: https://github.com/Limych/py-blueprint

## Overview

Py-Blueprint is a complete Python project template that developers can use as a
starting point for new projects. It includes best practices, CI/CD, testing,
and documentation setup.

## Features

✅ **Modern Python Setup** - pyproject.toml, setup.py
✅ **Testing Framework** - pytest with coverage
✅ **Code Quality** - pre-commit hooks, linters (Ruff)
✅ **CI/CD** - GitHub Actions workflows
✅ **Documentation** - README, CONTRIBUTING, LICENSE
✅ **Package Structure** - Proper Python package layout
✅ **Development Scripts** - Setup and update automation

## Quick Start

### Create New Repository from Blueprint

```bash
# Initialize your new origin repository
git init
git remote add origin https://github.com/YOUR_NEW_REPOSITORY

# Apply blueprint repository
git remote add blueprint https://github.com/Limych/py-blueprint.git
git fetch blueprint dev
git reset --hard blueprint/dev
git branch -M dev

# Push changes to origin repository
git push -u origin dev
```

### Apply Blueprint to Existing Repository

```bash
# Apply blueprint repository
git remote add blueprint https://github.com/Limych/py-blueprint.git
git fetch blueprint dev
git merge blueprint/dev --allow-unrelated-histories

# Push changes to origin repository
git push -u origin dev
```

### Update Blueprint

```bash
# Update blueprint to latest version
./scripts/update
git merge blueprint/dev
```

## Project Structure

```
py-blueprint/
├── .github/
│   ├── workflows/          # CI/CD workflows
│   └── PULL_REQUEST_TEMPLATE.md
├── blueprint_client/       # Main package
│   ├── __init__.py
│   ├── client.py          # Main client code
│   └── const.py           # Constants
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py        # pytest configuration
│   ├── const.py
│   └── test_client.py
├── scripts/
│   ├── setup              # Development setup script
│   └── update             # Blueprint update script
├── .editorconfig          # Editor configuration
├── .gitignore
├── .pre-commit-config.yaml # Pre-commit hooks
├── pyproject.toml         # Modern Python configuration
├── setup.py               # Package setup
├── requirements-dev.txt   # Development dependencies
├── requirements-test.txt  # Testing dependencies
├── CONTRIBUTING.md        # Contribution guidelines
├── LICENSE.md             # License file
└── README.md              # Project documentation
```

## Configuration Files

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "blueprint-client"
version = "1.0.0"
description = "Blueprint sample client library"
authors = [{name = "Your Name", email = "your.email@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=3.0.0",
    "ruff>=0.0.260",
    "pre-commit>=2.20.0",
]

[tool.setuptools]
packages = ["blueprint_client"]

[tool.ruff]
line-length = 88
target-version = "py38"
select = ["E", "F", "W", "C", "I"]
ignore = []

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.0.260
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
```

## Package Implementation

### Main Client Code

**File:** `blueprint_client/client.py`

```python
"""Main client implementation."""
from typing import Any, Dict, Optional
import requests
from .const import API_BASE_URL, DEFAULT_TIMEOUT

class Client:
    """Blueprint sample client."""
    
    def __init__(
        self,
        username: str,
        password: str,
        base_url: str = API_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Initialize client.
        
        Args:
            username: API username
            password: API password
            base_url: Base API URL
            timeout: Request timeout in seconds
        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.timeout = timeout
        self._session = requests.Session()
        self._session.auth = (username, password)
    
    def get_data(self) -> Dict[str, Any]:
        """Get data from API.
        
        Returns:
            API response data
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = self._session.get(
            f"{self.base_url}/data",
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
    
    def change_something(self, value: bool) -> bool:
        """Change a setting.
        
        Args:
            value: New setting value
            
        Returns:
            True if successful
            
        Raises:
            requests.HTTPError: If request fails
        """
        response = self._session.post(
            f"{self.base_url}/settings",
            json={"value": value},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return True
```

### Constants

**File:** `blueprint_client/const.py`

```python
"""Constants for blueprint client."""

API_BASE_URL = "https://api.example.com/v1"
DEFAULT_TIMEOUT = 30
USER_AGENT = "blueprint-client/1.0.0"
```

### Testing

**File:** `tests/test_client.py`

```python
"""Tests for client module."""
import pytest
from unittest.mock import Mock, patch
from blueprint_client.client import Client

@pytest.fixture
def client():
    """Create test client."""
    return Client(username="test", password="test")

def test_client_initialization(client):
    """Test client initialization."""
    assert client.username == "test"
    assert client.password == "test"

@patch("blueprint_client.client.requests.Session")
def test_get_data(mock_session, client):
    """Test get_data method."""
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}
    mock_session.return_value.get.return_value = mock_response
    
    data = client.get_data()
    
    assert data == {"key": "value"}
    mock_session.return_value.get.assert_called_once()

@patch("blueprint_client.client.requests.Session")
def test_change_something(mock_session, client):
    """Test change_something method."""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_session.return_value.post.return_value = mock_response
    
    result = client.change_something(True)
    
    assert result is True
    mock_session.return_value.post.assert_called_once()
```

## Development Scripts

### Setup Script

**File:** `scripts/setup`

```bash
#!/bin/bash
set -e

echo "Setting up development environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

echo "✅ Development environment ready!"
echo "Activate with: source venv/bin/activate"
```

### Update Script

**File:** `scripts/update`

```bash
#!/bin/bash
set -e

echo "Updating blueprint..."

# Fetch latest blueprint
git fetch blueprint dev

echo "✅ Blueprint updated!"
echo "Merge with: git merge blueprint/dev"
```

## Usage Example

```python
from blueprint_client.client import Client

# Initialize client
username = "user"
password = "pass"
client = Client(username, password)

# Get data
data = client.get_data()
print(f"Received data: {data}")

# Change setting
success = client.change_something(True)
print(f"Setting changed: {success}")
```

================================================================================
4. BEST PRACTICES FOR BLUEPRINT CREATION
================================================================================

## Template Design Principles

### 1. Keep Templates Simple

❌ **Bad:** Complex templates with too many options
```
templates/
└── mega-component/  # Too many files, too complex
    ├── 50+ files...
```

✅ **Good:** Focused templates for specific use cases
```
templates/
├── simple-component/     # Basic component
├── component-with-state/ # Component with state management
└── component-with-api/   # Component with API integration
```

### 2. Use Consistent Naming

✅ **Consistent variable naming across templates**
```typescript
// Always use same pattern
__pascalCase_name__Component.tsx
__pascalCase_name__Service.ts
__pascalCase_name__Types.ts
```

### 3. Include Documentation

✅ **Add comments and documentation in templates**
```typescript
/**
 * __pascalCase_name__ Component
 * 
 * Description: [Add component description]
 * Author: [Your Name]
 * Created: __date__
 */
export const __pascalCase_name__: React.FC = () => {
  // Implementation
};
```

### 4. Provide Examples

✅ **Include example usage in templates**
```typescript
/**
 * Example usage:
 * 
 * ```tsx
 * <__pascalCase_name__ 
 *   prop1="value1"
 *   prop2="value2"
 * />
 * ```
 */
```

### 5. Follow Project Conventions

✅ **Match existing project structure and style**
```
# Analyze existing project
src/
├── components/
│   └── Button/
│       ├── Button.tsx
│       ├── Button.module.css
│       └── Button.test.tsx

# Create matching template
templates/
└── component/
    └── __pascalCase_name__/
        ├── __pascalCase_name__.tsx
        ├── __pascalCase_name__.module.css
        └── __pascalCase_name__.test.tsx
```

## Template Organization

### Directory Structure

```
templates/
├── frontend/
│   ├── react-component/
│   ├── vue-component/
│   └── angular-component/
├── backend/
│   ├── django-app/
│   ├── fastapi-router/
│   └── flask-blueprint/
├── fullstack/
│   ├── crud-feature/
│   └── auth-module/
└── documentation/
    ├── api-doc/
    └── readme/
```

### Template Metadata

**File:** `template.json` (optional)

```json
{
  "name": "React Component",
  "description": "Create a new React functional component with TypeScript",
  "author": "Your Name",
  "version": "1.0.0",
  "tags": ["react", "typescript", "component"],
  "prompts": [
    {
      "name": "name",
      "message": "Component name:",
      "type": "input"
    },
    {
      "name": "withState",
      "message": "Include state management?",
      "type": "confirm",
      "default": false
    }
  ]
}
```

## Version Control

### Blueprint Repository Structure

```
blueprint-repo/
├── .git/
├── templates/           # Template files
├── docs/               # Documentation
│   ├── usage.md
│   └── contributing.md
├── examples/           # Example outputs
├── tests/             # Template tests
├── CHANGELOG.md       # Version history
└── README.md          # Main documentation
```

### Updating Templates

```bash
# Create feature branch
git checkout -b feature/new-template

# Add template
mkdir -p templates/new-feature
# ... create template files ...

# Commit changes
git add templates/new-feature
git commit -m "feat: add new-feature template"

# Push and create PR
git push origin feature/new-template
```

================================================================================
5. INTEGRATION WITH DEVELOPMENT WORKFLOWS
================================================================================

## CI/CD Integration

### GitHub Actions Workflow

**File:** `.github/workflows/blueprint.yml`

```yaml
name: Blueprint Templates

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test-templates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Test Template Generation
        run: |
          # Test each template
          for template in templates/*; do
            echo "Testing $template"
            # Add template testing logic
          done
      
      - name: Validate Template Structure
        run: |
          # Validate template files
          npm run validate-templates
```

## IDE Integration

### VS Code Settings

**File:** `.vscode/settings.json`

```json
{
  "blueprint.templatesPath": [
    "${workspaceFolder}/templates",
    "~/.vscode/templates"
  ],
  "blueprint.defaultAuthor": "Your Name",
  "blueprint.dateFormat": "YYYY-MM-DD"
}
```

### JetBrains IDEs

Use File Templates feature:
- Settings → Editor → File and Code Templates
- Create custom templates with variables
- Use Velocity Template Language (VTL)

## Team Collaboration

### Shared Template Repository

```bash
# Team template repository
git clone https://github.com/team/blueprints.git ~/.blueprints

# Configure in VS Code
{
  "blueprint.templatesPath": [
    "~/.blueprints/templates"
  ]
}

# Update templates
cd ~/.blueprints
git pull origin main
```

### Template Review Process

1. **Propose Template** - Create PR with new template
2. **Team Review** - Review structure and content
3. **Test Generation** - Test template with real use cases
4. **Documentation** - Update docs with usage examples
5. **Merge** - Merge to main branch
6. **Announce** - Notify team of new template

================================================================================
BLUEPRINT BEST PRACTICES SUMMARY
================================================================================

✅ **DO:**
- Keep templates simple and focused
- Use consistent naming conventions
- Include comprehensive documentation
- Provide usage examples
- Follow project conventions
- Version control templates
- Test template generation
- Update templates regularly

❌ **DON'T:**
- Create overly complex templates
- Use inconsistent naming
- Skip documentation
- Hardcode values
- Ignore project style guides
- Forget to test templates
- Leave templates outdated

================================================================================
RESOURCES
================================================================================

## VS Code Blueprint Extension
- Extension: https://marketplace.visualstudio.com/items?itemName=teamchilla.blueprint
- Templates: https://github.com/johh/blueprint-templates

## Python Blueprint
- Repository: https://github.com/Limych/py-blueprint
- Documentation: See README.md

## Related Tools
- Yeoman: https://yeoman.io/
- Cookiecutter: https://cookiecutter.readthedocs.io/
- Plop: https://plopjs.com/

================================================================================
END OF BLUEPRINT MODULE
================================================================================

