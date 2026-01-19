# /home/ubuntu/image_search_integration/auto_learning/config.py
"""
ملف إعدادات مديول البحث الذاتي الذكي

يحتوي هذا الملف على الإعدادات والثوابت الخاصة بمديول البحث الذاتي الذكي،
بما في ذلك إعدادات الاتصال بالخدمات الخارجية وإعدادات التكامل مع المديولات الأخرى.
"""

# إعدادات عامة
MODULE_NAME = "auto_learning"
MODULE_VERSION = "1.0.0"
MODULE_DESCRIPTION = "مديول البحث الذاتي الذكي لتحسين عمليات البحث عن صور الإصابات والآفات النباتية"

# إعدادات الذاكرة المركزية
MEMORY_API_URL = "http://localhost:8000/api/memory"
MEMORY_API_TIMEOUT = 30  # بالثواني

# إعدادات نظام A2A
A2A_API_URL = "http://localhost:8000/api/a2a"
A2A_API_TIMEOUT = 30  # بالثواني

# إعدادات محركات البحث
DEFAULT_SEARCH_ENGINE_TIMEOUT = 60  # بالثواني
MAX_SEARCH_RESULTS = 100
SEARCH_CACHE_EXPIRY = 3600  # بالثواني (ساعة واحدة)

# إعدادات تقييم المصادر
TRUST_LEVEL_MIN = 1
TRUST_LEVEL_MAX = 10
TRUST_LEVEL_DEFAULT = 5
BLACKLIST_THRESHOLD = 3  # عدد التقييمات السلبية قبل إضافة المصدر للقائمة السوداء

# إعدادات الكلمات المفتاحية
MAX_SYNONYMS_PER_KEYWORD = 20
MAX_RELATIONS_PER_KEYWORD = 50

# إعدادات التصنيف
CATEGORIES = [
    "PLANT",      # نبات
    "DISEASE",    # مرض
    "PEST",       # آفة
    "TECHNIQUE",  # تقنية
    "FERTILIZER",  # سماد
    "EQUIPMENT",  # معدات
    "SYMPTOM",    # عرض
    "OTHER"       # أخرى
]

PLANT_PARTS = [
    "LEAF",   # ورقة
    "STEM",   # ساق
    "ROOT",   # جذر
    "FLOWER",  # زهرة
    "FRUIT",  # ثمرة
    "SEED"    # بذرة
]

RELATION_TYPES = [
    "SYNONYM",   # مرادف
    "BROADER",   # أوسع
    "NARROWER",  # أضيق
    "RELATED",   # ذو صلة
    "CAUSE",     # سبب
    "EFFECT",    # نتيجة
    "PART_OF",   # جزء من
    "HAS_PART"   # يحتوي على
]

# إعدادات توزيع الحمل
LOAD_BALANCING_STRATEGIES = [
    "ROUND_ROBIN",  # التناوب الدائري
    "WEIGHTED",    # الموزون
    "LEAST_USED",  # الأقل استخداماً
    "PRIORITY",    # الأولوية
    "RANDOM"       # عشوائي
]

DEFAULT_LOAD_BALANCING_STRATEGY = "ROUND_ROBIN"

# إعدادات الصلاحيات
PERMISSION_LEVELS = {
    "READ": "read",           # قراءة
    "WRITE": "write",         # كتابة
    "DELETE": "delete",       # حذف
    "ADMIN": "admin",         # مدير
    "VERIFY": "verify",       # تحقق
    "TEST": "test",           # اختبار
    "APPROVE": "approve"      # موافقة
}

# إعدادات الاختبارات
TEST_DATABASE_URI = "sqlite:///test.db"
