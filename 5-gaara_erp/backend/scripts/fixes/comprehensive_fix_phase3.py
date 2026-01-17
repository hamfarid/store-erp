#!/usr/bin/env python3
"""
إصلاح شامل للمرحلة الثالثة - حل جميع المشاكل المتبقية
Comprehensive Fix Phase 3 - Resolve All Remaining Issues
"""

import os
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime


class ComprehensiveFix:
    def __init__(self):
        self.base_path = Path(".")
        self.src_path = self.base_path / "src"
        self.fixes_applied = []
        self.errors_found = []

    def fix_all_imports(self):
        """إصلاح جميع الاستيرادات المكسورة"""
        print("🔧 إصلاح جميع الاستيرادات...")

        # قائمة الاستيرادات المكسورة والبديلة
        import_fixes = {
            "from models.user import db": "from database import db",
            "from models.partners import Customer": "from models.customer import Customer",
            "from models.partners import Supplier": "from models.supplier import Supplier",
            "from models.partners import CustomerPartner": "from models.customer import Customer",
            "from src.database import": "from database import",
            "from src.models": "from models",
        }

        # البحث في جميع ملفات Python
        for py_file in self.src_path.rglob("*.py"):
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                original_content = content

                # تطبيق الإصلاحات
                for old_import, new_import in import_fixes.items():
                    if old_import in content:
                        content = content.replace(old_import, new_import)
                        self.fixes_applied.append(
                            f"إصلاح استيراد في {py_file.name}: {old_import} -> {new_import}"
                        )

                # حفظ الملف إذا تم تعديله
                if content != original_content:
                    with open(py_file, "w", encoding="utf-8") as f:
                        f.write(content)

            except Exception as e:
                self.errors_found.append(f"خطأ في إصلاح {py_file}: {e}")

    def create_missing_models(self):
        """إنشاء النماذج المفقودة"""
        print("📝 إنشاء النماذج المفقودة...")

        # إنشاء نموذج User مبسط
        user_model_path = self.src_path / "models" / "user.py"
        if not user_model_path.exists():
            user_model_content = '''"""
نموذج المستخدم المبسط
Simplified User Model
"""

from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    permissions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'permissions': self.permissions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # العلاقات
    role = db.relationship('Role', backref='users')
    
    def set_password(self, password):
        """تعيين كلمة المرور مع التشفير"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role_id': self.role_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
'''

            with open(user_model_path, "w", encoding="utf-8") as f:
                f.write(user_model_content)

            self.fixes_applied.append("إنشاء نموذج User مبسط")

        # إنشاء نموذج Category مبسط
        category_model_path = self.src_path / "models" / "inventory.py"
        if not category_model_path.exists():
            inventory_model_content = '''"""
نماذج المخزون المبسطة
Simplified Inventory Models
"""

from database import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات
    parent = db.relationship('Category', remote_side=[id], backref='children')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sku = db.Column(db.String(50), unique=True)
    barcode = db.Column(db.String(50), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    price = db.Column(db.Numeric(10, 2))
    cost = db.Column(db.Numeric(10, 2))
    quantity = db.Column(db.Integer, default=0)
    min_quantity = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    category = db.relationship('Category', backref='products')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sku': self.sku,
            'barcode': self.barcode,
            'category_id': self.category_id,
            'price': float(self.price) if self.price else None,
            'cost': float(self.cost) if self.cost else None,
            'quantity': self.quantity,
            'min_quantity': self.min_quantity,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
'''

            with open(category_model_path, "w", encoding="utf-8") as f:
                f.write(inventory_model_content)

            self.fixes_applied.append("إنشاء نماذج المخزون المبسطة")

    def fix_api_endpoints(self):
        """إصلاح نقاط النهاية API"""
        print("🌐 إصلاح نقاط النهاية API...")

        # إصلاح ملف products.py
        products_file = self.src_path / "routes" / "products.py"
        if products_file.exists():
            try:
                with open(products_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # إضافة معالجة أخطاء شاملة
                if "@products_bp.route('/api/products', methods=['GET'])" in content:
                    # البحث عن الدالة وإضافة try/except
                    pattern = r"(@products_bp\.route\(\'/api/products\', methods=\[\'GET\'\]\)\ndef get_products\(\):.*?)(return jsonify\(.*?\))"

                    replacement = r"""\1try:
        # التحقق من وجود النموذج
        from models.inventory import Product
        
        # الحصول على المنتجات
        products = Product.query.all()
        
        return jsonify({
            'success': True,
            'data': [product.to_dict() for product in products],
            'total': len(products)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'خطأ في الحصول على المنتجات'
        }), 500"""

                    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

                    with open(products_file, "w", encoding="utf-8") as f:
                        f.write(content)

                    self.fixes_applied.append("إصلاح نقطة نهاية /api/products")

            except Exception as e:
                self.errors_found.append(f"خطأ في إصلاح products.py: {e}")

    def create_security_fixes(self):
        """إنشاء إصلاحات الأمان"""
        print("🔒 تطبيق إصلاحات الأمان...")

        # إنشاء ملف .env.example
        env_example_path = self.base_path / ".env.example"
        env_example_content = """# إعدادات البيئة - نسخ إلى .env وتعديل القيم
# Environment Settings - Copy to .env and modify values

# إعدادات Flask
FLASK_ENV=development
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here

# إعدادات قاعدة البيانات
DATABASE_URL=sqlite:///instance/inventory.db

# إعدادات الأمان
JWT_SECRET_KEY=your-jwt-secret-here
BCRYPT_LOG_ROUNDS=12

# إعدادات الخادم
HOST=0.0.0.0
PORT=5001

# إعدادات البريد الإلكتروني (اختيارية)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
"""

        with open(env_example_path, "w", encoding="utf-8") as f:
            f.write(env_example_content)

        self.fixes_applied.append("إنشاء ملف .env.example للأمان")

        # إنشاء ملف .gitignore محسن
        gitignore_path = self.base_path / ".gitignore"
        gitignore_content = """# ملفات البيئة والأمان
.env
.env.local
.env.production
*.key
*.pem

# قواعد البيانات
*.db
*.sqlite
*.sqlite3
instance/

# ملفات Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# ملفات IDE
.vscode/
.idea/
*.swp
*.swo
*~

# ملفات النظام
.DS_Store
Thumbs.db

# ملفات السجلات
*.log
logs/

# ملفات مؤقتة
tmp/
temp/
.tmp/

# ملفات النسخ الاحتياطية
*.backup
*.bak
*_backup*
"""

        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(gitignore_content)

        self.fixes_applied.append("إنشاء ملف .gitignore محسن")

    def optimize_frontend_connections(self):
        """تحسين اتصالات الواجهة الأمامية"""
        print("🎨 تحسين اتصالات الواجهة الأمامية...")

        frontend_path = self.base_path.parent / "frontend"
        if frontend_path.exists():
            # تحديث ملف api.js
            api_config_path = frontend_path / "src" / "config" / "api.js"
            if api_config_path.exists():
                api_config_content = """// إعدادات API محسنة
const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5001',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
};

// إنشاء instance محسن
const api = {
  get: async (url, config = {}) => {
    try {
      const response = await fetch(`${API_CONFIG.baseURL}${url}`, {
        method: 'GET',
        headers: { ...API_CONFIG.headers, ...config.headers },
        ...config
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API GET Error:', error);
      throw error;
    }
  },
  
  post: async (url, data, config = {}) => {
    try {
      const response = await fetch(`${API_CONFIG.baseURL}${url}`, {
        method: 'POST',
        headers: { ...API_CONFIG.headers, ...config.headers },
        body: JSON.stringify(data),
        ...config
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API POST Error:', error);
      throw error;
    }
  }
};

export default api;
export { API_CONFIG };
"""

                with open(api_config_path, "w", encoding="utf-8") as f:
                    f.write(api_config_content)

                self.fixes_applied.append("تحسين ملف api.js في الواجهة الأمامية")

    def run_comprehensive_fix(self):
        """تشغيل الإصلاح الشامل"""
        print("🚀 بدء الإصلاح الشامل للمرحلة الثالثة...")
        print("=" * 60)

        self.fix_all_imports()
        self.create_missing_models()
        self.fix_api_endpoints()
        self.create_security_fixes()
        self.optimize_frontend_connections()

        print("=" * 60)
        print("✅ تم الانتهاء من الإصلاح الشامل!")

        # طباعة النتائج
        print(f"\n📊 النتائج:")
        print(f"الإصلاحات المطبقة: {len(self.fixes_applied)}")
        print(f"الأخطاء المكتشفة: {len(self.errors_found)}")

        if self.fixes_applied:
            print(f"\n✅ الإصلاحات المطبقة:")
            for fix in self.fixes_applied:
                print(f"  - {fix}")

        if self.errors_found:
            print(f"\n❌ الأخطاء المكتشفة:")
            for error in self.errors_found:
                print(f"  - {error}")

        return {
            "fixes_applied": len(self.fixes_applied),
            "errors_found": len(self.errors_found),
            "success": len(self.errors_found) == 0,
        }


if __name__ == "__main__":
    fixer = ComprehensiveFix()
    results = fixer.run_comprehensive_fix()

    if results["success"]:
        print(f"\n🎉 الإصلاح الشامل مكتمل بنجاح!")
        print(f"تم تطبيق {results['fixes_applied']} إصلاح")
    else:
        print(f"\n⚠️ الإصلاح مكتمل مع {results['errors_found']} خطأ")
        print(f"تم تطبيق {results['fixes_applied']} إصلاح")
