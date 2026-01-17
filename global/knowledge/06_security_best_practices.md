# Security Best Practices

> **Priority:** Security is the #1 factor in the OSF Framework (35% weight)

**Version:** 1.0
**Last Updated:** 2025-01-16

---

## 🔐 Authentication

### Password Security
- ✅ Use Argon2 for password hashing (preferred) or bcrypt
- ✅ Minimum password length: 8 characters
- ✅ Require complexity: uppercase, lowercase, number
- ✅ Check against common passwords list
- ❌ Never store plain text passwords
- ❌ Never use MD5 or SHA1 for passwords

### JWT Implementation
```python
# Good: Short access tokens, longer refresh tokens
ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRES = timedelta(days=7)

# Good: Include minimal claims
payload = {
    'user_id': user.id,
    'role': user.role,
    'exp': expiration_time
}
```

### Account Protection
- ✅ Lock account after 5 failed login attempts
- ✅ CAPTCHA after 3 failed attempts
- ✅ Notify user of suspicious login activity
- ✅ Implement session timeout

---

## 🛡️ Input Validation

### Validate Everything
```python
# Good: Use schemas for validation
from pydantic import BaseModel, validator

class ProductCreate(BaseModel):
    name: str
    price: float
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
```

### Sanitize Output
```python
# Good: Escape HTML in output
from markupsafe import escape

def render_user_content(content):
    return escape(content)
```

---

## 🗃️ Database Security

### SQL Injection Prevention
```python
# ❌ BAD: String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ GOOD: Parameterized queries
query = "SELECT * FROM users WHERE id = :user_id"
result = db.execute(query, {'user_id': user_id})

# ✅ BEST: Use ORM
user = User.query.filter_by(id=user_id).first()
```

### Principle of Least Privilege
- ✅ Create separate database users for app, migration, admin
- ✅ Limit app user to only required operations
- ✅ Use read-only replicas for reports

---

## 🌐 API Security

### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    pass
```

### CORS Configuration
```python
# Good: Specific origins, not wildcard
CORS(app, origins=[
    "http://localhost:6501",
    "https://store.example.com"
])
```

### Security Headers
```python
# Add to all responses
response.headers['X-Content-Type-Options'] = 'nosniff'
response.headers['X-Frame-Options'] = 'DENY'
response.headers['X-XSS-Protection'] = '1; mode=block'
response.headers['Strict-Transport-Security'] = 'max-age=31536000'
```

---

## 🔑 Secret Management

### Environment Variables
```python
# Good: Load from environment
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set")
```

### .env File
```bash
# .env (Never commit!)
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
JWT_SECRET=another-secret-key
```

### .gitignore
```gitignore
# Always ignore
.env
.env.local
.env.production
*.pem
*.key
```

---

## 🚨 Error Handling

### Don't Expose Internal Errors
```python
# ❌ BAD: Exposes internal details
@app.errorhandler(Exception)
def handle_error(e):
    return str(e), 500

# ✅ GOOD: Generic message, log details
@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Internal error: {str(e)}")
    return {"error": "An internal error occurred"}, 500
```

---

## ✅ Security Checklist

### Before Deployment
- [ ] All secrets in environment variables
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection tested
- [ ] XSS tested
- [ ] CORS properly configured
- [ ] Account lockout implemented
- [ ] Error messages don't expose internals

### Regular Audits
- [ ] Dependency vulnerability scan (weekly)
- [ ] Penetration testing (quarterly)
- [ ] Code review for security (every PR)
- [ ] Access review (monthly)

---

## 🔗 Related Files

- `global/knowledge/01_osf_framework.md` - Decision framework
- `global/errors/` - Security error tracking
- `backend/src/utils/security.py` - Security utilities
