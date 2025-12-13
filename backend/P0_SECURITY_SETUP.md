# FILE: backend/P0_SECURITY_SETUP.md | PURPOSE: P0 security setup quick guide | OWNER: security | RELATED: docs/JWT_Token_Rotation.md | LAST-AUDITED: 2025-11-04

# P0 Security Setup - Quick Start Guide

## ✅ Completed Tasks

### P0.1: Argon2id Password Hashing (COMPLETE)

**What was done:**
- ✅ Migrated from bcrypt to Argon2id (OWASP 2024 recommended)
- ✅ Automatic password rehashing on login for legacy hashes
- ✅ Created `backend/src/password_hasher.py` with secure hashing
- ✅ Updated `auth.py`, `encryption_manager.py`, and `routes/user.py`
- ✅ Created migration analysis script

**Installation:**
```bash
cd backend
pip install argon2-cffi==23.1.0
```

**Verify:**
```bash
python src/password_hasher.py
# Should output: Current algorithm: argon2id
```

**Migration Analysis:**
```bash
python scripts/migrate_password_hashes.py
# Shows users with legacy hashes (bcrypt/SHA-256)
```

**How it works:**
- New passwords: Hashed with Argon2id automatically
- Existing passwords: Automatically rehashed on next successful login
- No user action required!

---

### P0.2: JWT Token Rotation (COMPLETE)

**What was done:**
- ✅ Implemented 15min access + 7d refresh tokens
- ✅ Created `backend/src/jwt_manager.py` with token rotation
- ✅ Created `backend/src/models/refresh_token.py` for token storage
- ✅ Added database migration for `refresh_tokens` table
- ✅ Updated `routes/auth_routes.py` with new endpoints
- ✅ Added token revocation support

**Installation:**
```bash
cd backend

# Install dependencies (already in requirements.txt)
pip install PyJWT==2.8.0

# Run database migration
flask db upgrade
# OR manually:
python -m flask db migrate -m "Add refresh_tokens table"
python -m flask db upgrade
```

**Environment Setup:**
```bash
# Add to .env (REQUIRED)
JWT_SECRET_KEY=<generate-strong-secret>
JWT_ACCESS_TOKEN_EXPIRES=900  # 15 minutes
JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days

# Generate strong secret:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**New API Endpoints:**

1. **Login** (updated):
```bash
POST /api/auth/login
{
  "username": "admin",
  "password": "admin123",
  "use_jwt": true
}

Response:
{
  "status": "success",
  "data": {
    "user": {...},
    "tokens": {
      "access_token": "eyJ...",
      "refresh_token": "eyJ...",
      "token_type": "Bearer",
      "expires_in": 900,
      "refresh_expires_in": 604800
    }
  }
}
```

2. **Refresh Token**:
```bash
POST /api/auth/refresh
{
  "refresh_token": "eyJ..."
}

Response:
{
  "status": "success",
  "data": {
    "access_token": "eyJ...",
    "token_type": "Bearer",
    "expires_in": 900
  }
}
```

3. **Revoke Token**:
```bash
POST /api/auth/tokens/revoke
{
  "refresh_token": "eyJ..."
}
# OR revoke all:
{
  "revoke_all": true
}
```

4. **List Active Tokens**:
```bash
GET /api/auth/tokens
Authorization: Bearer eyJ...

Response:
{
  "status": "success",
  "data": {
    "tokens": [
      {
        "jti": "...",
        "created_at": "...",
        "expires_at": "...",
        "ip_address": "...",
        "user_agent": "...",
        "is_valid": true
      }
    ],
    "count": 1
  }
}
```

**Testing:**
```bash
# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","use_jwt":true}'

# Test refresh
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<token-from-login>"}'
```

---

## 🔄 Next Steps (P0.3 - P0.12)

### P0.3: CSRF Protection
- Enable CSRF protection in production
- Implement double-submit cookie pattern
- Update frontend to handle CSRF tokens

### P0.4: HTTPS Enforcement
- Force HTTPS in production
- Add HSTS header
- Set secure cookie flags

### P0.5: Security Headers
- Add CSP with nonces
- Add X-Frame-Options, X-Content-Type-Options
- Add Referrer-Policy, Permissions-Policy

### P0.6: Secrets Management
- Migrate to KMS/Vault
- Remove hardcoded secrets
- Add secret scanning to CI

### P0.7: SQL Injection Audit
- Verify parameterized queries
- Add SQL injection tests

### P0.8: XSS Prevention
- Add input sanitization
- Implement CSP
- Add XSS tests

### P0.9: File Upload Validation
- Add file type validation
- Implement virus scanning
- Add size limits

### P0.10: Brute-Force Protection
- Enhance rate limiting
- Add account lockout
- Add CAPTCHA

### P0.11: Dependency Audit
- Run pip-audit
- Update dependencies
- Add dependabot

### P0.12: Security Audit Logging
- Create security_audit.log
- Log all security events
- Add log rotation

---

## 📚 Documentation

- **JWT Token Rotation**: `docs/JWT_Token_Rotation.md`
- **Password Hashing**: `backend/src/password_hasher.py` (docstrings)
- **Refresh Token Model**: `backend/src/models/refresh_token.py` (docstrings)

---

## 🔒 Security Checklist

### Before Production Deployment

- [ ] Generate strong JWT_SECRET_KEY (32+ bytes)
- [ ] Set JWT_SECRET_KEY in environment (NOT in code)
- [ ] Run database migration for refresh_tokens table
- [ ] Test login flow with JWT tokens
- [ ] Test token refresh flow
- [ ] Test token revocation
- [ ] Verify HTTPS is enforced
- [ ] Verify secure cookie flags are set
- [ ] Run password hash migration analysis
- [ ] Enable CSRF protection
- [ ] Add security headers
- [ ] Run dependency audit
- [ ] Enable security logging

### Environment Variables (REQUIRED)

```bash
# CRITICAL - MUST SET IN PRODUCTION
JWT_SECRET_KEY=<strong-random-secret>
SECRET_KEY=<strong-random-secret>
ENCRYPTION_KEY=<strong-random-secret>

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Optional but recommended
PASSWORD_HASH_ALGORITHM=argon2id
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=604800
```

---

## 🧪 Testing

### Unit Tests

```bash
cd backend
pytest tests/test_password_hasher.py
pytest tests/test_jwt_manager.py
pytest tests/test_refresh_token.py
```

### Integration Tests

```bash
pytest tests/test_auth_routes.py
```

### Manual Testing

See `docs/JWT_Token_Rotation.md` for detailed testing examples.

---

## 🚨 Troubleshooting

### Issue: "argon2-cffi not available"

**Solution:**
```bash
pip install argon2-cffi==23.1.0
```

### Issue: "JWT_SECRET_KEY must be set in production"

**Solution:**
```bash
# Add to .env
JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### Issue: "Table refresh_tokens does not exist"

**Solution:**
```bash
flask db upgrade
```

### Issue: "Token verification failed"

**Possible causes:**
1. JWT_SECRET_KEY mismatch between token generation and verification
2. Token expired
3. Token revoked in database
4. Invalid token format

**Debug:**
```python
from jwt_manager import JWTManager
payload = JWTManager.decode_token(token, verify=False)
print(payload)  # Check token contents
```

---

## 📊 Monitoring

### Metrics to Track

1. **Password Hashing**
   - Legacy hash count (bcrypt/SHA-256)
   - Argon2id hash count
   - Rehashing rate

2. **JWT Tokens**
   - Active refresh tokens per user
   - Token refresh rate
   - Token revocation rate
   - Failed token verifications

### Cleanup Jobs

Add to cron:
```bash
# Daily cleanup of expired tokens
0 2 * * * cd /path/to/backend && python -c "from models.refresh_token import RefreshToken, db; from main import app; app.app_context().push(); RefreshToken.cleanup_expired(); db.session.commit()"

# Weekly cleanup of old revoked tokens (30+ days)
0 3 * * 0 cd /path/to/backend && python -c "from models.refresh_token import RefreshToken, db; from main import app; app.app_context().push(); RefreshToken.cleanup_revoked(30); db.session.commit()"
```

---

## 🔗 Related Files

### Created Files (P0.1 + P0.2)

- `backend/src/password_hasher.py` - Argon2id password hashing
- `backend/scripts/migrate_password_hashes.py` - Migration analysis
- `backend/src/jwt_manager.py` - JWT token management
- `backend/src/models/refresh_token.py` - Refresh token model
- `backend/migrations/versions/create_refresh_tokens_table.py` - DB migration
- `docs/JWT_Token_Rotation.md` - Detailed documentation

### Modified Files

- `backend/requirements.txt` - Added argon2-cffi, bleach
- `backend/src/auth.py` - Updated password hashing
- `backend/src/routes/user.py` - Added auto-rehashing on login
- `backend/src/encryption_manager.py` - Updated password methods
- `backend/src/routes/auth_routes.py` - Added JWT rotation endpoints
- `global/templates/.env.example` - Added JWT config

---

## ✅ Verification

Run this checklist to verify P0.1 + P0.2 are working:

```bash
# 1. Check Argon2id is available
python -c "from password_hasher import get_algorithm; print(get_algorithm())"
# Expected: argon2id

# 2. Check JWT manager is available
python -c "from jwt_manager import JWTManager; print('JWT Manager OK')"
# Expected: JWT Manager OK

# 3. Check database migration
flask db current
# Should show: refresh_tokens_001

# 4. Test login with JWT
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","use_jwt":true}'
# Should return access_token and refresh_token

# 5. Test token refresh
# (Use refresh_token from step 4)
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<token>"}'
# Should return new access_token
```

All tests passing? ✅ P0.1 + P0.2 are complete!

