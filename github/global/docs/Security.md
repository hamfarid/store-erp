# Security Documentation

**Store Management System - Security Guide**  
**Version:** 1.0  
**Last Updated:** 2025-12-01  
**Classification:** Internal Use Only

---

## Table of Contents

1. [Security Overview](#security-overview)
2. [Authentication](#authentication)
3. [Authorization (RBAC)](#authorization-rbac)
4. [Input Validation](#input-validation)
5. [Data Protection](#data-protection)
6. [API Security](#api-security)
7. [Infrastructure Security](#infrastructure-security)
8. [Monitoring & Logging](#monitoring--logging)
9. [Incident Response](#incident-response)
10. [Compliance](#compliance)

---

## Security Overview

### Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SECURITY LAYERS                          │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Network Security                                      │
│  ├── HTTPS (TLS 1.3)                                           │
│  ├── Rate Limiting                                             │
│  └── CORS Policy                                               │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Application Security                                  │
│  ├── JWT Authentication                                        │
│  ├── RBAC Authorization                                        │
│  ├── Input Validation                                          │
│  ├── CSRF Protection                                           │
│  └── CSP Headers                                               │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: Data Security                                         │
│  ├── Argon2id Password Hashing                                 │
│  ├── Database Encryption                                       │
│  └── Secure Session Management                                 │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: Infrastructure Security                               │
│  ├── Docker Hardening                                          │
│  ├── Non-root Containers                                       │
│  └── Read-only Filesystems                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Security Controls Summary

| Control | Status | Implementation |
|---------|--------|----------------|
| HTTPS Enforcement | ✅ | `main.py` - force_https middleware |
| JWT Authentication | ✅ | `jwt_manager.py`, `auth.py` |
| Refresh Token Rotation | ✅ | `token_blacklist.py` |
| RBAC | ✅ | `permissions.py` |
| Rate Limiting | ✅ | Flask-Limiter |
| CSRF Protection | ✅ | Flask-WTF |
| CSP with Nonces | ✅ | `csp_nonce.py` |
| Input Validation | ✅ | Marshmallow schemas |
| SQL Injection Protection | ✅ | SQLAlchemy ORM |
| XSS Protection | ✅ | Bleach sanitization |
| Password Hashing | ✅ | Argon2id |
| Account Lockout | ✅ | 5 failed attempts |

---

## Authentication

### JWT Token Flow

```
┌──────────┐     POST /api/auth/login      ┌──────────┐
│  Client  │ ──────────────────────────────▶│  Server  │
└──────────┘     {username, password}       └──────────┘
                                                  │
                                                  ▼
                                           ┌──────────────┐
                                           │ Validate     │
                                           │ Credentials  │
                                           └──────────────┘
                                                  │
                                                  ▼
┌──────────┐     {access_token,             ┌──────────────┐
│  Client  │ ◀──────────────────────────────│ Generate     │
└──────────┘      refresh_token}            │ Tokens       │
     │                                      └──────────────┘
     │
     ▼
┌──────────────────────────────────────────────────────────┐
│  Access Token (15 min)     │    Refresh Token (7 days)   │
│  - Used for API requests   │    - Used to get new access │
│  - Short-lived             │    - Rotated on use         │
│  - Contains user_id, role  │    - Blacklisted on logout  │
└──────────────────────────────────────────────────────────┘
```

### Token Configuration

```python
# JWT Settings (auth.py)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
JWT_ALGORITHM = 'HS256'
```

### Token Refresh Flow

1. Client sends refresh token to `/api/auth/refresh`
2. Server validates refresh token
3. Old refresh token is blacklisted
4. New access + refresh tokens issued
5. Client stores new tokens

### Account Lockout

- **Threshold:** 5 failed login attempts
- **Lockout Duration:** 30 minutes
- **Reset:** Automatic after duration or manual admin reset

```python
# User model (user.py)
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=30)
```

---

## Authorization (RBAC)

### Role Hierarchy

```
admin (Full Access)
├── inventory_manager
│   ├── Inventory CRUD
│   ├── Product CRUD
│   └── Warehouse CRUD
├── sales_person
│   ├── Sales Create/Edit
│   ├── Customer Create/Edit
│   └── View Products
├── purchasing_agent
│   ├── Purchase Create/Edit
│   ├── Supplier Create/Edit
│   └── View Products
├── accountant
│   ├── View All
│   └── Reports Export
└── user
    └── Dashboard View Only
```

### Permission Categories

| Category | Permissions |
|----------|-------------|
| System | `admin_full`, `system_settings_*` |
| Users | `user_management_view/add/edit/delete` |
| Inventory | `inventory_view/add/edit/delete/stock_adjust` |
| Products | `products_view/add/edit/delete` |
| Sales | `sales_view/add/edit/delete` |
| Purchases | `purchases_view/add/edit/delete` |
| Partners | `partners_view/add/edit/delete` |
| Reports | `reports_view/export/advanced` |

### Using Permissions

```python
from src.permissions import require_permission, Permissions

@app.route('/api/products')
@token_required
@require_permission(Permissions.PRODUCTS_VIEW)
def get_products():
    ...
```

---

## Input Validation

### Validation Layers

1. **Schema Validation** (Marshmallow)
   - Type checking
   - Length limits
   - Format validation

2. **Sanitization** (Bleach)
   - HTML stripping
   - XSS prevention

3. **SQL Injection Prevention**
   - SQLAlchemy ORM parameterization

### Example Schema

```python
class ProductCreateSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=200)
    )
    price = fields.Float(
        required=True,
        validate=validate.Range(min=0)
    )
    description = SafeString()  # Auto-sanitized
```

### Validation Decorator

```python
@app.route('/api/products', methods=['POST'])
@validate_json(ProductCreateSchema)
def create_product():
    data = g.validated_data  # Clean, validated data
    ...
```

---

## Data Protection

### Password Hashing

**Algorithm:** Argon2id (winner of Password Hashing Competition)

```python
# password_hasher.py
ARGON2_TIME_COST = 3      # Iterations
ARGON2_MEMORY_COST = 65536  # 64 MB
ARGON2_PARALLELISM = 4    # Threads
```

### Sensitive Data Handling

| Data Type | Protection |
|-----------|------------|
| Passwords | Argon2id hash (never stored plain) |
| API Keys | Environment variables |
| JWT Secrets | Environment variables |
| Database Credentials | Environment variables |
| Session Data | Server-side with secure cookies |

### Cookie Security

```python
SESSION_COOKIE_SECURE = True      # HTTPS only
SESSION_COOKIE_HTTPONLY = True    # No JS access
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection
```

---

## API Security

### Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/auth/login` | 5 | per minute |
| `/api/auth/register` | 3 | per minute |
| `/api/auth/refresh` | 10 | per minute |
| Default API | 100 | per minute |

### CORS Configuration

```python
CORS_ORIGINS = [
    'https://store.example.com',
    'https://admin.example.com'
]
```

### Security Headers

```python
# All responses include:
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-xxx'
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### CSRF Protection

- Enabled for all state-changing requests
- Token endpoint: `GET /api/csrf-token`
- Token header: `X-CSRF-Token`

---

## Infrastructure Security

### Docker Security

```dockerfile
# Security features in Dockerfile
USER 1001:1001              # Non-root user
HEALTHCHECK                 # Health monitoring
cap_drop: ALL               # Drop all capabilities
read_only: true             # Read-only filesystem
no-new-privileges: true     # Prevent privilege escalation
```

### Production Checklist

- [ ] HTTPS enforced
- [ ] Secrets in environment variables
- [ ] Database credentials rotated
- [ ] Firewall rules configured
- [ ] Logs shipped to SIEM
- [ ] Backups encrypted
- [ ] SBOM generated

---

## Monitoring & Logging

### Security Logs

| Event | Log Level | Action |
|-------|-----------|--------|
| Login Success | INFO | Audit trail |
| Login Failure | WARNING | Monitor for brute force |
| Account Locked | WARNING | Alert security team |
| Token Revoked | INFO | Audit trail |
| Permission Denied | WARNING | Monitor for privilege escalation |
| Rate Limit Hit | WARNING | Potential attack |

### Log Format

```json
{
    "timestamp": "2025-12-01T12:00:00Z",
    "level": "WARNING",
    "event": "AUTH_FAILED",
    "user": "unknown",
    "ip": "192.168.1.1",
    "details": "Invalid password attempt",
    "request_id": "abc123"
}
```

### Alerting Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Failed logins | >10/min | Alert + Block IP |
| Rate limit hits | >50/min | Alert |
| Error rate | >5% | Alert |
| Response time | >5s | Alert |

---

## Incident Response

### Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| P1 - Critical | Data breach, system compromise | Immediate |
| P2 - High | Authentication bypass, privilege escalation | 1 hour |
| P3 - Medium | Rate limiting bypass, minor vulnerability | 24 hours |
| P4 - Low | Security improvement needed | 1 week |

### Response Procedures

1. **Detect** - Security monitoring alerts
2. **Contain** - Isolate affected systems
3. **Eradicate** - Remove threat
4. **Recover** - Restore services
5. **Learn** - Post-incident review

### Emergency Contacts

- Security Team: security@company.com
- On-call: +966-XXX-XXXX
- Escalation: CTO

---

## Compliance

### Standards Followed

- OWASP Top 10 (2023)
- OWASP API Security Top 10
- CWE/SANS Top 25

### Security Testing

| Test Type | Frequency | Tool |
|-----------|-----------|------|
| SAST | Every commit | SonarQube |
| DAST | Weekly | OWASP ZAP |
| Dependency Scan | Daily | pip-audit |
| Penetration Test | Quarterly | External vendor |

### Documentation

| Document | Location |
|----------|----------|
| RBAC Matrix | `docs/RBAC_PERMISSION_MATRIX.md` |
| SQL Audit | `docs/SQL_INJECTION_AUDIT.md` |
| Secrets Scan | `docs/SECURITY_SCAN_REPORT.md` |
| API Contracts | `docs/API_Contracts.md` |

---

## Security Updates

### Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-01 | 1.0 | Initial security implementation |

### Planned Improvements

- [ ] T7: KMS/Vault integration
- [ ] T11: Frontend route guards
- [ ] T33: File upload scanning
- [ ] T34: SSRF defenses

---

**Document Owner:** Security Team  
**Review Cycle:** Quarterly  
**Next Review:** 2026-03-01
