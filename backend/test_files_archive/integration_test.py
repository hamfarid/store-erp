#!/usr/bin/env python3
"""
سكريبت فحص التكامل الشامل للنظام
Comprehensive System Integration Test
"""

import os
import sys
import requests
import json
import time
from datetime import datetime
import subprocess


class SystemIntegrationTester:
    def __init__(self):
        self.backend_url = "http://localhost:5001"
        self.frontend_url = "http://localhost:5502"
        self.results = {
            "backend_tests": [],
            "frontend_tests": [],
            "integration_tests": [],
            "security_tests": [],
            "performance_tests": [],
        }

    def test_backend_health(self):
        """فحص صحة الواجهة الخلفية"""
        print("🔍 فحص صحة الواجهة الخلفية...")

        try:
            # فحص الخادم
            response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            if response.status_code == 200:
                self.results["backend_tests"].append(
                    {
                        "test": "Backend Health Check",
                        "status": "PASS",
                        "message": "الخادم الخلفي يعمل بشكل طبيعي",
                    }
                )
            else:
                self.results["backend_tests"].append(
                    {
                        "test": "Backend Health Check",
                        "status": "FAIL",
                        "message": f"كود الاستجابة: {response.status_code}",
                    }
                )
        except Exception as e:
            self.results["backend_tests"].append(
                {
                    "test": "Backend Health Check",
                    "status": "FAIL",
                    "message": f"خطأ في الاتصال: {str(e)}",
                }
            )

    def test_api_endpoints(self):
        """فحص نقاط النهاية الأساسية"""
        print("🔍 فحص نقاط النهاية الأساسية...")

        endpoints = [
            "/api/products",
            "/api/customers",
            "/api/suppliers",
            "/api/invoices",
            "/api/inventory",
        ]

        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                if response.status_code in [200, 401]:  # 401 مقبول للنقاط المحمية
                    self.results["backend_tests"].append(
                        {
                            "test": f"API Endpoint {endpoint}",
                            "status": "PASS",
                            "message": f"النقطة متاحة (كود: {response.status_code})",
                        }
                    )
                else:
                    self.results["backend_tests"].append(
                        {
                            "test": f"API Endpoint {endpoint}",
                            "status": "FAIL",
                            "message": f"كود غير متوقع: {response.status_code}",
                        }
                    )
            except Exception as e:
                self.results["backend_tests"].append(
                    {
                        "test": f"API Endpoint {endpoint}",
                        "status": "FAIL",
                        "message": f"خطأ: {str(e)}",
                    }
                )

    def test_database_connection(self):
        """فحص اتصال قاعدة البيانات"""
        print("🔍 فحص اتصال قاعدة البيانات...")

        try:
            # فحص وجود ملفات قاعدة البيانات
            db_files = ["instance/inventory.db", "src/inventory.db"]

            found_db = False
            for db_file in db_files:
                if os.path.exists(db_file):
                    size = os.path.getsize(db_file)
                    self.results["backend_tests"].append(
                        {
                            "test": f"Database File {db_file}",
                            "status": "PASS",
                            "message": f"قاعدة البيانات موجودة (حجم: {size} بايت)",
                        }
                    )
                    found_db = True

            if not found_db:
                self.results["backend_tests"].append(
                    {
                        "test": "Database Connection",
                        "status": "FAIL",
                        "message": "لم يتم العثور على ملفات قاعدة البيانات",
                    }
                )

        except Exception as e:
            self.results["backend_tests"].append(
                {
                    "test": "Database Connection",
                    "status": "FAIL",
                    "message": f"خطأ: {str(e)}",
                }
            )

    def test_frontend_build(self):
        """فحص بناء الواجهة الأمامية"""
        print("🔍 فحص بناء الواجهة الأمامية...")

        try:
            # فحص وجود ملفات البناء
            build_files = ["../frontend/dist/index.html", "../frontend/package.json"]

            for build_file in build_files:
                if os.path.exists(build_file):
                    self.results["frontend_tests"].append(
                        {
                            "test": f"Frontend Build File {build_file}",
                            "status": "PASS",
                            "message": "ملف البناء موجود",
                        }
                    )
                else:
                    self.results["frontend_tests"].append(
                        {
                            "test": f"Frontend Build File {build_file}",
                            "status": "FAIL",
                            "message": "ملف البناء غير موجود",
                        }
                    )

        except Exception as e:
            self.results["frontend_tests"].append(
                {
                    "test": "Frontend Build",
                    "status": "FAIL",
                    "message": f"خطأ: {str(e)}",
                }
            )

    def test_security_config(self):
        """فحص الإعدادات الأمنية"""
        print("🔍 فحص الإعدادات الأمنية...")

        try:
            # فحص ملف .env
            if os.path.exists(".env"):
                with open(".env", "r") as f:
                    env_content = f.read()

                # فحص المتغيرات الأمنية المهمة
                security_vars = ["SECRET_KEY", "JWT_SECRET_KEY", "ENCRYPTION_KEY"]

                for var in security_vars:
                    if var in env_content:
                        # التحقق من أن القيمة ليست افتراضية
                        if "your-" not in env_content or "default" not in env_content:
                            self.results["security_tests"].append(
                                {
                                    "test": f"Security Variable {var}",
                                    "status": "PASS",
                                    "message": "متغير الأمان محدد",
                                }
                            )
                        else:
                            self.results["security_tests"].append(
                                {
                                    "test": f"Security Variable {var}",
                                    "status": "WARN",
                                    "message": "قيمة افتراضية - يجب تغييرها",
                                }
                            )
                    else:
                        self.results["security_tests"].append(
                            {
                                "test": f"Security Variable {var}",
                                "status": "FAIL",
                                "message": "متغير الأمان غير محدد",
                            }
                        )
            else:
                self.results["security_tests"].append(
                    {
                        "test": "Environment File",
                        "status": "FAIL",
                        "message": "ملف .env غير موجود",
                    }
                )

        except Exception as e:
            self.results["security_tests"].append(
                {
                    "test": "Security Configuration",
                    "status": "FAIL",
                    "message": f"خطأ: {str(e)}",
                }
            )

    def test_performance_metrics(self):
        """فحص مقاييس الأداء"""
        print("🔍 فحص مقاييس الأداء...")

        try:
            # فحص حجم الملفات
            total_size = 0
            file_count = 0

            for root, dirs, files in os.walk("."):
                for file in files:
                    if not file.startswith(".") and not file.endswith(".db"):
                        file_path = os.path.join(root, file)
                        try:
                            size = os.path.getsize(file_path)
                            total_size += size
                            file_count += 1
                        except:
                            continue

            # تحويل إلى MB
            total_size_mb = total_size / (1024 * 1024)

            self.results["performance_tests"].append(
                {
                    "test": "System Size",
                    "status": "INFO",
                    "message": f"حجم النظام: {total_size_mb:.2f} MB ({file_count} ملف)",
                }
            )

            # فحص عدد الملفات الكبيرة
            large_files = []
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith(".py") or file.endswith(".jsx"):
                        file_path = os.path.join(root, file)
                        try:
                            size = os.path.getsize(file_path)
                            if size > 50000:  # أكبر من 50KB
                                large_files.append((file_path, size))
                        except:
                            continue

            if large_files:
                self.results["performance_tests"].append(
                    {
                        "test": "Large Files",
                        "status": "WARN",
                        "message": f"عدد الملفات الكبيرة: {len(large_files)}",
                    }
                )
            else:
                self.results["performance_tests"].append(
                    {
                        "test": "Large Files",
                        "status": "PASS",
                        "message": "لا توجد ملفات كبيرة جداً",
                    }
                )

        except Exception as e:
            self.results["performance_tests"].append(
                {
                    "test": "Performance Metrics",
                    "status": "FAIL",
                    "message": f"خطأ: {str(e)}",
                }
            )

    def test_integration_flow(self):
        """فحص تدفق التكامل"""
        print("🔍 فحص تدفق التكامل...")

        try:
            # فحص تطابق نقاط النهاية
            frontend_api_file = "../frontend/src/config/api.js"
            if os.path.exists(frontend_api_file):
                with open(frontend_api_file, "r") as f:
                    frontend_content = f.read()

                # البحث عن نقاط النهاية في الواجهة الأمامية
                if "API_ENDPOINTS" in frontend_content:
                    self.results["integration_tests"].append(
                        {
                            "test": "API Configuration",
                            "status": "PASS",
                            "message": "ملف إعدادات API موجود",
                        }
                    )
                else:
                    self.results["integration_tests"].append(
                        {
                            "test": "API Configuration",
                            "status": "FAIL",
                            "message": "إعدادات API غير مكتملة",
                        }
                    )
            else:
                self.results["integration_tests"].append(
                    {
                        "test": "API Configuration",
                        "status": "FAIL",
                        "message": "ملف إعدادات API غير موجود",
                    }
                )

        except Exception as e:
            self.results["integration_tests"].append(
                {
                    "test": "Integration Flow",
                    "status": "FAIL",
                    "message": f"خطأ: {str(e)}",
                }
            )

    def generate_report(self):
        """إنشاء تقرير الفحص"""
        print("\n" + "=" * 60)
        print("📊 تقرير فحص التكامل الشامل")
        print("=" * 60)

        # إحصائيات عامة
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        warnings = 0

        for category, tests in self.results.items():
            print(f"\n🔍 {category.replace('_', ' ').title()}:")
            print("-" * 40)

            for test in tests:
                total_tests += 1
                status_icon = {
                    "PASS": "✅",
                    "FAIL": "❌",
                    "WARN": "⚠️",
                    "INFO": "ℹ️",
                }.get(test["status"], "❓")

                print(f"{status_icon} {test['test']}: {test['message']}")

                if test["status"] == "PASS":
                    passed_tests += 1
                elif test["status"] == "FAIL":
                    failed_tests += 1
                elif test["status"] == "WARN":
                    warnings += 1

        # ملخص النتائج
        print("\n" + "=" * 60)
        print("📈 ملخص النتائج:")
        print(f"إجمالي الاختبارات: {total_tests}")
        print(f"✅ نجح: {passed_tests}")
        print(f"❌ فشل: {failed_tests}")
        print(f"⚠️ تحذيرات: {warnings}")

        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"📊 معدل النجاح: {success_rate:.1f}%")

        # تقييم عام
        if success_rate >= 90:
            print("🎉 النظام في حالة ممتازة!")
        elif success_rate >= 75:
            print("👍 النظام في حالة جيدة مع بعض التحسينات المطلوبة")
        elif success_rate >= 50:
            print("⚠️ النظام يحتاج إلى تحسينات كبيرة")
        else:
            print("🚨 النظام يحتاج إلى إصلاحات عاجلة")

        # حفظ التقرير
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "warnings": warnings,
                "success_rate": success_rate,
            },
            "results": self.results,
        }

        with open("integration_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 تم حفظ التقرير التفصيلي في: integration_test_report.json")

    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🚀 بدء فحص التكامل الشامل للنظام...")
        print("=" * 60)

        # تشغيل جميع الاختبارات
        self.test_backend_health()
        self.test_api_endpoints()
        self.test_database_connection()
        self.test_frontend_build()
        self.test_security_config()
        self.test_performance_metrics()
        self.test_integration_flow()

        # إنشاء التقرير
        self.generate_report()


def main():
    """الدالة الرئيسية"""
    tester = SystemIntegrationTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
