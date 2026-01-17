# Import/Export Map

> **Purpose:** Track all imports and exports across the project to understand dependencies and prevent circular imports.

**Last Updated:** [DATE]  
**Project:** {{PROJECT_NAME}}

---

## How to Use This File

1. **When creating a new file:** Document its exports
2. **When importing:** Check this map to avoid circular dependencies
3. **When refactoring:** Update this map to reflect changes
4. **Before committing:** Verify this map is up to date

---

## Project Structure

```
{{PROJECT_NAME}}/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── products.py
│   │   └── orders.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── order_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── decorators.py
│   ├── config.py
│   ├── database.py
│   └── app.py
├── tests/
└── docs/
```

---

## Core Files

### src/app.py
**Purpose:** Main application entry point

**Exports:**
- `app` (Flask) - Main Flask application instance
- `create_app()` (function) - Application factory

**Imports:**
```python
from flask import Flask
from src.config import Config
from src.database import db
from src.api import users_bp, products_bp, orders_bp
```

**Dependencies:**
- src/config.py
- src/database.py
- src/api/__init__.py

**Imported By:**
- tests/conftest.py
- run.py

---

### src/config.py
**Purpose:** Application configuration

**Exports:**
- `Config` (class) - Base configuration
- `DevelopmentConfig` (class) - Development configuration
- `ProductionConfig` (class) - Production configuration
- `TestingConfig` (class) - Testing configuration

**Imports:**
```python
import os
from dotenv import load_dotenv
```

**Dependencies:**
- None (no internal dependencies)

**Imported By:**
- src/app.py
- tests/conftest.py

**Notes:**
- This is a leaf module (no internal imports)
- Safe to import from anywhere

---

### src/database.py
**Purpose:** Database connection and session management

**Exports:**
- `db` (SQLAlchemy) - Database instance
- `init_db()` (function) - Initialize database
- `get_session()` (function) - Get database session

**Imports:**
```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
```

**Dependencies:**
- None (no internal dependencies)

**Imported By:**
- src/app.py
- src/models/*.py
- src/services/*.py

**Notes:**
- This is a leaf module (no internal imports)
- Safe to import from anywhere

---

## Models Layer

### src/models/__init__.py
**Purpose:** Models package initialization

**Exports:**
- `User` (class) - Re-exported from user.py
- `Product` (class) - Re-exported from product.py
- `Order` (class) - Re-exported from order.py
- `OrderItem` (class) - Re-exported from order.py

**Imports:**
```python
from src.models.user import User
from src.models.product import Product
from src.models.order import Order, OrderItem
```

**Dependencies:**
- src/models/user.py
- src/models/product.py
- src/models/order.py

**Imported By:**
- src/api/*.py
- src/services/*.py
- tests/*.py

---

### src/models/user.py
**Purpose:** User model

**Exports:**
- `User` (class) - User model with authentication

**Imports:**
```python
from src.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
```

**Dependencies:**
- src/database.py

**Imported By:**
- src/models/__init__.py
- src/models/order.py (for foreign key)

**Relationships:**
- Has many: Order

**Methods:**
- `set_password(password)` - Hash and set password
- `check_password(password)` - Verify password
- `to_dict()` - Convert to dictionary
- `from_dict(data)` - Create from dictionary

---

### src/models/product.py
**Purpose:** Product model

**Exports:**
- `Product` (class) - Product model

**Imports:**
```python
from src.database import db
from datetime import datetime
```

**Dependencies:**
- src/database.py

**Imported By:**
- src/models/__init__.py
- src/models/order.py (for foreign key)

**Relationships:**
- Has many: OrderItem

**Methods:**
- `to_dict()` - Convert to dictionary
- `from_dict(data)` - Create from dictionary

---

### src/models/order.py
**Purpose:** Order and OrderItem models

**Exports:**
- `Order` (class) - Order model
- `OrderItem` (class) - Order item model

**Imports:**
```python
from src.database import db
from src.models.user import User
from src.models.product import Product
from datetime import datetime
```

**Dependencies:**
- src/database.py
- src/models/user.py
- src/models/product.py

**Imported By:**
- src/models/__init__.py

**Relationships:**
- Order belongs to: User
- Order has many: OrderItem
- OrderItem belongs to: Order
- OrderItem belongs to: Product

**Methods:**
- `calculate_total()` - Calculate order total
- `to_dict()` - Convert to dictionary
- `from_dict(data)` - Create from dictionary

---

## Services Layer

### src/services/__init__.py
**Purpose:** Services package initialization

**Exports:**
- `AuthService` (class) - Re-exported from auth_service.py
- `UserService` (class) - Re-exported from user_service.py
- `OrderService` (class) - Re-exported from order_service.py

**Imports:**
```python
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.services.order_service import OrderService
```

**Dependencies:**
- src/services/auth_service.py
- src/services/user_service.py
- src/services/order_service.py

**Imported By:**
- src/api/*.py

---

### src/services/auth_service.py
**Purpose:** Authentication service

**Exports:**
- `AuthService` (class) - Authentication logic

**Imports:**
```python
from src.models import User
from src.database import db
import jwt
from datetime import datetime, timedelta
from flask import current_app
```

**Dependencies:**
- src/models/__init__.py
- src/database.py

**Imported By:**
- src/services/__init__.py
- src/api/users.py

**Methods:**
- `register(email, password, name)` - Register new user
- `login(email, password)` - Authenticate user
- `generate_token(user_id)` - Generate JWT token
- `verify_token(token)` - Verify JWT token
- `refresh_token(refresh_token)` - Refresh JWT token

---

### src/services/user_service.py
**Purpose:** User business logic

**Exports:**
- `UserService` (class) - User operations

**Imports:**
```python
from src.models import User
from src.database import db
from sqlalchemy import or_
```

**Dependencies:**
- src/models/__init__.py
- src/database.py

**Imported By:**
- src/services/__init__.py
- src/api/users.py

**Methods:**
- `get_all(page, per_page)` - Get paginated users
- `get_by_id(user_id)` - Get user by ID
- `create(data)` - Create new user
- `update(user_id, data)` - Update user
- `delete(user_id)` - Delete user
- `search(query)` - Search users

---

### src/services/order_service.py
**Purpose:** Order business logic

**Exports:**
- `OrderService` (class) - Order operations

**Imports:**
```python
from src.models import Order, OrderItem, Product, User
from src.database import db
from sqlalchemy.orm import joinedload
```

**Dependencies:**
- src/models/__init__.py
- src/database.py

**Imported By:**
- src/services/__init__.py
- src/api/orders.py

**Methods:**
- `get_all(page, per_page)` - Get paginated orders
- `get_by_id(order_id)` - Get order by ID
- `get_by_user(user_id)` - Get user's orders
- `create(user_id, items)` - Create new order
- `update_status(order_id, status)` - Update order status
- `cancel(order_id)` - Cancel order

**Notes:**
- Uses joinedload to prevent N+1 queries
- Validates product availability before creating order

---

## API Layer

### src/api/__init__.py
**Purpose:** API package initialization and blueprint registration

**Exports:**
- `users_bp` (Blueprint) - Re-exported from users.py
- `products_bp` (Blueprint) - Re-exported from products.py
- `orders_bp` (Blueprint) - Re-exported from orders.py

**Imports:**
```python
from src.api.users import users_bp
from src.api.products import products_bp
from src.api.orders import orders_bp
```

**Dependencies:**
- src/api/users.py
- src/api/products.py
- src/api/orders.py

**Imported By:**
- src/app.py

---

### src/api/users.py
**Purpose:** User API endpoints

**Exports:**
- `users_bp` (Blueprint) - Users blueprint

**Imports:**
```python
from flask import Blueprint, request, jsonify
from src.services import AuthService, UserService
from src.utils.decorators import token_required, admin_required
from src.utils.validators import validate_user_data
```

**Dependencies:**
- src/services/__init__.py
- src/utils/decorators.py
- src/utils/validators.py

**Imported By:**
- src/api/__init__.py

**Endpoints:**
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login user
- `POST /api/users/refresh` - Refresh token
- `GET /api/users` - Get all users (admin only)
- `GET /api/users/<id>` - Get user by ID
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user (admin only)

---

### src/api/products.py
**Purpose:** Product API endpoints

**Exports:**
- `products_bp` (Blueprint) - Products blueprint

**Imports:**
```python
from flask import Blueprint, request, jsonify
from src.services import ProductService
from src.utils.decorators import token_required, admin_required
from src.utils.validators import validate_product_data
```

**Dependencies:**
- src/services/__init__.py
- src/utils/decorators.py
- src/utils/validators.py

**Imported By:**
- src/api/__init__.py

**Endpoints:**
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get product by ID
- `POST /api/products` - Create product (admin only)
- `PUT /api/products/<id>` - Update product (admin only)
- `DELETE /api/products/<id>` - Delete product (admin only)

---

### src/api/orders.py
**Purpose:** Order API endpoints

**Exports:**
- `orders_bp` (Blueprint) - Orders blueprint

**Imports:**
```python
from flask import Blueprint, request, jsonify
from src.services import OrderService
from src.utils.decorators import token_required
from src.utils.validators import validate_order_data
```

**Dependencies:**
- src/services/__init__.py
- src/utils/decorators.py
- src/utils/validators.py

**Imported By:**
- src/api/__init__.py

**Endpoints:**
- `GET /api/orders` - Get user's orders
- `GET /api/orders/<id>` - Get order by ID
- `POST /api/orders` - Create order
- `PUT /api/orders/<id>/status` - Update order status
- `DELETE /api/orders/<id>` - Cancel order

---

## Utils Layer

### src/utils/__init__.py
**Purpose:** Utils package initialization

**Exports:**
- All validators from validators.py
- All helpers from helpers.py
- All decorators from decorators.py

**Imports:**
```python
from src.utils.validators import *
from src.utils.helpers import *
from src.utils.decorators import *
```

**Dependencies:**
- src/utils/validators.py
- src/utils/helpers.py
- src/utils/decorators.py

**Imported By:**
- src/api/*.py
- src/services/*.py

---

### src/utils/validators.py
**Purpose:** Input validation functions

**Exports:**
- `validate_user_data(data)` (function) - Validate user data
- `validate_product_data(data)` (function) - Validate product data
- `validate_order_data(data)` (function) - Validate order data
- `validate_email(email)` (function) - Validate email format
- `validate_password(password)` (function) - Validate password strength

**Imports:**
```python
import re
from flask import abort
```

**Dependencies:**
- None (no internal dependencies)

**Imported By:**
- src/utils/__init__.py
- src/api/*.py

**Notes:**
- This is a leaf module (no internal imports)
- Safe to import from anywhere

---

### src/utils/helpers.py
**Purpose:** Helper utility functions

**Exports:**
- `format_response(data, message, status)` (function) - Format API response
- `handle_error(error)` (function) - Handle errors
- `paginate(query, page, per_page)` (function) - Paginate query results
- `generate_slug(text)` (function) - Generate URL slug

**Imports:**
```python
from flask import jsonify
import re
```

**Dependencies:**
- None (no internal dependencies)

**Imported By:**
- src/utils/__init__.py
- src/api/*.py
- src/services/*.py

**Notes:**
- This is a leaf module (no internal imports)
- Safe to import from anywhere

---

### src/utils/decorators.py
**Purpose:** Custom decorators

**Exports:**
- `token_required` (decorator) - Require valid JWT token
- `admin_required` (decorator) - Require admin role
- `rate_limit` (decorator) - Rate limiting

**Imports:**
```python
from functools import wraps
from flask import request, jsonify
from src.services import AuthService
```

**Dependencies:**
- src/services/__init__.py

**Imported By:**
- src/utils/__init__.py
- src/api/*.py

**Notes:**
- Depends on AuthService for token verification
- Should not be imported by services layer (circular dependency risk)

---

## Dependency Graph

```
app.py
├── config.py (leaf)
├── database.py (leaf)
└── api/
    ├── users.py
    │   ├── services/
    │   │   ├── auth_service.py
    │   │   │   └── models/
    │   │   └── user_service.py
    │   │       └── models/
    │   └── utils/
    │       ├── validators.py (leaf)
    │       ├── helpers.py (leaf)
    │       └── decorators.py
    │           └── services/auth_service.py
    ├── products.py
    │   ├── services/product_service.py
    │   │   └── models/
    │   └── utils/
    └── orders.py
        ├── services/order_service.py
        │   └── models/
        └── utils/
```

---

## Circular Dependency Risks

### ⚠️ Risk 1: Decorators ↔ Services
**Problem:** 
- `decorators.py` imports `AuthService`
- If `AuthService` imports decorators → circular dependency

**Solution:**
- Services should NOT import decorators
- Only API layer should use decorators

**Status:** ✅ Safe (services don't import decorators)

---

### ⚠️ Risk 2: Models ↔ Services
**Problem:**
- Models might need service logic
- Services import models

**Solution:**
- Keep models simple (data + basic methods only)
- All business logic in services
- Models should NOT import services

**Status:** ✅ Safe (models don't import services)

---

### ⚠️ Risk 3: API ↔ Services
**Problem:**
- API imports services
- Services might need to call API (webhooks, etc.)

**Solution:**
- Services should NOT import API
- Use events/signals for service-to-API communication
- Keep API as the top layer

**Status:** ✅ Safe (services don't import API)

---

## Import Rules

### ✅ Allowed Imports

**API Layer can import:**
- Services
- Utils
- Models (for type hints only)

**Services Layer can import:**
- Models
- Database
- Utils (validators, helpers only - NOT decorators)

**Models Layer can import:**
- Database only

**Utils Layer can import:**
- Services (only for decorators)
- Nothing else (validators and helpers are leaf modules)

### ❌ Forbidden Imports

**Models CANNOT import:**
- Services
- API
- Utils (except database)

**Services CANNOT import:**
- API
- Utils/decorators

**Utils/validators CANNOT import:**
- Anything internal

**Utils/helpers CANNOT import:**
- Anything internal

---

## Import Best Practices

1. **Import from package __init__.py when possible**
   ```python
   # ✅ Good
   from src.models import User, Product
   
   # ❌ Bad
   from src.models.user import User
   from src.models.product import Product
   ```

2. **Use absolute imports, not relative**
   ```python
   # ✅ Good
   from src.models import User
   
   # ❌ Bad
   from ..models import User
   ```

3. **Import only what you need**
   ```python
   # ✅ Good
   from src.models import User
   
   # ❌ Bad
   from src.models import *
   ```

4. **Group imports logically**
   ```python
   # Standard library
   import os
   from datetime import datetime
   
   # Third-party
   from flask import Flask
   from sqlalchemy import Column
   
   # Local
   from src.models import User
   from src.database import db
   ```

5. **Check this map before adding new imports**

---

## Update Checklist

When adding a new file:
- [ ] Document its exports
- [ ] Document its imports
- [ ] Document its dependencies
- [ ] Check for circular dependencies
- [ ] Update dependency graph
- [ ] Update this map

When refactoring:
- [ ] Update affected sections
- [ ] Check for new circular dependency risks
- [ ] Update dependency graph
- [ ] Verify import rules still hold

---

## Notes

- This map should be updated whenever imports change
- Review this map before major refactoring
- Use this map to onboard new developers
- Keep dependency graph up to date
- Check for circular dependencies regularly

