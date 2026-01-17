"""
Purchase Orders Routes
مسارات أوامر الشراء
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, date
from src.database import db
from src.models.purchase_order import PurchaseOrder, POStatus
from src.models.purchase_order_item import PurchaseOrderItem
from src.models.purchase_receipt import PurchaseReceipt
from src.models.lot_advanced import LotAdvanced
from src.decorators.auth_decorators import token_required
from sqlalchemy import func, and_, or_

purchases_bp = Blueprint('purchases', __name__, url_prefix='/api/purchases')


@purchases_bp.route('', methods=['GET'])
@token_required
def get_purchase_orders(current_user):
    """
    الحصول على قائمة أوامر الشراء
    """
    try:
        # الفلاتر
        status = request.args.get('status')
        supplier_id = request.args.get('supplier_id', type=int)
        warehouse_id = request.args.get('warehouse_id', type=int)
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        search = request.args.get('search', '')
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query
        query = PurchaseOrder.query
        
        # تطبيق الفلاتر
        if status:
            query = query.filter(PurchaseOrder.status == status)
        
        if supplier_id:
            query = query.filter(PurchaseOrder.supplier_id == supplier_id)
        
        if warehouse_id:
            query = query.filter(PurchaseOrder.warehouse_id == warehouse_id)
        
        if from_date:
            query = query.filter(PurchaseOrder.order_date >= datetime.fromisoformat(from_date))
        
        if to_date:
            query = query.filter(PurchaseOrder.order_date <= datetime.fromisoformat(to_date))
        
        if search:
            query = query.filter(
                or_(
                    PurchaseOrder.po_number.ilike(f'%{search}%'),
                    PurchaseOrder.notes.ilike(f'%{search}%')
                )
            )
        
        # الترتيب
        query = query.order_by(PurchaseOrder.order_date.desc())
        
        # Pagination
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': [po.to_dict() for po in paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@purchases_bp.route('/<int:po_id>', methods=['GET'])
@token_required
def get_purchase_order(current_user, po_id):
    """
    الحصول على تفاصيل أمر شراء
    """
    try:
        po = PurchaseOrder.query.get_or_404(po_id)
        
        # تضمين العناصر
        po_dict = po.to_dict()
        po_dict['items'] = [item.to_dict() for item in po.items.all()]
        po_dict['receipts'] = [receipt.to_dict() for receipt in po.receipts.all()]
        
        return jsonify({
            'success': True,
            'data': po_dict
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@purchases_bp.route('', methods=['POST'])
@token_required
def create_purchase_order(current_user):
    """
    إنشاء أمر شراء جديد
    """
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        if not data.get('supplier_id'):
            return jsonify({'success': False, 'message': 'معرف المورد مطلوب'}), 400
        
        if not data.get('items') or len(data['items']) == 0:
            return jsonify({'success': False, 'message': 'يجب إضافة عنصر واحد على الأقل'}), 400
        
        # توليد رقم أمر الشراء
        from src.utils.purchase_helper import generate_po_number
        po_number = generate_po_number()
        
        # إنشاء أمر الشراء
        po = PurchaseOrder(
            po_number=po_number,
            supplier_id=data['supplier_id'],
            warehouse_id=data.get('warehouse_id'),
            order_date=datetime.fromisoformat(data['order_date']) if data.get('order_date') else datetime.utcnow(),
            expected_date=datetime.fromisoformat(data['expected_date']) if data.get('expected_date') else None,
            status=data.get('status', POStatus.DRAFT.value),
            notes=data.get('notes'),
            created_by=current_user.id
        )
        
        db.session.add(po)
        db.session.flush()  # للحصول على po.id
        
        # إضافة العناصر
        total_amount = 0
        for item_data in data['items']:
            item = PurchaseOrderItem(
                po_id=po.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                discount_percentage=item_data.get('discount_percentage', 0),
                tax_percentage=item_data.get('tax_percentage', 0),
                notes=item_data.get('notes'),
                expiry_date=datetime.fromisoformat(item_data['expiry_date']).date() if item_data.get('expiry_date') else None,
                manufacture_date=datetime.fromisoformat(item_data['manufacture_date']).date() if item_data.get('manufacture_date') else None
            )
            
            # حساب الإجمالي
            item.calculate_total()
            total_amount += float(item.final_price or 0)
            
            db.session.add(item)
        
        # تحديث الإجمالي
        po.total_amount = total_amount
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء أمر الشراء بنجاح',
            'data': po.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@purchases_bp.route('/<int:po_id>', methods=['PUT'])
@token_required
def update_purchase_order(current_user, po_id):
    """
    تحديث أمر شراء
    """
    try:
        po = PurchaseOrder.query.get_or_404(po_id)
        
        # التحقق من الحالة
        if po.status not in [POStatus.DRAFT.value, POStatus.PENDING.value]:
            return jsonify({'success': False, 'message': 'لا يمكن تعديل أمر شراء معتمد أو مستلم'}), 400
        
        data = request.get_json()
        
        # تحديث البيانات الأساسية
        if 'supplier_id' in data:
            po.supplier_id = data['supplier_id']
        if 'warehouse_id' in data:
            po.warehouse_id = data['warehouse_id']
        if 'expected_date' in data:
            po.expected_date = datetime.fromisoformat(data['expected_date']) if data['expected_date'] else None
        if 'notes' in data:
            po.notes = data['notes']
        if 'status' in data:
            po.status = data['status']
        
        # تحديث العناصر إذا كانت موجودة
        if 'items' in data:
            # حذف العناصر القديمة
            PurchaseOrderItem.query.filter_by(po_id=po.id).delete()
            
            # إضافة العناصر الجديدة
            total_amount = 0
            for item_data in data['items']:
                item = PurchaseOrderItem(
                    po_id=po.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    discount_percentage=item_data.get('discount_percentage', 0),
                    tax_percentage=item_data.get('tax_percentage', 0),
                    notes=item_data.get('notes'),
                    expiry_date=datetime.fromisoformat(item_data['expiry_date']).date() if item_data.get('expiry_date') else None,
                    manufacture_date=datetime.fromisoformat(item_data['manufacture_date']).date() if item_data.get('manufacture_date') else None
                )
                
                item.calculate_total()
                total_amount += float(item.final_price or 0)
                
                db.session.add(item)
            
            po.total_amount = total_amount
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم تحديث أمر الشراء بنجاح',
            'data': po.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@purchases_bp.route('/<int:po_id>/approve', methods=['POST'])
@token_required
def approve_purchase_order(current_user, po_id):
    """
    اعتماد أمر شراء
    """
    try:
        po = PurchaseOrder.query.get_or_404(po_id)
        
        if po.status != POStatus.PENDING.value:
            return jsonify({'success': False, 'message': 'أمر الشراء ليس في حالة معلق'}), 400
        
        po.status = POStatus.APPROVED.value
        po.approved_by = current_user.id
        po.approved_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم اعتماد أمر الشراء بنجاح',
            'data': po.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@purchases_bp.route('/<int:po_id>/receive', methods=['POST'])
@token_required
def receive_purchase_order(current_user, po_id):
    """
    استلام أمر شراء
    """
    try:
        po = PurchaseOrder.query.get_or_404(po_id)
        data = request.get_json()
        
        # التحقق من الحالة
        if po.status not in [POStatus.APPROVED.value, POStatus.ORDERED.value, POStatus.PARTIAL.value]:
            return jsonify({'success': False, 'message': 'أمر الشراء غير جاهز للاستلام'}), 400
        
        # توليد رقم الإيصال
        from src.utils.purchase_helper import generate_receipt_number
        receipt_number = generate_receipt_number()
        
        # إنشاء إيصال الاستلام
        receipt = PurchaseReceipt(
            receipt_number=receipt_number,
            po_id=po.id,
            warehouse_id=data.get('warehouse_id', po.warehouse_id),
            received_by=current_user.id,
            receipt_date=date.today(),
            notes=data.get('notes'),
            delivery_notes=data.get('delivery_notes'),
            driver_name=data.get('driver_name'),
            vehicle_number=data.get('vehicle_number'),
            delivery_company=data.get('delivery_company'),
            created_by=current_user.id
        )
        
        db.session.add(receipt)
        db.session.flush()
        
        # تحديث الكميات المستلمة
        items_received = data.get('items', [])
        for item_data in items_received:
            item = PurchaseOrderItem.query.get(item_data['item_id'])
            if item and item.po_id == po.id:
                received_qty = item_data.get('received_quantity', 0)
                if received_qty > 0:
                    item.update_received(received_qty)
                    
                    # إنشاء لوط جديد إذا كان مطلوباً
                    if item_data.get('create_batch', True):
                        from src.utils.purchase_helper import create_batch_from_receipt
                        batch = create_batch_from_receipt(item, received_qty, data)
                        item.batch_id = batch.id
        
        # إتمام الاستلام
        receipt.complete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم استلام أمر الشراء بنجاح',
            'data': {
                'receipt': receipt.to_dict(),
                'purchase_order': po.to_dict()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@purchases_bp.route('/statistics', methods=['GET'])
@token_required
def get_statistics(current_user):
    """
    إحصائيات أوامر الشراء
    """
    try:
        # إحصائيات حسب الحالة
        status_stats = db.session.query(
            PurchaseOrder.status,
            func.count(PurchaseOrder.id).label('count'),
            func.sum(PurchaseOrder.total_amount).label('total')
        ).group_by(PurchaseOrder.status).all()
        
        # إحصائيات شهرية
        monthly_stats = db.session.query(
            func.strftime('%Y-%m', PurchaseOrder.order_date).label('month'),
            func.count(PurchaseOrder.id).label('count'),
            func.sum(PurchaseOrder.total_amount).label('total')
        ).group_by('month').order_by('month').limit(12).all()
        
        # أوامر الشراء المعلقة
        pending_count = PurchaseOrder.query.filter_by(status=POStatus.PENDING.value).count()
        
        # أوامر الشراء المتأخرة
        overdue_count = PurchaseOrder.query.filter(
            and_(
                PurchaseOrder.expected_date < datetime.utcnow(),
                PurchaseOrder.status.in_([POStatus.APPROVED.value, POStatus.ORDERED.value])
            )
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'by_status': [
                    {
                        'status': stat[0],
                        'count': stat[1],
                        'total': float(stat[2]) if stat[2] else 0
                    }
                    for stat in status_stats
                ],
                'monthly': [
                    {
                        'month': stat[0],
                        'count': stat[1],
                        'total': float(stat[2]) if stat[2] else 0
                    }
                    for stat in monthly_stats
                ],
                'pending_count': pending_count,
                'overdue_count': overdue_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@purchases_bp.route('/<int:po_id>', methods=['DELETE'])
@token_required
def delete_purchase_order(current_user, po_id):
    """
    حذف أمر شراء
    """
    try:
        po = PurchaseOrder.query.get_or_404(po_id)
        
        # التحقق من الحالة
        if po.status not in [POStatus.DRAFT.value, POStatus.CANCELLED.value]:
            return jsonify({'success': False, 'message': 'لا يمكن حذف أمر شراء معتمد أو مستلم'}), 400
        
        db.session.delete(po)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم حذف أمر الشراء بنجاح'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
