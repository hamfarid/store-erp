# Examples

**FILE**: github/global/examples/README.md | **PURPOSE**: Examples documentation | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

The `examples/` directory contains self-contained, working examples of best practices.

## Purpose

This directory provides **reference implementations** that demonstrate:
- Best practices
- Correct patterns
- Complete workflows
- Production-ready code

## Structure

```
examples/
├── authentication/
│   ├── jwt_auth_example.py
│   ├── oauth_example.py
│   └── README.md
├── api_design/
│   ├── rest_api_example.py
│   ├── graphql_example.py
│   └── README.md
├── frontend/
│   ├── react_component_example.tsx
│   ├── state_management_example.tsx
│   └── README.md
├── testing/
│   ├── unit_test_example.py
│   ├── integration_test_example.py
│   └── README.md
└── database/
    ├── migration_example.py
    ├── query_optimization_example.py
    └── README.md
```

## Example Format

Each example should:
1. Be **self-contained** (can run independently)
2. Include **comments** explaining key concepts
3. Follow **all best practices**
4. Be **production-ready** (not just a demo)
5. Include a **README.md** with:
   - Purpose
   - How to run
   - What it demonstrates
   - Key takeaways

## Example Template

```python
# FILE: examples/[category]/[name].py | PURPOSE: [Description] | OWNER: System | LAST-AUDITED: [Date]

"""
[Name] Example

This example demonstrates:
- [Key concept 1]
- [Key concept 2]
- [Key concept 3]

How to run:
    python [name].py

Expected output:
    [Description of output]
"""

# Imports
import os
from typing import Optional

# Example code with detailed comments
def example_function(param: str) -> Optional[str]:
    """
    Example function demonstrating best practices.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param is invalid
    """
    # Validate input
    if not param:
        raise ValueError("param cannot be empty")
    
    # Process
    result = param.upper()
    
    # Return
    return result

# Main execution
if __name__ == "__main__":
    # Example usage
    try:
        result = example_function("hello")
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")
```

## Categories

### Authentication
- JWT authentication
- OAuth 2.0 flow
- MFA implementation
- Session management

### API Design
- RESTful API
- GraphQL API
- gRPC service
- WebSocket server

### Frontend
- React component patterns
- State management (Zustand, Redux)
- Form handling
- API integration

### Testing
- Unit tests
- Integration tests
- E2E tests
- Mocking strategies

### Database
- Schema design
- Migrations
- Query optimization
- Transactions

### Security
- Input validation
- Output sanitization
- CSRF protection
- Rate limiting

### DevOps
- Docker setup
- CI/CD pipeline
- Monitoring
- Logging

## Usage

When implementing a feature:
1. Check if an example exists
2. Use it as a reference
3. Adapt to your specific needs
4. Follow the same patterns

## Contributing

When adding a new example:
1. Ensure it's self-contained
2. Add comprehensive comments
3. Include a README.md
4. Test that it works
5. Follow the template

---

**This directory should never be empty. Populate it with working examples.**

