"""
from flask import g
تطبيق Celery لنظام الزراعة الذكية
"""
import os
from celery import Celery

# إعداد متغيرات البيئة
# التأكد من استخدام المتغيرات البيئية الصحيحة
rabbitmq_user = os.getenv('RABBITMQ_USER', 'agri_ai_user')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'ATNqj7prF7au')
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
rabbitmq_port = os.getenv('RABBITMQ_PORT', '5672')

# بناء URL الاتصال - استخدام Redis كبديل لـ RabbitMQ
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', '6379')
redis_url = f'redis://{redis_host}:{redis_port}/0'

# محاولة استخدام RabbitMQ أولاً، ثم Redis كبديل
try:
    broker_url = os.getenv('CELERY_BROKER_URL', f'amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}//')
except Exception:
    # في حالة فشل RabbitMQ، استخدم Redis
    broker_url = redis_url

result_backend = os.getenv('REDIS_URL', redis_url)

# إنشاء تطبيق Celery
app = Celery('agri_ai_system')

# تكوين Celery
app.conf.update(
    broker_url=broker_url,
    result_backend=result_backend,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 دقيقة
    task_soft_time_limit=25 * 60,  # 25 دقيقة
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    broker_connection_retry_on_startup=True,  # إزالة التحذير
    task_routes={
        'src.tasks.*': {'queue': 'default'},
        'src.modules.*': {'queue': 'modules'},
    },
    beat_schedule={
        'health-check': {
            'task': 'src.tasks.health_check',
            'schedule': 60.0,  # كل دقيقة
        },
        'cleanup-old-data': {
            'task': 'src.tasks.cleanup_old_data',
            'schedule': 3600.0,  # كل ساعة
        },
    },
)

# استيراد المهام
try:
    from src.tasks import basic_tasks  # noqa: F401
except ImportError:
    pass

# تصدير التطبيق
celery = app

if __name__ == '__main__':
    app.start()
