"""
APIs نظام نقطة البيع (POS)
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy import and_, or_, desc
from src.database import db
from src.models.shift import Shift
from src.models.sale import Sale, SaleItem
from src.models.lot_advanced import LotAdvanced
from src.models.product_advanced import ProductAdvanced

pos_bp = Blueprint('pos', __name__, url_prefix='/api/pos')

# ==================== Shifts APIs ====================

@pos_bp.route('/shifts', methods=['GET'])
def get_shifts():
    """الحصول على قائمة الورديات"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        user_id = request.args.get('user_id', type=int)
        
        query = Shift.query
        
        if status:
            query = query.filter(Shift.status == status)
        if user_id:
            query = query.filter(Shift.user_id == user_id)
        
        query = query.order_by(desc(Shift.opening_time))
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'shifts': [shift.to_dict() for shift in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@pos_bp.route('/shifts/<int:shift_id>', methods=['GET'])
def get_shift(shift_id):
    """الحصول على تفاصيل وردية"""
    try:
        shift = Shift.query.get_or_404(shift_id)
        return jsonify({'success': True, 'shift': shift.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@pos_bp.route('/shifts/open', methods=['POST'])
def open_shift():
    """فتح وردية جديدة"""
    try:
        data = request.get_json()
        
        # التحقق من عدم وجود وردية مفتوحة للمستخدم
        open_shift = Shift.query.filter(
            and_(
                Shift.user_id == data['user_id'],
                Shift.status == 'open'
            )
        ).first()
        
        if open_shift:
            return jsonify({
                'success': False,
                'error': 'لديك وردية مفتوحة بالفعل'
            }), 400
        
        # إنشاء رقم الوردية
        shift_number = f"SH-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # إنشاء الوردية
        shift = Shift(
            shift_number=shift_number,
            user_id=data['user_id'],
            branch_id=data.get('branch_id'),
            opening_cash=data.get('opening_cash', 0.0),
            opening_notes=data.get('opening_notes'),
            status='open'
        )
        
        db.session.add(shift)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم فتح الوردية بنجاح',
            'shift': shift.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@pos_bp.route('/shifts/<int:shift_id>/close', methods=['POST'])
def close_shift(shift_id):
    """إغلاق وردية"""
    try:
        shift = Shift.query.get_or_404(shift_id)
        
        if shift.status == 'closed':
            return jsonify({
                'success': False,
                'error': 'الوردية مغلقة بالفعل'
            }), 400
        
        data = request.get_json()
        shift.close_shift(
            closing_cash=data['closing_cash'],
            closing_notes=data.get('closing_notes')
        )
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم إغلاق الوردية بنجاح',
            'shift': shift.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@pos_bp.route('/shifts/current', methods=['GET'])
def get_current_shift():
    """الحصول على الوردية الحالية للمستخدم"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id مطلوب'
            }), 400
        
        shift = Shift.query.filter(
            and_(
                Shift.user_id == user_id,
                Shift.status == 'open'
            )
        ).first()
        
        if not shift:
            return jsonify({
                'success': False,
                'error': 'لا توجد وردية مفتوحة'
            }), 404
        
        return jsonify({
            'success': True,
            'shift': shift.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Sales APIs ====================

@pos_bp.route('/sales', methods=['POST'])
def create_sale():
    """إنشاء عملية بيع جديدة"""
    try:
        data = request.get_json()
        
        # إنشاء رقم الفاتورة
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # إنشاء عملية البيع
        sale = Sale(
            invoice_number=invoice_number,
            customer_id=data.get('customer_id'),
            customer_name=data.get('customer_name'),
            shift_id=data.get('shift_id'),
            branch_id=data.get('branch_id'),
            user_id=data['user_id'],
            discount_percentage=data.get('discount_percentage', 0.0),
            tax_percentage=data.get('tax_percentage', 0.0),
            payment_method=data.get('payment_method', 'cash'),
            paid_amount=data.get('paid_amount', 0.0),
            notes=data.get('notes')
        )
        
        # إضافة العناصر
        for item_data in data.get('items', []):
            # الحصول على المنتج
            product = ProductAdvanced.query.get(item_data['product_id'])
            if not product:
                return jsonify({
                    'success': False,
                    'error': f'المنتج {item_data["product_id"]} غير موجود'
                }), 404
            
            # اختيار اللوط (FIFO)
            batch = None
            if item_data.get('batch_id'):
                batch = LotAdvanced.query.get(item_data['batch_id'])
            else:
                # اختيار أول لوط متاح (FIFO)
                batch = LotAdvanced.query.filter(
                    and_(
                        LotAdvanced.product_id == product.id,
                        LotAdvanced.status == 'active',
                        LotAdvanced.current_quantity >= item_data['quantity']
                    )
                ).order_by(LotAdvanced.expiry_date).first()
            
            # إنشاء عنصر البيع
            sale_item = SaleItem(
                product_id=product.id,
                batch_id=batch.id if batch else None,
                product_name=product.name,
                product_code=product.code,
                quantity=item_data['quantity'],
                unit_price=item_data.get('unit_price', product.selling_price),
                discount_percentage=item_data.get('discount_percentage', 0.0),
                lot_number=batch.batch_number if batch else None,
                expiry_date=batch.expiry_date if batch else None
            )
            
            sale_item.calculate_total()
            sale.items.append(sale_item)
            
            # تحديث كمية اللوط
            if batch:
                batch.current_quantity -= item_data['quantity']
                batch.reserved_quantity += item_data['quantity']
        
        # حساب الإجماليات
        sale.calculate_totals()
        
        # تحديث الوردية
        if sale.shift_id:
            shift = Shift.query.get(sale.shift_id)
            if shift:
                shift.add_sale(sale.total, sale.payment_method)
        
        db.session.add(sale)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء الفاتورة بنجاح',
            'sale': sale.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@pos_bp.route('/sales/<int:sale_id>', methods=['GET'])
def get_sale(sale_id):
    """الحصول على تفاصيل عملية بيع"""
    try:
        sale = Sale.query.get_or_404(sale_id)
        return jsonify({'success': True, 'sale': sale.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@pos_bp.route('/sales/<int:sale_id>/refund', methods=['POST'])
def refund_sale(sale_id):
    """إرجاع عملية بيع"""
    try:
        original_sale = Sale.query.get_or_404(sale_id)
        
        if original_sale.status == 'refunded':
            return jsonify({
                'success': False,
                'error': 'تم إرجاع هذه الفاتورة بالفعل'
            }), 400
        
        data = request.get_json()
        
        # إنشاء رقم فاتورة الإرجاع
        refund_invoice_number = f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # إنشاء فاتورة الإرجاع
        refund_sale = Sale(
            invoice_number=refund_invoice_number,
            customer_id=original_sale.customer_id,
            customer_name=original_sale.customer_name,
            shift_id=data.get('shift_id'),
            branch_id=original_sale.branch_id,
            user_id=data['user_id'],
            subtotal=-original_sale.subtotal,
            discount_amount=-original_sale.discount_amount,
            discount_percentage=original_sale.discount_percentage,
            tax_amount=-original_sale.tax_amount,
            tax_percentage=original_sale.tax_percentage,
            total=-original_sale.total,
            payment_method=original_sale.payment_method,
            paid_amount=-original_sale.total,
            is_refund=True,
            refund_of_sale_id=original_sale.id,
            notes=data.get('notes')
        )
        
        # إرجاع العناصر
        for original_item in original_sale.items:
            refund_item = SaleItem(
                product_id=original_item.product_id,
                batch_id=original_item.batch_id,
                product_name=original_item.product_name,
                product_code=original_item.product_code,
                quantity=-original_item.quantity,
                unit_price=original_item.unit_price,
                discount_amount=-original_item.discount_amount,
                discount_percentage=original_item.discount_percentage,
                total=-original_item.total,
                lot_number=original_item.lot_number,
                expiry_date=original_item.expiry_date
            )
            
            refund_sale.items.append(refund_item)
            
            # إرجاع الكمية للوط
            if original_item.batch_id:
                batch = LotAdvanced.query.get(original_item.batch_id)
                if batch:
                    batch.current_quantity += abs(original_item.quantity)
                    batch.reserved_quantity -= abs(original_item.quantity)
        
        # تحديث حالة الفاتورة الأصلية
        original_sale.status = 'refunded'
        
        # تحديث الوردية
        if refund_sale.shift_id:
            shift = Shift.query.get(refund_sale.shift_id)
            if shift:
                shift.add_refund(abs(refund_sale.total))
        
        db.session.add(refund_sale)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم إرجاع الفاتورة بنجاح',
            'refund_sale': refund_sale.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@pos_bp.route('/products/search', methods=['GET'])
def search_products():
    """البحث عن المنتجات (للباركود والاسم)"""
    try:
        query_text = request.args.get('q', '')
        
        if not query_text:
            return jsonify({'success': True, 'products': []})
        
        products = ProductAdvanced.query.filter(
            or_(
                ProductAdvanced.name.ilike(f'%{query_text}%'),
                ProductAdvanced.code.ilike(f'%{query_text}%'),
                ProductAdvanced.barcode == query_text
            )
        ).limit(20).all()
        
        results = []
        for product in products:
            # الحصول على اللوطات المتاحة
            batches = LotAdvanced.query.filter(
                and_(
                    LotAdvanced.product_id == product.id,
                    LotAdvanced.status == 'active',
                    LotAdvanced.current_quantity > 0
                )
            ).order_by(LotAdvanced.expiry_date).all()
            
            results.append({
                'id': product.id,
                'name': product.name,
                'code': product.code,
                'barcode': product.barcode,
                'selling_price': product.selling_price,
                'available_quantity': sum(b.current_quantity for b in batches),
                'batches': [b.to_dict() for b in batches]
            })
        
        return jsonify({'success': True, 'products': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@pos_bp.route('/stats', methods=['GET'])
def get_pos_stats():
    """إحصائيات نقطة البيع"""
    try:
        shift_id = request.args.get('shift_id', type=int)
        
        if not shift_id:
            return jsonify({
                'success': False,
                'error': 'shift_id مطلوب'
            }), 400
        
        shift = Shift.query.get_or_404(shift_id)
        
        # إحصائيات المبيعات
        sales = Sale.query.filter(Sale.shift_id == shift_id).all()
        
        stats = {
            'shift': shift.to_dict(),
            'total_sales': shift.total_sales,
            'total_refunds': shift.total_refunds,
            'total_transactions': shift.total_transactions,
            'cash_sales': shift.cash_sales,
            'card_sales': shift.card_sales,
            'other_sales': shift.other_sales,
            'net_sales': shift.total_sales - shift.total_refunds,
            'average_transaction': shift.total_sales / shift.total_transactions if shift.total_transactions > 0 else 0,
            'recent_sales': [sale.to_dict() for sale in sales[-10:]]
        }
        
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
