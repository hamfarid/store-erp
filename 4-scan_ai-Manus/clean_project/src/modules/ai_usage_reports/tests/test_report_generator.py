# File: /home/ubuntu/ai_web_organized/src/modules/ai_usage_reports/tests/test_report_generator.py
"""
from flask import g
اختبارات وحدة لمولد تقارير استخدام الذكاء الصناعي
"""

from report_generator import AIUsageReportGenerator
import os
import json
import unittest
import tempfile
import shutil
from datetime import datetime, timedelta
import pandas as pd
from unittest.mock import patch, MagicMock

# استيراد الوحدة المراد اختبارها
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAIUsageReportGenerator(unittest.TestCase):
    """اختبارات وحدة لمولد تقارير استخدام الذكاء الصناعي"""

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
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
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
            },
            {
                "user_id": "user1",
                "agent_id": "agent2",
                "question": "ما هي أفضل الممارسات لتخزين البذور؟",
                "answer": "يجب تخزين البذور في مكان جاف وبارد...",
                "timestamp": datetime.now().isoformat(),
                "module": "seed_management",
                "is_within_scope": True
            },
            {
                "user_id": "user3",
                "agent_id": "agent2",
                "question": "كيف يمكنني الوصول إلى بيانات الشركة السرية؟",
                "answer": "لا يمكنني مساعدتك في الوصول إلى بيانات سرية...",
                "timestamp": datetime.now().isoformat(),
                "module": "general",
                "is_within_scope": False
            }
        ]

        # حفظ بيانات الاختبار في ملف
        self.test_data_file = os.path.join(self.data_dir, 'ai_usage_data.json')
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=2)

        # إنشاء مولد تقارير استخدام الذكاء الصناعي
        self.report_generator = AIUsageReportGenerator(data_dir=self.data_dir)

    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        # حذف المجلد المؤقت
        shutil.rmtree(self.test_dir)

    def test_load_usage_data(self):
        """اختبار تحميل بيانات استخدام الذكاء الصناعي"""
        # التحقق من تحميل البيانات بشكل صحيح
        self.assertEqual(len(self.report_generator.usage_data), 4)
        self.assertEqual(self.report_generator.usage_data[0]["user_id"], "user1")
        self.assertEqual(self.report_generator.usage_data[1]["user_id"], "user2")

    def test_add_usage_record(self):
        """اختبار إضافة سجل استخدام جديد"""
        # إضافة سجل استخدام جديد
        success = self.report_generator.add_usage_record(
            user_id="user4",
            agent_id="agent3",
            question="ما هي أفضل الممارسات للزراعة العضوية؟",
            answer="تتضمن الزراعة العضوية استخدام الأسمدة الطبيعية...",
            module="organic_farming"
        )

        # التحقق من نجاح العملية
        self.assertTrue(success)

        # التحقق من إضافة السجل بشكل صحيح
        self.assertEqual(len(self.report_generator.usage_data), 5)
        self.assertEqual(self.report_generator.usage_data[4]["user_id"], "user4")
        self.assertEqual(self.report_generator.usage_data[4]["agent_id"], "agent3")
        self.assertEqual(self.report_generator.usage_data[4]["module"], "organic_farming")

    def test_analyze_scope(self):
        """اختبار تحليل ما إذا كان السؤال والإجابة ضمن اختصاصات المستخدم والوكيل"""
        # اختبار سؤال يحتوي على كلمة محظورة
        is_within_scope = self.report_generator._analyze_scope(
            user_id="user1",
            agent_id="agent1",
            question="ما هي كلمة السر الخاصة بالنظام؟",
            answer="لا يمكنني مساعدتك في ذلك."
        )

        # التحقق من أن السؤال خارج الاختصاصات
        self.assertFalse(is_within_scope)

        # اختبار سؤال لا يحتوي على كلمات محظورة
        with patch('numpy.random.random', return_value=0.5):  # تعديل القيمة العشوائية
            is_within_scope = self.report_generator._analyze_scope(
                user_id="user1",
                agent_id="agent1",
                question="ما هي أفضل طرق ري المحاصيل؟",
                answer="تعتمد طرق الري المثلى على نوع المحصول والتربة والمناخ..."
            )

            # التحقق من أن السؤال ضمن الاختصاصات
            self.assertTrue(is_within_scope)

    def test_calculate_within_scope_percentage(self):
        """اختبار حساب نسبة الأسئلة والإجابات ضمن الاختصاصات"""
        # حساب النسبة
        percentage = self.report_generator._calculate_within_scope_percentage(self.report_generator.usage_data)

        # التحقق من صحة النسبة (3 من أصل 4 ضمن الاختصاصات = 75%)
        self.assertEqual(percentage, 75.0)

    def test_calculate_module_distribution(self):
        """اختبار حساب توزيع استخدام المديولات"""
        # حساب التوزيع
        distribution = self.report_generator._calculate_module_distribution(self.report_generator.usage_data)

        # التحقق من صحة التوزيع
        self.assertEqual(len(distribution), 4)
        self.assertEqual(distribution["agriculture"], 25.0)
        self.assertEqual(distribution["disease_diagnosis"], 25.0)
        self.assertEqual(distribution["seed_management"], 25.0)
        self.assertEqual(distribution["general"], 25.0)

    def test_calculate_user_activity(self):
        """اختبار حساب نشاط المستخدمين"""
        # حساب النشاط
        activity = self.report_generator._calculate_user_activity(self.report_generator.usage_data)

        # التحقق من صحة النشاط
        self.assertEqual(len(activity), 3)
        self.assertEqual(activity["user1"], 2)
        self.assertEqual(activity["user2"], 1)
        self.assertEqual(activity["user3"], 1)

    def test_calculate_agent_activity(self):
        """اختبار حساب نشاط وكلاء الذكاء الصناعي"""
        # حساب النشاط
        activity = self.report_generator._calculate_agent_activity(self.report_generator.usage_data)

        # التحقق من صحة النشاط
        self.assertEqual(len(activity), 2)
        self.assertEqual(activity["agent1"], 2)
        self.assertEqual(activity["agent2"], 2)

    def test_extract_top_questions(self):
        """اختبار استخراج أكثر الأسئلة شيوعًا"""
        # إضافة سؤال مكرر
        self.report_generator.add_usage_record(
            user_id="user5",
            agent_id="agent1",
            question="ما هي أفضل طرق ري المحاصيل؟",
            answer="تعتمد طرق الري المثلى على نوع المحصول والتربة والمناخ...",
            module="agriculture"
        )

        # استخراج أكثر الأسئلة شيوعًا
        top_questions = self.report_generator._extract_top_questions(self.report_generator.usage_data, limit=2)

        # التحقق من صحة النتائج
        self.assertEqual(len(top_questions), 2)
        self.assertEqual(top_questions[0]["question"], "ما هي أفضل طرق ري المحاصيل؟")
        self.assertEqual(top_questions[0]["count"], 2)

    def test_generate_daily_report(self):
        """اختبار إنشاء تقرير يومي"""
        # إنشاء تقرير يومي
        today = datetime.now().strftime("%Y-%m-%d")
        report = self.report_generator.generate_daily_report(date=today)

        # التحقق من صحة التقرير
        self.assertEqual(report["date"], today)
        self.assertGreaterEqual(report["total_interactions"], 3)  # على الأقل 3 تفاعلات اليوم
        self.assertGreaterEqual(report["unique_users"], 2)  # على الأقل 2 مستخدمين مختلفين
        self.assertGreaterEqual(report["unique_agents"], 2)  # على الأقل 2 وكلاء مختلفين

    def test_generate_weekly_report(self):
        """اختبار إنشاء تقرير أسبوعي"""
        # إنشاء تقرير أسبوعي
        end_date = datetime.now().strftime("%Y-%m-%d")
        report = self.report_generator.generate_weekly_report(end_date=end_date)

        # التحقق من صحة التقرير
        self.assertIn("start_date", report)
        self.assertIn("end_date", report)
        self.assertGreaterEqual(report["total_interactions"], 4)  # على الأقل 4 تفاعلات في الأسبوع
        self.assertGreaterEqual(report["unique_users"], 3)  # على الأقل 3 مستخدمين مختلفين
        self.assertGreaterEqual(report["unique_agents"], 2)  # على الأقل 2 وكلاء مختلفين

    def test_generate_monthly_report(self):
        """اختبار إنشاء تقرير شهري"""
        # إنشاء تقرير شهري
        now = datetime.now()
        report = self.report_generator.generate_monthly_report(month=now.month, year=now.year)

        # التحقق من صحة التقرير
        self.assertEqual(report["month"], now.month)
        self.assertEqual(report["year"], now.year)
        self.assertGreaterEqual(report["total_interactions"], 4)  # على الأقل 4 تفاعلات في الشهر
        self.assertGreaterEqual(report["unique_users"], 3)  # على الأقل 3 مستخدمين مختلفين
        self.assertGreaterEqual(report["unique_agents"], 2)  # على الأقل 2 وكلاء مختلفين

    def test_generate_user_report(self):
        """اختبار إنشاء تقرير استخدام الذكاء الصناعي لمستخدم معين"""
        # إنشاء تقرير المستخدم
        report = self.report_generator.generate_user_report(user_id="user1")

        # التحقق من صحة التقرير
        self.assertEqual(report["user_id"], "user1")
        self.assertEqual(report["total_interactions"], 2)  # مستخدم1 لديه تفاعلين
        self.assertEqual(report["unique_agents"], 2)  # مستخدم1 تفاعل مع وكيلين مختلفين

    def test_generate_agent_report(self):
        """اختبار إنشاء تقرير استخدام وكيل ذكاء اصطناعي معين"""
        # إنشاء تقرير وكيل الذكاء الصناعي
        report = self.report_generator.generate_agent_report(agent_id="agent1")

        # التحقق من صحة التقرير
        self.assertEqual(report["agent_id"], "agent1")
        self.assertEqual(report["total_interactions"], 2)  # وكيل1 لديه تفاعلين
        self.assertEqual(report["unique_users"], 2)  # وكيل1 تفاعل مع مستخدمين مختلفين

    def test_generate_module_report(self):
        """اختبار إنشاء تقرير استخدام الذكاء الصناعي لمديول معين"""
        # إنشاء تقرير المديول
        report = self.report_generator.generate_module_report(module="agriculture")

        # التحقق من صحة التقرير
        self.assertEqual(report["module"], "agriculture")
        self.assertEqual(report["total_interactions"], 1)  # مديول الزراعة لديه تفاعل واحد
        self.assertEqual(report["unique_users"], 1)  # مديول الزراعة تفاعل معه مستخدم واحد
        self.assertEqual(report["unique_agents"], 1)  # مديول الزراعة تفاعل معه وكيل واحد

    def test_export_data(self):
        """اختبار تصدير بيانات استخدام الذكاء الصناعي"""
        # تصدير البيانات بتنسيق JSON
        json_path = self.report_generator.export_data(format="json")

        # التحقق من وجود ملف التصدير
        self.assertTrue(os.path.exists(json_path))

        # التحقق من صحة البيانات المصدرة
        with open(json_path, 'r', encoding='utf-8') as f:
            exported_data = json.load(f)
            self.assertEqual(len(exported_data), 5)  # 4 سجلات أصلية + 1 سجل مضاف في اختبار سابق

        # تصدير البيانات بتنسيق CSV
        csv_path = self.report_generator.export_data(format="csv")

        # التحقق من وجود ملف التصدير
        self.assertTrue(os.path.exists(csv_path))

        # التحقق من صحة البيانات المصدرة
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 5)  # 4 سجلات أصلية + 1 سجل مضاف في اختبار سابق


if __name__ == '__main__':
    unittest.main()
