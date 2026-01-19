#!/bin/bash
# نص برمجي لاختبار إعداد Docker

set -e

# تعيين المتغيرات
PROJECT_ROOT=$(dirname "$(dirname "$(readlink -f "$0")")")
DOCKER_DIR="$PROJECT_ROOT/docker"
ENV_FILE="$DOCKER_DIR/env/development.env"

# التحقق من وجود Docker و Docker Compose
if ! command -v docker &> /dev/null; then
    echo "خطأ: Docker غير مثبت. يرجى تثبيت Docker أولاً."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "خطأ: Docker Compose غير مثبت. يرجى تثبيت Docker Compose أولاً."
    exit 1
fi

# إنشاء ملف .env للاختبار إذا لم يكن موجودًا
if [ ! -f "$ENV_FILE" ]; then
    echo "إنشاء ملف .env للاختبار..."
    mkdir -p "$(dirname "$ENV_FILE")"
    cat > "$ENV_FILE" << EOF
# ملف بيئة الاختبار
APP_ENV=development
LOG_LEVEL=DEBUG
APP_PORT=8000
IMAGE_PROCESSOR_PORT=5000
NGINX_PORT=80
DOCKER_API_SERVER_REPLICAS=1
DOCKER_IMAGE_PROCESSOR_REPLICAS=1
API_CPU_LIMIT=0.5
API_MEMORY_LIMIT=512M
PROCESSOR_CPU_LIMIT=1
PROCESSOR_MEMORY_LIMIT=1G
NGINX_CPU_LIMIT=0.2
NGINX_MEMORY_LIMIT=128M
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=agricultural_ai_test
SECURITY_ALLOWED_HOSTS=localhost,127.0.0.1,api_server
RUN_MIGRATIONS=true
EOF
    echo "تم إنشاء ملف .env للاختبار بنجاح."
fi

# إنشاء المجلدات اللازمة
echo "إنشاء المجلدات اللازمة..."
mkdir -p "$PROJECT_ROOT/data"
mkdir -p "$PROJECT_ROOT/models"
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/uploads"
mkdir -p "$PROJECT_ROOT/temp"
mkdir -p "$PROJECT_ROOT/data/primitive_features"
mkdir -p "$PROJECT_ROOT/data/standard_features"
mkdir -p "$PROJECT_ROOT/data/comparison_results"
mkdir -p "$PROJECT_ROOT/data/visualizations"

# بناء الصور
echo "بناء صور Docker للاختبار..."
cd "$DOCKER_DIR" || exit
docker-compose build --no-cache

# تشغيل الخدمات
echo "تشغيل الخدمات للاختبار..."
docker-compose up -d

# الانتظار حتى تكون الخدمات جاهزة
echo "الانتظار حتى تكون الخدمات جاهزة..."
sleep 10

# اختبار الخدمات
echo "اختبار خدمة API..."
if curl -s -f http://localhost:8000/health > /dev/null; then
    echo "✅ خدمة API تعمل بشكل صحيح."
else
    echo "❌ خطأ في خدمة API."
fi

echo "اختبار خدمة معالجة الصور..."
if curl -s -f http://localhost:5000/health > /dev/null; then
    echo "✅ خدمة معالجة الصور تعمل بشكل صحيح."
else
    echo "❌ خطأ في خدمة معالجة الصور."
fi

echo "اختبار خدمة موازنة الحمل..."
if curl -s -f http://localhost/health > /dev/null; then
    echo "✅ خدمة موازنة الحمل تعمل بشكل صحيح."
else
    echo "❌ خطأ في خدمة موازنة الحمل."
fi

# عرض حالة الخدمات
echo "حالة الخدمات:"
docker-compose ps

# إيقاف الخدمات
echo "إيقاف الخدمات..."
docker-compose down

echo "تم اختبار إعداد Docker بنجاح."
