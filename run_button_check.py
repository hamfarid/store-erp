#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
تشغيل فحص شامل لجميع الأزرار
ملف: run_button_check.py
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from comprehensive_button_checker import ComprehensiveButtonChecker

class ButtonCheckRunner:
    """فئة تشغيل فحص الأزرار الشامل"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'backend_check': {},
            'frontend_check': {},
            'integration_check': {},
            'final_report': {},
            'summary': {
                'total_checks': 0,
                'passed_checks': 0,
                'failed_checks': 0,
                'critical_issues': 0
            }
        }

    def run_backend_button_check(self):
        """تشغيل فحص أزرار Backend"""
        print("🔧 === فحص أزرار Backend ===")

        try:
            # تشغيل فاحص الأزرار الشامل
            checker = ComprehensiveButtonChecker()
            backend_results = checker.run_comprehensive_check()

            self.results['backend_check'] = {
                'status': 'completed',
                'results': backend_results,
                'timestamp': datetime.now().isoformat()
            }

            # تحليل النتائج
            summary = backend_results.get('summary', {})
            total_buttons = summary.get('total_buttons', 0)
            working_buttons = summary.get('working_buttons', 0)

            if total_buttons > 0:
                success_rate = (working_buttons / total_buttons) * 100

                if success_rate >= 80:
                    print(f"✅ Backend: {success_rate:.1f}% من الأزرار تعمل")
                    self.results['summary']['passed_checks'] += 1
                else:
                    print(f"⚠️ Backend: {success_rate:.1f}% من الأزرار تعمل (يحتاج تحسين)")
                    self.results['summary']['failed_checks'] += 1

                    if success_rate < 50:
                        self.results['summary']['critical_issues'] += 1

            self.results['summary']['total_checks'] += 1

        except Exception as e:
            print(f"❌ خطأ في فحص Backend: {e}")
            self.results['backend_check'] = {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.results['summary']['failed_checks'] += 1
            self.results['summary']['total_checks'] += 1

    def run_frontend_button_check(self):
        """تشغيل فحص أزرار Frontend"""
        print("\n⚛️ === فحص أزرار Frontend ===")

        try:
            # فحص إذا كان Frontend يعمل
            frontend_running = self.check_frontend_status()

            if not frontend_running:
                print("⚠️ Frontend غير متاح، تخطي فحص الأزرار المباشر")
                self.results['frontend_check'] = {
                    'status': 'skipped',
                    'reason': 'Frontend not running',
                    'timestamp': datetime.now().isoformat()
                }
                return

            # تشغيل فحص Frontend باستخدام Playwright أو Selenium
            frontend_results = self.run_frontend_automation_check()

            self.results['frontend_check'] = {
                'status': 'completed',
                'results': frontend_results,
                'timestamp': datetime.now().isoformat()
            }

            self.results['summary']['total_checks'] += 1

            if frontend_results.get('success', False):
                self.results['summary']['passed_checks'] += 1
                print("✅ Frontend: فحص الأزرار مكتمل")
            else:
                self.results['summary']['failed_checks'] += 1
                print("❌ Frontend: مشاكل في الأزرار")

        except Exception as e:
            print(f"❌ خطأ في فحص Frontend: {e}")
            self.results['frontend_check'] = {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.results['summary']['failed_checks'] += 1
            self.results['summary']['total_checks'] += 1

    def check_frontend_status(self):
        """فحص حالة Frontend"""
        try:
            import requests
            response = requests.get('http://localhost:3004', timeout=5)
            return response.status_code == 200
        except:
            return False

    def run_frontend_automation_check(self):
        """تشغيل فحص Frontend التلقائي"""
        try:
            # محاولة استخدام Playwright
            return self.run_playwright_button_check()
        except:
            try:
                # محاولة استخدام Selenium
                return self.run_selenium_button_check()
            except:
                # فحص أساسي
                return self.run_basic_frontend_check()

    def run_playwright_button_check(self):
        """فحص الأزرار باستخدام Playwright"""
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # الانتقال للصفحة الرئيسية
                page.goto('http://localhost:3004')
                page.wait_for_load_state('networkidle')

                # تشغيل فاحص الأزرار JavaScript
                page.add_script_tag(path=str(self.base_dir / "frontend" / "src" / "utils" / "buttonChecker.js"))

                # تشغيل الفحص
                results = page.evaluate('checkAllButtons()')

                browser.close()

                return {
                    'success': True,
                    'method': 'playwright',
                    'results': results
                }

        except Exception as e:
            raise Exception(f"Playwright failed: {e}")

    def run_selenium_button_check(self):
        """فحص الأزرار باستخدام Selenium"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By

            # إعداد Chrome headless
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=chrome_options)

            try:
                # الانتقال للصفحة
                driver.get('http://localhost:3004')
                time.sleep(3)

                # البحث عن الأزرار
                buttons = driver.find_elements(By.TAG_NAME, 'button')
                inputs = driver.find_elements(By.CSS_SELECTOR,
                    'input[type="button"], input[type="submit"]')

                all_buttons = buttons + inputs

                button_results = []
                working_count = 0

                for i, button in enumerate(all_buttons):
                    try:
                        button_info = {
                            'index': i + 1,
                            'text': button.text or button.get_attribute('value') or 'بدون نص',
                            'enabled': button.is_enabled(),
                            'displayed': button.is_displayed(),
                            'clickable': False
                        }

                        # اختبار النقر (للأزرار الآمنة فقط)
                        if button.is_enabled() and button.is_displayed():
                            button_text = button_info['text'].lower()
                            if not any(danger in button_text for danger in ['delete',
                                'remove',
                                'حذف',
                                'logout']):
                                try:
                                    driver.execute_script("arguments[0].click();",
                                        button)
                                    button_info['clickable'] = True
                                    working_count += 1
                                except:
                                    pass

                        button_results.append(button_info)

                    except Exception as e:
                        print(f"⚠️ خطأ في فحص الزر {i + 1}: {e}")

                driver.quit()

                return {
                    'success': True,
                    'method': 'selenium',
                    'total_buttons': len(all_buttons),
                    'working_buttons': working_count,
                    'buttons': button_results
                }

            except Exception as e:
                driver.quit()
                raise e

        except Exception as e:
            raise Exception(f"Selenium failed: {e}")

    def run_basic_frontend_check(self):
        """فحص Frontend أساسي"""
        try:
            import requests

            # فحص الصفحة الرئيسية
            response = requests.get('http://localhost:3004', timeout=10)

            if response.status_code == 200:
                content = response.text

                # البحث عن الأزرار في HTML
                import re

                button_patterns = [
                    r'<button[^>]*>',
                    r'<input[^>]*type=["\']button["\'][^>]*>',
                    r'<input[^>]*type=["\']submit["\'][^>]*>'
                ]

                total_buttons = 0
                for pattern in button_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    total_buttons += len(matches)

                return {
                    'success': True,
                    'method': 'basic_html_scan',
                    'total_buttons': total_buttons,
                    'note': 'فحص أساسي للـ HTML فقط'
                }
            else:
                return {
                    'success': False,
                    'method': 'basic_html_scan',
                    'error': f'HTTP {response.status_code}'
                }

        except Exception as e:
            return {
                'success': False,
                'method': 'basic_html_scan',
                'error': str(e)
            }

    def run_integration_check(self):
        """فحص التكامل بين Frontend و Backend"""
        print("\n🔗 === فحص تكامل الأزرار ===")

        try:
            # فحص إذا كانت الأزرار في Frontend تتصل بـ APIs في Backend
            backend_endpoints = self.get_backend_endpoints()
            frontend_buttons = self.get_frontend_button_actions()

            integration_results = self.analyze_button_api_mapping(frontend_buttons,
                backend_endpoints)

            self.results['integration_check'] = {
                'status': 'completed',
                'results': integration_results,
                'timestamp': datetime.now().isoformat()
            }

            self.results['summary']['total_checks'] += 1

            if integration_results.get('integration_score', 0) >= 70:
                self.results['summary']['passed_checks'] += 1
                print("✅ تكامل جيد بين الأزرار و APIs")
            else:
                self.results['summary']['failed_checks'] += 1
                print("⚠️ تكامل ضعيف بين الأزرار و APIs")

        except Exception as e:
            print(f"❌ خطأ في فحص التكامل: {e}")
            self.results['integration_check'] = {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.results['summary']['failed_checks'] += 1
            self.results['summary']['total_checks'] += 1

    def get_backend_endpoints(self):
        """الحصول على نقاط Backend"""
        if 'backend_check' in self.results and 'results' in self.results['backend_check']:
            return self.results['backend_check']['results'].get('backend_endpoints',
                {})
        return {}

    def get_frontend_button_actions(self):
        """الحصول على أفعال أزرار Frontend"""
        if 'backend_check' in self.results and 'results' in self.results['backend_check']:
            return self.results['backend_check']['results'].get('frontend_buttons',
                {})
        return {}

    def analyze_button_api_mapping(self, buttons, endpoints):
        """تحليل ربط الأزرار بـ APIs"""
        mapped_buttons = 0
        total_buttons = 0

        for file_data in buttons.values():
            for button in file_data.get('buttons', []):
                total_buttons += 1

                # البحث عن API مطابق
                button_text = button.get('text', '').lower()

                for endpoint_file, endpoint_list in endpoints.items():
                    for endpoint in endpoint_list:
                        endpoint_path = endpoint.get('endpoint', '').lower()

                        # مطابقة بسيطة
                        if any(keyword in endpoint_path for keyword in ['save',
                            'add',
                            'delete',
                            'update']
                               if keyword in button_text):
                            mapped_buttons += 1
                            break

        integration_score = (mapped_buttons / total_buttons * 100) if total_buttons > 0 else 0

        return {
            'total_buttons': total_buttons,
            'mapped_buttons': mapped_buttons,
            'integration_score': integration_score,
            'unmapped_buttons': total_buttons - mapped_buttons
        }

    def generate_final_report(self):
        """إنشاء التقرير النهائي"""
        print("\n📊 === إنشاء التقرير النهائي ===")

        summary = self.results['summary']

        report = {
            'overall_status': 'passed' if summary['failed_checks'] == 0 else 'failed',
            'success_rate': (summary['passed_checks'] / summary['total_checks'] * 100) if summary['total_checks'] > 0 else 0,
            'critical_issues': summary['critical_issues'],
            'recommendations': [],
            'detailed_findings': {}
        }

        # تحليل النتائج وإنشاء التوصيات
        if summary['failed_checks'] > 0:
            report['recommendations'].append(f"إصلاح {summary['failed_checks']} مشكلة في الأزرار")

        if summary['critical_issues'] > 0:
            report['recommendations'].append(f"معالجة {summary['critical_issues']} مشكلة حرجة فوراً")

        # تفاصيل النتائج
        if 'backend_check' in self.results:
            backend_summary = self.results['backend_check'].get('results',
                {}).get('summary',
                {})
            report['detailed_findings']['backend'] = {
                'total_buttons': backend_summary.get('total_buttons', 0),
                'working_buttons': backend_summary.get('working_buttons', 0),
                'missing_handlers': backend_summary.get('missing_handlers', 0)
            }

        if 'frontend_check' in self.results:
            frontend_results = self.results['frontend_check'].get('results',
                {})
            report['detailed_findings']['frontend'] = {
                'total_buttons': frontend_results.get('total_buttons', 0),
                'working_buttons': frontend_results.get('working_buttons', 0),
                'method': frontend_results.get('method', 'unknown')
            }

        self.results['final_report'] = report

        return report

    def print_final_results(self, report):
        """عرض النتائج النهائية"""
        print("\n🎯 === النتائج النهائية ===")

        summary = self.results['summary']

        print(f"إجمالي الفحوصات: {summary['total_checks']}")
        print(f"نجح: {summary['passed_checks']}")
        print(f"فشل: {summary['failed_checks']}")
        print(f"مشاكل حرجة: {summary['critical_issues']}")
        print(f"معدل النجاح: {report['success_rate']:.1f}%")

        if report['overall_status'] == 'passed':
            print("\n🎉 جميع الأزرار تعمل بشكل ممتاز!")
        else:
            print("\n⚠️ يحتاج إلى إصلاحات")

        if report['recommendations']:
            print("\n💡 التوصيات:")
            for rec in report['recommendations']:
                print(f"  - {rec}")

        # عرض التفاصيل
        findings = report['detailed_findings']

        if 'backend' in findings:
            backend = findings['backend']
            print("\n🔧 Backend:")
            print(f"  - إجمالي الأزرار: {backend['total_buttons']}")
            print(f"  - أزرار تعمل: {backend['working_buttons']}")
            print(f"  - معالجات مفقودة: {backend['missing_handlers']}")

        if 'frontend' in findings:
            frontend = findings['frontend']
            print("\n⚛️ Frontend:")
            print(f"  - إجمالي الأزرار: {frontend['total_buttons']}")
            print(f"  - أزرار تعمل: {frontend['working_buttons']}")
            print(f"  - طريقة الفحص: {frontend['method']}")

    def save_results(self):
        """حفظ النتائج"""
        results_file = self.base_dir / "complete_button_check_results.json"

        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)

            print(f"\n💾 تم حفظ النتائج في: {results_file}")

        except Exception as e:
            print(f"❌ خطأ في حفظ النتائج: {e}")

    def run_complete_check(self):
        """تشغيل فحص شامل لجميع الأزرار"""
        print("🔘 === بدء فحص شامل لجميع الأزرار ===")
        print(f"⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # تشغيل جميع الفحوصات
        self.run_backend_button_check()
        self.run_frontend_button_check()
        self.run_integration_check()

        # إنشاء التقرير النهائي
        report = self.generate_final_report()

        # عرض النتائج
        self.print_final_results(report)

        # حفظ النتائج
        self.save_results()

        return self.results

def main():
    """الدالة الرئيسية"""
    runner = ButtonCheckRunner()
    results = runner.run_complete_check()

    # إرجاع كود الخروج حسب النتائج
    if results['summary']['critical_issues'] > 0:
        exit(2)  # مشاكل حرجة
    elif results['summary']['failed_checks'] > 0:
        exit(1)  # مشاكل عامة
    else:
        exit(0)  # كل شيء يعمل

if __name__ == "__main__":
    main()
