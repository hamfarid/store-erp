"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/activity_log/activity_log_validator.py
الوصف: أداة للتحقق من تسجيل جميع الأحداث في سجل النشاط
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import datetime
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.modules.activity_log.models import ActivityLog
from src.modules.notifications.telegram import TelegramNotificationService

# إعداد المسجل
logger = logging.getLogger(__name__)


class ActivityLogValidator:
    """
    أداة للتحقق من تسجيل جميع الأحداث في سجل النشاط وتحليلها

    توفر هذه الأداة وظائف للتحقق من اكتمال سجل النشاط، وتحليل الأحداث،
    والبحث عن أنماط مشبوهة، وإنشاء تقارير تحليلية.
    """

    def __init__(self, db: Session):
        """
        تهيئة أداة التحقق من سجل النشاط

        المعلمات:
            db: جلسة قاعدة البيانات
        """
        self.db = db
        self.telegram_service = TelegramNotificationService()

    def validate_event_logging(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        time_window: int = 60,  # بالثواني
        expected_details: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[ActivityLog]]:
        """
        التحقق من تسجيل حدث معين في سجل النشاط

        المعلمات:
            event_type: نوع الحدث
            user_id: معرف المستخدم (اختياري)
            time_window: النافذة الزمنية للبحث (بالثواني)
            expected_details: التفاصيل المتوقعة للحدث (اختياري)

        العائد:
            Tuple[bool, Optional[ActivityLog]]: نجاح التحقق وسجل النشاط إن وجد
        """
        # حساب الوقت الأدنى للبحث
        min_time = datetime.datetime.now() - datetime.timedelta(seconds=time_window)

        # بناء استعلام البحث
        query = self.db.query(ActivityLog).filter(
            ActivityLog.event_type == event_type,
            ActivityLog.timestamp >= min_time
        )

        # إضافة فلتر المستخدم إذا تم تحديده
        if user_id:
            query = query.filter(ActivityLog.user_id == user_id)

        # ترتيب النتائج حسب الوقت (الأحدث أولاً)
        query = query.order_by(desc(ActivityLog.timestamp))

        # الحصول على النتائج
        logs = query.all()

        # إذا لم يتم العثور على سجلات، فشل التحقق
        if not logs:
            logger.warning(
                f"لم يتم العثور على سجل للحدث {event_type} في النافذة الزمنية المحددة")
            return False, None

        # إذا لم يتم تحديد تفاصيل متوقعة، نجاح التحقق
        if not expected_details:
            return True, logs[0]

        # البحث عن سجل يطابق التفاصيل المتوقعة
        for log in logs:
            log_details = json.loads(
                log.details) if isinstance(
                log.details,
                str) else log.details

            # التحقق من تطابق جميع التفاصيل المتوقعة
            match = True
            for key, value in expected_details.items():
                if key not in log_details or log_details[key] != value:
                    match = False
                    break

            # إذا تم العثور على تطابق، نجاح التحقق
            if match:
                return True, log

        # إذا لم يتم العثور على تطابق، فشل التحقق
        logger.warning(
            f"لم يتم العثور على سجل للحدث {event_type} بالتفاصيل المتوقعة")
        return False, logs[0]

    def validate_user_action_logging(
        self,
        user_id: str,
        action_type: str,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        time_window: int = 60  # بالثواني
    ) -> Tuple[bool, Optional[ActivityLog]]:
        """
        التحقق من تسجيل إجراء مستخدم في سجل النشاط

        المعلمات:
            user_id: معرف المستخدم
            action_type: نوع الإجراء
            target_type: نوع الهدف (اختياري)
            target_id: معرف الهدف (اختياري)
            time_window: النافذة الزمنية للبحث (بالثواني)

        العائد:
            Tuple[bool, Optional[ActivityLog]]: نجاح التحقق وسجل النشاط إن وجد
        """
        # حساب الوقت الأدنى للبحث
        min_time = datetime.datetime.now() - datetime.timedelta(seconds=time_window)

        # بناء استعلام البحث
        query = self.db.query(ActivityLog).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.event_type == action_type,
            ActivityLog.timestamp >= min_time
        )

        # إضافة فلتر نوع الهدف إذا تم تحديده
        if target_type:
            query = query.filter(ActivityLog.target_type == target_type)

        # إضافة فلتر معرف الهدف إذا تم تحديده
        if target_id:
            query = query.filter(ActivityLog.target_id == target_id)

        # ترتيب النتائج حسب الوقت (الأحدث أولاً)
        query = query.order_by(desc(ActivityLog.timestamp))

        # الحصول على النتائج
        log = query.first()

        # إذا لم يتم العثور على سجل، فشل التحقق
        if not log:
            logger.warning(
                f"لم يتم العثور على سجل للإجراء {action_type} للمستخدم {user_id}")
            return False, None

        # نجاح التحقق
        return True, log

    def validate_security_event_logging(
        self,
        event_type: str,
        ip_address: Optional[str] = None,
        time_window: int = 60  # بالثواني
    ) -> Tuple[bool, Optional[ActivityLog]]:
        """
        التحقق من تسجيل حدث أمني في سجل النشاط

        المعلمات:
            event_type: نوع الحدث الأمني
            ip_address: عنوان IP (اختياري)
            time_window: النافذة الزمنية للبحث (بالثواني)

        العائد:
            Tuple[bool, Optional[ActivityLog]]: نجاح التحقق وسجل النشاط إن وجد
        """
        # حساب الوقت الأدنى للبحث
        min_time = datetime.datetime.now() - datetime.timedelta(seconds=time_window)

        # بناء استعلام البحث
        query = self.db.query(ActivityLog).filter(
            ActivityLog.event_type == event_type,
            ActivityLog.timestamp >= min_time
        )

        # ترتيب النتائج حسب الوقت (الأحدث أولاً)
        query = query.order_by(desc(ActivityLog.timestamp))

        # الحصول على النتائج
        logs = query.all()

        # إذا لم يتم العثور على سجلات، فشل التحقق
        if not logs:
            logger.warning(f"لم يتم العثور على سجل للحدث الأمني {event_type}")
            return False, None

        # إذا لم يتم تحديد عنوان IP، نجاح التحقق
        if not ip_address:
            return True, logs[0]

        # البحث عن سجل يطابق عنوان IP
        for log in logs:
            log_details = json.loads(
                log.details) if isinstance(
                log.details,
                str) else log.details

            # التحقق من تطابق عنوان IP
            if "ip_address" in log_details and log_details["ip_address"] == ip_address:
                return True, log

        # إذا لم يتم العثور على تطابق، فشل التحقق
        logger.warning(
            f"لم يتم العثور على سجل للحدث الأمني {event_type} لعنوان IP {ip_address}")
        return False, logs[0]

    def validate_ai_action_logging(
        self,
        agent_id: str,
        action_type: str,
        time_window: int = 60  # بالثواني
    ) -> Tuple[bool, Optional[ActivityLog]]:
        """
        التحقق من تسجيل إجراء وكيل الذكاء الاصطناعي في سجل النشاط

        المعلمات:
            agent_id: معرف وكيل الذكاء الاصطناعي
            action_type: نوع الإجراء
            time_window: النافذة الزمنية للبحث (بالثواني)

        العائد:
            Tuple[bool, Optional[ActivityLog]]: نجاح التحقق وسجل النشاط إن وجد
        """
        # حساب الوقت الأدنى للبحث
        min_time = datetime.datetime.now() - datetime.timedelta(seconds=time_window)

        # بناء استعلام البحث
        query = self.db.query(ActivityLog).filter(
            ActivityLog.agent_id == agent_id,
            ActivityLog.event_type == action_type,
            ActivityLog.timestamp >= min_time
        )

        # ترتيب النتائج حسب الوقت (الأحدث أولاً)
        query = query.order_by(desc(ActivityLog.timestamp))

        # الحصول على النتائج
        log = query.first()

        # إذا لم يتم العثور على سجل، فشل التحقق
        if not log:
            logger.warning(
                f"لم يتم العثور على سجل للإجراء {action_type} لوكيل الذكاء الاصطناعي {agent_id}")
            return False, None

        # نجاح التحقق
        return True, log

    def analyze_user_activity(
        self,
        user_id: str,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        event_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        تحليل نشاط المستخدم في سجل النشاط

        المعلمات:
            user_id: معرف المستخدم
            start_time: وقت البدء (اختياري)
            end_time: وقت الانتهاء (اختياري)
            event_types: أنواع الأحداث للتحليل (اختياري)

        العائد:
            Dict[str, Any]: نتائج التحليل
        """
        # بناء استعلام البحث
        query = self.db.query(ActivityLog).filter(
            ActivityLog.user_id == user_id)

        # إضافة فلتر الوقت إذا تم تحديده
        if start_time:
            query = query.filter(ActivityLog.timestamp >= start_time)
        if end_time:
            query = query.filter(ActivityLog.timestamp <= end_time)

        # إضافة فلتر أنواع الأحداث إذا تم تحديدها
        if event_types:
            query = query.filter(ActivityLog.event_type.in_(event_types))

        # ترتيب النتائج حسب الوقت (الأحدث أولاً)
        query = query.order_by(desc(ActivityLog.timestamp))

        # الحصول على النتائج
        logs = query.all()

        # تحليل النتائج
        analysis = {
            "total_events": len(logs),
            "event_types": {},
            "time_distribution": {},
            "details": []
        }

        # تحليل توزيع أنواع الأحداث
        for log in logs:
            # تحديث عدد الأحداث لكل نوع
            event_type = log.event_type
            analysis["event_types"][event_type] = analysis["event_types"].get(
                event_type, 0) + 1

            # تحديث التوزيع الزمني
            hour = log.timestamp.hour
            analysis["time_distribution"][hour] = analysis["time_distribution"].get(
                hour, 0) + 1

            # إضافة تفاصيل الحدث
            analysis["details"].append({
                "timestamp": log.timestamp.isoformat(),
                "event_type": event_type,
                "details": log.details
            })

        return analysis

    def analyze_security_events(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        تحليل الأحداث الأمنية في سجل النشاط

        المعلمات:
            start_time: وقت البدء (اختياري)
            end_time: وقت الانتهاء (اختياري)
            ip_address: عنوان IP للتحليل (اختياري)

        العائد:
            Dict[str, Any]: نتائج التحليل
        """
        # بناء استعلام البحث
        query = self.db.query(ActivityLog).filter(
            ActivityLog.event_type.like("security.%")
        )

        # إضافة فلتر الوقت إذا تم تحديده
        if start_time:
            query = query.filter(ActivityLog.timestamp >= start_time)
        if end_time:
            query = query.filter(ActivityLog.timestamp <= end_time)

        # إضافة فلتر عنوان IP إذا تم تحديده
        if ip_address:
            query = query.filter(ActivityLog.details.like(f"%{ip_address}%"))

        # ترتيب النتائج حسب الوقت (الأحدث أولاً)
        query = query.order_by(desc(ActivityLog.timestamp))

        # الحصول على النتائج
        logs = query.all()

        # تحليل النتائج
        analysis = {
            "total_events": len(logs),
            "event_types": {},
            "ip_addresses": {},
            "time_distribution": {},
            "details": []
        }

        # تحليل الأحداث
        for log in logs:
            # تحديث عدد الأحداث لكل نوع
            event_type = log.event_type
            analysis["event_types"][event_type] = analysis["event_types"].get(
                event_type, 0) + 1

            # تحديث التوزيع الزمني
            hour = log.timestamp.hour
            analysis["time_distribution"][hour] = analysis["time_distribution"].get(
                hour, 0) + 1

            # تحليل تفاصيل الحدث
            log_details = json.loads(
                log.details) if isinstance(
                log.details,
                str) else log.details

            # تحديث إحصائيات عناوين IP
            if "ip_address" in log_details:
                ip = log_details["ip_address"]
                analysis["ip_addresses"][ip] = analysis["ip_addresses"].get(
                    ip, 0) + 1

            # إضافة تفاصيل الحدث
            analysis["details"].append({
                "timestamp": log.timestamp.isoformat(),
                "event_type": event_type,
                "details": log_details
            })

        return analysis

    def detect_suspicious_patterns(
        self,
        time_window: int = 3600  # بالثواني
    ) -> List[Dict[str, Any]]:
        """
        اكتشاف الأنماط المشبوهة في سجل النشاط

        المعلمات:
            time_window: النافذة الزمنية للتحليل (بالثواني)

        العائد:
            List[Dict[str, Any]]: قائمة الأنماط المشبوهة المكتشفة
        """
        # حساب وقت البدء
        start_time = datetime.datetime.now() - datetime.timedelta(seconds=time_window)

        # الحصول على جميع السجلات في النافذة الزمنية
        logs = self.db.query(ActivityLog).filter(
            ActivityLog.timestamp >= start_time
        ).order_by(ActivityLog.timestamp).all()

        # تحليل الأنماط
        patterns = []

        # 1. تحليل محاولات تسجيل الدخول المتكررة
        login_attempts = {}
        for log in logs:
            if log.event_type == "security.login_attempt":
                log_details = json.loads(
                    log.details) if isinstance(
                    log.details,
                    str) else log.details
                ip = log_details.get("ip_address", "unknown")
                if ip not in login_attempts:
                    login_attempts[ip] = []
                login_attempts[ip].append(log.timestamp)

        # تحليل محاولات تسجيل الدخول
        for ip, timestamps in login_attempts.items():
            if len(timestamps) >= 5:  # أكثر من 5 محاولات
                patterns.append({
                    "type": "multiple_login_attempts",
                    "ip_address": ip,
                    "count": len(timestamps),
                    "first_attempt": timestamps[0].isoformat(),
                    "last_attempt": timestamps[-1].isoformat()
                })

        # 2. تحليل الأنشطة غير العادية
        user_activities = {}
        for log in logs:
            if log.user_id:
                if log.user_id not in user_activities:
                    user_activities[log.user_id] = []
                user_activities[log.user_id].append({
                    "timestamp": log.timestamp,
                    "event_type": log.event_type
                })

        # تحليل أنشطة المستخدمين
        for user_id, activities in user_activities.items():
            if len(activities) > 50:  # أكثر من 50 نشاط في الساعة
                patterns.append({
                    "type": "high_activity",
                    "user_id": user_id,
                    "count": len(activities),
                    "first_activity": activities[0]["timestamp"].isoformat(),
                    "last_activity": activities[-1]["timestamp"].isoformat()
                })

        return patterns

    def generate_activity_report(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        user_id: Optional[str] = None,
        event_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        إنشاء تقرير تحليلي لنشاط النظام

        المعلمات:
            start_time: وقت البدء (اختياري)
            end_time: وقت الانتهاء (اختياري)
            user_id: معرف المستخدم (اختياري)
            event_types: أنواع الأحداث (اختياري)

        العائد:
            Dict[str, Any]: التقرير التحليلي
        """
        # بناء استعلام البحث
        query = self.db.query(ActivityLog)

        # إضافة الفلاتر
        if start_time:
            query = query.filter(ActivityLog.timestamp >= start_time)
        if end_time:
            query = query.filter(ActivityLog.timestamp <= end_time)
        if user_id:
            query = query.filter(ActivityLog.user_id == user_id)
        if event_types:
            query = query.filter(ActivityLog.event_type.in_(event_types))

        # ترتيب النتائج حسب الوقت
        query = query.order_by(ActivityLog.timestamp)

        # الحصول على النتائج
        logs = query.all()

        # إنشاء التقرير
        report = {
            "summary": {
                "total_events": len(logs),
                "time_range": {
                    "start": logs[0].timestamp.isoformat() if logs else None,
                    "end": logs[-1].timestamp.isoformat() if logs else None
                }
            },
            "event_types": {},
            "user_activity": {},
            "time_distribution": {},
            "details": []
        }

        # تحليل النتائج
        for log in logs:
            # تحديث إحصائيات أنواع الأحداث
            event_type = log.event_type
            report["event_types"][event_type] = report["event_types"].get(
                event_type, 0) + 1

            # تحديث إحصائيات نشاط المستخدم
            if log.user_id:
                if log.user_id not in report["user_activity"]:
                    report["user_activity"][log.user_id] = {
                        "total_events": 0,
                        "event_types": {}
                    }
                report["user_activity"][log.user_id]["total_events"] += 1
                report["user_activity"][log.user_id]["event_types"][event_type] = \
                    report["user_activity"][log.user_id]["event_types"].get(event_type, 0) + 1

            # تحديث التوزيع الزمني
            hour = log.timestamp.hour
            report["time_distribution"][hour] = report["time_distribution"].get(
                hour, 0) + 1

            # إضافة تفاصيل الحدث
            report["details"].append({
                "timestamp": log.timestamp.isoformat(),
                "user_id": log.user_id,
                "event_type": event_type,
                "details": log.details
            })

        return report
