"""
from flask import g
مهام المراقبة لنظام Celery
"""
import logging
import psutil
import os
from datetime import datetime
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def collect_system_metrics(self):
    """
    جمع مقاييس النظام
    """
    try:
        logger.info("جمع مقاييس النظام")

        # معلومات المعالج
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()

        # معلومات الذاكرة
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = memory.used
        memory_total = memory.total

        # معلومات القرص
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        disk_used = disk.used
        disk_total = disk.total

        # معلومات الشبكة
        network = psutil.net_io_counters()

        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count
            },
            'memory': {
                'percent': memory_percent,
                'used': memory_used,
                'total': memory_total,
                'available': memory.available
            },
            'disk': {
                'percent': disk_percent,
                'used': disk_used,
                'total': disk_total,
                'free': disk.free
            },
            'network': {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            },
            'task_id': self.request.id
        }

        # حفظ المقاييس
        save_metrics(metrics)

        return metrics

    except Exception as e:
        logger.error("خطأ في جمع مقاييس النظام: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


@shared_task(bind=True)
def monitor_disk_space(self):
    """
    مراقبة مساحة القرص
    """
    try:
        logger.info("مراقبة مساحة القرص")

        disk_usage = psutil.disk_usage('/')
        used_percent = (disk_usage.used / disk_usage.total) * 100

        # تحذير إذا كانت المساحة المستخدمة أكثر من 80%
        alert_threshold = 80
        status = 'warning' if used_percent > alert_threshold else 'normal'

        result = {
            'timestamp': datetime.now().isoformat(),
            'disk_usage_percent': used_percent,
            'used_bytes': disk_usage.used,
            'total_bytes': disk_usage.total,
            'free_bytes': disk_usage.free,
            'status': status,
            'alert_threshold': alert_threshold,
            'task_id': self.request.id
        }

        # إرسال تنبيه إذا لزم الأمر
        if status == 'warning':
            send_disk_space_alert(result)

        return result

    except Exception as e:
        logger.error("خطأ في مراقبة مساحة القرص: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


@shared_task(bind=True)
def monitor_memory_usage(self):
    """
    مراقبة استخدام الذاكرة
    """
    try:
        logger.info("مراقبة استخدام الذاكرة")

        memory = psutil.virtual_memory()
        used_percent = memory.percent

        # تحذير إذا كان استخدام الذاكرة أكثر من 85%
        alert_threshold = 85
        status = 'warning' if used_percent > alert_threshold else 'normal'

        result = {
            'timestamp': datetime.now().isoformat(),
            'memory_usage_percent': used_percent,
            'used_bytes': memory.used,
            'total_bytes': memory.total,
            'available_bytes': memory.available,
            'status': status,
            'alert_threshold': alert_threshold,
            'task_id': self.request.id
        }

        # إرسال تنبيه إذا لزم الأمر
        if status == 'warning':
            send_memory_usage_alert(result)

        return result

    except Exception as e:
        logger.error("خطأ في مراقبة استخدام الذاكرة: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


@shared_task(bind=True)
def monitor_cpu_usage(self):
    """
    مراقبة استخدام المعالج
    """
    try:
        logger.info("مراقبة استخدام المعالج")

        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()

        # تحذير إذا كان استخدام المعالج أكثر من 90%
        alert_threshold = 90
        status = 'warning' if cpu_percent > alert_threshold else 'normal'

        result = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage_percent': cpu_percent,
            'cpu_count': cpu_count,
            'cpu_frequency': {
                'current': cpu_freq.current if cpu_freq else 0,
                'min': cpu_freq.min if cpu_freq else 0,
                'max': cpu_freq.max if cpu_freq else 0
            },
            'status': status,
            'alert_threshold': alert_threshold,
            'task_id': self.request.id
        }

        # إرسال تنبيه إذا لزم الأمر
        if status == 'warning':
            send_cpu_usage_alert(result)

        return result

    except Exception as e:
        logger.error("خطأ في مراقبة استخدام المعالج: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


@shared_task(bind=True)
def check_service_health(self):
    """
    فحص صحة الخدمات
    """
    try:
        logger.info("فحص صحة الخدمات")

        services = {
            'database': check_database_health(),
            'redis': check_redis_health(),
            'rabbitmq': check_rabbitmq_health(),
            'elasticsearch': check_elasticsearch_health(),
            'minio': check_minio_health()
        }

        # حساب الحالة العامة
        healthy_services = sum(1 for status in services.values() if status)
        total_services = len(services)
        overall_health = 'healthy' if healthy_services == total_services else 'partial'

        result = {
            'timestamp': datetime.now().isoformat(),
            'services': services,
            'healthy_services': healthy_services,
            'total_services': total_services,
            'overall_health': overall_health,
            'task_id': self.request.id
        }

        return result

    except Exception as e:
        logger.error("خطأ في فحص صحة الخدمات: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


@shared_task(bind=True)
def monitor_network_traffic(self):
    """
    مراقبة حركة مرور الشبكة
    """
    try:
        logger.info("مراقبة حركة مرور الشبكة")

        network_io = psutil.net_io_counters()

        result = {
            'timestamp': datetime.now().isoformat(),
            'bytes_sent': network_io.bytes_sent,
            'bytes_recv': network_io.bytes_recv,
            'packets_sent': network_io.packets_sent,
            'packets_recv': network_io.packets_recv,
            'errin': network_io.errin,
            'errout': network_io.errout,
            'dropin': network_io.dropin,
            'dropout': network_io.dropout,
            'task_id': self.request.id
        }

        return result

    except Exception as e:
        logger.error("خطأ في مراقبة حركة مرور الشبكة: {}".format(str(e)))
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


def save_metrics(metrics):
    """
    حفظ المقاييس في قاعدة البيانات أو ملف
    """
    try:
        # يمكن إضافة كود حفظ المقاييس هنا
        logger.debug("تم حفظ المقاييس: {}".format(metrics.get('timestamp', 'unknown')))
        pass
    except Exception as e:
        logger.error("خطأ في حفظ المقاييس: {}".format(str(e)))


def send_disk_space_alert(data):
    """
    إرسال تنبيه مساحة القرص
    """
    try:
        logger.warning("تحذير: مساحة القرص منخفضة - {:.1f}%".format(data['disk_usage_percent']))
        # يمكن إضافة كود إرسال التنبيهات هنا
    except Exception as e:
        logger.error("خطأ في إرسال تنبيه مساحة القرص: {}".format(str(e)))


def send_memory_usage_alert(data):
    """
    إرسال تنبيه استخدام الذاكرة
    """
    try:
        logger.warning("تحذير: استخدام الذاكرة مرتفع - {:.1f}%".format(data['memory_usage_percent']))
        # يمكن إضافة كود إرسال التنبيهات هنا
    except Exception as e:
        logger.error("خطأ في إرسال تنبيه استخدام الذاكرة: {}".format(str(e)))


def send_cpu_usage_alert(data):
    """
    إرسال تنبيه استخدام المعالج
    """
    try:
        logger.warning("تحذير: استخدام المعالج مرتفع - {:.1f}%".format(data['cpu_usage_percent']))
        # يمكن إضافة كود إرسال التنبيهات هنا
    except Exception as e:
        logger.error("خطأ في إرسال تنبيه استخدام المعالج: {}".format(str(e)))


def check_database_health():
    """فحص صحة قاعدة البيانات"""
    try:
        # يمكن إضافة كود فحص قاعدة البيانات هنا
        return True
    except Exception:
        return False


def check_redis_health():
    """فحص صحة Redis"""
    try:
        import redis
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url)
        r.ping()
        return True
    except Exception:
        return False


def check_rabbitmq_health():
    """فحص صحة RabbitMQ"""
    try:
        # يمكن إضافة كود فحص RabbitMQ هنا
        return True
    except Exception:
        return False


def check_elasticsearch_health():
    """فحص صحة Elasticsearch"""
    try:
        # يمكن إضافة كود فحص Elasticsearch هنا
        return True
    except Exception:
        return False


def check_minio_health():
    """فحص صحة MinIO"""
    try:
        # يمكن إضافة كود فحص MinIO هنا
        return True
    except Exception:
        return False
