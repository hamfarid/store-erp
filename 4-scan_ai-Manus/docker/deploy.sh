#!/bin/bash
# نص برمجي لبناء ونشر حاويات Docker للنظام الزراعي

# تعيين المتغيرات
PROJECT_ROOT=$(dirname "$(dirname "$(readlink -f "$0")")")
DOCKER_DIR="$PROJECT_ROOT/docker"
ENV_FILE="$PROJECT_ROOT/.env"

# التحقق من وجود ملف .env
if [ ! -f "$ENV_FILE" ]; then
    echo "خطأ: ملف .env غير موجود. يرجى إنشاء ملف .env باستخدام .env.example كقالب."
    exit 1
fi

# التحقق من تثبيت Docker و Docker Compose
if ! command -v docker &> /dev/null; then
    echo "خطأ: Docker غير مثبت. يرجى تثبيت Docker أولاً."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "خطأ: Docker Compose غير مثبت. يرجى تثبيت Docker Compose أولاً."
    exit 1
fi

# إنشاء المجلدات اللازمة إذا لم تكن موجودة
mkdir -p "$PROJECT_ROOT/data"
mkdir -p "$PROJECT_ROOT/models"

# بناء الصور
echo "بناء صور Docker..."
cd "$PROJECT_ROOT" || exit
docker-compose -f "$DOCKER_DIR/docker-compose.yml" build

# تشغيل الخدمات
echo "تشغيل الخدمات..."
docker-compose -f "$DOCKER_DIR/docker-compose.yml" up -d

# عرض حالة الخدمات
echo "حالة الخدمات:"
docker-compose -f "$DOCKER_DIR/docker-compose.yml" ps

echo "تم تشغيل النظام بنجاح. يمكن الوصول إلى واجهة المستخدم على http://localhost"
