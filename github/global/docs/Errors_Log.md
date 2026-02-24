# Errors Log - Don't Make These Errors Again

> **Purpose:** Document all errors encountered and their solutions to prevent repeating the same mistakes.

**Last Updated:** 2025-01-16
**Project:** Store Management System

---

## How to Use This File

1. **When you encounter an error:** Add it immediately to this log
2. **Before implementing:** Check this log to avoid known issues
3. **When fixing:** Update the error entry with the solution
4. **Regularly:** Review and learn from past errors

---

## Error Template

```markdown
## Error [ID]: [Short Title]
Date: YYYY-MM-DD
Severity: [Critical|High|Medium|Low]
Status: [Investigating|Fixed|Workaround|Won't Fix]
Category: [Database|API|Frontend|Backend|Security|Performance|Other]

### Error Message
[Full error message and stack trace]

### Context
- **What were you doing?** [Description]
- **What was expected?** [Expected behavior]
- **What actually happened?** [Actual behavior]
- **Environment:** [Development|Staging|Production]
- **Affected files:** [List of files]

### Root Cause
[Detailed explanation of why this error occurred]

### Solution
[Step-by-step solution that fixed the error]

### Prevention
**How to avoid this in the future:**
1. [Prevention measure 1]
2. [Prevention measure 2]

### Lessons Learned
[Key takeaways from this error]
```

---

## Critical Errors (Must Never Repeat)

### Error 001: Import Path Issues
Date: 2025-10-24
Severity: High
Status: Fixed
Category: Backend

#### Error Message
```
ModuleNotFoundError: No module named 'src.models'
```

#### Context
- **What were you doing?** Importing models in routes
- **What was expected?** Models to be found
- **What actually happened?** Import error due to wrong path
- **Environment:** Development
- **Affected files:** `backend/src/routes/*.py`

#### Root Cause
Using relative imports instead of absolute paths, and missing `__init__.py` files.

#### Solution
1. Added `__init__.py` to all packages
2. Used absolute imports from `backend.src`
3. Added `backend` to PYTHONPATH

#### Prevention
1. Always use absolute imports
2. Ensure `__init__.py` exists in all packages
3. Test imports before committing

#### Lessons Learned
- Python's import system requires proper package structure
- Always verify imports work before committing

---

### Error 002: CORS Configuration Missing
Date: 2025-10-25
Severity: High
Status: Fixed
Category: API

#### Error Message
```
Access to fetch at 'http://localhost:6001' from origin 'http://localhost:6501' 
has been blocked by CORS policy
```

#### Context
- **What were you doing?** Frontend calling backend API
- **What was expected?** API call to succeed
- **What actually happened?** CORS error blocked request
- **Environment:** Development
- **Affected files:** `backend/app.py`

#### Root Cause
Flask-CORS not configured with correct origins.

#### Solution
```python
CORS(app, origins=["http://localhost:6501", "http://localhost:5173"])
```

#### Prevention
1. Configure CORS early in development
2. Test cross-origin requests immediately
3. Use environment variables for origins

#### Lessons Learned
- CORS must be configured for frontend-backend separation
- Test API calls from frontend early

---

### Error 003: Database Migration Conflicts
Date: 2025-11-01
Severity: Medium
Status: Fixed
Category: Database

#### Error Message
```
alembic.util.exc.CommandError: Target database is not up to date.
```

#### Context
- **What were you doing?** Running migrations
- **What was expected?** Migration to apply
- **What actually happened?** Conflict with existing migrations
- **Environment:** Development
- **Affected files:** `backend/migrations/`

#### Root Cause
Multiple developers creating migrations simultaneously, causing branch conflicts.

#### Solution
1. Rolled back to common ancestor
2. Merged migrations manually
3. Created new migration from merged state

#### Prevention
1. Communicate before creating migrations
2. Use `alembic stamp` for manual fixes
3. Always pull latest before creating migrations

#### Lessons Learned
- Coordinate database changes with team
- Test migrations on clean database

---

## Common Error Patterns

### Pattern 1: Security Vulnerabilities
**Common Causes:**
- Not validating user input
- Using string concatenation for SQL
- Exposing secrets in code

**Prevention:**
- Always validate and sanitize input
- Use parameterized queries (SQLAlchemy ORM)
- Use environment variables for secrets

### Pattern 2: Performance Issues
**Common Causes:**
- N+1 queries
- Missing indexes
- No caching

**Prevention:**
- Use eager loading (joinedload)
- Add indexes on foreign keys
- Implement caching with Redis

### Pattern 3: Frontend-Backend Mismatch
**Common Causes:**
- API contract changes
- Different data formats
- Missing error handling

**Prevention:**
- Document API contracts
- Use TypeScript or validation schemas
- Handle all error states

---

## Statistics

**Total Errors:** 3
**Critical:** 0
**High:** 2
**Medium:** 1
**Low:** 0

**Status:**
**Fixed:** 3
**Investigating:** 0
**Workaround:** 0
**Won't Fix:** 0

---

## Review Schedule

- **Daily:** Review new errors
- **Weekly:** Update solutions and prevention
- **Monthly:** Analyze patterns and trends
- **Quarterly:** Archive resolved errors

---

## Notes

- This log is append-only for active errors
- Always update status when error is fixed
- Use error IDs in commit messages when fixing (e.g., "fix(ERR-001): resolve import paths")

