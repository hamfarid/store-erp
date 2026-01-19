"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/setup/config.py
الوصف: ملف التكوين لمديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# ثوابت
DEFAULT_TIMEZONE_SAUDI_ARABIA = 'Africa/Cairo'

# إعدادات مديول الإعداد
SETUP_CONFIG = {
    # حالة الإعداد الأولي للنظام
    'SETUP_COMPLETED': os.getenv('SETUP_COMPLETED', 'false').lower() == 'true',

    # مسار ملف الإعداد
    'SETUP_FILE_PATH': os.getenv('SETUP_FILE_PATH', 'storage/setup/setup_status.json'),

    # إعدادات قاعدة البيانات الافتراضية
    'DEFAULT_DB_CONNECTION': os.getenv('DB_CONNECTION', 'postgresql'),
    'DEFAULT_DB_HOST': os.getenv('DB_HOST', 'localhost'),
    'DEFAULT_DB_PORT': int(os.getenv('DB_PORT', 5432)),
    'DEFAULT_DB_DATABASE': os.getenv('DB_DATABASE', 'gaara_erp'),
    'DEFAULT_DB_USERNAME': os.getenv('DB_USERNAME', 'postgres'),
    'DEFAULT_DB_PASSWORD': os.getenv('DB_PASSWORD', ''),

    # إعدادات المسؤول الافتراضية
    'DEFAULT_ADMIN_EMAIL': os.getenv('ADMIN_EMAIL', 'admin@example.com'),
    'DEFAULT_ADMIN_PASSWORD': os.getenv('ADMIN_PASSWORD', 'admin123'),
    'DEFAULT_ADMIN_NAME': os.getenv('ADMIN_NAME', 'مسؤول النظام'),

    # إعدادات الشركة الافتراضية
    'DEFAULT_COMPANY_NAME': os.getenv('COMPANY_NAME', 'شركتي'),
    'DEFAULT_COMPANY_COUNTRY': os.getenv('COMPANY_COUNTRY', 'SA'),
    'DEFAULT_COMPANY_CURRENCY': os.getenv('COMPANY_CURRENCY', 'SAR'),
    'DEFAULT_COMPANY_TIMEZONE': os.getenv('COMPANY_TIMEZONE', DEFAULT_TIMEZONE_SAUDI_ARABIA),
    'DEFAULT_COMPANY_LOCALE': os.getenv('COMPANY_LOCALE', 'ar'),

    # خطوات الإعداد
    'SETUP_STEPS': [
        'database',
        'admin',
        'company',
        'modules',
        'settings',
        'finalize'
    ],

    # المديولات الأساسية التي يتم تثبيتها افتراضياً
    'CORE_MODULES': [
        'authentication',
        'user_management',
        'permissions',
        'memory',
        'ai_agent',
        'settings',
        'backup_restore'
    ],

    # المديولات الاختيارية
    'OPTIONAL_MODULES': [
        'plant_diagnosis',
        'image_processing',
        'image_search',
        'auto_learning'
    ],

    # إعدادات النسخ الاحتياطي
    'BACKUP_DIRECTORY': os.getenv('BACKUP_DIRECTORY', 'storage/backups'),
    'MAX_BACKUP_FILES': int(os.getenv('MAX_BACKUP_FILES', 10)),

    # إعدادات الأمان
    'SETUP_TOKEN_EXPIRY': int(os.getenv('SETUP_TOKEN_EXPIRY', 3600)),  # بالثواني
    'SETUP_SECRET_KEY': os.getenv('SETUP_SECRET_KEY', os.getenv('APP_SECRET_KEY', 'setup-secret-key')),

    # إعدادات الترقية
    'ALLOW_UPGRADE': os.getenv('ALLOW_UPGRADE', 'true').lower() == 'true',
    'UPGRADE_BACKUP': os.getenv('UPGRADE_BACKUP', 'true').lower() == 'true',
}

# قائمة الدول المدعومة
SUPPORTED_COUNTRIES = [
    {'code': 'SA', 'name': 'جمهورية مصر العربية', 'currency': 'SAR', 'timezone': DEFAULT_TIMEZONE_SAUDI_ARABIA, 'locale': 'ar'},
    {'code': 'AE', 'name': 'الإمارات العربية المتحدة', 'currency': 'AED', 'timezone': 'Asia/Dubai', 'locale': 'ar'},
    {'code': 'EG', 'name': 'مصر', 'currency': 'EGP', 'timezone': 'Africa/Cairo', 'locale': 'ar'},
    {'code': 'JO', 'name': 'الأردن', 'currency': 'JOD', 'timezone': 'Asia/Amman', 'locale': 'ar'},
    {'code': 'KW', 'name': 'الكويت', 'currency': 'KWD', 'timezone': 'Asia/Kuwait', 'locale': 'ar'},
    {'code': 'BH', 'name': 'البحرين', 'currency': 'BHD', 'timezone': 'Asia/Bahrain', 'locale': 'ar'},
    {'code': 'QA', 'name': 'قطر', 'currency': 'QAR', 'timezone': 'Asia/Qatar', 'locale': 'ar'},
    {'code': 'OM', 'name': 'عمان', 'currency': 'OMR', 'timezone': 'Asia/Muscat', 'locale': 'ar'},
    {'code': 'IQ', 'name': 'العراق', 'currency': 'IQD', 'timezone': 'Asia/Baghdad', 'locale': 'ar'},
    {'code': 'YE', 'name': 'اليمن', 'currency': 'YER', 'timezone': 'Asia/Aden', 'locale': 'ar'},
    {'code': 'PS', 'name': 'فلسطين', 'currency': 'ILS', 'timezone': 'Asia/Gaza', 'locale': 'ar'},
    {'code': 'LB', 'name': 'لبنان', 'currency': 'LBP', 'timezone': 'Asia/Beirut', 'locale': 'ar'},
    {'code': 'SY', 'name': 'سوريا', 'currency': 'SYP', 'timezone': 'Asia/Damascus', 'locale': 'ar'},
    {'code': 'SD', 'name': 'السودان', 'currency': 'SDG', 'timezone': 'Africa/Khartoum', 'locale': 'ar'},
    {'code': 'LY', 'name': 'ليبيا', 'currency': 'LYD', 'timezone': 'Africa/Tripoli', 'locale': 'ar'},
    {'code': 'TN', 'name': 'تونس', 'currency': 'TND', 'timezone': 'Africa/Tunis', 'locale': 'ar'},
    {'code': 'DZ', 'name': 'الجزائر', 'currency': 'DZD', 'timezone': 'Africa/Algiers', 'locale': 'ar'},
    {'code': 'MA', 'name': 'المغرب', 'currency': 'MAD', 'timezone': 'Africa/Casablanca', 'locale': 'ar'},
    {'code': 'MR', 'name': 'موريتانيا', 'currency': 'MRU', 'timezone': 'Africa/Nouakchott', 'locale': 'ar'},
    {'code': 'US', 'name': 'الولايات المتحدة الأمريكية', 'currency': 'USD', 'timezone': 'America/New_York', 'locale': 'en'},
    {'code': 'GB', 'name': 'المملكة المتحدة', 'currency': 'GBP', 'timezone': 'Europe/London', 'locale': 'en'},
]

# قائمة العملات المدعومة
SUPPORTED_CURRENCIES = [
    {'code': 'SAR', 'name': 'ريال سعودي', 'symbol': 'ر.س'},
    {'code': 'AED', 'name': 'درهم إماراتي', 'symbol': 'د.إ'},
    {'code': 'EGP', 'name': 'جنيه مصري', 'symbol': 'ج.م'},
    {'code': 'JOD', 'name': 'دينار أردني', 'symbol': 'د.أ'},
    {'code': 'KWD', 'name': 'دينار كويتي', 'symbol': 'د.ك'},
    {'code': 'BHD', 'name': 'دينار بحريني', 'symbol': 'د.ب'},
    {'code': 'QAR', 'name': 'ريال قطري', 'symbol': 'ر.ق'},
    {'code': 'OMR', 'name': 'ريال عماني', 'symbol': 'ر.ع'},
    {'code': 'IQD', 'name': 'دينار عراقي', 'symbol': 'د.ع'},
    {'code': 'YER', 'name': 'ريال يمني', 'symbol': 'ر.ي'},
    {'code': 'ILS', 'name': 'شيكل', 'symbol': '₪'},
    {'code': 'LBP', 'name': 'ليرة لبنانية', 'symbol': 'ل.ل'},
    {'code': 'SYP', 'name': 'ليرة سورية', 'symbol': 'ل.س'},
    {'code': 'SDG', 'name': 'جنيه سوداني', 'symbol': 'ج.س'},
    {'code': 'LYD', 'name': 'دينار ليبي', 'symbol': 'د.ل'},
    {'code': 'TND', 'name': 'دينار تونسي', 'symbol': 'د.ت'},
    {'code': 'DZD', 'name': 'دينار جزائري', 'symbol': 'د.ج'},
    {'code': 'MAD', 'name': 'درهم مغربي', 'symbol': 'د.م'},
    {'code': 'MRU', 'name': 'أوقية موريتانية', 'symbol': 'أ.م'},
    {'code': 'USD', 'name': 'دولار أمريكي', 'symbol': '$'},
    {'code': 'EUR', 'name': 'يورو', 'symbol': '€'},
    {'code': 'GBP', 'name': 'جنيه إسترليني', 'symbol': '£'},
]

# قائمة المناطق الزمنية المدعومة
SUPPORTED_TIMEZONES = [
    {'code': DEFAULT_TIMEZONE_SAUDI_ARABIA, 'name': 'الرياض (GMT+3)'},
    {'code': 'Asia/Dubai', 'name': 'دبي (GMT+4)'},
    {'code': 'Africa/Cairo', 'name': 'القاهرة (GMT+2)'},
    {'code': 'Asia/Amman', 'name': 'عمان (GMT+3)'},
    {'code': 'Asia/Kuwait', 'name': 'الكويت (GMT+3)'},
    {'code': 'Asia/Bahrain', 'name': 'المنامة (GMT+3)'},
    {'code': 'Asia/Qatar', 'name': 'الدوحة (GMT+3)'},
    {'code': 'Asia/Muscat', 'name': 'مسقط (GMT+4)'},
    {'code': 'Asia/Baghdad', 'name': 'بغداد (GMT+3)'},
    {'code': 'Asia/Aden', 'name': 'عدن (GMT+3)'},
    {'code': 'Asia/Gaza', 'name': 'غزة (GMT+2)'},
    {'code': 'Asia/Beirut', 'name': 'بيروت (GMT+2)'},
    {'code': 'Asia/Damascus', 'name': 'دمشق (GMT+2)'},
    {'code': 'Africa/Khartoum', 'name': 'الخرطوم (GMT+2)'},
    {'code': 'Africa/Tripoli', 'name': 'طرابلس (GMT+2)'},
    {'code': 'Africa/Tunis', 'name': 'تونس (GMT+1)'},
    {'code': 'Africa/Algiers', 'name': 'الجزائر (GMT+1)'},
    {'code': 'Africa/Casablanca', 'name': 'الدار البيضاء (GMT+1)'},
    {'code': 'Africa/Nouakchott', 'name': 'نواكشوط (GMT+0)'},
    {'code': 'UTC', 'name': 'التوقيت العالمي المنسق (GMT+0)'},
    {'code': 'Europe/London', 'name': 'لندن (GMT+0/+1)'},
    {'code': 'America/New_York', 'name': 'نيويورك (GMT-5/-4)'},
]

# قائمة اللغات المدعومة
SUPPORTED_LOCALES = [
    {'code': 'ar', 'name': 'العربية', 'direction': 'rtl'},
    {'code': 'en', 'name': 'الإنجليزية', 'direction': 'ltr'},
]
