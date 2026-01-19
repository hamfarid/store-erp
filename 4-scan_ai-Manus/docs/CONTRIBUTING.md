# Contributing to Gaara Scan AI

Thank you for your interest in contributing to Gaara Scan AI! This document provides guidelines and instructions for contributing.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Testing Requirements](#testing-requirements)
8. [Documentation](#documentation)

---

## Code of Conduct

### Our Pledge

We are committed to providing a friendly, safe, and welcoming environment for all contributors.

### Expected Behavior

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL 14+ (or SQLite for development)
- Docker & Docker Compose (optional)
- Git

### Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/gaara_scan_ai.git
cd gaara_scan_ai

# Add upstream remote
git remote add upstream https://github.com/original/gaara_scan_ai.git
```

---

## Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Copy environment file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start development server
python src/main.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

---

## Coding Standards

### Python (Backend)

Follow PEP 8 with these additional rules:

```python
# Use type hints
def calculate_score(value: int, multiplier: float = 1.0) -> float:
    """Calculate the weighted score.
    
    Args:
        value: The base value to calculate
        multiplier: Optional multiplier (default: 1.0)
    
    Returns:
        The calculated score as a float
    """
    return value * multiplier

# Use dataclasses for data containers
from dataclasses import dataclass

@dataclass
class UserData:
    name: str
    email: str
    role: str = "user"
```

### JavaScript/React (Frontend)

Follow ESLint configuration:

```javascript
// Use functional components with hooks
import React, { useState, useEffect } from 'react';

export function UserList({ initialUsers }) {
  const [users, setUsers] = useState(initialUsers);
  
  useEffect(() => {
    // Effect logic here
  }, []);
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Code Quality Tools

```bash
# Backend
black src/           # Format code
flake8 src/          # Check style
mypy src/            # Check types
isort src/           # Sort imports

# Frontend
npm run lint         # Check style
npm run format       # Format code
```

---

## Commit Guidelines

### Conventional Commits

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting) |
| `refactor` | Code refactoring |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| `perf` | Performance improvements |
| `security` | Security fixes |

### Examples

```bash
git commit -m "feat(auth): add MFA support with TOTP"
git commit -m "fix(diagnosis): resolve image upload timeout issue"
git commit -m "docs(api): update endpoint documentation"
git commit -m "test(security): add CSRF protection tests"
```

---

## Pull Request Process

### Before Submitting

1. **Update from upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   ```bash
   # Backend
   cd backend && pytest
   
   # Frontend
   cd frontend && npm test
   ```

3. **Update documentation** if needed

4. **Check linting**
   ```bash
   # Backend
   flake8 src/
   
   # Frontend
   npm run lint
   ```

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### Review Process

1. Submit PR with clear description
2. Wait for CI checks to pass
3. Address reviewer feedback
4. Squash commits if requested
5. Merge after approval

---

## Testing Requirements

### Minimum Coverage

| Category | Required Coverage |
|----------|------------------|
| Unit Tests | 80% |
| Integration Tests | 70% |
| E2E Tests | 60% |

### Writing Tests

```python
# Backend test example
import pytest
from src.utils.security import sanitize_html

class TestSecurity:
    """Security utility tests."""
    
    def test_sanitize_html_removes_script(self):
        """Test that script tags are removed."""
        input_html = '<script>alert("xss")</script>'
        result = sanitize_html(input_html)
        assert '<script>' not in result
    
    @pytest.mark.parametrize("input,expected", [
        ("<b>bold</b>", "<b>bold</b>"),
        ("<script>bad</script>", ""),
    ])
    def test_sanitize_html_parametrized(self, input, expected):
        """Test sanitization with multiple inputs."""
        assert sanitize_html(input) == expected
```

```javascript
// Frontend test example
import { render, screen } from '@testing-library/react';
import { UserList } from './UserList';

describe('UserList', () => {
  it('renders users correctly', () => {
    const users = [{ id: 1, name: 'John' }];
    render(<UserList initialUsers={users} />);
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});
```

---

## Documentation

### Required Documentation

When adding new features, update:

1. **API Documentation** - `docs/API_DOCUMENTATION.md`
2. **Architecture** - `docs/ARCHITECTURE.md` (if structural changes)
3. **README** - `README.md` (if user-facing changes)
4. **Inline Documentation** - Docstrings for all public functions

### Documentation Style

```python
def process_diagnosis(image_path: str, model: str = "default") -> DiagnosisResult:
    """Process an image for plant disease diagnosis.
    
    This function takes an image path, loads it, and runs it through
    the specified AI model for disease detection.
    
    Args:
        image_path: Path to the image file to analyze
        model: Name of the AI model to use (default: "default")
    
    Returns:
        DiagnosisResult object containing:
            - disease_name: Detected disease name
            - confidence: Confidence score (0-1)
            - recommendations: List of treatment recommendations
    
    Raises:
        FileNotFoundError: If image_path doesn't exist
        ModelNotFoundError: If specified model isn't available
        ProcessingError: If image processing fails
    
    Example:
        >>> result = process_diagnosis("/path/to/image.jpg")
        >>> print(f"Disease: {result.disease_name}")
        Disease: Tomato Late Blight
    """
```

---

## Questions?

- Open an issue for bugs or feature requests
- Join our Discord community (if available)
- Email: support@gaara-ai.com

Thank you for contributing! 🌱

