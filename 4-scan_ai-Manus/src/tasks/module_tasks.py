"""
from flask import g
مهام المديولات لنظام Celery
"""
import logging
from datetime import datetime
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def start_module_task(self, module_id):
    """
    مهمة تشغيل مديول
    """
    try:
        logger.info(f"بدء تشغيل المديول: {module_id}")

        # محاولة استيراد وتشغيل المديول
        result = start_module_service(module_id)

        return {
            'timestamp': datetime.now().isoformat(),
            'module_id': module_id,
            'status': 'started' if result else 'failed',
            'task_id': self.request.id
        }

    except Exception as e:
        logger.error(f"خطأ في تشغيل المديول {module_id}: {str(e)}")
        return {
            'timestamp': datetime.now().isoformat(),
            'module_id': module_id,
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


@shared_task(bind=True)
def stop_module_task(self, module_id):
    """
    مهمة إيقاف مديول
    """
    try:
        logger.info(f"بدء إيقاف المديول: {module_id}")

        # محاولة إيقاف المديول
        result = stop_module_service(module_id)

        return {
            'timestamp': datetime.now().isoformat(),
            'module_id': module_id,
            'status': 'stopped' if result else 'failed',
            'task_id': self.request.id
        }

    except Exception as e:
        logger.error(f"خطأ في إيقاف المديول {module_id}: {str(e)}")
        return {
            'timestamp': datetime.now().isoformat(),
            'module_id': module_id,
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


@shared_task(bind=True)
def restart_module_task(self, module_id):
    """
    مهمة إعادة تشغيل مديول
    """
    try:
        logger.info(f"بدء إعادة تشغيل المديول: {module_id}")

        # إيقاف المديول أولاً
        stop_result = stop_module_service(module_id)

        # انتظار قصير
        import time
        time.sleep(2)

        # تشغيل المديول مرة أخرى
        start_result = start_module_service(module_id)

        return {
            'timestamp': datetime.now().isoformat(),
            'module_id': module_id,
            'status': 'restarted' if (stop_result and start_result) else 'failed',
            'task_id': self.request.id
        }

    except Exception as e:
        logger.error(f"خطأ في إعادة تشغيل المديول {module_id}: {str(e)}")
        return {
            'timestamp': datetime.now().isoformat(),
            'module_id': module_id,
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


@shared_task(bind=True)
def monitor_modules_task(self):
    """
    مهمة مراقبة حالة المديولات
    """
    try:
        logger.info("بدء مراقبة المديولات")

        # الحصول على قائمة المديولات
        modules = get_all_modules()

        module_statuses = {}

        for module in modules:
            try:
                status = get_module_status(module['id'])
                module_statuses[module['id']] = {
                    'status': status,
                    'last_checked': datetime.now().isoformat()
                }
            except Exception as e:
                module_statuses[module['id']] = {
                    'status': 'error',
                    'error': str(e),
                    'last_checked': datetime.now().isoformat()
                }

        return {
            'timestamp': datetime.now().isoformat(),
            'modules': module_statuses,
            'total_modules': len(modules),
            'task_id': self.request.id
        }

    except Exception as e:
        logger.error(f"خطأ في مراقبة المديولات: {str(e)}")
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e),
            'task_id': self.request.id
        }


def start_module_service(module_id):
    """
    خدمة تشغيل المديول
    """
    try:
        # محاولة استيراد مديول إدارة المديولات
        from src.modules.module_management.api import start_module
        return start_module(module_id)
    except ImportError:
        logger.warning(f"مديول إدارة المديولات غير متوفر لتشغيل {module_id}")
        return False
    except Exception as e:
        logger.error(f"خطأ في تشغيل المديول {module_id}: {str(e)}")
        return False


def stop_module_service(module_id):
    """
    خدمة إيقاف المديول
    """
    try:
        # محاولة استيراد مديول إدارة المديولات
        from src.modules.module_management.api import stop_module
        return stop_module(module_id)
    except ImportError:
        logger.warning(f"مديول إدارة المديولات غير متوفر لإيقاف {module_id}")
        return False
    except Exception as e:
        logger.error(f"خطأ في إيقاف المديول {module_id}: {str(e)}")
        return False


def get_module_status(module_id):
    """
    الحصول على حالة المديول
    """
    try:
        # محاولة استيراد مديول إدارة المديولات
        from src.modules.module_management.api import get_module_status as get_status
        return get_status(module_id)
    except ImportError:
        return 'unknown'
    except Exception:
        return 'error'


def get_all_modules():
    """
    الحصول على جميع المديولات
    """
    try:
        # محاولة استيراد مديول إدارة المديولات
        from src.modules.module_management.api import discover_modules
        return discover_modules()
    except ImportError:
        return []
    except Exception:
        return []
