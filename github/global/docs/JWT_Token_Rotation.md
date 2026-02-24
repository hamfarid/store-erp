# FILE: docs/JWT_Token_Rotation.md | PURPOSE: JWT token rotation documentation (P0.2) | OWNER: security | RELATED: backend/src/jwt_manager.py,backend/src/models/refresh_token.py | LAST-AUDITED: 2025-11-04

# JWT Token Rotation - P0.2

## Overview

Implemented JWT token rotation with short-lived access tokens (15 minutes) and long-lived refresh tokens (7 days) for enhanced security.

## Architecture

### Token Types

1. **Access Token**
   - Lifetime: 15 minutes (OWASP recommended)
   - Purpose: API authentication
   - Storage: Client-side (memory/localStorage)
   - Revocation: Not stored in database (short-lived)

2. **Refresh Token**
   - Lifetime: 7 days
   - Purpose: Obtain new access tokens
   - Storage: Database + client-side
   - Revocation: Supported via database

### Components

#### 1. JWT Manager (`backend/src/jwt_manager.py`)

**Features:**
- Token generation with JTI (JWT ID)
- Token verification with signature and expiration checks
- Token rotation support
- Client information tracking (IP, user agent, device fingerprint)

**Key Functions:**
```python
# Create token pair (access + refresh)
tokens = create_token_pair(user_id)

# Verify access token
payload = JWTManager.verify_access_token(token)

# Verify refresh token (includes database revocation check)
payload = JWTManager.verify_refresh_token(token)
```

#### 2. Refresh Token Model (`backend/src/models/refresh_token.py`)

**Database Schema:**
```sql
CREATE TABLE refresh_tokens (
    id INTEGER PRIMARY KEY,
    jti VARCHAR(36) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    token_hash VARCHAR(128) NOT NULL,
    expires_at DATETIME NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    revoked_at DATETIME,
    revocation_reason VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent VARCHAR(512),
    device_fingerprint VARCHAR(128),
    created_at DATETIME NOT NULL,
    last_used_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Indexes:**
- `idx_refresh_token_jti` (unique)
- `idx_refresh_token_user_id`
- `idx_refresh_token_expires_at`
- `idx_refresh_token_is_revoked`
- `idx_refresh_token_user_active` (user_id, is_revoked, expires_at)
- `idx_refresh_token_jti_active` (jti, is_revoked)

**Key Methods:**
```python
# Create token
RefreshToken.create_token(user_id, jti, token_hash, expires_at, ...)

# Find by JTI
token = RefreshToken.find_by_jti(jti)

# Revoke token
token.revoke(reason='User logout')

# Revoke all user tokens
RefreshToken.revoke_all_for_user(user_id)

# Cleanup expired tokens
RefreshToken.cleanup_expired()
```

#### 3. Authentication Routes (`backend/src/routes/auth_routes.py`)

**Endpoints:**

1. **POST /api/auth/login**
   - Returns: `{access_token, refresh_token, token_type, expires_in, refresh_expires_in}`
   - Uses `create_token_pair()` if JWT rotation is available

2. **POST /api/auth/refresh**
   - Request: `{refresh_token}`
   - Response: `{access_token, token_type, expires_in}`
   - Verifies refresh token (includes database revocation check)
   - Issues new access token

3. **POST /api/auth/tokens/revoke**
   - Request: `{refresh_token}` OR `{revoke_all: true}`
   - Revokes specific token or all user tokens
   - Requires authentication for `revoke_all`

4. **GET /api/auth/tokens**
   - Lists all active refresh tokens for authenticated user
   - Returns: `{tokens: [{jti, created_at, expires_at, ip_address, ...}]}`

## Security Features

### 1. Token Revocation

**Individual Token:**
```bash
POST /api/auth/tokens/revoke
{
  "refresh_token": "eyJ..."
}
```

**All User Tokens (Logout from all devices):**
```bash
POST /api/auth/tokens/revoke
{
  "revoke_all": true
}
```

### 2. Token Rotation (Optional)

Uncomment in `auth_routes.py` to enable automatic refresh token rotation:
```python
rotate_refresh = data.get('rotate_refresh', False)
if rotate_refresh:
    # Revoke old token and issue new one
```

### 3. Device Tracking

Each refresh token stores:
- IP address
- User agent
- Device fingerprint (MD5 hash of user agent)

### 4. Automatic Cleanup

**Expired Tokens:**
```python
# Run periodically (e.g., daily cron job)
RefreshToken.cleanup_expired()
```

**Old Revoked Tokens:**
```python
# Delete revoked tokens older than 30 days
RefreshToken.cleanup_revoked(days=30)
```

## Usage Examples

### Client-Side Implementation

```javascript
// Login
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username, password, use_jwt: true})
});

const {data} = await response.json();
const {access_token, refresh_token, expires_in} = data.tokens;

// Store tokens
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);

// Set refresh timer (before expiration)
setTimeout(refreshAccessToken, (expires_in - 60) * 1000);

// Refresh access token
async function refreshAccessToken() {
  const refresh_token = localStorage.getItem('refresh_token');
  const response = await fetch('/api/auth/refresh', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({refresh_token})
  });
  
  const {data} = await response.json();
  localStorage.setItem('access_token', data.access_token);
  
  // Set next refresh timer
  setTimeout(refreshAccessToken, (data.expires_in - 60) * 1000);
}

// API requests with access token
async function apiRequest(url, options = {}) {
  const access_token = localStorage.getItem('access_token');
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${access_token}`
    }
  });
  
  // Handle 401 (token expired)
  if (response.status === 401) {
    await refreshAccessToken();
    // Retry request
    return apiRequest(url, options);
  }
  
  return response;
}

// Logout (revoke all tokens)
async function logout() {
  await fetch('/api/auth/tokens/revoke', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify({revoke_all: true})
  });
  
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}
```

## Migration

### Database Migration

```bash
cd backend
flask db upgrade
```

Or manually run:
```bash
python -m flask db migrate -m "Add refresh_tokens table"
python -m flask db upgrade
```

### Environment Variables

Add to `.env`:
```bash
# JWT Configuration (P0.2)
JWT_SECRET_KEY=<generate-strong-secret-key>  # REQUIRED in production
JWT_ACCESS_TOKEN_EXPIRES=900  # 15 minutes (seconds)
JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days (seconds)
```

**Generate strong secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Testing

### Manual Testing

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","use_jwt":true}'

# Refresh token
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJ..."}'

# List tokens
curl -X GET http://localhost:5000/api/auth/tokens \
  -H "Authorization: Bearer eyJ..."

# Revoke token
curl -X POST http://localhost:5000/api/auth/tokens/revoke \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJ..."}'

# Revoke all tokens
curl -X POST http://localhost:5000/api/auth/tokens/revoke \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{"revoke_all":true}'
```

## Security Considerations

1. **Secret Key Management**
   - NEVER commit JWT_SECRET_KEY to version control
   - Use KMS/Vault in production (P0.6)
   - Rotate secret periodically (invalidates all tokens)

2. **Token Storage**
   - Access token: Memory or sessionStorage (NOT localStorage for XSS protection)
   - Refresh token: httpOnly cookie (preferred) or localStorage

3. **HTTPS Only**
   - MUST use HTTPS in production (P0.4)
   - Tokens transmitted in plain text over HTTP are vulnerable

4. **Rate Limiting**
   - Login: 5 per minute
   - Refresh: 10 per minute
   - Revoke: 10 per minute

5. **Token Expiration**
   - Access: 15 minutes (balance between security and UX)
   - Refresh: 7 days (can be adjusted based on risk tolerance)

## Monitoring

### Metrics to Track

1. **Token Usage**
   - Active refresh tokens per user
   - Token refresh rate
   - Token revocation rate

2. **Security Events**
   - Failed token verifications
   - Revoked token usage attempts
   - Suspicious device changes

3. **Performance**
   - Token generation time
   - Database query performance for token lookups

### Alerts

- Multiple failed token verifications from same IP
- Unusual token refresh patterns
- High revocation rate

## Future Enhancements

1. **Automatic Token Rotation** (currently optional)
   - Enable by default for enhanced security
   - Implement sliding window refresh

2. **Device Management UI**
   - Show active sessions/devices
   - Revoke specific devices

3. **Anomaly Detection**
   - Detect suspicious login locations
   - Alert on unusual device changes

4. **Token Binding**
   - Bind tokens to specific devices/browsers
   - Prevent token theft

## References

- OWASP JWT Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
- RFC 7519 (JWT): https://tools.ietf.org/html/rfc7519
- RFC 6749 (OAuth 2.0): https://tools.ietf.org/html/rfc6749

