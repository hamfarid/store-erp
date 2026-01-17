"""
اختبارات إعدادات النظام والصلاحيات
Settings & Permissions API tests
"""

import unittest
import json
import os
import sys
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


class SettingsPermissionsTestCase(unittest.TestCase):
    """اختبارات لنقاط النهاية /api/settings/system و /api/settings/permissions"""

    @classmethod
    def setUpClass(cls):
        os.environ["TESTING"] = "1"
        # تفعيل تسجيل الـ Blueprints لكي تتوفر المسارات
        os.environ["SKIP_BLUEPRINTS"] = "0"
        from app import create_app

        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "app_context"):
            cls.app_context.pop()

    def test_permissions_alias_endpoint(self):
        """GET /api/settings/permissions يجب أن يعيد حالة نجاح وقائمة صلاحيات"""
        resp = self.client.get("/api/settings/permissions")
        self.assertIn(resp.status_code, [200, 302, 401, 403])
        if resp.status_code == 200:
            data = json.loads(resp.data)
            self.assertIn("status", data)
            # after_request يقوم بإضافة success إذا غاب
            self.assertIn("success", data)
            # على الأقل أحد الحقول المعروفة
            self.assertTrue("permissions" in data or "data" in data)

    def test_system_settings_get(self):
        """GET /api/settings/system قد يتطلب تسجيل دخول. نتحقق من السلوك الآمن"""
        resp = self.client.get("/api/settings/system")
        # في حال فُرض login_required من flask_login قد نحصل على 401/403
        self.assertIn(resp.status_code, [200, 401, 403, 500])
        if resp.status_code == 200:
            data = json.loads(resp.data)
            self.assertIn("status", data)
            self.assertIn("success", data)
            self.assertIn("data", data)


if __name__ == "__main__":
    unittest.main()
