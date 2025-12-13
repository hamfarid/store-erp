# Store ERP - Preferences & Settings

**Project:** Store ERP  
**Last Updated:** November 5, 2025

---

## Development Preferences

### Code Style

**Language:** Python 3.11+  
**Style Guide:** PEP 8  
**Line Length:** 88 characters (Black formatter)  
**Indentation:** 4 spaces  
**Quotes:** Double quotes for strings

### Formatting Tools

- **Black:** Code formatter
- **isort:** Import sorting
- **flake8:** Linting
- **mypy:** Type checking

### Editor Configuration

**Preferred:** VS Code  
**Extensions:**
- Python
- Pylance
- Black Formatter
- GitLens
- Augment / GitHub Copilot

---

## Workflow Preferences

### Task Execution

**Preference:** Execute tasks in sequence  
**Example:** Document branch protection first, then continue coverage improvements

**Rationale:**
- Clear focus on one task at a time
- Better quality results
- Easier to track progress

### Documentation

**Preference:** Complete documentation before moving forward  
**Coverage Target:** 80%+  
**Style:** Clear, concise, with examples

### Testing

**Preference:** Write tests alongside implementation  
**Coverage Target:** 80%+ (100% for critical paths)  
**Style:** Arrange-Act-Assert (AAA)

---

## Communication Preferences

### Updates

**Frequency:** After each significant milestone  
**Format:** Clear summary with:
- What was done
- Current status
- Next steps
- Any blockers

### Questions

**Preference:** Ask for clarification before proceeding  
**Don't assume:** Always confirm understanding

### Approval

**Preference:** Show plan before starting major work  
**Wait for approval:** Don't proceed without confirmation

---

## Quality Preferences

### Core Principle

> **"Always choose the BEST solution, not the easiest."**

### Decision Matrix

| Factor | Weight | Consideration |
|--------|--------|---------------|
| Correctness | Critical | Does it solve the problem completely? |
| Maintainability | High | Can others understand and modify it? |
| Scalability | High | Will it handle growth? |
| Performance | Medium | Is it efficient enough? |
| Simplicity | Medium | As simple as possible (but no simpler) |
| Speed of implementation | Low | Only matters if other factors are equal |

### Code Quality

**Prefer:**
- ✅ Clean, readable code
- ✅ Well-documented functions
- ✅ Meaningful variable names
- ✅ Small, focused functions
- ✅ DRY (Don't Repeat Yourself)

**Avoid:**
- ❌ Magic numbers
- ❌ Cryptic abbreviations
- ❌ God objects/functions
- ❌ Premature optimization
- ❌ Copy-paste code

---

## Architecture Preferences

### Design Patterns

**Prefer:**
- Repository Pattern for data access
- Service Layer for business logic
- Dependency Injection
- Factory Pattern for object creation

**Avoid:**
- Singletons (unless absolutely necessary)
- God classes
- Tight coupling

### Database

**Prefer:**
- Normalized schema
- Proper indexes
- Foreign key constraints
- Migrations for schema changes

**Avoid:**
- Denormalization (unless proven necessary)
- Raw SQL (use ORM)
- Schema changes without migrations

---

## Testing Preferences

### Test Structure

**Prefer:**
- Arrange-Act-Assert (AAA) pattern
- One assertion per test (when possible)
- Descriptive test names
- Test fixtures for common setup

### Test Coverage

**Targets:**
- Unit tests: 80%+
- Integration tests: 80%+
- Critical paths: 100%

**Focus:**
- Happy paths
- Error cases
- Edge cases
- Boundary conditions

---

## Documentation Preferences

### Code Documentation

**Prefer:**
- Docstrings for all functions/classes
- Type hints
- Inline comments for complex logic
- README for each module

**Format:**
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: When and why it's raised
    """
    # Implementation
```

### API Documentation

**Prefer:**
- OpenAPI/Swagger specification
- Request/response examples
- Error codes documented
- Authentication requirements clear

---

## Git Preferences

### Commit Messages

**Format:**
```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

**Example:**
```
feat(api): add user authentication endpoint

Implement JWT-based authentication for user login.
Includes token generation and validation.

Closes #123
```

### Branching

**Strategy:** Git Flow  
**Branches:**
- main: Production-ready
- develop: Integration branch
- feature/*: New features
- bugfix/*: Bug fixes
- hotfix/*: Emergency fixes

### Pull Requests

**Prefer:**
- Small, focused PRs
- Clear description
- Link to issue/ticket
- All tests passing
- Code review required

---

## Environment Preferences

### Development

**Database:** SQLite  
**Debug Mode:** Enabled  
**Hot Reload:** Enabled  
**Logging Level:** DEBUG

### Staging

**Database:** PostgreSQL  
**Debug Mode:** Disabled  
**Logging Level:** INFO  
**Similar to production:** Yes

### Production

**Database:** PostgreSQL  
**Debug Mode:** Disabled  
**Logging Level:** WARNING  
**Monitoring:** Enabled (Sentry)

---

## Tool Preferences

### AI Assistant Tools

**Location:** `C:\Users\hadym\.global\`  
**Structure:**
```
.global\
├── memory\store-erp\    # Project-specific memory
└── mcp\store-erp\       # Project-specific MCP
```

**MCP Servers:**
- Sentry (Active)
- Cloudflare (Available)
- Playwright (Available)
- Serena (Available)

### Guidelines

**Version:** GLOBAL_GUIDELINES v10.2.0  
**Modules:** AI-First (01-06)  
**Prompts:** All 21 prompts loaded

---

## Performance Preferences

### Optimization

**Approach:** Measure first, optimize later  
**Focus:** Bottlenecks identified by profiling  
**Avoid:** Premature optimization

### Caching

**Prefer:**
- Cache expensive operations
- Invalidate cache properly
- Document cache strategy

### Database Queries

**Prefer:**
- Eager loading when needed
- Lazy loading by default
- Proper indexes
- Query optimization based on EXPLAIN

---

## Security Preferences

### Authentication

**Method:** JWT tokens  
**Storage:** HTTP-only cookies  
**Expiration:** 24 hours  
**Refresh:** Refresh token mechanism

### Authorization

**Method:** Role-Based Access Control (RBAC)  
**Roles:** Admin, Manager, User  
**Principle:** Least privilege

### Data Protection

**Passwords:** bcrypt hashing  
**Sensitive Data:** Encrypted at rest  
**API Keys:** Environment variables  
**HTTPS:** Required in production

---

## Error Handling Preferences

### Approach

**Prefer:**
- Specific exceptions
- Meaningful error messages
- Proper logging
- User-friendly messages (hide technical details)

### Error Responses

**Format:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly message",
    "details": { ... }
  },
  "timestamp": "2025-11-05T12:00:00Z"
}
```

### Logging

**Levels:**
- DEBUG: Detailed information
- INFO: General information
- WARNING: Potential issues
- ERROR: Errors that need attention
- CRITICAL: System failures

---

## Monitoring Preferences

### Error Tracking

**Tool:** Sentry MCP  
**Organization:** gaara-group  
**Alerts:** Enabled for critical errors

### Performance Monitoring

**Track:**
- Response times
- Database query times
- Error rates
- Active users

### Logging

**Development:** Console  
**Production:** File + Sentry  
**Retention:** 30 days

---

## Deployment Preferences

### CI/CD

**Prefer:**
- Automated testing
- Automated deployment to staging
- Manual approval for production
- Rollback capability

### Containers

**Planned:** Docker  
**Orchestration:** Kubernetes (future)

### Monitoring

**Required:**
- Health checks
- Error tracking
- Performance monitoring
- Uptime monitoring

---

## Notes

- All preferences align with GLOBAL_GUIDELINES v10.2.0
- Core principle: "Always choose the BEST solution, not the easiest"
- Quality over speed
- Documentation is mandatory
- Testing is non-negotiable

---

**Last Updated:** November 5, 2025  
**Memory Location:** `C:\Users\hadym\.global\memory\store-erp\preferences.md`

