@echo off
REM ملف: /home/ubuntu/gaara_development/scripts/start.bat
REM سكريبت تشغيل نظام Gaara AI لنظام Windows

setlocal enabledelayedexpansion

echo ============================================================
echo 🌱 بدء تشغيل نظام Gaara AI
echo ============================================================

REM فحص Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker غير مثبت. يرجى تثبيت Docker Desktop أولاً.
    pause
    exit /b 1
)
echo ✅ Docker مثبت

REM فحص Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose غير مثبت. يرجى تثبيت Docker Compose أولاً.
    pause
    exit /b 1
)
echo ✅ Docker Compose مثبت

REM فحص وجود docker-compose.yml
if not exist docker-compose.yml (
    echo ❌ ملف docker-compose.yml غير موجود
    pause
    exit /b 1
)

echo ============================================================
echo 🔧 إعداد البيئة
echo ============================================================

REM إنشاء ملف .env إذا لم يكن موجوداً
if not exist .env (
    echo ℹ️  إنشاء ملف .env من النموذج...
    copy .env.example .env
    echo ✅ تم إنشاء ملف .env
    echo ⚠️  يرجى تعديل ملف .env حسب بيئتك
) else (
    echo ✅ ملف .env موجود
)

REM إنشاء المجلدات المطلوبة
echo ℹ️  إنشاء المجلدات المطلوبة...
if not exist uploads mkdir uploads
if not exist logs mkdir logs
if not exist backups mkdir backups
if not exist models mkdir models
if not exist models\tensorflow mkdir models\tensorflow
if not exist models\opencv mkdir models\opencv
echo ✅ تم إنشاء المجلدات

echo ============================================================
echo 🏗️  بناء صور Docker
echo ============================================================

echo ℹ️  بناء صورة الواجهة الخلفية...
docker-compose build backend
if errorlevel 1 (
    echo ❌ فشل في بناء صورة الواجهة الخلفية
    pause
    exit /b 1
)
echo ✅ تم بناء صورة الواجهة الخلفية

echo ℹ️  بناء صورة الواجهة الأمامية...
docker-compose build frontend
if errorlevel 1 (
    echo ❌ فشل في بناء صورة الواجهة الأمامية
    pause
    exit /b 1
)
echo ✅ تم بناء صورة الواجهة الأمامية

echo ============================================================
echo 🚀 تشغيل النظام
echo ============================================================

echo ℹ️  تشغيل الخدمات الأساسية...
docker-compose up -d database redis
if errorlevel 1 (
    echo ❌ فشل في تشغيل الخدمات الأساسية
    pause
    exit /b 1
)

echo ℹ️  انتظار جاهزية قاعدة البيانات...
timeout /t 10 /nobreak >nul

echo ℹ️  تشغيل الواجهة الخلفية...
docker-compose up -d backend celery_worker celery_beat
if errorlevel 1 (
    echo ❌ فشل في تشغيل الواجهة الخلفية
    pause
    exit /b 1
)

echo ℹ️  انتظار جاهزية الواجهة الخلفية...
timeout /t 15 /nobreak >nul

echo ℹ️  تشغيل الواجهة الأمامية...
docker-compose up -d frontend
if errorlevel 1 (
    echo ❌ فشل في تشغيل الواجهة الأمامية
    pause
    exit /b 1
)

echo ✅ تم تشغيل جميع الخدمات

echo ============================================================
echo 📊 فحص حالة النظام
echo ============================================================

timeout /t 10 /nobreak >nul

REM فحص الواجهة الخلفية
curl -f http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  الواجهة الخلفية قد تحتاج وقت إضافي للتشغيل
) else (
    echo ✅ الواجهة الخلفية تعمل بشكل صحيح
)

REM فحص الواجهة الأمامية
curl -f http://localhost:80/ >nul 2>&1
if errorlevel 1 (
    echo ⚠️  الواجهة الأمامية قد تحتاج وقت إضافي للتشغيل
) else (
    echo ✅ الواجهة الأمامية تعمل بشكل صحيح
)

echo ============================================================
echo 🎉 نظام Gaara AI جاهز!
echo ============================================================

echo.
echo 📱 الواجهة الأمامية: http://localhost
echo 🔧 الواجهة الخلفية: http://localhost:5000
echo 📊 API التوثيق: http://localhost:5000/api/docs
echo 💾 قاعدة البيانات: localhost:5432
echo 🔴 Redis: localhost:6379
echo.
echo 📋 أوامر مفيدة:
echo   • عرض السجلات: docker-compose logs -f
echo   • إيقاف النظام: docker-compose down
echo   • إعادة التشغيل: docker-compose restart
echo   • فحص الحالة: docker-compose ps
echo.
echo 🚀 النظام جاهز للاستخدام!
echo.

pause

