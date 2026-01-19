# File:
# /home/ubuntu/ai_web_organized/src/modules/alert_management/alert_manager.py
"""
from flask import g
وحدة إدارة التنبيهات
توفر هذه الوحدة وظائف إدارة التنبيهات والإشعارات
"""

import json
import logging
import os
import smtplib
import threading
import time
import uuid
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict

import requests

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# مسارات ملفات البيانات
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
ALERTS_FILE = os.path.join(DATA_DIR, 'alerts.json')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

# التأكد من وجود مجلد البيانات
os.makedirs(DATA_DIR, exist_ok=True)

# دالة مساعدة لتحميل البيانات من ملف JSON


def load_data(file_path, default_data=None):
    if default_data is None:
        default_data = {}

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
        return default_data

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default_data

# دالة مساعدة لحفظ البيانات في ملف JSON


def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# دالة لإنشاء تنبيه جديد


def create_alert(
        alert_type,
        severity,
        module,
        message_ar,
        message_en,
        details=None):
    """إنشاء تنبيه جديد"""
    try:
        # الحصول على التنبيهات الحالية
        alerts = load_data(ALERTS_FILE, {"alerts": []})

        # إنشاء معرف فريد للتنبيه
        alert_id = str(uuid.uuid4())

        # إنشاء كائن التنبيه
        alert = {
            "id": alert_id,
            "type": alert_type,
            "severity": severity,
            "module": module,
            "messageAr": message_ar,
            "messageEn": message_en,
            "details": details or {},
            "timestamp": datetime.now().isoformat(),
            "status": "active",
            "acknowledged": False,
            "acknowledgedBy": None,
            "acknowledgedAt": None,
            "resolved": False,
            "resolvedBy": None,
            "resolvedAt": None
        }

        # إضافة التنبيه إلى القائمة
        alerts["alerts"].append(alert)

        # حفظ التنبيهات
        save_data(ALERTS_FILE, alerts)

        # إرسال الإشعارات
        send_alert_notifications(alert)

        return alert
    except Exception as e:
        logger.error(f"Error creating alert: {str(e)}")
        return None

# دالة للحصول على التنبيهات


def get_alerts(
        status=None,
        severity=None,
        module=None,
        start_date=None,
        end_date=None,
        limit=None):
    """الحصول على التنبيهات"""
    try:
        # الحصول على التنبيهات
        alerts = load_data(ALERTS_FILE, {"alerts": []})

        # تصفية التنبيهات حسب الحالة
        if status:
            alerts["alerts"] = [
                alert for alert in alerts["alerts"] if alert["status"] == status]

        # تصفية التنبيهات حسب الخطورة
        if severity:
            alerts["alerts"] = [alert for alert in alerts["alerts"]
                                if alert["severity"] == severity]

        # تصفية التنبيهات حسب المديول
        if module:
            alerts["alerts"] = [
                alert for alert in alerts["alerts"] if alert["module"] == module]

        # تصفية التنبيهات حسب التاريخ
        if start_date:
            alerts["alerts"] = [alert for alert in alerts["alerts"]
                                if alert["timestamp"] >= start_date]

        if end_date:
            alerts["alerts"] = [alert for alert in alerts["alerts"]
                                if alert["timestamp"] <= end_date]

        # ترتيب التنبيهات حسب التاريخ (الأحدث أولاً)
        alerts["alerts"] = sorted(
            alerts["alerts"],
            key=lambda x: x["timestamp"],
            reverse=True)

        # تحديد عدد التنبيهات المطلوبة
        if limit:
            try:
                limit = int(limit)
                alerts["alerts"] = alerts["alerts"][:limit]
            except ValueError:
                pass

        return alerts["alerts"]
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        return []

# دالة للحصول على تنبيه محدد


def get_alert(alert_id):
    """الحصول على تنبيه محدد"""
    try:
        # الحصول على التنبيهات
        alerts = load_data(ALERTS_FILE, {"alerts": []})

        # البحث عن التنبيه
        for alert in alerts["alerts"]:
            if alert["id"] == alert_id:
                return alert

        return None
    except Exception as e:
        logger.error(f"Error getting alert: {str(e)}")
        return None

# دالة لتحديث حالة التنبيه


def update_alert_status(alert_id, status, user=None):
    """تحديث حالة التنبيه"""
    try:
        # الحصول على التنبيهات
        alerts = load_data(ALERTS_FILE, {"alerts": []})

        # البحث عن التنبيه
        for alert in alerts["alerts"]:
            if alert["id"] == alert_id:
                # تحديث الحالة
                alert["status"] = status

                # تحديث معلومات الإقرار أو الحل
                if status == "acknowledged":
                    alert["acknowledged"] = True
                    alert["acknowledgedBy"] = user or "admin"
                    alert["acknowledgedAt"] = datetime.now().isoformat()
                elif status == "resolved":
                    alert["resolved"] = True
                    alert["resolvedBy"] = user or "admin"
                    alert["resolvedAt"] = datetime.now().isoformat()

                # حفظ التنبيهات
                save_data(ALERTS_FILE, alerts)

                return alert

        return None
    except Exception as e:
        logger.error(f"Error updating alert status: {str(e)}")
        return None

# دالة لحذف تنبيه


def delete_alert(alert_id):
    """حذف تنبيه"""
    try:
        # الحصول على التنبيهات
        alerts = load_data(ALERTS_FILE, {"alerts": []})

        # البحث عن التنبيه
        for i, alert in enumerate(alerts["alerts"]):
            if alert["id"] == alert_id:
                # حذف التنبيه
                del alerts["alerts"][i]

                # حفظ التنبيهات
                save_data(ALERTS_FILE, alerts)

                return True

        return False
    except Exception as e:
        logger.error(f"Error deleting alert: {str(e)}")
        return False

# دالة للحصول على إعدادات التنبيهات


def get_alerts_config():
    """الحصول على إعدادات التنبيهات"""
    try:
        # الحصول على إعدادات التنبيهات
        config = load_data(CONFIG_FILE, {
            "enabled": True,
            "email_notifications": False,
            "sms_notifications": False,
            "default_severity": "medium",
            "auto_acknowledge": False,
            "alert_levels": {
                "low": {"email": False, "sms": False, "push": False, "webhook": False},
                "medium": {"email": True, "sms": False, "push": True, "webhook": False},
                "high": {"email": True, "sms": True, "push": True, "webhook": True},
                "critical": {"email": True, "sms": True, "push": True, "webhook": True}
            },
            "notifications": {
                "email": False,
                "sms": False,
                "push": False,
                "webhook": False
            },
            "thresholds": {
                "cpu": 80,
                "memory": 80,
                "disk": 80,
                "network": 80
            },
            "recipients": {
                "email": [],
                "sms": [],
                "push": []
            }
        })

        return config
    except Exception as e:
        logger.error(f"Error getting alerts config: {str(e)}")
        return {}

# دالة لتحديث إعدادات التنبيهات


def update_alerts_config(config):
    """تحديث إعدادات التنبيهات"""
    try:
        # حفظ إعدادات التنبيهات
        save_data(CONFIG_FILE, config)

        return config
    except Exception as e:
        logger.error(f"Error updating alerts config: {str(e)}")
        return {}

# دالة لإرسال إشعارات التنبيه


def send_alert_notifications(alert):
    """إرسال إشعارات التنبيه"""
    try:
        # الحصول على إعدادات التنبيهات
        config = get_alerts_config()

        # التأكد من أن config هو قاموس
        if not isinstance(config, dict):
            logger.warning(
                "Config is not a dictionary, skipping notifications")
            return False

        # التحقق من مستوى التنبيه
        severity = alert["severity"]
        alert_levels: Dict[str, Any] = config.get("alert_levels", {})
        if severity not in alert_levels:
            severity = "medium"  # المستوى الافتراضي

        # التحقق من تمكين الإشعارات لهذا المستوى
        alert_level: Dict[str, Any] = alert_levels.get(severity, {})
        notifications_config: Dict[str, Any] = config.get("notifications", {})

        # إرسال إشعار بالبريد الإلكتروني
        if alert_level.get(
                "email",
                False) and notifications_config.get(
                "email",
                False):
            send_email_notification(alert, config)

        # إرسال إشعار بالرسائل القصيرة
        if alert_level.get(
                "sms",
                False) and notifications_config.get(
                "sms",
                False):
            send_sms_notification(alert, config)

        # إرسال إشعار بالدفع
        if alert_level.get(
                "push",
                False) and notifications_config.get(
                "push",
                False):
            send_push_notification(alert, config)

        # إرسال إشعار بالويب هوك
        if alert_level.get(
                "webhook",
                False) and notifications_config.get(
                "webhook",
                False):
            send_webhook_notification(alert, config)

        return True
    except Exception as e:
        logger.error(f"Error sending alert notifications: {str(e)}")
        return False

# دالة لإرسال إشعار بالبريد الإلكتروني


def send_email_notification(alert, config):
    """إرسال إشعار بالبريد الإلكتروني"""
    try:
        # التحقق من وجود مستلمين
        recipients = config["recipients"].get("email", [])
        if not recipients:
            return False

        # الحصول على إعدادات البريد الإلكتروني
        email_settings = config.get("email_settings", {})
        smtp_server = email_settings.get("smtp_server")
        smtp_port = email_settings.get("smtp_port", 587)
        smtp_username = email_settings.get("smtp_username")
        smtp_password = email_settings.get("smtp_password")
        from_email = email_settings.get("from_email")
        use_tls = email_settings.get("use_tls", True)

        if not smtp_server or not smtp_username or not smtp_password or not from_email:
            logger.warning("Email settings are incomplete")
            return False

        # إنشاء رسالة البريد الإلكتروني
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = f"[{alert['severity'].upper()}] {alert['messageEn']}"

        # إنشاء نص الرسالة
        body = f"""
        Alert Details:
        --------------
        Type: {alert['type']}
        Severity: {alert['severity']}
        Module: {alert['module']}
        Message (EN): {alert['messageEn']}
        Message (AR): {alert['messageAr']}
        Timestamp: {alert['timestamp']}
        Status: {alert['status']}

        Details:
        {json.dumps(alert['details'], indent=2) if alert['details'] else 'No additional details'}

        Please take appropriate action.
        """

        msg.attach(MIMEText(body, 'plain'))

        # إرسال البريد الإلكتروني
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if use_tls:
                server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
            logger.info(f"Email notification sent for alert {alert['id']}")
            return True
        except Exception as e:
            logger.error(f"Error sending email notification: {str(e)}")
            return False
    except Exception as e:
        logger.error(f"Error preparing email notification: {str(e)}")
        return False

# دالة لإرسال إشعار بالرسائل القصيرة


def send_sms_notification(alert, config):
    """إرسال إشعار بالرسائل القصيرة"""
    # ملاحظة: هذه دالة تجريبية، في التطبيق الحقيقي يجب استخدام خدمة رسائل
    # قصيرة مثل Twilio
    try:
        # التحقق من وجود مستلمين
        recipients = config["recipients"].get("sms", [])
        if not recipients:
            return False

        # إنشاء نص الرسالة
        message = f"[{alert['severity'].upper()}] {alert['messageEn']} - {alert['module']}"

        # تسجيل الإشعار
        logger.info(
            f"SMS notification would be sent to {recipients}: {message}")

        return True
    except Exception as e:
        logger.error(f"Error sending SMS notification: {str(e)}")
        return False

# دالة لإرسال إشعار بالدفع


def send_push_notification(alert, config):
    """إرسال إشعار بالدفع"""
    # ملاحظة: هذه دالة تجريبية، في التطبيق الحقيقي يجب استخدام خدمة إشعارات
    # مثل Firebase Cloud Messaging
    try:
        # التحقق من وجود مستلمين
        recipients = config["recipients"].get("push", [])
        if not recipients:
            return False

        # إنشاء نص الإشعار
        notification = {
            "title": f"[{alert['severity'].upper()}] Alert",
            "body": alert['messageEn'],
            "icon": "warning",
            "data": {
                "alert_id": alert['id'],
                "module": alert['module'],
                "severity": alert['severity'],
                "timestamp": alert['timestamp']
            }
        }

        # تسجيل الإشعار
        logger.info(
            f"Push notification would be sent to {recipients}: {notification}")

        return True
    except Exception as e:
        logger.error(f"Error sending push notification: {str(e)}")
        return False

# دالة لإرسال إشعار بالويب هوك


def send_webhook_notification(alert, config):
    """إرسال إشعار بالويب هوك"""
    try:
        # التحقق من وجود عنوان الويب هوك
        webhook_url = config.get("webhook_url")
        if not webhook_url:
            return False

        # إنشاء بيانات الإشعار
        payload = {
            "alert": alert,
            "timestamp": datetime.now().isoformat()
        }

        # إرسال الإشعار
        try:
            response = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if response.status_code == 200:
                logger.info(
                    f"Webhook notification sent for alert {alert['id']}")
                return True
            else:
                logger.warning(
                    f"Webhook notification failed with status code {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error sending webhook notification: {str(e)}")
            return False
    except Exception as e:
        logger.error(f"Error preparing webhook notification: {str(e)}")
        return False

# فئة لمراقبة الموارد وإنشاء التنبيهات


class AlertMonitor:
    """فئة لمراقبة الموارد وإنشاء التنبيهات"""

    def __init__(self, interval=60):
        """تهيئة مراقب التنبيهات"""
        self.interval = interval  # الفترة الزمنية بين عمليات المراقبة (بالثواني)
        self.running = False
        self.thread = None

    def start(self):
        """بدء المراقبة"""
        if self.running is not None:
            logger.warning("Alert monitor is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._monitor_resources)
        self.thread.daemon = True
        self.thread.start()
        logger.info(
            f"Alert monitor started with interval {self.interval} seconds")

    def stop(self):
        """إيقاف المراقبة"""
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=5)
            logger.info("Alert monitor stopped")

    def _monitor_resources(self):
        """مراقبة الموارد وإنشاء التنبيهات"""
        while self.running:
            try:
                # الحصول على إعدادات التنبيهات
                config = get_alerts_config()
                if not isinstance(config, dict):
                    logger.warning(
                        "Config is not a dictionary, skipping monitoring")
                    continue
                thresholds = config.get("thresholds", {})

                # الحصول على بيانات الموارد
                try:
                    # محاولة استيراد وحدة مراقبة الموارد
                    from ..resource_monitoring.resource_collector import (
                        get_cpu_usage,
                        get_disk_usage,
                        get_memory_usage,
                        get_network_usage,
                    )

                    # الحصول على بيانات الموارد
                    cpu_usage = get_cpu_usage()
                    memory_usage = get_memory_usage()
                    disk_usage = get_disk_usage()
                    network_usage = get_network_usage()

                    # التحقق من تجاوز العتبات

                    # التحقق من استخدام المعالج
                    if isinstance(thresholds, dict):
                        cpu_threshold = thresholds.get("cpu", 80)
                    else:
                        cpu_threshold = 80
                    if cpu_usage["percent"] > cpu_threshold:
                        create_alert(
                            "resource",
                            "high" if cpu_usage["percent"] > 90 else "medium",
                            "resource_monitoring",
                            f"استخدام المعالج مرتفع ({cpu_usage['percent']}%)",
                            f"High CPU usage ({cpu_usage['percent']}%)",
                            {
                                "resource": "cpu",
                                "value": cpu_usage["percent"],
                                "threshold": cpu_threshold
                            }
                        )

                    # التحقق من استخدام الذاكرة
                    memory_threshold = thresholds.get("memory", 80)
                    if memory_usage["virtual"]["percent"] > memory_threshold:
                        create_alert(
                            "resource",
                            "high" if memory_usage["virtual"]["percent"] > 90 else "medium",
                            "resource_monitoring",
                            f"استخدام الذاكرة مرتفع ({memory_usage['virtual']['percent']}%)",
                            f"High memory usage ({memory_usage['virtual']['percent']}%)",
                            {
                                "resource": "memory",
                                "value": memory_usage["virtual"]["percent"],
                                "threshold": memory_threshold})

                    # التحقق من استخدام القرص
                    disk_threshold = thresholds.get("disk", 80)
                    if disk_usage["main"]["percent"] > disk_threshold:
                        create_alert("resource",
                                     "high" if disk_usage["main"]["percent"] > 90 else "medium",
                                     "resource_monitoring",
                                     f"استخدام القرص مرتفع ({disk_usage['main']['percent']}%)",
                                     f"High disk usage ({disk_usage['main']['percent']}%)",
                                     {"resource": "disk",
                                      "value": disk_usage["main"]["percent"],
                                      "threshold": disk_threshold})

                    # التحقق من استخدام الشبكة
                    network_threshold = thresholds.get("network", 80)
                    if network_usage["percent"] > network_threshold:
                        create_alert("resource",
                                     "medium",
                                     "resource_monitoring",
                                     f"استخدام الشبكة مرتفع ({network_usage['percent']}%)",
                                     f"High network usage ({network_usage['percent']}%)",
                                     {"resource": "network",
                                      "value": network_usage["percent"],
                                         "threshold": network_threshold})
                except ImportError:
                    logger.warning("Resource monitoring module not available")
                except Exception as e:
                    logger.error(f"Error monitoring resources: {str(e)}")

                # انتظار الفترة الزمنية المحددة
                for _ in range(int(self.interval)):
                    if not self.running:
                        break
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Error in alert monitor: {str(e)}")
                time.sleep(10)  # انتظار قبل المحاولة مرة أخرى في حالة حدوث خطأ


# إنشاء كائن مراقب التنبيهات
alert_monitor = AlertMonitor(interval=60)

# تهيئة البيانات الافتراضية


def init_default_data():
    """تهيئة البيانات الافتراضية"""
    # تهيئة التنبيهات إذا لم تكن موجودة
    if not os.path.exists(ALERTS_FILE):
        # إنشاء بعض التنبيهات الافتراضية للاختبار
        alerts = {"alerts": []}

        # تنبيه استخدام المعالج
        alerts["alerts"].append({
            "id": str(uuid.uuid4()),
            "type": "resource",
            "severity": "high",
            "module": "resource_monitoring",
            "messageAr": "استخدام المعالج مرتفع (85%)",
            "messageEn": "High CPU usage (85%)",
            "details": {
                "resource": "cpu",
                "value": 85,
                "threshold": 80
            },
            "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
            "status": "active",
            "acknowledged": False,
            "acknowledgedBy": None,
            "acknowledgedAt": None,
            "resolved": False,
            "resolvedBy": None,
            "resolvedAt": None
        })

        # تنبيه استخدام الذاكرة
        alerts["alerts"].append({
            "id": str(uuid.uuid4()),
            "type": "resource",
            "severity": "medium",
            "module": "resource_monitoring",
            "messageAr": "استخدام الذاكرة مرتفع (75%)",
            "messageEn": "High memory usage (75%)",
            "details": {
                "resource": "memory",
                "value": 75,
                "threshold": 80
            },
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "status": "acknowledged",
            "acknowledged": True,
            "acknowledgedBy": "admin",
            "acknowledgedAt": (datetime.now() - timedelta(hours=1, minutes=30)).isoformat(),
            "resolved": False,
            "resolvedBy": None,
            "resolvedAt": None
        })

        # تنبيه خطأ في المديول
        alerts["alerts"].append({
            "id": str(uuid.uuid4()),
            "type": "error",
            "severity": "critical",
            "module": "disease_diagnosis",
            "messageAr": "فشل في تحميل نموذج تشخيص الأمراض",
            "messageEn": "Failed to load disease diagnosis model",
            "details": {
                "error": "FileNotFoundError",
                "message": "Model file not found"
            },
            "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
            "status": "resolved",
            "acknowledged": True,
            "acknowledgedBy": "admin",
            "acknowledgedAt": (datetime.now() - timedelta(hours=2, minutes=45)).isoformat(),
            "resolved": True,
            "resolvedBy": "admin",
            "resolvedAt": (datetime.now() - timedelta(hours=2)).isoformat()
        })

        # حفظ التنبيهات
        save_data(ALERTS_FILE, alerts)

    # تهيئة إعدادات التنبيهات إذا لم تكن موجودة
    get_alerts_config()

    # بدء مراقب التنبيهات
    alert_monitor.start()


# تهيئة البيانات الافتراضية
init_default_data()
