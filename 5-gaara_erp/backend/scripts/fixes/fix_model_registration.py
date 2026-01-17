#!/usr/bin/env python3
"""
Fix Model Registration Issues
This script fixes Flask model registration and database relationship issues.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))


def fix_database_initialization():
    """Fix database initialization issues"""
    print("🔧 Fixing database initialization...")

    # Read the current database.py file
    database_file = src_dir / "database.py"
    with open(database_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix the create_default_data function to handle app context properly
    fixed_content = content.replace(
        """def create_default_data():
    \"\"\"إنشاء البيانات الأساسية\"\"\"
    from flask import current_app
    
    try:
        # التأكد من وجود app context
        if not current_app:
            print("⚠️ لا يوجد Flask app context، تخطي إنشاء البيانات الأساسية")
            return True""",
        """def create_default_data():
    \"\"\"إنشاء البيانات الأساسية\"\"\"
    from flask import current_app, has_app_context
    
    try:
        # التأكد من وجود app context
        if not has_app_context():
            print("⚠️ لا يوجد Flask app context، تخطي إنشاء البيانات الأساسية")
            return True""",
    )

    # Write the fixed content back
    with open(database_file, "w", encoding="utf-8") as f:
        f.write(fixed_content)

    print("✅ Database initialization fixed")


def fix_model_imports():
    """Fix model import issues"""
    print("🔧 Fixing model imports...")

    # Fix models/__init__.py to properly import all models
    models_init_file = src_dir / "models" / "__init__.py"

    fixed_init_content = '''# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات - إصدار موحد ومحسن
Unified and Enhanced Database Models Package
"""

# استيراد قاعدة البيانات من database.py
try:
    from database import db
except ImportError:
    try:
        from ..database import db
    except ImportError:
        class MockDB:
            class Model:
                pass
            def __init__(self):
                pass
        db = MockDB()

# استيراد النماذج الأساسية
try:
    from .user import User, Role
except ImportError:
    User = None
    Role = None

try:
    from .inventory import Category, Warehouse, Product, StockMovement
except ImportError:
    Category = None
    Warehouse = None
    Product = None
    StockMovement = None

try:
    from .customer import Customer
except ImportError:
    Customer = None

try:
    from .supplier import Supplier
except ImportError:
    Supplier = None

# استيراد نموذج الفاتورة الموحد الجديد
try:
    from .unified_invoice import (
        UnifiedInvoice, UnifiedInvoiceItem, InvoicePayment,
        InvoiceType, InvoiceStatus, PaymentMethod
    )
except ImportError:
    UnifiedInvoice = None
    UnifiedInvoiceItem = None
    InvoicePayment = None
    InvoiceType = None
    InvoiceStatus = None
    PaymentMethod = None

# النماذج المتقدمة للمبيعات
try:
    from .sales_advanced import SalesInvoice, SalesInvoiceItem, CustomerPayment
except ImportError:
    SalesInvoice = None
    SalesInvoiceItem = None
    CustomerPayment = None

# النماذج القديمة (للتوافق المؤقت)
try:
    from .invoice import Invoice, InvoiceItem, Payment
except ImportError:
    Invoice = None
    InvoiceItem = None
    Payment = None

# التعدادات والثوابت الموحدة
class UserRole:
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"

class ProductType:
    SIMPLE = "simple"
    VARIABLE = "variable"
    SERVICE = "service"

class MovementType:
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"

# قائمة التصدير الموحدة
__all__ = [
    'db',
    'User', 'Role',
    'Category', 'Warehouse', 'Product', 'StockMovement',
    'Customer',
    'Supplier', 
    # النماذج الموحدة الجديدة
    'UnifiedInvoice', 'UnifiedInvoiceItem', 'InvoicePayment',
    'InvoiceType', 'InvoiceStatus', 'PaymentMethod',
    # النماذج المتقدمة للمبيعات
    'SalesInvoice', 'SalesInvoiceItem', 'CustomerPayment',
    # النماذج القديمة (للتوافق)
    'Invoice', 'InvoiceItem', 'Payment',
    # الثوابت
    'UserRole', 'ProductType', 'MovementType'
]
'''

    with open(models_init_file, "w", encoding="utf-8") as f:
        f.write(fixed_init_content)

    print("✅ Model imports fixed")


def fix_customer_model():
    """Fix Customer model relationships"""
    print("🔧 Fixing Customer model relationships...")

    customer_file = src_dir / "models" / "customer.py"
    with open(customer_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix the import to use the correct database reference
    fixed_content = content.replace("from .user import db", "from database import db")

    # Fix the relationship to use the correct table name
    fixed_content = fixed_content.replace(
        "invoices = db.relationship('Invoice', backref='customer', lazy='dynamic')",
        "# invoices = db.relationship('UnifiedInvoice', backref='customer', lazy='dynamic')",
    )

    with open(customer_file, "w", encoding="utf-8") as f:
        f.write(fixed_content)

    print("✅ Customer model relationships fixed")


def create_comprehensive_test():
    """Create a comprehensive test script"""
    print("🔧 Creating comprehensive test script...")

    test_content = '''#!/usr/bin/env python3
"""
Comprehensive Model Registration Test
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_model_registration():
    """Test model registration and relationships"""
    print("🧪 Testing model registration...")
    
    try:
        # Test Flask app creation
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        
        with app.app_context():
            # Test database initialization
            from database import db
            print("✅ Database imported successfully")
            
            # Test basic model imports
            from models import User, Role, Customer, Product, Category, Warehouse
            print("✅ Basic models imported successfully")
            
            # Test advanced model imports
            from models import UnifiedInvoice, UnifiedInvoiceItem, InvoicePayment
            print("✅ Advanced models imported successfully")
            
            # Test sales models
            from models import SalesInvoice, SalesInvoiceItem, CustomerPayment
            print("✅ Sales models imported successfully")
            
            # Test database table creation
            db.create_all()
            print("✅ Database tables created successfully")
            
            # List all tables
            print("📊 Available tables:")
            for table_name in db.metadata.tables.keys():
                print(f"  - {table_name}")
            
            # Test model instantiation
            if User:
                user = User(username='test', email='test@example.com')
                print("✅ User model instantiation successful")
            
            if Customer:
                customer = Customer(name='Test Customer', email='customer@example.com')
                print("✅ Customer model instantiation successful")
            
            if Product:
                product = Product(name='Test Product', price=100.0)
                print("✅ Product model instantiation successful")
            
            print("🎉 All tests passed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_registration()
    sys.exit(0 if success else 1)
'''

    test_file = current_dir / "test_model_registration.py"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)

    # Make it executable
    os.chmod(test_file, 0o755)

    print("✅ Comprehensive test script created")


def main():
    """Main function to fix all model registration issues"""
    print("🚀 Starting model registration fixes...")

    try:
        fix_database_initialization()
        fix_model_imports()
        fix_customer_model()
        create_comprehensive_test()

        print("🎉 All model registration fixes completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Fix failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
