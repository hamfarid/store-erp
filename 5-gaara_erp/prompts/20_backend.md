=================================================================================
BACKEND DEVELOPMENT - Django, FastAPI, Flask, Express
=================================================================================

Version: Latest
Type: Architecture - Backend

This prompt provides comprehensive guidance for backend development across
multiple frameworks and languages.

=================================================================================
FRAMEWORK SELECTION
=================================================================================

## When to Use Each Framework

**Django:**
- Full-featured web applications
- Admin panel needed
- ORM preferred
- Batteries-included approach
- Python ecosystem

**FastAPI:**
- Modern async APIs
- High performance needed
- Auto-generated docs important
- Type hints preferred
- Python 3.7+

**Flask:**
- Lightweight applications
- Microservices
- Custom architecture needed
- Flexibility over convention
- Python ecosystem

**Express (Node.js):**
- JavaScript full-stack
- Real-time applications
- NPM ecosystem
- Event-driven architecture
- High concurrency

=================================================================================
DJANGO BEST PRACTICES
=================================================================================

## Project Structure

```
project/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── products/
│   └── orders/
├── static/
├── media/
├── templates/
└── requirements/
    ├── base.txt
    ├── development.txt
    └── production.txt
```

## Models Best Practices

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model."""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.email

class Product(models.Model):
    """Product model."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_stock(self):
        return self.stock > 0
```

## Views & ViewSets

```python
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """Product CRUD operations."""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by query params
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        """Custom action for purchasing."""
        product = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if product.stock < quantity:
            return Response(
                {'error': 'Not enough stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.stock -= quantity
        product.save()
        
        return Response({'status': 'purchased'})
```

## Serializers

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 
            'stock', 'is_in_stock', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be positive"
            )
        return value
```

## URLs

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## Settings Organization

**base.py:**
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'rest_framework',
    'corsheaders',
    # Local apps
    'apps.users',
    'apps.products',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

**development.py:**
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'myproject_dev'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

CORS_ALLOW_ALL_ORIGINS = True
```

**production.py:**
```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', ''
).split(',')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

=================================================================================
FASTAPI BEST PRACTICES
=================================================================================

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── products.py
│   ├── services/
│   └── utils/
├── tests/
├── requirements.txt
└── .env
```

## Main Application

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, products
from app.database import engine
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My API",
    description="API documentation",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(products.router, prefix="/api/products", tags=["products"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
```

## Models (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

## Schemas (Pydantic)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## Routers

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.is_active == True
    ).offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    return None
```

## Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/dbname"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

=================================================================================
COMMON PATTERNS
=================================================================================

## Pagination

**Django:**
```python
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

**FastAPI:**
```python
@router.get("/")
async def get_items(skip: int = 0, limit: int = 20):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items
```

## Filtering

**Django:**
```python
from django_filters import rest_framework as filters

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    class Meta:
        model = Product
        fields = ['category', 'is_active']
```

**FastAPI:**
```python
@router.get("/")
async def get_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    return query.all()
```

## Error Handling

**Django:**
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code
    
    return response
```

**FastAPI:**
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )
```

=================================================================================
TESTING
=================================================================================

## Django Tests

```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product

class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            name="Test Product",
            price=99.99,
            stock=10
        )
    
    def test_get_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_product(self):
        data = {
            'name': 'New Product',
            'price': 49.99,
            'stock': 5
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## FastAPI Tests

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_products():
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product():
    product_data = {
        "name": "Test Product",
        "price": 99.99,
        "stock": 10
    }
    response = client.post("/api/products/", json=product_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"
```

=================================================================================
DEPLOYMENT
=================================================================================

## Django with Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## FastAPI with Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

=================================================================================
END OF BACKEND PROMPT
=================================================================================


================================================================================
RECOVERED CONTENT FROM  (Phase 2)
================================================================================

- Visual regression: Percy, Chromatic

E) Performance Testing
- Load testing: k6, Locust
- Stress testing: find breaking point
- Spike testing: sudden traffic
- Endurance testing: sustained load

F) Security Testing
- SAST: Semgrep, SonarQube
- DAST: OWASP ZAP
- Dependency scanning: Snyk, npm audit
- Secret scanning: TruffleHog
- Penetration testing: annual

G) Accessibility Testing
- Automated: axe, Lighthouse
- Manual: screen reader, keyboard nav
- WCAG AA compliance

H) Quality Gates
- All tests pass
- Coverage >80%
- No critical/high vulnerabilities
- Lighthouse score >90
- No secrets in code

⸻

11) DOCUMENTATION REQUIREMENTS (30+ files)

Required Files:
1. README.md - Project overview
2. docs/Inventory.md - All components, versions
3. docs/TODO.md - Prioritized task list
4. docs/DONT_DO_THIS_AGAIN.md - Lessons learned
5. docs/TechStack.md - Technologies used
6. docs/API_Contracts.md - API specifications
7. docs/DB_Schema.md - Database schema
8. docs/Security.md - Security measure
 1)
```
FILE: <repo-path> | PURPOSE: <brief> | OWNER: <team/person> | RELATED: <files> | LAST-AUDITED: <YYYY-MM-DD>
```

B) Examples
```python
# FILE: backend/src/services/auth.py | PURPOSE: Authentication service | OWNER: Security Team | RELATED: models/user.py, routes/auth.py | LAST-AUDITED: 2025-10-28
```

```typescript
// FILE: frontend/src/components/Dashboard.tsx | PURPOSE: Main dashboard component | OWNER: Frontend Team | RELATED: pages/Home.tsx | LAST-AUDITED: 2025-10-28
```

C) CI Enforcement
- Pre-commit hook: check header presence
- CI pipeline: fail if missing
- Auto-generate for new files
- Update LAST-AUDITED on changes

D) Benefits
- Quick file identification
- Ownership clarity
- Audit trail
- Related files discovery

⸻

24) CLASS & TYPE CANONICAL REGISTRY (NEW in )

A) Purpose
- Single source of truth for all classes/types
- Prevent duplication
- Track relationships
- Migration history

B) Location
`/docs/Class_Registry.md` (APPEND-ONLY)

C) Entry Format
```markdow
n
## User

- **CanonicalName**: User
- **Location**: `backend/src/models/user.py`
- **DomainContext**: Authentication & Authorization
- **Purpose**: Represents system users
- **Fields**:
  - id: UUID (PK)
  - email: String (unique, indexed)
  - password_hash: String
  - role: Enum (admin, manager, user)
  - created_at: DateTime
  - updated_at: DateTime
- **Relations**:
  - has_many: sessions, activity_logs
  - belongs_to: tenant (if multi-tenant)
- **Invariants**:
  - email must be valid format
  - password_hash never null
  - role must be valid enum value
- **Visibility**: Internal (not exposed directly in API)
- **Lifecycle**: Active users can be soft-deleted
- **DTO/API**: UserDTO in `contracts/user.dto.ts`
- **FE Mapping**: `frontend/src/types/user.ts`
- **DB Mapping**: `users` table
- **Tests**: `tests/models/test_user.py`
- **Aliases**: None
- **Migration Notes**:  - Added role field
```

D) Workflow
1. Before creating new class: search registry
2. If exists: reuse canonica
 `/docs/File_Map.md` - Complete file inventory
   - `/docs/Class_Registry.md` - All classes/types
   - `/docs/Imports_Map.md` - Import dependencies
   - `/docs/Exports_Map.md` - Export mappings

3. **Search for Existing Files**
   ```bash
   # Search by name
   find . -name "*user*" -type f
   
   # Search by content (AST-based)
   python scripts/detect_duplicates.py --semantic --target "User"
   ```

B) FILE MAP STRUCTURE

`/docs/File_Map.md` format:
```markdown
# File Map - Generated: 2025-10-28

## Backend Files

### Models
- `backend/src/models/user.py` - User model (CANONICAL)
  - Classes: User
  - Functions: create_user(), get_user_by_email()
  - Dependencies: db, auth
  - Last Modified: 2025-10-27
  - Owner: Auth Team

### Services
- `backend/src/services/auth_service.py` - Authentication service
  - Functions: login(), logout(), verify_token()
  - Dependencies: models/user, jwt
  - Last Modified: 2025-10-26
  - Owner: Auth Team

## Frontend Files

### Components
- `frontend/src
p] [Back] [Continue]               │
└─────────────────────────────────────────┘
```

### Step 5: Security Settings
```
┌─────────────────────────────────────────┐
│  Security Configuration                 │
│                                         │
│  Secret Key: [Auto-generated]           │
│  ⚠️ NEVER share this key!               │
│                                         │
│  Session Timeout: [15] minutes          │
│  Max Login Attempts: [5]                │
│  Password Min Length: [12]              │
│                                         │
│  Enable MFA: [✓] Recommended            │
│                                         │
│  [Back] [Continue]                      │
└─────────────────────────────────────────┘
```

### Step 6: Final Review & Confirmation
```
┌─────────────────────────────────────────┐
│  Review Configuration                   │
│                                         │
│  ✅ Admin user created                  │
│  ✅ Database connected                 
 of changes

⸻

38) PRE-DEVELOPMENT CHECKLIST (CRITICAL - NEW in )

**PURPOSE:** Mandatory checklist before starting any development

A) THE CHECKLIST

```markdown
# Pre-Development Checklist

Before starting ANY development work, complete this checklist:

## 1. Environment Setup
- [ ] `.env` file exists and is valid
- [ ] Run `python scripts/validate_env.py` - all checks pass
- [ ] APP_ENV is set correctly (development/production)
- [ ] All required services are running (database, redis, etc.)

## 2. Documentation Review
- [ ] Read `/docs/File_Map.md` - know where files are
- [ ] Read `/docs/Class_Registry.md` - know what classes exist
- [ ] Read `/docs/Imports_Map.md` - understand dependencies
- [ ] Read `/docs/TODO.md` - know what's planned
- [ ] Read `/docs/DONT_DO_THIS_AGAIN.md` - learn from past mistakes

## 3. Search for Existing Code
- [ ] Search for similar files: `find . -name "*<keyword>*"`
- [ ] Search for similar classes: check Class_Registry.md
- [ ] Search for simila
usage in function reference

**When Creating:**
- Make it reusable from the start
- Document in function reference
- Add to module map
- Write comprehensive tests


---

## 50. Task Management System

### 50.1 TODO File Structure (APPEND-ONLY)

**Location:** `docs/TODO.md`

**Rules:**
- **APPEND-ONLY** - Never delete tasks
- Mark completed with 'x'
- Move completed to bottom
- Create `docs/completed_tasks.md` for archive

**Template:**
```markdown
# TODO List

**Last Updated:** YYYY-MM-DD

## Classification

### 🔴 Errors (P0 - Critical)
- [ ] [Module] Error description
- [ ] [Module] Error description
- [x] [Module] Fixed error (moved to bottom)

### 🟠 Fixes (P1 - High)
- [ ] [Module] Fix description
- [ ] [Module] Fix description

### 🟡 Development (P2 - Medium)
- [ ] [Module] Feature description
- [ ] [Module] Feature description

### 🟢 Integration (P3 - Low)
- [ ] [Module] Integration task
- [ ] [Module] Integration task

### 🔵 Inspection
- [ ] [Module] Review/audit task
- [ ] [Modu
le] Review/audit task

---

## Completed Tasks (Move here, don't delete)

- [x] [2025-01-15] [Module] Task description
- [x] [2025-01-14] [Module] Task description
```

### 50.2 Task Classification

**Priority Levels:**
- **P0 (🔴 Critical):** System broken, security issue, data loss
- **P1 (🟠 High):** Major bug, broken feature, performance issue
- **P2 (🟡 Medium):** New feature, enhancement, minor bug
- **P3 (🟢 Low):** Integration, optimization, nice-to-have
- **Inspection (🔵):** Code review, audit, documentation

**Task Format:**
```markdown
- [ ] [Priority] [Module] [Owner?] Task description
      Estimate: X hours/days
      Dependencies: Task #Y, #Z
      Status: Not Started / In Progress / Blocked / Done
```

**Example:**
```markdown
- [ ] [P0] [Auth] [hamfarid] Fix login bypass vulnerability
      Estimate: 4 hours
      Dependencies: None
      Status: In Progress
```

### 50.3 Workflow

**Adding Tasks:**
1. Add to appropriate classification section
2. Include priority, module, 
ps (ForeignKey, ManyToMany)
   - Custom methods (confirm(), cancel(), compute_totals())
   - State management
   - Validation logic

3. **Arabic Docstrings**
   - All classes and functions documented in Arabic
   - Clear, professional language
   - Examples where helpful

4. **Custom Reports**
   - PDF generation
   - Excel exports
   - Custom templates

5. **Smart Filters**
   - Date ranges
   - Status filters
   - Search functionality

### 54.2 Module Structure Template

```
module_name/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── main_model.py
│   └── related_models.py
├── views/
│   ├── __init__.py
│   ├── api_views.py
│   └── frontend_views.py
├── services/
│   ├── __init__.py
│   └── business_logic.py
├── serializers/
│   ├── __init__.py
│   └── serializers.py
├── permissions/
│   ├── __init__.py
│   └── permissions.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_services.py
├── frontend/
│   ├── components/
│   ├── pages/
│
# العلاقات
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='المستخدم',
        related_name='%(class)s_records'
    )
    
    # الحالة
    state = models.CharField(
        'الحالة',
        max_length=20,
        choices=STATES,
        default=STATE_DRAFT
    )
    
    # التواريخ
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    confirmed_at = models.DateTimeField('تاريخ التأكيد', null=True, blank=True)
    
    # الحقول المحسوبة
    total = models.DecimalField('الإجمالي', max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'النموذج الرئيسي'
        verbose_name_plural = 'النماذج الرئيسية'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['state', 'created_at']),
        ]
    
    def __str__(self):
        """تمثيل نصي
ion detector
2. Check if similar function exists
3. If exists (≥80% similarity):
   - Reuse existing function
   - Or enhance existing function
   - Do NOT create duplicate

**After Merging Modules:**

1. Run duplication detector
2. Review all duplicates
3. Merge duplicates systematically
4. Update all dependent files

### 58.5 Ignore Trivial Differences

- Variable names
- Whitespace
- Comments
- String literals (if logic is same)
- Numeric literals (if logic is same)

### 58.6 CI/CD Integration

```yaml
# .github/workflows/ci.yml
- name: Detect Code Duplication
  run: |
    python scripts/detect_code_duplication.py .
    if [ -s docs/Code_Duplication_Report.md ]; then
      echo "⚠️ Code duplication detected!"
      cat docs/Code_Duplication_Report.md
      exit 1
    fi
```

### 58.7 Metrics

- **Duplication Rate:** (Duplicate LOC / Total LOC) × 100%
- **Target:** <5%
- **Maximum Allowed:** 10%

---

================================================================================
##
===========================

### 60.1 Principle

**NEVER** merge manually when tools can do it safely.  
**ALWAYS** backup before merge.  
**ALWAYS** update all dependent files.

### 60.2 Smart Merge Tool

**Tool:** `scripts/smart_merge.py`

```bash
# Interactive merge
python scripts/smart_merge.py

# Auto-merge (with confirmation)
python scripts/smart_merge.py --auto

# Dry-run (no changes)
python scripts/smart_merge.py --dry-run
```

### 60.3 Merge Workflow

1. **Detect Duplicates**
   - Run `detect_code_duplication.py`
   - Load duplication report
   
2. **For Each Duplicate Pair:**
   
   a. **Show Comparison**
      ```
      File 1: models/user.py::create_user()
      File 2: models/user_unified.py::add_user()
      Similarity: 95%
      
      Differences:
      - Line 10: Variable name (user_data vs data)
      - Line 15: Return type annotation
      ```
   
   b. **Ask User**
      ```
      Merge these functions? (y/n/skip)
      Keep which implementation? (1/2/best)
      ``
 flows/

---

### 4.3 apply.sh

**الوظيفة:** تطبيق المكونات على المشروع

**الاستخدام:**
```bash
# تطبيق الكل
.global/scripts/apply.sh

# تطبيق مكون محدد
.global/scripts/apply.sh --only config

# مع نسخ احتياطي
.global/scripts/apply.sh --backup
```

---

### 4.4 update.sh

**الوظيفة:** تحديث Global Guidelines

**الاستخدام:**
```bash
# آخر إصدار
.global/scripts/update.sh

# إصدار محدد
.global/scripts/update.sh --version 3.7.0
```

---

### 4.5 uninstall.sh

**الوظيفة:** إزالة Global Guidelines

**الاستخدام:**
```bash
# إزالة .global/ فقط
.global/scripts/uninstall.sh

# إزالة كاملة
.global/scripts/uninstall.sh --full
```

---

## 5. Flows / سير العمل 📚

### 5.1 DEVELOPMENT_FLOW.md

**المحتوى:**
- 7 مراحل للتطوير
- من التهيئة إلى النشر
- Best practices لكل مرحلة
- أمثلة CI/CD

---

### 5.2 INTEGRATION_FLOW.md ⭐

**المحتوى:**
- 3 طرق للدمج
- خطوات تفصيلية
- أمثلة لـ Django, Flask, FastAPI
- FAQ شامل

**الأهم للمشاريع القائمة!**

---

### 5.3 DEPLOYMENT_FLOW.md

**المحتوى:**
- 3 استراتيجيات 
es يوفر:

✅ **4 أدوات احترافية** للتحليل والصيانة  
✅ **قوالب جاهزة** لـ config/definitions  
✅ **3 أمثلة كاملة** لأنماط مختلفة  
✅ **5 سكريبتات** للتكامل السلس  
✅ **3 workflows** شاملة  
✅ **توثيق شامل** لكل شيء

**للاستخدام في Augment:**
1. انسخ البرومبت
2. انسخ الأدوات
3. انسخ الأمثلة
4. أشر إليها في التكوين
5. ابدأ العمل!

---

**Last Updated:** 2025-11-02  
**Version:** 3.9.0  
**Status:** ✅ Active

================================================================================
END OF SECTION 63
================================================================================



⸻

## Section 64: Interactive Project Setup & State Management

### Overview

This section defines an **interactive project setup system** that collects project information at the start and manages project state throughout development and deployment phases.

---

### 64.1 Initial Project Questions

**When to Ask:**
- At the very beginning of a new project
- When user starts working on a project for the fi
                                      │
│  Step 6: Security Settings                                  │
│  ─────────────────────────                                  │
│  - Password policies                                        │
│  - Session timeout                                          │
│  - IP whitelist/blacklist                                   │
│  - Rate limiting                                            │
│                                                             │
│  Step 7: Integrations (Optional)                            │
│  ───────────────────────────────                            │
│  - Payment gateways                                         │
│  - Analytics                                                │
│  - Social login                                             │
│  - Third-party APIs                                         │
│                                                             │
│  Step 8: Final Review                                       │

loyment process
```

**Production Phase:**

```bash
# Database
backup-db             # Create database backup
restore-db [file]     # Restore from backup
migrate-db            # Run migrations (with backup)

# Monitoring
health-check          # Check system health
view-logs             # View application logs
monitor-stats         # View performance stats

# Management
rollback              # Rollback to previous version
restart-services      # Restart all services
update-config         # Update configuration
```

---

### 64.11 Configuration Update

**To update configuration:**

```bash
# Interactive update
update-config

# Direct edit
nano .global/project_config.json

# Reload config
reload-config
```

**Augment will ask:**

```
Which setting would you like to update?

1. Project name
2. Port configuration
3. Database settings
4. Environment settings
5. Admin settings
6. All settings

Your choice: ___
```

---

### 64.12 Best Practices

**For Augment:**

1. **Always ask questions fir
ations
- Newsletters
- Transactional emails

**Use Cases:**
- Email campaigns
- Notifications
- Marketing emails

---

### 7. AI Assistant Template ⭐⭐⭐

**Path:** `templates/ai_assistant/`

**Description:** Intelligent AI-powered assistant

**Features:**
- Natural language processing
- Knowledge base (RAG)
- Chat interface
- Multi-model support (GPT, Claude, Gemini)
- Context awareness
- Custom training

**Tech Stack:**
- Frontend: React + TypeScript
- Backend: FastAPI + LangChain
- Vector DB: Pinecone/Chroma
- LLM: OpenAI/Anthropic

**Use Cases:**
- Customer support chatbots
- Internal knowledge assistants
- AI-powered help systems
- Virtual assistants

---

### 8. Charity Management Template ⭐⭐⭐

**Path:** `templates/charity_management/`

**Description:** Complete charity and donation management

**Features:**
- Donation processing (Stripe, PayPal)
- Beneficiary management
- Campaign management
- Volunteer management
- Reporting & analytics

**Tech Stack:**
- Frontend: React + Materi
al-UI
- Backend: Django + DRF
- Database: PostgreSQL
- Payment: Stripe/PayPal

**Use Cases:**
- Charity organizations
- NGOs
- Fundraising platforms
- Volunteer management

---

### 9. AI Prediction Template ⭐⭐⭐

**Path:** `templates/ai_prediction/`

**Description:** ML prediction and forecasting system

**Features:**
- Time series forecasting
- Classification & regression
- Anomaly detection
- Model training & deployment
- MLOps (MLflow)
- Monitoring & drift detection

**Tech Stack:**
- Frontend: React + Plotly
- Backend: FastAPI
- ML: Scikit-learn, XGBoost, Prophet
- MLOps: MLflow

**Use Cases:**
- Sales forecasting
- Demand prediction
- Fraud detection
- Price prediction
- Customer churn prediction

---

## Template Generator Tool

### Usage

```bash
# List available templates
python3 tools/template_generator.py --list

# Interactive mode
python3 tools/template_generator.py --interactive

# Generate with defaults
python3 tools/template_generator.py \
  --template erp_system \
  --ou
**
   - Explain template features
   - Ask for confirmation

3. **Gather variables**
   - Ask for project name
   - Ask for ports (if needed)
   - Ask for database name
   - Ask for other variables

4. **Generate project**
   - Run template generator
   - Show progress
   - Report completion

5. **Next steps**
   - Show generated files
   - Explain setup process
   - Offer to help with customization

---

## Examples

### Example 1: Generate ERP System

```
User: "I need to build an ERP system for my company"

Augment: "I can generate a complete ERP system template for you! It includes:
- Inventory Management
- Sales & Purchases
- Accounting
- HR & Payroll

All with React frontend, Django backend, and PostgreSQL database.

Would you like me to generate it?"

User: "Yes"

Augment: "Great! I need a few details:

1. Project name? (e.g., 'Company ERP')
2. Database name? (e.g., 'company_erp_db')
3. Frontend port? (default: 3000)
4. Backend port? (default: 5000)

[Collects answers]

Generati
ng project...

✅ Done! Your ERP system is ready at: ~/projects/company-erp

Next steps:
1. cd ~/projects/company-erp
2. Read README.md
3. Run: docker-compose up -d

Would you like help with setup?"
```

### Example 2: Generate AI Assistant

```
User: "Create an AI chatbot for customer support"

Augment: "Perfect! I'll use our AI Assistant template which includes:
- Chat interface
- Knowledge base (RAG)
- Multi-model support (GPT-4, Claude)
- Vector database for semantic search

Generating...

✅ Project created!

I've set it up with:
- React frontend with chat UI
- FastAPI backend with LangChain
- Pinecone for vector storage
- OpenAI GPT-4 integration

You'll need to add your OpenAI API key to .env

Want me to help you set it up?"
```

---

## Best Practices

### For Augment

1. **Always suggest templates** for new projects
2. **Explain template features** before generating
3. **Ask for confirmation** before generating
4. **Collect all variables** upfront
5. **Show progress** during gen
eration
6. **Provide next steps** after generation
7. **Offer customization help**

### For Users

1. **Review README.md** after generation
2. **Customize variables** in .env
3. **Read documentation** in docs/
4. **Test locally** before deployment
5. **Commit to Git** after customization

---

## Template Maintenance

### Adding New Templates

1. Create directory in `templates/`
2. Add template files
3. Create `README.md`
4. Create `config.json`
5. Test generation
6. Update this section

### Updating Templates

1. Modify template files
2. Update version in `config.json`
3. Update `README.md`
4. Test generation
5. Document changes

---

## Summary

**9 professional templates** covering:

1. ✅ **ERP System** - Complete business management
2. ✅ **Web Page** - Simple websites
3. ✅ **Web Page with Login** - Web applications
4. ✅ **ML Template** - Machine learning projects
5. ✅ **Test Template** - Comprehensive testing
6. ✅ **Email Template** - Professional emails
7. ✅ **AI Assistant** - Int

================================================================================
CRITICAL MISSING CONTENT - Deep Search Recovery
================================================================================

```bash
   mkdir -p /unneeded/models
   mv models/user_unified.py /unneeded/models/user_unified.removed.py
   mv models/users.py /unneeded/models/users.removed.py
   ```

4. **Add Pointer File**
   ```python
   # /unneeded/models/user_unified.removed.py
   """
   REMOVED: 2025-10-28
   REASON: Duplicate of models/user.py
   COMMIT: abc123def456
   CANONICAL: models/user.py
   
   This file was a duplicate and has been removed.
   All imports should use: from models.user import User
   """
   ```

5. **Document in Duplicates Log**
   ```markdown
   # /docs/Duplicates_Log.md
   
   ## 2025-10-28: User Model Consolidation
   
   **Canonical:** `models/user.py`
   
   **Removed Duplicates:**
   - `models/user_unified.py` → `/unneeded/models/user_unified.removed.py`
   - `models/users.py` → `/unneeded/models/users.removed.py`
   
   **Commit:** abc123def456
   
   **Files Updated:** 8 files
   - `services/auth_service.py`
   - `routes/user_routes.py`
   - (list all updated files)
   ```

C) CI ENFORCEMENT

```

```bash
# Update imports after moving/renaming module
python scripts/update_imports.py <old_module> <new_module>

# Example
python scripts/update_imports.py models.user_unified models.user

# Dry-run
python scripts/update_imports.py models.user_unified models.user --dry-run
```

```python
# backend/src/services/error_logger.py
import logging
from datetime import datetime
from models import ErrorLog

class ErrorLogger:
    @staticmethod
    def log_error(
        trace_id: str,
        error_type: str,
        error_message: str,
        stack_trace: str,
        user_id: int = None,
        request_data: dict = None
    ):
        """Log error to database for analysis"""
        error_log = ErrorLog(
            trace_id=trace_id,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            user_id=user_id,
            request_data=request_data,
            timestamp=datetime.utcnow()
        )
        db.session.add(error_log)
        db.session.commit()
        
        # Also log to file
        logging.error(
            f"[{trace_id}] {error_type}: {error_message}",
            extra={'stack_trace': stack_trace}
        )
        
        # Send alert if critical
        if error_type in ['DatabaseError', 'SecurityError']:
            send_alert_to_admin(trace_id, error_type, error_message)
```

```python
# scripts/generate_env.py
import secrets

def generate_secret_key(length=32):
    """Generate secure random key"""
    return secrets.token_hex(length)

def generate_env_file():
    """Generate .env file with secure defaults"""
    template = f"""# Generated .env file - {datetime.now().isoformat()}

# IMPORTANT: Review and update all values before use!

APP_ENV=development
SECRET_KEY={generate_secret_key()}
JWT_SECRET_KEY={generate_secret_key()}

DB_HOST=localhost
DB_PORT=5432
DB_NAME={your_database_name}
DB_USER=postgres
DB_PASSWORD={generate_secret_key(16)}

# Add other variables from .env.example
"""
    
    with open('.env', 'w') as f:
        f.write(template)
    
    print("✅ .env file generated!")
    print("⚠️ Please review and update the values before running the application.")

if __name__ == '__main__':
    generate_env_file()
```

```python
   # Before (scattered)
   from models.user import User
   from models.user_unified import User
   from models.users import User
   
   # After (consolidated)
   from models.user import User  # CANONICAL
   ```

3. **Move Duplicates to /unneeded**
   ```bash
   mkdir -p /unneeded/models
   mv models/user_unified.py /unneeded/models/user_unified.removed.py
   mv models/users.py /unneeded/models/users.removed.py
   ```

4. **Add Pointer File**
   ```python
   # /unneeded/models/user_unified.removed.py
   """
   REMOVED: 2025-10-28
   REASON: Duplicate of models/user.py
   COMMIT: abc123def456
   CANONICAL: models/user.py
   
   This file was a duplicate and has been removed.
   All imports should use: from models.user import User
   """
   ```

5. **Document in Duplicates Log**
   ```markdown
   # /docs/Duplicates_Log.md
   
   ## 2025-10-28: User Model Consolidation
   
   **Canonical:** `models/user.py`
   
   **Removed Duplicates:**
   - `models/user_unified.py` → `/unneeded/models/user_unified.removed.py`
   - `models/users.py` → `/unneeded/models/users.removed.py`
   
   **Commit:** abc123def456
   
   **Files Updated:** 8 files
   - `services/auth_service.py`
   - `routes/user_routes.py`
   - (list all updated files)
   ```

C) CI ENFORCEMENT

```

```python
"""Core base models and mixins"""

from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, Field

class BaseModel(PydanticBaseModel):
    """Base for all Pydantic models"""
    class Config:
        from_attributes = True
        validate_assignment = True

class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SoftDeleteMixin(BaseModel):
    is_deleted: bool = False
    deleted_at: datetime | None = None
```

```python
"""Central registry for all definitions"""

from .common import *
from .core import *
from .custom import *

__all__ = [
    # Common
    'Status', 'UserRole', 'APIResponse',
    # Core
    'BaseModel', 'TimestampMixin', 'SoftDeleteMixin',
    # Custom
    'ProjectStatus', 'Priority',
]
```

```python
#!/usr/bin/env python3
"""Analyze module dependencies and suggest build order."""

import ast
from pathlib import Path
from collections import defaultdict

def get_dependencies(file_path):
    """Get internal dependencies of a module."""
    with open(file_path) as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return set()
    
    deps = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and not node.module.startswith(('os', 'sys', 'json')):
                # Only internal imports
                if not node.module.startswith(('django', 'flask', 'fastapi')):
                    deps.add(node.module.split('.')[0])
    
    return deps

def topological_sort(modules):
    """Sort modules by dependency order."""
    # Build dependency graph
    graph = {}
    in_degree = defaultdict(int)
    
    for module, deps in modules.items():
        graph[module] = deps
        for dep in deps:
            in_degree[dep] += 1
    
    # Find modules with no dependencies
    queue = [m for m in graph if in_degree[m] == 0]
    result = []
    
    while queue:
        module = queue.pop(0)
        result.append(module)
        
        for dep in graph.get(module, []):
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)
    
    return result

def main():
    """Analyze and print dependency order."""
    modules = {}
    
    for py_file in Path('.').rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        module_name = str(py_file).replace('/', '.').replace('.py', '')
        deps = get_dependencies(py_file)
        modules[module_name] = deps
    
    order = topological_sort(modules)
    
    print("📊 Module Build Order (Least Dependent First):\n")
    for i, module in enumerate(order, 1):
        deps = modules.get(module, set())
        print(f"{i:3d}. {module}")
        if deps:
            print(f"     Dependencies: {', '.join(sorted(deps))}")
    
    print(f"\n✅ Total modules: {len(order)}")
    print(f"✅ Start with: {order[0] if order else 'None'}")

if __name__ == '__main__':
    main()
```

```python
# In multiple files
def view1(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    # ...

def view2(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    # ...
```

```python
"""
File: module_name/models/main_model.py
Module: module_name.models.main_model
Created: 2025-01-15
Author: Team
Description: النموذج الرئيسي للوحدة

Dependencies:
- django.db.models
- django.contrib.auth.models
"""

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class MainModel(models.Model):
    """
    النموذج الرئيسي للوحدة.
    
    يحتوي على جميع الحقول والعلاقات الأساسية.
    """
    
    # حالات النموذج
    STATE_DRAFT = 'draft'
    STATE_CONFIRMED = 'confirmed'
    STATE_CANCELLED = 'cancelled'
    
    STATES = [
        (STATE_DRAFT, 'مسودة'),
        (STATE_CONFIRMED, 'مؤكد'),
        (STATE_CANCELLED, 'ملغي'),
    ]
    
    # الحقول الأساسية
    name = models.CharField('الاسم', max_length=255)
    code = models.CharField('الرمز', max_length=50, unique=True)
    description = models.TextField('الوصف', blank=True)
    
    # العلاقات
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='المستخدم',
        related_name='%(class)s_records'
    )
    
    # الحالة
    state = models.CharField(
        'الحالة',
        max_length=20,
        choices=STATES,
        default=STATE_DRAFT
    )
    
    # التواريخ
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    confirmed_at = models.DateTimeField('تاريخ التأكيد', null=True, blank=True)
    
    # الحقول المحسوبة
    total = models.DecimalField('الإجمالي', max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'النموذج الرئيسي'
        verbose_name_plural = 'النماذج الرئيسية'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['state', 'created_at']),
        ]
    
    def __str__(self):
        """تمثيل نصي للنموذج."""
        return f"{self.code} - {self.name}"
    
    def confirm(self):
        """
        تأكيد النموذج.
        
        يقوم بتغيير الحالة إلى مؤكد وحفظ تاريخ التأكيد.
        
        Raises:
            ValueError: إذا كان النموذج ليس في حالة مسودة
        """
        if self.state != self.STATE_DRAFT:
            raise ValueError("لا يمكن تأكيد نموذج غير مسودة")
        
        from django.utils import timezone
        self.state = self.STATE_CONFIRMED
        self.confirmed_at = timezone.now()
        self.save()
    
    def cancel(self):
        """
        إلغاء النموذج.
        
        يقوم بتغيير الحالة إلى ملغي.
        
        Raises:
            ValueError: إذا كان النموذج ملغي بالفعل
        """
        if self.state == self.STATE_CANCELLED:
            raise ValueError("النموذج ملغي بالفعل")
        
        self.state = self.STATE_CANCELLED
        self.save()
    
    def compute_total(self):
        """
        حساب الإجمالي.
        
        يقوم بحساب الإجمالي من العناصر المرتبطة.
        
        Returns:
            Decimal: الإجمالي المحسوب
        """
        total = sum(
            item.subtotal for item in self.items.all()
        )
        self.total = Decimal(str(total))
        self.save()
        return self.total
```

```python
"""
File: config/constants.py
Module: config.constants
Created: 2025-01-15
Author: Team
Description: System-wide constants and definitions

Dependencies: None
"""

from decimal import Decimal

# Application
APP_NAME = "{YOUR_PROJECT_NAME}"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Enterprise Resource Planning System"

# Ports (SINGLE SOURCE OF TRUTH)
BACKEND_PORT = 8000
FRONTEND_PORT = 3000
API_PORT = 8000

# URLs
BACKEND_URL = f"http://{HOST}:{BACKEND_PORT}"
FRONTEND_URL = f"http://{HOST}:{FRONTEND_PORT}"
API_BASE_URL = f"{BACKEND_URL}/api"

# Database
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Business Rules
DEFAULT_TAX_RATE = Decimal('0.15')  # 15%
DEFAULT_CURRENCY = 'SAR'
DEFAULT_LANGUAGE = 'ar'

# File Upload
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
ALLOWED_DOCUMENT_TYPES = ['application/pdf', 'application/msword']

# Validation
MIN_PASSWORD_LENGTH = 8
MAX_USERNAME_LENGTH = 50
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# States
STATE_DRAFT = 'draft'
STATE_CONFIRMED = 'confirmed'
STATE_CANCELLED = 'cancelled'
STATE_DONE = 'done'

COMMON_STATES = [
    (STATE_DRAFT, 'مسودة'),
    (STATE_CONFIRMED, 'مؤكد'),
    (STATE_CANCELLED, 'ملغي'),
    (STATE_DONE, 'منتهي'),
]

# Permissions
PERM_VIEW = 'view'
PERM_CREATE = 'create'
PERM_EDIT = 'edit'
PERM_DELETE = 'delete'
PERM_ADMIN = 'admin'

ALL_PERMISSIONS = [PERM_VIEW, PERM_CREATE, PERM_EDIT, PERM_DELETE, PERM_ADMIN]

# Error Messages
ERROR_REQUIRED_FIELD = "هذا الحقل مطلوب"
ERROR_INVALID_EMAIL = "البريد الإلكتروني غير صحيح"
ERROR_PASSWORD_TOO_SHORT = f"كلمة المرور يجب أن تكون {MIN_PASSWORD_LENGTH} أحرف على الأقل"
ERROR_UNAUTHORIZED = "غير مصرح"
ERROR_NOT_FOUND = "غير موجود"
ERROR_INTERNAL_SERVER = "خطأ في الخادم"

# Success Messages
SUCCESS_CREATED = "تم الإنشاء بنجاح"
SUCCESS_UPDATED = "تم التحديث بنجاح"
SUCCESS_DELETED = "تم الحذف بنجاح"
SUCCESS_CONFIRMED = "تم التأكيد بنجاح"
```

```python
"""
File: config/definitions/types.py
Module: config.definitions.types
Created: 2025-01-15
Author: Team
Description: Type definitions and type hints
"""

from typing import TypedDict, Literal, Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime

# State types
StateType = Literal['draft', 'confirmed', 'cancelled', 'done']
PermissionType = Literal['view', 'create', 'edit', 'delete', 'admin']

# API Response types
class APIResponse(TypedDict):
    """Standard API response structure."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]]
    errors: Optional[List[str]]

class PaginatedResponse(TypedDict):
    """Paginated API response."""
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Dict[str, Any]]

# Business types
class OrderItem(TypedDict):
    """Order item structure."""
    product_id: int
    quantity: int
    price: Decimal
    subtotal: Decimal

class Order(TypedDict):
    """Order structure."""
    id: int
    code: str
    customer_id: int
    items: List[OrderItem]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    state: StateType
    created_at: datetime
```

```python
#!/usr/bin/env python3
"""
Analyze gaps between design and implementation.

File: scripts/analyze_gaps.py
Module: scripts.analyze_gaps
Created: 2025-01-15
Author: Team
Description: Compare design specs with actual implementation
"""

import ast
import json
from pathlib import Path
from typing import Dict, List, Set

def find_api_endpoints() -> Set[str]:
    """Find all defined API endpoints."""
    endpoints = set()
    
    for py_file in Path('.').rglob('*views.py'):
        with open(py_file) as f:
            content = f.read()
        
        # Find @api_view decorators
        import re
        patterns = re.findall(r'@api_view\([\'"]([A-Z]+)[\'"]\)', content)
        # Find route definitions
        routes = re.findall(r'path\([\'"]([^\'\"]+)[\'"]', content)
        
        endpoints.update(routes)
    
    return endpoints

def find_frontend_routes() -> Set[str]:
    """Find all frontend routes."""
    routes = set()
    
    # Check React Router
    for tsx_file in Path('.').rglob('*.tsx'):
        with open(tsx_file) as f:
            content = f.read()
        
        import re
        patterns = re.findall(r'<Route\s+path=[\'"]([^\'\"]+)[\'"]', content)
        routes.update(patterns)
    
    return routes

def find_database_models() -> Set[str]:
    """Find all database models."""
    models = set()
    
    for py_file in Path('.').rglob('models.py'):
        with open(py_file) as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                continue
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's a Django model
                for base in node.bases:
                    if isinstance(base, ast.Attribute):
                        if base.attr == 'Model':
                            models.add(node.name)
    
    return models

def load_design_spec(spec_file: str) -> Dict:
    """Load design specification."""
    with open(spec_file) as f:
        return json.load(f)

def analyze_gaps(spec_file: str = 'docs/design_spec.json'):
    """Analyze gaps between design and implementation."""
    print("🔍 Analyzing Design vs Implementation Gaps\n")
    
    # Load design spec
    try:
        spec = load_design_spec(spec_file)
    except FileNotFoundError:
        print(f"⚠️  Design spec not found: {spec_file}")
        print("   Create docs/design_spec.json with your design")
        return
    
    # Find implementation
    api_endpoints = find_api_endpoints()
    frontend_routes = find_frontend_routes()
    db_models = find_database_models()
    
    # Compare
    gaps = []
    
    # Check API endpoints
    if 'api_endpoints' in spec:
        for endpoint in spec['api_endpoints']:
            if endpoint not in api_endpoints:
                gaps.append(f"Missing API endpoint: {endpoint}")
    
    # Check frontend routes
    if 'frontend_routes' in spec:
        for route in spec['frontend_routes']:
            if route not in frontend_routes:
                gaps.append(f"Missing frontend route: {route}")
    
    # Check database models
    if 'models' in spec:
        for model in spec['models']:
            if model not in db_models:
                gaps.append(f"Missing database model: {model}")
    
    # Report
    if gaps:
        print("❌ Gaps Found:\n")
        for gap in gaps:
            print(f"  • {gap}")
        print(f"\nTotal gaps: {len(gaps)}")
    else:
        print("✅ No gaps found! Design matches implementation.")
    
    # Summary
    print("\n📊 Summary:")
    print(f"  API Endpoints: {len(api_endpoints)} implemented")
    print(f"  Frontend Routes: {len(frontend_routes)} implemented")
    print(f"  Database Models: {len(db_models)} implemented")

if __name__ == '__main__':
    analyze_gaps()
```

```python
# Cannot be updated automatically
module_name = "models.user_unified"
mod = __import__(module_name)
```

```python
# myapp/__init__.py
"""
MyApp - Main application package

Subpackages:
    - core: Core functionality
    - models: Data models
    - services: Business logic
    - api: API endpoints
    - utils: Utility functions
"""

# Import commonly used items from subpackages
from .core import App, Config
from .models import User, Session
from .services import UserService, AuthService

# Version info
from .version import __version__, __version_info__

# Public API
__all__ = [
    # Core
    'App',
    'Config',
    # Models
    'User',
    'Session',
    # Services
    'UserService',
    'AuthService',
    # Version
    '__version__',
    '__version_info__',
]

# Subpackage references (for documentation)
__subpackages__ = [
    'core',
    'models',
    'services',
    'api',
    'utils',
]
```

```python
# ❌ PROBLEM: Circular dependency
# models/__init__.py
from .user import User
from .post import Post  # Post imports User, User imports Post!

# ✅ SOLUTION 1: Import at function level
# models/user.py
def get_user_posts(user_id):
    from .post import Post  # Import here, not at module level
    return Post.query.filter_by(user_id=user_id).all()

# ✅ SOLUTION 2: Use TYPE_CHECKING
# models/user.py
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .post import Post

class User:
    def get_posts(self) -> List['Post']:  # String annotation
        from .post import Post
        return Post.query.filter_by(user_id=self.id).all()

# ✅ SOLUTION 3: Restructure - create base module
# models/base.py - common base classes
# models/user.py - imports from base
# models/post.py - imports from base
# models/__init__.py - imports both
```

```python
# enterprise_app/__init__.py
"""
Enterprise Application

Large-scale application with multiple subpackages.
Import subpackages explicitly for better organization.

Usage:
    # Import main app
    from enterprise_app import App
    
    # Import specific modules
    from enterprise_app.core import Config
    from enterprise_app.models import User
    from enterprise_app.services.auth import AuthService
"""

# Only expose the absolute essentials at top level
from .core import App
from ._version import __version__

# Make subpackages easily accessible
from . import (
    core,
    models,
    services,
    api,
    utils,
    exceptions,
)

# Minimal public API at package level
__all__ = [
    'App',
    '__version__',
    # Subpackages
    'core',
    'models',
    'services',
    'api',
    'utils',
    'exceptions',
]

# Package metadata
__author__ = 'Enterprise Team'
__license__ = 'Proprietary'
__copyright__ = 'Copyright 2025, Enterprise Corp'
```

