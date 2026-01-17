#!/usr/bin/env python3
"""
سكريبت migration لنقل البيانات من النماذج القديمة إلى النموذج الموحد
"""

from datetime import datetime
import sys
import os

# إضافة مسار src للاستيراد
sys.path.insert(0, "src")


def migrate_invoices():
    """نقل بيانات الفواتير من النماذج القديمة"""
    print("🔄 بدء migration الفواتير...")

    try:
        from models.invoice import Invoice as OldInvoice, InvoiceItem as OldInvoiceItem
        from models.unified_invoice import UnifiedInvoice, UnifiedInvoiceItem
        from database import db

        # نقل الفواتير الأساسية
        old_invoices = OldInvoice.query.all()

        for old_invoice in old_invoices:
            # إنشاء فاتورة موحدة جديدة
            new_invoice = UnifiedInvoice(
                invoice_number=old_invoice.invoice_number,
                invoice_date=old_invoice.invoice_date,
                customer_id=old_invoice.customer_id,
                total_amount=old_invoice.total_amount,
                # إضافة باقي الحقول...
            )

            db.session.add(new_invoice)

            # نقل عناصر الفاتورة
            for old_item in old_invoice.items:
                new_item = UnifiedInvoiceItem(
                    invoice=new_invoice,
                    product_id=old_item.product_id,
                    quantity=old_item.quantity,
                    unit_price=old_item.unit_price,
                    total_amount=old_item.total_amount,
                )
                db.session.add(new_item)

        db.session.commit()
        print(f"✓ تم نقل {len(old_invoices)} فاتورة")

    except Exception as e:
        print(f"✗ خطأ في migration: {e}")
        db.session.rollback()


if __name__ == "__main__":
    migrate_invoices()
