#!/usr/bin/env python3
"""
سكريبت اختبار الخادم الموحد
Unified Server Testing Script

هذا السكريبت يختبر جميع APIs في الخادم الموحد
"""

# pylint: disable=no-else-return, too-many-return-statements, too-many-nested-blocks

import time
import requests

BASE_URL = "http://localhost:5000"


def test_health_check():
    """اختبار فحص صحة الخادم"""
    print("🔍 اختبار فحص صحة الخادم...")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ الخادم يعمل بشكل صحيح: {data['status']}")
            return True
        else:
            print(f"❌ فشل فحص الصحة: {response.status_code}")
            return False
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في الاتصال بالخادم: {str(e)}")
        return False


def test_login():
    """اختبار تسجيل الدخول"""
    print("🔐 اختبار تسجيل الدخول...")

    try:
        # بيانات تسجيل الدخول
        login_data = {"username": "admin", "password": "admin123"}

        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                print(f"✅ تم تسجيل الدخول بنجاح: {data['user']['username']}")
                # حفظ الكوكيز للطلبات التالية
                return response.cookies
            else:
                print(f"❌ فشل تسجيل الدخول: {data['message']}")
                return None
        else:
            print(f"❌ خطأ في تسجيل الدخول: {response.status_code}")
            return None

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار تسجيل الدخول: {str(e)}")
        return None


def test_dashboard_stats(cookies):
    """اختبار إحصائيات لوحة التحكم"""
    print("📊 اختبار إحصائيات لوحة التحكم...")

    try:
        response = requests.get(
            f"{BASE_URL}/api/dashboard/stats",
            cookies=cookies,
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                stats = data["stats"]
                print("✅ تم الحصول على الإحصائيات:")
                print(f"   - إجمالي المنتجات: {stats['products']['total']}")
                print(f"   - منتجات قليلة المخزون: {stats['products']['low_stock']}")
                print(f"   - إجمالي العملاء: {stats['sales']['total_customers']}")
                print(f"   - إجمالي الموردين: {stats['purchases']['total_suppliers']}")
                return True
            else:
                print(f"❌ فشل في الحصول على الإحصائيات: {data['message']}")
                return False
        else:
            print(f"❌ خطأ في طلب الإحصائيات: {response.status_code}")
            return False

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار الإحصائيات: {str(e)}")
        return False


def test_products_api(cookies):
    """اختبار APIs المنتجات"""
    print("📦 اختبار APIs المنتجات...")

    try:
        # اختبار الحصول على قائمة المنتجات
        response = requests.get(
            f"{BASE_URL}/api/products",
            cookies=cookies,
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                products = data["products"]
                pagination = data["pagination"]
                print(f"✅ تم الحصول على {len(products)} منتج")
                print(f"   - إجمالي المنتجات: {pagination['total']}")
                print(f"   - الصفحات: {pagination['pages']}")

                # اختبار الحصول على منتج محدد
                if products:
                    product_id = products[0]["id"]
                    response = requests.get(
                        f"{BASE_URL}/api/products/{product_id}",
                        cookies=cookies,
                        timeout=5,
                    )

                    if response.status_code == 200:
                        product_data = response.json()
                        if product_data["success"]:
                            product = product_data["product"]
                            print(f"✅ تم الحصول على المنتج: {product['name']}")
                            print(f"   - الكود: {product['code']}")
                            print(f"   - المخزون الحالي: {product['current_stock']}")
                            return True
                        else:
                            print(
                                f"❌ فشل في الحصول على المنتج: {product_data['message']}"
                            )
                            return False
                    else:
                        print(f"❌ خطأ في طلب المنتج: {response.status_code}")
                        return False
                else:
                    print("⚠️ لا توجد منتجات للاختبار")
                    return True
            else:
                print(f"❌ فشل في الحصول على المنتجات: {data['message']}")
                return False
        else:
            print(f"❌ خطأ في طلب المنتجات: {response.status_code}")
            return False

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار APIs المنتجات: {str(e)}")
        return False


def test_create_product(cookies):
    """اختبار إنشاء منتج جديد"""
    print("➕ اختبار إنشاء منتج جديد...")

    try:
        # بيانات المنتج الجديد
        product_data = {
            "name": "منتج تجريبي للاختبار",
            "code": f"TEST-{int(time.time())}",
            "description": "منتج تجريبي لاختبار API",
            "cost_price": 100.0,
            "selling_price": 150.0,
            "current_stock": 50.0,
            "min_stock": 10.0,
            "max_stock": 200.0,
            "unit": "قطعة",
            "product_type": "test",
            "brand": "علامة تجارية تجريبية",
            "origin_country": "مصر",
            "category_id": 1,  # افتراض وجود فئة بـ ID = 1
            "warehouse_id": 1,  # افتراض وجود مخزن بـ ID = 1
        }

        response = requests.post(
            f"{BASE_URL}/api/products",
            json=product_data,
            cookies=cookies,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        if response.status_code == 201:
            data = response.json()
            if data["success"]:
                product = data["product"]
                print(f"✅ تم إنشاء المنتج بنجاح: {product['name']}")
                print(f"   - ID: {product['id']}")
                print(f"   - الكود: {product['code']}")
                return product["id"]
            else:
                print(f"❌ فشل في إنشاء المنتج: {data['message']}")
                return None
        else:
            print(f"❌ خطأ في إنشاء المنتج: {response.status_code}")
            if response.content:
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", "غير محدد")
                    print(f"   - رسالة الخطأ: {error_msg}")
                except ValueError:
                    print(f"   - محتوى الاستجابة: {response.text}")
            return None

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار إنشاء المنتج: {str(e)}")
        return None


def test_logout(cookies):
    """اختبار تسجيل الخروج"""
    print("🚪 اختبار تسجيل الخروج...")

    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/logout",
            cookies=cookies,
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                print("✅ تم تسجيل الخروج بنجاح")
                return True
            else:
                print(f"❌ فشل تسجيل الخروج: {data['message']}")
                return False
        else:
            print(f"❌ خطأ في تسجيل الخروج: {response.status_code}")
            return False

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار تسجيل الخروج: {str(e)}")
        return False


def test_customers_api(cookies):
    """اختبار APIs العملاء"""
    print("👥 اختبار APIs العملاء...")

    try:
        # اختبار الحصول على قائمة العملاء
        response = requests.get(
            f"{BASE_URL}/api/customers",
            cookies=cookies,
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                customers = data["customers"]
                print(f"✅ تم الحصول على {len(customers)} عميل")
                return True
            else:
                print(f"❌ فشل في الحصول على العملاء: {data['message']}")
                return False
        else:
            print(f"❌ خطأ في طلب العملاء: {response.status_code}")
            return False

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار APIs العملاء: {str(e)}")
        return False


def test_suppliers_api(cookies):
    """اختبار APIs الموردين"""
    print("🏭 اختبار APIs الموردين...")

    try:
        # اختبار الحصول على قائمة الموردين
        response = requests.get(
            f"{BASE_URL}/api/suppliers",
            cookies=cookies,
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                suppliers = data["suppliers"]
                print(f"✅ تم الحصول على {len(suppliers)} مورد")
                return True
            else:
                print(f"❌ فشل في الحصول على الموردين: {data['message']}")
                return False
        else:
            print(f"❌ خطأ في طلب الموردين: {response.status_code}")
            return False

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار APIs الموردين: {str(e)}")
        return False


def test_warehouses_api(cookies):
    """اختبار APIs المخازن"""
    print("🏭 اختبار APIs المخازن...")

    try:
        # اختبار الحصول على قائمة المخازن
        response = requests.get(
            f"{BASE_URL}/api/warehouses",
            cookies=cookies,
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                warehouses = data["warehouses"]
                print(f"✅ تم الحصول على {len(warehouses)} مخزن")

                # اختبار الحصول على منتجات مخزن محدد
                if warehouses:
                    warehouse_id = warehouses[0]["id"]
                    response = requests.get(
                        f"{BASE_URL}/api/warehouses/{warehouse_id}/products",
                        cookies=cookies,
                        timeout=5,
                    )

                    if response.status_code == 200:
                        products_data = response.json()
                        if products_data["success"]:
                            products = products_data["products"]
                            print(f"✅ المخزن يحتوي على {len(products)} منتج")
                            return True
                        else:
                            print(
                                f"❌ فشل في الحصول على منتجات المخزن: {products_data['message']}"
                            )
                            return False
                    else:
                        print(f"❌ خطأ في طلب منتجات المخزن: {response.status_code}")
                        return False
                else:
                    print("⚠️ لا توجد مخازن للاختبار")
                    return True
            else:
                print(f"❌ فشل في الحصول على المخازن: {data['message']}")
                return False
        else:
            print(f"❌ خطأ في طلب المخازن: {response.status_code}")
            return False

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار APIs المخازن: {str(e)}")
        return False


def test_stock_movements_api(cookies):
    """اختبار APIs حركات المخزون"""
    print("📈 اختبار APIs حركات المخزون...")

    try:
        # اختبار الحصول على حركات المخزون
        response = requests.get(
            f"{BASE_URL}/api/stock-movements",
            cookies=cookies,
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                movements = data["movements"]
                print(f"✅ تم الحصول على {len(movements)} حركة مخزون")
                return True
            else:
                print(f"❌ فشل في الحصول على حركات المخزون: {data['message']}")
                return False
        else:
            print(f"❌ خطأ في طلب حركات المخزون: {response.status_code}")
            return False

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار APIs حركات المخزون: {str(e)}")
        return False


def test_invoices_api(cookies):
    """اختبار APIs الفواتير"""
    print("🧾 اختبار APIs الفواتير...")

    try:
        # اختبار الحصول على قائمة الفواتير
        response = requests.get(
            f"{BASE_URL}/api/invoices",
            cookies=cookies,
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                invoices = data["invoices"]
                print(f"✅ تم الحصول على {len(invoices)} فاتورة")

                # اختبار الحصول على فاتورة محددة
                if invoices:
                    invoice_id = invoices[0]["id"]
                    response = requests.get(
                        f"{BASE_URL}/api/invoices/{invoice_id}",
                        cookies=cookies,
                        timeout=5,
                    )

                    if response.status_code == 200:
                        invoice_data = response.json()
                        if invoice_data["success"]:
                            invoice = invoice_data["invoice"]
                            print(
                                f"✅ تم الحصول على الفاتورة: {invoice['invoice_number']}"
                            )
                            print(f"   - النوع: {invoice['invoice_type']}")
                            print(f"   - المبلغ الإجمالي: {invoice['total_amount']}")
                            return True
                        else:
                            print(
                                f"❌ فشل في الحصول على الفاتورة: {invoice_data['message']}"
                            )
                            return False
                    else:
                        print(f"❌ خطأ في طلب الفاتورة: {response.status_code}")
                        return False
                else:
                    print("⚠️ لا توجد فواتير للاختبار")
                    return True
            else:
                print(f"❌ فشل في الحصول على الفواتير: {data['message']}")
                return False
        else:
            print(f"❌ خطأ في طلب الفواتير: {response.status_code}")
            return False

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"❌ خطأ في اختبار APIs الفواتير: {str(e)}")
        return False


def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🧪 سكريبت اختبار الخادم الموحد")
    print("=" * 60)

    # اختبار فحص الصحة
    if not test_health_check():
        print("❌ فشل في فحص صحة الخادم - توقف الاختبار")
        return

    # اختبار تسجيل الدخول
    cookies = test_login()
    if not cookies:
        print("❌ فشل في تسجيل الدخول - توقف الاختبار")
        return

    # اختبار الإحصائيات
    test_dashboard_stats(cookies)

    # اختبار APIs المنتجات
    test_products_api(cookies)

    # اختبار إنشاء منتج جديد
    test_create_product(cookies)

    # اختبار APIs العملاء
    test_customers_api(cookies)

    # اختبار APIs الموردين
    test_suppliers_api(cookies)

    # اختبار APIs المخازن
    test_warehouses_api(cookies)

    # اختبار APIs حركات المخزون
    test_stock_movements_api(cookies)

    # اختبار APIs الفواتير
    test_invoices_api(cookies)

    # اختبار تسجيل الخروج
    test_logout(cookies)

    print("\n🎉 تم الانتهاء من جميع الاختبارات!")


if __name__ == "__main__":
    main()
