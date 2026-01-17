## برومبت التطوير الشامل والمحسن - الإصدار 3.3

### ملخص التحسينات الجديدة:

- **إدارة البيئة:** نظام شامل لإدارة متغيرات البيئة والتحقق منها.
- **توثيق شامل:** خرائط للملفات والوحدات والتبعيات.
- **منع التكرار:** أدوات لكشف وإزالة الكود المكرر.
- **جودة الكود:** فرض طول الأسطر وإزالة الكود غير المستخدم.
- **CI/CD محسن:** إصلاح وتحسين GitHub Workflows.
- **قائمة تحقق إلزامية:** قائمة مهام يجب إكمالها قبل بدء أي تطوير.

---



## برومبت التطوير الشامل - نظام إدارة المخزون العربي
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
    sql = f"SELECT * FROM products WHERE name LIKE 
'%{query}%'"
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
}

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
    .container { max-width: 960px; }
}

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
    .container { max-width: 1140px; }
}
```

### 4. إعادة هيكلة الكود (20+ ملف عالي التعقيد)

#### أ. إعادة هيكلة الواجهة الخلفية
- **الهدف:** تطبيق بنية Hexagonal Architecture
- **الطبقات:**
  - `src/domain`: نماذج قاعدة البيانات والمنطق الأساسي
  - `src/application`: خدمات التطبيق (use cases)
  - `src/infrastructure`: الواجهات (API routes, database adapters)

```python
# ❌ خطأ موجود - كل شيء في ملف واحد
# backend/app.py

# ✅ الإصلاح المطلوب
# backend/src/domain/product.py
# backend/src/application/product_service.py
# backend/src/infrastructure/api/product_routes.py
# backend/src/infrastructure/db/product_repository.py
```

#### ب. إعادة هيكلة الواجهة الأمامية
- **الهدف:** تطبيق بنية Atomic Design
- **المجلدات:**
  - `src/components/atoms`: (Button, Input, Label)
  - `src/components/molecules`: (SearchForm, ProductCard)
  - `src/components/organisms`: (ProductList, Header)
  - `src/components/templates`: (MainLayout, SidebarLayout)
  - `src/components/pages`: (HomePage, ProductPage)

```jsx
// ❌ خطأ موجود - مكونات كبيرة ومعقدة
// src/components/ProductPage.jsx

// ✅ الإصلاح المطلوب
// src/components/atoms/Button.jsx
// src/components/molecules/ProductCard.jsx
// src/components/organisms/ProductList.jsx
// src/components/pages/ProductPage.jsx
```

### 5. الاختبارات والتوثيق

#### أ. إضافة اختبارات شاملة
- **الهدف:** تحقيق تغطية اختبار > 80%
- **الأدوات:** Pytest (backend), Jest + React Testing Library (frontend)

```python
# ✅ إضافة اختبارات الوحدة والتكامل
# backend/tests/test_product_service.py
# backend/tests/test_product_api.py
```

```jsx
// ✅ إضافة اختبارات المكونات
// src/components/molecules/ProductCard.test.jsx
```

#### ب. توثيق شامل
- **الهدف:** توثيق جميع مكونات النظام
- **الأدوات:** Sphinx (backend), JSDoc (frontend)

```python
# ✅ إضافة docstrings شاملة
def create_product(data):
    """Create a new product.

    Args:
        data (dict): Product data.

    Returns:
        Product: The created product.
    """
    pass
```

---

## 📅 خطة العمل المقترحة (6-8 أسابيع)

### المرحلة الأولى (أسبوعان): الأمان وإعادة الهيكلة
- إصلاح جميع الثغرات الأمنية الحرجة
- إعادة هيكلة الواجهة الخلفية والأمامية
- إضافة نظام Caching

### المرحلة الثانية (أسبوعان): قاعدة البيانات والأداء
- إضافة الفهارس المطلوبة
- إصلاح مشاكل N+1
- تحسين أداء الاستعلامات

### المرحلة الثالثة (أسبوعان): تجربة المستخدم
- إصلاح جميع مشاكل إمكانية الوصول
- تحسين دعم العربية الكامل
- تطوير نظام التصميم

### المرحلة الرابعة (أسبوعان): الاختبار والإنتاج
- اختبارات شاملة
- توثيق كامل
- إعداد الإنتاج

---

## ✅ قائمة المهام التفصيلية

- [ ] **الأمان:**
  - [ ] إصلاح جميع ثغرات حقن SQL
  - [ ] إضافة حماية CSRF لجميع النماذج
  - [ ] تطبيق تشفير كلمات المرور القوي
  - [ ] إضافة رؤوس الأمان
  - [ ] التحقق من جميع المدخلات باستخدام Marshmallow
- [ ] **الأداء:**
  - [ ] إصلاح جميع مشاكل N+1
  - [ ] إضافة جميع الفهارس المطلوبة
  - [ ] تطبيق نظام Caching شامل
- [ ] **تجربة المستخدم:**
  - [ ] إصلاح جميع مشاكل إمكانية الوصول (66 مشكلة)
  - [ ] تطبيق دعم RTL كامل
  - [ ] تطوير نظام تصميم متجاوب
- [ ] **إعادة الهيكلة:**
  - [ ] إعادة هيكلة الواجهة الخلفية (Hexagonal Architecture)
  - [ ] إعادة هيكلة الواجهة الأمامية (Atomic Design)
- [ ] **الاختبارات:**
  - [ ] تحقيق تغطية اختبار > 80% للواجهة الخلفية
  - [ ] تحقيق تغطية اختبار > 80% للواجهة الأمامية
- [ ] **التوثيق:**
  - [ ] توثيق جميع مكونات الواجهة الخلفية
  - [ ] توثيق جميع مكونات الواجهة الأمامية

---

## 🎯 معايير الجودة

- **الأمان:** صفر ثغرات حرجة
- **الأداء:** < 3 ثواني تحميل، < 200ms API
- **إمكانية الوصول:** امتثال كامل لـ WCAG AA
- **العربية:** RTL كامل مع خطوط احترافية
- **الاختبارات:** > 80% test coverage

---

## 🚀 أوامر التنفيذ

- **إعداد البيئة:** `pip install -r requirements.txt && npm install`
- **تشغيل الاختبارات:** `pytest && npm test`
- **بناء الإنتاج:** `npm run build`


## التحسينات الجديدة - الإصدار 3.3

### 35. إدارة متغيرات البيئة والتحقق منها

- **الهدف:** ضمان أن جميع متغيرات البيئة المطلوبة موجودة وصحيحة قبل بدء تشغيل التطبيق.
- **التنفيذ:**
  - إنشاء ملف `.env.example` لتوثيق جميع المتغيرات المطلوبة.
  - إنشاء سكريبت `scripts/validate_env.py` للتحقق من صحة المتغيرات.
  - إنشاء سكريبت `scripts/generate_env.py` لإنشاء ملف `.env` مع قيم افتراضية آمنة.
  - تشغيل التحقق من متغيرات البيئة عند بدء تشغيل التطبيق.

### 36. توثيق الاستيراد والتصدير

- **الهدف:** تتبع جميع عمليات الاستيراد والتصدير لمنع التبعيات الدائرية والتكرار.
- **التنفيذ:**
  - إنشاء سكريبت `scripts/generate_imports_map.py` لإنشاء خريطة للاستيراد والتصدير.
  - إنشاء ملف `/docs/Imports_Map.md` و `/docs/Exports_Map.md`.
  - إضافة فحص للتبعيات الدائرية والتصدير المكرر في CI.

### 37. كشف وإزالة الكود المكرر

- **الهدف:** منع وإزالة الكود والملفات المكررة.
- **التنفيذ:**
  - إنشاء سكريبت `scripts/detect_duplicates.py` للكشف عن الكود المكرر.
  - إنشاء عملية موحدة لدمج الكود المكرر.
  - إضافة فحص للكود المكرر في CI.

### 38. قائمة تحقق إلزامية قبل التطوير

- **الهدف:** فرض قائمة مهام إلزامية يجب إكمالها قبل بدء أي تطوير.
- **التنفيذ:**
  - إنشاء ملف `/docs/PRE_DEVELOPMENT_CHECKLIST.md`.
  - إنشاء سكريبت `scripts/pre_dev_check.py` للتحقق من إكمال القائمة.
  - إضافة git hook لتشغيل التحقق قبل كل commit.

### 39. إدارة تكوين المنافذ

- **الهدف:** توحيد إدارة منافذ التطبيق لمنع التعارض.
- **التنفيذ:**
  - إنشاء ملف `config/ports.py` لتعريف جميع المنافذ.
  - إضافة فحص للتعارض في CI.

### 40. هيكلة التعريفات المنظمة

- **الهدف:** تنظيم جميع التعريفات المشتركة في مكان واحد.
- **التنفيذ:**
  - إنشاء مجلد `config/definitions` مع ملفات `common.py`, `core.py`, `custom.py`.
  - إنشاء ملف `__init__.py` لتصدير جميع التعريفات.

### 41. فرض طول الأسطر (≤120)

- **الهدف:** فرض طول أقصى للأسطر لتحسين قابلية القراءة.
- **التنفيذ:**
  - تحديث إعدادات `flake8`, `autopep8`, `black`, `isort`.
  - إضافة git hook للتحقق من طول الأسطر.
  - إنشاء سكريبت `scripts/fix_line_length.sh` لإصلاح طول الأسطر تلقائياً.

### 42. معالجة الأخطاء بناءً على البيئة

- **الهدف:** عرض رسائل خطأ مختلفة في بيئة التطوير والإنتاج.
- **التنفيذ:**
  - إنشاء middleware `middleware/error_handler.py` لمعالجة الأخطاء.
  - عرض رسائل خطأ مفصلة في التطوير ورسائل عامة في الإنتاج.

### 43. إزالة الكود غير المستخدم

- **الهدف:** إزالة الكود غير المستخدم تلقائياً.
- **التنفيذ:**
  - إنشاء سكريبت `scripts/remove_unused.sh` لإزالة الكود غير المستخدم.
  - إضافة git hook للتحقق من وجود كود غير مستخدم.

### 44. إصلاح GitHub Workflows

- **الهدف:** إصلاح وتحسين CI/CD pipeline.
- **التنفيذ:**
  - تحديث ملف `.github/workflows/ci.yml` و `.github/workflows/deploy.yml`.
  - إضافة خطوات لتثبيت التبعيات وتشغيل جميع الفحوصات.

### 45. توثيق الاستيراد والتصدير

- **الهدف:** توثيق جميع عمليات الاستيراد والتصدير تلقائياً.
- **التنفيذ:**
  - إنشاء سكريبت `scripts/document_imports.py` لإنشاء التوثيق.
  - إضافة خطوة في CI لإنشاء التوثيق تلقائياً.

