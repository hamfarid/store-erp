# SECURITY RULES (P0 - Zero Tolerance)

**FILE**: github/global/rules/security_rules.md | **PURPOSE**: Security rules | **OWNER**: Security | **LAST-AUDITED**: 2025-11-18

## Overview

These are **zero-tolerance** security rules. Any violation must be fixed immediately before proceeding.

## 1. No Hardcoded Secrets

### Rule
Never hardcode secrets, API keys, passwords, or tokens in source code.

### ❌ Bad
```python
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"
SECRET_KEY = "my-secret-key-123"
```

```typescript
const apiKey = "sk-1234567890abcdef";
const dbPassword = "password123";
```

### ✅ Good
```python
import os

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

```typescript
const apiKey = process.env.VITE_API_KEY;
if (!apiKey) {
  throw new Error("VITE_API_KEY environment variable not set");
}
```

### Enforcement
- Use environment variables
- Use KMS/Vault for production
- Never commit `.env` files
- Use `.env.example` for templates

## 2. No SQL Injection

### Rule
Always use parameterized queries. Never concatenate user input into SQL.

### ❌ Bad
```python
# NEVER DO THIS
query = f"SELECT * FROM users WHERE email = '{email}'"
db.execute(query)

query = "SELECT * FROM users WHERE id = " + user_id
db.execute(query)
```

### ✅ Good
```python
# Parameterized query
query = "SELECT * FROM users WHERE email = :email"
db.execute(query, {"email": email})

# ORM (SQLAlchemy)
user = db.query(User).filter(User.email == email).first()
```

```typescript
// Parameterized query (Prisma)
const user = await prisma.user.findUnique({
  where: { email: email }
});

// Never do this
const query = `SELECT * FROM users WHERE email = '${email}'`;
```

### Enforcement
- Use ORMs (SQLAlchemy, Prisma, TypeORM)
- Use parameterized queries
- Never use string concatenation for SQL
- Run SQL injection scanners

## 3. No XSS (Cross-Site Scripting)

### Rule
Always sanitize user input before rendering in HTML.

### ❌ Bad
```typescript
// NEVER DO THIS
element.innerHTML = userInput;
document.write(userInput);
```

```python
# NEVER DO THIS
return f"<div>{user_input}</div>"
```

### ✅ Good
```typescript
import DOMPurify from 'dompurify';

// Sanitize before rendering
element.innerHTML = DOMPurify.sanitize(userInput);

// Or use framework's built-in escaping
// React automatically escapes
<div>{userInput}</div>
```

```python
from markupsafe import escape

# Escape user input
return f"<div>{escape(user_input)}</div>"

# Or use template engine (Jinja2)
return render_template("page.html", user_input=user_input)
```

### Enforcement
- Use DOMPurify for HTML sanitization
- Use framework's built-in escaping
- Set Content-Security-Policy headers
- Never use `dangerouslySetInnerHTML` without sanitization

## 4. Proper Authentication

### Rule
All protected routes must require authentication.

### ❌ Bad
```python
@router.get("/api/users")
async def get_users():
    # No authentication check!
    return db.query(User).all()
```

### ✅ Good
```python
from middleware.auth import verify_token

@router.get("/api/users")
async def get_users(user = Depends(verify_token)):
    # Only authenticated users can access
    return db.query(User).all()
```

```typescript
// Express middleware
app.get('/api/users', authenticateToken, (req, res) => {
  // Only authenticated users can access
});
```

### Enforcement
- Use authentication middleware
- Verify JWT tokens
- Check token expiration
- Implement token refresh

## 5. Proper Authorization (RBAC)

### Rule
Check user permissions before allowing actions.

### ❌ Bad
```python
@router.delete("/api/users/{id}")
async def delete_user(id: str, user = Depends(verify_token)):
    # No permission check!
    db.query(User).filter(User.id == id).delete()
```

### ✅ Good
```python
@router.delete("/api/users/{id}")
async def delete_user(id: str, user = Depends(verify_token)):
    # Check if user is admin
    if user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Forbidden")
    
    db.query(User).filter(User.id == id).delete()
```

### Enforcement
- Implement RBAC
- Check permissions at route level
- Check permissions at service level
- Log all permission checks

## 6. Password Security

### Rule
Hash passwords with bcrypt or argon2. Never store plain text.

### ❌ Bad
```python
# NEVER DO THIS
user.password = password  # Plain text!
```

### ✅ Good
```python
import bcrypt

# Hash password
salt = bcrypt.gensalt()
user.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

# Verify password
is_valid = bcrypt.checkpw(password.encode('utf-8'), user.password_hash)
```

### Enforcement
- Use bcrypt (cost factor ≥12) or argon2
- Never store plain text passwords
- Enforce password policy (min 12 chars, complexity)
- Implement password reset flow

## 7. HTTPS Only

### Rule
Always use HTTPS in production. Redirect HTTP to HTTPS.

### ✅ Good
```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### Enforcement
- Configure HTTPS in production
- Redirect HTTP to HTTPS
- Set HSTS header
- Use secure cookies

## 8. Security Headers

### Rule
Set all security headers.

### ✅ Good
```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

### Enforcement
- Set all security headers
- Use CSP with nonces
- Enable HSTS
- Disable X-Powered-By

## 9. Input Validation

### Rule
Validate all user input against a schema.

### ❌ Bad
```python
@router.post("/api/users")
async def create_user(data: dict):
    # No validation!
    user = User(**data)
    db.add(user)
```

### ✅ Good
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

@router.post("/api/users")
async def create_user(data: UserCreate):
    # Validated by Pydantic
    user = User(**data.dict())
    db.add(user)
```

### Enforcement
- Use Pydantic (Python) or Zod (TypeScript)
- Validate all inputs
- Sanitize all outputs
- Reject invalid data

## 10. Rate Limiting

### Rule
Implement rate limiting to prevent abuse.

### ✅ Good
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/users")
@limiter.limit("100/minute")
async def get_users():
    pass
```

### Enforcement
- Implement rate limiting
- Use per-user and per-IP limits
- Return 429 Too Many Requests
- Log rate limit violations

## Automated Checks

Run these tools in CI:

```bash
# Python
bandit -r backend/
safety check

# JavaScript/TypeScript
npm audit
snyk test

# Secrets scanning
trufflehog --regex --entropy=False .
```

---

**Remember**: Security is the #1 priority (35% in OSF Framework). Never compromise on security.

