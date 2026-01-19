"""
Customers API Routes - مسارات API العملاء
Gaara ERP v12

API endpoints for customer and contact management.

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
customers_api = Blueprint('customers_api', __name__, url_prefix='/api/customers')


# =============================================================================
# Mock Data
# =============================================================================

MOCK_CUSTOMERS = [
    {
        'id': 'C001',
        'name': 'شركة الزراعة الحديثة',
        'type': 'customer',
        'category': 'company',
        'email': 'info@modernagri.com',
        'phone': '+966-50-123-4567',
        'city': 'الرياض',
        'address': '',
        'tax_number': '',
        'credit_limit': 100000,
        'payment_terms': 'net30',
        'status': 'active',
        'rating': 5,
        'total_orders': 25,
        'total_amount': 450000,
        'balance': 15000,
        'last_order': '2026-01-15',
        'created_at': '2024-01-01T00:00:00Z'
    },
    {
        'id': 'C002',
        'name': 'أحمد محمد العلي',
        'type': 'customer',
        'category': 'individual',
        'email': 'ahmed@example.com',
        'phone': '+966-55-987-6543',
        'city': 'جدة',
        'address': '',
        'tax_number': '',
        'credit_limit': 50000,
        'payment_terms': 'cash',
        'status': 'active',
        'rating': 4,
        'total_orders': 8,
        'total_amount': 75000,
        'balance': 0,
        'last_order': '2026-01-10',
        'created_at': '2024-03-15T00:00:00Z'
    },
    {
        'id': 'S001',
        'name': 'مؤسسة البذور الذهبية',
        'type': 'supplier',
        'category': 'company',
        'email': 'contact@goldenseeds.sa',
        'phone': '+966-12-345-6789',
        'city': 'الدمام',
        'address': '',
        'tax_number': '',
        'credit_limit': 0,
        'payment_terms': 'net30',
        'status': 'active',
        'rating': 5,
        'total_orders': 42,
        'total_amount': 890000,
        'balance': -25000,
        'last_order': '2026-01-17',
        'created_at': '2023-06-01T00:00:00Z'
    },
]


# =============================================================================
# Customer Endpoints
# =============================================================================

@customers_api.route('', methods=['GET'])
def get_customers() -> Response:
    """Get all customers/contacts."""
    contact_type = request.args.get('type')
    status = request.args.get('status')
    search = request.args.get('search', '').lower()
    
    customers = MOCK_CUSTOMERS.copy()
    
    if contact_type:
        customers = [c for c in customers if c['type'] == contact_type or c['type'] == 'both']
    
    if status:
        customers = [c for c in customers if c['status'] == status]
    
    if search:
        customers = [c for c in customers if 
                    search in c['name'].lower() or 
                    search in c.get('email', '').lower() or
                    search in c.get('phone', '')]
    
    return jsonify({'success': True, 'data': customers})


@customers_api.route('/<customer_id>', methods=['GET'])
def get_customer(customer_id: str) -> Response:
    """Get single customer."""
    customer = next((c for c in MOCK_CUSTOMERS if c['id'] == customer_id), None)
    
    if not customer:
        return jsonify({'success': False, 'message_ar': 'جهة الاتصال غير موجودة'}), 404
    
    return jsonify({'success': True, 'data': customer})


@customers_api.route('', methods=['POST'])
def create_customer() -> Response:
    """Create customer."""
    data = request.get_json()
    
    prefix = 'C' if data.get('type') != 'supplier' else 'S'
    count = len([c for c in MOCK_CUSTOMERS if c['id'].startswith(prefix)])
    new_id = f"{prefix}{count + 1:03d}"
    
    new_customer = {
        'id': new_id,
        'name': data.get('name', ''),
        'type': data.get('type', 'customer'),
        'category': data.get('category', 'individual'),
        'email': data.get('email', ''),
        'phone': data.get('phone', ''),
        'city': data.get('city', ''),
        'address': data.get('address', ''),
        'tax_number': data.get('tax_number', ''),
        'credit_limit': data.get('credit_limit', 0),
        'payment_terms': data.get('payment_terms', 'net30'),
        'status': 'active' if data.get('is_active', True) else 'inactive',
        'rating': 0,
        'total_orders': 0,
        'total_amount': 0,
        'balance': 0,
        'last_order': None,
        'created_at': datetime.now().isoformat()
    }
    
    MOCK_CUSTOMERS.append(new_customer)
    
    return jsonify({
        'success': True,
        'data': new_customer,
        'message_ar': 'تم إضافة جهة الاتصال'
    }), 201


@customers_api.route('/<customer_id>', methods=['PUT'])
def update_customer(customer_id: str) -> Response:
    """Update customer."""
    data = request.get_json()
    
    customer = next((c for c in MOCK_CUSTOMERS if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'success': False, 'message_ar': 'جهة الاتصال غير موجودة'}), 404
    
    for key, value in data.items():
        if key in customer and key not in ['id', 'created_at']:
            customer[key] = value
    
    if 'is_active' in data:
        customer['status'] = 'active' if data['is_active'] else 'inactive'
    
    return jsonify({'success': True, 'data': customer, 'message_ar': 'تم تحديث جهة الاتصال'})


@customers_api.route('/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id: str) -> Response:
    """Delete customer."""
    global MOCK_CUSTOMERS
    
    customer = next((c for c in MOCK_CUSTOMERS if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'success': False, 'message_ar': 'جهة الاتصال غير موجودة'}), 404
    
    MOCK_CUSTOMERS = [c for c in MOCK_CUSTOMERS if c['id'] != customer_id]
    
    return jsonify({'success': True, 'message_ar': 'تم حذف جهة الاتصال'})


@customers_api.route('/<customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id: str) -> Response:
    """Get customer orders."""
    return jsonify({'success': True, 'data': []})


@customers_api.route('/<customer_id>/invoices', methods=['GET'])
def get_customer_invoices(customer_id: str) -> Response:
    """Get customer invoices."""
    return jsonify({'success': True, 'data': []})


@customers_api.route('/<customer_id>/balance', methods=['GET'])
def get_customer_balance(customer_id: str) -> Response:
    """Get customer balance."""
    customer = next((c for c in MOCK_CUSTOMERS if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'success': False, 'message_ar': 'جهة الاتصال غير موجودة'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'balance': customer['balance'],
            'credit_limit': customer['credit_limit'],
            'available_credit': customer['credit_limit'] - customer['balance']
        }
    })


@customers_api.route('/<customer_id>/payments', methods=['POST'])
def add_payment(customer_id: str) -> Response:
    """Add customer payment."""
    data = request.get_json()
    
    customer = next((c for c in MOCK_CUSTOMERS if c['id'] == customer_id), None)
    if not customer:
        return jsonify({'success': False, 'message_ar': 'جهة الاتصال غير موجودة'}), 404
    
    payment = {
        'id': f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'customer_id': customer_id,
        'amount': data.get('amount', 0),
        'method': data.get('method', 'cash'),
        'date': datetime.now().isoformat()
    }
    
    customer['balance'] -= payment['amount']
    
    return jsonify({'success': True, 'data': payment, 'message_ar': 'تم تسجيل الدفعة'})


@customers_api.route('/<customer_id>/contacts', methods=['GET'])
def get_contacts(customer_id: str) -> Response:
    """Get customer contacts."""
    return jsonify({'success': True, 'data': []})


@customers_api.route('/<customer_id>/contacts', methods=['POST'])
def add_contact(customer_id: str) -> Response:
    """Add customer contact."""
    data = request.get_json()
    return jsonify({'success': True, 'data': data, 'message_ar': 'تم إضافة جهة الاتصال'})


@customers_api.route('/<customer_id>/addresses', methods=['GET'])
def get_addresses(customer_id: str) -> Response:
    """Get customer addresses."""
    return jsonify({'success': True, 'data': []})


@customers_api.route('/<customer_id>/addresses', methods=['POST'])
def add_address(customer_id: str) -> Response:
    """Add customer address."""
    data = request.get_json()
    return jsonify({'success': True, 'data': data, 'message_ar': 'تم إضافة العنوان'})


@customers_api.route('/stats', methods=['GET'])
def get_stats() -> Response:
    """Get customer statistics."""
    total = len(MOCK_CUSTOMERS)
    customers = len([c for c in MOCK_CUSTOMERS if c['type'] == 'customer' or c['type'] == 'both'])
    suppliers = len([c for c in MOCK_CUSTOMERS if c['type'] == 'supplier' or c['type'] == 'both'])
    active = len([c for c in MOCK_CUSTOMERS if c['status'] == 'active'])
    
    return jsonify({
        'success': True,
        'data': {
            'total': total,
            'customers': customers,
            'suppliers': suppliers,
            'active': active
        }
    })


@customers_api.route('/search', methods=['GET'])
def search_customers() -> Response:
    """Search customers."""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'success': True, 'data': []})
    
    results = [c for c in MOCK_CUSTOMERS if query in c['name'].lower()]
    
    return jsonify({'success': True, 'data': results[:10]})


@customers_api.route('/export', methods=['GET'])
def export_customers() -> Response:
    """Export customers."""
    return jsonify({'success': True, 'data': MOCK_CUSTOMERS})
