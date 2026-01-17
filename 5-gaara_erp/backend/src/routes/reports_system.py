"""
APIs نظام التقارير الشامل
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, func, desc, extract
from src.database import db
from src.models.sale import Sale, SaleItem
from src.models.purchase_order import PurchaseOrder
from src.models.lot_advanced import LotAdvanced
from src.models.product_advanced import ProductAdvanced
from src.models.shift import Shift

reports_system_bp = Blueprint('reports_system', __name__, url_prefix='/api/reports')

# ==================== Sales Reports ====================

@reports_system_bp.route('/sales/summary', methods=['GET'])
def sales_summary():
    """تقرير ملخص المبيعات"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Sale.query.filter(Sale.status != 'refunded')
        
        if start_date:
            query = query.filter(Sale.sale_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Sale.sale_date <= datetime.fromisoformat(end_date))
        
        sales = query.all()
        
        total_sales = sum(sale.total for sale in sales)
        total_refunds = sum(sale.total for sale in Sale.query.filter(Sale.is_refund == True).all())
        total_transactions = len(sales)
        average_sale = total_sales / total_transactions if total_transactions > 0 else 0
        
        # المبيعات حسب طريقة الدفع
        cash_sales = sum(sale.total for sale in sales if sale.payment_method == 'cash')
        card_sales = sum(sale.total for sale in sales if sale.payment_method == 'card')
        
        # المبيعات حسب اليوم
        sales_by_day = {}
        for sale in sales:
            day = sale.sale_date.date().isoformat()
            if day not in sales_by_day:
                sales_by_day[day] = 0
            sales_by_day[day] += sale.total
        
        return jsonify({
            'success': True,
            'summary': {
                'total_sales': total_sales,
                'total_refunds': total_refunds,
                'net_sales': total_sales - total_refunds,
                'total_transactions': total_transactions,
                'average_sale': average_sale,
                'cash_sales': cash_sales,
                'card_sales': card_sales,
                'sales_by_day': sales_by_day
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_system_bp.route('/sales/by-product', methods=['GET'])
def sales_by_product():
    """تقرير المبيعات حسب المنتج"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = db.session.query(
            SaleItem.product_id,
            SaleItem.product_name,
            func.sum(SaleItem.quantity).label('total_quantity'),
            func.sum(SaleItem.total).label('total_amount'),
            func.count(SaleItem.id).label('transaction_count')
        ).join(Sale).filter(Sale.status != 'refunded')
        
        if start_date:
            query = query.filter(Sale.sale_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Sale.sale_date <= datetime.fromisoformat(end_date))
        
        results = query.group_by(SaleItem.product_id, SaleItem.product_name)\
                      .order_by(desc('total_amount'))\
                      .all()
        
        products = []
        for result in results:
            products.append({
                'product_id': result.product_id,
                'product_name': result.product_name,
                'total_quantity': float(result.total_quantity),
                'total_amount': float(result.total_amount),
                'transaction_count': result.transaction_count,
                'average_price': float(result.total_amount / result.total_quantity) if result.total_quantity > 0 else 0
            })
        
        return jsonify({
            'success': True,
            'products': products,
            'total_products': len(products)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_system_bp.route('/sales/by-customer', methods=['GET'])
def sales_by_customer():
    """تقرير المبيعات حسب العميل"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = db.session.query(
            Sale.customer_id,
            Sale.customer_name,
            func.count(Sale.id).label('transaction_count'),
            func.sum(Sale.total).label('total_amount'),
            func.avg(Sale.total).label('average_sale')
        ).filter(Sale.status != 'refunded', Sale.customer_id.isnot(None))
        
        if start_date:
            query = query.filter(Sale.sale_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Sale.sale_date <= datetime.fromisoformat(end_date))
        
        results = query.group_by(Sale.customer_id, Sale.customer_name)\
                      .order_by(desc('total_amount'))\
                      .all()
        
        customers = []
        for result in results:
            customers.append({
                'customer_id': result.customer_id,
                'customer_name': result.customer_name,
                'transaction_count': result.transaction_count,
                'total_amount': float(result.total_amount),
                'average_sale': float(result.average_sale)
            })
        
        return jsonify({
            'success': True,
            'customers': customers,
            'total_customers': len(customers)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Inventory Reports ====================

@reports_system_bp.route('/inventory/stock-levels', methods=['GET'])
def inventory_stock_levels():
    """تقرير مستويات المخزون"""
    try:
        low_stock_only = request.args.get('low_stock_only', 'false').lower() == 'true'
        
        # الحصول على المنتجات مع اللوطات
        products_query = ProductAdvanced.query
        
        products_data = []
        for product in products_query.all():
            # الحصول على اللوطات النشطة
            batches = LotAdvanced.query.filter(
                and_(
                    LotAdvanced.product_id == product.id,
                    LotAdvanced.status == 'active'
                )
            ).all()
            
            total_quantity = sum(batch.current_quantity for batch in batches)
            
            # تخطي إذا كان المخزون كافي ونريد فقط المنخفض
            if low_stock_only and total_quantity >= product.min_stock_level:
                continue
            
            products_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'product_code': product.code,
                'total_quantity': total_quantity,
                'min_stock_level': product.min_stock_level,
                'max_stock_level': product.max_stock_level,
                'is_low_stock': total_quantity < product.min_stock_level,
                'batches_count': len(batches)
            })
        
        return jsonify({
            'success': True,
            'products': products_data,
            'total_products': len(products_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_system_bp.route('/inventory/expiring-lots', methods=['GET'])
def inventory_expiring_lots():
    """تقرير اللوطات قريبة الانتهاء"""
    try:
        days = request.args.get('days', 30, type=int)
        
        expiry_date = datetime.now() + timedelta(days=days)
        
        batches = LotAdvanced.query.filter(
            and_(
                LotAdvanced.status == 'active',
                LotAdvanced.expiry_date <= expiry_date,
                LotAdvanced.current_quantity > 0
            )
        ).order_by(LotAdvanced.expiry_date).all()
        
        batches_data = []
        for batch in batches:
            days_to_expiry = (batch.expiry_date - datetime.now()).days
            
            batches_data.append({
                'batch_id': batch.id,
                'batch_number': batch.batch_number,
                'product_id': batch.product_id,
                'product_name': batch.product_name,
                'current_quantity': batch.current_quantity,
                'expiry_date': batch.expiry_date.isoformat(),
                'days_to_expiry': days_to_expiry,
                'is_expired': days_to_expiry < 0,
                'urgency': 'critical' if days_to_expiry < 7 else 'warning' if days_to_expiry < 30 else 'normal'
            })
        
        return jsonify({
            'success': True,
            'batches': batches_data,
            'total_batches': len(batches_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Financial Reports ====================

@reports_system_bp.route('/financial/profit-loss', methods=['GET'])
def financial_profit_loss():
    """تقرير الأرباح والخسائر"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # المبيعات
        sales_query = Sale.query.filter(Sale.status != 'refunded')
        if start_date:
            sales_query = sales_query.filter(Sale.sale_date >= datetime.fromisoformat(start_date))
        if end_date:
            sales_query = sales_query.filter(Sale.sale_date <= datetime.fromisoformat(end_date))
        
        total_revenue = sum(sale.total for sale in sales_query.all())
        
        # المشتريات
        purchases_query = PurchaseOrder.query.filter(PurchaseOrder.status == 'received')
        if start_date:
            purchases_query = purchases_query.filter(PurchaseOrder.order_date >= datetime.fromisoformat(start_date))
        if end_date:
            purchases_query = purchases_query.filter(PurchaseOrder.order_date <= datetime.fromisoformat(end_date))
        
        total_cost = sum(po.total_amount for po in purchases_query.all())
        
        # الأرباح
        gross_profit = total_revenue - total_cost
        profit_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return jsonify({
            'success': True,
            'report': {
                'total_revenue': total_revenue,
                'total_cost': total_cost,
                'gross_profit': gross_profit,
                'profit_margin': profit_margin,
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Shift Reports ====================

@reports_system_bp.route('/shifts/performance', methods=['GET'])
def shifts_performance():
    """تقرير أداء الورديات"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Shift.query.filter(Shift.status == 'closed')
        
        if start_date:
            query = query.filter(Shift.opening_time >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Shift.closing_time <= datetime.fromisoformat(end_date))
        
        shifts = query.all()
        
        shifts_data = []
        for shift in shifts:
            duration = (shift.closing_time - shift.opening_time).total_seconds() / 3600  # hours
            
            shifts_data.append({
                'shift_id': shift.id,
                'shift_number': shift.shift_number,
                'user_id': shift.user_id,
                'opening_time': shift.opening_time.isoformat(),
                'closing_time': shift.closing_time.isoformat(),
                'duration_hours': round(duration, 2),
                'total_sales': shift.total_sales,
                'total_transactions': shift.total_transactions,
                'cash_difference': shift.cash_difference,
                'sales_per_hour': shift.total_sales / duration if duration > 0 else 0
            })
        
        # إحصائيات عامة
        total_sales = sum(shift.total_sales for shift in shifts)
        total_transactions = sum(shift.total_transactions for shift in shifts)
        average_shift_sales = total_sales / len(shifts) if len(shifts) > 0 else 0
        
        return jsonify({
            'success': True,
            'shifts': shifts_data,
            'summary': {
                'total_shifts': len(shifts),
                'total_sales': total_sales,
                'total_transactions': total_transactions,
                'average_shift_sales': average_shift_sales
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Dashboard Stats ====================

@reports_system_bp.route('/dashboard/stats', methods=['GET'])
def dashboard_stats():
    """إحصائيات لوحة التحكم"""
    try:
        # المبيعات اليوم
        today = datetime.now().date()
        today_sales = Sale.query.filter(
            and_(
                func.date(Sale.sale_date) == today,
                Sale.status != 'refunded'
            )
        ).all()
        
        today_revenue = sum(sale.total for sale in today_sales)
        today_transactions = len(today_sales)
        
        # المبيعات هذا الشهر
        this_month = datetime.now().replace(day=1)
        month_sales = Sale.query.filter(
            and_(
                Sale.sale_date >= this_month,
                Sale.status != 'refunded'
            )
        ).all()
        
        month_revenue = sum(sale.total for sale in month_sales)
        
        # المخزون المنخفض
        low_stock_count = 0
        for product in ProductAdvanced.query.all():
            batches = LotAdvanced.query.filter(
                and_(
                    LotAdvanced.product_id == product.id,
                    LotAdvanced.status == 'active'
                )
            ).all()
            total_quantity = sum(batch.current_quantity for batch in batches)
            if total_quantity < product.min_stock_level:
                low_stock_count += 1
        
        # اللوطات منتهية الصلاحية
        expired_lots = LotAdvanced.query.filter(
            and_(
                LotAdvanced.expiry_date < datetime.now(),
                LotAdvanced.status == 'active',
                LotAdvanced.current_quantity > 0
            )
        ).count()
        
        # الورديات المفتوحة
        open_shifts = Shift.query.filter(Shift.status == 'open').count()
        
        return jsonify({
            'success': True,
            'stats': {
                'today': {
                    'revenue': today_revenue,
                    'transactions': today_transactions,
                    'average_sale': today_revenue / today_transactions if today_transactions > 0 else 0
                },
                'month': {
                    'revenue': month_revenue,
                    'transactions': len(month_sales)
                },
                'inventory': {
                    'low_stock_count': low_stock_count,
                    'expired_lots': expired_lots
                },
                'operations': {
                    'open_shifts': open_shifts
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
