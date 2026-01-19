"""
Purchasing API Routes - مسارات API المشتريات
Gaara ERP v12

API endpoints for purchasing and supplier management.

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
purchasing_api = Blueprint('purchasing_api', __name__, url_prefix='/api/purchasing')


# =============================================================================
# Mock Data
# =============================================================================

MOCK_ORDERS = [
    {
        'id': 'PO-001',
        'supplier': 'مؤسسة البذور الذهبية',
        'supplier_id': 'S001',
        'date': '2026-01-17',
        'items': 5,
        'items_list': [],
        'total': 45000,
        'status': 'received',
        'payment_status': 'paid',
        'expected_date': '2026-01-20',
        'payment_terms': 'net30',
        'notes': '',
        'created_at': '2026-01-17T10:00:00Z'
    },
    {
        'id': 'PO-002',
        'supplier': 'شركة الأسمدة المتحدة',
        'supplier_id': 'S002',
        'date': '2026-01-16',
        'items': 3,
        'items_list': [],
        'total': 28000,
        'status': 'shipped',
        'payment_status': 'pending',
        'expected_date': '2026-01-22',
        'payment_terms': 'net30',
        'notes': '',
        'created_at': '2026-01-16T14:30:00Z'
    },
]

MOCK_SUPPLIERS = [
    {
        'id': 'S001',
        'name': 'مؤسسة البذور الذهبية',
        'email': 'info@goldenseeds.sa',
        'phone': '0501234567',
        'city': 'الرياض',
        'address': '',
        'tax_number': '',
        'payment_terms': 'net30',
        'orders': 25,
        'total': 450000,
        'status': 'active',
        'created_at': '2023-06-01T00:00:00Z'
    },
    {
        'id': 'S002',
        'name': 'شركة الأسمدة المتحدة',
        'email': 'sales@unifert.com',
        'phone': '0559876543',
        'city': 'جدة',
        'address': '',
        'tax_number': '',
        'payment_terms': 'net30',
        'orders': 18,
        'total': 320000,
        'status': 'active',
        'created_at': '2024-01-15T00:00:00Z'
    },
]


# =============================================================================
# Purchase Order Endpoints
# =============================================================================

@purchasing_api.route('/orders', methods=['GET'])
def get_orders() -> Response:
    """Get all purchase orders."""
    status = request.args.get('status')
    search = request.args.get('search', '').lower()
    
    orders = MOCK_ORDERS.copy()
    
    if status:
        orders = [o for o in orders if o['status'] == status]
    
    if search:
        orders = [o for o in orders if search in o['id'].lower() or search in o['supplier'].lower()]
    
    return jsonify({
        'success': True,
        'data': orders
    })


@purchasing_api.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id: str) -> Response:
    """Get single purchase order."""
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    
    if not order:
        return jsonify({'success': False, 'message': 'Order not found', 'message_ar': 'الأمر غير موجود'}), 404
    
    return jsonify({'success': True, 'data': order})


@purchasing_api.route('/orders', methods=['POST'])
def create_order() -> Response:
    """Create purchase order."""
    data = request.get_json()
    
    new_id = f"PO-{len(MOCK_ORDERS) + 1:03d}"
    
    new_order = {
        'id': new_id,
        'supplier': data.get('supplier_name', ''),
        'supplier_id': data.get('supplier_id', ''),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'items': len(data.get('items', [])),
        'items_list': data.get('items', []),
        'total': sum(i.get('quantity', 0) * i.get('unit_price', 0) for i in data.get('items', [])),
        'status': 'draft',
        'payment_status': 'pending',
        'expected_date': data.get('expected_date', ''),
        'payment_terms': data.get('payment_terms', 'net30'),
        'notes': data.get('notes', ''),
        'created_at': datetime.now().isoformat()
    }
    
    MOCK_ORDERS.append(new_order)
    
    return jsonify({
        'success': True,
        'data': new_order,
        'message': 'Order created',
        'message_ar': 'تم إنشاء أمر الشراء'
    }), 201


@purchasing_api.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id: str) -> Response:
    """Update purchase order."""
    data = request.get_json()
    
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    if not order:
        return jsonify({'success': False, 'message_ar': 'الأمر غير موجود'}), 404
    
    for key, value in data.items():
        if key in order and key not in ['id', 'created_at']:
            order[key] = value
    
    return jsonify({'success': True, 'data': order, 'message_ar': 'تم تحديث الأمر'})


@purchasing_api.route('/orders/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id: str) -> Response:
    """Cancel purchase order."""
    data = request.get_json()
    
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    if not order:
        return jsonify({'success': False, 'message_ar': 'الأمر غير موجود'}), 404
    
    order['status'] = 'cancelled'
    order['cancel_reason'] = data.get('reason', '')
    
    return jsonify({'success': True, 'data': order, 'message_ar': 'تم إلغاء الأمر'})


@purchasing_api.route('/orders/<order_id>/approve', methods=['POST'])
def approve_order(order_id: str) -> Response:
    """Approve purchase order."""
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    if not order:
        return jsonify({'success': False, 'message_ar': 'الأمر غير موجود'}), 404
    
    order['status'] = 'approved'
    order['approved_at'] = datetime.now().isoformat()
    
    return jsonify({'success': True, 'data': order, 'message_ar': 'تم اعتماد الأمر'})


@purchasing_api.route('/orders/<order_id>/receive', methods=['POST'])
def receive_order(order_id: str) -> Response:
    """Mark order as received."""
    data = request.get_json()
    
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    if not order:
        return jsonify({'success': False, 'message_ar': 'الأمر غير موجود'}), 404
    
    order['status'] = 'received'
    order['received_at'] = data.get('received_date', datetime.now().isoformat())
    
    return jsonify({'success': True, 'data': order, 'message_ar': 'تم استلام الطلب'})


# =============================================================================
# Supplier Endpoints
# =============================================================================

@purchasing_api.route('/suppliers', methods=['GET'])
def get_suppliers() -> Response:
    """Get all suppliers."""
    search = request.args.get('search', '').lower()
    
    suppliers = MOCK_SUPPLIERS.copy()
    
    if search:
        suppliers = [s for s in suppliers if search in s['name'].lower() or search in s.get('email', '').lower()]
    
    return jsonify({'success': True, 'data': suppliers})


@purchasing_api.route('/suppliers/<supplier_id>', methods=['GET'])
def get_supplier(supplier_id: str) -> Response:
    """Get single supplier."""
    supplier = next((s for s in MOCK_SUPPLIERS if s['id'] == supplier_id), None)
    
    if not supplier:
        return jsonify({'success': False, 'message_ar': 'المورد غير موجود'}), 404
    
    return jsonify({'success': True, 'data': supplier})


@purchasing_api.route('/suppliers', methods=['POST'])
def create_supplier() -> Response:
    """Create supplier."""
    data = request.get_json()
    
    new_id = f"S{len(MOCK_SUPPLIERS) + 1:03d}"
    
    new_supplier = {
        'id': new_id,
        'name': data.get('name', ''),
        'email': data.get('email', ''),
        'phone': data.get('phone', ''),
        'city': data.get('city', ''),
        'address': data.get('address', ''),
        'tax_number': data.get('tax_number', ''),
        'payment_terms': data.get('payment_terms', 'net30'),
        'orders': 0,
        'total': 0,
        'status': 'active' if data.get('is_active', True) else 'inactive',
        'created_at': datetime.now().isoformat()
    }
    
    MOCK_SUPPLIERS.append(new_supplier)
    
    return jsonify({
        'success': True,
        'data': new_supplier,
        'message_ar': 'تم إضافة المورد'
    }), 201


@purchasing_api.route('/suppliers/<supplier_id>', methods=['PUT'])
def update_supplier(supplier_id: str) -> Response:
    """Update supplier."""
    data = request.get_json()
    
    supplier = next((s for s in MOCK_SUPPLIERS if s['id'] == supplier_id), None)
    if not supplier:
        return jsonify({'success': False, 'message_ar': 'المورد غير موجود'}), 404
    
    for key, value in data.items():
        if key in supplier and key not in ['id', 'created_at']:
            supplier[key] = value
    
    if 'is_active' in data:
        supplier['status'] = 'active' if data['is_active'] else 'inactive'
    
    return jsonify({'success': True, 'data': supplier, 'message_ar': 'تم تحديث المورد'})


@purchasing_api.route('/suppliers/<supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id: str) -> Response:
    """Delete supplier."""
    global MOCK_SUPPLIERS
    
    supplier = next((s for s in MOCK_SUPPLIERS if s['id'] == supplier_id), None)
    if not supplier:
        return jsonify({'success': False, 'message_ar': 'المورد غير موجود'}), 404
    
    MOCK_SUPPLIERS = [s for s in MOCK_SUPPLIERS if s['id'] != supplier_id]
    
    return jsonify({'success': True, 'message_ar': 'تم حذف المورد'})


@purchasing_api.route('/suppliers/<supplier_id>/products', methods=['GET'])
def get_supplier_products(supplier_id: str) -> Response:
    """Get supplier products."""
    return jsonify({'success': True, 'data': []})


@purchasing_api.route('/stats', methods=['GET'])
def get_stats() -> Response:
    """Get purchasing statistics."""
    total = sum(o['total'] for o in MOCK_ORDERS if o['status'] != 'cancelled')
    pending = len([o for o in MOCK_ORDERS if o['status'] == 'pending'])
    in_transit = len([o for o in MOCK_ORDERS if o['status'] == 'shipped'])
    active_suppliers = len([s for s in MOCK_SUPPLIERS if s['status'] == 'active'])
    
    return jsonify({
        'success': True,
        'data': {
            'total_purchases': total,
            'pending_orders': pending,
            'in_transit': in_transit,
            'active_suppliers': active_suppliers
        }
    })
