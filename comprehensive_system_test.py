#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبار شامل للنظام
Comprehensive System Test

يختبر جميع المهام والوظائف:
- API endpoints
- قاعدة البيانات
- الأمان
- الوظائف الأساسية
"""

import requests
import json
import time
import os
from datetime import datetime

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_error(message):
    print(f"❌ {message}")

class SystemTester:
    def __init__(self):
        self.backend_url = "http://localhost:5002"
        self.frontend_url = "http://localhost:5502"
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'warnings': 0,
            'details': []
        }
        self.auth_token = None
    
    def add_result(self, test_name, status, message, details=None):
        """إضافة نتيجة اختبار"""
        self.test_results['total_tests'] += 1
        
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        
        if status == 'PASS':
            self.test_results['passed_tests'] += 1
            print_success(f"{test_name}: {message}")
        elif status == 'FAIL':
            self.test_results['failed_tests'] += 1
            print_error(f"{test_name}: {message}")
        elif status == 'WARN':
            self.test_results['warnings'] += 1
            print_warning(f"{test_name}: {message}")
        
        self.test_results['details'].append(result)
    
    def test_backend_health(self):
        """اختبار صحة الخادم الخلفي"""
        print_step("اختبار صحة الخادم الخلفي...")
        
        try:
            response = requests.get(f"{self.backend_url}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.add_result(
                    "Backend Health",
                    "PASS",
                    f"الخادم يعمل - الإصدار {data.get('version', 'غير محدد')}",
                    data
                )
                return True
            else:
                self.add_result(
                    "Backend Health",
                    "FAIL",
                    f"رمز الخطأ: {response.status_code}"
                )
                return False
        except Exception as e:
            self.add_result(
                "Backend Health",
                "FAIL",
                f"فشل الاتصال: {str(e)}"
            )
            return False
    
    def test_api_endpoints(self):
        """اختبار نقاط النهاية الأساسية"""
        print_step("اختبار نقاط النهاية الأساسية...")
        
        endpoints = [
            ("/api/health", "GET", "فحص الصحة"),
            ("/api/system/status", "GET", "حالة النظام"),
            ("/api/products", "GET", "قائمة المنتجات"),
            ("/api/customers", "GET", "قائمة العملاء"),
            ("/api/suppliers", "GET", "قائمة الموردين"),
            ("/api/categories", "GET", "قائمة الفئات"),
            ("/api/warehouses", "GET", "قائمة المستودعات"),
            ("/api/inventory", "GET", "المخزون"),
            ("/api/reports/sales", "GET", "تقارير المبيعات"),
            ("/api/users", "GET", "قائمة المستخدمين")
        ]
        
        passed = 0
        for endpoint, method, description in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                
                if response.status_code in [200, 201]:
                    self.add_result(
                        f"API {endpoint}",
                        "PASS",
                        f"{description} - {response.status_code}"
                    )
                    passed += 1
                elif response.status_code == 401:
                    self.add_result(
                        f"API {endpoint}",
                        "WARN",
                        f"{description} - يتطلب مصادقة"
                    )
                else:
                    self.add_result(
                        f"API {endpoint}",
                        "FAIL",
                        f"{description} - خطأ {response.status_code}"
                    )
            except Exception as e:
                self.add_result(
                    f"API {endpoint}",
                    "FAIL",
                    f"{description} - خطأ: {str(e)}"
                )
        
        return passed
    
    def test_authentication(self):
        """اختبار نظام المصادقة"""
        print_step("اختبار نظام المصادقة...")
        
        # اختبار تسجيل الدخول
        login_data = {
            "username": "admin",
            "password": "u-fZEk2jsOQN3bwvFrj93A"
        }
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    self.auth_token = data['token']
                    self.add_result(
                        "Authentication Login",
                        "PASS",
                        "تسجيل الدخول نجح"
                    )
                    return True
                else:
                    self.add_result(
                        "Authentication Login",
                        "FAIL",
                        "لم يتم إرجاع token"
                    )
            else:
                self.add_result(
                    "Authentication Login",
                    "FAIL",
                    f"فشل تسجيل الدخول - {response.status_code}"
                )
        except Exception as e:
            self.add_result(
                "Authentication Login",
                "FAIL",
                f"خطأ في تسجيل الدخول: {str(e)}"
            )
        
        return False
    
    def test_database_operations(self):
        """اختبار عمليات قاعدة البيانات"""
        print_step("اختبار عمليات قاعدة البيانات...")
        
        # اختبار إنشاء منتج جديد
        headers = {}
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
        
        test_product = {
            "name": "منتج اختبار",
            "description": "وصف منتج الاختبار",
            "price": 100.0,
            "category_id": 1,
            "sku": f"TEST-{int(time.time())}"
        }
        
        try:
            # إنشاء منتج
            response = requests.post(
                f"{self.backend_url}/api/products",
                json=test_product,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                product_data = response.json()
                product_id = product_data.get('id')
                
                self.add_result(
                    "Database Create",
                    "PASS",
                    f"تم إنشاء منتج - ID: {product_id}"
                )
                
                # اختبار قراءة المنتج
                if product_id:
                    read_response = requests.get(
                        f"{self.backend_url}/api/products/{product_id}",
                        headers=headers,
                        timeout=5
                    )
                    
                    if read_response.status_code == 200:
                        self.add_result(
                            "Database Read",
                            "PASS",
                            "تم قراءة المنتج بنجاح"
                        )
                    else:
                        self.add_result(
                            "Database Read",
                            "FAIL",
                            f"فشل قراءة المنتج - {read_response.status_code}"
                        )
                
                return True
            else:
                self.add_result(
                    "Database Create",
                    "FAIL",
                    f"فشل إنشاء المنتج - {response.status_code}"
                )
        except Exception as e:
            self.add_result(
                "Database Create",
                "FAIL",
                f"خطأ في قاعدة البيانات: {str(e)}"
            )
        
        return False
    
    def test_security_features(self):
        """اختبار الميزات الأمنية"""
        print_step("اختبار الميزات الأمنية...")
        
        # اختبار الوصول بدون مصادقة
        try:
            response = requests.get(f"{self.backend_url}/api/users", timeout=5)
            if response.status_code == 401:
                self.add_result(
                    "Security Unauthorized",
                    "PASS",
                    "الحماية من الوصول غير المصرح تعمل"
                )
            else:
                self.add_result(
                    "Security Unauthorized",
                    "WARN",
                    f"قد تكون هناك مشكلة أمنية - {response.status_code}"
                )
        except Exception as e:
            self.add_result(
                "Security Unauthorized",
                "FAIL",
                f"خطأ في اختبار الأمان: {str(e)}"
            )
        
        # اختبار CORS headers
        try:
            response = requests.options(f"{self.backend_url}/api/health", timeout=5)
            headers = response.headers
            
            if 'Access-Control-Allow-Origin' in headers:
                self.add_result(
                    "Security CORS",
                    "PASS",
                    "إعدادات CORS موجودة"
                )
            else:
                self.add_result(
                    "Security CORS",
                    "WARN",
                    "إعدادات CORS قد تكون مفقودة"
                )
        except Exception as e:
            self.add_result(
                "Security CORS",
                "FAIL",
                f"خطأ في اختبار CORS: {str(e)}"
            )
    
    def test_reports_functionality(self):
        """اختبار وظائف التقارير"""
        print_step("اختبار وظائف التقارير...")
        
        headers = {}
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
        
        report_endpoints = [
            "/api/reports/sales/daily",
            "/api/reports/inventory/summary",
            "/api/reports/customers/analysis",
            "/api/reports/financial/summary"
        ]
        
        for endpoint in report_endpoints:
            try:
                response = requests.get(
                    f"{self.backend_url}{endpoint}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    self.add_result(
                        f"Report {endpoint.split('/')[-1]}",
                        "PASS",
                        "تقرير يعمل بنجاح"
                    )
                elif response.status_code == 401:
                    self.add_result(
                        f"Report {endpoint.split('/')[-1]}",
                        "WARN",
                        "يتطلب مصادقة"
                    )
                else:
                    self.add_result(
                        f"Report {endpoint.split('/')[-1]}",
                        "FAIL",
                        f"خطأ {response.status_code}"
                    )
            except Exception as e:
                self.add_result(
                    f"Report {endpoint.split('/')[-1]}",
                    "FAIL",
                    f"خطأ: {str(e)}"
                )
    
    def test_frontend_availability(self):
        """اختبار توفر الواجهة الأمامية"""
        print_step("اختبار توفر الواجهة الأمامية...")
        
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                self.add_result(
                    "Frontend Availability",
                    "PASS",
                    "الواجهة الأمامية متاحة"
                )
                return True
            else:
                self.add_result(
                    "Frontend Availability",
                    "FAIL",
                    f"الواجهة الأمامية غير متاحة - {response.status_code}"
                )
        except Exception as e:
            self.add_result(
                "Frontend Availability",
                "WARN",
                f"الواجهة الأمامية غير متاحة: {str(e)}"
            )
        
        return False
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        report = {
            'test_summary': {
                'total_tests': self.test_results['total_tests'],
                'passed_tests': self.test_results['passed_tests'],
                'failed_tests': self.test_results['failed_tests'],
                'warnings': self.test_results['warnings'],
                'success_rate': round((self.test_results['passed_tests'] / self.test_results['total_tests']) * 100, 2) if self.test_results['total_tests'] > 0 else 0
            },
            'test_details': self.test_results['details'],
            'timestamp': datetime.now().isoformat(),
            'system_info': {
                'backend_url': self.backend_url,
                'frontend_url': self.frontend_url
            }
        }
        
        # حفظ التقرير
        with open('comprehensive_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🧪 بدء الاختبار الشامل للنظام...")
        print("=" * 60)
        
        # اختبار الخادم الخلفي
        backend_healthy = self.test_backend_health()
        
        if backend_healthy:
            # اختبار نقاط النهاية
            self.test_api_endpoints()
            
            # اختبار المصادقة
            auth_success = self.test_authentication()
            
            # اختبار قاعدة البيانات
            if auth_success:
                self.test_database_operations()
            
            # اختبار الأمان
            self.test_security_features()
            
            # اختبار التقارير
            self.test_reports_functionality()
        
        # اختبار الواجهة الأمامية
        self.test_frontend_availability()
        
        # إنشاء التقرير
        report = self.generate_report()
        
        print("=" * 60)
        print("📊 ملخص النتائج:")
        print(f"   إجمالي الاختبارات: {report['test_summary']['total_tests']}")
        print(f"   نجح: {report['test_summary']['passed_tests']}")
        print(f"   فشل: {report['test_summary']['failed_tests']}")
        print(f"   تحذيرات: {report['test_summary']['warnings']}")
        print(f"   معدل النجاح: {report['test_summary']['success_rate']}%")
        print(f"📄 التقرير محفوظ في: comprehensive_test_report.json")
        
        return report

def main():
    tester = SystemTester()
    report = tester.run_all_tests()
    
    # تحديد حالة النظام العامة
    success_rate = report['test_summary']['success_rate']
    
    if success_rate >= 90:
        print_success(f"🎉 النظام في حالة ممتازة! ({success_rate}%)")
    elif success_rate >= 75:
        print_warning(f"⚠️ النظام في حالة جيدة مع بعض المشاكل ({success_rate}%)")
    else:
        print_error(f"❌ النظام يحتاج إصلاحات ({success_rate}%)")

if __name__ == "__main__":
    main()
