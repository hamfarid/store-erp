"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/notifications/config.py
الوصف: ملف التكوين لمديول الإشعارات
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
تاريخ التعديل: 29 مايو 2025 - إضافة دعم إشعارات تيليجرام
"""

import os

from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعدادات مديول الإشعارات
NOTIFICATIONS_CONFIG = {
    # إعدادات البريد الإلكتروني
    'EMAIL_NOTIFICATIONS_ENABLED': os.getenv('EMAIL_NOTIFICATIONS_ENABLED', 'true').lower() == 'true',
    'EMAIL_TEMPLATE_DIR': os.getenv('EMAIL_TEMPLATE_DIR', 'src/modules/notifications/templates/email'),

    # إعدادات الإشعارات داخل النظام
    'IN_APP_NOTIFICATIONS_ENABLED': os.getenv('IN_APP_NOTIFICATIONS_ENABLED', 'true').lower() == 'true',
    'MAX_IN_APP_NOTIFICATIONS': int(os.getenv('MAX_IN_APP_NOTIFICATIONS', 100)),
    'NOTIFICATION_EXPIRY_DAYS': int(os.getenv('NOTIFICATION_EXPIRY_DAYS', 30)),

    # إعدادات الإشعارات عبر الرسائل القصيرة
    'SMS_NOTIFICATIONS_ENABLED': os.getenv('SMS_NOTIFICATIONS_ENABLED', 'false').lower() == 'true',
    'SMS_PROVIDER': os.getenv('SMS_PROVIDER', 'twilio'),
    'SMS_TWILIO_SID': os.getenv('SMS_TWILIO_SID', ''),
    'SMS_TWILIO_TOKEN': os.getenv('SMS_TWILIO_TOKEN', ''),
    'SMS_TWILIO_FROM': os.getenv('SMS_TWILIO_FROM', ''),

    # إعدادات الإشعارات عبر تطبيقات الجوال
    'PUSH_NOTIFICATIONS_ENABLED': os.getenv('PUSH_NOTIFICATIONS_ENABLED', 'false').lower() == 'true',
    'PUSH_PROVIDER': os.getenv('PUSH_PROVIDER', 'firebase'),
    'FIREBASE_SERVER_KEY': os.getenv('FIREBASE_SERVER_KEY', ''),

    # إعدادات الإشعارات عبر Webhook
    'WEBHOOK_NOTIFICATIONS_ENABLED': os.getenv('WEBHOOK_NOTIFICATIONS_ENABLED', 'false').lower() == 'true',
    'WEBHOOK_DEFAULT_URL': os.getenv('WEBHOOK_DEFAULT_URL', ''),
    'WEBHOOK_SECRET': os.getenv('WEBHOOK_SECRET', ''),

    # إعدادات الإشعارات عبر تيليجرام
    'TELEGRAM_NOTIFICATIONS_ENABLED': os.getenv('TELEGRAM_NOTIFICATIONS_ENABLED', 'false').lower() == 'true',
    'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'TELEGRAM_DEFAULT_CHAT_ID': os.getenv('TELEGRAM_DEFAULT_CHAT_ID', ''),
    'TELEGRAM_ADMIN_CHAT_IDS': os.getenv('TELEGRAM_ADMIN_CHAT_IDS', ''),

    # إعدادات الجدولة
    'SCHEDULED_NOTIFICATIONS_ENABLED': os.getenv('SCHEDULED_NOTIFICATIONS_ENABLED', 'true').lower() == 'true',
    # بالثواني
    'NOTIFICATION_CHECK_INTERVAL': int(os.getenv('NOTIFICATION_CHECK_INTERVAL', 60)),

    # إعدادات التجميع
    'NOTIFICATION_AGGREGATION_ENABLED': os.getenv('NOTIFICATION_AGGREGATION_ENABLED', 'true').lower() == 'true',
    'NOTIFICATION_AGGREGATION_THRESHOLD': int(os.getenv('NOTIFICATION_AGGREGATION_THRESHOLD', 5)),
    # بالثواني
    'NOTIFICATION_AGGREGATION_TIME_WINDOW': int(os.getenv('NOTIFICATION_AGGREGATION_TIME_WINDOW', 3600)),
}

# أنواع الإشعارات
NOTIFICATION_TYPES = {
    'INFO': 'info',
    'SUCCESS': 'success',
    'WARNING': 'warning',
    'ERROR': 'error',
    'SYSTEM': 'system',
    'SECURITY': 'security',
    'TASK': 'task',
    'MESSAGE': 'message',
    'UPDATE': 'update',
}

# أولويات الإشعارات
NOTIFICATION_PRIORITIES = {
    'LOW': 'low',
    'MEDIUM': 'medium',
    'HIGH': 'high',
    'URGENT': 'urgent',
}

# قنوات الإشعارات
NOTIFICATION_CHANNELS = {
    'EMAIL': 'email',
    'IN_APP': 'in_app',
    'SMS': 'sms',
    'PUSH': 'push',
    'WEBHOOK': 'webhook',
    'TELEGRAM': 'telegram',  # إضافة قناة تيليجرام
}

# قوالب الإشعارات الافتراضية
DEFAULT_NOTIFICATION_TEMPLATES = {
    'welcome': {
        'subject': 'مرحباً بك في نظام Gaara ERP',
        'template': 'welcome.html',
    },
    'password_reset': {
        'subject': 'إعادة تعيين كلمة المرور',
        'template': 'password_reset.html',
    },
    'account_locked': {
        'subject': 'تم قفل حسابك',
        'template': 'account_locked.html',
    },
    'new_login': {
        'subject': 'تسجيل دخول جديد',
        'template': 'new_login.html',
    },
    'system_update': {
        'subject': 'تحديث النظام',
        'template': 'system_update.html',
    },
}
