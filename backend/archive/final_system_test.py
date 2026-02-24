#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبار شامل نهائي للنظام
Final Comprehensive System Test

يقوم بفحص واختبار جميع أجزاء النظام:
- الخادم الخلفي ونقاط النهاية
- الخادم الأمامي والاتصال
- قاعدة البيانات والبيانات
- التكامل بين الواجهات
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
        self.frontend_url = "http://localhost:5502"
        self.test_results = {
            'backend_tests': {},
            'frontend_tests': {},
            'integration_tests': {},
            'database_tests': {},
            'overall_status': 'UNKNOWN'
        }
        self.success_count = 0
        self.total_tests = 0
    
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_test(self, test_name, status, details=""):
        self.total_tests += 1
        if status == "PASS":
            self.success_count += 1
            print(f"✅ {test_name}")
        elif status == "FAIL":
            print(f"❌ {test_name}")
        else:
            print(f"⚠️  {test_name}")
        
        if details:
            print(f"   📋 {details}")
    
    def test_backend_endpoints(self):
        """اختبار نقاط النهاية في الخادم الخلفي"""
        self.print_header("اختبار الخادم الخلفي")
        
        # اختبار حالة الخادم
        try:
            response = requests.get(f"{self.backend_url}/api/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.print_test("حالة الخادم", "PASS", "الخادم يعمل بشكل طبيعي")
                    self.test_results['backend_tests']['status'] = True
                else:
                    self.print_test("حالة الخادم", "FAIL", "الخادم لا يرد بشكل صحيح")
                    self.test_results['backend_tests']['status'] = False
            else:
                self.print_test("حالة الخادم", "FAIL", f"كود الاستجابة: {response.status_code}")
                self.test_results['backend_tests']['status'] = False
        except Exception as e:
            self.print_test("حالة الخادم", "FAIL", f"خطأ في الاتصال: {str(e)}")
            self.test_results['backend_tests']['status'] = False
        
        # اختبار الفئات
        try:
            response = requests.get(f"{self.backend_url}/api/categories", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') is not False:
                    self.print_test("نقطة نهاية الفئات", "PASS", f"عدد الفئات: {len(data.get('categories', []))}")
                    self.test_results['backend_tests']['categories'] = True
                else:
                    self.print_test("نقطة نهاية الفئات", "FAIL", "فشل في جلب الفئات")
                    self.test_results['backend_tests']['categories'] = False
            else:
                self.print_test("نقطة نهاية الفئات", "FAIL", f"كود الاستجابة: {response.status_code}")
                self.test_results['backend_tests']['categories'] = False
        except Exception as e:
            self.print_test("نقطة نهاية الفئات", "FAIL", f"خطأ: {str(e)}")
            self.test_results['backend_tests']['categories'] = False
        
        # اختبار المستودعات
        try:
            response = requests.get(f"{self.backend_url}/api/warehouses", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') is not False:
                    self.print_test("نقطة نهاية المستودعات", "PASS", f"عدد المستودعات: {len(data.get('warehouses', []))}")
                    self.test_results['backend_tests']['warehouses'] = True
                else:
                    self.print_test("نقطة نهاية المستودعات", "FAIL", "فشل في جلب المستودعات")
                    self.test_results['backend_tests']['warehouses'] = False
            else:
                self.print_test("نقطة نهاية المستودعات", "FAIL", f"كود الاستجابة: {response.status_code}")
                self.test_results['backend_tests']['warehouses'] = False
        except Exception as e:
            self.print_test("نقطة نهاية المستودعات", "FAIL", f"خطأ: {str(e)}")
            self.test_results['backend_tests']['warehouses'] = False
        
        # اختبار المنتجات
        try:
            response = requests.get(f"{self.backend_url}/api/products", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') is not False:
                    self.print_test("نقطة نهاية المنتجات", "PASS", f"عدد المنتجات: {len(data.get('products', []))}")
                    self.test_results['backend_tests']['products'] = True
                else:
                    self.print_test("نقطة نهاية المنتجات", "FAIL", "فشل في جلب المنتجات")
                    self.test_results['backend_tests']['products'] = False
            else:
                self.print_test("نقطة نهاية المنتجات", "FAIL", f"كود الاستجابة: {response.status_code}")
                self.test_results['backend_tests']['products'] = False
        except Exception as e:
            self.print_test("نقطة نهاية المنتجات", "FAIL", f"خطأ: {str(e)}")
            self.test_results['backend_tests']['products'] = False
        
        # اختبار المستخدمين
        try:
            response = requests.get(f"{self.backend_url}/api/users", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') is not False:
                    self.print_test("نقطة نهاية المستخدمين", "PASS", f"عدد المستخدمين: {len(data.get('users', []))}")
                    self.test_results['backend_tests']['users'] = True
                else:
                    self.print_test("نقطة نهاية المستخدمين", "FAIL", "فشل في جلب المستخدمين")
                    self.test_results['backend_tests']['users'] = False
            else:
                self.print_test("نقطة نهاية المستخدمين", "FAIL", f"كود الاستجابة: {response.status_code}")
                self.test_results['backend_tests']['users'] = False
        except Exception as e:
            self.print_test("نقطة نهاية المستخدمين", "FAIL", f"خطأ: {str(e)}")
            self.test_results['backend_tests']['users'] = False
    
    def test_frontend_server(self):
        """اختبار الخادم الأمامي"""
        self.print_header("اختبار الخادم الأمامي")
        
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                self.print_test("الخادم الأمامي", "PASS", "الخادم يستجيب بشكل طبيعي")
                self.test_results['frontend_tests']['server'] = True
            else:
                self.print_test("الخادم الأمامي", "FAIL", f"كود الاستجابة: {response.status_code}")
                self.test_results['frontend_tests']['server'] = False
        except Exception as e:
            self.print_test("الخادم الأمامي", "FAIL", f"خطأ في الاتصال: {str(e)}")
            self.test_results['frontend_tests']['server'] = False
    
    def test_database_integrity(self):
        """اختبار سلامة قاعدة البيانات"""
        self.print_header("اختبار قاعدة البيانات")
        
        db_path = "backend/instance/inventory.db"
        if os.path.exists(db_path):
            self.print_test("وجود قاعدة البيانات", "PASS", f"الملف موجود: {db_path}")
            self.test_results['database_tests']['exists'] = True
            
            # فحص الجداول
            try:
                import sqlite3
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # فحص الجداول الأساسية
                tables = ['users', 'categories', 'warehouses', 'products']
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    self.print_test(f"جدول {table}", "PASS", f"عدد السجلات: {count}")
                    self.test_results['database_tests'][table] = True
                
                conn.close()
            except Exception as e:
                self.print_test("فحص الجداول", "FAIL", f"خطأ: {str(e)}")
                self.test_results['database_tests']['tables'] = False
        else:
            self.print_test("وجود قاعدة البيانات", "FAIL", "ملف قاعدة البيانات غير موجود")
            self.test_results['database_tests']['exists'] = False
    
    def test_integration(self):
        """اختبار التكامل بين الأجزاء"""
        self.print_header("اختبار التكامل")
        
        # اختبار إنشاء فئة جديدة
        try:
            test_category = {
                "name": f"فئة اختبار {int(time.time())}",
                "description": "فئة للاختبار"
            }
            
            response = requests.post(
                f"{self.backend_url}/api/categories",
                json=test_category,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.print_test("إنشاء فئة جديدة", "PASS", "تم إنشاء الفئة بنجاح")
                    self.test_results['integration_tests']['create_category'] = True
                else:
                    self.print_test("إنشاء فئة جديدة", "FAIL", data.get('error', 'خطأ غير معروف'))
                    self.test_results['integration_tests']['create_category'] = False
            else:
                self.print_test("إنشاء فئة جديدة", "FAIL", f"كود الاستجابة: {response.status_code}")
                self.test_results['integration_tests']['create_category'] = False
        except Exception as e:
            self.print_test("إنشاء فئة جديدة", "FAIL", f"خطأ: {str(e)}")
            self.test_results['integration_tests']['create_category'] = False
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        self.print_header("تقرير النتائج النهائي")
        
        success_rate = (self.success_count / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📊 إجمالي الاختبارات: {self.total_tests}")
        print(f"✅ الاختبارات الناجحة: {self.success_count}")
        print(f"❌ الاختبارات الفاشلة: {self.total_tests - self.success_count}")
        print(f"📈 معدل النجاح: {success_rate:.1f}%")
        
        if success_rate >= 80:
            self.test_results['overall_status'] = 'GOOD'
            print(f"\n🎉 النظام يعمل بشكل جيد!")
        elif success_rate >= 60:
            self.test_results['overall_status'] = 'FAIR'
            print(f"\n⚠️  النظام يعمل بشكل مقبول مع بعض المشاكل")
        else:
            self.test_results['overall_status'] = 'POOR'
            print(f"\n❌ النظام يحتاج إلى إصلاحات كبيرة")
        
        # حفظ التقرير
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'success_rate': success_rate,
            'total_tests': self.total_tests,
            'successful_tests': self.success_count,
            'failed_tests': self.total_tests - self.success_count,
            'test_results': self.test_results
        }
        
        with open('final_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 تم حفظ التقرير التفصيلي في: final_test_report.json")
        
        return success_rate >= 80

def main():
    print("🚀 بدء الاختبار الشامل النهائي للنظام...")
    print(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = SystemTester()
    
    # تشغيل جميع الاختبارات
    tester.test_backend_endpoints()
    tester.test_frontend_server()
    tester.test_database_integrity()
    tester.test_integration()
    
    # إنشاء التقرير النهائي
    success = tester.generate_report()
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
