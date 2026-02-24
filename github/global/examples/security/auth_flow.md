# Perfect Authentication Flow (Global System v26 Diamond 32 Synchronized Intelligence Edition)

## 1. The Planner's Intent
*   **Goal:** Secure, stateless JWT authentication.
*   **Constraints:** No sensitive data in tokens. Short-lived access tokens (15m). HttpOnly cookies for refresh tokens.

## 2. The Executor's Implementation
```python
# auth_service.py
import jwt
import datetime
from fastapi import HTTPException

SECRET_KEY = os.getenv("JWT_SECRET")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

## 3. The Reviewer's Audit
*   [x] `SECRET_KEY` loaded from env? Yes.
*   [x] Expiration set? Yes (15m).
*   [x] Algorithm specified? Yes (HS256).

## 4. The Critic's Verdict
*   **Status:** APPROVED.
*   **Note:** Ensure `JWT_SECRET` is rotated weekly.
