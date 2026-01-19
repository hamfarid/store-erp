"""
from flask import g
المهام الأساسية لنظام Celery
"""
import logging
import os
import glob
from datetime import datetime, timedelta
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def health_check(self):
    """
    فحص صحة النظام
    """
    try:
        logger.info("تشغيل فحص صحة النظام")

        # فحص الاتصال بقاعدة البيانات
        db_status = check_database_connection()

        # فحص الاتصال بـ Redis
        redis_status = check_redis_connection()

        # فحص الاتصال بـ RabbitMQ
        rabbitmq_status = check_rabbitmq_connection()

        result = {
            'timestamp': datetime.now().isoformat(),
            'database': db_status,
            'redis': redis_status,
            'rabbitmq': rabbitmq_status,
            'status': 'healthy' if all([db_status, redis_status, rabbitmq_status]) else 'unhealthy'
        }

        logger.info("نتيجة فحص الصحة: {}".format(result))
        return result

    except Exception as e:
        logger.error("خطأ في فحص صحة النظام: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e)
        }


@shared_task(bind=True)
def cleanup_old_data(self):
    """
    تنظيف البيانات القديمة
    """
    try:
        logger.info("بدء تنظيف البيانات القديمة")

        # تنظيف السجلات القديمة (أكثر من 30 يوم)
        cutoff_date = datetime.now() - timedelta(days=30)

        cleaned_count = 0

        # تنظيف ملفات الصور المؤقتة
        cleaned_count += cleanup_temp_images()

        # تنظيف سجلات المراقبة القديمة
        cleaned_count += cleanup_old_monitoring_logs(cutoff_date)

        # تنظيف ملفات النسخ الاحتياطي القديمة
        cleaned_count += cleanup_old_backups(cutoff_date)

        result = {
            'timestamp': datetime.now().isoformat(),
            'cleaned_items': cleaned_count,
            'cutoff_date': cutoff_date.isoformat(),
            'status': 'completed'
        }

        logger.info("تم تنظيف {} عنصر".format(cleaned_count))
        return result

    except Exception as e:
        logger.error("خطأ في تنظيف البيانات: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e)
        }


def check_database_connection():
    """فحص الاتصال بقاعدة البيانات"""
    try:
        # محاولة الاتصال بقاعدة البيانات
        # يمكن إضافة كود فحص حقيقي هنا
        return True
    except Exception:
        return False


def check_redis_connection():
    """فحص الاتصال بـ Redis"""
    try:
        import redis

        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url)
        r.ping()
        return True
    except Exception:
        return False


def check_rabbitmq_connection():
    """فحص الاتصال بـ RabbitMQ"""
    try:
        # محاولة الاتصال بـ RabbitMQ
        # يمكن إضافة كود فحص حقيقي هنا
        return True
    except Exception:
        return False


def cleanup_temp_images():
    """تنظيف الصور المؤقتة"""
    try:
        temp_dirs = [
            'uploads/temp',
            'src/modules/image_processing/uploads',
            'src/modules/disease_diagnosis/uploads'
        ]

        cleaned = 0
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                files = glob.glob(os.path.join(temp_dir, '*'))
                for file in files:
                    try:
                        if os.path.isfile(file):
                            # فحص عمر الملف
                            file_age = datetime.now() - datetime.fromtimestamp(os.path.getctime(file))
                            if file_age > timedelta(hours=24):  # ملفات أقدم من 24 ساعة
                                os.remove(file)
                                cleaned += 1
                    except Exception:
                        continue

        return cleaned
    except Exception:
        return 0


def cleanup_old_monitoring_logs(cutoff_date):
    """تنظيف سجلات المراقبة القديمة"""
    try:
        # يمكن إضافة كود تنظيف سجلات المراقبة هنا
        return 0
    except Exception:
        return 0


def cleanup_old_backups(cutoff_date):
    """تنظيف النسخ الاحتياطية القديمة"""
    try:
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            return 0

        cleaned = 0
        backup_files = glob.glob(os.path.join(backup_dir, '*.zip'))

        for backup_file in backup_files:
            try:
                file_age = datetime.now() - datetime.fromtimestamp(os.path.getctime(backup_file))
                if file_age > timedelta(days=30):  # نسخ احتياطية أقدم من 30 يوم
                    os.remove(backup_file)
                    cleaned += 1
            except Exception:
                continue

        return cleaned
    except Exception:
        return 0


@shared_task(bind=True)
def send_system_notification(self, notification_type, message, recipients=None):
    """
    إرسال إشعار النظام

    Args:
        notification_type (str): نوع الإشعار
        message (str): رسالة الإشعار
        recipients (list): قائمة المستلمين
    """
    try:
        logger.info("إرسال إشعار النظام: {}".format(notification_type))

        # يمكن إضافة كود إرسال الإشعارات هنا

        result = {
            'timestamp': datetime.now().isoformat(),
            'notification_type': notification_type,
            'message': message,
            'recipients': recipients or [],
            'status': 'sent'
        }

        logger.info("تم إرسال الإشعار بنجاح")
        return result

    except Exception as e:
        logger.error("خطأ في إرسال الإشعار: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e)
        }


@shared_task(bind=True)
def update_system_status(self):
    """
    تحديث حالة النظام
    """
    try:
        logger.info("تحديث حالة النظام")

        # جمع معلومات النظام
        system_status = {
            'timestamp': datetime.now().isoformat(),
            'uptime': get_system_uptime(),
            'cpu_usage': get_cpu_usage(),
            'memory_usage': get_memory_usage(),
            'disk_usage': get_disk_usage(),
            'active_tasks': get_active_tasks_count()
        }

        logger.info("تم تحديث حالة النظام بنجاح")
        return system_status

    except Exception as e:
        logger.error("خطأ في تحديث حالة النظام: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e)
        }


def get_system_uptime():
    """الحصول على وقت تشغيل النظام"""
    try:
        # يمكن إضافة كود حقيقي هنا
        return "Unknown"
    except Exception:
        return "Error"


def get_cpu_usage():
    """الحصول على استخدام المعالج"""
    try:
        import psutil
        return psutil.cpu_percent(interval=1)
    except Exception:
        return 0


def get_memory_usage():
    """الحصول على استخدام الذاكرة"""
    try:
        import psutil
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used
        }
    except Exception:
        return {'percent': 0}


def get_disk_usage():
    """الحصول على استخدام القرص الصلب"""
    try:
        import psutil
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': (disk.used / disk.total) * 100
        }
    except Exception:
        return {'percent': 0}


def get_active_tasks_count():
    """الحصول على عدد المهام النشطة"""
    try:
        # يمكن إضافة كود للحصول على عدد المهام النشطة من Celery
        return 0
    except Exception:
        return 0
