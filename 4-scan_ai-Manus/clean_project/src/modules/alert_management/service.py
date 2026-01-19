#!/usr/bin/env python3
"""
خدمة إدارة التنبيهات
توفر هذه الوحدة خدمات إدارة التنبيهات والإشعارات للنظام
"""

import sys
import time
import logging
import threading
from datetime import datetime
from pathlib import Path

# إضافة مسار المشروع إلى sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from .alert_manager import AlertManager
except ImportError:
    # في حالة عدم وجود الملف، إنشاء مدير تنبيهات بسيط
    class AlertManager:
        def __init__(self):
            self.logger = logging.getLogger(__name__)
            self.alerts = []

        def create_alert(self, alert_type, message, severity="info"):
            alert = {
                "id": len(self.alerts) + 1,
                "type": alert_type,
                "message": message,
                "severity": severity,
                "timestamp": datetime.now(),
                "status": "active"
            }
            self.alerts.append(alert)
            self.logger.info(f"تم إنشاء تنبيه: {message}")
            return alert

        def get_alerts(self, status=None):
            if status:
                return [a for a in self.alerts if a["status"] == status]
            return self.alerts

        def dismiss_alert(self, alert_id):
            for alert in self.alerts:
                if alert["id"] == alert_id:
                    alert["status"] = "dismissed"
                    self.logger.info(f"تم إغلاق التنبيه: {alert_id}")
                    return True
            return False

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AlertManagementService:
    """خدمة إدارة التنبيهات الرئيسية"""

    def __init__(self):
        """تهيئة خدمة إدارة التنبيهات"""
        self.alert_manager = AlertManager()
        self.is_running = False
        self.monitoring_thread = None
        self.check_interval = 30  # فحص كل 30 ثانية

        logger.info("تم تهيئة خدمة إدارة التنبيهات")

    def start_service(self):
        """بدء خدمة إدارة التنبيهات"""
        if self.is_running is not None:
            logger.warning("خدمة إدارة التنبيهات تعمل بالفعل")
            return

        self.is_running = True
        logger.info("تم بدء خدمة إدارة التنبيهات")

        # بدء مراقبة النظام
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def stop_service(self):
        """إيقاف خدمة إدارة التنبيهات"""
        self.is_running = False
        logger.info("تم إيقاف خدمة إدارة التنبيهات")

    def _monitoring_loop(self):
        """حلقة مراقبة النظام للتنبيهات"""
        logger.info("بدء مراقبة النظام للتنبيهات...")

        while self.is_running:
            try:
                # فحص حالة النظام
                self._check_system_health()

                # فحص الموارد
                self._check_resources()

                # فحص الخدمات
                self._check_services()

                # انتظار قبل الفحص التالي
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("تم إيقاف المراقبة بواسطة المستخدم")
                break
            except Exception as e:
                logger.error(f"خطأ في مراقبة التنبيهات: {str(e)}")
                time.sleep(10)  # انتظار قصير قبل المحاولة مرة أخرى

    def _check_system_health(self):
        """فحص صحة النظام"""
        try:
            # فحص مساحة القرص
            disk_usage = self._get_disk_usage()
            if disk_usage > 90:
                self.alert_manager.create_alert(
                    "system",
                    f"مساحة القرص ممتلئة: {disk_usage} %",
                    "critical"
                )
            elif disk_usage > 80:
                self.alert_manager.create_alert(
                    "system",
                    f"مساحة القرص منخفضة: {disk_usage}%",
                    "warning"
                )

            # فحص الذاكرة
            memory_usage = self._get_memory_usage()
            if memory_usage > 90:
                self.alert_manager.create_alert(
                    "system",
                    f"استخدام الذاكرة مرتفع: {memory_usage}%",
                    "warning"
                )

        except Exception as e:
            logger.error(f"خطأ في فحص صحة النظام: {str(e)}")

    def _check_resources(self):
        """فحص الموارد"""
        try:
            # فحص استخدام المعالج
            cpu_usage = self._get_cpu_usage()
            if cpu_usage > 90:
                self.alert_manager.create_alert(
                    "resource",
                    f"استخدام المعالج مرتفع: {cpu_usage} %",
                    "warning"
                )

        except Exception as e:
            logger.error(f"خطأ في فحص الموارد: {str(e)}")

    def _check_services(self):
        """فحص حالة الخدمات"""
        try:
            # فحص الخدمات المهمة
            services_to_check = [
                "database",
                "redis",
                "rabbitmq",
                "elasticsearch"
            ]

            for service in services_to_check:
                if not self._is_service_healthy(service):
                    self.alert_manager.create_alert(
                        "service",
                        f"الخدمة {service} غير متاحة",
                        "critical"
                    )

        except Exception as e:
            logger.error(f"خطأ في فحص الخدمات: {str(e)}")

    def _get_disk_usage(self):
        """الحصول على نسبة استخدام القرص"""
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            return (used / total) * 100
        except Exception:
            return 0

    def _get_memory_usage(self):
        """الحصول على نسبة استخدام الذاكرة"""
        try:
            import psutil
            return psutil.virtual_memory().percent
        except ImportError:
            return 0
        except Exception:
            return 0

    def _get_cpu_usage(self):
        """الحصول على نسبة استخدام المعالج"""
        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except ImportError:
            return 0
        except Exception:
            return 0

    def _is_service_healthy(self, service_name):
        """فحص صحة خدمة معينة"""
        # محاكاة فحص الخدمة
        # في التطبيق الحقيقي، يمكن فحص الخدمات الفعلية
        return True

    def get_service_status(self):
        """الحصول على حالة الخدمة"""
        return {
            "status": "running" if self.is_running else "stopped",
            "active_alerts": len(self.alert_manager.get_alerts("active")),
            "total_alerts": len(self.alert_manager.get_alerts()),
            "last_check": datetime.now().isoformat()
        }

    def get_alerts(self, status=None):
        """الحصول على التنبيهات"""
        return self.alert_manager.get_alerts(status)

    def create_alert(self, alert_type, message, severity="info"):
        """إنشاء تنبيه جديد"""
        return self.alert_manager.create_alert(alert_type, message, severity)

    def dismiss_alert(self, alert_id):
        """إغلاق تنبيه"""
        return self.alert_manager.dismiss_alert(alert_id)


def main():
    """الدالة الرئيسية لتشغيل الخدمة"""
    try:
        service = AlertManagementService()
        service.start_service()

        # الحفاظ على تشغيل الخدمة
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        logger.info("تم إيقاف الخدمة بواسطة المستخدم")
    except Exception as e:
        logger.error(f"خطأ في تشغيل خدمة إدارة التنبيهات: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
