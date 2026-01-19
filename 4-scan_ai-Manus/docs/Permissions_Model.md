# Permissions Model - Gaara Scan AI v4.3

**Last Updated:** 2025-12-05  
**Version:** 4.3.0

---

## Overview

Gaara Scan AI uses a **Role-Based Access Control (RBAC)** system with four primary roles and granular permissions.

---

## User Roles

### 1. **ADMIN** (Administrator)
- **Full system access**
- Can manage all users, farms, and system settings
- Can access all API endpoints
- Can modify system configuration
- Can view audit logs and security reports

### 2. **MANAGER** (Farm Manager)
- **Farm management access**
- Can create, edit, and delete farms
- Can view and manage diagnoses for assigned farms
- Can generate reports for assigned farms
- Cannot manage users or system settings

### 3. **USER** (Standard User)
- **Limited access**
- Can view assigned farms
- Can create diagnoses
- Can view own reports
- Cannot create or delete farms
- Cannot access admin features

### 4. **GUEST** (Read-Only)
- **View-only access**
- Can view public farms and diagnoses
- Cannot create, edit, or delete anything
- Cannot access reports or analytics

---

## Permission Matrix

| Feature | ADMIN | MANAGER | USER | GUEST |
|---------|-------|---------|------|-------|
| **User Management** |
| View all users | ✅ | ❌ | ❌ | ❌ |
| Create users | ✅ | ❌ | ❌ | ❌ |
| Edit users | ✅ | ❌ | ❌ | ❌ |
| Delete users | ✅ | ❌ | ❌ | ❌ |
| **Farm Management** |
| View all farms | ✅ | ✅ (assigned) | ✅ (assigned) | ✅ (public) |
| Create farms | ✅ | ✅ | ❌ | ❌ |
| Edit farms | ✅ | ✅ (assigned) | ❌ | ❌ |
| Delete farms | ✅ | ✅ (assigned) | ❌ | ❌ |
| **Diagnosis** |
| View all diagnoses | ✅ | ✅ (assigned farms) | ✅ (own) | ✅ (public) |
| Create diagnoses | ✅ | ✅ | ✅ | ❌ |
| Edit diagnoses | ✅ | ✅ (assigned farms) | ✅ (own) | ❌ |
| Delete diagnoses | ✅ | ✅ (assigned farms) | ✅ (own) | ❌ |
| **Reports** |
| View all reports | ✅ | ✅ (assigned farms) | ✅ (own) | ❌ |
| Generate reports | ✅ | ✅ | ✅ | ❌ |
| Export reports | ✅ | ✅ | ✅ | ❌ |
| **Analytics** |
| View analytics | ✅ | ✅ (assigned farms) | ✅ (own) | ❌ |
| **System Settings** |
| View settings | ✅ | ❌ | ❌ | ❌ |
| Edit settings | ✅ | ❌ | ❌ | ❌ |
| **Security** |
| View audit logs | ✅ | ❌ | ❌ | ❌ |
| View security reports | ✅ | ❌ | ❌ | ❌ |

---

## Implementation

### Database Model

The `User` model includes a `role` field:

```python
role = Column(String(50), default='USER', nullable=False)
# Values: 'ADMIN', 'MANAGER', 'USER', 'GUEST'
```

### Role Assignment

Roles are assigned during user creation or can be updated by administrators:

```python
# Default role
user.role = 'USER'

# Admin role
user.role = 'ADMIN'

# Manager role
user.role = 'MANAGER'

# Guest role
user.role = 'GUEST'
```

### Permission Checking

Permissions are checked in API endpoints and frontend routes:

**Backend Example:**
```python
from functools import wraps

def require_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            user = get_current_user(request)
            if user.role not in allowed_roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

# Usage
@router.get("/admin/users")
@require_role("ADMIN")
async def get_all_users():
    ...
```

**Frontend Example:**
```javascript
// Check role before rendering
const canManageUsers = user.role === 'ADMIN';

{canManageUsers && (
  <Button onClick={handleCreateUser}>Create User</Button>
)}
```

---

## MFA (Multi-Factor Authentication)

MFA is available for all roles but **required** for:
- **ADMIN** users
- **MANAGER** users with access to sensitive data

MFA fields in User model:
- `mfa_secret`: TOTP secret key
- `mfa_enabled`: Boolean flag
- `mfa_backup_codes`: JSON array of backup codes

---

## Account Status

### Active Status
- `is_active`: Boolean - User can log in
- `is_verified`: Boolean - Email verified
- `email_verified_at`: DateTime - When email was verified

### Security Status
- `failed_login_attempts`: Integer - Count of failed logins
- `locked_until`: DateTime - Account lockout expiry
- `last_login_at`: DateTime - Last successful login
- `last_login_ip`: String - IP address of last login

---

## Password Policy

All users must follow password policy:
- Minimum 12 characters
- Must contain uppercase, lowercase, numbers, and special characters
- Cannot reuse last 5 passwords
- Must change password every 90 days (ADMIN/MANAGER)
- Account locked after 5 failed login attempts

---

## Future Enhancements

### Planned Features:
1. **Granular Permissions** - Per-module permissions (e.g., `farms.create`, `diagnosis.delete`)
2. **Permission Groups** - Custom permission sets
3. **Time-Based Access** - Scheduled access restrictions
4. **IP Whitelisting** - Restrict access by IP address
5. **API Key Permissions** - Separate permissions for API keys

---

## Security Considerations

1. **Principle of Least Privilege**: Users get minimum required permissions
2. **Role Separation**: Clear boundaries between roles
3. **Audit Logging**: All permission checks logged
4. **Session Management**: Roles checked on every request
5. **Token Validation**: JWT tokens include role information

---

## Related Documentation

- [Security Guidelines](Security.md)
- [API Documentation](API_DOCUMENTATION.md)
- [User Model](../backend/src/models/user.py)
- [Authentication API](../backend/src/api/v1/auth.py)

---

**Last Updated:** 2025-12-05  
**Maintained by:** Backend Team

