"""
إنشاء بيانات تجريبية للوطات المتقدمة
Created: 2025-12-13
"""

import sys
from pathlib import Path

# Add both backend and src to path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / 'src'
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(src_dir))

from src.database import db
from src.models.lot_advanced import LotAdvanced
from src.models.product_advanced import ProductAdvanced as Product
from datetime import datetime, timedelta, date
import random


def create_sample_batches(count=20):
    """إنشاء بيانات تجريبية للوطات"""
    
    # Get existing products
    products = Product.query.limit(10).all()
    
    if not products:
        print("❌ لا توجد منتجات في قاعدة البيانات. يرجى إضافة منتجات أولاً.")
        return []
    
    batches = []
    statuses = ['active', 'active', 'active', 'active', 'quarantine', 'expired']
    quality_statuses = ['approved', 'approved', 'approved', 'pending', 'rejected']
    
    for i in range(1, count + 1):
        product = random.choice(products)
        
        # Generate dates
        manufacture_date = date.today() - timedelta(days=random.randint(30, 365))
        expiry_date = manufacture_date + timedelta(days=random.randint(365, 730))
        received_date = manufacture_date + timedelta(days=random.randint(7, 30))
        
        # Generate batch
        batch = LotAdvanced(
            batch_number=f'BATCH-{i:05d}',
            internal_batch_number=f'INT-{i:05d}',
            supplier_batch_number=f'SUP-{random.randint(1000, 9999)}',
            ministry_batch_number=f'MIN-{random.randint(10000, 99999)}' if random.random() > 0.5 else None,
            product_id=product.id,
            warehouse_id=1 if random.random() > 0.3 else None,
            supplier_id=1 if random.random() > 0.3 else None,
            quantity=random.randint(100, 1000),
            original_quantity=random.randint(100, 1000),
            cost_price=random.uniform(50, 500),
            selling_price=random.uniform(60, 600),
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            received_date=received_date,
            germination_rate=random.uniform(80, 98) if random.random() > 0.5 else None,
            purity_percentage=random.uniform(95, 99.9),
            moisture_content=random.uniform(5, 15),
            temperature_storage=random.uniform(15, 25),
            ph_level=random.uniform(6.0, 7.5) if random.random() > 0.5 else None,
            status=random.choice(statuses),
            quality_status=random.choice(quality_statuses),
            quality_test_date=received_date + timedelta(days=1) if random.random() > 0.3 else None,
            ministry_approval_date=received_date + timedelta(days=7) if random.random() > 0.5 else None,
            ministry_approval_number=f'APP-{random.randint(10000, 99999)}' if random.random() > 0.5 else None,
            storage_location=f'رف {random.randint(1, 20)}-{random.randint(1, 10)}',
            notes=f'ملاحظات اللوط {i}',
            created_by=1
        )
        batches.append(batch)
    
    db.session.bulk_save_objects(batches)
    db.session.commit()
    
    print(f'✅ تم إنشاء {len(batches)} لوط تجريبي')
    return batches


def main():
    """تشغيل السكريبت"""
    from app import app
    
    with app.app_context():
        print('🚀 بدء إنشاء بيانات تجريبية للوطات...')
        print()
        
        # Check if batches_advanced table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'batches_advanced' not in tables:
            print('❌ جدول batches_advanced غير موجود!')
            print('يرجى تشغيل migration أولاً:')
            print('sqlite3 instance/inventory.db < migrations/001_create_batches_advanced.sql')
            return
        
        # Create sample batches
        batches = create_sample_batches(20)
        
        print()
        print('✅ تم إنشاء جميع البيانات التجريبية بنجاح!')
        print(f'   - {len(batches)} لوط')
        print()
        print('📊 يمكنك الآن اختبار APIs:')
        print('   GET  /api/batches')
        print('   GET  /api/batches/1')
        print('   GET  /api/batches/expiring-soon')
        print('   GET  /api/batches/low-stock')
        print('   GET  /api/batches/statistics')


if __name__ == '__main__':
    main()
