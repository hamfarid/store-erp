# دليل المطور - Store ERP Developer Guide

**Version:** 2.0  
**Last Updated:** 2025-12-13  
**Language:** Arabic/English

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Backend Development](#backend-development)
5. [Frontend Development](#frontend-development)
6. [Database](#database)
7. [API Documentation](#api-documentation)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Contributing](#contributing)

---

## Introduction

### About Store ERP

Store ERP is a comprehensive inventory management system built with:
- **Backend:** Python 3.11, Flask, SQLAlchemy
- **Frontend:** React 18, Vite, TailwindCSS
- **Database:** SQLite (development), PostgreSQL (production)
- **Architecture:** RESTful API, SPA (Single Page Application)

### Tech Stack

#### Backend
- **Framework:** Flask 3.0
- **ORM:** SQLAlchemy 2.0
- **Authentication:** Flask-Login, JWT
- **Validation:** Marshmallow
- **Testing:** Pytest
- **Logging:** Custom JSON logger

#### Frontend
- **Framework:** React 18
- **Build Tool:** Vite 5
- **Styling:** TailwindCSS, Custom CSS
- **State Management:** React Context, Hooks
- **Charts:** Recharts
- **Icons:** Lucide React
- **Routing:** React Router 6

#### Database
- **Development:** SQLite
- **Production:** PostgreSQL 15+
- **Migrations:** Alembic

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 22+
- pnpm 9+
- Git

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/hamfarid/store-erp.git
cd store-erp
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment (optional but recommended)
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python src/app.py
```

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

#### 4. Access Application

- **Frontend:** http://localhost:5502
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs

### Environment Variables

Create `.env` files in both `backend/` and `frontend/`:

#### Backend `.env`
```env
FLASK_APP=src/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/inventory.db
JWT_SECRET_KEY=your-jwt-secret-here
```

#### Frontend `.env`
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Store ERP
```

---

## Project Structure

```
store-erp/
├── backend/
│   ├── src/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # Flask blueprints
│   │   ├── utils/           # Utilities (logger, helpers)
│   │   ├── middleware/      # Custom middleware
│   │   ├── schemas/         # Marshmallow schemas
│   │   └── app.py           # Main Flask application
│   ├── tests/               # Backend tests
│   ├── instance/            # SQLite database
│   ├── logs/                # Log files
│   ├── requirements.txt     # Python dependencies
│   └── pytest.ini           # Pytest configuration
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ui/          # UI components (73 files)
│   │   │   └── ...          # Feature components
│   │   ├── styles/          # CSS files
│   │   │   ├── design-tokens.css  # Design system
│   │   │   └── ...
│   │   ├── utils/           # Utilities
│   │   ├── hooks/           # Custom React hooks
│   │   └── main.jsx         # Entry point
│   ├── public/              # Static assets
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # Architecture documentation
│   ├── USER_GUIDE.md        # User guide
│   ├── DEVELOPER_GUIDE.md   # This file
│   └── Task_List.md         # Task list
├── .memory/                 # Memory system
│   ├── conversations/       # Conversation logs
│   ├── decisions/           # Decision records
│   ├── checkpoints/         # Progress checkpoints
│   ├── context/             # Current context
│   └── learnings/           # Learnings
└── README.md                # Project README
```

---

## Backend Development

### Models

Models are defined in `backend/src/models/`. Each model represents a database table.

#### Example: Product Model

```python
# backend/src/models/product.py

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    barcode = Column(String(100), unique=True, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    purchase_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    min_quantity = Column(Integer, default=10)
    unit = Column(String(50), default='piece')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship('Category', back_populates='products')
    lots = relationship('Lot', back_populates='product')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'barcode': self.barcode,
            'category_id': self.category_id,
            'purchase_price': self.purchase_price,
            'sale_price': self.sale_price,
            'quantity': self.quantity,
            'min_quantity': self.min_quantity,
            'unit': self.unit,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
```

### Routes (Blueprints)

Routes are defined in `backend/src/routes/`. Each blueprint handles a specific feature.

#### Example: Products Route

```python
# backend/src/routes/products.py

from flask import Blueprint, request, jsonify
from src.models.product import Product
from src.utils.logger import log_api_request, log_error_with_context
from src.middleware.auth import require_auth, require_permission
from datetime import datetime

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

@products_bp.route('/', methods=['GET'])
@require_auth
@require_permission('products.view')
def get_products():
    """Get all products with optional filtering."""
    start_time = datetime.now()
    
    try:
        # Get query parameters
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', type=str)
        is_active = request.args.get('is_active', type=bool, default=True)
        
        # Build query
        query = Product.query
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(
                (Product.name.ilike(f'%{search}%')) |
                (Product.barcode.ilike(f'%{search}%'))
            )
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        # Execute query
        products = query.all()
        
        # Log API request
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        log_api_request(
            method='GET',
            endpoint='/api/products',
            user_id=request.user.id,
            status_code=200,
            duration_ms=duration_ms
        )
        
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in products],
            'count': len(products)
        }), 200
        
    except Exception as e:
        log_error_with_context(e, {'endpoint': '/api/products', 'method': 'GET'})
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@products_bp.route('/', methods=['POST'])
@require_auth
@require_permission('products.create')
def create_product():
    """Create a new product."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'purchase_price', 'sale_price']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create product
        product = Product(
            name=data['name'],
            barcode=data.get('barcode'),
            category_id=data.get('category_id'),
            purchase_price=data['purchase_price'],
            sale_price=data['sale_price'],
            quantity=data.get('quantity', 0),
            min_quantity=data.get('min_quantity', 10),
            unit=data.get('unit', 'piece')
        )
        
        db.session.add(product)
        db.session.commit()
        
        log_user_action(
            user_id=request.user.id,
            action='create_product',
            details={'product_id': product.id, 'name': product.name}
        )
        
        return jsonify({
            'success': True,
            'data': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        log_error_with_context(e, {'endpoint': '/api/products', 'method': 'POST'})
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### Logging

Use the custom logger for all logging operations:

```python
from src.utils.logger import (
    info, warning, error,
    log_user_action,
    log_security_event,
    log_api_request,
    log_performance
)

# Simple logging
info("User logged in", user_id="user_123")
warning("Low stock detected", product_id=456)
error("Database connection failed")

# Specialized logging
log_user_action("user_123", "create_product", {"product_id": 789})
log_security_event("failed_login", user_id="user_123", ip_address="192.168.1.1")
log_api_request("POST", "/api/products", status_code=201, duration_ms=45.3)
log_performance("database_query", 123.45, {"query": "SELECT * FROM products"})
```

### Authentication & Authorization

#### Authentication (Login)

```python
from flask_login import login_user, logout_user, current_user

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'success': True, 'user': user.to_dict()})
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
```

#### Authorization (Permissions)

```python
from src.middleware.auth import require_permission

@products_bp.route('/<int:id>', methods=['DELETE'])
@require_auth
@require_permission('products.delete')
def delete_product(id):
    # Only users with 'products.delete' permission can access
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True})
```

---

## Frontend Development

### Components

Components are in `frontend/src/components/`.

#### Example: Product Card Component

```jsx
// frontend/src/components/ProductCard.jsx

import React from 'react';
import { Package, Edit, Trash2 } from 'lucide-react';
import './ProductCard.css';

const ProductCard = ({ product, onEdit, onDelete }) => {
  const isLowStock = product.quantity <= product.min_quantity;
  
  return (
    <div className="product-card">
      <div className="product-card__header">
        <div className="product-card__icon">
          <Package size={24} />
        </div>
        {isLowStock && (
          <span className="product-card__badge product-card__badge--warning">
            مخزون منخفض
          </span>
        )}
      </div>
      
      <div className="product-card__body">
        <h3 className="product-card__name">{product.name}</h3>
        <p className="product-card__barcode">{product.barcode}</p>
        
        <div className="product-card__details">
          <div className="product-card__detail">
            <span className="product-card__label">السعر:</span>
            <span className="product-card__value">{product.sale_price} ريال</span>
          </div>
          <div className="product-card__detail">
            <span className="product-card__label">الكمية:</span>
            <span className={`product-card__value ${isLowStock ? 'text-warning' : ''}`}>
              {product.quantity} {product.unit}
            </span>
          </div>
        </div>
      </div>
      
      <div className="product-card__footer">
        <button
          className="btn btn-sm btn-ghost"
          onClick={() => onEdit(product)}
        >
          <Edit size={16} />
          تعديل
        </button>
        <button
          className="btn btn-sm btn-danger"
          onClick={() => onDelete(product)}
        >
          <Trash2 size={16} />
          حذف
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
```

### Design System

Use design tokens from `frontend/src/styles/design-tokens.css`:

```css
/* Use CSS variables */
.my-component {
  /* Colors */
  color: var(--color-text-primary);
  background-color: var(--color-bg-primary);
  border-color: var(--color-border-light);
  
  /* Typography */
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-normal);
  
  /* Spacing */
  padding: var(--spacing-4);
  margin-bottom: var(--spacing-6);
  gap: var(--spacing-2);
  
  /* Border Radius */
  border-radius: var(--radius-lg);
  
  /* Shadows */
  box-shadow: var(--shadow-md);
  
  /* Transitions */
  transition: var(--transition-all);
}
```

### API Integration

Use fetch or axios to call backend APIs:

```jsx
// frontend/src/utils/api.js

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  async get(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  },
  
  async post(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  },
  
  // ... put, delete, etc.
};

// Usage in component
import { api } from '../utils/api';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await api.get('/api/products');
        setProducts(data.data);
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProducts();
  }, []);
  
  // ... render
};
```

---

## Database

### Schema

The database schema is defined in SQLAlchemy models. Key tables:

- **users** - User accounts
- **roles** - User roles
- **permissions** - Permissions
- **products** - Products
- **categories** - Product categories
- **lots** - Product lots (batches)
- **customers** - Customers
- **suppliers** - Suppliers
- **invoices** - Sales invoices
- **invoice_items** - Invoice line items
- **purchases** - Purchase orders
- **purchase_items** - Purchase order line items
- **inventory_movements** - Stock movements
- **payments** - Payments

### Migrations

Use Alembic for database migrations:

```bash
# Create migration
alembic revision --autogenerate -m "Add new column to products"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## API Documentation

### Authentication

All API endpoints (except `/api/auth/login`) require authentication.

**Login:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin",
    "name": "Administrator",
    "role": "Super Admin"
  }
}
```

### Products API

#### Get All Products
```http
GET /api/products?category_id=1&search=tomato&is_active=true
```

#### Get Single Product
```http
GET /api/products/123
```

#### Create Product
```http
POST /api/products
Content-Type: application/json

{
  "name": "بذور طماطم F1",
  "barcode": "1234567890",
  "category_id": 1,
  "purchase_price": 50.00,
  "sale_price": 75.00,
  "quantity": 100,
  "min_quantity": 20,
  "unit": "كيس"
}
```

#### Update Product
```http
PUT /api/products/123
Content-Type: application/json

{
  "sale_price": 80.00,
  "quantity": 150
}
```

#### Delete Product
```http
DELETE /api/products/123
```

### Error Handling

All API responses follow this format:

**Success:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message here"
}
```

---

## Testing

### Backend Tests

Tests are in `backend/tests/`.

#### Running Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_logger.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_logger.py::TestJSONFormatter::test_formatter_creates_valid_json
```

#### Writing Tests

```python
# backend/tests/test_products.py

import pytest
from src.models.product import Product

class TestProductModel:
    def test_create_product(self):
        """Test creating a product."""
        product = Product(
            name="Test Product",
            purchase_price=50.0,
            sale_price=75.0
        )
        
        assert product.name == "Test Product"
        assert product.purchase_price == 50.0
        assert product.sale_price == 75.0
    
    def test_product_to_dict(self):
        """Test product serialization."""
        product = Product(
            name="Test Product",
            purchase_price=50.0,
            sale_price=75.0
        )
        
        data = product.to_dict()
        
        assert data['name'] == "Test Product"
        assert data['purchase_price'] == 50.0
```

### Frontend Tests

(To be implemented with Vitest/Jest)

---

## Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure CORS properly
- [ ] Set up backup system
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Run security audit

### Docker Deployment

```dockerfile
# Dockerfile (example)
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.app:app"]
```

---

## Contributing

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Write docstrings
- Max line length: 100

**JavaScript/React:**
- Use ESLint
- Use Prettier
- Follow Airbnb style guide
- Use functional components

### Git Workflow

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes
3. Commit: `git commit -m "feat: add new feature"`
4. Push: `git push origin feature/my-feature`
5. Create Pull Request

### Commit Messages

Follow Conventional Commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

---

## Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **React Documentation:** https://react.dev/
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
- **Vite Documentation:** https://vitejs.dev/
- **TailwindCSS Documentation:** https://tailwindcss.com/

---

**End of Developer Guide**

**Version:** 2.0  
**Last Updated:** 2025-12-13  
**Copyright:** © 2025 Store ERP. All rights reserved.
