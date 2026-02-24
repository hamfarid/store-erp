# 🛡️ Security & Audit Workflow (AI Learning Guide)

This document teaches the AI how to implement security controls and conduct audits.

## 1. Standard Security Module Structure
Every security module (e.g., `auth_middleware.py`, `encryption_utils.py`) must follow this pattern:

### 📥 Imports (Inputs)
*   **Crypto Libraries**: `cryptography`, `passlib`, `jose`.
*   **Standards**: `OAuth2`, `OIDC`.
*   **Context**: Request headers, User session.

### 📤 Exports (Outputs)
*   **Guards**: Decorators/Middleware (e.g., `@require_admin`).
*   **Tokens**: Secure strings (JWT, API Keys).
*   **Audit Logs**: Secure log entries.

### 🔄 Operational Workflow
1.  **Interception**: Intercept request/action at the boundary.
2.  **Verification**: Validate credentials, signatures, or permissions.
3.  **Decision**: Allow (Pass) or Deny (Raise Exception).
4.  **Logging**: Record the decision in the Audit Log.

## 2. Example: Role-Based Access Control (RBAC)

```python
# security/rbac.py

# 📥 IMPORTS
from functools import wraps
from flask import request, abort
from tools.logger import audit_log

# 🔄 WORKFLOW
# 1. Decorator receives required role.
# 2. Check user role from session/token.
# 3. If match, execute function.
# 4. If mismatch, abort 403 and log attempt.

# 📤 EXPORTS
def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = request.headers.get('X-Role')
            if user_role != role:
                audit_log(f"Unauthorized access attempt by {user_role}")
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

## 3. AI Action Items
*   **Zero Trust**: Verify every request, internal or external.
*   **Least Privilege**: Grant only necessary permissions.
*   **Sanitization**: Validate and sanitize all inputs to prevent Injection.
