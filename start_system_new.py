#!/usr/bin/env python3
"""
تشغيل نظام إدارة المخزون الزراعي - الإصدار الجديد
"""

import sys
import os
from datetime import datetime


def check_python_version():
    """فحص إصدار Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} مدعوم")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} غير مدعوم")
        print("💡 يتطلب Python 3.7 أو أحدث")
        return False


def test_basic_imports():
    """اختبار الاستيرادات الأساسية"""
    print("🔍 اختبار الاستيرادات الأساسية...")

    try:
        import json
        print("✅ json متوفر")
    except ImportError:
        print("❌ json غير متوفر")
        return False

    try:
        import datetime
        print("✅ datetime متوفر")
    except ImportError:
        print("❌ datetime غير متوفر")
        return False

    try:
        import http.server
        print("✅ http.server متوفر")
    except ImportError:
        print("❌ http.server غير متوفر")
        return False

    return True


def start_basic_http_server():
    """تشغيل خادم HTTP أساسي"""
    try:
        import http.server
        import socketserver
        import json
        from urllib.parse import urlparse, parse_qs

        class InventoryHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                parsed_path = urlparse(self.path)

                if parsed_path.path == '/api/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()

                    response = {
                        'status': 'healthy',
                        'message': 'نظام إدارة المخزون يعمل بنجاح',
                        'timestamp': datetime.now().isoformat(),
                        'version': '1.0.0',
                        'server': 'Basic HTTP Server'
                    }

                    response_json = json.dumps(response, ensure_ascii=False)
                    self.wfile.write(response_json.encode('utf-8'))

                elif parsed_path.path == '/api/test':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()

                    response = {
                        'success': True,
                        'message': 'اختبار الخادم نجح',
                        'data': {
                            'server': 'Basic HTTP',
                            'status': 'running',
                            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'endpoints': [
                                '/api/health',
                                '/api/test',
                                '/api/products',
                                '/api/dashboard'
                            ]
                        }
                    }

                    response_json = json.dumps(response, ensure_ascii=False)
                    self.wfile.write(response_json.encode('utf-8'))

                elif parsed_path.path == '/api/products':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()

                    products = [
                        {
                            'id': 1,
                            'name': 'بذور طماطم هجين',
                            'sku': 'TOM-HYB-001',
                            'category': 'بذور',
                            'price': 35.00,
                            'stock': 150,
                            'status': 'متوفر'
                        },
                        {
                            'id': 2,
                            'name': 'سماد NPK متوازن',
                            'sku': 'NPK-BAL-001',
                            'category': 'أسمدة',
                            'price': 60.00,
                            'stock': 75,
                            'status': 'متوفر'
                        },
                        {
                            'id': 3,
                            'name': 'مبيد حشري طبيعي',
                            'sku': 'INS-NAT-001',
                            'category': 'مبيدات',
                            'price': 110.00,
                            'stock': 50,
                            'status': 'متوفر'
                        }
                    ]

                    response = {
                        'success': True,
                        'data': products,
                        'total': len(products),
                        'message': 'تم تحميل المنتجات بنجاح'
                    }

                    response_json = json.dumps(response, ensure_ascii=False)
                    self.wfile.write(response_json.encode('utf-8'))

                elif parsed_path.path == '/api/dashboard':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()

                    dashboard_data = {
                        'success': True,
                        'data': {
                            'summary': {
                                'total_products': 3,
                                'total_value': 23275.0,
                                'low_stock_alerts': 0,
                                'pending_orders': 5
                            },
                            'recent_activities': [
                                {'action': 'إضافة منتج جديد',
                                    'time': '10:30 ص'},
                                {'action': 'تحديث المخزون', 'time': '09:15 ص'},
                                {'action': 'فاتورة مبيعات جديدة',
                                    'time': '08:45 ص'}
                            ]
                        },
                        'message': 'تم تحميل بيانات لوحة التحكم بنجاح'
                    }

                    response_json = json.dumps(dashboard_data, ensure_ascii=False)
                    self.wfile.write(response_json.encode('utf-8'))

                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()

                    response = {
                        'success': False,
                        'error': 'المسار غير موجود',
                        'available_endpoints': [
                            '/api/health',
                            '/api/test',
                            '/api/products',
                            '/api/dashboard'
                        ]
                    }

                    response_json = json.dumps(response, ensure_ascii=False)
                    self.wfile.write(response_json.encode('utf-8'))

            def log_message(self, format, *args):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

        PORT = 8001
        with socketserver.TCPServer(("", PORT), InventoryHandler) as httpd:
            print("🚀 تم تشغيل الخادم الأساسي بنجاح!")
            print(f"🔗 الخادم متاح على: http://localhost:{PORT}")
            print(f"📋 فحص الحالة: http://localhost:{PORT}/api/health")
            print(f"🧪 اختبار: http://localhost:{PORT}/api/test")
            print(f"📦 المنتجات: http://localhost:{PORT}/api/products")
            print(f"📊 لوحة التحكم: http://localhost:{PORT}/api/dashboard")
            print("=" * 50)
            print("اضغط Ctrl+C لإيقاف الخادم")
            print("=" * 50)

            httpd.serve_forever()

    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return False


def main():
    """الدالة الرئيسية"""
    print("🌾 نظام إدارة المخزون الزراعي - الإصدار الجديد")
    print("=" * 50)
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"⏰ الوقت: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)

    # فحص إصدار Python
    if not check_python_version():
        return

    # اختبار الاستيرادات الأساسية
    if not test_basic_imports():
        print("❌ فشل في اختبار الاستيرادات الأساسية")
        return

    print("\n✅ جميع الفحوصات نجحت!")
    print("🚀 بدء تشغيل الخادم...")

    # تشغيل الخادم
    start_basic_http_server()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 تم إيقاف الخادم بواسطة المستخدم")
        print("👋 شكراً لاستخدام نظام إدارة المخزون")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()
