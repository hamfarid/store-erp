from report_generator import AIUsageReportGenerator
from api import ai_usage_reports_api, register_api
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from functools import wraps
# File: /home/ubuntu/ai_web_organized/src/modules/ai_usage_reports/tests/test_api.py
"""
اختبارات تكامل لواجهة برمجة التطبيقات لمديول تقارير استخدام الذكاء الصناعي
"""

import os
import json
import unittest
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock
import io

# استيراد الوحدة المراد اختبارها
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAIUsageReportsAPI(unittest.TestCase):
    """اختبارات تكامل لواجهة برمجة التطبيقات لمديول تقارير استخدام الذكاء الصناعي"""

    def setUp(self):
        """إعداد بيئة الاختبار"""
        # إنشاء مجلد مؤقت للاختبار
        self.test_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.test_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)

        # إنشاء بيانات اختبار
        self.test_data = [
            {
                "user_id": "user1",
                "agent_id": "agent1",
                "question": "ما هي أفضل طرق ري المحاصيل؟",
                "answer": "تعتمد طرق الري المثلى على نوع المحصول والتربة والمناخ...",
                "timestamp": datetime.now().isoformat(),
                "module": "agriculture",
                "is_within_scope": True
            },
            {
                "user_id": "user2",
                "agent_id": "agent1",
                "question": "كيف يمكنني تشخيص مرض البياض الدقيقي في النباتات؟",
                "answer": "يمكن تشخيص مرض البياض الدقيقي من خلال ظهور بقع بيضاء...",
                "timestamp": datetime.now().isoformat(),
                "module": "disease_diagnosis",
                "is_within_scope": True
            }
        ]

        # حفظ بيانات الاختبار في ملف
        self.test_data_file = os.path.join(self.data_dir, 'ai_usage_data.json')
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=2)

        # إنشاء تطبيق Flask للاختبار
        self.app = Flask(__name__)

        # تعديل مولد تقارير استخدام الذكاء الصناعي ليستخدم مجلد الاختبار
        with patch('api.AIUsageReportGenerator') as mock_generator:
            mock_instance = MagicMock()
            mock_generator.return_value = mock_instance

            # تسجيل واجهة برمجة التطبيقات في التطبيق
            register_api(self.app)

            # تخزين النسخة المعدلة من مولد التقارير
            self.report_generator = mock_instance

        # إنشاء عميل اختبار
        self.client = self.app.test_client()

    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        # حذف المجلد المؤقت
        shutil.rmtree(self.test_dir)

    def test_add_usage_record(self):
        """اختبار إضافة سجل استخدام جديد"""
        # تعيين سلوك مولد التقارير المعدل
        self.report_generator.add_usage_record.return_value = True

        # إرسال طلب إضافة سجل استخدام جديد
        response = self.client.post('/api/ai_usage_reports/add_usage_record', json={
            "user_id": "user3",
            "agent_id": "agent2",
            "question": "ما هي أفضل الممارسات للزراعة العضوية؟",
            "answer": "تتضمن الزراعة العضوية استخدام الأسمدة الطبيعية...",
            "module": "organic_farming"
        })

        # التحقق من نجاح العملية
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data["success"])

        # التحقق من استدعاء مولد التقارير بشكل صحيح
        self.report_generator.add_usage_record.assert_called_once_with(
            user_id="user3",
            agent_id="agent2",
            question="ما هي أفضل الممارسات للزراعة العضوية؟",
            answer="تتضمن الزراعة العضوية استخدام الأسمدة الطبيعية...",
            timestamp=None,
            module="organic_farming",
            is_within_scope=None
        )

    def test_add_usage_record_missing_fields(self):
        """اختبار إضافة سجل استخدام جديد مع حقول مفقودة"""
        # إرسال طلب إضافة سجل استخدام جديد مع حقول مفقودة
        response = self.client.post('/api/ai_usage_reports/add_usage_record', json={
            "user_id": "user3",
            "agent_id": "agent2",
            # حقل السؤال مفقود
            "answer": "تتضمن الزراعة العضوية استخدام الأسمدة الطبيعية..."
        })

        # التحقق من فشل العملية
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])

    def test_daily_report(self):
        """اختبار إنشاء تقرير يومي"""
        # تعيين سلوك مولد التقارير المعدل
        mock_report = {
            "date": "2025-05-17",
            "total_interactions": 10,
            "unique_users": 5,
            "unique_agents": 3,
            "within_scope_percentage": 90.0,
            "module_distribution": {
                "agriculture": 40.0,
                "disease_diagnosis": 30.0,
                "seed_management": 20.0,
                "general": 10.0
            }
        }
        self.report_generator.generate_daily_report.return_value = mock_report

        # إرسال طلب إنشاء تقرير يومي
        response = self.client.get('/api/ai_usage_reports/daily_report?date=2025-05-17')

        # التحقق من نجاح العملية
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["date"], "2025-05-17")
        self.assertEqual(data["total_interactions"], 10)

        # التحقق من استدعاء مولد التقارير بشكل صحيح
        self.report_generator.generate_daily_report.assert_called_once_with(date="2025-05-17")

    def test_weekly_report(self):
        """اختبار إنشاء تقرير أسبوعي"""
        # تعيين سلوك مولد التقارير المعدل
        mock_report = {
            "start_date": "2025-05-10",
            "end_date": "2025-05-17",
            "total_interactions": 50,
            "unique_users": 15,
            "unique_agents": 5,
            "within_scope_percentage": 85.0,
            "module_distribution": {
                "agriculture": 35.0,
                "disease_diagnosis": 25.0,
                "seed_management": 20.0,
                "general": 20.0
            }
        }
        self.report_generator.generate_weekly_report.return_value = mock_report

        # إرسال طلب إنشاء تقرير أسبوعي
        response = self.client.get('/api/ai_usage_reports/weekly_report?end_date=2025-05-17')

        # التحقق من نجاح العملية
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["start_date"], "2025-05-10")
        self.assertEqual(data["end_date"], "2025-05-17")
        self.assertEqual(data["total_interactions"], 50)

        # التحقق من استدعاء مولد التقارير بشكل صحيح
        self.report_generator.generate_weekly_report.assert_called_once_with(end_date="2025-05-17")

    def test_monthly_report(self):
        """اختبار إنشاء تقرير شهري"""
        # تعيين سلوك مولد التقارير المعدل
        mock_report = {
            "month": 5,
            "year": 2025,
            "total_interactions": 200,
            "unique_users": 50,
            "unique_agents": 10,
            "within_scope_percentage": 80.0,
            "module_distribution": {
                "agriculture": 30.0,
                "disease_diagnosis": 25.0,
                "seed_management": 20.0,
                "general": 25.0
            }
        }
        self.report_generator.generate_monthly_report.return_value = mock_report

        # إرسال طلب إنشاء تقرير شهري
        response = self.client.get('/api/ai_usage_reports/monthly_report?month=5&year=2025')

        # التحقق من نجاح العملية
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["month"], 5)
        self.assertEqual(data["year"], 2025)
        self.assertEqual(data["total_interactions"], 200)

        # التحقق من استدعاء مولد التقارير بشكل صحيح
        self.report_generator.generate_monthly_report.assert_called_once_with(month=5, year=2025)

    def test_user_report(self):
        """اختبار إنشاء تقرير استخدام الذكاء الصناعي لمستخدم معين"""
        # تعيين سلوك مولد التقارير المعدل
        mock_report = {
            "user_id": "user1",
            "start_date": "2025-05-01",
            "end_date": "2025-05-17",
            "total_interactions": 30,
            "unique_agents": 5,
            "within_scope_percentage": 95.0,
            "module_distribution": {
                "agriculture": 50.0,
                "disease_diagnosis": 30.0,
                "seed_management": 20.0
            }
        }
        self.report_generator.generate_user_report.return_value = mock_report

        # إرسال طلب إنشاء تقرير المستخدم
        response = self.client.get('/api/ai_usage_reports/user_report?user_id=user1&start_date=2025-05-01&end_date=2025-05-17')

        # التحقق من نجاح العملية
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["user_id"], "user1")
        self.assertEqual(data["total_interactions"], 30)

        # التحقق من استدعاء مولد التقارير بشكل صحيح
        self.report_generator.generate_user_report.assert_called_once_with(
            user_id="user1",
            start_date="2025-05-01",
            end_date="2025-05-17"
        )

    def test_user_report_missing_user_id(self):
        """اختبار إنشاء تقرير استخدام الذكاء الصناعي لمستخدم معين مع معرف مستخدم مفقود"""
        # إرسال طلب إنشاء تقرير المستخدم مع معرف مستخدم مفقود
        response = self.client.get('/api/ai_usage_reports/user_report?start_date=2025-05-01&end_date=2025-05-17')

        # التحقق من فشل العملية
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])

    def test_agent_report(self):
        """اختبار إنشاء تقرير استخدام وكيل ذكاء اصطناعي معين"""
        # تعيين سلوك مولد التقارير المعدل
        mock_report = {
            "agent_id": "agent1",
            "start_date": "2025-05-01",
            "end_date": "2025-05-17",
            "total_interactions": 40,
            "unique_users": 20,
            "within_scope_percentage": 90.0,
            "module_distribution": {
                "agriculture": 40.0,
                "disease_diagnosis": 30.0,
                "seed_management": 20.0,
                "general": 10.0
            }
        }
        self.report_generator.generate_agent_report.return_value = mock_report

        # إرسال طلب إنشاء تقرير وكيل الذكاء الصناعي
        response = self.client.get('/api/ai_usage_reports/agent_report?agent_id=agent1&start_date=2025-05-01&end_date=2025-05-17')

        # التحقق من نجاح العملية
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["agent_id"], "agent1")
        self.assertEqual(data["total_interactions"], 40)

        # التحقق من استدعاء مولد التقارير بشكل صحيح
        self.report_generator.generate_agent_report.assert_called_once_with(
            agent_id="agent1",
            start_date="2025-05-01",
            end_date="2025-05-17"
        )

    def test_module_report(self):
        """اختبار إنشاء تقرير استخدام الذكاء الصناعي لمديول معين"""
        # تعيين سلوك مولد التقارير المعدل
        mock_report = {
            "module": "agriculture",
            "start_date": "2025-05-01",
            "end_date": "2025-05-17",
            "total_interactions": 80,
            "unique_users": 30,
            "unique_agents": 8,
            "within_scope_percentage": 95.0
        }
        self.report_generator.generate_module_report.return_value = mock_report

        # إرسال طلب إنشاء تقرير المديول
        response = self.client.get('/api/ai_usage_reports/module_report?module=agriculture&start_date=2025-05-01&end_date=2025-05-17')

        # التحقق من نجاح العملية
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["module"], "agriculture")
        self.assertEqual(data["total_interactions"], 80)

        # التحقق من استدعاء مولد التقارير بشكل صحيح
        self.report_generator.generate_module_report.assert_called_once_with(
            module="agriculture",
            start_date="2025-05-01",
            end_date="2025-05-17"
        )

    def test_export_data(self):
        """اختبار تصدير بيانات استخدام الذكاء الصناعي"""
        # تعيين سلوك مولد التقارير المعدل
        mock_export_path = os.path.join(self.test_dir, 'ai_usage_data_20250517_123456.json')
        with open(mock_export_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=2)

        self.report_generator.export_data.return_value = mock_export_path

        # إرسال طلب تصدير البيانات
        with patch('api.send_file', return_value=jsonify({"success": True})) as mock_send_file:
            response = self.client.get('/api/ai_usage_reports/export_data?format=json&start_date=2025-05-01&end_date=2025-05-17&module=agriculture')

            # التحقق من نجاح العملية
            self.assertEqual(response.status_code, 200)

            # التحقق من استدعاء مولد التقارير بشكل صحيح
            self.report_generator.export_data.assert_called_once_with(
                format="json",
                start_date="2025-05-01",
                end_date="2025-05-17",
                module="agriculture"
            )

            # التحقق من استدعاء send_file بشكل صحيح
            mock_send_file.assert_called_once_with(mock_export_path, as_attachment=True)

    def test_visual_report(self):
        """اختبار الحصول على التقرير المرئي"""
        # تعيين سلوك مولد التقارير المعدل
        mock_report = {
            "date": "2025-05-17",
            "total_interactions": 10,
            "unique_users": 5,
            "unique_agents": 3,
            "within_scope_percentage": 90.0,
            "module_distribution": {
                "agriculture": 40.0,
                "disease_diagnosis": 30.0,
                "seed_management": 20.0,
                "general": 10.0
            }
        }
        self.report_generator.generate_daily_report.return_value = mock_report

        # إنشاء ملف رسم بياني وهمي
        mock_chart_path = os.path.join(self.test_dir, 'daily_visual_report_2025-05-17_module_distribution.png')
        with open(mock_chart_path, 'wb') as f:
            f.write(b'PNG')

        # تعديل مسار الرسم البياني
        with patch('os.path.exists', return_value=True), \
                patch('os.path.join', return_value=mock_chart_path), \
                patch('api.send_file', return_value=jsonify({"success": True})) as mock_send_file:

            # إرسال طلب الحصول على التقرير المرئي
            response = self.client.get('/api/ai_usage_reports/visual_report/daily?date=2025-05-17&chart_type=module_distribution')

            # التحقق من نجاح العملية
            self.assertEqual(response.status_code, 200)

            # التحقق من استدعاء مولد التقارير بشكل صحيح
            self.report_generator.generate_daily_report.assert_called_once_with(date="2025-05-17")

            # التحقق من استدعاء send_file بشكل صحيح
            mock_send_file.assert_called_once()


if __name__ == '__main__':
    unittest.main()
