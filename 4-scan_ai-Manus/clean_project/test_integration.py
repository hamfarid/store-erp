# File: /home/ubuntu/clean_project/test_integration.py
"""
اختبار التكامل الشامل لنظام Gaara Scan AI
"""

import requests
import json
import time
from datetime import datetime


class GaaraScanIntegrationTest:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []

    def log_test(self, test_name, status, message="", response_time=0):
        """تسجيل نتيجة الاختبار"""
        result = {
            "test_name": test_name,
            "status": status,
            "message": message,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"[{status}] {test_name}: {message} ({response_time:.2f}s)")

    def test_health_check(self):
        """اختبار صحة النظام"""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/health")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Health Check", "PASS", "النظام يعمل بشكل طبيعي", response_time)
                    return True
                else:
                    self.log_test("Health Check", "FAIL", f"حالة غير متوقعة: {data.get('status')}", response_time)
            else:
                self.log_test("Health Check", "FAIL", f"HTTP {response.status_code}", response_time)

        except Exception as e:
            self.log_test("Health Check", "ERROR", str(e), 0)

        return False

    def test_authentication(self):
        """اختبار نظام المصادقة"""
        try:
            # اختبار تسجيل الدخول
            start_time = time.time()
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            response = self.session.post(f"{self.base_url}/api/auth/login", json=login_data)
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    # حفظ الرمز المميز للاستخدام في الاختبارات الأخرى
                    self.session.headers.update({
                        "Authorization": f"Bearer {data['access_token']}"
                    })
                    self.log_test("Authentication - Login", "PASS", "تم تسجيل الدخول بنجاح", response_time)
                    return True
                else:
                    self.log_test("Authentication - Login", "FAIL", "لا يوجد رمز مميز في الاستجابة", response_time)
            else:
                self.log_test("Authentication - Login", "FAIL", f"HTTP {response.status_code}", response_time)

        except Exception as e:
            self.log_test("Authentication - Login", "ERROR", str(e), 0)

        return False

    def test_dashboard_apis(self):
        """اختبار APIs لوحة التحكم"""
        apis_to_test = [
            ("/api/dashboard/stats", "Dashboard Stats"),
            ("/api/dashboard/charts", "Dashboard Charts")
        ]

        all_passed = True
        for endpoint, test_name in apis_to_test:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}")
                response_time = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    if "data" in data:
                        self.log_test(test_name, "PASS", "البيانات متوفرة", response_time)
                    else:
                        self.log_test(test_name, "FAIL", "لا توجد بيانات في الاستجابة", response_time)
                        all_passed = False
                else:
                    self.log_test(test_name, "FAIL", f"HTTP {response.status_code}", response_time)
                    all_passed = False

            except Exception as e:
                self.log_test(test_name, "ERROR", str(e), 0)
                all_passed = False

        return all_passed

    def test_image_enhancement_api(self):
        """اختبار API تحسين الصور"""
        try:
            # اختبار الحصول على الإحصائيات
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/image-enhancement/stats")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "data" in data and "total_processed" in data["data"]:
                    self.log_test("Image Enhancement - Stats", "PASS", "إحصائيات متوفرة", response_time)
                else:
                    self.log_test("Image Enhancement - Stats", "FAIL", "بيانات الإحصائيات غير مكتملة", response_time)
                    return False
            else:
                self.log_test("Image Enhancement - Stats", "FAIL", f"HTTP {response.status_code}", response_time)
                return False

            # اختبار معرض الصور
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/image-enhancement/gallery")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "data" in data and isinstance(data["data"], list):
                    self.log_test("Image Enhancement - Gallery", "PASS", f"المعرض يحتوي على {len(data['data'])} عنصر", response_time)
                    return True
                else:
                    self.log_test("Image Enhancement - Gallery", "FAIL", "بيانات المعرض غير صحيحة", response_time)
            else:
                self.log_test("Image Enhancement - Gallery", "FAIL", f"HTTP {response.status_code}", response_time)

        except Exception as e:
            self.log_test("Image Enhancement API", "ERROR", str(e), 0)

        return False

    def test_plant_hybridization_api(self):
        """اختبار API تهجين النباتات"""
        try:
            # اختبار الحصول على النباتات المتاحة
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/plant-hybridization/plants")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                    plants = data["data"]
                    self.log_test("Plant Hybridization - Plants", "PASS", f"متوفر {len(plants)} نوع نبات", response_time)

                    # اختبار محاكاة التهجين
                    simulation_data = {
                        "parent1_id": plants[0]["id"],
                        "parent2_id": plants[1]["id"] if len(plants) > 1 else plants[0]["id"],
                        "settings": {
                            "type": "simple",
                            "generations": 1,
                            "sample_size": "medium"
                        }
                    }

                    start_time = time.time()
                    response = self.session.post(f"{self.base_url}/api/plant-hybridization/simulate", json=simulation_data)
                    response_time = time.time() - start_time

                    if response.status_code == 200:
                        data = response.json()
                        if "data" in data and "offspring" in data["data"]:
                            offspring_count = len(data["data"]["offspring"])
                            self.log_test("Plant Hybridization - Simulation", "PASS", f"تم إنتاج {offspring_count} نتيجة", response_time)
                            return True
                        else:
                            self.log_test("Plant Hybridization - Simulation", "FAIL", "نتائج المحاكاة غير مكتملة", response_time)
                    else:
                        self.log_test("Plant Hybridization - Simulation", "FAIL", f"HTTP {response.status_code}", response_time)
                else:
                    self.log_test("Plant Hybridization - Plants", "FAIL", "لا توجد نباتات متاحة", response_time)

        except Exception as e:
            self.log_test("Plant Hybridization API", "ERROR", str(e), 0)

        return False

    def test_yolo_detection_api(self):
        """اختبار API كشف الكائنات YOLO"""
        try:
            # اختبار الحصول على الإحصائيات
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/yolo-detection/stats")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "data" in data and "total_detections" in data["data"]:
                    self.log_test("YOLO Detection - Stats", "PASS", "إحصائيات الكشف متوفرة", response_time)
                else:
                    self.log_test("YOLO Detection - Stats", "FAIL", "بيانات الإحصائيات غير مكتملة", response_time)
                    return False
            else:
                self.log_test("YOLO Detection - Stats", "FAIL", f"HTTP {response.status_code}", response_time)
                return False

            # اختبار سجل العمليات
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/yolo-detection/history")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "data" in data and isinstance(data["data"], list):
                    self.log_test("YOLO Detection - History", "PASS", f"السجل يحتوي على {len(data['data'])} عملية", response_time)
                    return True
                else:
                    self.log_test("YOLO Detection - History", "FAIL", "بيانات السجل غير صحيحة", response_time)
            else:
                self.log_test("YOLO Detection - History", "FAIL", f"HTTP {response.status_code}", response_time)

        except Exception as e:
            self.log_test("YOLO Detection API", "ERROR", str(e), 0)

        return False

    def test_docker_management_api(self):
        """اختبار API إدارة Docker"""
        try:
            # اختبار الحصول على إحصائيات Docker
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/docker/stats")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "data" in data and "total_containers" in data["data"]:
                    self.log_test("Docker Management - Stats", "PASS", "إحصائيات Docker متوفرة", response_time)
                else:
                    self.log_test("Docker Management - Stats", "FAIL", "بيانات الإحصائيات غير مكتملة", response_time)
                    return False
            else:
                self.log_test("Docker Management - Stats", "FAIL", f"HTTP {response.status_code}", response_time)
                return False

            # اختبار الحصول على حالة الخدمات
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/docker/services")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "data" in data and isinstance(data["data"], list):
                    services_count = len(data["data"])
                    self.log_test("Docker Management - Services", "PASS", f"متوفر {services_count} خدمة", response_time)
                    return True
                else:
                    self.log_test("Docker Management - Services", "FAIL", "بيانات الخدمات غير صحيحة", response_time)
            else:
                self.log_test("Docker Management - Services", "FAIL", f"HTTP {response.status_code}", response_time)

        except Exception as e:
            self.log_test("Docker Management API", "ERROR", str(e), 0)

        return False

    def test_system_settings_api(self):
        """اختبار API إعدادات النظام"""
        try:
            # اختبار الحصول على الإعدادات
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/settings/system")
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if "data" in data and "language" in data["data"]:
                    self.log_test("System Settings - Get", "PASS", "إعدادات النظام متوفرة", response_time)
                    return True
                else:
                    self.log_test("System Settings - Get", "FAIL", "بيانات الإعدادات غير مكتملة", response_time)
            else:
                self.log_test("System Settings - Get", "FAIL", f"HTTP {response.status_code}", response_time)

        except Exception as e:
            self.log_test("System Settings API", "ERROR", str(e), 0)

        return False

    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("=" * 60)
        print("بدء اختبار التكامل الشامل لنظام Gaara Scan AI")
        print("=" * 60)

        tests = [
            ("فحص صحة النظام", self.test_health_check),
            ("نظام المصادقة", self.test_authentication),
            ("APIs لوحة التحكم", self.test_dashboard_apis),
            ("API تحسين الصور", self.test_image_enhancement_api),
            ("API تهجين النباتات", self.test_plant_hybridization_api),
            ("API كشف الكائنات YOLO", self.test_yolo_detection_api),
            ("API إدارة Docker", self.test_docker_management_api),
            ("API إعدادات النظام", self.test_system_settings_api)
        ]

        passed_tests = 0
        total_tests = len(tests)

        for test_name, test_function in tests:
            print(f"\n--- اختبار: {test_name} ---")
            if test_function():
                passed_tests += 1

        print("\n" + "=" * 60)
        print("ملخص نتائج الاختبار")
        print("=" * 60)
        print(f"إجمالي الاختبارات: {total_tests}")
        print(f"الاختبارات الناجحة: {passed_tests}")
        print(f"الاختبارات الفاشلة: {total_tests - passed_tests}")
        print(f"معدل النجاح: {(passed_tests / total_tests) * 100:.1f}%")

        return passed_tests == total_tests

    def generate_report(self):
        """إنشاء تقرير مفصل للاختبارات"""
        report = {
            "test_summary": {
                "total_tests": len(self.test_results),
                "passed": len([r for r in self.test_results if r["status"] == "PASS"]),
                "failed": len([r for r in self.test_results if r["status"] == "FAIL"]),
                "errors": len([r for r in self.test_results if r["status"] == "ERROR"]),
                "average_response_time": sum(r["response_time"] for r in self.test_results) / len(self.test_results) if self.test_results else 0
            },
            "test_results": self.test_results,
            "generated_at": datetime.now().isoformat()
        }

        return report


if __name__ == "__main__":
    # تشغيل الاختبارات
    tester = GaaraScanIntegrationTest()
    success = tester.run_all_tests()

    # إنشاء تقرير
    report = tester.generate_report()

    # حفظ التقرير
    with open("/home/ubuntu/clean_project/integration_test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nتم حفظ تقرير الاختبار في: /home/ubuntu/clean_project/integration_test_report.json")

    if success:
        print("\n✅ جميع الاختبارات نجحت!")
        exit(0)
    else:
        print("\n❌ بعض الاختبارات فشلت!")
        exit(1)

