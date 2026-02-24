#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 إصلاح وحدات التقارير والمخزون
Fix Reports and Inventory Modules Script

يقوم بإصلاح وتحسين وحدات التقارير والمخزون:
- إصلاح مسارات التقارير
- تحسين وحدة المخزون
- إضافة تقارير جديدة
- ربط الوحدات ببعضها البعض
"""

import os
from pathlib import Path

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def create_inventory_routes():
    """إنشاء مسارات المخزون المحسنة"""
    print_step("إنشاء مسارات المخزون المحسنة...")
    
    inventory_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/inventory.py
مسارات إدارة المخزون المحسنة
Enhanced Inventory Management Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.inventory import Inventory
from src.models.product import Product
from src.models.warehouse import Warehouse
from src.decorators.auth_decorators import token_required
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/api/inventory', methods=['GET'])
@token_required
def get_inventory():
    """الحصول على قائمة المخزون"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        warehouse_id = request.args.get('warehouse_id', type=int)
        product_id = request.args.get('product_id', type=int)
        
        query = Inventory.query
        
        # تطبيق المرشحات
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)
        if product_id:
            query = query.filter_by(product_id=product_id)
        
        # الترقيم
        inventory_items = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in inventory_items.items],
            'pagination': {
                'page': page,
                'pages': inventory_items.pages,
                'per_page': per_page,
                'total': inventory_items.total
            }
        })
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على المخزون: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على المخزون'
        }), 500

@inventory_bp.route('/api/inventory/summary', methods=['GET'])
@token_required
def get_inventory_summary():
    """الحصول على ملخص المخزون"""
    try:
        # إحصائيات عامة
        total_products = db.session.query(Inventory.product_id).distinct().count()
        total_quantity = db.session.query(db.func.sum(Inventory.quantity)).scalar() or 0
        low_stock_count = Inventory.query.filter(
            Inventory.quantity <= Inventory.min_stock_level
        ).count()
        
        # المنتجات الأكثر كمية
        top_products = db.session.query(
            Inventory.product_id,
            Product.name,
            db.func.sum(Inventory.quantity).label('total_quantity')
        ).join(Product).group_by(
            Inventory.product_id, Product.name
        ).order_by(
            db.func.sum(Inventory.quantity).desc()
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_products': total_products,
                'total_quantity': total_quantity,
                'low_stock_count': low_stock_count,
                'top_products': [
                    {
                        'product_id': item[0],
                        'product_name': item[1],
                        'total_quantity': item[2]
                    }
                    for item in top_products
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على ملخص المخزون: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على ملخص المخزون'
        }), 500

@inventory_bp.route('/api/inventory/low-stock', methods=['GET'])
@token_required
def get_low_stock_items():
    """الحصول على المنتجات منخفضة المخزون"""
    try:
        low_stock_items = db.session.query(
            Inventory, Product, Warehouse
        ).join(Product).join(Warehouse).filter(
            Inventory.quantity <= Inventory.min_stock_level
        ).all()
        
        result = []
        for inventory, product, warehouse in low_stock_items:
            result.append({
                'inventory_id': inventory.id,
                'product_id': product.id,
                'product_name': product.name,
                'warehouse_id': warehouse.id,
                'warehouse_name': warehouse.name,
                'current_quantity': inventory.quantity,
                'min_stock_level': inventory.min_stock_level,
                'shortage': inventory.min_stock_level - inventory.quantity
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'total': len(result)
        })
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على المنتجات منخفضة المخزون: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على المنتجات منخفضة المخزون'
        }), 500

@inventory_bp.route('/api/inventory/adjust', methods=['POST'])
@token_required
def adjust_inventory():
    """تعديل كمية المخزون"""
    try:
        data = request.get_json()
        
        required_fields = ['product_id', 'warehouse_id', 'adjustment_quantity', 'reason']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'جميع الحقول مطلوبة'
            }), 400
        
        # البحث عن عنصر المخزون أو إنشاؤه
        inventory_item = Inventory.query.filter_by(
            product_id=data['product_id'],
            warehouse_id=data['warehouse_id']
        ).first()
        
        if not inventory_item:
            inventory_item = Inventory(
                product_id=data['product_id'],
                warehouse_id=data['warehouse_id'],
                quantity=0
            )
            db.session.add(inventory_item)
        
        # تطبيق التعديل
        old_quantity = inventory_item.quantity
        inventory_item.quantity += data['adjustment_quantity']
        inventory_item.last_updated = datetime.utcnow()
        
        # تسجيل حركة المخزون (يمكن إضافة جدول منفصل لهذا)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'inventory_id': inventory_item.id,
                'old_quantity': old_quantity,
                'new_quantity': inventory_item.quantity,
                'adjustment': data['adjustment_quantity']
            },
            'message': 'تم تعديل المخزون بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تعديل المخزون: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في تعديل المخزون'
        }), 500

@inventory_bp.route('/api/inventory/transfer', methods=['POST'])
@token_required
def transfer_inventory():
    """نقل المخزون بين المستودعات"""
    try:
        data = request.get_json()
        
        required_fields = ['product_id', 'from_warehouse_id', 'to_warehouse_id', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'جميع الحقول مطلوبة'
            }), 400
        
        if data['from_warehouse_id'] == data['to_warehouse_id']:
            return jsonify({
                'success': False,
                'error': 'لا يمكن النقل إلى نفس المستودع'
            }), 400
        
        # التحقق من توفر الكمية في المستودع المصدر
        source_inventory = Inventory.query.filter_by(
            product_id=data['product_id'],
            warehouse_id=data['from_warehouse_id']
        ).first()
        
        if not source_inventory or source_inventory.quantity < data['quantity']:
            return jsonify({
                'success': False,
                'error': 'الكمية غير متوفرة في المستودع المصدر'
            }), 400
        
        # خصم من المستودع المصدر
        source_inventory.quantity -= data['quantity']
        source_inventory.last_updated = datetime.utcnow()
        
        # إضافة إلى المستودع الهدف
        target_inventory = Inventory.query.filter_by(
            product_id=data['product_id'],
            warehouse_id=data['to_warehouse_id']
        ).first()
        
        if not target_inventory:
            target_inventory = Inventory(
                product_id=data['product_id'],
                warehouse_id=data['to_warehouse_id'],
                quantity=0
            )
            db.session.add(target_inventory)
        
        target_inventory.quantity += data['quantity']
        target_inventory.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم نقل المخزون بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في نقل المخزون: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في نقل المخزون'
        }), 500
'''
    
    inventory_path = Path("backend/src/routes/inventory.py")
    with open(inventory_path, 'w', encoding='utf-8') as f:
        f.write(inventory_code)
    
    print_success("تم إنشاء مسارات المخزون المحسنة")

def create_enhanced_reports():
    """إنشاء مسارات التقارير المحسنة"""
    print_step("إنشاء مسارات التقارير المحسنة...")
    
    reports_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/reports.py
مسارات التقارير المحسنة
Enhanced Reports Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.product import Product
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.models.inventory import Inventory
from src.models.warehouse import Warehouse
from src.decorators.auth_decorators import token_required
import logging
from datetime import datetime, timedelta
from sqlalchemy import func, desc

logger = logging.getLogger(__name__)

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/api/reports/dashboard', methods=['GET'])
@token_required
def dashboard_report():
    """تقرير لوحة المعلومات"""
    try:
        # إحصائيات عامة
        total_products = Product.query.count()
        total_customers = Customer.query.count()
        total_suppliers = Supplier.query.count()
        total_warehouses = Warehouse.query.count()
        
        # إحصائيات المخزون
        total_inventory_value = db.session.query(
            func.sum(Inventory.quantity * Product.price)
        ).join(Product).scalar() or 0
        
        low_stock_count = Inventory.query.filter(
            Inventory.quantity <= Inventory.min_stock_level
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'overview': {
                    'total_products': total_products,
                    'total_customers': total_customers,
                    'total_suppliers': total_suppliers,
                    'total_warehouses': total_warehouses
                },
                'inventory': {
                    'total_value': float(total_inventory_value),
                    'low_stock_items': low_stock_count
                }
            }
        })
        
    except Exception as e:
        logger.error(f"خطأ في تقرير لوحة المعلومات: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في إنشاء تقرير لوحة المعلومات'
        }), 500

@reports_bp.route('/api/reports/inventory', methods=['GET'])
@token_required
def inventory_report():
    """تقرير المخزون"""
    try:
        warehouse_id = request.args.get('warehouse_id', type=int)
        category_id = request.args.get('category_id', type=int)
        
        query = db.session.query(
            Product.id,
            Product.name,
            Product.sku,
            Warehouse.name.label('warehouse_name'),
            Inventory.quantity,
            Inventory.min_stock_level,
            Inventory.max_stock_level,
            Product.price,
            (Inventory.quantity * Product.price).label('total_value')
        ).join(Inventory).join(Warehouse)
        
        # تطبيق المرشحات
        if warehouse_id:
            query = query.filter(Inventory.warehouse_id == warehouse_id)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        results = query.all()
        
        # تحويل النتائج
        inventory_data = []
        total_value = 0
        
        for row in results:
            item_data = {
                'product_id': row.id,
                'product_name': row.name,
                'sku': row.sku,
                'warehouse_name': row.warehouse_name,
                'quantity': row.quantity,
                'min_stock_level': row.min_stock_level,
                'max_stock_level': row.max_stock_level,
                'unit_price': float(row.price) if row.price else 0,
                'total_value': float(row.total_value) if row.total_value else 0,
                'stock_status': 'منخفض' if row.quantity <= row.min_stock_level else 'طبيعي'
            }
            inventory_data.append(item_data)
            total_value += item_data['total_value']
        
        return jsonify({
            'success': True,
            'data': {
                'items': inventory_data,
                'summary': {
                    'total_items': len(inventory_data),
                    'total_value': total_value
                }
            }
        })
        
    except Exception as e:
        logger.error(f"خطأ في تقرير المخزون: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في إنشاء تقرير المخزون'
        }), 500

@reports_bp.route('/api/reports/sales', methods=['GET'])
@token_required
def sales_report():
    """تقرير المبيعات"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # تحويل التواريخ
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date = datetime.now() - timedelta(days=30)
        
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = datetime.now()
        
        # هنا يجب إضافة استعلامات المبيعات الفعلية
        # حالياً سنعيد بيانات وهمية
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'summary': {
                    'total_sales': 0,
                    'total_orders': 0,
                    'average_order_value': 0
                },
                'message': 'تقرير المبيعات قيد التطوير'
            }
        })
        
    except Exception as e:
        logger.error(f"خطأ في تقرير المبيعات: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في إنشاء تقرير المبيعات'
        }), 500

@reports_bp.route('/api/reports/products', methods=['GET'])
@token_required
def products_report():
    """تقرير المنتجات"""
    try:
        # المنتجات الأكثر مبيعاً (بناءً على المخزون المتاح)
        top_products = db.session.query(
            Product.id,
            Product.name,
            Product.sku,
            func.sum(Inventory.quantity).label('total_stock')
        ).join(Inventory).group_by(
            Product.id, Product.name, Product.sku
        ).order_by(desc('total_stock')).limit(10).all()
        
        # المنتجات بدون مخزون
        out_of_stock = db.session.query(Product).outerjoin(Inventory).filter(
            (Inventory.quantity == 0) | (Inventory.quantity.is_(None))
        ).all()
        
        return jsonify({
            'success': True,
            'data': {
                'top_products': [
                    {
                        'product_id': item.id,
                        'name': item.name,
                        'sku': item.sku,
                        'total_stock': item.total_stock
                    }
                    for item in top_products
                ],
                'out_of_stock': [
                    {
                        'product_id': item.id,
                        'name': item.name,
                        'sku': item.sku
                    }
                    for item in out_of_stock
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"خطأ في تقرير المنتجات: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في إنشاء تقرير المنتجات'
        }), 500

@reports_bp.route('/api/reports/export', methods=['POST'])
@token_required
def export_report():
    """تصدير التقارير"""
    try:
        data = request.get_json()
        report_type = data.get('report_type')
        format_type = data.get('format', 'json')  # json, csv, excel
        
        if not report_type:
            return jsonify({
                'success': False,
                'error': 'نوع التقرير مطلوب'
            }), 400
        
        # هنا يمكن إضافة منطق التصدير الفعلي
        
        return jsonify({
            'success': True,
            'data': {
                'report_type': report_type,
                'format': format_type,
                'message': 'ميزة التصدير قيد التطوير'
            }
        })
        
    except Exception as e:
        logger.error(f"خطأ في تصدير التقرير: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في تصدير التقرير'
        }), 500
'''
    
    reports_path = Path("backend/src/routes/reports.py")
    with open(reports_path, 'w', encoding='utf-8') as f:
        f.write(reports_code)
    
    print_success("تم إنشاء مسارات التقارير المحسنة")

def create_inventory_model():
    """إنشاء نموذج المخزون المحسن"""
    print_step("إنشاء نموذج المخزون المحسن...")
    
    inventory_model = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/models/inventory.py
نموذج المخزون المحسن
Enhanced Inventory Model
"""

from src.database import db
from datetime import datetime

class Inventory(db.Model):
    """نموذج المخزون"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    reserved_quantity = db.Column(db.Integer, default=0)  # الكمية المحجوزة
    min_stock_level = db.Column(db.Integer, default=0)  # الحد الأدنى للمخزون
    max_stock_level = db.Column(db.Integer, default=0)  # الحد الأقصى للمخزون
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات
    product = db.relationship('Product', backref='inventory_items')
    warehouse = db.relationship('Warehouse', backref='inventory_items')
    
    # فهرس فريد لضمان عدم تكرار المنتج في نفس المستودع
    __table_args__ = (db.UniqueConstraint('product_id', 'warehouse_id'),)
    
    @property
    def available_quantity(self):
        """الكمية المتاحة (الكمية الإجمالية - المحجوزة)"""
        return self.quantity - self.reserved_quantity
    
    @property
    def is_low_stock(self):
        """هل المخزون منخفض؟"""
        return self.quantity <= self.min_stock_level
    
    @property
    def is_out_of_stock(self):
        """هل المخزون منتهي؟"""
        return self.quantity <= 0
    
    @property
    def stock_status(self):
        """حالة المخزون"""
        if self.is_out_of_stock:
            return 'out_of_stock'
        elif self.is_low_stock:
            return 'low_stock'
        elif self.quantity >= self.max_stock_level:
            return 'overstock'
        else:
            return 'normal'
    
    def reserve_quantity(self, quantity):
        """حجز كمية من المخزون"""
        if self.available_quantity >= quantity:
            self.reserved_quantity += quantity
            return True
        return False
    
    def release_quantity(self, quantity):
        """إلغاء حجز كمية من المخزون"""
        if self.reserved_quantity >= quantity:
            self.reserved_quantity -= quantity
            return True
        return False
    
    def adjust_quantity(self, adjustment, reason=None):
        """تعديل كمية المخزون"""
        old_quantity = self.quantity
        self.quantity += adjustment
        self.last_updated = datetime.utcnow()
        
        # يمكن إضافة تسجيل الحركة هنا
        return {
            'old_quantity': old_quantity,
            'new_quantity': self.quantity,
            'adjustment': adjustment,
            'reason': reason
        }
    
    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id,
            'quantity': self.quantity,
            'reserved_quantity': self.reserved_quantity,
            'available_quantity': self.available_quantity,
            'min_stock_level': self.min_stock_level,
            'max_stock_level': self.max_stock_level,
            'stock_status': self.stock_status,
            'is_low_stock': self.is_low_stock,
            'is_out_of_stock': self.is_out_of_stock,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'product_name': self.product.name if self.product else None,
            'warehouse_name': self.warehouse.name if self.warehouse else None
        }
    
    def __repr__(self):
        return f'<Inventory Product:{self.product_id} Warehouse:{self.warehouse_id} Qty:{self.quantity}>'
'''
    
    inventory_model_path = Path("backend/src/models/inventory.py")
    with open(inventory_model_path, 'w', encoding='utf-8') as f:
        f.write(inventory_model)
    
    print_success("تم إنشاء نموذج المخزون المحسن")

def update_app_blueprints():
    """تحديث app.py لتسجيل المخططات المحسنة"""
    print_step("تحديث تسجيل المخططات...")
    
    app_py_path = Path("backend/app.py")
    
    if app_py_path.exists():
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التأكد من تسجيل المخططات المحسنة
        if "('routes.inventory', 'inventory_bp')" not in content:
            content = content.replace(
                "('routes.invoices', 'invoices_bp'),",
                "('routes.invoices', 'invoices_bp'),\n        ('routes.inventory', 'inventory_bp'),"
            )
        
        if "('routes.reports', 'reports_bp')" not in content:
            content = content.replace(
                "('routes.inventory', 'inventory_bp'),",
                "('routes.inventory', 'inventory_bp'),\n        ('routes.reports', 'reports_bp'),"
            )
        
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print_success("تم تحديث تسجيل المخططات")

def main():
    print("📊 بدء إصلاح وحدات التقارير والمخزون...")
    print("=" * 60)
    
    # إنشاء نموذج المخزون المحسن
    create_inventory_model()
    
    # إنشاء مسارات المخزون المحسنة
    create_inventory_routes()
    
    # إنشاء مسارات التقارير المحسنة
    create_enhanced_reports()
    
    # تحديث تسجيل المخططات
    update_app_blueprints()
    
    print("=" * 60)
    print_success("تم إصلاح وحدات التقارير والمخزون بنجاح!")
    print("📋 التحسينات المطبقة:")
    print("   - إنشاء نموذج المخزون المحسن")
    print("   - تحسين مسارات المخزون")
    print("   - إنشاء تقارير شاملة")
    print("   - ربط الوحدات ببعضها البعض")
    print("   - إضافة ميزات متقدمة للمخزون")
    print()
    print("📋 الميزات الجديدة:")
    print("   - تقرير لوحة المعلومات")
    print("   - تقرير المخزون التفصيلي")
    print("   - تقرير المنتجات منخفضة المخزون")
    print("   - نقل المخزون بين المستودعات")
    print("   - تعديل كميات المخزون")

if __name__ == "__main__":
    main()
