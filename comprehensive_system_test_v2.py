#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبار شامل للنظام - الإصدار الثاني
Comprehensive System Test v2

يقوم بإجراء اختبار شامل لجميع أجزاء النظام:
- فحص الكود باستخدام flake8
- اختبار الخادم الخلفي
- اختبار الواجهة الأمامية
- اختبار قاعدة البيانات
- اختبار نقاط النهاية الجديدة
- اختبار المصادقة
"""

import requests
import json
import time
import subprocess
import os
from pathlib import Path
import sqlite3
from datetime import datetime

class SystemTester:
    def __init__(self):
        self.backend_url = "http://localhost:5002"
        self.frontend_url = "http://localhost:5502"
        self.test_results = {
            'code_quality': {},
            'backend': {},
            'frontend': {},
            'database': {},
            'authentication': {},
            'endpoints': {},
            'overall_status': 'unknown'
        }
        self.auth_token = None
    
    def print_step(self, message):
        print(f"📋 {message}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def print_warning(self, message):
        print(f"⚠️  {message}")
    
    def test_code_quality(self):
        """فحص جودة الكود"""
        self.print_step("فحص جودة الكود...")
        
        try:
            # فحص الكود الخلفي
            result = subprocess.run([
                'python3', '-m', 'flake8', 'backend/src/',
                '--max-line-length=120',
                '--ignore=E501,W503,E402'
            ], capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                self.test_results['code_quality']['backend'] = 'passed'
                self.print_success("فحص الكود الخلفي: نجح")
            else:
                self.test_results['code_quality']['backend'] = 'failed'
                self.print_warning(f"فحص الكود الخلفي: مشاكل موجودة\\n{result.stdout}")
            
            # فحص ملفات Python الأخرى
            python_files = list(Path('.').glob('*.py'))
            if python_files:
                result = subprocess.run([
                    'python3', '-m', 'flake8'
                ] + [str(f) for f in python_files] + [
                    '--max-line-length=120',
                    '--ignore=E501,W503,E402'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.test_results['code_quality']['scripts'] = 'passed'
                    self.print_success("فحص السكريبتات: نجح")
                else:
                    self.test_results['code_quality']['scripts'] = 'warning'
                    self.print_warning("فحص السكريبتات: مشاكل بسيطة")
            
        except Exception as e:
            self.test_results['code_quality']['error'] = str(e)
            self.print_error(f"خطأ في فحص جودة الكود: {e}")
    
    def test_database(self):
        """اختبار قاعدة البيانات"""
        self.print_step("اختبار قاعدة البيانات...")
        
        try:
            db_path = Path("backend/instance/inventory.db")
            if not db_path.exists():
                self.test_results['database']['status'] = 'missing'
                self.print_error("قاعدة البيانات غير موجودة")
                return
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # فحص الجداول المطلوبة
            required_tables = [
                'users', 'products', 'customers', 'suppliers',
                'categories', 'warehouses', 'inventory'
            ]
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            missing_tables = [t for t in required_tables if t not in existing_tables]
            
            if missing_tables:
                self.test_results['database']['missing_tables'] = missing_tables
                self.print_warning(f"جداول مفقودة: {missing_tables}")
            else:
                self.test_results['database']['tables'] = 'complete'
                self.print_success("جميع الجداول موجودة")
            
            # فحص المستخدم الإداري
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]
            
            if admin_count > 0:
                self.test_results['database']['admin_user'] = 'exists'
                self.print_success("المستخدم الإداري موجود")
            else:
                self.test_results['database']['admin_user'] = 'missing'
                self.print_warning("المستخدم الإداري غير موجود")
            
            # فحص البيانات الأساسية
            cursor.execute("SELECT COUNT(*) FROM categories")
            categories_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM warehouses")
            warehouses_count = cursor.fetchone()[0]
            
            self.test_results['database']['data'] = {
                'categories': categories_count,
                'warehouses': warehouses_count
            }
            
            if categories_count > 0 and warehouses_count > 0:
                self.print_success("البيانات الأساسية موجودة")
            else:
                self.print_warning("البيانات الأساسية ناقصة")
            
            conn.close()
            self.test_results['database']['status'] = 'healthy'
            
        except Exception as e:
            self.test_results['database']['error'] = str(e)
            self.print_error(f"خطأ في اختبار قاعدة البيانات: {e}")
    
    def test_backend_server(self):
        """اختبار الخادم الخلفي"""
        self.print_step("اختبار الخادم الخلفي...")
        
        try:
            # اختبار الاتصال الأساسي
            response = requests.get(f"{self.backend_url}/api/health", timeout=10)
            
            if response.status_code == 200:
                self.test_results['backend']['health'] = 'healthy'
                self.print_success("الخادم الخلفي يعمل")
            else:
                self.test_results['backend']['health'] = 'unhealthy'
                self.print_error(f"الخادم الخلفي لا يستجيب: {response.status_code}")
                return
            
            # اختبار نقاط النهاية الجديدة
            endpoints_to_test = [
                '/api/categories',
                '/api/warehouses', 
                '/api/users',
                '/api/inventory',
                '/api/reports/dashboard'
            ]
            
            working_endpoints = []
            failed_endpoints = []
            
            for endpoint in endpoints_to_test:
                try:
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                    if response.status_code in [200, 401]:  # 401 يعني أن النقطة موجودة لكن تحتاج مصادقة
                        working_endpoints.append(endpoint)
                    else:
                        failed_endpoints.append(f"{endpoint} ({response.status_code})")
                except Exception as e:
                    failed_endpoints.append(f"{endpoint} (خطأ: {str(e)})")
            
            self.test_results['backend']['endpoints'] = {
                'working': working_endpoints,
                'failed': failed_endpoints
            }
            
            if len(working_endpoints) >= len(endpoints_to_test) * 0.8:
                self.print_success(f"نقاط النهاية تعمل: {len(working_endpoints)}/{len(endpoints_to_test)}")
            else:
                self.print_warning(f"بعض نقاط النهاية لا تعمل: {failed_endpoints}")
            
        except Exception as e:
            self.test_results['backend']['error'] = str(e)
            self.print_error(f"خطأ في اختبار الخادم الخلفي: {e}")
    
    def test_authentication(self):
        """اختبار نظام المصادقة"""
        self.print_step("اختبار نظام المصادقة...")
        
        try:
            # محاولة تسجيل الدخول
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            
            response = requests.post(
                f"{self.backend_url}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'token' in data.get('data', {}):
                    self.auth_token = data['data']['token']
                    self.test_results['authentication']['login'] = 'success'
                    self.print_success("تسجيل الدخول نجح")
                    
                    # اختبار التحقق من الرمز
                    headers = {'Authorization': f'Bearer {self.auth_token}'}
                    verify_response = requests.get(
                        f"{self.backend_url}/api/auth/verify",
                        headers=headers,
                        timeout=5
                    )
                    
                    if verify_response.status_code == 200:
                        self.test_results['authentication']['token_verification'] = 'success'
                        self.print_success("التحقق من الرمز نجح")
                    else:
                        self.test_results['authentication']['token_verification'] = 'failed'
                        self.print_warning("التحقق من الرمز فشل")
                else:
                    self.test_results['authentication']['login'] = 'failed'
                    self.print_error("تسجيل الدخول فشل: استجابة غير صحيحة")
            else:
                self.test_results['authentication']['login'] = 'failed'
                self.print_error(f"تسجيل الدخول فشل: {response.status_code}")
                
        except Exception as e:
            self.test_results['authentication']['error'] = str(e)
            self.print_error(f"خطأ في اختبار المصادقة: {e}")
    
    def test_frontend_server(self):
        """اختبار الخادم الأمامي"""
        self.print_step("اختبار الخادم الأمامي...")
        
        try:
            response = requests.get(self.frontend_url, timeout=10)
            
            if response.status_code == 200:
                self.test_results['frontend']['status'] = 'working'
                self.print_success("الخادم الأمامي يعمل")
                
                # فحص محتوى الصفحة
                content = response.text
                if 'React' in content or 'Vite' in content or 'app' in content.lower():
                    self.test_results['frontend']['content'] = 'valid'
                    self.print_success("محتوى الواجهة الأمامية صحيح")
                else:
                    self.test_results['frontend']['content'] = 'suspicious'
                    self.print_warning("محتوى الواجهة الأمامية قد يكون غير صحيح")
            else:
                self.test_results['frontend']['status'] = 'failed'
                self.print_error(f"الخادم الأمامي لا يعمل: {response.status_code}")
                
        except Exception as e:
            self.test_results['frontend']['error'] = str(e)
            self.print_error(f"خطأ في اختبار الخادم الأمامي: {e}")
    
    def test_protected_endpoints(self):
        """اختبار نقاط النهاية المحمية"""
        if not self.auth_token:
            self.print_warning("لا يمكن اختبار نقاط النهاية المحمية بدون رمز مصادقة")
            return
        
        self.print_step("اختبار نقاط النهاية المحمية...")
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        protected_endpoints = [
            '/api/categories',
            '/api/warehouses',
            '/api/users',
            '/api/inventory',
            '/api/inventory/summary',
            '/api/reports/dashboard'
        ]
        
        working_protected = []
        failed_protected = []
        
        for endpoint in protected_endpoints:
            try:
                response = requests.get(
                    f"{self.backend_url}{endpoint}",
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 200:
                    working_protected.append(endpoint)
                else:
                    failed_protected.append(f"{endpoint} ({response.status_code})")
                    
            except Exception as e:
                failed_protected.append(f"{endpoint} (خطأ: {str(e)})")
        
        self.test_results['endpoints']['protected'] = {
            'working': working_protected,
            'failed': failed_protected
        }
        
        if len(working_protected) >= len(protected_endpoints) * 0.7:
            self.print_success(f"نقاط النهاية المحمية تعمل: {len(working_protected)}/{len(protected_endpoints)}")
        else:
            self.print_warning(f"بعض نقاط النهاية المحمية لا تعمل: {failed_protected}")
    
    def calculate_overall_score(self):
        """حساب النتيجة الإجمالية"""
        scores = []
        
        # نتيجة جودة الكود
        if self.test_results['code_quality'].get('backend') == 'passed':
            scores.append(20)
        elif self.test_results['code_quality'].get('backend') == 'failed':
            scores.append(10)
        
        # نتيجة قاعدة البيانات
        if self.test_results['database'].get('status') == 'healthy':
            scores.append(20)
        elif 'error' not in self.test_results['database']:
            scores.append(10)
        
        # نتيجة الخادم الخلفي
        if self.test_results['backend'].get('health') == 'healthy':
            scores.append(25)
        
        # نتيجة المصادقة
        if self.test_results['authentication'].get('login') == 'success':
            scores.append(15)
        
        # نتيجة الخادم الأمامي
        if self.test_results['frontend'].get('status') == 'working':
            scores.append(20)
        
        total_score = sum(scores)
        
        if total_score >= 90:
            self.test_results['overall_status'] = 'excellent'
        elif total_score >= 70:
            self.test_results['overall_status'] = 'good'
        elif total_score >= 50:
            self.test_results['overall_status'] = 'fair'
        else:
            self.test_results['overall_status'] = 'poor'
        
        self.test_results['overall_score'] = total_score
        
        return total_score
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🧪 بدء الاختبار الشامل للنظام...")
        print("=" * 60)
        
        # فحص جودة الكود
        self.test_code_quality()
        
        # اختبار قاعدة البيانات
        self.test_database()
        
        # اختبار الخادم الخلفي
        self.test_backend_server()
        
        # اختبار المصادقة
        self.test_authentication()
        
        # اختبار الخادم الأمامي
        self.test_frontend_server()
        
        # اختبار نقاط النهاية المحمية
        self.test_protected_endpoints()
        
        # حساب النتيجة الإجمالية
        score = self.calculate_overall_score()
        
        print("=" * 60)
        print(f"📊 النتيجة الإجمالية: {score}/100")
        print(f"🎯 حالة النظام: {self.test_results['overall_status']}")
        
        # حفظ التقرير
        self.save_report()
        
        return self.test_results
    
    def save_report(self):
        """حفظ تقرير الاختبار"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'test_results': self.test_results,
            'summary': {
                'overall_score': self.test_results.get('overall_score', 0),
                'overall_status': self.test_results.get('overall_status', 'unknown'),
                'recommendations': self.generate_recommendations()
            }
        }
        
        with open('comprehensive_test_report_v2.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        self.print_success("تم حفظ تقرير الاختبار في comprehensive_test_report_v2.json")
    
    def generate_recommendations(self):
        """إنشاء توصيات للتحسين"""
        recommendations = []
        
        if self.test_results['code_quality'].get('backend') == 'failed':
            recommendations.append("إصلاح مشاكل جودة الكود في الخادم الخلفي")
        
        if self.test_results['database'].get('admin_user') == 'missing':
            recommendations.append("إنشاء مستخدم إداري في قاعدة البيانات")
        
        if self.test_results['backend'].get('health') != 'healthy':
            recommendations.append("إصلاح مشاكل الخادم الخلفي")
        
        if self.test_results['authentication'].get('login') != 'success':
            recommendations.append("إصلاح نظام المصادقة")
        
        if self.test_results['frontend'].get('status') != 'working':
            recommendations.append("إصلاح الخادم الأمامي")
        
        failed_endpoints = self.test_results.get('endpoints', {}).get('protected', {}).get('failed', [])
        if failed_endpoints:
            recommendations.append(f"إصلاح نقاط النهاية التالية: {failed_endpoints}")
        
        return recommendations

def main():
    tester = SystemTester()
    results = tester.run_all_tests()
    
    print("\\n📋 ملخص النتائج:")
    print(f"   - جودة الكود: {results['code_quality']}")
    print(f"   - قاعدة البيانات: {results['database'].get('status', 'unknown')}")
    print(f"   - الخادم الخلفي: {results['backend'].get('health', 'unknown')}")
    print(f"   - المصادقة: {results['authentication'].get('login', 'unknown')}")
    print(f"   - الخادم الأمامي: {results['frontend'].get('status', 'unknown')}")
    
    return results

if __name__ == "__main__":
    main()
