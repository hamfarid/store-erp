# Errors Log - Don't Make These Errors Again

> **Purpose:** Document all errors encountered and their solutions to prevent repeating the same mistakes.

**Last Updated:** [DATE]

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
```
[Full error message and stack trace]
```

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
3. [Prevention measure 3]

### Related Errors
- [Link to related error IDs]

### Lessons Learned
[Key takeaways from this error]
```

---

## Critical Errors (Must Never Repeat)

### Error 001: SQL Injection Vulnerability
Date: [DATE]
Severity: Critical
Status: Fixed
Category: Security

#### Error Message
```
SQL injection vulnerability found in user search endpoint
```

#### Context
- **What were you doing?** Implementing user search functionality
- **What was expected?** Secure parameterized query
- **What actually happened?** Used string concatenation for SQL query
- **Environment:** Development
- **Affected files:** `src/api/users.py`

#### Root Cause
Used f-strings to build SQL query instead of parameterized queries, allowing SQL injection attacks.

#### Solution
```python
# ❌ BAD - Vulnerable to SQL injection
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ✅ GOOD - Safe parameterized query
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))
```

#### Prevention
**How to avoid this in the future:**
1. Always use parameterized queries (never string concatenation)
2. Use ORM (SQLAlchemy) which handles this automatically
3. Add SQL injection tests to test suite
4. Run security scan (bandit) before committing

#### Related Errors
- Error 015: XSS vulnerability (similar security issue)

#### Lessons Learned
- Security must be the top priority (35% in OSF Framework)
- Never trust user input
- Always use parameterized queries or ORM
- Security testing is mandatory

---

## High Priority Errors

### Error 002: N+1 Query Problem
Date: [DATE]
Severity: High
Status: Fixed
Category: Performance

#### Error Message
```
Page load time > 5 seconds due to N+1 queries
```

#### Context
- **What were you doing?** Loading list of users with their orders
- **What was expected?** Fast page load (< 200ms)
- **What actually happened?** One query per user to fetch orders
- **Environment:** Production
- **Affected files:** `src/api/users.py`

#### Root Cause
Loaded users first, then made separate query for each user's orders in a loop.

#### Solution
```python
# ❌ BAD - N+1 queries
users = User.query.all()
for user in users:
    user.orders = Order.query.filter_by(user_id=user.id).all()

# ✅ GOOD - Single query with join
users = User.query.options(
    joinedload(User.orders)
).all()
```

#### Prevention
**How to avoid this in the future:**
1. Always use eager loading (joinedload) for relationships
2. Run EXPLAIN ANALYZE on all queries
3. Monitor query count in development
4. Add performance tests to catch this early

#### Related Errors
- Error 008: Missing database index

#### Lessons Learned
- Always think about query performance
- Use ORM features like joinedload
- Test with realistic data volumes
- Monitor query count, not just time

---

### Error 003: Missing Foreign Key Constraint
Date: [DATE]
Severity: High
Status: Fixed
Category: Database

#### Error Message
```
Orphaned records found in orders table
```

#### Context
- **What were you doing?** Deleting users
- **What was expected?** Orders should be deleted or prevented
- **What actually happened?** Orders remained with invalid user_id
- **Environment:** Staging
- **Affected files:** `migrations/001_create_orders.py`

#### Root Cause
Foreign key constraint not defined, allowing orphaned records.

#### Solution
```sql
-- ❌ BAD - No foreign key
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER
);

-- ✅ GOOD - With foreign key and cascade
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### Prevention
**How to avoid this in the future:**
1. Always define foreign keys for relationships
2. Choose appropriate ON DELETE action (CASCADE, SET NULL, RESTRICT)
3. Document foreign keys in docs/DB_Schema.md
4. Add database integrity tests

#### Related Errors
- Error 012: Missing unique constraint

#### Lessons Learned
- Database integrity is critical (part of Correctness - 20% in OSF)
- Always define foreign keys
- Test data integrity scenarios
- Document all constraints

---

## Medium Priority Errors

### Error 004: Missing Environment Variable
Date: [DATE]
Severity: Medium
Status: Fixed
Category: Backend

#### Error Message
```
KeyError: 'DATABASE_URL'
```

#### Context
- **What were you doing?** Deploying to production
- **What was expected?** Application starts successfully
- **What actually happened?** Crash due to missing environment variable
- **Environment:** Production
- **Affected files:** `src/config.py`

#### Root Cause
Environment variable not set in production environment.

#### Solution
```python
# ❌ BAD - No default or validation
DATABASE_URL = os.environ['DATABASE_URL']

# ✅ GOOD - With default and validation
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")
```

#### Prevention
**How to avoid this in the future:**
1. Document all required environment variables in README
2. Use .env.example file with all variables
3. Validate environment variables at startup
4. Add deployment checklist

#### Related Errors
- Error 009: Missing API key

#### Lessons Learned
- Always validate environment variables at startup
- Document all required variables
- Use .env.example as template
- Fail fast with clear error messages

---

### Error 005: CORS Not Configured
Date: [DATE]
Severity: Medium
Status: Fixed
Category: API

#### Error Message
```
Access to fetch at 'http://api.example.com' from origin 'http://frontend.example.com' 
has been blocked by CORS policy
```

#### Context
- **What were you doing?** Connecting frontend to backend
- **What was expected?** Frontend can call API
- **What actually happened?** CORS error blocked requests
- **Environment:** Development
- **Affected files:** `src/app.py`

#### Root Cause
CORS not configured in Flask application.

#### Solution
```python
# ❌ BAD - No CORS
app = Flask(__name__)

# ✅ GOOD - CORS configured
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://frontend.example.com"])
```

#### Prevention
**How to avoid this in the future:**
1. Configure CORS early in development
2. Use environment-specific origins
3. Don't use CORS(app, origins="*") in production
4. Document CORS configuration

#### Related Errors
- Error 018: CSP headers not set

#### Lessons Learned
- CORS is required for frontend-backend separation
- Configure early to avoid surprises
- Use specific origins, not wildcards
- Test cross-origin requests

---

## Low Priority Errors

### Error 006: Missing Docstring
Date: [DATE]
Severity: Low
Status: Fixed
Category: Documentation

#### Error Message
```
pylint: Missing function docstring
```

#### Context
- **What were you doing?** Running code quality checks
- **What was expected?** All functions documented
- **What actually happened?** Many functions missing docstrings
- **Environment:** Development
- **Affected files:** Multiple files

#### Root Cause
Forgot to add docstrings while writing code.

#### Solution
```python
# ❌ BAD - No docstring
def calculate_total(items):
    return sum(item.price for item in items)

# ✅ GOOD - With docstring
def calculate_total(items):
    """
    Calculate the total price of all items.
    
    Args:
        items (list): List of Item objects with price attribute
        
    Returns:
        float: Total price of all items
        
    Example:
        >>> items = [Item(price=10), Item(price=20)]
        >>> calculate_total(items)
        30.0
    """
    return sum(item.price for item in items)
```

#### Prevention
**How to avoid this in the future:**
1. Write docstring immediately after function signature
2. Use IDE templates for docstrings
3. Run pylint before committing
4. Add docstring check to CI/CD

#### Related Errors
- Error 020: Missing type hints

#### Lessons Learned
- Documentation is part of Maintainability (10% in OSF)
- Write docstrings as you code, not later
- Use consistent docstring format (Google style)
- Automate checks with linters

---

## Common Error Patterns

### Pattern 1: Security Vulnerabilities
**Common Causes:**
- Not validating user input
- Using string concatenation for SQL
- Not escaping output
- Exposing secrets in code

**Prevention:**
- Always validate and sanitize input
- Use parameterized queries
- Escape output
- Use environment variables for secrets
- Run security scans (bandit)

### Pattern 2: Performance Issues
**Common Causes:**
- N+1 queries
- Missing indexes
- No caching
- Inefficient algorithms

**Prevention:**
- Use eager loading
- Add indexes on foreign keys
- Implement caching
- Profile and optimize
- Run EXPLAIN ANALYZE

### Pattern 3: Data Integrity Issues
**Common Causes:**
- Missing foreign keys
- Missing constraints
- No validation
- Race conditions

**Prevention:**
- Define all foreign keys
- Add constraints (UNIQUE, NOT NULL, CHECK)
- Validate at multiple levels
- Use transactions
- Test data integrity

### Pattern 4: Configuration Issues
**Common Causes:**
- Missing environment variables
- Hardcoded values
- Wrong environment
- Missing dependencies

**Prevention:**
- Document all variables
- Use .env.example
- Validate at startup
- Use dependency management
- Deployment checklist

---

## Statistics

**Total Errors:** [COUNT]
**Critical:** [COUNT]
**High:** [COUNT]
**Medium:** [COUNT]
**Low:** [COUNT]

**Status:**
**Fixed:** [COUNT]
**Investigating:** [COUNT]
**Workaround:** [COUNT]
**Won't Fix:** [COUNT]

**Categories:**
**Security:** [COUNT]
**Performance:** [COUNT]
**Database:** [COUNT]
**API:** [COUNT]
**Frontend:** [COUNT]
**Backend:** [COUNT]
**Other:** [COUNT]

---

## Review Schedule

- **Daily:** Review new errors
- **Weekly:** Update solutions and prevention
- **Monthly:** Analyze patterns and trends
- **Quarterly:** Clean up resolved errors (move to archive)

---

## Notes

- This log is append-only for active errors
- Archive old errors to `Errors_Log_Archive.md` quarterly
- Always update status when error is fixed
- Share learnings with team
- Use error IDs in commit messages when fixing

