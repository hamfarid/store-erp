# Import/Export Map

> **Purpose:** Track all imports and exports across the project to understand dependencies and prevent circular imports.

**Last Updated:** 2025-01-16
**Project:** Store Management System

---

## How to Use This File

1. **When creating a new file:** Document its exports
2. **When importing:** Check this map to avoid circular dependencies
3. **When refactoring:** Update this map to reflect changes
4. **Before committing:** Verify this map is up to date

---

## Project Structure

```
store/
├── backend/
│   ├── src/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utility functions
│   │   └── decorators/      # Custom decorators
│   ├── app.py               # Application entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── services/        # API services
│   │   ├── hooks/           # Custom hooks
│   │   └── contexts/        # React contexts
│   ├── App.jsx              # Application root
│   └── package.json
└── docs/
```

---

## Backend Core Files

### backend/app.py
**Purpose:** Main Flask application entry point

**Exports:**
- `app` (Flask) - Main Flask application instance
- `create_app()` (function) - Application factory

**Imports:**
```python
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.src.routes import register_blueprints
from backend.src.models import db
```

**Dependencies:**
- backend/src/routes/__init__.py
- backend/src/models/__init__.py

**Imported By:**
- tests/conftest.py
- wsgi.py

---

### backend/src/models/__init__.py
**Purpose:** Models package initialization

**Exports:**
- `db` (SQLAlchemy) - Database instance
- `User` - User model
- `Product` - Product model
- `ProductAdvanced` - Advanced product with lots
- `BatchAdvanced` - Batch/Lot model
- `Invoice` - Invoice model
- `Sale` - Sale model

**Imports:**
```python
from flask_sqlalchemy import SQLAlchemy
from backend.src.models.user import User
from backend.src.models.product import Product, ProductAdvanced
from backend.src.models.batch import BatchAdvanced
from backend.src.models.invoice import Invoice
from backend.src.models.sale import Sale
```

**Imported By:**
- backend/app.py
- backend/src/routes/*.py
- backend/src/services/*.py

---

## Backend Routes

### backend/src/routes/__init__.py
**Purpose:** Routes package and blueprint registration

**Exports:**
- `register_blueprints(app)` - Function to register all blueprints

**Imports:**
```python
from backend.src.routes.auth import auth_bp
from backend.src.routes.users import users_bp
from backend.src.routes.products import products_bp
from backend.src.routes.invoices import invoices_bp
from backend.src.routes.reports import reports_bp
```

**Imported By:**
- backend/app.py

---

### backend/src/routes/auth.py
**Purpose:** Authentication endpoints

**Exports:**
- `auth_bp` (Blueprint) - Authentication blueprint

**Endpoints:**
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Token refresh
- `POST /api/auth/logout` - User logout

**Imports:**
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from backend.src.models import User, db
from backend.src.utils.validators import validate_user_data
```

---

### backend/src/routes/products.py
**Purpose:** Product management endpoints

**Exports:**
- `products_bp` (Blueprint) - Products blueprint

**Endpoints:**
- `GET /api/products` - List products
- `GET /api/products/<id>` - Get product
- `POST /api/products` - Create product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

**Imports:**
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.src.models import Product, ProductAdvanced, db
from backend.src.decorators.permissions import require_permission
```

---

## Backend Services

### backend/src/services/auth_service.py
**Purpose:** Authentication business logic

**Exports:**
- `AuthService` (class) - Authentication service

**Methods:**
- `login(email, password)` - Authenticate user
- `register(data)` - Create new user
- `generate_tokens(user)` - Generate JWT tokens
- `verify_token(token)` - Verify JWT token

**Imports:**
```python
from backend.src.models import User, db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
```

---

## Frontend Core Files

### frontend/src/App.jsx
**Purpose:** Main React application root

**Exports:**
- `App` (component) - Root component (default export)

**Imports:**
```javascript
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import AppRouter from './AppRouter';
```

**Imported By:**
- frontend/src/main.jsx

---

### frontend/src/services/api.js
**Purpose:** API client configuration

**Exports:**
- `api` (axios instance) - Configured axios client
- `authAPI` - Authentication API methods
- `productsAPI` - Products API methods
- `invoicesAPI` - Invoices API methods

**Imports:**
```javascript
import axios from 'axios';
import { API_BASE_URL } from '../config/constants';
```

**Imported By:**
- frontend/src/pages/*.jsx
- frontend/src/contexts/AuthContext.jsx

---

### frontend/src/contexts/AuthContext.jsx
**Purpose:** Authentication state management

**Exports:**
- `AuthProvider` (component) - Auth context provider
- `useAuth` (hook) - Auth context hook

**State:**
- `user` - Current user object
- `token` - JWT access token
- `isAuthenticated` - Boolean auth status

**Methods:**
- `login(email, password)` - Login user
- `logout()` - Logout user
- `register(data)` - Register user

**Imports:**
```javascript
import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';
```

**Imported By:**
- frontend/src/App.jsx
- frontend/src/pages/*.jsx (via useAuth hook)

---

## Dependency Graph

```
Backend:
app.py
├── src/models/__init__.py
│   ├── user.py
│   ├── product.py
│   ├── batch.py
│   └── invoice.py
├── src/routes/__init__.py
│   ├── auth.py → models, services
│   ├── products.py → models, decorators
│   └── invoices.py → models, decorators
├── src/services/
│   ├── auth_service.py → models
│   └── product_service.py → models
└── src/utils/ (leaf modules)
    ├── validators.py
    └── helpers.py

Frontend:
main.jsx
└── App.jsx
    ├── contexts/AuthContext.jsx → services/api
    ├── contexts/ThemeContext.jsx
    └── AppRouter.jsx
        └── pages/*.jsx → contexts, services, components
```

---

## Import Rules

### ✅ Allowed Imports

**Routes can import:**
- Models
- Services
- Utils
- Decorators

**Services can import:**
- Models
- Utils (validators, helpers)

**Models can import:**
- Database only (SQLAlchemy)

### ❌ Forbidden Imports

**Models CANNOT import:**
- Routes
- Services

**Services CANNOT import:**
- Routes

---

## Port Configuration

| Service | Port | Purpose |
|---------|------|---------|
| Backend | 6001 | Flask API |
| Frontend | 6501 | React Dev/Build |
| ML Service | 6101 | ML/AI Endpoints |
| AI Service | 6601 | AI Chatbot |

---

## Notes

- Keep this map updated when imports change
- Check for circular dependencies regularly
- Use absolute imports for clarity

