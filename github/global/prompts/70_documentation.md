# PROMPT 70: LIVING DOCUMENTATION (v29.0)

## 1. The "Atomic Update" Rule
**Rule:** Documentation is NOT a separate phase. It happens **atomically** with code changes.
*   **If you change a function signature:** Update the docstring IMMEDIATELY.
*   **If you change an API endpoint:** Update `global/docs/Routes_BE.md` IMMEDIATELY.
*   **If you change the DB schema:** Update `global/docs/DATABASE_SCHEMA.md` IMMEDIATELY.

## 2. The "Speckit" Integration
**Rule:** Use Speckit to verify documentation freshness.
*   **Check:** "Does the code match the docs?"
*   **Action:** If NO, fail the build (mentally) and fix the docs.

## 3. The "Why" over "What"
**Rule:** Comments should explain WHY, not WHAT.
*   ❌ `// Increment i by 1`
*   ✅ `// Increment retry counter to trigger exponential backoff`

## 4. Visual Documentation (v29.0)
**Rule:** Use Mermaid diagrams for complex logic.
*   **Flowcharts:** For business logic.
*   **Sequence Diagrams:** For API interactions.
*   **ER Diagrams:** For database relationships.

================================================================================
MODULE 70: DOCUMENTATION
================================================================================
Version: 1.0.0
Last Updated: 2025-11-07
Purpose: Code documentation, API docs, user guides, best practices
================================================================================

## OVERVIEW

Documentation is as important as code. Good documentation helps developers
understand, use, and maintain the system. This module covers all aspects of
documentation.

================================================================================
## WHY DOCUMENTATION?
================================================================================

**Benefits:**
✓ Helps onboarding new developers
✓ Reduces support burden
✓ Improves code maintainability
✓ Serves as a reference
✓ Documents decisions and rationale
✓ Facilitates collaboration
✓ Enables self-service

**When to Document:**
- While writing code (not after!)
- When making design decisions
- When fixing bugs
- When adding features
- Before code review
- Before deployment

================================================================================
## TYPES OF DOCUMENTATION
================================================================================

### 1. Code Documentation
Docstrings, comments, type hints

### 2. API Documentation
Endpoints, parameters, responses, examples

### 3. User Documentation
How to use the system, tutorials, guides

### 4. Architecture Documentation
System design, decisions, diagrams

### 5. Process Documentation
Workflows, procedures, best practices

================================================================================
## CODE DOCUMENTATION
================================================================================

### Python Docstrings
```python
def calculate_total(items: list[dict], tax_rate: float = 0.1) -> float:
    """
    Calculate the total price including tax.
    
    Args:
        items: List of items, each with 'price' and 'quantity' keys.
        tax_rate: Tax rate as a decimal (default: 0.1 for 10%).
    
    Returns:
        Total price including tax.
    
    Raises:
        ValueError: If any item is missing 'price' or 'quantity'.
        TypeError: If tax_rate is not a number.
    
    Examples:
        >>> items = [{'price': 10, 'quantity': 2}, {'price': 5, 'quantity': 3}]
        >>> calculate_total(items)
        38.5
        
        >>> calculate_total(items, tax_rate=0.2)
        42.0
    """
    if not isinstance(tax_rate, (int, float)):
        raise TypeError("tax_rate must be a number")
    
    subtotal = 0
    for item in items:
        if 'price' not in item or 'quantity' not in item:
            raise ValueError("Each item must have 'price' and 'quantity'")
        subtotal += item['price'] * item['quantity']
    
    return subtotal * (1 + tax_rate)
```

### JavaScript JSDoc
```javascript
/**
 * Calculate the total price including tax.
 * 
 * @param {Array<{price: number, quantity: number}>} items - List of items
 * @param {number} [taxRate=0.1] - Tax rate as a decimal
 * @returns {number} Total price including tax
 * @throws {Error} If any item is missing price or quantity
 * 
 * @example
 * const items = [{price: 10, quantity: 2}, {price: 5, quantity: 3}];
 * calculateTotal(items); // 38.5
 * calculateTotal(items, 0.2); // 42.0
 */
function calculateTotal(items, taxRate = 0.1) {
  let subtotal = 0;
  for (const item of items) {
    if (!item.price || !item.quantity) {
      throw new Error('Each item must have price and quantity');
    }
    subtotal += item.price * item.quantity;
  }
  return subtotal * (1 + taxRate);
}
```

### TypeScript
```typescript
/**
 * Item interface for cart calculations.
 */
interface CartItem {
  /** Item price in dollars */
  price: number;
  /** Quantity of items */
  quantity: number;
  /** Optional discount percentage (0-100) */
  discount?: number;
}

/**
 * Calculate the total price including tax.
 * 
 * @param items - List of cart items
 * @param taxRate - Tax rate as a decimal (default: 0.1)
 * @returns Total price including tax
 * @throws {Error} If any item has invalid values
 * 
 * @example
 * ```typescript
 * const items: CartItem[] = [
 *   {price: 10, quantity: 2},
 *   {price: 5, quantity: 3, discount: 10}
 * ];
 * calculateTotal(items); // 36.85
 * ```
 */
function calculateTotal(items: CartItem[], taxRate: number = 0.1): number {
  let subtotal = 0;
  for (const item of items) {
    if (item.price < 0 || item.quantity < 0) {
      throw new Error('Price and quantity must be non-negative');
    }
    let itemTotal = item.price * item.quantity;
    if (item.discount) {
      itemTotal *= (1 - item.discount / 100);
    }
    subtotal += itemTotal;
  }
  return subtotal * (1 + taxRate);
}
```

### Comments Best Practices
```python
# Good: Explain WHY, not WHAT
# We use a cache here because this calculation is expensive
# and the input data rarely changes
cache = {}

# Bad: Stating the obvious
# Increment counter by 1
counter += 1

# Good: Explain complex logic
# Binary search requires the array to be sorted.
# We sort here once instead of on every search.
items.sort()

# Good: Document edge cases
# Handle the case where the user has no posts yet
if not user.posts.exists():
    return []

# Good: Document workarounds
# HACK: The API sometimes returns null instead of an empty array.
# This is a known bug that will be fixed in v2.
posts = response.data or []
```

================================================================================
## API DOCUMENTATION
================================================================================

### OpenAPI/Swagger (Recommended)
```python
# FastAPI automatically generates OpenAPI docs
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    description="API for managing users and posts",
    version="1.0.0",
)

class User(BaseModel):
    """User model"""
    id: int
    email: str
    name: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "name": "John Doe"
            }
        }

@app.get("/users/{user_id}", response_model=User, tags=["users"])
async def get_user(user_id: int):
    """
    Get a user by ID.
    
    - **user_id**: The ID of the user to retrieve
    
    Returns the user object if found, otherwise 404.
    """
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Docs available at: http://localhost:8000/docs
```

### Manual API Documentation
```markdown
# API Documentation

## Authentication

All API requests require authentication using a Bearer token:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Endpoints

### GET /api/users

Get a list of all users.

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Items per page (default: 20)
- `search` (string, optional): Search query

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

**Errors:**
- `401 Unauthorized`: Missing or invalid token
- `500 Internal Server Error`: Server error

**Example:**
```bash
curl -H "Authorization: Bearer TOKEN" \
  "https://api.example.com/users?page=1&limit=10"
```

### POST /api/users

Create a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Errors:**
- `400 Bad Request`: Invalid input
- `409 Conflict`: Email already exists

**Example:**
```bash
curl -X POST \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"John Doe","password":"pass123"}' \
  https://api.example.com/users
```
```

================================================================================
## USER DOCUMENTATION
================================================================================

### README.md Template
```markdown
# Project Name

Brief description of what the project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Node.js 18+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/project.git
cd project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the server:
```bash
python manage.py runserver
```

## Usage

### Basic Example

```python
from myproject import Calculator

calc = Calculator()
result = calc.add(2, 3)
print(result)  # 5
```

### Advanced Example

```python
from myproject import DataProcessor

processor = DataProcessor(config={
    'batch_size': 100,
    'parallel': True
})

results = processor.process(data)
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `postgresql://localhost/mydb` |
| `SECRET_KEY` | Secret key for sessions | (required) |
| `DEBUG` | Enable debug mode | `False` |

## API Documentation

See [API.md](docs/API.md) for full API documentation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
```

### User Guide Template
```markdown
# User Guide

## Getting Started

### Creating Your First Project

1. Click "New Project" in the dashboard
2. Enter a project name
3. Select a template (optional)
4. Click "Create"

### Adding Team Members

1. Go to Project Settings
2. Click "Team"
3. Enter email addresses
4. Select roles
5. Click "Invite"

## Common Tasks

### Task 1: Uploading Files

To upload files:

1. Navigate to the Files section
2. Click "Upload"
3. Select files from your computer
4. Click "Upload"

Files will be processed automatically.

### Task 2: Generating Reports

To generate a report:

1. Go to Reports
2. Select report type
3. Choose date range
4. Click "Generate"

Reports are available in PDF and Excel formats.

## Troubleshooting

### Issue: Upload fails

**Cause:** File size too large

**Solution:** Compress the file or split into smaller files

### Issue: Report generation slow

**Cause:** Large date range

**Solution:** Use a smaller date range or schedule the report
```

================================================================================
## ARCHITECTURE DOCUMENTATION
================================================================================

### Architecture Decision Record (ADR)
```markdown
# ADR 001: Use PostgreSQL for Database

## Status
Accepted

## Context
We need to choose a database for our application. Requirements:
- ACID compliance
- Support for complex queries
- Good performance
- Reliable
- Open source

## Decision
We will use PostgreSQL.

## Consequences

### Positive
- Excellent ACID compliance
- Rich feature set (JSON, full-text search, etc.)
- Great performance
- Large community
- Free and open source

### Negative
- Slightly more complex than MySQL
- Requires more memory than SQLite
- Horizontal scaling requires additional tools

## Alternatives Considered
- MySQL: Simpler but fewer features
- MongoDB: NoSQL, not suitable for our relational data
- SQLite: Too limited for production use
```

### System Architecture
```markdown
# System Architecture

## Overview

The system follows a microservices architecture with the following components:

```
┌─────────────┐
│   Frontend  │ (React)
└──────┬──────┘
       │
       │ HTTPS
       │
┌──────▼──────┐
│   API GW    │ (Nginx)
└──────┬──────┘
       │
       ├──────────────┬──────────────┐
       │              │              │
┌──────▼──────┐ ┌────▼────┐ ┌───────▼────────┐
│  Auth API   │ │ User API│ │  Project API   │
└──────┬──────┘ └────┬────┘ └───────┬────────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
               ┌──────▼──────┐
               │  PostgreSQL │
               └─────────────┘
```

## Components

### Frontend
- Technology: React 18 + TypeScript
- Styling: Tailwind CSS
- State: Redux Toolkit
- Routing: React Router

### API Gateway
- Technology: Nginx
- Purpose: Load balancing, SSL termination, rate limiting

### Auth API
- Technology: FastAPI + Python
- Purpose: Authentication and authorization
- Database: PostgreSQL (users table)

### User API
- Technology: FastAPI + Python
- Purpose: User management
- Database: PostgreSQL (users, profiles tables)

### Project API
- Technology: FastAPI + Python
- Purpose: Project management
- Database: PostgreSQL (projects, tasks tables)

## Data Flow

1. User makes request from frontend
2. Request goes through API Gateway
3. API Gateway routes to appropriate service
4. Service processes request
5. Service queries database
6. Service returns response
7. API Gateway returns response to frontend
8. Frontend updates UI

## Security

- All communication over HTTPS
- JWT tokens for authentication
- Rate limiting on API Gateway
- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- XSS prevention (Content Security Policy)
```

================================================================================
## PROCESS DOCUMENTATION
================================================================================

### Development Workflow
```markdown
# Development Workflow

## Branching Strategy

We use Git Flow:

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Emergency fixes

## Feature Development

1. Create feature branch:
```bash
git checkout develop
git pull
git checkout -b feature/my-feature
```

2. Develop and commit:
```bash
git add .
git commit -m "feat: add my feature"
```

3. Push and create PR:
```bash
git push origin feature/my-feature
# Create PR on GitHub
```

4. Code review and merge:
- At least 1 approval required
- All tests must pass
- No merge conflicts

## Commit Messages

Follow Conventional Commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

Examples:
```
feat: add user authentication
fix: resolve login redirect issue
docs: update API documentation
```

## Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests are included
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Error handling is proper
```

================================================================================
## DOCUMENTATION TOOLS
================================================================================

### Sphinx (Python)
```bash
# Install
pip install sphinx

# Initialize
sphinx-quickstart docs

# Build
cd docs
make html

# Output in docs/_build/html/
```

### JSDoc (JavaScript)
```bash
# Install
npm install -g jsdoc

# Generate
jsdoc src/ -d docs/

# Output in docs/
```

### MkDocs (Markdown)
```bash
# Install
pip install mkdocs mkdocs-material

# Initialize
mkdocs new my-project

# Serve locally
mkdocs serve

# Build
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

================================================================================
## CHECKLIST
================================================================================

DOCUMENTATION CHECKLIST:
────────────────────────────────────────────────────────────────────────────
☐ All functions have docstrings
☐ All classes have docstrings
☐ All modules have docstrings
☐ Complex logic has comments
☐ API endpoints documented
☐ Request/response examples provided
☐ Error codes documented
☐ README is complete
☐ Installation instructions clear
☐ Usage examples provided
☐ Configuration documented
☐ Architecture documented
