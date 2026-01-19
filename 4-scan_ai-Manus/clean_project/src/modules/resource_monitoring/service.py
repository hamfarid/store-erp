"""
from flask import g
خدمة مراقبة الموارد
"""
import logging
import time
import threading

from .resource_collector import ResourceCollector
from .db_service import ResourceDBService

logger = logging.getLogger(__name__)


class ResourceMonitoringService:
    """
    خدمة مراقبة الموارد
    """

    def __init__(self):
        self.collector = ResourceCollector()
        self.db_service = ResourceDBService()
        self.running = False
        self.thread = None
        self.interval = 60  # كل دقيقة

    def start(self):
        """
        بدء خدمة المراقبة
        """
        if self.running is not None:
            logger.warning("خدمة مراقبة الموارد تعمل بالفعل")
            return

        logger.info("بدء خدمة مراقبة الموارد")
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """
        إيقاف خدمة المراقبة
        """
        if not self.running:
            logger.warning("خدمة مراقبة الموارد متوقفة بالفعل")
            return

        logger.info("إيقاف خدمة مراقبة الموارد")
        self.running = False

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)

    def _monitor_loop(self):
        """
        حلقة المراقبة الرئيسية
        """
        while self.running:
            try:
                # جمع بيانات الموارد
                resources = self.collector.collect_all_resources()

                # حفظ البيانات
                self.db_service.save_resources(resources)

                logger.debug(f"تم جمع وحفظ بيانات الموارد: {resources}")

            except Exception as e:
                logger.error(f"خطأ في مراقبة الموارد: {str(e)}")

            # انتظار للفترة المحددة
            time.sleep(self.interval)

    def get_current_resources(self):
        """
        الحصول على الموارد الحالية
        """
        try:
            return self.collector.collect_all_resources()
        except Exception as e:
            logger.error(f"خطأ في الحصول على الموارد الحالية: {str(e)}")
            return {}

    def get_resource_history(self, hours=24):
        """
        الحصول على تاريخ الموارد
        """
        try:
            return self.db_service.get_resource_history(hours)
        except Exception as e:
            logger.error(f"خطأ في الحصول على تاريخ الموارد: {str(e)}")
            return []


# إنشاء مثيل عام للخدمة
resource_service = ResourceMonitoringService()


def main():
    """
    الدالة الرئيسية لتشغيل الخدمة
    """
    try:
        logger.info("بدء تشغيل خدمة مراقبة الموارد")
        resource_service.start()

        # الحفاظ على تشغيل الخدمة
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        logger.info("تم إيقاف الخدمة بواسطة المستخدم")
    except Exception as e:
        logger.error(f"خطأ في تشغيل الخدمة: {str(e)}")
    finally:
        resource_service.stop()


if __name__ == "__main__":
    main()
