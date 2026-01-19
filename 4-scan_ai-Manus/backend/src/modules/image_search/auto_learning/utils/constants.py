# /home/ubuntu/image_search_integration/auto_learning/utils/constants.py
"""
ثوابت مديول البحث الذاتي الذكي

يحتوي هذا الملف على الثوابت المستخدمة في مديول البحث الذاتي الذكي،
مثل رسائل الخطأ والنجاح، والقيم الافتراضية، والرموز الثابتة.
"""

# رسائل الخطأ
ERROR_MESSAGES = {
    # رسائل خطأ عامة
    "GENERAL": {
        "UNAUTHORIZED": "غير مصرح لك بتنفيذ هذه العملية",
        "NOT_FOUND": "العنصر المطلوب غير موجود",
        "VALIDATION_ERROR": "خطأ في التحقق من صحة البيانات",
        "DATABASE_ERROR": "خطأ في قاعدة البيانات",
        "INTERNAL_ERROR": "خطأ داخلي في النظام"
    },

    # رسائل خطأ الكلمات المفتاحية
    "KEYWORD": {
        "NOT_FOUND": "الكلمة المفتاحية غير موجودة",
        "ALREADY_EXISTS": "الكلمة المفتاحية موجودة بالفعل",
        "INVALID_CATEGORY": "تصنيف الكلمة المفتاحية غير صالح",
        "INVALID_PLANT_PART": "جزء النبات غير صالح",
        "RELATION_ERROR": "خطأ في العلاقة بين الكلمات المفتاحية",
        "SELF_RELATION": "لا يمكن إنشاء علاقة بين الكلمة المفتاحية ونفسها"
    },

    # رسائل خطأ المصادر
    "SOURCE": {
        "NOT_FOUND": "المصدر غير موجود",
        "ALREADY_EXISTS": "المصدر موجود بالفعل",
        "INVALID_DOMAIN": "نطاق المصدر غير صالح",
        "INVALID_TRUST_LEVEL": "مستوى الثقة غير صالح",
        "BLACKLISTED": "المصدر موجود في القائمة السوداء"
    },

    # رسائل خطأ محركات البحث
    "SEARCH_ENGINE": {
        "NOT_FOUND": "محرك البحث غير موجود",
        "ALREADY_EXISTS": "محرك البحث موجود بالفعل",
        "INVALID_URL": "عنوان URL غير صالح",
        "CONNECTION_ERROR": "خطأ في الاتصال بمحرك البحث",
        "TIMEOUT": "انتهت مهلة الاتصال بمحرك البحث",
        "INVALID_STRATEGY": "استراتيجية توزيع الحمل غير صالحة"
    },

    # رسائل خطأ التكامل
    "INTEGRATION": {
        "MEMORY_ERROR": "خطأ في الاتصال بالذاكرة المركزية",
        "A2A_ERROR": "خطأ في الاتصال بنظام A2A",
        "TELEGRAM_ERROR": "خطأ في الاتصال بمساعد Telegram"
    }
}

# رسائل النجاح
SUCCESS_MESSAGES = {
    # رسائل نجاح عامة
    "GENERAL": {
        "CREATED": "تم الإنشاء بنجاح",
        "UPDATED": "تم التحديث بنجاح",
        "DELETED": "تم الحذف بنجاح"
    },

    # رسائل نجاح الكلمات المفتاحية
    "KEYWORD": {
        "CREATED": "تم إنشاء الكلمة المفتاحية بنجاح",
        "UPDATED": "تم تحديث الكلمة المفتاحية بنجاح",
        "DELETED": "تم حذف الكلمة المفتاحية بنجاح",
        "RELATION_ADDED": "تم إضافة العلاقة بنجاح",
        "RELATION_REMOVED": "تم إزالة العلاقة بنجاح"
    },

    # رسائل نجاح المصادر
    "SOURCE": {
        "CREATED": "تم إنشاء المصدر بنجاح",
        "UPDATED": "تم تحديث المصدر بنجاح",
        "DELETED": "تم حذف المصدر بنجاح",
        "VERIFIED": "تم التحقق من المصدر بنجاح",
        "BLACKLISTED": "تم إضافة المصدر إلى القائمة السوداء بنجاح",
        "REMOVED_FROM_BLACKLIST": "تم إزالة المصدر من القائمة السوداء بنجاح"
    },

    # رسائل نجاح محركات البحث
    "SEARCH_ENGINE": {
        "CREATED": "تم إنشاء محرك البحث بنجاح",
        "UPDATED": "تم تحديث محرك البحث بنجاح",
        "DELETED": "تم حذف محرك البحث بنجاح",
        "TESTED": "تم اختبار محرك البحث بنجاح"
    },

    # رسائل نجاح التكامل
    "INTEGRATION": {
        "MEMORY_CONNECTED": "تم الاتصال بالذاكرة المركزية بنجاح",
        "A2A_CONNECTED": "تم الاتصال بنظام A2A بنجاح",
        "TELEGRAM_CONNECTED": "تم الاتصال بمساعد Telegram بنجاح"
    }
}

# القيم الافتراضية
DEFAULT_VALUES = {
    "PAGE": 1,
    "PAGE_SIZE": 10,
    "MAX_PAGE_SIZE": 100,
    "SEARCH_LIMIT": 20,
    "CACHE_EXPIRY": 3600,  # بالثواني (ساعة واحدة)
    "REQUEST_TIMEOUT": 30,  # بالثواني
    "MAX_RETRIES": 3
}

# رموز الحالة
STATUS_CODES = {
    "SUCCESS": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "CONFLICT": 409,
    "INTERNAL_ERROR": 500
}

# أنواع الملفات المدعومة
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff"]

# أقصى حجم للملفات (بالبايت)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 ميجابايت

# تنسيقات التاريخ
DATE_FORMATS = {
    "DEFAULT": "%Y-%m-%d %H:%M:%S",
    "ISO": "%Y-%m-%dT%H:%M:%S",
    "DATE_ONLY": "%Y-%m-%d",
    "TIME_ONLY": "%H:%M:%S"
}

# رموز اللغات المدعومة
SUPPORTED_LANGUAGES = ["ar", "en"]

# رموز الأحداث
EVENT_TYPES = {
    "KEYWORD_CREATED": "keyword_created",
    "KEYWORD_UPDATED": "keyword_updated",
    "KEYWORD_DELETED": "keyword_deleted",
    "SOURCE_CREATED": "source_created",
    "SOURCE_UPDATED": "source_updated",
    "SOURCE_DELETED": "source_deleted",
    "SOURCE_VERIFIED": "source_verified",
    "SOURCE_BLACKLISTED": "source_blacklisted",
    "SEARCH_ENGINE_CREATED": "search_engine_created",
    "SEARCH_ENGINE_UPDATED": "search_engine_updated",
    "SEARCH_ENGINE_DELETED": "search_engine_deleted",
    "SEARCH_PERFORMED": "search_performed",
    "MEMORY_UPDATED": "memory_updated",
    "A2A_INTERACTION": "a2a_interaction"
}

# رموز مستويات السجل
LOG_LEVELS = {
    "DEBUG": "debug",
    "INFO": "info",
    "WARNING": "warning",
    "ERROR": "error",
    "CRITICAL": "critical"
}

# رموز أنواع الإشعارات
NOTIFICATION_TYPES = {
    "INFO": "info",
    "SUCCESS": "success",
    "WARNING": "warning",
    "ERROR": "error"
}

# رموز أنواع التقارير
REPORT_TYPES = {
    "KEYWORD_USAGE": "keyword_usage",
    "SOURCE_RELIABILITY": "source_reliability",
    "SEARCH_ENGINE_PERFORMANCE": "search_engine_performance",
    "SYSTEM_USAGE": "system_usage"
}

# رموز أنواع التصدير
EXPORT_FORMATS = {
    "JSON": "json",
    "CSV": "csv",
    "EXCEL": "excel",
    "PDF": "pdf"
}
