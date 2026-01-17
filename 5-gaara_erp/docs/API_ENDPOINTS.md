# Gaara ERP API Endpoints Documentation

**Generated**: 2025-12-01
**Base URL**: `/api/v1/`
**Authentication**: JWT Bearer Token
**Total URL Files**: 79

---

## Authentication

### Auth Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | User login, returns JWT tokens |
| POST | `/api/auth/logout/` | User logout, blacklist refresh token |
| POST | `/api/auth/refresh/` | Refresh access token |
| POST | `/api/auth/register/` | New user registration |
| GET | `/api/auth/me/` | Get current user info |

### Security Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/security/login/` | Secure login with lockout protection |
| POST | `/api/security/change-password/` | Change user password |
| GET | `/api/security/audit-logs/` | View audit logs |
| GET | `/api/security/events/` | Security events list |

---

## Core Modules

### Users (`/api/users/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List all users |
| POST | `/api/users/` | Create new user |
| GET | `/api/users/{id}/` | Get user details |
| PUT | `/api/users/{id}/` | Update user |
| DELETE | `/api/users/{id}/` | Delete user |

### Companies (`/api/companies/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/companies/` | List all companies |
| POST | `/api/companies/` | Create new company |
| GET | `/api/companies/{id}/` | Get company details |
| GET | `/api/companies/{id}/branches/` | Get company branches |

### Organizations (`/api/organization/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/organization/branches/` | List branches |
| GET | `/api/organization/departments/` | List departments |
| POST | `/api/organization/branches/` | Create branch |
| POST | `/api/organization/departments/` | Create department |

### Permissions (`/api/permissions/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/permissions/` | List all permissions |
| GET | `/api/permissions/roles/` | List all roles |
| POST | `/api/permissions/roles/` | Create role |
| GET | `/api/permissions/user-permissions/` | Get user permissions |

---

## Business Modules

### Accounting (`/api/accounting/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounting/accounts/` | Chart of accounts |
| POST | `/api/accounting/accounts/` | Create account |
| GET | `/api/accounting/journal-entries/` | Journal entries |
| POST | `/api/accounting/journal-entries/` | Create journal entry |
| GET | `/api/accounting/invoices/` | List invoices |
| POST | `/api/accounting/invoices/` | Create invoice |
| GET | `/api/accounting/fiscal-years/` | Fiscal years |
| GET | `/api/accounting/reports/trial-balance/` | Trial balance report |
| GET | `/api/accounting/reports/profit-loss/` | P&L report |
| GET | `/api/accounting/reports/balance-sheet/` | Balance sheet |

### Inventory (`/api/inventory/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/inventory/products/` | List products |
| POST | `/api/inventory/products/` | Create product |
| GET | `/api/inventory/products/{id}/` | Product details |
| GET | `/api/inventory/warehouses/` | List warehouses |
| GET | `/api/inventory/stock-levels/` | Stock levels |
| POST | `/api/inventory/stock-movements/` | Create stock movement |
| GET | `/api/inventory/categories/` | Product categories |

### Sales (`/api/sales/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sales/orders/` | List sales orders |
| POST | `/api/sales/orders/` | Create sales order |
| GET | `/api/sales/customers/` | List customers |
| POST | `/api/sales/customers/` | Create customer |
| GET | `/api/sales/quotes/` | List quotations |

### Purchasing (`/api/purchasing/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/purchasing/orders/` | Purchase orders |
| POST | `/api/purchasing/orders/` | Create PO |
| GET | `/api/purchasing/suppliers/` | List suppliers |
| POST | `/api/purchasing/suppliers/` | Create supplier |
| GET | `/api/purchasing/requisitions/` | Purchase requisitions |

### Contacts (`/api/contacts/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/contacts/` | List all contacts |
| POST | `/api/contacts/` | Create contact |
| GET | `/api/contacts/leads/` | List leads |
| GET | `/api/contacts/opportunities/` | List opportunities |
| GET | `/api/contacts/campaigns/` | Marketing campaigns |

### POS (`/api/pos/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/pos/sessions/` | POS sessions |
| POST | `/api/pos/sessions/open/` | Open POS session |
| POST | `/api/pos/sessions/close/` | Close POS session |
| POST | `/api/pos/orders/` | Create POS order |
| GET | `/api/pos/payments/` | Payment methods |

---

## Services Modules

### Projects (`/api/projects/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | List projects |
| POST | `/api/projects/` | Create project |
| GET | `/api/projects/{id}/tasks/` | Project tasks |
| POST | `/api/projects/{id}/tasks/` | Create task |

### HR (`/api/hr/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/hr/employees/` | List employees |
| POST | `/api/hr/employees/` | Create employee |
| GET | `/api/hr/departments/` | HR departments |
| GET | `/api/hr/payroll/` | Payroll entries |
| GET | `/api/hr/attendance/` | Attendance records |
| GET | `/api/hr/leaves/` | Leave requests |

### Documents (`/api/documents/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/documents/` | List documents |
| POST | `/api/documents/upload/` | Upload document |
| GET | `/api/documents/{id}/download/` | Download document |

---

## Admin Modules

### System Settings (`/api/settings/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/settings/` | Get system settings |
| PUT | `/api/settings/` | Update settings |
| GET | `/api/settings/preferences/` | User preferences |

### Backups (`/api/backups/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/backups/` | List backups |
| POST | `/api/backups/create/` | Create backup |
| POST | `/api/backups/{id}/restore/` | Restore backup |
| GET | `/api/backups/schedules/` | Backup schedules |

### Notifications (`/api/notifications/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | User notifications |
| PUT | `/api/notifications/{id}/read/` | Mark as read |
| POST | `/api/notifications/send/` | Send notification |

### Health Monitoring (`/api/health/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Basic health check |
| GET | `/api/health/detailed/` | Detailed health status |
| GET | `/api/health/metrics/` | System metrics |

---

## AI Modules

### RAG (`/api/rag/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/rag/ingest/` | Ingest document |
| POST | `/api/rag/search/` | Search documents |
| GET | `/api/rag/documents/` | List documents |
| GET | `/api/rag/chunks/` | List chunks |

### Memory (`/api/memory/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/memory/create/` | Create memory |
| GET | `/api/memory/search/` | Search memories |
| DELETE | `/api/memory/delete/` | Delete memory |

### AI Assistant (`/api/ai/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/chat/` | Chat with AI |
| GET | `/api/ai/history/` | Chat history |
| GET | `/api/ai/agents/` | List AI agents |

---

## Response Format

### Success Response
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": { ... }
  }
}
```

### Paginated Response
```json
{
  "count": 100,
  "next": "http://api/endpoint/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## Authentication Headers

```
Authorization: Bearer <access_token>
Content-Type: application/json
Accept: application/json
Accept-Language: ar  # or en
```

---

## Rate Limiting

| Endpoint Type | Limit |
|--------------|-------|
| Authentication | 5 requests/5 minutes |
| RAG Search | 100 requests/hour |
| General API | 1000 requests/hour |
| Admin API | 500 requests/hour |

---

## API Versioning

- Current Version: v1
- URL Format: `/api/v1/`
- Header: `Accept: application/vnd.gaara-erp.v1+json`

---

**Last Updated**: 2025-12-01

