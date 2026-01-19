"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/import_export/tests.py
الوصف: اختبارات مديول الاستيراد والتصدير
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import unittest
import os
import tempfile
import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from src.modules.import_export import api, schemas
from src.database import get_db, Base, engine


class TestImportExport(unittest.TestCase):
    """
    اختبارات مديول الاستيراد والتصدير
    """

    @classmethod
    def setUpClass(cls):
        """
        إعداد بيئة الاختبار
        """
        # إنشاء قاعدة بيانات اختبار مؤقتة
        Base.metadata.create_all(bind=engine)

        # إنشاء عميل اختبار
        cls.client = TestClient(app)

        # تجاوز التحقق من المصادقة والصلاحيات
        def override_get_current_user():
            return {"id": 1, "username": "test_user", "role": "admin"}

        def override_check_permission(*args, **kwargs):
            return True

        app.dependency_overrides[api.get_current_user] = override_get_current_user
        app.dependency_overrides[api.check_permission] = override_check_permission

        # إنشاء جلسة قاعدة بيانات
        cls.db = next(get_db())

        # إنشاء إعدادات افتراضية

        cls.db.commit()

    @classmethod
    def tearDownClass(cls):
        """
        تنظيف بيئة الاختبار
        """
        # إغلاق جلسة قاعدة البيانات
        cls.db.close()

        # إزالة تجاوزات التبعيات
        app.dependency_overrides.clear()

        # حذف قاعدة البيانات المؤقتة
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        """
        إعداد كل اختبار
        """
        # تنظيف البيانات قبل كل اختبار
        for table in reversed(Base.metadata.sorted_tables):
            self.db.execute(table.delete())
        self.db.commit()

        # إنشاء إعدادات افتراضية

        self.db.commit()

        # تجاوز دالة تسجيل النشاط
        self.log_activity_patch = patch('src.modules.activity_log.service.log_user_action')
        self.mock_log_activity = self.log_activity_patch.start()

    def tearDown(self):
        """
        تنظيف بعد كل اختبار
        """
        # إيقاف تجاوز دالة تسجيل النشاط
        self.log_activity_patch.stop()

    def test_get_available_modules(self):
        """
        اختبار الحصول على المديولات المتاحة
        """
        # إنشاء مديول اختبار
        module_data = {
            "id": "test_module",
            "name": "Test Module",
            "description": "Test module description",
            "supports_import": True,
            "supports_export": True,
            "fields": [
                {"name": "id", "type": "integer", "description": "ID"},
                {"name": "name", "type": "string", "description": "Name"},
                {"name": "email", "type": "email", "description": "Email"}
            ],
            "required_fields": ["name"],
            "unique_fields": ["id", "email"]
        }

        # تجاوز دالة الحصول على المديولات
        with patch('src.modules.import_export.service.get_available_modules', return_value=[schemas.ModuleInfo(**module_data)]):
            response = self.client.get("/api/import-export/modules")

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]["id"], "test_module")
            self.assertEqual(response.json()[0]["name"], "Test Module")

    def test_create_template(self):
        """
        اختبار إنشاء قالب
        """
        # بيانات القالب
        template_data = {
            "name": "Test Template",
            "description": "Test template description",
            "module_id": "test_module",
            "type": "import",
            "format": "csv",
            "field_mapping": {
                "Column A": "name",
                "Column B": "email"
            },
            "options": {
                "skip_header": True
            }
        }

        # تجاوز دالة إنشاء القالب
        with patch('src.modules.import_export.service.create_template', return_value=schemas.ImportExportTemplate(
            id=1,
            created_at="2025-05-29T12:00:00",
            updated_at="2025-05-29T12:00:00",
            created_by=1,
            **template_data
        )):
            response = self.client.post(
                "/api/import-export/templates",
                json=template_data
            )

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["name"], "Test Template")
            self.assertEqual(response.json()["module_id"], "test_module")

            # التحقق من تسجيل النشاط
            self.mock_log_activity.assert_called_once()

    def test_import_data_validation(self):
        """
        اختبار التحقق من صحة بيانات الاستيراد
        """
        # إنشاء ملف CSV مؤقت
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            # كتابة بيانات CSV
            df = pd.DataFrame({
                'Column A': ['Test 1', 'Test 2', ''],
                'Column B': ['test1@example.com', 'invalid-email', 'test3@example.com']
            })
            df.to_csv(temp_file.name, index=False)

        # تجاوز دالة التحقق من صحة الملف
        with patch('src.modules.import_export.dependencies.validate_import_file'):
            # تجاوز دالة استيراد البيانات
            with patch('src.modules.import_export.service.import_data', return_value=schemas.ImportResult(
                job_id="test-job-id",
                status=schemas.JobStatus.COMPLETED,
                message="تم استيراد البيانات بنجاح",
                imported_count=2,
                error_count=1,
                warnings=["الصف 3: الحقل 'name' فارغ"],
                details={
                    "valid_rows": [1, 2],
                    "invalid_rows": [3],
                    "errors": {
                        "3": ["الحقل 'name' مطلوب", "الحقل 'email' غير صالح"]
                    }
                }
            )):
                with open(temp_file.name, 'rb') as f:
                    response = self.client.post(
                        "/api/import-export/import",
                        files={"file": ("test.csv", f, "text/csv")},
                        data={
                            "module": "test_module",
                            "options": "{}"
                        }
                    )

                    # التحقق من الاستجابة
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json()["status"], "completed")
                    self.assertEqual(response.json()["imported_count"], 2)
                    self.assertEqual(response.json()["error_count"], 1)

                    # التحقق من تسجيل النشاط
                    self.mock_log_activity.assert_called_once()

        # حذف الملف المؤقت
        os.unlink(temp_file.name)

    def test_export_data(self):
        """
        اختبار تصدير البيانات
        """
        # بيانات طلب التصدير
        export_request = {
            "module": "test_module",
            "format": "xlsx",
            "fields": ["id", "name", "email"],
            "filters": {
                "name": "Test"
            },
            "options": {
                "include_header": True
            }
        }

        # تجاوز دالة التحقق من صحة طلب التصدير
        with patch('src.modules.import_export.dependencies.validate_export_request'):
            # تجاوز دالة تصدير البيانات
            with patch('src.modules.import_export.service.export_data', return_value=schemas.ExportResult(
                job_id="test-job-id",
                status=schemas.JobStatus.COMPLETED,
                message="تم تصدير البيانات بنجاح",
                exported_count=10,
                download_url="/api/import-export/download/test-file-id",
                filename="test_export.xlsx"
            )):
                response = self.client.post(
                    "/api/import-export/export",
                    json=export_request
                )

                # التحقق من الاستجابة
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["status"], "completed")
                self.assertEqual(response.json()["exported_count"], 10)
                self.assertEqual(response.json()["download_url"], "/api/import-export/download/test-file-id")

                # التحقق من تسجيل النشاط
                self.mock_log_activity.assert_called_once()

    def test_validate_field_mapping(self):
        """
        اختبار التحقق من صحة تعيين الحقول
        """
        # بيانات طلب التحقق
        validation_request = {
            "module": "test_module",
            "field_mapping": {
                "Column A": "name",
                "Column B": "email",
                "Column C": "invalid_field"
            },
            "sample_data": [
                {"Column A": "Test 1", "Column B": "test1@example.com", "Column C": "Value 1"},
                {"Column A": "", "Column B": "invalid-email", "Column C": "Value 2"}
            ]
        }

        # تجاوز دالة التحقق من صحة تعيين الحقول
        with patch('src.modules.import_export.service.validate_field_mapping', return_value=schemas.ValidationResult(
            is_valid=False,
            errors=["الحقل 'invalid_field' غير موجود في المديول 'test_module'"],
            warnings=["الصف 2: الحقل 'name' فارغ", "الصف 2: الحقل 'email' غير صالح"],
            details={
                "valid_fields": ["name", "email"],
                "invalid_fields": ["invalid_field"],
                "sample_validation": {
                    "total_records": 2,
                    "valid_records": 1,
                    "invalid_records": 1
                }
            }
        )):
            response = self.client.post(
                "/api/import-export/validate-mapping",
                json=validation_request
            )

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.json()["is_valid"])
            self.assertEqual(len(response.json()["errors"]), 1)
            self.assertEqual(len(response.json()["warnings"]), 2)

    def test_job_history(self):
        """
        اختبار سجل المهام
        """
        # تجاوز دالة الحصول على سجل المهام
        with patch('src.modules.import_export.service.get_job_history', return_value=schemas.PaginatedImportExportJobs(
            items=[
                schemas.JobStatusDetail(
                    job_id="job-1",
                    job_type=schemas.JobType.IMPORT,
                    module="test_module",
                    status=schemas.JobStatus.COMPLETED,
                    progress=100,
                    message="تم استيراد البيانات بنجاح",
                    created_at="2025-05-29T10:00:00",
                    updated_at="2025-05-29T10:05:00",
                    completed_at="2025-05-29T10:05:00",
                    user_id=1,
                    result={
                        "imported_count": 10,
                        "error_count": 0
                    }
                ),
                schemas.JobStatusDetail(
                    job_id="job-2",
                    job_type=schemas.JobType.EXPORT,
                    module="test_module",
                    status=schemas.JobStatus.FAILED,
                    progress=50,
                    message="فشل في تصدير البيانات: خطأ في الاتصال بقاعدة البيانات",
                    created_at="2025-05-29T11:00:00",
                    updated_at="2025-05-29T11:02:00",
                    completed_at=None,
                    user_id=1,
                    result=None
                )
            ],
            total=2,
            page=1,
            page_size=10,
            total_pages=1
        )):
            response = self.client.get("/api/import-export/history?page=1&page_size=10")

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()["items"]), 2)
            self.assertEqual(response.json()["total"], 2)
            self.assertEqual(response.json()["items"][0]["job_type"], "import")
            self.assertEqual(response.json()["items"][1]["job_type"], "export")

    def test_error_handling(self):
        """
        اختبار معالجة الأخطاء
        """
        # اختبار خطأ في التحقق من صحة الملف
        with patch('src.modules.import_export.dependencies.validate_import_file', side_effect=Exception("خطأ في التحقق من صحة الملف")):
            with tempfile.NamedTemporaryFile(suffix='.csv') as temp_file:
                # كتابة بيانات CSV
                df = pd.DataFrame({
                    'Column A': ['Test 1'],
                    'Column B': ['test1@example.com']
                })
                df.to_csv(temp_file.name, index=False)

                with open(temp_file.name, 'rb') as f:
                    response = self.client.post(
                        "/api/import-export/import",
                        files={"file": ("test.csv", f, "text/csv")},
                        data={
                            "module": "test_module",
                            "options": "{}"
                        }
                    )

                    # التحقق من الاستجابة
                    self.assertEqual(response.status_code, 500)

        # اختبار خطأ في طلب التصدير
        with patch('src.modules.import_export.dependencies.validate_export_request', side_effect=Exception("خطأ في التحقق من صحة طلب التصدير")):
            response = self.client.post(
                "/api/import-export/export",
                json={
                    "module": "test_module",
                    "format": "xlsx"
                }
            )

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
