from modules.ai_management.api import ai_management_api, load_data, save_data, init_default_data
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from functools import wraps
# File: /home/ubuntu/ai_web_organized/src/modules/ai_management/tests/test_api.py
"""
from flask import g
اختبارات وحدة لواجهة برمجة التطبيقات لإدارة الذكاء الصناعي
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# إضافة المسار الرئيسي للمشروع إلى مسارات البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))


class TestAIManagementAPI(unittest.TestCase):
    """اختبارات وحدة لواجهة برمجة التطبيقات لإدارة الذكاء الصناعي"""

    def setUp(self):
        """إعداد بيئة الاختبار"""
        # إنشاء مجلد مؤقت للاختبارات
        self.test_dir = tempfile.mkdtemp()

        # تعديل مسارات الملفات للاختبارات
        self.original_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
        self.patcher = patch('modules.ai_management.api.DATA_DIR', self.test_dir)
        self.mock_data_dir = self.patcher.start()

        # تعديل مسارات الملفات
        self.agents_file = os.path.join(self.test_dir, 'agents.json')
        self.stats_file = os.path.join(self.test_dir, 'stats.json')
        self.settings_file = os.path.join(self.test_dir, 'settings.json')
        self.permissions_file = os.path.join(self.test_dir, 'permissions.json')

        # تهيئة البيانات الافتراضية للاختبارات
        init_default_data()

    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        # إيقاف التعديلات
        self.patcher.stop()

        # حذف المجلد المؤقت
        shutil.rmtree(self.test_dir)

    def test_load_data(self):
        """اختبار تحميل البيانات من ملف JSON"""
        # إنشاء بيانات اختبار
        test_data = {"test": "data"}
        test_file = os.path.join(self.test_dir, 'test.json')

        # حفظ البيانات في ملف
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        # اختبار تحميل البيانات
        loaded_data = load_data(test_file)
        self.assertEqual(loaded_data, test_data)

        # اختبار تحميل البيانات من ملف غير موجود
        non_existent_file = os.path.join(self.test_dir, 'non_existent.json')
        default_data = {"default": "data"}
        loaded_data = load_data(non_existent_file, default_data)
        self.assertEqual(loaded_data, default_data)

        # التحقق من إنشاء الملف بالبيانات الافتراضية
        self.assertTrue(os.path.exists(non_existent_file))
        with open(non_existent_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, default_data)

    def test_save_data(self):
        """اختبار حفظ البيانات في ملف JSON"""
        # إنشاء بيانات اختبار
        test_data = {"test": "save_data"}
        test_file = os.path.join(self.test_dir, 'test_save.json')

        # حفظ البيانات
        save_data(test_file, test_data)

        # التحقق من حفظ البيانات بشكل صحيح
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, test_data)

    def test_init_default_data(self):
        """اختبار تهيئة البيانات الافتراضية"""
        # التحقق من إنشاء ملفات البيانات
        self.assertTrue(os.path.exists(self.agents_file))
        self.assertTrue(os.path.exists(self.stats_file))
        self.assertTrue(os.path.exists(self.settings_file))
        self.assertTrue(os.path.exists(self.permissions_file))

        # التحقق من محتوى ملفات البيانات
        with open(self.agents_file, 'r', encoding='utf-8') as f:
            agents_data = json.load(f)
        self.assertIn('agents', agents_data)
        self.assertTrue(len(agents_data['agents']) > 0)

        with open(self.stats_file, 'r', encoding='utf-8') as f:
            stats_data = json.load(f)
        self.assertIn('totalRequests', stats_data)
        self.assertIn('modelUsage', stats_data)
        self.assertIn('dailyUsage', stats_data)

        with open(self.settings_file, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)
        self.assertIn('defaultModel', settings_data)
        self.assertIn('resourceLimits', settings_data)
        self.assertIn('autoSuspend', settings_data)

        with open(self.permissions_file, 'r', encoding='utf-8') as f:
            permissions_data = json.load(f)
        self.assertIn('roles', permissions_data)
        self.assertIn('userRoles', permissions_data)
        self.assertIn('agentRoles', permissions_data)


# تشغيل الاختبارات إذا تم تنفيذ الملف مباشرة
if __name__ == '__main__':
    unittest.main()
