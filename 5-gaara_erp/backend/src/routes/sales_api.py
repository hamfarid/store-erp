"""
Sales API Routes - مسارات API المبيعات
Gaara ERP v12

API endpoints for sales order management.

Author: Global v35.0 Singularity
Version: 1.0.0
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from flask import Blueprint, g, jsonify, request

if TYPE_CHECKING:
    from flask import Response

# Create Blueprint
sales_api = Blueprint('sales_api', __name__, url_prefix='/api/sales')


# =============================================================================
# Helper Functions
# =============================================================================

def get_tenant_id() -> str | None:
    """Get current tenant ID from request context."""
    return getattr(g, 'tenant_id', None)


def paginate_query(items: list, page: int = 1, per_page: int = 10) -> dict:
    """Paginate a list of items."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }


# =============================================================================
# Mock Data (Replace with DB queries)
# =============================================================================

MOCK_ORDERS = [
    {
        'id': 'SO-001',
        'customer': 'شركة التقنية',
        'customer_id': 'C001',
        'date': '2026-01-17',
        'items': 5,
        'items_list': [],
        'total': 15000,
        'status': 'completed',
        'payment': 'paid',
        'payment_method': 'cash',
        'notes': '',
        'created_at': '2026-01-17T10:00:00Z'
    },
    {
        'id': 'SO-002',
        'customer': 'مؤسسة الزراعة',
        'customer_id': 'C002',
        'date': '2026-01-16',
        'items': 3,
        'items_list': [],
        'total': 8500,
        'status': 'pending',
        'payment': 'pending',
        'payment_method': 'credit',
        'notes': '',
        'created_at': '2026-01-16T14:30:00Z'
    },
]


# =============================================================================
# Sales Order Endpoints
# =============================================================================

@sales_api.route('/orders', methods=['GET'])
def get_orders() -> Response:
    """
    Get all sales orders with optional filtering.
    
    Query params:
        - status: Filter by status
        - search: Search in order ID or customer name
        - page: Page number
        - per_page: Items per page
    """
    # Get query parameters
    status = request.args.get('status')
    search = request.args.get('search', '').lower()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Filter orders
    orders = MOCK_ORDERS.copy()
    
    if status:
        orders = [o for o in orders if o['status'] == status]
    
    if search:
        orders = [
            o for o in orders 
            if search in o['id'].lower() or search in o['customer'].lower()
        ]
    
    # Paginate
    result = paginate_query(orders, page, per_page)
    
    return jsonify({
        'success': True,
        'data': result['items'],
        'pagination': {
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'pages': result['pages']
        }
    })


@sales_api.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id: str) -> Response:
    """Get a single sales order by ID."""
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'Order not found',
            'message_ar': 'الطلب غير موجود'
        }), 404
    
    return jsonify({
        'success': True,
        'data': order
    })


@sales_api.route('/orders', methods=['POST'])
def create_order() -> Response:
    """Create a new sales order."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['customer_name', 'items']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}',
                'message_ar': f'الحقل مطلوب: {field}'
            }), 400
    
    # Generate order ID
    new_id = f"SO-{len(MOCK_ORDERS) + 1:03d}"
    
    # Calculate total
    items_list = data.get('items', [])
    total = sum(
        item.get('quantity', 0) * item.get('unit_price', 0) 
        for item in items_list
    )
    
    # Apply discount
    discount = data.get('discount', 0)
    total = total - discount
    
    # Apply tax
    tax_rate = data.get('tax_rate', 15)
    total = total * (1 + tax_rate / 100)
    
    new_order = {
        'id': new_id,
        'customer': data.get('customer_name'),
        'customer_id': data.get('customer_id', ''),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'items': len(items_list),
        'items_list': items_list,
        'total': round(total, 2),
        'status': 'pending',
        'payment': 'pending',
        'payment_method': data.get('payment_method', 'cash'),
        'notes': data.get('notes', ''),
        'discount': discount,
        'tax_rate': tax_rate,
        'created_at': datetime.now().isoformat()
    }
    
    MOCK_ORDERS.append(new_order)
    
    return jsonify({
        'success': True,
        'data': new_order,
        'message': 'Order created successfully',
        'message_ar': 'تم إنشاء الطلب بنجاح'
    }), 201


@sales_api.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id: str) -> Response:
    """Update a sales order."""
    data = request.get_json()
    
    order_index = next(
        (i for i, o in enumerate(MOCK_ORDERS) if o['id'] == order_id), 
        None
    )
    
    if order_index is None:
        return jsonify({
            'success': False,
            'message': 'Order not found',
            'message_ar': 'الطلب غير موجود'
        }), 404
    
    # Update fields
    order = MOCK_ORDERS[order_index]
    for key, value in data.items():
        if key in order and key not in ['id', 'created_at']:
            order[key] = value
    
    order['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'data': order,
        'message': 'Order updated successfully',
        'message_ar': 'تم تحديث الطلب بنجاح'
    })


@sales_api.route('/orders/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id: str) -> Response:
    """Cancel a sales order."""
    data = request.get_json()
    reason = data.get('reason', '')
    
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'Order not found',
            'message_ar': 'الطلب غير موجود'
        }), 404
    
    if order['status'] == 'completed':
        return jsonify({
            'success': False,
            'message': 'Cannot cancel completed order',
            'message_ar': 'لا يمكن إلغاء طلب مكتمل'
        }), 400
    
    order['status'] = 'cancelled'
    order['cancel_reason'] = reason
    order['cancelled_at'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'data': order,
        'message': 'Order cancelled',
        'message_ar': 'تم إلغاء الطلب'
    })


@sales_api.route('/orders/<order_id>/status', methods=['PATCH'])
def update_order_status(order_id: str) -> Response:
    """Update order status."""
    data = request.get_json()
    new_status = data.get('status')
    
    valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({
            'success': False,
            'message': f'Invalid status. Must be one of: {valid_statuses}',
            'message_ar': 'حالة غير صالحة'
        }), 400
    
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'Order not found',
            'message_ar': 'الطلب غير موجود'
        }), 404
    
    order['status'] = new_status
    order['status_updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'data': order,
        'message': 'Status updated',
        'message_ar': 'تم تحديث الحالة'
    })


@sales_api.route('/orders/<order_id>/invoice', methods=['POST'])
def generate_invoice(order_id: str) -> Response:
    """Generate invoice for an order."""
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'Order not found',
            'message_ar': 'الطلب غير موجود'
        }), 404
    
    invoice = {
        'id': f"INV-{order_id}",
        'order_id': order_id,
        'customer': order['customer'],
        'total': order['total'],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'due_date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'generated'
    }
    
    return jsonify({
        'success': True,
        'data': invoice,
        'message': 'Invoice generated',
        'message_ar': 'تم إنشاء الفاتورة'
    })


@sales_api.route('/orders/<order_id>/payments', methods=['POST'])
def add_payment(order_id: str) -> Response:
    """Add payment to an order."""
    data = request.get_json()
    
    order = next((o for o in MOCK_ORDERS if o['id'] == order_id), None)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'Order not found',
            'message_ar': 'الطلب غير موجود'
        }), 404
    
    payment = {
        'id': f"PAY-{order_id}-{datetime.now().strftime('%H%M%S')}",
        'order_id': order_id,
        'amount': data.get('amount', 0),
        'method': data.get('method', 'cash'),
        'date': datetime.now().isoformat(),
        'reference': data.get('reference', '')
    }
    
    # Update order payment status
    if payment['amount'] >= order['total']:
        order['payment'] = 'paid'
    else:
        order['payment'] = 'partial'
    
    return jsonify({
        'success': True,
        'data': payment,
        'message': 'Payment recorded',
        'message_ar': 'تم تسجيل الدفعة'
    })


@sales_api.route('/stats', methods=['GET'])
def get_stats() -> Response:
    """Get sales statistics."""
    total_sales = sum(o['total'] for o in MOCK_ORDERS if o['status'] != 'cancelled')
    orders_count = len([o for o in MOCK_ORDERS if o['status'] != 'cancelled'])
    pending_count = len([o for o in MOCK_ORDERS if o['status'] == 'pending'])
    
    return jsonify({
        'success': True,
        'data': {
            'total_sales': total_sales,
            'orders_count': orders_count,
            'pending_orders': pending_count,
            'avg_order_value': total_sales / orders_count if orders_count > 0 else 0,
            'completed_orders': len([o for o in MOCK_ORDERS if o['status'] == 'completed']),
            'cancelled_orders': len([o for o in MOCK_ORDERS if o['status'] == 'cancelled'])
        }
    })


@sales_api.route('/export', methods=['GET'])
def export_data() -> Response:
    """Export sales data."""
    format_type = request.args.get('format', 'json')
    
    if format_type == 'json':
        return jsonify({
            'success': True,
            'data': MOCK_ORDERS
        })
    
    # For other formats, return placeholder
    return jsonify({
        'success': True,
        'message': f'Export to {format_type} not implemented yet',
        'message_ar': f'التصدير إلى {format_type} غير متاح حالياً'
    })
