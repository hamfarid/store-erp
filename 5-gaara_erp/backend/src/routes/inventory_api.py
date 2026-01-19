"""
Inventory API Routes - مسارات API المخزون
Gaara ERP v12

API endpoints for inventory and product management.

Author: Global v35.0 Singularity
Version: 1.0.0
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from flask import Blueprint, g, jsonify, request

if TYPE_CHECKING:
    from flask import Response

# Create Blueprint
inventory_api = Blueprint('inventory_api', __name__, url_prefix='/api/inventory')


# =============================================================================
# Mock Data (Replace with DB queries)
# =============================================================================

MOCK_PRODUCTS = [
    {
        'id': 'PRD-001',
        'name': 'قمح فاخر',
        'name_ar': 'قمح فاخر',
        'sku': 'WHT-001',
        'category': 'حبوب',
        'stock': 5000,
        'min_stock': 1000,
        'max_stock': 10000,
        'unit': 'كجم',
        'warehouse': 'المستودع الرئيسي',
        'warehouse_id': '1',
        'price': 15,
        'cost': 10,
        'status': 'in_stock',
        'is_active': True,
        'description': 'قمح فاخر عالي الجودة',
        'created_at': '2026-01-01T00:00:00Z'
    },
    {
        'id': 'PRD-002',
        'name': 'سماد NPK',
        'name_ar': 'سماد NPK',
        'sku': 'FRT-001',
        'category': 'أسمدة',
        'stock': 250,
        'min_stock': 500,
        'max_stock': 2000,
        'unit': 'كجم',
        'warehouse': 'المستودع الفرعي',
        'warehouse_id': '2',
        'price': 45,
        'cost': 30,
        'status': 'low_stock',
        'is_active': True,
        'description': 'سماد متوازن للمحاصيل',
        'created_at': '2026-01-01T00:00:00Z'
    },
    {
        'id': 'PRD-003',
        'name': 'بذور طماطم',
        'name_ar': 'بذور طماطم',
        'sku': 'SED-001',
        'category': 'بذور',
        'stock': 0,
        'min_stock': 100,
        'max_stock': 500,
        'unit': 'عبوة',
        'warehouse': 'المستودع الرئيسي',
        'warehouse_id': '1',
        'price': 120,
        'cost': 80,
        'status': 'out_of_stock',
        'is_active': True,
        'description': 'بذور طماطم هجين',
        'created_at': '2026-01-01T00:00:00Z'
    },
]

MOCK_CATEGORIES = [
    {'id': 1, 'name': 'حبوب', 'name_en': 'Grains', 'count': 15},
    {'id': 2, 'name': 'أسمدة', 'name_en': 'Fertilizers', 'count': 8},
    {'id': 3, 'name': 'بذور', 'name_en': 'Seeds', 'count': 25},
    {'id': 4, 'name': 'مبيدات', 'name_en': 'Pesticides', 'count': 12},
    {'id': 5, 'name': 'شتلات', 'name_en': 'Seedlings', 'count': 30},
]

MOCK_WAREHOUSES = [
    {'id': '1', 'name': 'المستودع الرئيسي', 'location': 'الرياض', 'capacity': 10000},
    {'id': '2', 'name': 'المستودع الفرعي', 'location': 'جدة', 'capacity': 5000},
    {'id': '3', 'name': 'المشتل', 'location': 'الدمام', 'capacity': 2000},
]

MOCK_MOVEMENTS = []


# =============================================================================
# Helper Functions
# =============================================================================

def calculate_status(stock: int, min_stock: int) -> str:
    """Calculate product status based on stock levels."""
    if stock <= 0:
        return 'out_of_stock'
    elif stock < min_stock:
        return 'low_stock'
    else:
        return 'in_stock'


def generate_sku(category: str, count: int) -> str:
    """Generate SKU for new product."""
    prefix = category[:3].upper() if category else 'PRD'
    return f"{prefix}-{count:03d}"


# =============================================================================
# Product Endpoints
# =============================================================================

@inventory_api.route('/products', methods=['GET'])
def get_products() -> Response:
    """Get all products with optional filtering."""
    category = request.args.get('category')
    status = request.args.get('status')
    warehouse = request.args.get('warehouse')
    search = request.args.get('search', '').lower()
    
    products = MOCK_PRODUCTS.copy()
    
    if category:
        products = [p for p in products if p['category'] == category]
    
    if status:
        products = [p for p in products if p['status'] == status]
    
    if warehouse:
        products = [p for p in products if p['warehouse'] == warehouse]
    
    if search:
        products = [
            p for p in products 
            if search in p['name'].lower() or search in p['sku'].lower()
        ]
    
    return jsonify({
        'success': True,
        'data': products
    })


@inventory_api.route('/products/<product_id>', methods=['GET'])
def get_product(product_id: str) -> Response:
    """Get a single product by ID."""
    product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'Product not found',
            'message_ar': 'المنتج غير موجود'
        }), 404
    
    return jsonify({
        'success': True,
        'data': product
    })


@inventory_api.route('/products', methods=['POST'])
def create_product() -> Response:
    """Create a new product."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'sku', 'category', 'unit', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}',
                'message_ar': f'الحقل مطلوب: {field}'
            }), 400
    
    # Check SKU uniqueness
    if any(p['sku'] == data['sku'] for p in MOCK_PRODUCTS):
        return jsonify({
            'success': False,
            'message': 'SKU already exists',
            'message_ar': 'رمز SKU موجود مسبقاً'
        }), 400
    
    # Generate ID
    new_id = f"PRD-{len(MOCK_PRODUCTS) + 1:03d}"
    
    # Calculate status
    stock = data.get('stock', 0)
    min_stock = data.get('min_stock', 0)
    status = calculate_status(stock, min_stock)
    
    new_product = {
        'id': new_id,
        'name': data.get('name'),
        'name_ar': data.get('name_ar', data.get('name')),
        'sku': data.get('sku'),
        'category': data.get('category'),
        'stock': stock,
        'min_stock': min_stock,
        'max_stock': data.get('max_stock', 0),
        'unit': data.get('unit'),
        'warehouse': data.get('warehouse', ''),
        'warehouse_id': data.get('warehouse_id', ''),
        'price': data.get('price', 0),
        'cost': data.get('cost', 0),
        'status': status,
        'is_active': data.get('is_active', True),
        'description': data.get('description', ''),
        'created_at': datetime.now().isoformat()
    }
    
    MOCK_PRODUCTS.append(new_product)
    
    return jsonify({
        'success': True,
        'data': new_product,
        'message': 'Product created successfully',
        'message_ar': 'تم إضافة المنتج بنجاح'
    }), 201


@inventory_api.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id: str) -> Response:
    """Update a product."""
    data = request.get_json()
    
    product_index = next(
        (i for i, p in enumerate(MOCK_PRODUCTS) if p['id'] == product_id), 
        None
    )
    
    if product_index is None:
        return jsonify({
            'success': False,
            'message': 'Product not found',
            'message_ar': 'المنتج غير موجود'
        }), 404
    
    product = MOCK_PRODUCTS[product_index]
    
    # Update fields
    for key, value in data.items():
        if key in product and key not in ['id', 'created_at']:
            product[key] = value
    
    # Recalculate status
    product['status'] = calculate_status(product['stock'], product['min_stock'])
    product['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'data': product,
        'message': 'Product updated successfully',
        'message_ar': 'تم تحديث المنتج بنجاح'
    })


@inventory_api.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id: str) -> Response:
    """Delete a product."""
    global MOCK_PRODUCTS
    
    product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'Product not found',
            'message_ar': 'المنتج غير موجود'
        }), 404
    
    MOCK_PRODUCTS = [p for p in MOCK_PRODUCTS if p['id'] != product_id]
    
    return jsonify({
        'success': True,
        'message': 'Product deleted',
        'message_ar': 'تم حذف المنتج'
    })


# =============================================================================
# Stock Operations
# =============================================================================

@inventory_api.route('/products/<product_id>/adjust', methods=['POST'])
def adjust_stock(product_id: str) -> Response:
    """Adjust product stock."""
    data = request.get_json()
    
    product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'Product not found',
            'message_ar': 'المنتج غير موجود'
        }), 404
    
    adjustment_type = data.get('type', 'add')  # add, subtract, set
    quantity = data.get('quantity', 0)
    reason = data.get('reason', '')
    
    old_stock = product['stock']
    
    if adjustment_type == 'add':
        product['stock'] += quantity
    elif adjustment_type == 'subtract':
        product['stock'] = max(0, product['stock'] - quantity)
    elif adjustment_type == 'set':
        product['stock'] = max(0, quantity)
    
    # Recalculate status
    product['status'] = calculate_status(product['stock'], product['min_stock'])
    
    # Record movement
    movement = {
        'id': f"MOV-{len(MOCK_MOVEMENTS) + 1:04d}",
        'product_id': product_id,
        'type': adjustment_type,
        'quantity': quantity,
        'old_stock': old_stock,
        'new_stock': product['stock'],
        'reason': reason,
        'date': datetime.now().isoformat()
    }
    MOCK_MOVEMENTS.append(movement)
    
    return jsonify({
        'success': True,
        'data': {
            'product': product,
            'movement': movement
        },
        'message': 'Stock adjusted',
        'message_ar': 'تم تعديل المخزون'
    })


@inventory_api.route('/products/<product_id>/movements', methods=['GET'])
def get_stock_movements(product_id: str) -> Response:
    """Get stock movement history for a product."""
    movements = [m for m in MOCK_MOVEMENTS if m['product_id'] == product_id]
    
    return jsonify({
        'success': True,
        'data': movements
    })


@inventory_api.route('/transfers', methods=['POST'])
def transfer_stock() -> Response:
    """Transfer stock between warehouses."""
    data = request.get_json()
    
    product_id = data.get('product_id')
    from_warehouse = data.get('from_warehouse')
    to_warehouse = data.get('to_warehouse')
    quantity = data.get('quantity', 0)
    
    # Validate
    product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'Product not found',
            'message_ar': 'المنتج غير موجود'
        }), 404
    
    if product['stock'] < quantity:
        return jsonify({
            'success': False,
            'message': 'Insufficient stock',
            'message_ar': 'المخزون غير كافٍ'
        }), 400
    
    # Create transfer record
    transfer = {
        'id': f"TRF-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'product_id': product_id,
        'from_warehouse': from_warehouse,
        'to_warehouse': to_warehouse,
        'quantity': quantity,
        'status': 'completed',
        'date': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'data': transfer,
        'message': 'Stock transferred',
        'message_ar': 'تم نقل المخزون'
    })


# =============================================================================
# Categories
# =============================================================================

@inventory_api.route('/categories', methods=['GET'])
def get_categories() -> Response:
    """Get all product categories."""
    return jsonify({
        'success': True,
        'data': MOCK_CATEGORIES
    })


@inventory_api.route('/categories', methods=['POST'])
def create_category() -> Response:
    """Create a new category."""
    data = request.get_json()
    
    new_category = {
        'id': len(MOCK_CATEGORIES) + 1,
        'name': data.get('name'),
        'name_en': data.get('name_en', ''),
        'count': 0
    }
    
    MOCK_CATEGORIES.append(new_category)
    
    return jsonify({
        'success': True,
        'data': new_category,
        'message': 'Category created',
        'message_ar': 'تم إضافة التصنيف'
    }), 201


# =============================================================================
# Warehouses
# =============================================================================

@inventory_api.route('/warehouses', methods=['GET'])
def get_warehouses() -> Response:
    """Get all warehouses."""
    return jsonify({
        'success': True,
        'data': MOCK_WAREHOUSES
    })


@inventory_api.route('/warehouses/<warehouse_id>/stock', methods=['GET'])
def get_warehouse_stock(warehouse_id: str) -> Response:
    """Get stock in a specific warehouse."""
    products = [p for p in MOCK_PRODUCTS if p['warehouse_id'] == warehouse_id]
    
    return jsonify({
        'success': True,
        'data': products
    })


# =============================================================================
# Alerts & Statistics
# =============================================================================

@inventory_api.route('/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts() -> Response:
    """Get products with low stock."""
    alerts = [
        p for p in MOCK_PRODUCTS 
        if p['status'] in ['low_stock', 'out_of_stock']
    ]
    
    return jsonify({
        'success': True,
        'data': alerts
    })


@inventory_api.route('/stats', methods=['GET'])
def get_stats() -> Response:
    """Get inventory statistics."""
    total_products = len(MOCK_PRODUCTS)
    total_value = sum(p['stock'] * p['price'] for p in MOCK_PRODUCTS)
    low_stock = len([p for p in MOCK_PRODUCTS if p['status'] == 'low_stock'])
    out_of_stock = len([p for p in MOCK_PRODUCTS if p['status'] == 'out_of_stock'])
    
    return jsonify({
        'success': True,
        'data': {
            'total_products': total_products,
            'total_value': total_value,
            'low_stock_count': low_stock,
            'out_of_stock_count': out_of_stock,
            'categories_count': len(MOCK_CATEGORIES),
            'warehouses_count': len(MOCK_WAREHOUSES)
        }
    })


@inventory_api.route('/export', methods=['GET'])
def export_data() -> Response:
    """Export inventory data."""
    format_type = request.args.get('format', 'json')
    
    if format_type == 'json':
        return jsonify({
            'success': True,
            'data': {
                'products': MOCK_PRODUCTS,
                'categories': MOCK_CATEGORIES,
                'warehouses': MOCK_WAREHOUSES
            }
        })
    
    return jsonify({
        'success': True,
        'message': f'Export to {format_type} not implemented yet',
        'message_ar': f'التصدير إلى {format_type} غير متاح حالياً'
    })
