# Class Registry - Complete Reference

> **Purpose:** Complete registry of all classes, functions, and their purposes across the project.

**Last Updated:** [DATE]  
**Project:** {{PROJECT_NAME}}

---

## How to Use This File

1. **When creating a class/function:** Add it to this registry
2. **When looking for functionality:** Search this file first
3. **When refactoring:** Update this registry
4. **Before implementing:** Check if functionality already exists

---

## Quick Index

- [Models](#models) - Database models
- [Services](#services) - Business logic
- [API](#api) - API endpoints
- [Utils](#utils) - Utility functions
- [Middleware](#middleware) - Custom middleware
- [Decorators](#decorators) - Custom decorators

---

## Models

### User Model
**File:** `src/models/user.py`  
**Class:** `User`  
**Purpose:** User account and authentication

**Attributes:**
- `id` (Integer) - Primary key
- `email` (String) - Unique email address
- `password_hash` (String) - Hashed password
- `name` (String) - User's full name
- `role` (String) - User role (admin, user, guest)
- `is_active` (Boolean) - Account active status
- `created_at` (DateTime) - Account creation time
- `updated_at` (DateTime) - Last update time

**Relationships:**
- `orders` (One-to-Many) - User's orders

**Methods:**
```python
set_password(password: str) -> None
    """Hash and set user password"""
    
check_password(password: str) -> bool
    """Verify password against hash"""
    
to_dict() -> dict
    """Convert user to dictionary (excludes password)"""
    
from_dict(data: dict) -> User
    """Create user from dictionary"""
    
is_admin() -> bool
    """Check if user is admin"""
```

**Usage Example:**
```python
from src.models import User

# Create user
user = User(email="user@example.com", name="John Doe")
user.set_password("secure_password")

# Check password
if user.check_password("secure_password"):
    print("Password correct")

# Convert to dict
user_data = user.to_dict()
```

---

### Product Model
**File:** `src/models/product.py`  
**Class:** `Product`  
**Purpose:** Product catalog

**Attributes:**
- `id` (Integer) - Primary key
- `name` (String) - Product name
- `description` (Text) - Product description
- `price` (Decimal) - Product price
- `stock` (Integer) - Available quantity
- `category` (String) - Product category
- `is_active` (Boolean) - Product active status
- `created_at` (DateTime) - Creation time
- `updated_at` (DateTime) - Last update time

**Relationships:**
- `order_items` (One-to-Many) - Order items containing this product

**Methods:**
```python
to_dict() -> dict
    """Convert product to dictionary"""
    
from_dict(data: dict) -> Product
    """Create product from dictionary"""
    
is_available(quantity: int = 1) -> bool
    """Check if product has sufficient stock"""
    
reduce_stock(quantity: int) -> None
    """Reduce stock by quantity (with validation)"""
    
increase_stock(quantity: int) -> None
    """Increase stock by quantity"""
```

**Usage Example:**
```python
from src.models import Product

# Create product
product = Product(
    name="Laptop",
    description="High-performance laptop",
    price=999.99,
    stock=10
)

# Check availability
if product.is_available(2):
    product.reduce_stock(2)
```

---

### Order Model
**File:** `src/models/order.py`  
**Class:** `Order`  
**Purpose:** Customer orders

**Attributes:**
- `id` (Integer) - Primary key
- `user_id` (Integer) - Foreign key to User
- `status` (String) - Order status (pending, confirmed, shipped, delivered, cancelled)
- `total` (Decimal) - Order total amount
- `created_at` (DateTime) - Order creation time
- `updated_at` (DateTime) - Last update time

**Relationships:**
- `user` (Many-to-One) - Order owner
- `items` (One-to-Many) - Order items

**Methods:**
```python
calculate_total() -> Decimal
    """Calculate total from order items"""
    
to_dict() -> dict
    """Convert order to dictionary (includes items)"""
    
from_dict(data: dict, user_id: int) -> Order
    """Create order from dictionary"""
    
can_cancel() -> bool
    """Check if order can be cancelled"""
    
cancel() -> None
    """Cancel order and restore stock"""
```

**Usage Example:**
```python
from src.models import Order, OrderItem

# Create order
order = Order(user_id=1, status="pending")

# Add items
item1 = OrderItem(product_id=1, quantity=2, price=999.99)
order.items.append(item1)

# Calculate total
order.calculate_total()
```

---

### OrderItem Model
**File:** `src/models/order.py`  
**Class:** `OrderItem`  
**Purpose:** Individual items in an order

**Attributes:**
- `id` (Integer) - Primary key
- `order_id` (Integer) - Foreign key to Order
- `product_id` (Integer) - Foreign key to Product
- `quantity` (Integer) - Quantity ordered
- `price` (Decimal) - Price at time of order

**Relationships:**
- `order` (Many-to-One) - Parent order
- `product` (Many-to-One) - Product ordered

**Methods:**
```python
get_subtotal() -> Decimal
    """Calculate subtotal (quantity * price)"""
    
to_dict() -> dict
    """Convert to dictionary"""
```

---

## Services

### AuthService
**File:** `src/services/auth_service.py`  
**Class:** `AuthService`  
**Purpose:** Authentication and token management

**Methods:**
```python
register(email: str, password: str, name: str) -> User
    """
    Register new user
    
    Args:
        email: User email (must be unique)
        password: Plain text password (will be hashed)
        name: User's full name
        
    Returns:
        User: Created user object
        
    Raises:
        ValueError: If email already exists
        ValueError: If password is weak
    """

login(email: str, password: str) -> dict
    """
    Authenticate user and generate tokens
    
    Args:
        email: User email
        password: Plain text password
        
    Returns:
        dict: {
            "access_token": str,
            "refresh_token": str,
            "user": dict
        }
        
    Raises:
        ValueError: If credentials invalid
    """

generate_token(user_id: int, token_type: str = "access") -> str
    """
    Generate JWT token
    
    Args:
        user_id: User ID
        token_type: "access" or "refresh"
        
    Returns:
        str: JWT token
    """

verify_token(token: str) -> int
    """
    Verify JWT token and extract user ID
    
    Args:
        token: JWT token
        
    Returns:
        int: User ID
        
    Raises:
        ValueError: If token invalid or expired
    """

refresh_token(refresh_token: str) -> dict
    """
    Generate new access token from refresh token
    
    Args:
        refresh_token: Valid refresh token
        
    Returns:
        dict: {"access_token": str}
        
    Raises:
        ValueError: If refresh token invalid
    """
```

**Usage Example:**
```python
from src.services import AuthService

auth = AuthService()

# Register
user = auth.register("user@example.com", "password123", "John Doe")

# Login
tokens = auth.login("user@example.com", "password123")
access_token = tokens["access_token"]

# Verify token
user_id = auth.verify_token(access_token)
```

---

### UserService
**File:** `src/services/user_service.py`  
**Class:** `UserService`  
**Purpose:** User management operations

**Methods:**
```python
get_all(page: int = 1, per_page: int = 20) -> dict
    """
    Get paginated list of users
    
    Args:
        page: Page number (1-indexed)
        per_page: Items per page
        
    Returns:
        dict: {
            "users": [User],
            "total": int,
            "page": int,
            "per_page": int,
            "pages": int
        }
    """

get_by_id(user_id: int) -> User
    """
    Get user by ID
    
    Args:
        user_id: User ID
        
    Returns:
        User: User object
        
    Raises:
        ValueError: If user not found
    """

create(data: dict) -> User
    """
    Create new user
    
    Args:
        data: User data dictionary
        
    Returns:
        User: Created user
        
    Raises:
        ValueError: If validation fails
    """

update(user_id: int, data: dict) -> User
    """
    Update user
    
    Args:
        user_id: User ID
        data: Updated data
        
    Returns:
        User: Updated user
        
    Raises:
        ValueError: If user not found or validation fails
    """

delete(user_id: int) -> None
    """
    Delete user (soft delete)
    
    Args:
        user_id: User ID
        
    Raises:
        ValueError: If user not found
    """

search(query: str, page: int = 1, per_page: int = 20) -> dict
    """
    Search users by name or email
    
    Args:
        query: Search query
        page: Page number
        per_page: Items per page
        
    Returns:
        dict: Paginated search results
    """
```

**Usage Example:**
```python
from src.services import UserService

service = UserService()

# Get all users
result = service.get_all(page=1, per_page=20)
users = result["users"]

# Get specific user
user = service.get_by_id(1)

# Search users
results = service.search("john")
```

---

### OrderService
**File:** `src/services/order_service.py`  
**Class:** `OrderService`  
**Purpose:** Order management operations

**Methods:**
```python
get_all(page: int = 1, per_page: int = 20) -> dict
    """Get paginated list of all orders"""

get_by_id(order_id: int) -> Order
    """Get order by ID with items"""

get_by_user(user_id: int, page: int = 1, per_page: int = 20) -> dict
    """Get user's orders"""

create(user_id: int, items: list) -> Order
    """
    Create new order
    
    Args:
        user_id: User ID
        items: List of {product_id, quantity}
        
    Returns:
        Order: Created order
        
    Raises:
        ValueError: If product not available
        ValueError: If insufficient stock
    """

update_status(order_id: int, status: str) -> Order
    """
    Update order status
    
    Args:
        order_id: Order ID
        status: New status (pending, confirmed, shipped, delivered, cancelled)
        
    Returns:
        Order: Updated order
        
    Raises:
        ValueError: If invalid status transition
    """

cancel(order_id: int) -> Order
    """
    Cancel order and restore stock
    
    Args:
        order_id: Order ID
        
    Returns:
        Order: Cancelled order
        
    Raises:
        ValueError: If order cannot be cancelled
    """
```

**Usage Example:**
```python
from src.services import OrderService

service = OrderService()

# Create order
items = [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1}
]
order = service.create(user_id=1, items=items)

# Update status
service.update_status(order.id, "confirmed")

# Cancel order
service.cancel(order.id)
```

---

## Utils

### Validators
**File:** `src/utils/validators.py`

**Functions:**
```python
validate_user_data(data: dict) -> None
    """
    Validate user data
    
    Args:
        data: User data dictionary
        
    Raises:
        ValueError: If validation fails
        
    Checks:
        - Email format
        - Password strength
        - Required fields
    """

validate_product_data(data: dict) -> None
    """Validate product data"""

validate_order_data(data: dict) -> None
    """Validate order data"""

validate_email(email: str) -> bool
    """
    Validate email format
    
    Args:
        email: Email address
        
    Returns:
        bool: True if valid
    """

validate_password(password: str) -> bool
    """
    Validate password strength
    
    Args:
        password: Password string
        
    Returns:
        bool: True if strong enough
        
    Requirements:
        - At least 8 characters
        - At least one uppercase
        - At least one lowercase
        - At least one digit
        - At least one special character
    """
```

**Usage Example:**
```python
from src.utils.validators import validate_user_data, validate_email

# Validate user data
try:
    validate_user_data({
        "email": "user@example.com",
        "password": "SecurePass123!",
        "name": "John Doe"
    })
except ValueError as e:
    print(f"Validation error: {e}")

# Validate email
if validate_email("user@example.com"):
    print("Email is valid")
```

---

### Helpers
**File:** `src/utils/helpers.py`

**Functions:**
```python
format_response(data: any, message: str = "", status: int = 200) -> tuple
    """
    Format API response
    
    Args:
        data: Response data
        message: Optional message
        status: HTTP status code
        
    Returns:
        tuple: (response_dict, status_code)
    """

handle_error(error: Exception) -> tuple
    """
    Handle and format error response
    
    Args:
        error: Exception object
        
    Returns:
        tuple: (error_dict, status_code)
    """

paginate(query: Query, page: int, per_page: int) -> dict
    """
    Paginate SQLAlchemy query
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        per_page: Items per page
        
    Returns:
        dict: {
            "items": [items],
            "total": int,
            "page": int,
            "per_page": int,
            "pages": int
        }
    """

generate_slug(text: str) -> str
    """
    Generate URL-safe slug from text
    
    Args:
        text: Input text
        
    Returns:
        str: URL-safe slug
        
    Example:
        >>> generate_slug("Hello World!")
        "hello-world"
    """
```

**Usage Example:**
```python
from src.utils.helpers import format_response, paginate

# Format response
response, status = format_response(
    data={"user": user.to_dict()},
    message="User created successfully",
    status=201
)

# Paginate query
from src.models import User
query = User.query.filter_by(is_active=True)
result = paginate(query, page=1, per_page=20)
```

---

## Decorators

### Authentication Decorators
**File:** `src/utils/decorators.py`

**Decorators:**
```python
@token_required
def protected_route():
    """
    Require valid JWT token
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected():
            return {"message": "Access granted"}
            
    Adds to function:
        current_user (User): Authenticated user object
    """

@admin_required
def admin_route():
    """
    Require admin role
    
    Usage:
        @app.route('/admin')
        @admin_required
        def admin_panel():
            return {"message": "Admin access"}
            
    Adds to function:
        current_user (User): Authenticated admin user
    """

@rate_limit(limit=100, per=60)
def rate_limited_route():
    """
    Rate limiting decorator
    
    Args:
        limit: Maximum requests
        per: Time period in seconds
        
    Usage:
        @app.route('/api/search')
        @rate_limit(limit=10, per=60)
        def search():
            return {"results": [...]}
    """
```

**Usage Example:**
```python
from flask import Blueprint
from src.utils.decorators import token_required, admin_required

bp = Blueprint('api', __name__)

@bp.route('/profile')
@token_required
def get_profile(current_user):
    return {"user": current_user.to_dict()}

@bp.route('/admin/users')
@admin_required
def list_users(current_user):
    # Only admins can access
    return {"users": [...]}
```

---

## API Endpoints

### Users API
**File:** `src/api/users.py`  
**Blueprint:** `users_bp`

**Endpoints:**
```python
POST /api/users/register
    """
    Register new user
    
    Body:
        {
            "email": str,
            "password": str,
            "name": str
        }
        
    Returns:
        {
            "user": User,
            "access_token": str,
            "refresh_token": str
        }
    """

POST /api/users/login
    """Login user and get tokens"""

POST /api/users/refresh
    """Refresh access token"""

GET /api/users
    """Get all users (admin only)"""

GET /api/users/<id>
    """Get user by ID"""

PUT /api/users/<id>
    """Update user"""

DELETE /api/users/<id>
    """Delete user (admin only)"""
```

---

### Products API
**File:** `src/api/products.py`  
**Blueprint:** `products_bp`

**Endpoints:**
```python
GET /api/products
    """Get all products"""

GET /api/products/<id>
    """Get product by ID"""

POST /api/products
    """Create product (admin only)"""

PUT /api/products/<id>
    """Update product (admin only)"""

DELETE /api/products/<id>
    """Delete product (admin only)"""
```

---

### Orders API
**File:** `src/api/orders.py`  
**Blueprint:** `orders_bp`

**Endpoints:**
```python
GET /api/orders
    """Get user's orders"""

GET /api/orders/<id>
    """Get order by ID"""

POST /api/orders
    """Create order"""

PUT /api/orders/<id>/status
    """Update order status"""

DELETE /api/orders/<id>
    """Cancel order"""
```

---

## Middleware

### Auth Middleware
**File:** `src/middleware/auth.py`

**Purpose:** Process authentication for all requests

**Functions:**
```python
before_request():
    """
    Run before each request
    - Extract token from header
    - Verify token
    - Load user into g.current_user
    """

after_request(response):
    """
    Run after each request
    - Add security headers
    - Log request/response
    """
```

---

### Logging Middleware
**File:** `src/middleware/logging.py`

**Purpose:** Log all requests and responses

**Functions:**
```python
log_request():
    """Log incoming request details"""

log_response(response):
    """Log outgoing response details"""
```

---

## Statistics

**Total Classes:** [COUNT]
**Total Functions:** [COUNT]
**Total Decorators:** [COUNT]
**Total API Endpoints:** [COUNT]

**By Category:**
- Models: [COUNT]
- Services: [COUNT]
- Utils: [COUNT]
- API: [COUNT]
- Middleware: [COUNT]

---

## Update Checklist

When adding new class/function:
- [ ] Add to this registry
- [ ] Document purpose
- [ ] Document parameters and returns
- [ ] Add usage example
- [ ] Update statistics
- [ ] Update Import_Export_Map.md

---

## Notes

- Keep this registry updated when code changes
- Use this as API documentation
- Include usage examples for complex functions
- Document all parameters and return values
- Note any side effects or important behavior

