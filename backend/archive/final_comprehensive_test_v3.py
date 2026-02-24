#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبار نهائي شامل للنظام - الإصدار الثالث
Final Comprehensive System Test - Version 3

هذا السكريبت يقوم بإجراء اختبار شامل ونهائي للنظام بأكمله
"""

import requests
import json
import time
import subprocess
import os
from datetime import datetime

class SystemTester:
    def __init__(self):
        self.backend_url = "http://localhost:5002"
        self.frontend_url = "http://localhost:5503"
        self.test_results = {
            'backend_tests': {},
            'frontend_tests': {},
            'integration_tests': {},
            'overall_score': 0,
            'timestamp': datetime.now().isoformat()
        }
        
    def test_backend_basic(self):
        """اختبار الوظائف الأساسية للخادم الخلفي"""
        print("🔧 اختبار الخادم الخلفي الأساسي...")
        
        tests = {
            'server_status': '/api/status',
            'health_check': '/api/health'
        }
        
        results = {}
        
        for test_name, endpoint in tests.items():
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    results[test_name] = {'status': 'PASS', 'code': response.status_code}
                    print(f"   ✅ {test_name}: نجح ({response.status_code})")
                else:
                    results[test_name] = {'status': 'FAIL', 'code': response.status_code}
                    print(f"   ❌ {test_name}: فشل ({response.status_code})")
            except Exception as e:
                results[test_name] = {'status': 'ERROR', 'error': str(e)}
                print(f"   ❌ {test_name}: خطأ - {e}")
        
        self.test_results['backend_tests']['basic'] = results
        return len([r for r in results.values() if r['status'] == 'PASS']) / len(results) * 100
    
    def test_backend_auth(self):
        """اختبار نظام المصادقة"""
        print("🔐 اختبار نظام المصادقة...")
        
        results = {}
        
        # اختبار تسجيل الدخول
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        try:
            response = requests.post(f"{self.backend_url}/api/auth/login", 
                                   json=login_data, timeout=10)
            if response.status_code == 200:
                results['login'] = {'status': 'PASS', 'code': response.status_code}
                print("   ✅ تسجيل الدخول: نجح")
                
                # محاولة الحصول على رمز الجلسة
                data = response.json()
                if 'session_token' in data:
                    results['session_token'] = {'status': 'PASS'}
                    print("   ✅ رمز الجلسة: متوفر")
                else:
                    results['session_token'] = {'status': 'FAIL'}
                    print("   ❌ رمز الجلسة: غير متوفر")
            else:
                results['login'] = {'status': 'FAIL', 'code': response.status_code}
                print(f"   ❌ تسجيل الدخول: فشل ({response.status_code})")
                results['session_token'] = {'status': 'SKIP'}
        except Exception as e:
            results['login'] = {'status': 'ERROR', 'error': str(e)}
            results['session_token'] = {'status': 'SKIP'}
            print(f"   ❌ تسجيل الدخول: خطأ - {e}")
        
        self.test_results['backend_tests']['auth'] = results
        return len([r for r in results.values() if r['status'] == 'PASS']) / len(results) * 100
    
    def test_backend_endpoints(self):
        """اختبار نقاط النهاية المختلفة"""
        print("🌐 اختبار نقاط النهاية...")
        
        endpoints = {
            'categories': '/api/categories',
            'products': '/api/products',
            'warehouses': '/api/warehouses',
            'users': '/api/users',
            'inventory': '/api/inventory',
            'dashboard': '/api/reports/dashboard'
        }
        
        results = {}
        
        for name, endpoint in endpoints.items():
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                if response.status_code in [200, 401]:  # 401 مقبول للنقاط المحمية
                    results[name] = {'status': 'PASS', 'code': response.status_code}
                    print(f"   ✅ {name}: متاح ({response.status_code})")
                else:
                    results[name] = {'status': 'FAIL', 'code': response.status_code}
                    print(f"   ❌ {name}: غير متاح ({response.status_code})")
            except Exception as e:
                results[name] = {'status': 'ERROR', 'error': str(e)}
                print(f"   ❌ {name}: خطأ - {e}")
        
        self.test_results['backend_tests']['endpoints'] = results
        return len([r for r in results.values() if r['status'] == 'PASS']) / len(results) * 100
    
    def test_frontend_basic(self):
        """اختبار الواجهة الأمامية الأساسية"""
        print("🖥️ اختبار الواجهة الأمامية...")
        
        results = {}
        
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                results['homepage'] = {'status': 'PASS', 'code': response.status_code}
                print("   ✅ الصفحة الرئيسية: متاحة")
                
                # فحص المحتوى
                content = response.text
                if 'نظام إدارة المخزون' in content or 'Inventory Management' in content:
                    results['content'] = {'status': 'PASS'}
                    print("   ✅ المحتوى: صحيح")
                else:
                    results['content'] = {'status': 'FAIL'}
                    print("   ❌ المحتوى: غير صحيح")
            else:
                results['homepage'] = {'status': 'FAIL', 'code': response.status_code}
                results['content'] = {'status': 'SKIP'}
                print(f"   ❌ الصفحة الرئيسية: غير متاحة ({response.status_code})")
        except Exception as e:
            results['homepage'] = {'status': 'ERROR', 'error': str(e)}
            results['content'] = {'status': 'SKIP'}
            print(f"   ❌ الواجهة الأمامية: خطأ - {e}")
        
        self.test_results['frontend_tests']['basic'] = results
        return len([r for r in results.values() if r['status'] == 'PASS']) / len(results) * 100
    
    def test_database_integrity(self):
        """اختبار سلامة قاعدة البيانات"""
        print("🗄️ اختبار سلامة قاعدة البيانات...")
        
        results = {}
        db_path = "backend/instance/inventory.db"
        
        try:
            import sqlite3
            
            if os.path.exists(db_path):
                results['db_exists'] = {'status': 'PASS'}
                print("   ✅ قاعدة البيانات: موجودة")
                
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # فحص الجداول الأساسية
                required_tables = ['users', 'roles', 'user_roles', 'categories', 
                                 'products', 'warehouses']
                
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                missing_tables = []
                for table in required_tables:
                    if table in existing_tables:
                        results[f'table_{table}'] = {'status': 'PASS'}
                        print(f"   ✅ جدول {table}: موجود")
                    else:
                        results[f'table_{table}'] = {'status': 'FAIL'}
                        missing_tables.append(table)
                        print(f"   ❌ جدول {table}: مفقود")
                
                # فحص البيانات الأساسية
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                if user_count > 0:
                    results['admin_user'] = {'status': 'PASS'}
                    print(f"   ✅ المستخدمين: {user_count} مستخدم")
                else:
                    results['admin_user'] = {'status': 'FAIL'}
                    print("   ❌ المستخدمين: لا يوجد مستخدمين")
                
                conn.close()
            else:
                results['db_exists'] = {'status': 'FAIL'}
                print("   ❌ قاعدة البيانات: غير موجودة")
                
        except Exception as e:
            results['db_error'] = {'status': 'ERROR', 'error': str(e)}
            print(f"   ❌ قاعدة البيانات: خطأ - {e}")
        
        self.test_results['integration_tests']['database'] = results
        return len([r for r in results.values() if r['status'] == 'PASS']) / len(results) * 100
    
    def test_system_integration(self):
        """اختبار تكامل النظام"""
        print("🔗 اختبار تكامل النظام...")
        
        results = {}
        
        # اختبار الاتصال بين الواجهة الأمامية والخلفية
        try:
            # محاولة الوصول للواجهة الأمامية
            frontend_response = requests.get(self.frontend_url, timeout=5)
            backend_response = requests.get(f"{self.backend_url}/api/status", timeout=5)
            
            if frontend_response.status_code == 200 and backend_response.status_code == 200:
                results['frontend_backend_connection'] = {'status': 'PASS'}
                print("   ✅ الاتصال بين الواجهات: يعمل")
            else:
                results['frontend_backend_connection'] = {'status': 'FAIL'}
                print("   ❌ الاتصال بين الواجهات: لا يعمل")
                
        except Exception as e:
            results['frontend_backend_connection'] = {'status': 'ERROR', 'error': str(e)}
            print(f"   ❌ الاتصال بين الواجهات: خطأ - {e}")
        
        # اختبار المنافذ
        import socket
        
        ports_to_check = [5002, 5503]
        for port in ports_to_check:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                
                if result == 0:
                    results[f'port_{port}'] = {'status': 'PASS'}
                    print(f"   ✅ المنفذ {port}: مفتوح")
                else:
                    results[f'port_{port}'] = {'status': 'FAIL'}
                    print(f"   ❌ المنفذ {port}: مغلق")
            except Exception as e:
                results[f'port_{port}'] = {'status': 'ERROR', 'error': str(e)}
                print(f"   ❌ المنفذ {port}: خطأ - {e}")
        
        self.test_results['integration_tests']['system'] = results
        return len([r for r in results.values() if r['status'] == 'PASS']) / len(results) * 100
    
    def calculate_overall_score(self):
        """حساب النتيجة الإجمالية"""
        all_results = []
        
        # جمع جميع النتائج
        for category in self.test_results.values():
            if isinstance(category, dict):
                for test_group in category.values():
                    if isinstance(test_group, dict):
                        for result in test_group.values():
                            if isinstance(result, dict) and 'status' in result:
                                all_results.append(result['status'])
        
        if not all_results:
            return 0
        
        pass_count = all_results.count('PASS')
        total_count = len(all_results)
        
        return (pass_count / total_count) * 100
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🧪 بدء الاختبار الشامل النهائي للنظام")
        print("=" * 70)
        
        scores = []
        
        # اختبارات الخادم الخلفي
        print("\n🔧 اختبارات الخادم الخلفي:")
        print("-" * 40)
        scores.append(self.test_backend_basic())
        scores.append(self.test_backend_auth())
        scores.append(self.test_backend_endpoints())
        
        # اختبارات الواجهة الأمامية
        print("\n🖥️ اختبارات الواجهة الأمامية:")
        print("-" * 40)
        scores.append(self.test_frontend_basic())
        
        # اختبارات التكامل
        print("\n🔗 اختبارات التكامل:")
        print("-" * 40)
        scores.append(self.test_database_integrity())
        scores.append(self.test_system_integration())
        
        # حساب النتيجة الإجمالية
        overall_score = self.calculate_overall_score()
        self.test_results['overall_score'] = overall_score
        
        # عرض النتائج
        print("\n" + "=" * 70)
        print("📊 النتائج النهائية:")
        print(f"🎯 النتيجة الإجمالية: {overall_score:.1f}%")
        
        if overall_score >= 90:
            print("🎉 ممتاز! النظام يعمل بشكل مثالي")
        elif overall_score >= 75:
            print("✅ جيد! النظام يعمل بشكل جيد مع بعض المشاكل البسيطة")
        elif overall_score >= 50:
            print("⚠️ متوسط! النظام يعمل جزئياً ويحتاج إصلاحات")
        else:
            print("❌ ضعيف! النظام يحتاج إصلاحات جذرية")
        
        # حفظ التقرير
        self.save_report()
        
        return overall_score
    
    def save_report(self):
        """حفظ تقرير الاختبار"""
        report_file = "final_comprehensive_test_report_v3.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            print(f"\n📄 تم حفظ التقرير في: {report_file}")
        except Exception as e:
            print(f"❌ خطأ في حفظ التقرير: {e}")

def main():
    """الدالة الرئيسية"""
    tester = SystemTester()
    
    # انتظار قصير للتأكد من استقرار الخوادم
    print("⏳ انتظار استقرار الخوادم...")
    time.sleep(3)
    
    # تشغيل الاختبارات
    final_score = tester.run_all_tests()
    
    # تحديد حالة النجاح
    if final_score >= 80:
        print(f"\n🎉 تم تحقيق الهدف! النظام يعمل بنسبة {final_score:.1f}%")
        exit(0)
    else:
        print(f"\n⚠️ لم يتم تحقيق الهدف بعد. النظام يعمل بنسبة {final_score:.1f}%")
        exit(1)

if __name__ == "__main__":
    main()
