# FILE: docs/Symbol_Index.md | PURPOSE: Index of classes/functions/constants | OWNER: Architecture | RELATED: docs/Imports_Map.md, docs/Class_Registry.md | LAST-AUDITED: 2025-10-21

# Symbol Index — فهرس الرموز

Version: 1.0  
Last Updated: 2025-10-21

—

## 1. Models (src/models)

- User — src/models/user_unified.py:class User
- Role — src/models/user_unified.py:class Role
- Product — src/models/product_unified.py:class Product
- Invoice — src/models/invoice_unified.py:class Invoice
- InvoiceItem — src/models/invoice_unified.py:class InvoiceItem
- Payment — src/models/supporting_models.py:class Payment
- StockMovement — src/models/supporting_models.py:class StockMovement
- AuditLog — src/models/supporting_models.py:class AuditLog

## 2. Routes (src/routes)

- auth — src/routes/auth_unified.py:Blueprint auth_bp
- products — src/routes/products.py:Blueprint products_bp
- invoices — src/routes/invoices.py:Blueprint invoices_bp
- users — src/routes/users.py:Blueprint users_bp

## 3. Database (src/database)

- db — src/database/db.py:SQLAlchemy instance
- init_db — src/database/init.py:function init_db

## 4. Utils (src/utils)

- security — src/utils/security.py:function hash_password, verify_password
- logging — src/utils/logging.py:function get_logger
- errors — src/utils/errors.py:function error_response

## 5. Frontend (frontend/src)

- Router — frontend/src/router/index.jsx:function AppRouter
- AuthProvider — frontend/src/context/AuthProvider.jsx:function AuthProvider
- API client — frontend/src/api/index.js:function apiFetch

—

Note: Keep this index updated as part of PR review checklist.
