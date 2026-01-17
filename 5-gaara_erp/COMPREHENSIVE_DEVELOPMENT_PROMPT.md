# برومبت التطوير الشامل - نظام إدارة المخزون العربي
## Comprehensive Development Prompt - Arabic Inventory Management System

---

## 🎯 مهمة التطوير الرئيسية

أنت مطور برمجيات خبير متخصص في الأمان والأداء وتجربة المستخدم. مهمتك هي إصلاح وتطوير نظام إدارة المخزون العربي ليصبح نظاماً آمناً ومحترفاً وجاهزاً للإنتاج.

### معلومات المشروع:
- **النوع:** نظام إدارة مخزون شامل
- **التقنيات:** React (Frontend) + Flask (Backend) + SQLite/PostgreSQL
- **اللغة:** دعم كامل للعربية مع RTL
- **الهدف:** منافسة Odoo في الأسواق العربية
- **الحالة الحالية:** غير آمن للإنتاج - يحتاج إصلاح شامل

---

## 🚨 المشاكل الحرجة المكتشفة (يجب إصلاحها فوراً)

### 1. مشاكل الأمان الحرجة (289 مشكلة)

#### أ. ثغرات حقن SQL (8 مواقع حرجة)
```python
# ❌ خطأ موجود - ثغرة حقن SQL
def search_products(query):
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    return db.execute(sql)

# ✅ الإصلاح المطلوب
def search_products(query):
    sql = "SELECT * FROM products WHERE name LIKE %s"
    return db.execute(sql, (f'%{query}%',))
```

**المواقع المتأثرة:**
- `backend/src/routes/products.py` - خط 45, 67, 89
- `backend/src/routes/inventory.py` - خط 23, 156
- `backend/src/services/reports.py` - خط 78, 134, 201

#### ب. عدم وجود حماية CSRF (45+ نموذج)
```python
# ❌ خطأ موجود - بدون حماية CSRF
@app.route('/api/products', methods=['POST'])
def add_product():
    name = request.form['name']
    return create_product(name)

# ✅ الإصلاح المطلوب
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

@app.route('/api/products', methods=['POST'])
@csrf.exempt  # للAPI، أو استخدم token validation
def add_product():
    # التحقق من CSRF token للنماذج
    if not csrf.validate():
        return jsonify({'error': 'CSRF token missing'}), 400
    name = request.form['name']
    return create_product(name)
```

#### ج. ضعف المصادقة وتشفير كلمات المرور
```python
# ❌ خطأ موجود - تشفير ضعيف
import hashlib
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    return stored_password == hashlib.md5(provided_password.encode()).hexdigest()

# ✅ الإصلاح المطلوب
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def check_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)

# إضافة JWT للمصادقة
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
jwt = JWTManager(app)
```

#### د. عدم وجود رؤوس الأمان
```python
# ✅ إضافة رؤوس الأمان المطلوبة
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
```

#### هـ. عدم التحقق من المدخلات (156+ نقطة دخول)
```python
# ❌ خطأ موجود - بدون تحقق
@app.route('/api/products', methods=['POST'])
def add_product():
    name = request.json['name']  # خطر!
    price = request.json['price']  # خطر!
    category_id = request.json['category_id']  # خطر!

# ✅ الإصلاح المطلوب
from marshmallow import Schema, fields, validate, ValidationError

class ProductSchema(Schema):
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'اسم المنتج مطلوب'}
    )
    price = fields.Float(
        required=True, 
        validate=validate.Range(min=0, max=1000000),
        error_messages={'required': 'السعر مطلوب'}
    )
    category_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={'required': 'تصنيف المنتج مطلوب'}
    )

@app.route('/api/products', methods=['POST'])
@jwt_required()
def add_product():
    schema = ProductSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # التحقق من وجود التصنيف
    if not Category.query.get(data['category_id']):
        return jsonify({'error': 'التصنيف غير موجود'}), 400
    
    return create_product(data)
```

### 2. مشاكل الأداء الحرجة

#### أ. مشاكل N+1 في قاعدة البيانات
```python
# ❌ خطأ موجود - N+1 Problem
def get_products_with_categories():
    products = Product.query.all()
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'category': product.category.name  # استعلام إضافي لكل منتج!
        })
    return result

# ✅ الإصلاح المطلوب
def get_products_with_categories():
    products = Product.query.options(
        joinedload(Product.category)
    ).all()
    
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'category': product.category.name  # بدون استعلام إضافي
        })
    return result
```

#### ب. عدم وجود فهارس في قاعدة البيانات
```sql
-- ✅ إضافة الفهارس المطلوبة
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_inventory_product_id ON inventory(product_id);
CREATE INDEX idx_inventory_warehouse_id ON inventory(warehouse_id);
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_sales_customer_id ON sales(customer_id);
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_products_barcode ON products(barcode);
```

#### ج. عدم وجود Caching
```python
# ✅ إضافة نظام Caching شامل
from flask_caching import Cache
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@app.route('/api/categories')
@cache.cached(timeout=3600)  # cache لمدة ساعة
def get_categories():
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'name_ar': cat.name_ar
    } for cat in Category.query.all()])

@app.route('/api/products')
def get_products():
    page = request.args.get('page', 1, type=int)
    cache_key = f'products_page_{page}'
    
    result = cache.get(cache_key)
    if result is None:
        products = Product.query.paginate(
            page=page, per_page=20, error_out=False
        )
        result = {
            'products': [product.to_dict() for product in products.items],
            'pagination': {
                'page': products.page,
                'pages': products.pages,
                'total': products.total
            }
        }
        cache.set(cache_key, result, timeout=300)  # 5 دقائق
    
    return jsonify(result)
```

### 3. مشاكل تجربة المستخدم (66 مشكلة إمكانية وصول)

#### أ. مشاكل إمكانية الوصول
```html
<!-- ❌ خطأ موجود - صور بدون alt -->
<img src="/images/product1.jpg">
<img src="/images/product2.jpg" alt="">
<img src="/images/product3.jpg" alt="image">

<!-- ✅ الإصلاح المطلوب -->
<img src="/images/product1.jpg" alt="لابتوب ديل إنسبايرون 15 - 8GB RAM، 256GB SSD">
<img src="/images/product2.jpg" alt="ماوس لاسلكي لوجيتك MX Master 3 - أسود">
<img src="/images/product3.jpg" alt="لوحة مفاتيح ميكانيكية كورسير K95 - إضاءة RGB">

<!-- ❌ خطأ موجود - نماذج بدون labels -->
<input type="text" name="product_name" placeholder="اسم المنتج">
<input type="number" name="price" placeholder="السعر">

<!-- ✅ الإصلاح المطلوب -->
<label for="product_name">اسم المنتج *</label>
<input type="text" id="product_name" name="product_name" 
       placeholder="اسم المنتج" required 
       aria-describedby="product_name_help">
<small id="product_name_help">أدخل اسم المنتج باللغة العربية أو الإنجليزية</small>

<label for="price">السعر *</label>
<input type="number" id="price" name="price" 
       placeholder="السعر" required min="0" step="0.01"
       aria-describedby="price_help">
<small id="price_help">السعر بالريال السعودي</small>
```

#### ب. مشاكل دعم العربية وRTL
```css
/* ❌ خطأ موجود - تخطيط ثابت */
.sidebar {
    float: left;
    margin-right: 20px;
    text-align: left;
}

.product-card {
    text-align: left;
    padding-left: 15px;
}

/* ✅ الإصلاح المطلوب */
.sidebar {
    float: inline-start;
    margin-inline-end: 20px;
    text-align: start;
}

[dir="rtl"] .sidebar {
    float: right;
    margin-left: 20px;
    margin-right: 0;
}

.product-card {
    text-align: start;
    padding-inline-start: 15px;
}

[dir="rtl"] .product-card {
    text-align: right;
    padding-right: 15px;
    padding-left: 0;
}

/* إضافة خطوط عربية */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

body {
    font-family: 'Cairo', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    direction: rtl;
}

[lang="en"] {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    direction: ltr;
}
```

#### ج. مشاكل التصميم المتجاوب
```css
/* ❌ خطأ موجود - عدد قليل من media queries */
@media (max-width: 768px) {
    .container { width: 100%; }
}

/* ✅ الإصلاح المطلوب - نظام responsive شامل */
/* Mobile First Approach */
.container {
    width: 100%;
    padding: 0 15px;
    margin: 0 auto;
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
    .container { max-width: 540px; }
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
    .container { max-width: 720px; }
    .sidebar { display: block; }
    .main-content { margin-inline-start: 250px; }
}

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
    .container { max-width: 960px; }
}

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
    .container { max-width: 1140px; }
}

/* RTL specific responsive */
[dir="rtl"] .main-content {
    margin-right: 250px;
    margin-left: 0;
}

@media (max-width: 767px) {
    [dir="rtl"] .main-content {
        margin-right: 0;
    }
}
```

---

## 🔧 التطويرات المطلوبة بالتفصيل

### 1. إعادة هيكلة الكود (20 ملف عالي التعقيد)

#### أ. تبسيط ملف المنتجات
```python
# ❌ ملف معقد - backend/src/routes/products.py (تعقيد: 15)
# الملف الحالي يحتوي على 500+ سطر مع منطق معقد

# ✅ إعادة الهيكلة المطلوبة
# تقسيم إلى ملفات منفصلة:

# backend/src/routes/products/__init__.py
from .products_routes import products_bp
from .products_api import products_api_bp

# backend/src/routes/products/products_routes.py
from flask import Blueprint
from ..services.product_service import ProductService
from ..validators.product_validator import ProductValidator

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def list_products():
    service = ProductService()
    return service.get_products_paginated(request.args)

@products_bp.route('/products/<int:product_id>')
def get_product(product_id):
    service = ProductService()
    return service.get_product_by_id(product_id)

# backend/src/services/product_service.py
class ProductService:
    def __init__(self):
        self.validator = ProductValidator()
    
    def get_products_paginated(self, args):
        page = args.get('page', 1, type=int)
        per_page = args.get('per_page', 20, type=int)
        search = args.get('search', '')
        category_id = args.get('category_id', type=int)
        
        query = Product.query
        
        if search:
            query = query.filter(Product.name.contains(search))
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        products = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'products': [p.to_dict() for p in products.items],
            'pagination': {
                'page': products.page,
                'pages': products.pages,
                'total': products.total,
                'has_next': products.has_next,
                'has_prev': products.has_prev
            }
        }
```

#### ب. إنشاء طبقة خدمات منفصلة
```python
# ✅ إنشاء طبقة خدمات شاملة
# backend/src/services/base_service.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class BaseService(ABC):
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_by_id(self, id: int) -> Optional[Any]:
        return self.model_class.query.get(id)
    
    def get_all(self) -> List[Any]:
        return self.model_class.query.all()
    
    def create(self, data: Dict) -> Any:
        instance = self.model_class(**data)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def update(self, id: int, data: Dict) -> Optional[Any]:
        instance = self.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            db.session.commit()
        return instance
    
    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False

# backend/src/services/inventory_service.py
class InventoryService(BaseService):
    def __init__(self):
        super().__init__(Inventory)
    
    def get_stock_level(self, product_id: int, warehouse_id: int = None) -> int:
        query = Inventory.query.filter_by(product_id=product_id)
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)
        
        total_stock = db.session.query(
            func.sum(Inventory.quantity)
        ).filter_by(product_id=product_id).scalar() or 0
        
        return total_stock
    
    def update_stock(self, product_id: int, quantity_change: int, 
                    warehouse_id: int, transaction_type: str) -> bool:
        try:
            # إنشاء معاملة مخزون
            transaction = InventoryTransaction(
                product_id=product_id,
                warehouse_id=warehouse_id,
                quantity_change=quantity_change,
                transaction_type=transaction_type,
                timestamp=datetime.utcnow()
            )
            db.session.add(transaction)
            
            # تحديث المخزون
            inventory = Inventory.query.filter_by(
                product_id=product_id,
                warehouse_id=warehouse_id
            ).first()
            
            if inventory:
                inventory.quantity += quantity_change
            else:
                inventory = Inventory(
                    product_id=product_id,
                    warehouse_id=warehouse_id,
                    quantity=max(0, quantity_change)
                )
                db.session.add(inventory)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
```

### 2. تحسين نماذج قاعدة البيانات

#### أ. إضافة العلاقات المفقودة
```python
# ✅ تحسين نماذج قاعدة البيانات
# backend/src/models/product.py
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    name_ar = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    barcode = db.Column(db.String(50), unique=True, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    cost = db.Column(db.Numeric(10, 2))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), index=True)
    unit_of_measure = db.Column(db.String(20), default='piece')
    min_stock_level = db.Column(db.Integer, default=0)
    max_stock_level = db.Column(db.Integer, default=1000)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    category = db.relationship('Category', backref='products')
    supplier = db.relationship('Supplier', backref='products')
    inventory_items = db.relationship('Inventory', backref='product', cascade='all, delete-orphan')
    sale_items = db.relationship('SaleItem', backref='product')
    
    # فهارس مركبة
    __table_args__ = (
        db.Index('idx_product_category_active', 'category_id', 'is_active'),
        db.Index('idx_product_supplier_active', 'supplier_id', 'is_active'),
    )
    
    def to_dict(self, include_inventory=False):
        data = {
            'id': self.id,
            'name': self.name,
            'name_ar': self.name_ar,
            'description': self.description,
            'description_ar': self.description_ar,
            'barcode': self.barcode,
            'price': float(self.price) if self.price else 0,
            'cost': float(self.cost) if self.cost else 0,
            'category': self.category.to_dict() if self.category else None,
            'supplier': self.supplier.to_dict() if self.supplier else None,
            'unit_of_measure': self.unit_of_measure,
            'min_stock_level': self.min_stock_level,
            'max_stock_level': self.max_stock_level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_inventory:
            data['total_stock'] = sum(item.quantity for item in self.inventory_items)
            data['warehouses'] = [
                {
                    'warehouse_id': item.warehouse_id,
                    'warehouse_name': item.warehouse.name,
                    'quantity': item.quantity
                } for item in self.inventory_items
            ]
        
        return data
    
    @classmethod
    def search(cls, query, category_id=None, supplier_id=None, is_active=True):
        search_query = cls.query
        
        if is_active is not None:
            search_query = search_query.filter(cls.is_active == is_active)
        
        if category_id:
            search_query = search_query.filter(cls.category_id == category_id)
        
        if supplier_id:
            search_query = search_query.filter(cls.supplier_id == supplier_id)
        
        if query:
            search_filter = db.or_(
                cls.name.contains(query),
                cls.name_ar.contains(query),
                cls.barcode.contains(query)
            )
            search_query = search_query.filter(search_filter)
        
        return search_query
```

#### ب. إضافة نموذج معاملات المخزون
```python
# ✅ إضافة نموذج تتبع معاملات المخزون
# backend/src/models/inventory_transaction.py
class InventoryTransaction(db.Model):
    __tablename__ = 'inventory_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    transaction_type = db.Column(db.String(20), nullable=False, index=True)  # 'in', 'out', 'transfer', 'adjustment'
    quantity_change = db.Column(db.Integer, nullable=False)
    quantity_before = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)
    reference_type = db.Column(db.String(20))  # 'sale', 'purchase', 'transfer', 'adjustment'
    reference_id = db.Column(db.Integer)
    notes = db.Column(db.Text)
    notes_ar = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # العلاقات
    product = db.relationship('Product')
    warehouse = db.relationship('Warehouse')
    user = db.relationship('User')
    
    # فهارس مركبة
    __table_args__ = (
        db.Index('idx_transaction_product_date', 'product_id', 'timestamp'),
        db.Index('idx_transaction_warehouse_date', 'warehouse_id', 'timestamp'),
        db.Index('idx_transaction_type_date', 'transaction_type', 'timestamp'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'warehouse': self.warehouse.to_dict() if self.warehouse else None,
            'user': self.user.to_dict() if self.user else None,
            'transaction_type': self.transaction_type,
            'quantity_change': self.quantity_change,
            'quantity_before': self.quantity_before,
            'quantity_after': self.quantity_after,
            'reference_type': self.reference_type,
            'reference_id': self.reference_id,
            'notes': self.notes,
            'notes_ar': self.notes_ar,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
```

### 3. تحسين الواجهة الأمامية (React)

#### أ. إنشاء نظام تصميم موحد
```javascript
// ✅ إنشاء نظام تصميم شامل
// frontend/src/theme/index.js
export const theme = {
  colors: {
    primary: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      500: '#0ea5e9',
      600: '#0284c7',
      700: '#0369a1',
      900: '#0c4a6e'
    },
    secondary: {
      50: '#fefce8',
      100: '#fef3c7',
      500: '#eab308',
      600: '#ca8a04',
      700: '#a16207'
    },
    success: {
      50: '#f0fdf4',
      500: '#22c55e',
      700: '#15803d'
    },
    error: {
      50: '#fef2f2',
      500: '#ef4444',
      700: '#dc2626'
    },
    warning: {
      50: '#fffbeb',
      500: '#f59e0b',
      700: '#d97706'
    }
  },
  fonts: {
    arabic: "'Cairo', 'Amiri', 'Noto Sans Arabic', sans-serif",
    english: "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    mono: "'Fira Code', 'Consolas', monospace"
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem'
  },
  borderRadius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem'
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
  }
};

// frontend/src/components/ui/Button.jsx
import React from 'react';
import { theme } from '../../theme';

export const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
  className = '',
  ...props 
}) => {
  const baseStyles = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: '500',
    borderRadius: theme.borderRadius.md,
    border: 'none',
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'all 0.2s ease-in-out',
    fontFamily: theme.fonts.arabic
  };

  const variantStyles = {
    primary: {
      backgroundColor: theme.colors.primary[500],
      color: 'white',
      '&:hover': {
        backgroundColor: theme.colors.primary[600]
      }
    },
    secondary: {
      backgroundColor: theme.colors.secondary[500],
      color: 'white',
      '&:hover': {
        backgroundColor: theme.colors.secondary[600]
      }
    },
    outline: {
      backgroundColor: 'transparent',
      color: theme.colors.primary[500],
      border: `1px solid ${theme.colors.primary[500]}`,
      '&:hover': {
        backgroundColor: theme.colors.primary[50]
      }
    }
  };

  const sizeStyles = {
    sm: {
      padding: `${theme.spacing.sm} ${theme.spacing.md}`,
      fontSize: '0.875rem'
    },
    md: {
      padding: `${theme.spacing.md} ${theme.spacing.lg}`,
      fontSize: '1rem'
    },
    lg: {
      padding: `${theme.spacing.lg} ${theme.spacing.xl}`,
      fontSize: '1.125rem'
    }
  };

  return (
    <button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      style={{
        ...baseStyles,
        ...variantStyles[variant],
        ...sizeStyles[size],
        opacity: disabled ? 0.6 : 1
      }}
      className={className}
      {...props}
    >
      {loading && (
        <svg 
          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24"
        >
          <circle 
            className="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4"
          ></circle>
          <path 
            className="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      )}
      {children}
    </button>
  );
};
```

#### ب. إنشاء مكونات إمكانية الوصول
```javascript
// ✅ مكون نموذج مع إمكانية وصول كاملة
// frontend/src/components/forms/FormField.jsx
import React from 'react';
import { theme } from '../../theme';

export const FormField = ({ 
  label, 
  labelAr,
  name, 
  type = 'text', 
  value, 
  onChange, 
  error, 
  required = false,
  disabled = false,
  placeholder,
  placeholderAr,
  helpText,
  helpTextAr,
  className = '',
  ...props 
}) => {
  const fieldId = `field-${name}`;
  const helpId = `${fieldId}-help`;
  const errorId = `${fieldId}-error`;
  
  const currentLang = document.documentElement.lang || 'ar';
  const isRTL = currentLang === 'ar';

  return (
    <div className={`form-field ${className}`} style={{ marginBottom: theme.spacing.lg }}>
      <label 
        htmlFor={fieldId}
        style={{
          display: 'block',
          fontWeight: '500',
          marginBottom: theme.spacing.sm,
          color: error ? theme.colors.error[700] : '#374151',
          fontFamily: theme.fonts.arabic
        }}
      >
        {isRTL ? labelAr || label : label}
        {required && <span style={{ color: theme.colors.error[500] }}>*</span>}
      </label>
      
      <input
        id={fieldId}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        disabled={disabled}
        required={required}
        placeholder={isRTL ? placeholderAr || placeholder : placeholder}
        aria-describedby={`${helpText ? helpId : ''} ${error ? errorId : ''}`.trim()}
        aria-invalid={error ? 'true' : 'false'}
        style={{
          width: '100%',
          padding: theme.spacing.md,
          border: `1px solid ${error ? theme.colors.error[500] : '#d1d5db'}`,
          borderRadius: theme.borderRadius.md,
          fontSize: '1rem',
          fontFamily: theme.fonts.arabic,
          direction: isRTL ? 'rtl' : 'ltr',
          textAlign: isRTL ? 'right' : 'left',
          '&:focus': {
            outline: 'none',
            borderColor: theme.colors.primary[500],
            boxShadow: `0 0 0 3px ${theme.colors.primary[100]}`
          }
        }}
        {...props}
      />
      
      {helpText && (
        <small 
          id={helpId}
          style={{
            display: 'block',
            marginTop: theme.spacing.sm,
            color: '#6b7280',
            fontSize: '0.875rem',
            fontFamily: theme.fonts.arabic
          }}
        >
          {isRTL ? helpTextAr || helpText : helpText}
        </small>
      )}
      
      {error && (
        <div 
          id={errorId}
          role="alert"
          style={{
            display: 'block',
            marginTop: theme.spacing.sm,
            color: theme.colors.error[700],
            fontSize: '0.875rem',
            fontFamily: theme.fonts.arabic
          }}
        >
          {error}
        </div>
      )}
    </div>
  );
};
```

#### ج. تحسين إدارة الحالة
```javascript
// ✅ إنشاء Context للإدارة الشاملة للحالة
// frontend/src/context/AppContext.jsx
import React, { createContext, useContext, useReducer, useEffect } from 'react';

const AppContext = createContext();

const initialState = {
  user: null,
  language: 'ar',
  theme: 'light',
  loading: false,
  error: null,
  products: [],
  categories: [],
  inventory: [],
  notifications: []
};

function appReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    
    case 'SET_USER':
      return { ...state, user: action.payload };
    
    case 'SET_LANGUAGE':
      return { ...state, language: action.payload };
    
    case 'SET_PRODUCTS':
      return { ...state, products: action.payload };
    
    case 'ADD_PRODUCT':
      return { ...state, products: [...state.products, action.payload] };
    
    case 'UPDATE_PRODUCT':
      return {
        ...state,
        products: state.products.map(product =>
          product.id === action.payload.id ? action.payload : product
        )
      };
    
    case 'DELETE_PRODUCT':
      return {
        ...state,
        products: state.products.filter(product => product.id !== action.payload)
      };
    
    case 'SET_CATEGORIES':
      return { ...state, categories: action.payload };
    
    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [...state.notifications, {
          id: Date.now(),
          ...action.payload
        }]
      };
    
    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload)
      };
    
    default:
      return state;
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // تحميل البيانات الأولية
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    
    try {
      // تحميل المستخدم من التخزين المحلي
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        dispatch({ type: 'SET_USER', payload: JSON.parse(savedUser) });
      }

      // تحميل اللغة المحفوظة
      const savedLanguage = localStorage.getItem('language') || 'ar';
      dispatch({ type: 'SET_LANGUAGE', payload: savedLanguage });
      document.documentElement.lang = savedLanguage;
      document.documentElement.dir = savedLanguage === 'ar' ? 'rtl' : 'ltr';

      // تحميل التصنيفات
      const categoriesResponse = await fetch('/api/categories');
      if (categoriesResponse.ok) {
        const categories = await categoriesResponse.json();
        dispatch({ type: 'SET_CATEGORIES', payload: categories });
      }

    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const actions = {
    setLoading: (loading) => dispatch({ type: 'SET_LOADING', payload: loading }),
    setError: (error) => dispatch({ type: 'SET_ERROR', payload: error }),
    setUser: (user) => {
      dispatch({ type: 'SET_USER', payload: user });
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
      } else {
        localStorage.removeItem('user');
      }
    },
    setLanguage: (language) => {
      dispatch({ type: 'SET_LANGUAGE', payload: language });
      localStorage.setItem('language', language);
      document.documentElement.lang = language;
      document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr';
    },
    addNotification: (notification) => {
      dispatch({ type: 'ADD_NOTIFICATION', payload: notification });
      // إزالة الإشعار تلقائياً بعد 5 ثواني
      setTimeout(() => {
        dispatch({ type: 'REMOVE_NOTIFICATION', payload: notification.id });
      }, 5000);
    }
  };

  return (
    <AppContext.Provider value={{ state, dispatch, actions }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
```

### 4. إضافة الاختبارات الشاملة

#### أ. اختبارات الوحدة للخدمات
```python
# ✅ اختبارات شاملة للخدمات
# backend/tests/test_product_service.py
import pytest
from unittest.mock import Mock, patch
from src.services.product_service import ProductService
from src.models.product import Product
from src.models.category import Category

class TestProductService:
    def setup_method(self):
        self.service = ProductService()
    
    def test_get_products_paginated_success(self):
        # إعداد البيانات التجريبية
        mock_products = [
            Mock(id=1, name='Product 1', name_ar='منتج 1'),
            Mock(id=2, name='Product 2', name_ar='منتج 2')
        ]
        
        mock_pagination = Mock()
        mock_pagination.items = mock_products
        mock_pagination.page = 1
        mock_pagination.pages = 1
        mock_pagination.total = 2
        mock_pagination.has_next = False
        mock_pagination.has_prev = False
        
        with patch.object(Product.query, 'paginate', return_value=mock_pagination):
            result = self.service.get_products_paginated({'page': 1, 'per_page': 20})
        
        assert result['pagination']['page'] == 1
        assert result['pagination']['total'] == 2
        assert len(result['products']) == 2
    
    def test_create_product_success(self):
        product_data = {
            'name': 'Test Product',
            'name_ar': 'منتج تجريبي',
            'price': 100.0,
            'category_id': 1
        }
        
        with patch.object(self.service, 'create') as mock_create:
            mock_product = Mock(id=1, **product_data)
            mock_create.return_value = mock_product
            
            result = self.service.create_product(product_data)
            
            mock_create.assert_called_once_with(product_data)
            assert result.id == 1
            assert result.name == 'Test Product'
    
    def test_search_products_with_query(self):
        search_args = {
            'search': 'laptop',
            'category_id': 1,
            'page': 1,
            'per_page': 20
        }
        
        with patch.object(Product, 'search') as mock_search:
            mock_query = Mock()
            mock_search.return_value = mock_query
            
            with patch.object(mock_query, 'paginate') as mock_paginate:
                mock_paginate.return_value = Mock(
                    items=[],
                    page=1,
                    pages=0,
                    total=0,
                    has_next=False,
                    has_prev=False
                )
                
                result = self.service.get_products_paginated(search_args)
                
                mock_search.assert_called_once_with(
                    query='laptop',
                    category_id=1,
                    supplier_id=None,
                    is_active=True
                )
```

#### ب. اختبارات التكامل للAPI
```python
# ✅ اختبارات التكامل للAPI
# backend/tests/test_api_integration.py
import pytest
import json
from app import create_app
from src.database import db
from src.models.user import User
from src.models.product import Product
from src.models.category import Category

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # إنشاء مستخدم تجريبي
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    
    response = client.post('/api/auth/register', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    
    # تسجيل الدخول
    login_data = {
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    
    response = client.post('/api/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    token = response.json['access_token']
    
    return {'Authorization': f'Bearer {token}'}

class TestProductAPI:
    def test_get_products_without_auth(self, client):
        response = client.get('/api/products')
        assert response.status_code == 401
    
    def test_get_products_with_auth(self, client, auth_headers):
        response = client.get('/api/products', headers=auth_headers)
        assert response.status_code == 200
        assert 'products' in response.json
        assert 'pagination' in response.json
    
    def test_create_product_success(self, client, auth_headers):
        # إنشاء تصنيف أولاً
        category_data = {
            'name': 'Electronics',
            'name_ar': 'إلكترونيات'
        }
        
        response = client.post('/api/categories',
                              data=json.dumps(category_data),
                              content_type='application/json',
                              headers=auth_headers)
        
        assert response.status_code == 201
        category_id = response.json['id']
        
        # إنشاء منتج
        product_data = {
            'name': 'Laptop',
            'name_ar': 'لابتوب',
            'description': 'Gaming laptop',
            'description_ar': 'لابتوب ألعاب',
            'price': 1500.00,
            'category_id': category_id,
            'barcode': '1234567890123'
        }
        
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              content_type='application/json',
                              headers=auth_headers)
        
        assert response.status_code == 201
        assert response.json['name'] == 'Laptop'
        assert response.json['name_ar'] == 'لابتوب'
        assert response.json['price'] == 1500.00
    
    def test_create_product_validation_error(self, client, auth_headers):
        # بيانات ناقصة (بدون اسم)
        product_data = {
            'price': 100.00,
            'category_id': 1
        }
        
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              content_type='application/json',
                              headers=auth_headers)
        
        assert response.status_code == 400
        assert 'errors' in response.json
    
    def test_update_product_success(self, client, auth_headers):
        # إنشاء منتج أولاً
        category_data = {'name': 'Test Category', 'name_ar': 'تصنيف تجريبي'}
        category_response = client.post('/api/categories',
                                       data=json.dumps(category_data),
                                       content_type='application/json',
                                       headers=auth_headers)
        category_id = category_response.json['id']
        
        product_data = {
            'name': 'Original Product',
            'name_ar': 'منتج أصلي',
            'price': 100.00,
            'category_id': category_id
        }
        
        create_response = client.post('/api/products',
                                     data=json.dumps(product_data),
                                     content_type='application/json',
                                     headers=auth_headers)
        
        product_id = create_response.json['id']
        
        # تحديث المنتج
        update_data = {
            'name': 'Updated Product',
            'name_ar': 'منتج محدث',
            'price': 150.00
        }
        
        response = client.put(f'/api/products/{product_id}',
                             data=json.dumps(update_data),
                             content_type='application/json',
                             headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json['name'] == 'Updated Product'
        assert response.json['price'] == 150.00
    
    def test_delete_product_success(self, client, auth_headers):
        # إنشاء منتج للحذف
        category_data = {'name': 'Test Category', 'name_ar': 'تصنيف تجريبي'}
        category_response = client.post('/api/categories',
                                       data=json.dumps(category_data),
                                       content_type='application/json',
                                       headers=auth_headers)
        category_id = category_response.json['id']
        
        product_data = {
            'name': 'Product to Delete',
            'name_ar': 'منتج للحذف',
            'price': 100.00,
            'category_id': category_id
        }
        
        create_response = client.post('/api/products',
                                     data=json.dumps(product_data),
                                     content_type='application/json',
                                     headers=auth_headers)
        
        product_id = create_response.json['id']
        
        # حذف المنتج
        response = client.delete(f'/api/products/{product_id}',
                               headers=auth_headers)
        
        assert response.status_code == 204
        
        # التأكد من الحذف
        get_response = client.get(f'/api/products/{product_id}',
                                 headers=auth_headers)
        assert get_response.status_code == 404
```

#### ج. اختبارات الأمان
```python
# ✅ اختبارات الأمان الشاملة
# backend/tests/test_security.py
import pytest
import json
from app import create_app

class TestSecurityFeatures:
    def test_sql_injection_protection(self, client, auth_headers):
        # محاولة حقن SQL في البحث
        malicious_query = "'; DROP TABLE products; --"
        
        response = client.get(f'/api/products/search?q={malicious_query}',
                             headers=auth_headers)
        
        # يجب أن يعود بنتيجة آمنة بدون خطأ
        assert response.status_code == 200
        assert 'products' in response.json
    
    def test_xss_protection(self, client, auth_headers):
        # محاولة XSS في إنشاء منتج
        xss_payload = "<script>alert('XSS')</script>"
        
        product_data = {
            'name': xss_payload,
            'name_ar': xss_payload,
            'description': xss_payload,
            'price': 100.00,
            'category_id': 1
        }
        
        response = client.post('/api/products',
                              data=json.dumps(product_data),
                              content_type='application/json',
                              headers=auth_headers)
        
        # يجب أن يتم تنظيف البيانات
        if response.status_code == 201:
            assert '<script>' not in response.json['name']
            assert '<script>' not in response.json['description']
    
    def test_csrf_protection(self, client):
        # محاولة إرسال طلب بدون CSRF token
        product_data = {
            'name': 'Test Product',
            'price': 100.00
        }
        
        response = client.post('/products/create',
                              data=product_data)
        
        # يجب أن يرفض الطلب
        assert response.status_code in [400, 403]
    
    def test_rate_limiting(self, client):
        # محاولة إرسال طلبات كثيرة بسرعة
        for i in range(100):
            response = client.post('/api/auth/login',
                                  data=json.dumps({
                                      'email': 'test@example.com',
                                      'password': 'wrongpassword'
                                  }),
                                  content_type='application/json')
            
            # يجب أن يتم تطبيق rate limiting
            if response.status_code == 429:
                break
        else:
            pytest.fail("Rate limiting not working")
    
    def test_password_strength_validation(self, client):
        # محاولة إنشاء مستخدم بكلمة مرور ضعيفة
        weak_passwords = ['123', 'password', 'abc', '12345678']
        
        for weak_password in weak_passwords:
            user_data = {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': weak_password
            }
            
            response = client.post('/api/auth/register',
                                  data=json.dumps(user_data),
                                  content_type='application/json')
            
            assert response.status_code == 400
            assert 'password' in response.json.get('errors', {})
    
    def test_secure_headers_present(self, client):
        response = client.get('/')
        
        # التحقق من وجود رؤوس الأمان
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
        
        assert 'X-XSS-Protection' in response.headers
        
        assert 'Content-Security-Policy' in response.headers
```

---

## 📋 قائمة المهام التفصيلية (Task Checklist)

### المرحلة الأولى: الأمان الحرج (أسبوعان)

#### الأسبوع الأول:
- [ ] **اليوم 1-2: إصلاح ثغرات SQL Injection**
  - [ ] مراجعة ملف `backend/src/routes/products.py` خطوط 45, 67, 89
  - [ ] مراجعة ملف `backend/src/routes/inventory.py` خطوط 23, 156
  - [ ] مراجعة ملف `backend/src/services/reports.py` خطوط 78, 134, 201
  - [ ] تحويل جميع الاستعلامات إلى parameterized queries
  - [ ] اختبار جميع endpoints للتأكد من الأمان

- [ ] **اليوم 3-4: تطبيق CSRF Protection**
  - [ ] تثبيت Flask-WTF
  - [ ] إضافة CSRFProtect للتطبيق
  - [ ] إضافة CSRF tokens لجميع النماذج (45+ نموذج)
  - [ ] تحديث الواجهة الأمامية لإرسال CSRF tokens
  - [ ] اختبار جميع النماذج

- [ ] **اليوم 5-7: تحسين المصادقة**
  - [ ] استبدال MD5 بـ PBKDF2
  - [ ] تطبيق Flask-JWT-Extended
  - [ ] إضافة session management آمن
  - [ ] تطبيق rate limiting مع Flask-Limiter
  - [ ] إضافة password strength validation

#### الأسبوع الثاني:
- [ ] **اليوم 8-10: رؤوس الأمان**
  - [ ] إضافة X-Content-Type-Options: nosniff
  - [ ] إضافة X-Frame-Options: DENY
  - [ ] إضافة X-XSS-Protection: 1; mode=block
  - [ ] إضافة Strict-Transport-Security
  - [ ] تكوين Content-Security-Policy
  - [ ] إضافة Referrer-Policy
  - [ ] اختبار الأمان مع أدوات scanning

- [ ] **اليوم 11-14: التحقق من المدخلات**
  - [ ] تثبيت Marshmallow للـ validation
  - [ ] إنشاء schemas للتحقق من البيانات
  - [ ] إضافة validation لجميع endpoints (156+ نقطة)
  - [ ] تطبيق input sanitization
  - [ ] إضافة error handling شامل
  - [ ] اختبار جميع نقاط الدخول

### المرحلة الثانية: الأداء وقاعدة البيانات (أسبوعان)

#### الأسبوع الثالث:
- [ ] **تحسين قاعدة البيانات**
  - [ ] إضافة فهارس للجداول الرئيسية
  - [ ] تحسين استعلامات N+1 في Products
  - [ ] تحسين استعلامات N+1 في Inventory
  - [ ] تحسين استعلامات N+1 في Sales
  - [ ] إضافة connection pooling
  - [ ] تطبيق database migration scripts

- [ ] **تطبيق Caching**
  - [ ] تثبيت Redis
  - [ ] تكوين Flask-Caching
  - [ ] إضافة cache للتصنيفات
  - [ ] إضافة cache للمنتجات
  - [ ] إضافة cache للتقارير
  - [ ] تطبيق cache invalidation strategy

#### الأسبوع الرابع:
- [ ] **تحسين الأداء العام**
  - [ ] تحسين bundle size للواجهة الأمامية
  - [ ] تطبيق lazy loading للمكونات
  - [ ] تطبيق code splitting
  - [ ] تحسين الصور وإضافة compression
  - [ ] تطبيق CDN للملفات الثابتة
  - [ ] إضافة performance monitoring

### المرحلة الثالثة: تجربة المستخدم (أسبوعان)

#### الأسبوع الخامس:
- [ ] **إصلاح مشاكل إمكانية الوصول**
  - [ ] إضافة alt text لجميع الصور (66 صورة)
  - [ ] إضافة labels لجميع النماذج (23 نموذج)
  - [ ] تحسين keyboard navigation
  - [ ] إضافة ARIA labels وdescriptions
  - [ ] تحسين color contrast
  - [ ] إضافة focus indicators
  - [ ] اختبار مع screen readers

- [ ] **تحسين دعم العربية**
  - [ ] تطبيق RTL layout شامل
  - [ ] إضافة خطوط عربية احترافية
  - [ ] تحسين تنسيق التواريخ والأرقام
  - [ ] تحسين اتجاه النصوص والعناصر
  - [ ] إضافة دعم للتقويم الهجري

#### الأسبوع السادس:
- [ ] **تطوير نظام التصميم**
  - [ ] إنشاء theme system شامل
  - [ ] تطوير مكونات UI قابلة لإعادة الاستخدام
  - [ ] تطبيق design tokens
  - [ ] تحسين responsive design
  - [ ] إضافة dark mode support
  - [ ] إنشاء style guide

### المرحلة الرابعة: الاختبار والتوثيق (أسبوعان)

#### الأسبوع السابع:
- [ ] **إضافة الاختبارات**
  - [ ] كتابة unit tests للخدمات
  - [ ] كتابة integration tests للAPI
  - [ ] كتابة security tests
  - [ ] كتابة performance tests
  - [ ] إضافة test coverage reporting
  - [ ] تطبيق continuous testing

#### الأسبوع الثامن:
- [ ] **التوثيق والإنتاج**
  - [ ] إنشاء API documentation مع OpenAPI
  - [ ] كتابة user manual باللغة العربية
  - [ ] إنشاء deployment guide
  - [ ] تطبيق CI/CD pipeline
  - [ ] إعداد monitoring وlogging
  - [ ] إجراء penetration testing نهائي

---

## 🎯 معايير الجودة والقبول

### معايير الأمان:
- [ ] صفر ثغرات حرجة أو عالية الخطورة
- [ ] تطبيق جميع رؤوس الأمان المطلوبة
- [ ] اجتياز penetration testing
- [ ] تطبيق rate limiting فعال
- [ ] تشفير قوي لجميع البيانات الحساسة

### معايير الأداء:
- [ ] وقت تحميل الصفحة < 3 ثواني
- [ ] وقت استجابة API < 200ms
- [ ] وقت استعلام قاعدة البيانات < 100ms
- [ ] حجم bundle JavaScript < 1MB
- [ ] نتيجة Lighthouse > 90

### معايير إمكانية الوصول:
- [ ] امتثال كامل لمعايير WCAG AA
- [ ] دعم كامل للـ screen readers
- [ ] keyboard navigation سلس
- [ ] color contrast مناسب
- [ ] alt text لجميع الصور

### معايير دعم العربية:
- [ ] RTL layout صحيح 100%
- [ ] خطوط عربية احترافية
- [ ] تنسيق صحيح للتواريخ والأرقام
- [ ] ترجمة كاملة للواجهة
- [ ] دعم التقويم الهجري

### معايير الاختبار:
- [ ] test coverage > 80%
- [ ] اجتياز جميع unit tests
- [ ] اجتياز جميع integration tests
- [ ] اجتياز جميع security tests
- [ ] اجتياز user acceptance testing

---

## 🚀 أوامر التنفيذ السريع

### إعداد البيئة:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install flask-wtf flask-jwt-extended marshmallow flask-caching flask-limiter

# Frontend
cd frontend
npm install
npm install @testing-library/react @testing-library/jest-dom
npm install axios react-router-dom react-hook-form
```

### تشغيل الاختبارات:
```bash
# Backend tests
cd backend
python -m pytest tests/ -v --cov=src --cov-report=html

# Frontend tests
cd frontend
npm test -- --coverage --watchAll=false

# Security tests
cd backend
bandit -r src/ -f json -o security_report.json
```

### بناء الإنتاج:
```bash
# Frontend build
cd frontend
npm run build

# Backend deployment
cd backend
gunicorn --bind 0.0.0.0:5000 app:app
```

---

## 📞 نقاط الاتصال والدعم

### للمساعدة التقنية:
- **الأمان:** راجع OWASP Top 10 وCWE Top 25
- **الأداء:** استخدم Chrome DevTools وLighthouse
- **إمكانية الوصول:** راجع WCAG 2.1 Guidelines
- **العربية:** راجع Unicode Bidirectional Algorithm

### أدوات التطوير المطلوبة:
- **IDE:** VS Code مع extensions للـ Python وReact
- **Database:** PostgreSQL للإنتاج، SQLite للتطوير
- **Cache:** Redis
- **Testing:** pytest، Jest، Cypress
- **Security:** Bandit، OWASP ZAP
- **Performance:** Lighthouse، WebPageTest

---

**هذا البرومبت يحتوي على جميع التفاصيل اللازمة لتحويل النظام من حالته الحرجة الحالية إلى نظام آمن ومحترف وجاهز للإنتاج. اتبع المراحل بالترتيب المحدد مع التركيز على الأمان كأولوية قصوى.**
