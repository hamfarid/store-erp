التوثيق التقني - نظام إدارة المخزون

## 📋 نظرة عامة تقنية

### معمارية النظام
- **Frontend**: React.js مع Tailwind CSS
- **Backend**: Flask (Python)
- **Database**: SQLite/PostgreSQL
- **Authentication**: Flask-Login
- **API**: RESTful APIs
- **File Storage**: Local/Cloud Storage

### متطلبات النظام
- **Node.js**: 16.0 أو أحدث
- **Python**: 3.8 أو أحدث
- **RAM**: 4GB كحد أدنى
- **Storage**: 10GB مساحة فارغة
- **Browser**: Chrome, Firefox, Safari, Edge

---

## 🏗️ هيكل المشروع

```
complete_inventory_system/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CompanySettings.jsx
│   │   │   ├── FinancialReports.jsx
│   │   │   ├── ImportExportAdvanced.jsx
│   │   │   ├── NotificationSystem.jsx
│   │   │   ├── AdvancedPermissions.jsx
│   │   │   ├── WorkflowManagement.jsx
│   │   │   ├── SystemTesting.jsx
│   │   │   ├── SystemDocumentation.jsx
│   │   │   └── TrainingCenter.jsx
│   │   ├── services/
│   │   │   └── ApiService.js
│   │   ├── utils/
│   │   └── App.jsx
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── company_settings.py
│   │   │   ├── financial_reports_advanced.py
│   │   │   └── import_export_advanced.py
│   │   ├── models/
│   │   ├── utils/
│   │   └── main.py
│   └── requirements.txt
├── database/
├── uploads/
├── USER_MANUAL.md
├── TECHNICAL_DOCUMENTATION.md
└── IMPLEMENTATION_SUMMARY.md
```

---

## 🔧 تثبيت وإعداد النظام

### 1. إعداد الواجهة الأمامية (Frontend)

```bash
# الانتقال إلى مجلد الواجهة الأمامية
cd complete_inventory_system/frontend

# تثبيت المكتبات المطلوبة
npm install

# تشغيل الخادم التطويري
npm start
```

### 2. إعداد الخادم الخلفي (Backend)

```bash
# الانتقال إلى مجلد الخادم الخلفي
cd complete_inventory_system/backend

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# تثبيت المكتبات المطلوبة
pip install -r requirements.txt

# تشغيل الخادم
python src/main.py
```

### 3. إعداد قاعدة البيانات

```python
# في ملف main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

# إنشاء الجداول
with app.app_context():
    db.create_all()
```

---

## 📡 واجهات البرمجة (APIs)

### 1. إعدادات الشركة

#### GET /api/company/settings
```json
{
  "success": true,
  "data": {
    "name": "اسم الشركة",
    "address": "العنوان",
    "phone": "رقم الهاتف",
    "email": "البريد الإلكتروني",
    "tax_number": "الرقم الضريبي",
    "logo": "مسار الشعار",
    "currency": "العملة",
    "timezone": "المنطقة الزمنية"
  }
}
```

#### POST /api/company/settings
```json
{
  "name": "اسم الشركة الجديد",
  "address": "العنوان الجديد",
  "phone": "رقم الهاتف الجديد",
  "email": "البريد الإلكتروني الجديد"
}
```

### 2. التقارير المالية

#### GET /api/reports/financial/profit-loss
```json
{
  "success": true,
  "data": {
    "period": "2024-01",
    "revenue": 150000,
    "expenses": 80000,
    "gross_profit": 70000,
    "net_profit": 65000,
    "details": [...]
  }
}
```

#### GET /api/reports/financial/sales
```json
{
  "success": true,
  "data": {
    "total_sales": 150000,
    "sales_count": 45,
    "average_sale": 3333.33,
    "top_products": [...],
    "monthly_trend": [...]
  }
}
```

### 3. الاستيراد والتصدير

#### POST /api/import-export/import
```json
{
  "dataType": "products",
  "fileFormat": "excel",
  "validateData": true,
  "skipDuplicates": true,
  "updateExisting": false
}
```

#### GET /api/import-export/export
```
GET /api/import-export/export?dataType=products&fileFormat=excel
```

### 4. إدارة الصلاحيات

#### GET /api/admin/roles
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "مدير النظام",
      "description": "صلاحيات كاملة",
      "permissions": ["products.view", "products.create", ...],
      "userCount": 2
    }
  ]
}
```

#### POST /api/admin/roles
```json
{
  "name": "اسم الدور",
  "description": "وصف الدور",
  "permissions": ["products.view", "products.create"]
}
```

---

## 🗄️ نماذج قاعدة البيانات

### 1. نموذج الشركة (Company)
```python
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    tax_number = db.Column(db.String(50))
    logo_path = db.Column(db.String(255))
    currency = db.Column(db.String(10), default='EGP')
    timezone = db.Column(db.String(50), default='Africa/Cairo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 2. نموذج المنتج (Product)
```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    unit = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2))
    cost = db.Column(db.Numeric(10, 2))
    barcode = db.Column(db.String(100), unique=True)
    image_path = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 3. نموذج المخزون (Inventory)
```python
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    quantity = db.Column(db.Integer, default=0)
    reserved_quantity = db.Column(db.Integer, default=0)
    min_stock_level = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
```

### 4. نموذج الفاتورة (Invoice)
```python
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(20))  # 'sale' or 'purchase'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    date = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date)
    subtotal = db.Column(db.Numeric(10, 2))
    tax_amount = db.Column(db.Numeric(10, 2))
    discount_amount = db.Column(db.Numeric(10, 2))
    total_amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## 🔐 الأمان والحماية

### 1. المصادقة والتخويل
```python
from flask_login import login_required, current_user
from functools import wraps

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                return jsonify({'error': 'غير مخول'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/products', methods=['POST'])
@login_required
@require_permission('products.create')
def create_product():
    # كود إنشاء المنتج
    pass
```

### 2. التحقق من صحة البيانات
```python
from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    price = fields.Decimal(required=True, validate=validate.Range(min=0))
    category_id = fields.Int(required=True)
    unit = fields.Str(required=True)

def validate_product_data(data):
    schema = ProductSchema()
    try:
        result = schema.load(data)
        return result, None
    except ValidationError as err:
        return None, err.messages
```

### 3. حماية من هجمات CSRF
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

---

## 📊 مراقبة الأداء

### 1. تسجيل الأحداث (Logging)
```python
import logging
from logging.handlers import RotatingFileHandler

# إعداد نظام التسجيل
if not app.debug:
    file_handler = RotatingFileHandler('logs/inventory.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 2. مراقبة قاعدة البيانات
```python
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    if total > 0.1:  # تسجيل الاستعلامات البطيئة
        app.logger.warning(f"Slow query: {total:.2f}s - {statement[:100]}")
```

---

## 🧪 الاختبارات

### 1. اختبارات الوحدة (Unit Tests)
```python
import unittest
from app import app, db
from models import Product, Category

class ProductTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def test_create_product(self):
        response = self.app.post('/api/products', json={
            'name': 'منتج تجريبي',
            'price': 100.0,
            'category_id': 1,
            'unit': 'قطعة'
        })
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        with app.app_context():
            db.drop_all()
```

### 2. اختبارات التكامل (Integration Tests)
```python
def test_product_inventory_integration(self):
    # إنشاء منتج
    product_response = self.app.post('/api/products', json={
        'name': 'منتج تجريبي',
        'price': 100.0
    })
    product_id = product_response.json['data']['id']
    
    # إضافة مخزون
    inventory_response = self.app.post('/api/inventory/movements', json={
        'product_id': product_id,
        'quantity': 50,
        'type': 'in'
    })
    
    # التحقق من المخزون
    stock_response = self.app.get(f'/api/inventory/stock/{product_id}')
    self.assertEqual(stock_response.json['data']['quantity'], 50)
```

---

## 🚀 النشر والإنتاج

### 1. إعداد خادم الإنتاج
```bash
# تثبيت Gunicorn
pip install gunicorn

# تشغيل الخادم
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

### 2. إعداد Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/static/files;
    }
}
```

### 3. متغيرات البيئة
```bash
# .env file
DATABASE_URL=postgresql://user:password@localhost/inventory_db
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
UPLOAD_FOLDER=/var/uploads
MAX_CONTENT_LENGTH=16777216
```

---

## 📝 صيانة النظام

### 1. النسخ الاحتياطية
```python
import subprocess
from datetime import datetime

def create_database_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_{timestamp}.sql'
    
    subprocess.run([
        'pg_dump',
        '-h', 'localhost',
        '-U', 'username',
        '-d', 'inventory_db',
        '-f', backup_file
    ])
    
    return backup_file
```

### 2. تنظيف الملفات المؤقتة
```python
import os
import time

def cleanup_temp_files():
    temp_dir = 'uploads/temp'
    current_time = time.time()
    
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > 86400:  # 24 hours
                os.remove(file_path)
```

---

## 📞 الدعم التقني

للمطورين والدعم التقني:
- **Repository**: GitHub Repository URL
- **Documentation**: Technical Wiki
- **Issue Tracking**: GitHub Issues
- **API Documentation**: Swagger/OpenAPI

---

**آخر تحديث:** يناير 2024
**إصدار التوثيق:** 1.0
