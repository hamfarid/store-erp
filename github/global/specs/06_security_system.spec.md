# Security System Specification

**Version:** 2.0.0  
**Status:** Implemented  
**Last Updated:** 2026-01-16

---

## Overview

نظام أمان متعدد الطبقات يشمل JWT + 2FA + RBAC مع 68 صلاحية.

---

## Authentication

### JWT Token Structure
```json
{
  "sub": "user_id",
  "role": "admin",
  "permissions": ["..."],
  "exp": 1704067200,
  "iat": 1704063600
}
```

### Token Configuration
| Setting | Value |
|---------|-------|
| Access Token Expiry | 1 hour |
| Refresh Token Expiry | 7 days |
| Algorithm | HS256 |

### Login Flow
1. User submits credentials
2. Backend validates
3. Returns access + refresh tokens
4. Frontend stores in localStorage
5. Auto-refresh on expiry

---

## Two-Factor Authentication (2FA)

### TOTP Setup
1. User enables 2FA
2. Backend generates secret
3. QR code displayed
4. User scans with Google Authenticator
5. User enters verification code
6. 2FA enabled

### Verification
- 6-digit TOTP code
- 30-second window
- Backup codes available

---

## Role-Based Access Control (RBAC)

### Default Roles

| Role | Description | Users |
|------|-------------|-------|
| admin | Full system access | 1+ |
| manager | Management access | 2+ |
| accountant | Financial access | 2+ |
| cashier | POS access | 5+ |
| warehouse | Inventory access | 3+ |
| sales | Sales access | 5+ |
| viewer | Read-only access | 10+ |

### Permission Categories (68 total)

**Products (8)**
- `products.view`, `products.create`, `products.update`, `products.delete`
- `products.import`, `products.export`, `products.price`, `products.cost`

**Inventory (8)**
- `inventory.view`, `inventory.adjust`, `inventory.transfer`
- `lots.view`, `lots.create`, `lots.update`, `lots.delete`, `lots.status`

**Sales (8)**
- `sales.view`, `sales.create`, `sales.update`, `sales.void`
- `pos.access`, `pos.discount`, `pos.return`, `pos.void`

**Purchases (8)**
- `purchases.view`, `purchases.create`, `purchases.update`, `purchases.approve`
- `purchases.receive`, `purchases.cancel`, `purchases.payment`, `purchases.void`

**Customers (6)**
- `customers.view`, `customers.create`, `customers.update`, `customers.delete`
- `customers.credit`, `customers.balance`

**Suppliers (6)**
- `suppliers.view`, `suppliers.create`, `suppliers.update`, `suppliers.delete`
- `suppliers.payment`, `suppliers.balance`

**Reports (8)**
- `reports.view`, `reports.sales`, `reports.inventory`, `reports.financial`
- `reports.export`, `reports.schedule`, `reports.custom`, `reports.dashboard`

**Settings (8)**
- `settings.view`, `settings.update`, `settings.company`, `settings.tax`
- `settings.notifications`, `settings.backup`, `settings.restore`, `settings.system`

**Users (8)**
- `users.view`, `users.create`, `users.update`, `users.delete`
- `users.roles`, `users.permissions`, `users.2fa`, `users.audit`

---

## Security Headers

```
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

---

## Rate Limiting

| Endpoint | Limit |
|----------|-------|
| `/api/auth/login` | 5/minute |
| `/api/auth/2fa` | 3/minute |
| `/api/*` | 100/second |

---

## Audit Logging

Every sensitive action is logged:
- User login/logout
- CRUD operations
- Permission changes
- Settings changes
- Failed attempts

Log format:
```json
{
  "timestamp": "2026-01-16T12:00:00Z",
  "user_id": 1,
  "action": "user.login",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "details": {}
}
```

---

## Implementation Status

- ✅ JWT Authentication
- ✅ Token Refresh
- ✅ 2FA (TOTP)
- ✅ RBAC (68 permissions)
- ✅ Security Headers
- ✅ Rate Limiting
- ✅ Audit Logging
- ✅ Input Validation
- ✅ SQL Injection Prevention
- ✅ XSS Prevention
