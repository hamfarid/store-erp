#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔬 الاختبار الشامل النهائي للنظام
Ultimate System Test

اختبار شامل ونهائي لجميع مكونات النظام:
- الخادم الخلفي ونقاط النهاية
- الخادم الأمامي والواجهة
- قاعدة البيانات والبيانات
- نظام المصادقة والأمان
- التكامل بين المكونات
"""

import json
import sqlite3
import time
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class UltimateSystemTest:
    def __init__(self):
        self.backend_url = "http://localhost:5002"
        self.frontend_url = "http://localhost:5503"
        self.db_path = "backend/instance/inventory.db"
        self.test_results = {
            'backend_tests': {},
            'frontend_tests': {},
            'database_tests': {},
            'integration_tests': {},
            'overall_score': 0,
            'timestamp': datetime.now().isoformat()
        }
        self.session_token = None

    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🔬 بدء الاختبار الشامل النهائي للنظام")
        print("=" * 60)

        # اختبارات الخادم الخلفي
        print("\n🔧 اختبار الخادم الخلفي...")
        self.test_backend()

        # اختبارات قاعدة البيانات
        print("\n💾 اختبار قاعدة البيانات...")
        self.test_database()

        # اختبارات الخادم الأمامي
        print("\n🌐 اختبار الخادم الأمامي...")
        self.test_frontend()

        # اختبارات التكامل
        print("\n🔗 اختبار التكامل...")
        self.test_integration()

        # حساب النتيجة الإجمالية
        self.calculate_overall_score()

        # إنشاء التقرير
        self.generate_report()

        print(f"\n📊 النتيجة الإجمالية: {self.test_results['overall_score']:.1f}%")

        return self.test_results

    def test_backend(self):
        """اختبار الخادم الخلفي"""
        backend_tests = {}

        # اختبار حالة الخادم
        try:
            response = requests.get(f"{self.backend_url}/api/status", timeout=5)
            backend_tests['server_status'] = {
                'passed': response.status_code == 200,
                'response_time': response.elapsed.total_seconds(),
                'details': response.json() if response.status_code == 200 else str(response.status_code)
            }
        except Exception as e:
            backend_tests['server_status'] = {
                'passed': False,
                'error': str(e)
            }

        # اختبار تسجيل الدخول
        try:
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            response = requests.post(f"{self.backend_url}/api/auth/login",
                                   json=login_data, timeout=5)

            if response.status_code == 200:
                data = response.json()
                self.session_token = data.get('session_token')
                backend_tests['authentication'] = {
                    'passed': True,
                    'has_token': bool(self.session_token),
                    'user_data': data.get('user', {})
                }
            else:
                backend_tests['authentication'] = {
                    'passed': False,
                    'status_code': response.status_code,
                    'error': response.text
                }
        except Exception as e:
            backend_tests['authentication'] = {
                'passed': False,
                'error': str(e)
            }

        # اختبار نقاط النهاية المحمية
        headers = {'Authorization': f'Bearer {self.session_token}'} if self.session_token else {}

        endpoints_to_test = [
            '/api/categories',
            '/api/warehouses',
            '/api/products',
            '/api/users',
            '/api/reports/dashboard'
        ]

        for endpoint in endpoints_to_test:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}",
                                      headers=headers, timeout=5)
                backend_tests[f'endpoint_{endpoint.split("/")[-1]}'] = {
                    'passed': response.status_code == 200,
                    'status_code': response.status_code,
                    'has_data': bool(response.json().get('success')) if response.status_code == 200 else False
                }
            except Exception as e:
                backend_tests[f'endpoint_{endpoint.split("/")[-1]}'] = {
                    'passed': False,
                    'error': str(e)
                }

        # اختبار إنشاء البيانات
        if self.session_token:
            try:
                new_category = {
                    'name': f'فئة اختبار {int(time.time())}',
                    'description': 'فئة تم إنشاؤها للاختبار'
                }
                response = requests.post(f"{self.backend_url}/api/categories",
                                       json=new_category, headers=headers, timeout=5)
                backend_tests['create_data'] = {
                    'passed': response.status_code in [200, 201],
                    'status_code': response.status_code,
                    'response': response.json() if response.status_code in [200, 201] else response.text
                }
            except Exception as e:
                backend_tests['create_data'] = {
                    'passed': False,
                    'error': str(e)
                }

        self.test_results['backend_tests'] = backend_tests

    def test_database(self):
        """اختبار قاعدة البيانات"""
        database_tests = {}

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # فحص وجود الجداول الأساسية
            required_tables = ['users', 'categories', 'warehouses', 'products',
                             'roles', 'user_roles', 'user_sessions']

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]

            database_tests['tables_exist'] = {
                'passed': all(table in existing_tables for table in required_tables),
                'existing_tables': existing_tables,
                'missing_tables': [table for table in required_tables if table not in existing_tables]
            }

            # فحص البيانات الأساسية
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM roles")
            role_count = cursor.fetchone()[0]

            database_tests['basic_data'] = {
                'passed': user_count > 0 and role_count > 0,
                'user_count': user_count,
                'role_count': role_count
            }

            # فحص المستخدم الإداري
            cursor.execute("SELECT username, is_active FROM users WHERE username = 'admin'")
            admin_user = cursor.fetchone()

            database_tests['admin_user'] = {
                'passed': admin_user is not None and admin_user[1] == 1,
                'exists': admin_user is not None,
                'is_active': admin_user[1] if admin_user else False
            }

            conn.close()

        except Exception as e:
            database_tests['connection_error'] = {
                'passed': False,
                'error': str(e)
            }

        self.test_results['database_tests'] = database_tests

    def test_frontend(self):
        """اختبار الخادم الأمامي"""
        frontend_tests = {}

        # اختبار الوصول للخادم الأمامي
        try:
            response = requests.get(self.frontend_url, timeout=10)
            frontend_tests['server_accessible'] = {
                'passed': response.status_code == 200,
                'status_code': response.status_code,
                'content_length': len(response.content)
            }
        except Exception as e:
            frontend_tests['server_accessible'] = {
                'passed': False,
                'error': str(e)
            }

        # اختبار الواجهة باستخدام Selenium
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)

            # فتح الصفحة الرئيسية
            driver.get(self.frontend_url)
            time.sleep(3)

            # فحص العنوان
            title = driver.title
            frontend_tests['page_title'] = {
                'passed': 'مخزون' in title or 'inventory' in title.lower(),
                'title': title
            }

            # فحص وجود عناصر الواجهة
            try:
                # البحث عن أي عنصر تفاعلي
                interactive_elements = driver.find_elements(By.TAG_NAME, "button")
                interactive_elements.extend(driver.find_elements(By.TAG_NAME, "input"))
                interactive_elements.extend(driver.find_elements(By.TAG_NAME, "a"))

                frontend_tests['interactive_elements'] = {
                    'passed': len(interactive_elements) > 0,
                    'count': len(interactive_elements)
                }
            except Exception as e:
                frontend_tests['interactive_elements'] = {
                    'passed': False,
                    'error': str(e)
                }

            # فحص وجود محتوى
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text
                frontend_tests['has_content'] = {
                    'passed': len(body_text.strip()) > 0,
                    'content_length': len(body_text)
                }
            except Exception as e:
                frontend_tests['has_content'] = {
                    'passed': False,
                    'error': str(e)
                }

            driver.quit()

        except Exception as e:
            frontend_tests['selenium_test'] = {
                'passed': False,
                'error': str(e)
            }

        self.test_results['frontend_tests'] = frontend_tests

    def test_integration(self):
        """اختبار التكامل بين المكونات"""
        integration_tests = {}

        # اختبار التكامل بين الخادم الأمامي والخلفي
        try:
            # محاولة الوصول للخادم الخلفي من خلال CORS
            headers = {
                'Origin': self.frontend_url,
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }

            response = requests.options(f"{self.backend_url}/api/status",
                                      headers=headers, timeout=5)

            integration_tests['cors_enabled'] = {
                'passed': 'Access-Control-Allow-Origin' in response.headers,
                'cors_headers': dict(response.headers)
            }

        except Exception as e:
            integration_tests['cors_enabled'] = {
                'passed': False,
                'error': str(e)
            }

        # اختبار تدفق المصادقة الكامل
        if self.session_token:
            try:
                # اختبار الحصول على بيانات المستخدم
                headers = {'Authorization': f'Bearer {self.session_token}'}
                response = requests.get(f"{self.backend_url}/api/auth/me",
                                      headers=headers, timeout=5)

                integration_tests['auth_flow'] = {
                    'passed': response.status_code == 200,
                    'user_data': response.json() if response.status_code == 200 else None
                }

                # اختبار تسجيل الخروج
                logout_response = requests.post(f"{self.backend_url}/api/auth/logout",
                                              headers=headers, timeout=5)

                integration_tests['logout'] = {
                    'passed': logout_response.status_code == 200,
                    'status_code': logout_response.status_code
                }

            except Exception as e:
                integration_tests['auth_flow'] = {
                    'passed': False,
                    'error': str(e)
                }

        self.test_results['integration_tests'] = integration_tests

    def calculate_overall_score(self):
        """حساب النتيجة الإجمالية"""
        total_tests = 0
        passed_tests = 0

        for category, tests in self.test_results.items():
            if category in ['backend_tests', 'frontend_tests', 'database_tests', 'integration_tests']:
                for test_name, test_result in tests.items():
                    total_tests += 1
                    if test_result.get('passed', False):
                        passed_tests += 1

        if total_tests > 0:
            self.test_results['overall_score'] = (passed_tests / total_tests) * 100
            self.test_results['total_tests'] = total_tests
            self.test_results['passed_tests'] = passed_tests
        else:
            self.test_results['overall_score'] = 0

    def generate_report(self):
        """إنشاء تقرير مفصل"""
        report = {
            'test_summary': {
                'timestamp': self.test_results['timestamp'],
                'overall_score': self.test_results['overall_score'],
                'total_tests': self.test_results.get('total_tests', 0),
                'passed_tests': self.test_results.get('passed_tests', 0)
            },
            'detailed_results': self.test_results
        }

        # حفظ التقرير
        with open('ultimate_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print("\n📄 تم حفظ التقرير المفصل في: ultimate_test_report.json")

        # طباعة ملخص النتائج
        print("\n📊 ملخص النتائج:")
        print("-" * 40)

        categories = {
            'backend_tests': 'الخادم الخلفي',
            'database_tests': 'قاعدة البيانات',
            'frontend_tests': 'الخادم الأمامي',
            'integration_tests': 'التكامل'
        }

        for category, name in categories.items():
            if category in self.test_results:
                tests = self.test_results[category]
                passed = sum(1 for test in tests.values() if test.get('passed', False))
                total = len(tests)
                percentage = (passed / total * 100) if total > 0 else 0

                status = "✅" if percentage == 100 else "⚠️" if percentage >= 50 else "❌"
                print(f"{status} {name}: {passed}/{total} ({percentage:.1f}%)")

if __name__ == "__main__":
    tester = UltimateSystemTest()
    results = tester.run_all_tests()

    if results['overall_score'] >= 90:
        print("\n🎉 النظام يعمل بشكل ممتاز!")
    elif results['overall_score'] >= 70:
        print("\n👍 النظام يعمل بشكل جيد مع بعض المشاكل البسيطة")
    elif results['overall_score'] >= 50:
        print("\n⚠️ النظام يعمل جزئياً ويحتاج إلى إصلاحات")
    else:
        print("\n❌ النظام يحتاج إلى إصلاحات جوهرية")
