"""
Purchase Helper Functions
دوال مساعدة لنظام المشتريات
"""

from datetime import datetime, date
from src.database import db
from src.models.purchase_order import PurchaseOrder
from src.models.purchase_receipt import PurchaseReceipt
from src.models.lot_advanced import LotAdvanced


def generate_po_number():
    """
    توليد رقم أمر شراء تلقائي
    
    Returns:
        str: رقم أمر الشراء (مثال: PO-2025-0001)
    """
    year = datetime.now().year
    prefix = f"PO-{year}-"
    
    # البحث عن آخر رقم
    last_po = PurchaseOrder.query.filter(
        PurchaseOrder.po_number.like(f"{prefix}%")
    ).order_by(PurchaseOrder.id.desc()).first()
    
    if last_po:
        # استخراج الرقم من آخر أمر شراء
        try:
            last_number = int(last_po.po_number.split('-')[-1])
            new_number = last_number + 1
        except:
            new_number = 1
    else:
        new_number = 1
    
    return f"{prefix}{new_number:04d}"


def generate_receipt_number():
    """
    توليد رقم إيصال استلام تلقائي
    
    Returns:
        str: رقم الإيصال (مثال: REC-2025-0001)
    """
    year = datetime.now().year
    prefix = f"REC-{year}-"
    
    # البحث عن آخر رقم
    last_receipt = PurchaseReceipt.query.filter(
        PurchaseReceipt.receipt_number.like(f"{prefix}%")
    ).order_by(PurchaseReceipt.id.desc()).first()
    
    if last_receipt:
        try:
            last_number = int(last_receipt.receipt_number.split('-')[-1])
            new_number = last_number + 1
        except:
            new_number = 1
    else:
        new_number = 1
    
    return f"{prefix}{new_number:04d}"


def calculate_po_total(items):
    """
    حساب إجمالي أمر الشراء
    
    Args:
        items: قائمة عناصر أمر الشراء
    
    Returns:
        float: الإجمالي
    """
    total = 0
    for item in items:
        if hasattr(item, 'final_price') and item.final_price:
            total += float(item.final_price)
        elif hasattr(item, 'total_price') and item.total_price:
            total += float(item.total_price)
    
    return total


def create_batch_from_receipt(purchase_item, received_quantity, receipt_data):
    """
    إنشاء لوط جديد من إيصال الاستلام
    
    Args:
        purchase_item: عنصر أمر الشراء
        received_quantity: الكمية المستلمة
        receipt_data: بيانات الإيصال
    
    Returns:
        LotAdvanced: اللوط المنشأ
    """
    from src.models.product_advanced import ProductAdvanced
    
    # الحصول على المنتج
    product = ProductAdvanced.query.get(purchase_item.product_id)
    if not product:
        raise ValueError(f"المنتج {purchase_item.product_id} غير موجود")
    
    # توليد رقم اللوط
    batch_number = generate_batch_number(product.id)
    
    # إنشاء اللوط
    batch = LotAdvanced(
        batch_number=batch_number,
        product_id=product.id,
        quantity=received_quantity,
        original_quantity=received_quantity,
        available_quantity=received_quantity,
        reserved_quantity=0,
        unit_cost=float(purchase_item.unit_price) if purchase_item.unit_price else 0,
        
        # تواريخ
        manufacture_date=purchase_item.manufacture_date or date.today(),
        expiry_date=purchase_item.expiry_date,
        receipt_date=date.today(),
        
        # الحالة
        status='active',
        
        # معلومات إضافية من الإيصال
        supplier_batch_number=receipt_data.get('supplier_batch_number'),
        notes=purchase_item.notes or receipt_data.get('batch_notes'),
        
        # معلومات الجودة الأساسية
        quality_status='pending',
        
        # Audit
        created_by=receipt_data.get('created_by')
    )
    
    db.session.add(batch)
    db.session.flush()
    
    return batch


def generate_batch_number(product_id):
    """
    توليد رقم لوط تلقائي
    
    Args:
        product_id: معرف المنتج
    
    Returns:
        str: رقم اللوط (مثال: BATCH-123-2025-0001)
    """
    year = datetime.now().year
    prefix = f"BATCH-{product_id}-{year}-"
    
    # البحث عن آخر رقم
    last_batch = LotAdvanced.query.filter(
        LotAdvanced.batch_number.like(f"{prefix}%")
    ).order_by(LotAdvanced.id.desc()).first()
    
    if last_batch:
        try:
            last_number = int(last_batch.batch_number.split('-')[-1])
            new_number = last_number + 1
        except:
            new_number = 1
    else:
        new_number = 1
    
    return f"{prefix}{new_number:04d}"


def update_inventory_from_receipt(receipt):
    """
    تحديث المخزون من إيصال الاستلام
    
    Args:
        receipt: إيصال الاستلام
    
    Returns:
        bool: نجاح العملية
    """
    from src.models.purchase_order_item import PurchaseOrderItem
    
    items = PurchaseOrderItem.query.filter_by(po_id=receipt.po_id).all()
    
    for item in items:
        if item.batch_id and item.received_quantity > 0:
            batch = LotAdvanced.query.get(item.batch_id)
            if batch:
                # تحديث الكمية
                batch.quantity = item.received_quantity
                batch.original_quantity = item.received_quantity
                batch.available_quantity = item.received_quantity
    
    db.session.commit()
    return True


def send_po_notification(po, notification_type='created'):
    """
    إرسال إشعار عن أمر الشراء
    
    Args:
        po: أمر الشراء
        notification_type: نوع الإشعار (created, approved, received, etc.)
    
    Returns:
        bool: نجاح الإرسال
    """
    # TODO: تطبيق نظام الإشعارات
    # يمكن إرسال إشعارات عبر:
    # - البريد الإلكتروني
    # - SMS
    # - إشعارات داخل النظام
    
    print(f"Notification: PO {po.po_number} - {notification_type}")
    return True


def validate_po_items(items_data):
    """
    التحقق من صحة عناصر أمر الشراء
    
    Args:
        items_data: بيانات العناصر
    
    Returns:
        tuple: (valid, errors)
    """
    errors = []
    
    if not items_data or len(items_data) == 0:
        errors.append("يجب إضافة عنصر واحد على الأقل")
        return False, errors
    
    for idx, item in enumerate(items_data):
        # التحقق من المنتج
        if not item.get('product_id'):
            errors.append(f"العنصر {idx + 1}: معرف المنتج مطلوب")
        
        # التحقق من الكمية
        if not item.get('quantity') or item['quantity'] <= 0:
            errors.append(f"العنصر {idx + 1}: الكمية يجب أن تكون أكبر من صفر")
        
        # التحقق من السعر
        if not item.get('unit_price') or item['unit_price'] <= 0:
            errors.append(f"العنصر {idx + 1}: سعر الوحدة يجب أن يكون أكبر من صفر")
    
    return len(errors) == 0, errors


def calculate_item_total(quantity, unit_price, discount_percentage=0, tax_percentage=0):
    """
    حساب إجمالي عنصر
    
    Args:
        quantity: الكمية
        unit_price: سعر الوحدة
        discount_percentage: نسبة الخصم
        tax_percentage: نسبة الضريبة
    
    Returns:
        dict: تفاصيل الحساب
    """
    # السعر الأساسي
    base_total = quantity * unit_price
    
    # الخصم
    discount_amount = base_total * (discount_percentage / 100)
    after_discount = base_total - discount_amount
    
    # الضريبة
    tax_amount = after_discount * (tax_percentage / 100)
    final_total = after_discount + tax_amount
    
    return {
        'base_total': base_total,
        'discount_amount': discount_amount,
        'after_discount': after_discount,
        'tax_amount': tax_amount,
        'final_total': final_total
    }
