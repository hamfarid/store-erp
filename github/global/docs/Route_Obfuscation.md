# FILE: docs/Route_Obfuscation.md | PURPOSE: Route obfuscation and anti-enumeration documentation | OWNER: Security | RELATED: docs/Security.md, docs/CSP.md | LAST-AUDITED: 2025-10-21

# Route Obfuscation — إخفاء المسارات

**Version**: 1.0  
**Last Updated**: 2025-10-21  
**Status**: 🔴 Not Implemented

---

## 1. Overview

Route obfuscation prevents attackers from enumerating application endpoints, discovering hidden features, and mapping the application structure through predictable URL patterns.

**Threat**: Attackers can discover sensitive endpoints by:
- Guessing predictable URLs (`/admin`, `/api/users`, `/api/internal`)
- Brute-forcing sequential IDs (`/api/users/1`, `/api/users/2`, ...)
- Analyzing JavaScript bundles for route definitions
- Observing network traffic for API patterns

**Mitigation Strategy**:
1. **HMAC-Signed Route Labels** — Dynamic, time-limited route identifiers
2. **Contenthash Chunk Names** — Obfuscated JavaScript bundle names
3. **Anti-Enumeration 404** — Uniform error responses
4. **Server-Side Authorization** — Never rely on client-side route hiding

---

## 2. HMAC-Signed Route Labels

### 2.1 Concept

Instead of exposing predictable route names in the frontend, generate HMAC-signed labels that:
- Change periodically (short TTL)
- Cannot be guessed or forged
- Are validated server-side

**Example**:
```
❌ Predictable: /api/users/123
✅ Obfuscated: /api/r/a7f3c2e1b9d4/123
```

Where `a7f3c2e1b9d4` is an HMAC-signed label for the `users` route.

---

### 2.2 Implementation (Backend)

**Generate Route Label**:
```python
import hmac
import hashlib
import time
from flask import current_app

def generate_route_label(route_name: str, ttl_seconds: int = 3600) -> str:
    """
    Generate HMAC-signed route label with TTL.
    
    Args:
        route_name: Internal route name (e.g., 'users')
        ttl_seconds: Time-to-live in seconds (default: 1 hour)
    
    Returns:
        HMAC-signed label (e.g., 'a7f3c2e1b9d4')
    """
    secret = current_app.config['SECRET_KEY'].encode()
    timestamp = int(time.time() // ttl_seconds)  # Bucket by TTL
    message = f"{route_name}:{timestamp}".encode()
    
    signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return signature[:12]  # First 12 chars for brevity
```

**Validate Route Label**:
```python
def validate_route_label(label: str, route_name: str, ttl_seconds: int = 3600) -> bool:
    """
    Validate HMAC-signed route label.
    
    Args:
        label: Provided route label
        route_name: Expected route name
        ttl_seconds: Time-to-live in seconds
    
    Returns:
        True if valid, False otherwise
    """
    expected_label = generate_route_label(route_name, ttl_seconds)
    return hmac.compare_digest(label, expected_label)
```

**Flask Route Example**:
```python
from flask import Blueprint, request, jsonify, abort

api = Blueprint('api', __name__)

@api.route('/r/<label>/<int:user_id>', methods=['GET'])
def get_user_obfuscated(label: str, user_id: int):
    # Validate route label
    if not validate_route_label(label, 'users'):
        abort(404)  # Return 404, not 403 (anti-enumeration)
    
    # Proceed with normal logic
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())
```

---

### 2.3 Implementation (Frontend)

**Route Label Provider**:
```javascript
// src/utils/routeLabels.js
const ROUTE_LABELS_CACHE_KEY = 'route_labels';
const ROUTE_LABELS_TTL = 3600 * 1000; // 1 hour in ms

export async function getRouteLabel(routeName) {
  // Check cache
  const cached = localStorage.getItem(ROUTE_LABELS_CACHE_KEY);
  if (cached) {
    const { labels, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp < ROUTE_LABELS_TTL) {
      return labels[routeName];
    }
  }
  
  // Fetch fresh labels from server
  const response = await fetch('/api/route-labels', {
    headers: { 'Authorization': `Bearer ${getAccessToken()}` }
  });
  const labels = await response.json();
  
  // Cache labels
  localStorage.setItem(ROUTE_LABELS_CACHE_KEY, JSON.stringify({
    labels,
    timestamp: Date.now()
  }));
  
  return labels[routeName];
}
```

**API Client Example**:
```javascript
// src/api/users.js
import { getRouteLabel } from '@/utils/routeLabels';

export async function getUser(userId) {
  const label = await getRouteLabel('users');
  const response = await fetch(`/api/r/${label}/${userId}`, {
    headers: { 'Authorization': `Bearer ${getAccessToken()}` }
  });
  return response.json();
}
```

---

### 2.4 Route Labels Endpoint

**Backend**:
```python
@api.route('/route-labels', methods=['GET'])
@jwt_required()
def get_route_labels():
    """
    Return HMAC-signed labels for all routes.
    Requires authentication.
    """
    labels = {
        'users': generate_route_label('users'),
        'products': generate_route_label('products'),
        'invoices': generate_route_label('invoices'),
        'customers': generate_route_label('customers'),
        'suppliers': generate_route_label('suppliers'),
        'reports': generate_route_label('reports'),
        # ... all routes
    }
    return jsonify(labels)
```

---

## 3. Contenthash Chunk Names

### 3.1 Concept

Obfuscate JavaScript bundle names to prevent attackers from:
- Identifying specific features by chunk names
- Discovering new features by monitoring bundle changes
- Reverse-engineering application structure

**Example**:
```
❌ Predictable: admin-panel.js, user-management.js
✅ Obfuscated: a7f3c2e1.js, b9d4e5f6.js
```

---

### 3.2 Implementation (Vite)

**vite.config.js**:
```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        // Obfuscate chunk names with contenthash
        chunkFileNames: 'assets/[hash].js',
        entryFileNames: 'assets/[hash].js',
        assetFileNames: 'assets/[hash].[ext]',
        
        // Manual chunks (optional - for code splitting)
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return 'vendor';
          }
          // Do NOT use descriptive names like 'admin' or 'user-management'
        }
      }
    },
    
    // Enable minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,  // Remove console.log in production
        drop_debugger: true
      },
      mangle: {
        toplevel: true  // Mangle top-level variable names
      }
    }
  }
});
```

---

### 3.3 Source Map Security

**IMPORTANT**: Never deploy source maps to production.

**vite.config.js**:
```javascript
export default defineConfig({
  build: {
    sourcemap: process.env.NODE_ENV === 'development',  // Only in dev
  }
});
```

**Nginx Configuration** (block .map files):
```nginx
location ~* \.map$ {
  deny all;
  return 404;
}
```

---

## 4. Anti-Enumeration 404

### 4.1 Concept

Return uniform 404 responses for:
- Invalid routes
- Unauthorized access
- Non-existent resources

**DO NOT** return different status codes that leak information:
- ❌ 403 Forbidden → "Resource exists but you can't access it"
- ❌ 401 Unauthorized → "Resource exists but you're not logged in"
- ✅ 404 Not Found → "Nothing to see here"

---

### 4.2 Implementation (Backend)

**Flask Error Handler**:
```python
from flask import jsonify

@app.errorhandler(403)
def forbidden(error):
    # Return 404 instead of 403 to prevent enumeration
    return jsonify({
        'success': False,
        'error': {
            'code': 'NOT_FOUND',
            'message': 'المورد غير موجود',
            'traceId': generate_trace_id()
        }
    }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': {
            'code': 'NOT_FOUND',
            'message': 'المورد غير موجود',
            'traceId': generate_trace_id()
        }
    }), 404
```

**Authorization Check**:
```python
@api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    
    # Check if user exists
    if not user:
        abort(404)  # Not found
    
    # Check authorization
    if not current_user.can_view_user(user):
        abort(404)  # Return 404, not 403
    
    return jsonify(user.to_dict())
```

---

### 4.3 Timing Attack Prevention

**Problem**: Attackers can distinguish between "not found" and "unauthorized" by measuring response time.

**Solution**: Add constant-time delay for all 404 responses.

```python
import time
import random

@app.errorhandler(404)
def not_found(error):
    # Add random delay (50-150ms) to prevent timing attacks
    time.sleep(random.uniform(0.05, 0.15))
    
    return jsonify({
        'success': False,
        'error': {
            'code': 'NOT_FOUND',
            'message': 'المورد غير موجود',
            'traceId': generate_trace_id()
        }
    }), 404
```

---

## 5. Server-Side Authorization

### 5.1 Never Trust Client-Side Route Hiding

**IMPORTANT**: Route obfuscation is **defense in depth**, not a replacement for proper authorization.

**Always enforce authorization server-side**:
```python
@api.route('/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    # ✅ Server-side authorization check
    if not current_user.has_permission('ADMIN'):
        abort(404)  # Not 403
    
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
```

---

### 5.2 Frontend Route Guards

**React Router Example**:
```javascript
// src/components/ProtectedRoute.jsx
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

export function ProtectedRoute({ children, requiredPermission }) {
  const { user, hasPermission } = useAuth();
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  if (requiredPermission && !hasPermission(requiredPermission)) {
    // Redirect to 404, not "Unauthorized" page
    return <Navigate to="/404" replace />;
  }
  
  return children;
}
```

**Usage**:
```javascript
<Route
  path="/admin/users"
  element={
    <ProtectedRoute requiredPermission="ADMIN">
      <UserManagement />
    </ProtectedRoute>
  }
/>
```

---

## 6. Additional Hardening

### 6.1 Disable Directory Listing

**Nginx**:
```nginx
autoindex off;
```

---

### 6.2 Remove Server Headers

**Nginx**:
```nginx
server_tokens off;
more_clear_headers 'Server';
more_clear_headers 'X-Powered-By';
```

**Flask**:
```python
@app.after_request
def remove_server_header(response):
    response.headers.pop('Server', None)
    return response
```

---

### 6.3 Rate Limiting

**Prevent brute-force enumeration**:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@api.route('/users/<int:user_id>', methods=['GET'])
@limiter.limit("10 per minute")
@jwt_required()
def get_user(user_id):
    # ...
```

---

## 7. Implementation Checklist

- [ ] Implement HMAC-signed route labels (backend)
- [ ] Create `/api/route-labels` endpoint
- [ ] Implement route label validation middleware
- [ ] Update frontend API client to use route labels
- [ ] Configure Vite for contenthash chunk names
- [ ] Disable source maps in production
- [ ] Block .map files in Nginx
- [ ] Implement anti-enumeration 404 error handler
- [ ] Add timing attack prevention
- [ ] Verify server-side authorization on all endpoints
- [ ] Add frontend route guards
- [ ] Disable directory listing (Nginx)
- [ ] Remove server headers
- [ ] Implement rate limiting on sensitive endpoints
- [ ] Test with security scanner (OWASP ZAP)

---

## 8. Testing

### 8.1 Manual Testing

**Test 1: Route Label Validation**
```bash
# Valid label (should return 200)
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5002/api/r/a7f3c2e1b9d4/123

# Invalid label (should return 404)
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5002/api/r/invalid/123
```

**Test 2: Expired Label**
```bash
# Wait for TTL to expire (1 hour)
# Request with old label (should return 404)
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5002/api/r/old_label/123
```

**Test 3: Unauthorized Access**
```bash
# Request without permission (should return 404, not 403)
curl -H "Authorization: Bearer $USER_TOKEN" \
  http://localhost:5002/api/admin/users
```

---

### 8.2 Automated Testing

**Pytest Example**:
```python
def test_route_label_validation():
    # Generate valid label
    label = generate_route_label('users')
    
    # Valid request
    response = client.get(f'/api/r/{label}/123', headers=auth_headers)
    assert response.status_code == 200
    
    # Invalid label
    response = client.get('/api/r/invalid/123', headers=auth_headers)
    assert response.status_code == 404

def test_anti_enumeration():
    # Non-existent resource
    response = client.get('/api/users/99999', headers=auth_headers)
    assert response.status_code == 404
    
    # Unauthorized access
    response = client.get('/api/admin/users', headers=user_headers)
    assert response.status_code == 404  # Not 403
```

---

## 9. Monitoring

### 9.1 Metrics

Track the following metrics:
- **404 rate** — Spike may indicate enumeration attempt
- **Invalid route label attempts** — Potential attack
- **Rate limit violations** — Brute-force attempt

**Prometheus Example**:
```python
from prometheus_client import Counter

route_label_invalid = Counter(
    'route_label_invalid_total',
    'Total invalid route label attempts',
    ['route_name']
)

@api.route('/r/<label>/<int:user_id>', methods=['GET'])
def get_user_obfuscated(label: str, user_id: int):
    if not validate_route_label(label, 'users'):
        route_label_invalid.labels(route_name='users').inc()
        abort(404)
    # ...
```

---

### 9.2 Alerts

**Alert on suspicious activity**:
```yaml
# Prometheus alert rule
- alert: HighInvalidRouteLabelRate
  expr: rate(route_label_invalid_total[5m]) > 10
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High rate of invalid route label attempts"
    description: "{{ $value }} invalid attempts per second"
```

---

## 10. References

- OWASP: Insecure Direct Object References (IDOR)
- OWASP: Security Misconfiguration
- NIST: SP 800-53 (AC-3: Access Enforcement)
- CWE-639: Authorization Bypass Through User-Controlled Key

