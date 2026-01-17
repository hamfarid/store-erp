# 🔐 Authentication Flow Documentation

**Version:** 2.0.0  
**Last Updated:** 2026-01-17

---

## 📋 Overview

This document describes the complete authentication flow in Store ERP, including login, logout, registration, password reset, and two-factor authentication.

---

## 🌐 Auth Routes

### Frontend Pages

| Route | Page | Description |
|-------|------|-------------|
| `/login` | `Login.jsx` | تسجيل الدخول |
| `/logout` | `Logout.jsx` | تسجيل الخروج |
| `/register` | `Register.jsx` | تسجيل مستخدم جديد |
| `/forgot-password` | `ForgotPassword.jsx` | طلب استعادة كلمة المرور |
| `/reset-password` | `ResetPassword.jsx` | إعادة تعيين كلمة المرور |
| `/2fa-verify` | `TwoFactorVerify.jsx` | التحقق من المصادقة الثنائية |

### Backend Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login` | POST | تسجيل الدخول |
| `/api/auth/logout` | POST | تسجيل الخروج |
| `/api/auth/refresh` | POST | تجديد التوكن |
| `/api/auth/register` | POST | تسجيل مستخدم جديد |
| `/api/auth/me` | GET | بيانات المستخدم الحالي |
| `/api/auth/change-password` | POST | تغيير كلمة المرور |
| `/api/auth/forgot-password` | POST | طلب استعادة كلمة المرور |
| `/api/auth/reset-password` | POST | إعادة تعيين كلمة المرور |
| `/api/auth/2fa/enable` | POST | تفعيل المصادقة الثنائية |
| `/api/auth/2fa/disable` | POST | إلغاء المصادقة الثنائية |
| `/api/auth/2fa/verify` | POST | التحقق من رمز 2FA |
| `/api/auth/sessions` | GET | الجلسات النشطة |

---

## 🔄 Login Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         LOGIN FLOW                              │
└─────────────────────────────────────────────────────────────────┘

     User                    Frontend                   Backend
       │                         │                         │
       │  Enter credentials      │                         │
       │─────────────────────────►                         │
       │                         │                         │
       │                         │  POST /api/auth/login   │
       │                         │─────────────────────────►
       │                         │                         │
       │                         │      Validate           │
       │                         │◄─────────────────────────
       │                         │                         │
       │                    ┌────┴────┐                    │
       │                    │ 2FA     │                    │
       │                    │Enabled? │                    │
       │                    └────┬────┘                    │
       │                    Yes  │  No                     │
       │                    ┌────┴────┐                    │
       │                    │         │                    │
       │                    ▼         ▼                    │
       │            ┌──────────┐  ┌──────────┐            │
       │            │2FA Verify│  │ Success  │            │
       │            │  Page    │  │ + Tokens │            │
       │            └──────────┘  └──────────┘            │
       │                    │         │                    │
       │◄───────────────────┴─────────┘                    │
       │                                                   │
```

### Login Request

```json
POST /api/auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

### Login Response (Success)

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1Ni...",
    "refresh_token": "eyJhbGciOiJIUzI1Ni...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@store.com",
      "full_name": "مدير النظام",
      "role": "admin",
      "permissions": ["*"]
    }
  }
}
```

### Login Response (2FA Required)

```json
{
  "success": true,
  "data": {
    "requires_2fa": true,
    "temp_token": "eyJhbGciOiJIUzI1Ni..."
  }
}
```

---

## 🔑 Two-Factor Authentication

### Enable 2FA

```json
POST /api/auth/2fa/enable

Response:
{
  "success": true,
  "data": {
    "secret": "JBSWY3DPEHPK3PXP",
    "qr_code": "data:image/png;base64,...",
    "backup_codes": [
      "XXXX-XXXX-XXXX",
      "YYYY-YYYY-YYYY",
      ...
    ]
  }
}
```

### Verify 2FA

```json
POST /api/auth/2fa/verify
{
  "code": "123456"
}

Response:
{
  "success": true,
  "data": {
    "access_token": "...",
    "refresh_token": "...",
    "user": {...}
  }
}
```

---

## 🔄 Token Refresh Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      TOKEN REFRESH FLOW                          │
└─────────────────────────────────────────────────────────────────┘

  API Client                 Frontend                    Backend
       │                         │                         │
       │  Request (401)          │                         │
       │◄────────────────────────│                         │
       │                         │                         │
       │  Check refresh token    │                         │
       │─────────────────────────►                         │
       │                         │                         │
       │                         │ POST /api/auth/refresh  │
       │                         │─────────────────────────►
       │                         │                         │
       │                         │    New tokens           │
       │                         │◄─────────────────────────
       │                         │                         │
       │  Retry original req     │                         │
       │─────────────────────────►                         │
       │                         │                         │
```

### Refresh Request

```json
POST /api/auth/refresh
{
  "refresh_token": "eyJhbGciOiJIUzI1Ni..."
}
```

---

## 🔒 Password Reset Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PASSWORD RESET FLOW                           │
└─────────────────────────────────────────────────────────────────┘

   1. User clicks "Forgot Password"
   2. Enters email address
   3. Backend sends reset email with token
   4. User clicks link in email
   5. User enters new password
   6. Backend validates token and updates password
   7. User redirected to login
```

### Forgot Password Request

```json
POST /api/auth/forgot-password
{
  "email": "user@example.com"
}
```

### Reset Password Request

```json
POST /api/auth/reset-password
{
  "token": "reset_token_from_email",
  "new_password": "newSecurePassword123"
}
```

---

## 🚪 Logout Flow

```javascript
// Frontend - Logout.jsx
const logout = async () => {
  try {
    // Call backend logout
    await authService.logout();
  } finally {
    // Clear local storage
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    
    // Redirect to login
    navigate('/login');
  }
};
```

### Logout Request

```json
POST /api/auth/logout
Headers:
  Authorization: Bearer {access_token}
```

---

## 🛡️ Protected Routes

### Frontend Route Protection

```jsx
const ProtectedRoute = ({ children, requiredPermission }) => {
  const { user, isAuthenticated } = useAuth();

  // Not authenticated → redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // No permission → redirect to 403
  if (requiredPermission && !hasPermission(user, requiredPermission)) {
    return <Navigate to="/403" replace />;
  }

  return children;
};
```

### Backend Route Protection

```python
@app.route('/api/protected')
@jwt_required()
@require_permission('resource.view')
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({"user": current_user})
```

---

## 📱 Session Management

### Session Security Features

1. **Session Fingerprinting** - Browser fingerprint validation
2. **Activity Monitoring** - Track user activity
3. **Idle Timeout** - Auto-logout after inactivity
4. **Token Rotation** - Rotate refresh tokens on use

### Session Storage

```javascript
// sessionSecurity.js
const sessionSecurity = {
  initializeSession(user, tokens) {
    localStorage.setItem('token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('session_fingerprint', this.generateFingerprint());
  },
  
  validateSession() {
    const fingerprint = localStorage.getItem('session_fingerprint');
    return fingerprint === this.generateFingerprint();
  },
  
  cleanLogout() {
    localStorage.clear();
    sessionStorage.clear();
  }
};
```

---

## 📊 Auth Context

### AuthContext Provider

```jsx
// AuthContext.jsx
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = async (username, password) => {
    const result = await authService.login(username, password);
    if (result.success) {
      setUser(result.data.user);
      setIsAuthenticated(true);
      return { success: true };
    }
    return { success: false, error: result.error };
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

---

## 🔧 Configuration

### Environment Variables

```env
# Frontend
VITE_API_BASE=http://localhost:6001
VITE_ENABLE_2FA=true

# Backend
JWT_SECRET_KEY=your-super-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=604800
```

### JWT Token Structure

```json
{
  "sub": "1",              // User ID
  "username": "admin",
  "role": "admin",
  "permissions": ["*"],
  "iat": 1704067200,       // Issued at
  "exp": 1704070800        // Expires
}
```

---

*Authentication Flow Documentation - Store ERP v2.0.0*
