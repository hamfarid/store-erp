"""
APIs لنظام اللوطات المتقدم
Created: 2025-12-13
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, date
from sqlalchemy import and_, or_, desc
from models.lot_advanced import LotAdvanced
from models.product import Product
from database import db

batches_bp = Blueprint('batches_advanced', __name__)


@batches_bp.route('/api/batches', methods=['GET'])
def get_batches():
    """الحصول على قائمة اللوطات مع فلاتر"""
    try:
        # Filters
        product_id = request.args.get('product_id', type=int)
        warehouse_id = request.args.get('warehouse_id', type=int)
        supplier_id = request.args.get('supplier_id', type=int)
        status = request.args.get('status')
        quality_status = request.args.get('quality_status')
        search = request.args.get('search')
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Query
        query = LotAdvanced.query
        
        if product_id:
            query = query.filter_by(product_id=product_id)
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)
        if supplier_id:
            query = query.filter_by(supplier_id=supplier_id)
        if status:
            query = query.filter_by(status=status)
        if quality_status:
            query = query.filter_by(quality_status=quality_status)
        if search:
            query = query.filter(
                or_(
                    LotAdvanced.batch_number.like(f'%{search}%'),
                    LotAdvanced.internal_batch_number.like(f'%{search}%'),
                    LotAdvanced.supplier_batch_number.like(f'%{search}%'),
                    LotAdvanced.ministry_batch_number.like(f'%{search}%')
                )
            )
        
        # Order by
        query = query.order_by(desc(LotAdvanced.created_at))
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': [batch.to_dict() for batch in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/<int:batch_id>', methods=['GET'])
def get_batch(batch_id):
    """الحصول على تفاصيل لوط"""
    try:
        batch = LotAdvanced.query.get_or_404(batch_id)
        return jsonify({
            'success': True,
            'data': batch.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@batches_bp.route('/api/batches', methods=['POST'])
def create_batch():
    """إنشاء لوط جديد"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['batch_number', 'product_id', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Check if batch_number exists
        existing = LotAdvanced.query.filter_by(batch_number=data['batch_number']).first()
        if existing:
            return jsonify({'success': False, 'error': 'Batch number already exists'}), 400
        
        # Parse dates
        manufacture_date = None
        if data.get('manufacture_date'):
            try:
                manufacture_date = datetime.fromisoformat(data['manufacture_date'].replace('Z', '+00:00')).date()
            except:
                manufacture_date = datetime.strptime(data['manufacture_date'], '%Y-%m-%d').date()
        
        expiry_date = None
        if data.get('expiry_date'):
            try:
                expiry_date = datetime.fromisoformat(data['expiry_date'].replace('Z', '+00:00')).date()
            except:
                expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
        
        received_date = None
        if data.get('received_date'):
            try:
                received_date = datetime.fromisoformat(data['received_date'].replace('Z', '+00:00')).date()
            except:
                received_date = datetime.strptime(data['received_date'], '%Y-%m-%d').date()
        else:
            received_date = date.today()
        
        # Create batch
        batch = LotAdvanced(
            batch_number=data['batch_number'],
            internal_batch_number=data.get('internal_batch_number'),
            supplier_batch_number=data.get('supplier_batch_number'),
            ministry_batch_number=data.get('ministry_batch_number'),
            product_id=data['product_id'],
            warehouse_id=data.get('warehouse_id'),
            supplier_id=data.get('supplier_id'),
            quantity=data['quantity'],
            original_quantity=data.get('original_quantity', data['quantity']),
            cost_price=data.get('cost_price'),
            selling_price=data.get('selling_price'),
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            received_date=received_date,
            germination_rate=data.get('germination_rate'),
            purity_percentage=data.get('purity_percentage'),
            moisture_content=data.get('moisture_content'),
            temperature_storage=data.get('temperature_storage'),
            ph_level=data.get('ph_level'),
            nutrient_content=data.get('nutrient_content'),
            storage_location=data.get('storage_location'),
            storage_conditions=data.get('storage_conditions'),
            handling_instructions=data.get('handling_instructions'),
            safety_warnings=data.get('safety_warnings'),
            notes=data.get('notes'),
            tags=data.get('tags'),
            created_by=data.get('created_by')
        )
        
        db.session.add(batch)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Batch created successfully',
            'data': batch.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/<int:batch_id>', methods=['PUT'])
def update_batch(batch_id):
    """تحديث لوط"""
    try:
        batch = LotAdvanced.query.get_or_404(batch_id)
        data = request.get_json()
        
        # Update simple fields
        simple_fields = [
            'internal_batch_number', 'supplier_batch_number', 'ministry_batch_number',
            'warehouse_id', 'supplier_id', 'quantity', 'cost_price', 'selling_price',
            'germination_rate', 'purity_percentage', 'moisture_content', 
            'temperature_storage', 'ph_level', 'nutrient_content',
            'status', 'quality_status', 'storage_location', 'storage_conditions',
            'handling_instructions', 'safety_warnings', 'notes', 'tags'
        ]
        
        for field in simple_fields:
            if field in data:
                setattr(batch, field, data[field])
        
        # Update date fields
        date_fields = ['manufacture_date', 'expiry_date', 'received_date']
        for field in date_fields:
            if field in data and data[field]:
                try:
                    date_value = datetime.fromisoformat(data[field].replace('Z', '+00:00')).date()
                except:
                    date_value = datetime.strptime(data[field], '%Y-%m-%d').date()
                setattr(batch, field, date_value)
        
        batch.updated_by = data.get('updated_by')
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Batch updated successfully',
            'data': batch.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/<int:batch_id>', methods=['DELETE'])
def delete_batch(batch_id):
    """حذف لوط"""
    try:
        batch = LotAdvanced.query.get_or_404(batch_id)
        
        # Check if batch has quantity
        if batch.quantity > 0:
            return jsonify({
                'success': False,
                'error': 'Cannot delete batch with remaining quantity'
            }), 400
        
        db.session.delete(batch)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Batch deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/<int:batch_id>/quality-test', methods=['POST'])
def quality_test(batch_id):
    """إجراء فحص الجودة"""
    try:
        batch = LotAdvanced.query.get_or_404(batch_id)
        data = request.get_json()
        
        batch.quality_status = data.get('quality_status', 'approved')
        batch.quality_test_date = date.today()
        batch.quality_test_by = data.get('quality_test_by')
        batch.quality_notes = data.get('quality_notes')
        batch.quality_certificate_number = data.get('quality_certificate_number')
        batch.quality_certificate_url = data.get('quality_certificate_url')
        
        # Update quality parameters if provided
        if 'germination_rate' in data:
            batch.germination_rate = data['germination_rate']
        if 'purity_percentage' in data:
            batch.purity_percentage = data['purity_percentage']
        if 'moisture_content' in data:
            batch.moisture_content = data['moisture_content']
        if 'ph_level' in data:
            batch.ph_level = data['ph_level']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Quality test completed',
            'data': batch.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/<int:batch_id>/ministry-approval', methods=['POST'])
def ministry_approval(batch_id):
    """موافقة الوزارة"""
    try:
        batch = LotAdvanced.query.get_or_404(batch_id)
        data = request.get_json()
        
        batch.ministry_approval_date = date.today()
        batch.ministry_approval_number = data.get('ministry_approval_number')
        batch.ministry_inspector = data.get('ministry_inspector')
        batch.ministry_notes = data.get('ministry_notes')
        batch.ministry_certificate_url = data.get('ministry_certificate_url')
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ministry approval recorded',
            'data': batch.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/expiring-soon', methods=['GET'])
def expiring_soon():
    """لوطات قريبة من انتهاء الصلاحية"""
    try:
        days = request.args.get('days', 30, type=int)
        threshold_date = date.today() + timedelta(days=days)
        
        batches = LotAdvanced.query.filter(
            and_(
                LotAdvanced.expiry_date <= threshold_date,
                LotAdvanced.expiry_date >= date.today(),
                LotAdvanced.status == 'active'
            )
        ).order_by(LotAdvanced.expiry_date.asc()).all()
        
        return jsonify({
            'success': True,
            'data': [batch.to_dict() for batch in batches],
            'count': len(batches)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/low-stock', methods=['GET'])
def low_stock():
    """لوطات منخفضة المخزون"""
    try:
        threshold = request.args.get('threshold', 10, type=int)
        
        batches = LotAdvanced.query.filter(
            and_(
                LotAdvanced.quantity <= threshold,
                LotAdvanced.quantity > 0,
                LotAdvanced.status == 'active'
            )
        ).order_by(LotAdvanced.quantity.asc()).all()
        
        return jsonify({
            'success': True,
            'data': [batch.to_dict() for batch in batches],
            'count': len(batches)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/by-product/<int:product_id>', methods=['GET'])
def get_batches_by_product(product_id):
    """الحصول على لوطات منتج معين (مرتبة حسب FIFO)"""
    try:
        # Get only available batches
        batches = LotAdvanced.query.filter(
            and_(
                LotAdvanced.product_id == product_id,
                LotAdvanced.status == 'active',
                LotAdvanced.quality_status == 'approved',
                LotAdvanced.quantity > 0
            )
        ).order_by(LotAdvanced.received_date.asc()).all()
        
        return jsonify({
            'success': True,
            'data': [batch.to_dict() for batch in batches],
            'count': len(batches)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@batches_bp.route('/api/batches/statistics', methods=['GET'])
def get_statistics():
    """إحصائيات اللوطات"""
    try:
        total_batches = LotAdvanced.query.count()
        active_batches = LotAdvanced.query.filter_by(status='active').count()
        expired_batches = LotAdvanced.query.filter_by(status='expired').count()
        quarantine_batches = LotAdvanced.query.filter_by(status='quarantine').count()
        
        # Batches expiring in 30 days
        threshold_date = date.today() + timedelta(days=30)
        expiring_soon = LotAdvanced.query.filter(
            and_(
                LotAdvanced.expiry_date <= threshold_date,
                LotAdvanced.expiry_date >= date.today(),
                LotAdvanced.status == 'active'
            )
        ).count()
        
        # Low stock batches
        low_stock = LotAdvanced.query.filter(
            and_(
                LotAdvanced.quantity <= 10,
                LotAdvanced.quantity > 0,
                LotAdvanced.status == 'active'
            )
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_batches': total_batches,
                'active_batches': active_batches,
                'expired_batches': expired_batches,
                'quarantine_batches': quarantine_batches,
                'expiring_soon': expiring_soon,
                'low_stock': low_stock
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
