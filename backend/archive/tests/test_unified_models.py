#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار النماذج الموحدة
Test Unified Models

يقوم باختبار جميع النماذج الموحدة والعلاقات بينها
"""

import sys
import os
from datetime import datetime, date

# إضافة المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from src.models import (
    User,
    Role,
    Product,
    Invoice,
    Warehouse,
    InvoiceItem,
    Payment,
    StockMovement,
    AuditLog,
    Category,
    Customer,
    Supplier,
    ProductType,
    TrackingType,
    InvoiceType,
    InvoiceStatus,
    PaymentStatus,
    PaymentMethod,
    MovementType,
    ActionType,
)


def test_database_connection():
    """اختبار الاتصال بقاعدة البيانات"""
    print("\n🔌 اختبار الاتصال بقاعدة البيانات...")

    try:
        with app.app_context():
            # محاولة الاستعلام البسيط
            result = db.session.execute(db.text("SELECT 1")).fetchone()
            if result:
                print("✅ الاتصال بقاعدة البيانات ناجح")
                return True
            else:
                print("❌ فشل الاتصال بقاعدة البيانات")
                return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False


def test_create_tables():
    """اختبار إنشاء الجداول"""
    print("\n🔨 اختبار إنشاء الجداول...")

    try:
        with app.app_context():
            db.create_all()
            print("✅ تم إنشاء جميع الجداول بنجاح")
            return True
    except Exception as e:
        print(f"❌ خطأ في إنشاء الجداول: {e}")
        return False


def test_role_model():
    """اختبار نموذج Role"""
    print("\n👥 اختبار نموذج Role...")

    try:
        with app.app_context():
            # إنشاء دور جديد
            role = Role(
                name="test_role", display_name="دور اختباري", description="دور للاختبار"
            )
            role.set_permissions(["view_products", "create_product"])

            db.session.add(role)
            db.session.commit()

            # التحقق من الدور
            saved_role = Role.query.filter_by(name="test_role").first()
            assert saved_role is not None, "فشل حفظ الدور"
            assert saved_role.has_permission("view_products"), "فشل التحقق من الصلاحية"

            # حذف الدور
            db.session.delete(saved_role)
            db.session.commit()

            print("✅ نموذج Role يعمل بشكل صحيح")
            return True

    except Exception as e:
        print(f"❌ خطأ في اختبار Role: {e}")
        db.session.rollback()
        return False


def test_user_model():
    """اختبار نموذج User"""
    print("\n👤 اختبار نموذج User...")

    try:
        with app.app_context():
            # إنشاء مستخدم جديد
            user = User(
                username="test_user",
                email="test@example.com",
                full_name="مستخدم اختباري",
            )
            user.set_password("password123")

            db.session.add(user)
            db.session.commit()

            # التحقق من المستخدم
            saved_user = User.query.filter_by(username="test_user").first()
            assert saved_user is not None, "فشل حفظ المستخدم"
            assert saved_user.check_password("password123"), "فشل التحقق من كلمة المرور"
            assert not saved_user.check_password(
                "wrong_password"
            ), "كلمة مرور خاطئة تم قبولها"

            # اختبار قفل الحساب
            for i in range(5):
                saved_user.record_failed_login()
            assert saved_user.is_account_locked(), "فشل قفل الحساب"

            # حذف المستخدم
            db.session.delete(saved_user)
            db.session.commit()

            print("✅ نموذج User يعمل بشكل صحيح")
            return True

    except Exception as e:
        print(f"❌ خطأ في اختبار User: {e}")
        db.session.rollback()
        return False


def test_product_model():
    """اختبار نموذج Product"""
    print("\n📦 اختبار نموذج Product...")

    try:
        with app.app_context():
            # إنشاء منتج جديد
            product = Product(
                name="منتج اختباري",
                sku="TEST-001",
                barcode="1234567890",
                product_type=ProductType.STORABLE,
                cost_price=100.00,
                sale_price=150.00,
                current_stock=50,
                min_quantity=10,
            )

            db.session.add(product)
            db.session.commit()

            # التحقق من المنتج
            saved_product = Product.query.filter_by(sku="TEST-001").first()
            assert saved_product is not None, "فشل حفظ المنتج"
            assert (
                saved_product.calculate_profit_margin() == 50.0
            ), "خطأ في حساب هامش الربح"
            assert not saved_product.is_low_stock(), "خطأ في التحقق من المخزون المنخفض"

            # اختبار تحديث المخزون
            saved_product.update_stock(10, "subtract")
            assert saved_product.current_stock == 40, "فشل تحديث المخزون"

            # حذف المنتج
            db.session.delete(saved_product)
            db.session.commit()

            print("✅ نموذج Product يعمل بشكل صحيح")
            return True

    except Exception as e:
        print(f"❌ خطأ في اختبار Product: {e}")
        db.session.rollback()
        return False


def test_warehouse_model():
    """اختبار نموذج Warehouse"""
    print("\n🏢 اختبار نموذج Warehouse...")

    try:
        with app.app_context():
            # إنشاء مستودع جديد
            warehouse = Warehouse(
                name="مستودع اختباري", code="WH-TEST", location="الرياض", is_main=True
            )

            db.session.add(warehouse)
            db.session.commit()

            # التحقق من المستودع
            saved_warehouse = Warehouse.query.filter_by(code="WH-TEST").first()
            assert saved_warehouse is not None, "فشل حفظ المستودع"
            assert saved_warehouse.is_main == True, "خطأ في حقل is_main"

            # حذف المستودع
            db.session.delete(saved_warehouse)
            db.session.commit()

            print("✅ نموذج Warehouse يعمل بشكل صحيح")
            return True

    except Exception as e:
        print(f"❌ خطأ في اختبار Warehouse: {e}")
        db.session.rollback()
        return False


def test_invoice_model():
    """اختبار نموذج Invoice"""
    print("\n🧾 اختبار نموذج Invoice...")

    try:
        with app.app_context():
            # إنشاء مستخدم للفاتورة
            user = User(username="invoice_user", email="invoice@test.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            # إنشاء فاتورة جديدة
            invoice = Invoice(
                invoice_number="INV-TEST-001",
                invoice_type=InvoiceType.SALES,
                invoice_date=date.today(),
                created_by=user.id,
                subtotal=1000.00,
                tax_rate=15.00,
            )

            db.session.add(invoice)
            db.session.commit()

            # التحقق من الفاتورة
            saved_invoice = Invoice.query.filter_by(
                invoice_number="INV-TEST-001"
            ).first()
            assert saved_invoice is not None, "فشل حفظ الفاتورة"
            assert (
                saved_invoice.invoice_type == InvoiceType.SALES
            ), "خطأ في نوع الفاتورة"

            # اختبار حساب الإجماليات
            saved_invoice.calculate_totals()
            assert saved_invoice.tax_amount > 0, "فشل حساب الضريبة"

            # حذف الفاتورة والمستخدم
            db.session.delete(saved_invoice)
            db.session.delete(user)
            db.session.commit()

            print("✅ نموذج Invoice يعمل بشكل صحيح")
            return True

    except Exception as e:
        print(f"❌ خطأ في اختبار Invoice: {e}")
        db.session.rollback()
        return False


def test_relationships():
    """اختبار العلاقات بين النماذج"""
    print("\n🔗 اختبار العلاقات بين النماذج...")

    try:
        with app.app_context():
            # إنشاء دور
            role = Role(name="test_rel_role", display_name="دور")
            db.session.add(role)
            db.session.commit()

            # إنشاء مستخدم مع دور
            user = User(username="rel_user", email="rel@test.com", role_id=role.id)
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            # التحقق من العلاقة
            assert user.role_obj is not None, "فشل ربط المستخدم بالدور"
            assert user.role_obj.name == "test_rel_role", "خطأ في العلاقة"

            # حذف البيانات
            db.session.delete(user)
            db.session.delete(role)
            db.session.commit()

            print("✅ العلاقات تعمل بشكل صحيح")
            return True

    except Exception as e:
        print(f"❌ خطأ في اختبار العلاقات: {e}")
        db.session.rollback()
        return False


def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🧪 بدء اختبار النماذج الموحدة")
    print("=" * 60)

    tests = [
        ("الاتصال بقاعدة البيانات", test_database_connection),
        ("إنشاء الجداول", test_create_tables),
        ("نموذج Role", test_role_model),
        ("نموذج User", test_user_model),
        ("نموذج Product", test_product_model),
        ("نموذج Warehouse", test_warehouse_model),
        ("نموذج Invoice", test_invoice_model),
        ("العلاقات", test_relationships),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ خطأ غير متوقع في {test_name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print("📊 نتائج الاختبار")
    print("=" * 60)
    print(f"✅ نجح: {passed}")
    print(f"❌ فشل: {failed}")
    print(f"📈 نسبة النجاح: {(passed / len(tests) * 100):.1f}%")

    if failed == 0:
        print("\n🎉 جميع الاختبارات نجحت!")
        return True
    else:
        print(f"\n⚠️ فشل {failed} اختبار(ات)")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ تم إيقاف الاختبار بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
