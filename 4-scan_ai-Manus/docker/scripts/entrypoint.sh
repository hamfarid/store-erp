#!/bin/bash
# نص برمجي لبدء تشغيل خادم API

set -e

# طباعة رسالة ترحيبية
echo "بدء تشغيل خادم API للنظام الزراعي المتكامل..."

# التحقق من وجود متغيرات البيئة الضرورية
if [ -z "$CONFIG_PATH" ]; then
    echo "تحذير: متغير البيئة CONFIG_PATH غير محدد، سيتم استخدام المسار الافتراضي"
    export CONFIG_PATH="/app/config/default.yaml"
fi

# الانتظار حتى تكون قاعدة البيانات جاهزة
if [ ! -z "$DB_HOST" ] && [ ! -z "$DB_PORT" ]; then
    echo "الانتظار حتى تكون قاعدة البيانات جاهزة..."
    /app/wait-for-it.sh "$DB_HOST:$DB_PORT" -t 60
    
    # إضافة تأخير إضافي للتأكد من أن قاعدة البيانات جاهزة تمامًا
    sleep 2
fi

# الانتظار حتى تكون خدمة Redis جاهزة (إذا كانت مستخدمة)
if [ ! -z "$REDIS_HOST" ] && [ ! -z "$REDIS_PORT" ]; then
    echo "الانتظار حتى تكون خدمة Redis جاهزة..."
    /app/wait-for-it.sh "$REDIS_HOST:$REDIS_PORT" -t 30
fi

# إنشاء مجلدات البيانات إذا لم تكن موجودة
mkdir -p /app/data /app/logs /app/uploads

# تنفيذ ترحيل قاعدة البيانات (إذا كان مطلوبًا)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "تنفيذ ترحيل قاعدة البيانات..."
    python -m src.database.migration_manager
fi

# تنفيذ الاختبارات (إذا كان مطلوبًا)
if [ "$RUN_TESTS" = "true" ]; then
    echo "تنفيذ الاختبارات..."
    python -m pytest /app/tests
fi

# تحديد ما إذا كان يجب تشغيل الخادم في وضع التطوير أو الإنتاج
if [ "$APP_ENV" = "development" ]; then
    echo "تشغيل الخادم في وضع التطوير..."
    RELOAD_FLAG="--reload"
else
    echo "تشغيل الخادم في وضع الإنتاج..."
    RELOAD_FLAG=""
fi

# طباعة معلومات التكوين
echo "معلومات التكوين:"
echo "- مسار التكوين: $CONFIG_PATH"
echo "- مستوى السجل: $LOG_LEVEL"
echo "- المضيفون المسموح بهم: $ALLOWED_HOSTS"
echo "- البيئة: $APP_ENV"

# تنفيذ الأمر المحدد
echo "بدء تنفيذ الأمر: $@"
exec "$@"
