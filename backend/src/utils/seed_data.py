"""
Database Seed Data Script
Populates the database with initial/sample data for testing and development.
"""

from datetime import datetime, timedelta
import random
from decimal import Decimal

def seed_database(db, models):
    """
    Seed the database with initial data.
    
    Args:
        db: SQLAlchemy database instance
        models: Dictionary of model classes
    """
    print("🌱 Starting database seeding...")
    
    # Get models
    User = models.get('User')
    Category = models.get('Category')
    Product = models.get('Product')
    Warehouse = models.get('Warehouse')
    Supplier = models.get('Supplier')
    Customer = models.get('Customer')
    
    try:
        # Create admin user if not exists
        if User:
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@store.local',
                    first_name='مدير',
                    last_name='النظام',
                    role='admin',
                    is_active=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                print("  ✅ Admin user created")
        
        # Create default categories
        if Category:
            categories_data = [
                {'name': 'إلكترونيات', 'name_en': 'Electronics', 'code': 'ELEC'},
                {'name': 'ملابس', 'name_en': 'Clothing', 'code': 'CLTH'},
                {'name': 'أغذية', 'name_en': 'Food', 'code': 'FOOD'},
                {'name': 'مستلزمات منزلية', 'name_en': 'Home', 'code': 'HOME'},
                {'name': 'أدوات مكتبية', 'name_en': 'Office', 'code': 'OFFC'},
            ]
            
            for cat_data in categories_data:
                exists = Category.query.filter_by(code=cat_data['code']).first()
                if not exists:
                    cat = Category(**cat_data)
                    db.session.add(cat)
            print("  ✅ Categories created")
        
        # Create default warehouse
        if Warehouse:
            main_warehouse = Warehouse.query.filter_by(code='MAIN').first()
            if not main_warehouse:
                main_warehouse = Warehouse(
                    name='المستودع الرئيسي',
                    name_en='Main Warehouse',
                    code='MAIN',
                    address='المدينة الصناعية',
                    is_default=True,
                    is_active=True
                )
                db.session.add(main_warehouse)
                print("  ✅ Main warehouse created")
        
        # Create sample suppliers
        if Supplier:
            suppliers_data = [
                {'name': 'شركة التوريدات العامة', 'code': 'SUP001', 'phone': '0551234567'},
                {'name': 'مؤسسة المنتجات الغذائية', 'code': 'SUP002', 'phone': '0559876543'},
            ]
            
            for sup_data in suppliers_data:
                exists = Supplier.query.filter_by(code=sup_data['code']).first()
                if not exists:
                    sup = Supplier(**sup_data, is_active=True)
                    db.session.add(sup)
            print("  ✅ Suppliers created")
        
        # Create sample customers
        if Customer:
            customers_data = [
                {'name': 'عميل نقدي', 'code': 'CASH', 'customer_type': 'individual', 'is_default': True},
                {'name': 'شركة التجارة الحديثة', 'code': 'CUS001', 'customer_type': 'company'},
            ]
            
            for cust_data in customers_data:
                exists = Customer.query.filter_by(code=cust_data['code']).first()
                if not exists:
                    cust = Customer(**cust_data, is_active=True)
                    db.session.add(cust)
            print("  ✅ Customers created")
        
        # Create sample products
        if Product and Category:
            electronics = Category.query.filter_by(code='ELEC').first()
            if electronics:
                products_data = [
                    {'name': 'هاتف ذكي', 'sku': 'PRD001', 'barcode': '6281001234567', 
                     'price': Decimal('1500.00'), 'cost': Decimal('1200.00')},
                    {'name': 'ساعة ذكية', 'sku': 'PRD002', 'barcode': '6281001234568', 
                     'price': Decimal('350.00'), 'cost': Decimal('250.00')},
                    {'name': 'سماعات لاسلكية', 'sku': 'PRD003', 'barcode': '6281001234569', 
                     'price': Decimal('200.00'), 'cost': Decimal('120.00')},
                ]
                
                for prod_data in products_data:
                    exists = Product.query.filter_by(sku=prod_data['sku']).first()
                    if not exists:
                        prod = Product(
                            **prod_data,
                            category_id=electronics.id,
                            is_active=True,
                            track_inventory=True,
                            track_lots=True
                        )
                        db.session.add(prod)
                print("  ✅ Sample products created")
        
        db.session.commit()
        print("✅ Database seeding complete!")
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding database: {str(e)}")
        return False


def seed_demo_data(db, models):
    """
    Seed additional demo data for presentations.
    """
    print("🎭 Seeding demo data...")
    
    # Add more comprehensive demo data here
    # This can include:
    # - More products
    # - Sample invoices
    # - Sample inventory movements
    # - Sample lots
    
    print("✅ Demo data seeding complete!")
    return True


if __name__ == '__main__':
    print("This script should be imported and called with db and models parameters.")
    print("Usage: from utils.seed_data import seed_database")
