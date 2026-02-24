# Errors Log (Global System v26 Diamond 32)

> **Purpose:** Document all errors encountered and their solutions to prevent repeating the same mistakes.
> **Automation:** Sentinel reads this file to learn from past mistakes.

**Last Updated:** [DATE]

---

## How to Use This File

1. **When you encounter an error:** Add it immediately to this log.
2. **Before implementing:** Check this log to avoid known issues.
3. **Speckit Integration:** `speckit.py analyze` checks this file for recurring patterns.

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

### Prevention (Global System v26 Diamond 32)
**How to avoid this in the future:**
1. [Prevention measure 1]
2. **Sentinel Rule:** [Add a rule to sentinel.py if applicable]
3. **CodeRabbit Rule:** [Add a custom rule if applicable]

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

#### Prevention (Global System v26 Diamond 32)
**How to avoid this in the future:**
1. Always use parameterized queries (never string concatenation)
2. **Sentinel Rule:** Block commits with `f"SELECT * FROM` patterns.
3. **CodeRabbit Rule:** Enable SQL Injection check.

#### Lessons Learned
- Security must be the top priority.
- Never trust user input.
- Automation is the only way to guarantee security.
