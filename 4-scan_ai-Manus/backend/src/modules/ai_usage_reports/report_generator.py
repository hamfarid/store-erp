# File:
# /home/ubuntu/ai_web_organized/src/modules/ai_usage_reports/report_generator.py
"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/ai_usage_reports/report_generator.py
الوصف: مولد تقارير استخدام الذكاء الصناعي
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import json
import logging
import os
from collections import Counter
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants for repeated string literals
INTERACTIONS_COUNT_LABEL = 'عدد التفاعلات'


class AIUsageReportGenerator:
    """مولد تقارير استخدام الذكاء الصناعي"""

    def __init__(self, data_dir=None):
        """تهيئة مولد التقارير"""
        # مسار حفظ البيانات
        if data_dir:
            self.data_dir = data_dir
        else:
            self.data_dir = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)), 'data')

        # مسار حفظ التقارير
        self.reports_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'reports')

        # إنشاء المجلدات إذا لم تكن موجودة
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

        # مسار ملف بيانات استخدام الذكاء الصناعي
        self.usage_data_file = os.path.join(
            self.data_dir, 'ai_usage_data.json')

        # تحميل بيانات الاستخدام
        self.usage_data = self._load_usage_data()

        logger.info("تم تهيئة مولد تقارير استخدام الذكاء الصناعي")

    def _load_usage_data(self):
        """
        تحميل بيانات استخدام الذكاء الصناعي

        العائد:
            list: بيانات استخدام الذكاء الصناعي
        """
        try:
            if os.path.exists(self.usage_data_file):
                with open(self.usage_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # إنشاء ملف بيانات فارغ
                with open(self.usage_data_file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                return []

        except Exception as e:
            logger.error(
                "خطأ أثناء تحميل بيانات استخدام الذكاء الصناعي: %s",
                str(e))
            return []

    def _save_usage_data(self):
        """حفظ بيانات استخدام الذكاء الصناعي"""
        try:
            with open(self.usage_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_data, f, ensure_ascii=False, indent=2)

            logger.info("تم حفظ بيانات استخدام الذكاء الصناعي")

        except Exception as e:
            logger.error(
                "خطأ أثناء حفظ بيانات استخدام الذكاء الصناعي: %s",
                str(e))

    def add_usage_record(
            self,
            user_id,
            agent_id,
            question,
            answer,
            timestamp=None,
            module=None,
            is_within_scope=None):
        """
        إضافة سجل استخدام جديد

        المعلمات:
            user_id (str): معرف المستخدم
            agent_id (str): معرف وكيل الذكاء الصناعي
            question (str): السؤال المطروح
            answer (str): الإجابة المقدمة
            timestamp (str, optional): الطابع الزمني
            module (str, optional): المديول المستخدم
            is_within_scope (bool, optional): هل السؤال والإجابة ضمن اختصاصات المستخدم والوكيل

        العائد:
            bool: نجاح العملية
        """
        try:
            # إنشاء سجل استخدام جديد
            usage_record = {
                "user_id": user_id,
                "agent_id": agent_id,
                "question": question,
                "answer": answer,
                "timestamp": timestamp or datetime.now().isoformat(),
                "module": module or "general"
            }

            # إضافة تحليل ما إذا كان السؤال والإجابة ضمن اختصاصات المستخدم
            # والوكيل
            if is_within_scope is not None:
                usage_record["is_within_scope"] = is_within_scope
            else:
                # تحليل تلقائي (محاكاة)
                usage_record["is_within_scope"] = self._analyze_scope(
                    user_id, agent_id, question, answer)

            # إضافة السجل إلى بيانات الاستخدام
            self.usage_data.append(usage_record)

            # حفظ بيانات الاستخدام
            self._save_usage_data()

            logger.info("تم إضافة سجل استخدام جديد للمستخدم: %s", user_id)

            return True

        except Exception as e:
            logger.error("خطأ أثناء إضافة سجل استخدام: %s", str(e))
            return False

    def _analyze_scope(self, user_id, agent_id, question, answer):
        """
        تحليل ما إذا كان السؤال والإجابة ضمن اختصاصات المستخدم والوكيل

        المعلمات:
            user_id (str): معرف المستخدم
            agent_id (str): معرف وكيل الذكاء الصناعي
            question (str): السؤال المطروح
            answer (str): الإجابة المقدمة

        العائد:
            bool: هل السؤال والإجابة ضمن اختصاصات المستخدم والوكيل
        """
        try:
            # في التطبيق الحقيقي، سيتم استخدام نموذج ذكاء اصطناعي مركزي لتحليل السؤال والإجابة
            # هذه مجرد محاكاة بسيطة

            # قائمة الكلمات المحظورة (مثال)
            forbidden_words = [
                "كلمة_سر",
                "password",
                "خاص",
                "سري",
                "private",
                "secret"]

            # التحقق من وجود كلمات محظورة في السؤال أو الإجابة
            for word in forbidden_words:
                if word in question.lower() or word in answer.lower():
                    return False

            # محاكاة: 90% من الأسئلة والإجابات ضمن الاختصاصات
            return np.random.default_rng(42).random() < 0.9

        except Exception as e:
            logger.error("خطأ أثناء تحليل نطاق السؤال والإجابة: %s", str(e))
            return True  # افتراضيًا، نفترض أن السؤال والإجابة ضمن الاختصاصات

    def generate_daily_report(self, date=None):
        """
        إنشاء تقرير يومي لاستخدام الذكاء الصناعي

        المعلمات:
            date (str, optional): التاريخ (بتنسيق YYYY-MM-DD)

        العائد:
            dict: تقرير استخدام الذكاء الصناعي
        """
        try:
            # تحديد التاريخ
            if date:
                report_date = datetime.strptime(date, "%Y-%m-%d")
            else:
                report_date = datetime.now()

            # تحديد بداية ونهاية اليوم
            start_of_day = datetime(
                report_date.year,
                report_date.month,
                report_date.day).isoformat()
            end_of_day = (
                datetime(
                    report_date.year,
                    report_date.month,
                    report_date.day) +
                timedelta(
                    days=1) -
                timedelta(
                    microseconds=1)).isoformat()

            # فلترة بيانات الاستخدام حسب التاريخ
            daily_usage = [
                record for record in self.usage_data if start_of_day <= record["timestamp"] <= end_of_day]

            # إنشاء تقرير
            report = {
                "date": report_date.strftime("%Y-%m-%d"),
                "total_interactions": len(daily_usage),
                "unique_users": len(set(record["user_id"] for record in daily_usage)),
                "unique_agents": len(set(record["agent_id"] for record in daily_usage)),
                "within_scope_percentage": self._calculate_within_scope_percentage(daily_usage),
                "module_distribution": self._calculate_module_distribution(daily_usage),
                "user_activity": self._calculate_user_activity(daily_usage),
                "agent_activity": self._calculate_agent_activity(daily_usage),
                "top_questions": self._extract_top_questions(daily_usage),
                "interactions": daily_usage
            }

            # حفظ التقرير
            report_filename = f"daily_report_{report_date.strftime('%Y%m%d')}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            logger.info("تم إنشاء التقرير اليومي: %s", report_path)

            # إنشاء تقرير مرئي
            self._generate_visual_report(report, "daily")

            return report

        except Exception as e:
            logger.error("خطأ أثناء إنشاء التقرير اليومي: %s", str(e))
            return {
                "error": f"خطأ أثناء إنشاء التقرير اليومي: {str(e)}",
                "date": datetime.now().strftime("%Y-%m-%d")
            }

    def generate_weekly_report(self, end_date=None):
        """
        إنشاء تقرير أسبوعي لاستخدام الذكاء الصناعي

        المعلمات:
            end_date (str, optional): تاريخ نهاية الأسبوع (بتنسيق YYYY-MM-DD)

        العائد:
            dict: تقرير استخدام الذكاء الصناعي
        """
        try:
            # تحديد تاريخ نهاية الأسبوع
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            else:
                end_date = datetime.now()

            # تحديد بداية ونهاية الأسبوع
            start_of_week = (
                end_date -
                timedelta(
                    days=end_date.weekday() +
                    7)).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0).isoformat()
            end_of_week = (
                end_date -
                timedelta(
                    days=end_date.weekday()) -
                timedelta(
                    microseconds=1)).isoformat()

            # فلترة بيانات الاستخدام حسب التاريخ
            weekly_usage = [
                record for record in self.usage_data if start_of_week <= record["timestamp"] <= end_of_week]

            # إنشاء تقرير
            report = {
                "start_date": start_of_week.split('T')[0],
                "end_date": end_of_week.split('T')[0],
                "total_interactions": len(weekly_usage),
                "unique_users": len(set(record["user_id"] for record in weekly_usage)),
                "unique_agents": len(set(record["agent_id"] for record in weekly_usage)),
                "within_scope_percentage": self._calculate_within_scope_percentage(weekly_usage),
                "module_distribution": self._calculate_module_distribution(weekly_usage),
                "user_activity": self._calculate_user_activity(weekly_usage),
                "agent_activity": self._calculate_agent_activity(weekly_usage),
                "top_questions": self._extract_top_questions(weekly_usage),
                "daily_activity": self._calculate_daily_activity(weekly_usage, start_of_week, end_of_week)
            }

            # حفظ التقرير
            report_filename = f"weekly_report_{start_of_week.split('T')[0]}_{end_of_week.split('T')[0]}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            logger.info("تم إنشاء التقرير الأسبوعي: %s", report_path)

            # إنشاء تقرير مرئي
            self._generate_visual_report(report, "weekly")

            return report

        except Exception as e:
            logger.error("خطأ أثناء إنشاء التقرير الأسبوعي: %s", str(e))
            return {
                "error": f"خطأ أثناء إنشاء التقرير الأسبوعي: {str(e)}",
                "end_date": datetime.now().strftime("%Y-%m-%d")
            }

    def generate_monthly_report(self, month=None, year=None):
        """
        إنشاء تقرير شهري لاستخدام الذكاء الصناعي

        المعلمات:
            month (int, optional): الشهر (1-12)
            year (int, optional): السنة

        العائد:
            dict: تقرير استخدام الذكاء الصناعي
        """
        try:
            # تحديد الشهر والسنة
            if month is None or year is None:
                now = datetime.now()
                month = now.month
                year = now.year

            # تحديد بداية ونهاية الشهر
            start_of_month = datetime(year, month, 1).isoformat()
            if month == 12:
                end_of_month = datetime(
                    year + 1, 1, 1) - timedelta(microseconds=1)
            else:
                end_of_month = datetime(
                    year, month + 1, 1) - timedelta(microseconds=1)
            end_of_month = end_of_month.isoformat()

            # فلترة بيانات الاستخدام حسب التاريخ
            monthly_usage = [
                record for record in self.usage_data if start_of_month <= record["timestamp"] <= end_of_month]

            # إنشاء تقرير
            report = {
                "month": month,
                "year": year,
                "total_interactions": len(monthly_usage),
                "unique_users": len(set(record["user_id"] for record in monthly_usage)),
                "unique_agents": len(set(record["agent_id"] for record in monthly_usage)),
                "within_scope_percentage": self._calculate_within_scope_percentage(monthly_usage),
                "module_distribution": self._calculate_module_distribution(monthly_usage),
                "user_activity": self._calculate_user_activity(monthly_usage),
                "agent_activity": self._calculate_agent_activity(monthly_usage),
                "top_questions": self._extract_top_questions(monthly_usage),
                "weekly_activity": self._calculate_weekly_activity(monthly_usage, start_of_month, end_of_month)
            }

            # حفظ التقرير
            report_filename = f"monthly_report_{year}_{month:02d}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            logger.info("تم إنشاء التقرير الشهري: %s", report_path)

            # إنشاء تقرير مرئي
            self._generate_visual_report(report, "monthly")

            return report

        except Exception as e:
            logger.error("خطأ أثناء إنشاء التقرير الشهري: %s", str(e))
            return {
                "error": f"خطأ أثناء إنشاء التقرير الشهري: {str(e)}",
                "month": datetime.now().month,
                "year": datetime.now().year
            }

    def generate_user_report(self, user_id, start_date=None, end_date=None):
        """
        إنشاء تقرير استخدام الذكاء الصناعي لمستخدم معين

        المعلمات:
            user_id (str): معرف المستخدم
            start_date (str, optional): تاريخ البداية (بتنسيق YYYY-MM-DD)
            end_date (str, optional): تاريخ النهاية (بتنسيق YYYY-MM-DD)

        العائد:
            dict: تقرير استخدام الذكاء الصناعي
        """
        try:
            # تحديد تاريخ البداية والنهاية
            if start_date:
                start_date = datetime.strptime(
                    start_date, "%Y-%m-%d").isoformat()
            else:
                start_date = datetime(1970, 1, 1).isoformat()

            if end_date:
                end_date = (
                    datetime.strptime(
                        end_date,
                        "%Y-%m-%d") +
                    timedelta(
                        days=1) -
                    timedelta(
                        microseconds=1)).isoformat()
            else:
                end_date = datetime.now().isoformat()

            # فلترة بيانات الاستخدام حسب المستخدم والتاريخ
            user_usage = [record for record in self.usage_data if record["user_id"]
                          == user_id and start_date <= record["timestamp"] <= end_date]

            # إنشاء تقرير
            report = {
                "user_id": user_id,
                "start_date": start_date.split('T')[0],
                "end_date": end_date.split('T')[0],
                "total_interactions": len(user_usage),
                "unique_agents": len(set(record["agent_id"] for record in user_usage)),
                "within_scope_percentage": self._calculate_within_scope_percentage(user_usage),
                "module_distribution": self._calculate_module_distribution(user_usage),
                "agent_activity": self._calculate_agent_activity(user_usage),
                "top_questions": self._extract_top_questions(user_usage),
                "interactions": user_usage
            }

            # حفظ التقرير
            report_filename = f"user_report_{user_id}_{start_date.split('T')[0]}_{end_date.split('T')[0]}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            logger.info("تم إنشاء تقرير المستخدم: %s", report_path)

            # إنشاء تقرير مرئي
            self._generate_visual_report(report, "user")

            return report

        except Exception as e:
            logger.error("خطأ أثناء إنشاء تقرير المستخدم: %s", str(e))
            return {
                "error": f"خطأ أثناء إنشاء تقرير المستخدم: {str(e)}",
                "user_id": user_id
            }

    def generate_agent_report(self, agent_id, start_date=None, end_date=None):
        """
        إنشاء تقرير استخدام وكيل ذكاء اصطناعي معين

        المعلمات:
            agent_id (str): معرف وكيل الذكاء الصناعي
            start_date (str, optional): تاريخ البداية (بتنسيق YYYY-MM-DD)
            end_date (str, optional): تاريخ النهاية (بتنسيق YYYY-MM-DD)

        العائد:
            dict: تقرير استخدام الذكاء الصناعي
        """
        try:
            # تحديد تاريخ البداية والنهاية
            if start_date:
                start_date = datetime.strptime(
                    start_date, "%Y-%m-%d").isoformat()
            else:
                start_date = datetime(1970, 1, 1).isoformat()

            if end_date:
                end_date = (
                    datetime.strptime(
                        end_date,
                        "%Y-%m-%d") +
                    timedelta(
                        days=1) -
                    timedelta(
                        microseconds=1)).isoformat()
            else:
                end_date = datetime.now().isoformat()

            # فلترة بيانات الاستخدام حسب وكيل الذكاء الصناعي والتاريخ
            agent_usage = [record for record in self.usage_data if record["agent_id"]
                           == agent_id and start_date <= record["timestamp"] <= end_date]

            # إنشاء تقرير
            report = {
                "agent_id": agent_id,
                "start_date": start_date.split('T')[0],
                "end_date": end_date.split('T')[0],
                "total_interactions": len(agent_usage),
                "unique_users": len(set(record["user_id"] for record in agent_usage)),
                "within_scope_percentage": self._calculate_within_scope_percentage(agent_usage),
                "module_distribution": self._calculate_module_distribution(agent_usage),
                "user_activity": self._calculate_user_activity(agent_usage),
                "top_questions": self._extract_top_questions(agent_usage),
                "interactions": agent_usage
            }

            # حفظ التقرير
            report_filename = f"agent_report_{agent_id}_{start_date.split('T')[0]}_{end_date.split('T')[0]}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            logger.info("تم إنشاء تقرير وكيل الذكاء الصناعي: %s", report_path)

            # إنشاء تقرير مرئي
            self._generate_visual_report(report, "agent")

            return report

        except Exception as e:
            logger.error(
                "خطأ أثناء إنشاء تقرير وكيل الذكاء الصناعي: %s",
                str(e))
            return {
                "error": f"خطأ أثناء إنشاء تقرير وكيل الذكاء الصناعي: {str(e)}",
                "agent_id": agent_id}

    def generate_module_report(self, module, start_date=None, end_date=None):
        """
        إنشاء تقرير استخدام الذكاء الصناعي لمديول معين

        المعلمات:
            module (str): المديول
            start_date (str, optional): تاريخ البداية (بتنسيق YYYY-MM-DD)
            end_date (str, optional): تاريخ النهاية (بتنسيق YYYY-MM-DD)

        العائد:
            dict: تقرير استخدام الذكاء الصناعي
        """
        try:
            # تحديد تاريخ البداية والنهاية
            if start_date:
                start_date = datetime.strptime(
                    start_date, "%Y-%m-%d").isoformat()
            else:
                start_date = datetime(1970, 1, 1).isoformat()

            if end_date:
                end_date = (
                    datetime.strptime(
                        end_date,
                        "%Y-%m-%d") +
                    timedelta(
                        days=1) -
                    timedelta(
                        microseconds=1)).isoformat()
            else:
                end_date = datetime.now().isoformat()

            # فلترة بيانات الاستخدام حسب المديول والتاريخ
            module_usage = [record for record in self.usage_data if record.get(
                "module") == module and start_date <= record["timestamp"] <= end_date]

            # إنشاء تقرير
            report = {
                "module": module,
                "start_date": start_date.split('T')[0],
                "end_date": end_date.split('T')[0],
                "total_interactions": len(module_usage),
                "unique_users": len(set(record["user_id"] for record in module_usage)),
                "unique_agents": len(set(record["agent_id"] for record in module_usage)),
                "within_scope_percentage": self._calculate_within_scope_percentage(module_usage),
                "user_activity": self._calculate_user_activity(module_usage),
                "agent_activity": self._calculate_agent_activity(module_usage),
                "top_questions": self._extract_top_questions(module_usage),
                "interactions": module_usage
            }

            # حفظ التقرير
            report_filename = f"module_report_{module}_{start_date.split('T')[0]}_{end_date.split('T')[0]}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            logger.info("تم إنشاء تقرير المديول: %s", report_path)

            # إنشاء تقرير مرئي
            self._generate_visual_report(report, "module")

            return report

        except Exception as e:
            logger.error("خطأ أثناء إنشاء تقرير المديول: %s", str(e))
            return {
                "error": f"خطأ أثناء إنشاء تقرير المديول: {str(e)}",
                "module": module
            }

    def _calculate_within_scope_percentage(self, usage_data):
        """
        حساب نسبة الأسئلة والإجابات ضمن الاختصاصات

        المعلمات:
            usage_data (list): بيانات استخدام الذكاء الصناعي

        العائد:
            float: نسبة الأسئلة والإجابات ضمن الاختصاصات
        """
        try:
            if not usage_data:
                return 100.0

            # حساب عدد السجلات التي تحتوي على معلومات النطاق
            records_with_scope_info = [
                record for record in usage_data if "is_within_scope" in record]

            if not records_with_scope_info:
                return 100.0

            # حساب عدد السجلات ضمن الاختصاصات
            within_scope_count = sum(
                1 for record in records_with_scope_info if record["is_within_scope"])

            # حساب النسبة المئوية
            return (within_scope_count / len(records_with_scope_info)) * 100

        except Exception as e:
            logger.error(
                "خطأ أثناء حساب نسبة الأسئلة والإجابات ضمن الاختصاصات: %s",
                str(e))
            return 100.0

    def _calculate_module_distribution(self, usage_data):
        """
        حساب توزيع استخدام المديولات

        المعلمات:
            usage_data (list): بيانات استخدام الذكاء الصناعي

        العائد:
            dict: توزيع استخدام المديولات
        """
        try:
            if not usage_data:
                return {}

            # حساب عدد الاستخدامات لكل مديول
            module_counts = {}
            for record in usage_data:
                module = record.get("module", "general")
                if module in module_counts:
                    module_counts[module] += 1
                else:
                    module_counts[module] = 1

            # حساب النسب المئوية
            total_count = len(usage_data)
            module_distribution = {
                module: (
                    count /
                    total_count) *
                100 for module,
                count in module_counts.items()}

            return module_distribution

        except Exception as e:
            logger.error("خطأ أثناء حساب توزيع استخدام المديولات: %s", str(e))
            return {}

    def _calculate_user_activity(self, usage_data):
        """
        حساب نشاط المستخدمين

        المعلمات:
            usage_data (list): بيانات استخدام الذكاء الصناعي

        العائد:
            dict: نشاط المستخدمين
        """
        try:
            if not usage_data:
                return {}

            # حساب عدد الاستخدامات لكل مستخدم
            user_counts = {}
            for record in usage_data:
                user_id = record["user_id"]
                if user_id in user_counts:
                    user_counts[user_id] += 1
                else:
                    user_counts[user_id] = 1

            # ترتيب المستخدمين حسب عدد الاستخدامات (من الأعلى إلى الأدنى)
            sorted_users = sorted(
                user_counts.items(),
                key=lambda x: x[1],
                reverse=True)

            # تحويل إلى قاموس
            user_activity = {user_id: count for user_id, count in sorted_users}

            return user_activity

        except Exception as e:
            logger.error("خطأ أثناء حساب نشاط المستخدمين: %s", str(e))
            return {}

    def _calculate_agent_activity(self, usage_data):
        """
        حساب نشاط وكلاء الذكاء الصناعي

        المعلمات:
            usage_data (list): بيانات استخدام الذكاء الصناعي

        العائد:
            dict: نشاط وكلاء الذكاء الصناعي
        """
        try:
            if not usage_data:
                return {}

            # حساب عدد الاستخدامات لكل وكيل
            agent_counts = {}
            for record in usage_data:
                agent_id = record["agent_id"]
                if agent_id in agent_counts:
                    agent_counts[agent_id] += 1
                else:
                    agent_counts[agent_id] = 1

            # ترتيب الوكلاء حسب عدد الاستخدامات (من الأعلى إلى الأدنى)
            sorted_agents = sorted(
                agent_counts.items(),
                key=lambda x: x[1],
                reverse=True)

            # تحويل إلى قاموس
            agent_activity = {
                agent_id: count for agent_id,
                count in sorted_agents}

            return agent_activity

        except Exception as e:
            logger.error(
                "خطأ أثناء حساب نشاط وكلاء الذكاء الصناعي: %s",
                str(e))
            return {}

    def _extract_top_questions(self, usage_data, limit=10):
        """
        استخراج أكثر الأسئلة شيوعًا

        المعلمات:
            usage_data (list): بيانات استخدام الذكاء الصناعي
            limit (int, optional): عدد الأسئلة المطلوبة

        العائد:
            list: أكثر الأسئلة شيوعًا
        """
        try:
            if not usage_data:
                return []

            # استخراج الأسئلة
            questions = [record["question"] for record in usage_data]

            # حساب تكرار كل سؤال
            question_counts = Counter(questions)

            # استخراج أكثر الأسئلة شيوعًا
            top_questions = question_counts.most_common(limit)

            # تحويل إلى قائمة من القواميس
            top_questions_list = [{"question": question, "count": count}
                                  for question, count in top_questions]

            return top_questions_list

        except Exception as e:
            logger.error("خطأ أثناء استخراج أكثر الأسئلة شيوعًا: %s", str(e))
            return []

    def _calculate_daily_activity(self, usage_data, start_date, end_date):
        """
        حساب النشاط اليومي

        المعلمات:
            usage_data (list): بيانات استخدام الذكاء الصناعي
            start_date (str): تاريخ البداية
            end_date (str): تاريخ النهاية

        العائد:
            dict: النشاط اليومي
        """
        try:
            # تحويل التواريخ إلى كائنات datetime
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)

            # إنشاء قاموس لتخزين النشاط اليومي
            daily_activity = {}

            # إنشاء قائمة بجميع الأيام في الفترة
            current_dt = start_dt
            while current_dt <= end_dt:
                daily_activity[current_dt.strftime("%Y-%m-%d")] = 0
                current_dt += timedelta(days=1)

            # حساب عدد الاستخدامات لكل يوم
            for record in usage_data:
                record_dt = datetime.fromisoformat(record["timestamp"])
                record_date = record_dt.strftime("%Y-%m-%d")
                if record_date in daily_activity:
                    daily_activity[record_date] += 1

            return daily_activity

        except Exception as e:
            logger.error("خطأ أثناء حساب النشاط اليومي: %s", str(e))
            return {}

    def _calculate_weekly_activity(self, usage_data, start_date, end_date):
        """
        حساب النشاط الأسبوعي

        المعلمات:
            usage_data (list): بيانات استخدام الذكاء الصناعي
            start_date (str): تاريخ البداية
            end_date (str): تاريخ النهاية

        العائد:
            dict: النشاط الأسبوعي
        """
        try:
            # تحويل التواريخ إلى كائنات datetime
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)

            # إنشاء قاموس لتخزين النشاط الأسبوعي
            weekly_activity = {}

            # إنشاء قائمة بجميع الأسابيع في الفترة
            current_dt = start_dt
            while current_dt <= end_dt:
                # تحديد بداية الأسبوع (الاثنين)
                week_start = current_dt - timedelta(days=current_dt.weekday())
                week_end = week_start + timedelta(days=6)

                # تنسيق الأسبوع
                week_key = f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}"

                weekly_activity[week_key] = 0

                # الانتقال إلى الأسبوع التالي
                current_dt = week_start + timedelta(days=7)

            # حساب عدد الاستخدامات لكل أسبوع
            for record in usage_data:
                record_dt = datetime.fromisoformat(record["timestamp"])

                # تحديد بداية الأسبوع
                week_start = record_dt - timedelta(days=record_dt.weekday())
                week_end = week_start + timedelta(days=6)

                # تنسيق الأسبوع
                week_key = f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}"

                if week_key in weekly_activity:
                    weekly_activity[week_key] += 1

            return weekly_activity

        except Exception as e:
            logger.error("خطأ أثناء حساب النشاط الأسبوعي: %s", str(e))
            return {}

    def _generate_visual_report(self, report, report_type):
        """
        إنشاء تقرير مرئي

        المعلمات:
            report (dict): بيانات التقرير
            report_type (str): نوع التقرير
        """
        try:
            # إنشاء مجلد للتقارير المرئية
            visual_reports_dir = os.path.join(self.reports_dir, 'visual')
            os.makedirs(visual_reports_dir, exist_ok=True)

            # تحديد اسم ملف التقرير المرئي
            if report_type == "daily":
                report_filename = f"daily_visual_report_{report['date']}"
            elif report_type == "weekly":
                report_filename = f"weekly_visual_report_{report['start_date']}_{report['end_date']}"
            elif report_type == "monthly":
                report_filename = f"monthly_visual_report_{report['year']}_{report['month']:02d}"
            elif report_type == "user":
                report_filename = f"user_visual_report_{report['user_id']}_{report['start_date']}_{report['end_date']}"
            elif report_type == "agent":
                report_filename = f"agent_visual_report_{report['agent_id']}_{report['start_date']}_{report['end_date']}"
            elif report_type == "module":
                report_filename = f"module_visual_report_{report['module']}_{report['start_date']}_{report['end_date']}"
            else:
                report_filename = f"visual_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # إنشاء رسم بياني لتوزيع المديولات
            if "module_distribution" in report and report["module_distribution"]:
                plt.figure(figsize=(10, 6))
                modules = list(report["module_distribution"].keys())
                values = list(report["module_distribution"].values())

                plt.bar(modules, values)
                plt.xlabel('المديولات')
                plt.ylabel('النسبة المئوية')
                plt.title('توزيع استخدام المديولات')
                plt.xticks(rotation=45)
                plt.tight_layout()

                # حفظ الرسم البياني
                module_chart_path = os.path.join(
                    visual_reports_dir, f"{report_filename}_module_distribution.png")
                plt.savefig(module_chart_path)
                plt.close()

                logger.info(
                    "تم إنشاء الرسم البياني لتوزيع المديولات: %s",
                    module_chart_path)

            # إنشاء رسم بياني لنشاط المستخدمين
            if "user_activity" in report and report["user_activity"]:
                plt.figure(figsize=(10, 6))
                users = list(report["user_activity"].keys())[
                    :10]  # أخذ أول 10 مستخدمين
                values = list(report["user_activity"].values())[:10]

                plt.bar(users, values)
                plt.xlabel('المستخدمين')
                plt.ylabel(INTERACTIONS_COUNT_LABEL)
                plt.title('نشاط المستخدمين')
                plt.xticks(rotation=45)
                plt.tight_layout()

                # حفظ الرسم البياني
                user_chart_path = os.path.join(
                    visual_reports_dir, f"{report_filename}_user_activity.png")
                plt.savefig(user_chart_path)
                plt.close()

                logger.info(
                    "تم إنشاء الرسم البياني لنشاط المستخدمين: %s",
                    user_chart_path)

            # إنشاء رسم بياني لنشاط وكلاء الذكاء الصناعي
            if "agent_activity" in report and report["agent_activity"]:
                plt.figure(figsize=(10, 6))
                agents = list(report["agent_activity"].keys())
                values = list(report["agent_activity"].values())

                plt.bar(agents, values)
                plt.xlabel('وكلاء الذكاء الصناعي')
                plt.ylabel(INTERACTIONS_COUNT_LABEL)
                plt.title('نشاط وكلاء الذكاء الصناعي')
                plt.xticks(rotation=45)
                plt.tight_layout()

                # حفظ الرسم البياني
                agent_chart_path = os.path.join(
                    visual_reports_dir, f"{report_filename}_agent_activity.png")
                plt.savefig(agent_chart_path)
                plt.close()

                logger.info(
                    "تم إنشاء الرسم البياني لنشاط وكلاء الذكاء الصناعي: %s",
                    agent_chart_path)

            # إنشاء رسم بياني للنشاط اليومي
            if "daily_activity" in report and report["daily_activity"]:
                plt.figure(figsize=(12, 6))
                dates = list(report["daily_activity"].keys())
                values = list(report["daily_activity"].values())

                plt.plot(dates, values, marker='o')
                plt.xlabel('التاريخ')
                plt.ylabel(INTERACTIONS_COUNT_LABEL)
                plt.title('النشاط اليومي')
                plt.xticks(rotation=45)
                plt.tight_layout()

                # حفظ الرسم البياني
                daily_chart_path = os.path.join(
                    visual_reports_dir, f"{report_filename}_daily_activity.png")
                plt.savefig(daily_chart_path)
                plt.close()

                logger.info(
                    "تم إنشاء الرسم البياني للنشاط اليومي: %s",
                    daily_chart_path)

            # إنشاء رسم بياني للنشاط الأسبوعي
            if "weekly_activity" in report and report["weekly_activity"]:
                plt.figure(figsize=(12, 6))
                weeks = list(report["weekly_activity"].keys())
                values = list(report["weekly_activity"].values())

                plt.plot(weeks, values, marker='o')
                plt.xlabel('الأسبوع')
                plt.ylabel(INTERACTIONS_COUNT_LABEL)
                plt.title('النشاط الأسبوعي')
                plt.xticks(rotation=45)
                plt.tight_layout()

                # حفظ الرسم البياني
                weekly_chart_path = os.path.join(
                    visual_reports_dir, f"{report_filename}_weekly_activity.png")
                plt.savefig(weekly_chart_path)
                plt.close()

                logger.info(
                    "تم إنشاء الرسم البياني للنشاط الأسبوعي: %s",
                    weekly_chart_path)

            # إنشاء رسم بياني لنسبة الأسئلة والإجابات ضمن الاختصاصات
            if "within_scope_percentage" in report:
                plt.figure(figsize=(8, 8))
                labels = ['ضمن الاختصاصات', 'خارج الاختصاصات']
                sizes = [
                    report["within_scope_percentage"],
                    100 - report["within_scope_percentage"]]
                colors = ['#66b3ff', '#ff9999']
                explode = (0.1, 0)  # إبراز الشريحة الأولى

                plt.pie(
                    sizes,
                    explode=explode,
                    labels=labels,
                    colors=colors,
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=90)
                plt.axis('equal')  # جعل الرسم البياني دائريًا
                plt.title('نسبة الأسئلة والإجابات ضمن الاختصاصات')

                # حفظ الرسم البياني
                scope_chart_path = os.path.join(
                    visual_reports_dir, f"{report_filename}_within_scope.png")
                plt.savefig(scope_chart_path)
                plt.close()

                logger.info(
                    "تم إنشاء الرسم البياني لنسبة الأسئلة والإجابات ضمن الاختصاصات: %s",
                    scope_chart_path)

        except Exception as e:
            logger.error("خطأ أثناء إنشاء التقرير المرئي: %s", str(e))

    def export_data(
            self,
            format="json",
            start_date=None,
            end_date=None,
            module=None):
        """
        تصدير بيانات استخدام الذكاء الصناعي

        المعلمات:
            format (str, optional): تنسيق التصدير (json, csv)
            start_date (str, optional): تاريخ البداية (بتنسيق YYYY-MM-DD)
            end_date (str, optional): تاريخ النهاية (بتنسيق YYYY-MM-DD)
            module (str, optional): المديول

        العائد:
            str: مسار ملف التصدير
        """
        try:
            # تحديد تاريخ البداية والنهاية
            if start_date:
                start_date = datetime.strptime(
                    start_date, "%Y-%m-%d").isoformat()
            else:
                start_date = datetime(1970, 1, 1).isoformat()

            if end_date:
                end_date = (
                    datetime.strptime(
                        end_date,
                        "%Y-%m-%d") +
                    timedelta(
                        days=1) -
                    timedelta(
                        microseconds=1)).isoformat()
            else:
                end_date = datetime.now().isoformat()

            # فلترة بيانات الاستخدام حسب التاريخ والمديول
            filtered_data = [
                record for record in self.usage_data if start_date <= record["timestamp"] <= end_date]

            if module:
                filtered_data = [
                    record for record in filtered_data if record.get("module") == module]

            # تحديد اسم ملف التصدير
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if module:
                export_filename = f"ai_usage_data_{module}_{timestamp}"
            else:
                export_filename = f"ai_usage_data_{timestamp}"

            # تصدير البيانات حسب التنسيق المطلوب
            if format.lower() == "csv":
                # تحويل البيانات إلى DataFrame
                df = pd.DataFrame(filtered_data)

                # حفظ البيانات في ملف CSV
                export_path = os.path.join(
                    self.reports_dir, f"{export_filename}.csv")
                df.to_csv(export_path, index=False, encoding='utf-8')

            else:  # json
                # حفظ البيانات في ملف JSON
                export_path = os.path.join(
                    self.reports_dir, f"{export_filename}.json")
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

            logger.info(
                "تم تصدير بيانات استخدام الذكاء الصناعي: %s",
                export_path)

            return export_path

        except Exception as e:
            logger.error(
                "خطأ أثناء تصدير بيانات استخدام الذكاء الصناعي: %s",
                str(e))
            return None
