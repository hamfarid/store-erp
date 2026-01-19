@echo off
REM سكريبت تشغيل النظام الزراعي الذكي - Windows
REM يقوم بتشغيل النظام بشكل مرحلي

echo ========================================
echo   النظام الزراعي الذكي - التشغيل المرحلي
echo ========================================
echo.

REM التحقق من وجود Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [خطأ] Docker غير مثبت أو غير متاح
    echo يرجى تثبيت Docker Desktop أولاً
    pause
    exit /b 1
)

REM التحقق من وجود docker-compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [خطأ] Docker Compose غير متاح
    echo يرجى تثبيت Docker Compose أولاً
    pause
    exit /b 1
)

echo [معلومات] Docker متاح ويعمل بشكل صحيح
echo.

REM إنشاء الشبكة إذا لم تكن موجودة
echo [معلومات] إنشاء شبكة Docker...
docker network create agri_ai_network 2>nul
echo [نجاح] تم إنشاء الشبكة أو هي موجودة بالفعل
echo.

REM التحقق من وجود ملف .env
if not exist ".env" (
    echo [تحذير] ملف .env غير موجود
    if exist ".env.template" (
        echo [معلومات] نسخ ملف .env من القالب...
        copy ".env.template" ".env" >nul
        echo [تحذير] يرجى تعديل كلمات المرور في ملف .env قبل المتابعة
        echo اضغط أي مفتاح للمتابعة بعد تعديل الملف...
        pause >nul
    ) else (
        echo [خطأ] ملف .env.template غير موجود
        pause
        exit /b 1
    )
)

echo ========================================
echo   بدء تشغيل المراحل
echo ========================================
echo.

REM المرحلة 1: قواعد البيانات
echo [المرحلة 1] تشغيل قواعد البيانات والخدمات الأساسية...
docker-compose -f docker-compose.stage1-databases.yml up -d
if errorlevel 1 (
    echo [خطأ] فشل في تشغيل المرحلة 1
    pause
    exit /b 1
)
echo [نجاح] تم تشغيل المرحلة 1
echo.

REM انتظار قواعد البيانات
echo [معلومات] انتظار تشغيل قواعد البيانات...
timeout /t 30 /nobreak >nul
echo.

REM المرحلة 2: التطبيق الأساسي
echo [المرحلة 2] تشغيل التطبيق الأساسي...
docker-compose -f docker-compose.stage2-core-app.yml up -d
if errorlevel 1 (
    echo [خطأ] فشل في تشغيل المرحلة 2
    pause
    exit /b 1
)
echo [نجاح] تم تشغيل المرحلة 2
echo.

REM انتظار التطبيق الأساسي
echo [معلومات] انتظار تشغيل التطبيق الأساسي...
timeout /t 20 /nobreak >nul
echo.

REM سؤال المستخدم عن تشغيل المراحل الإضافية
echo هل تريد تشغيل خدمات الذكاء الاصطناعي؟ (y/n)
set /p ai_choice=
if /i "%ai_choice%"=="y" (
    echo [المرحلة 3] تشغيل خدمات الذكاء الاصطناعي...
    docker-compose -f docker-compose.stage3-ai-services.yml up -d
    if errorlevel 1 (
        echo [تحذير] فشل في تشغيل بعض خدمات الذكاء الاصطناعي
    ) else (
        echo [نجاح] تم تشغيل المرحلة 3
    )
    echo.
)

echo هل تريد تشغيل خدمات المراقبة؟ (y/n)
set /p monitor_choice=
if /i "%monitor_choice%"=="y" (
    echo [المرحلة 4] تشغيل خدمات المراقبة...
    docker-compose -f docker-compose.stage4-monitoring.yml up -d
    if errorlevel 1 (
        echo [تحذير] فشل في تشغيل بعض خدمات المراقبة
    ) else (
        echo [نجاح] تم تشغيل المرحلة 4
    )
    echo.
)

echo ========================================
echo   تم تشغيل النظام بنجاح!
echo ========================================
echo.
echo يمكنك الوصول إلى:
echo - التطبيق الرئيسي: http://localhost:8031
echo - إدارة RabbitMQ: http://localhost:15672
if /i "%monitor_choice%"=="y" (
    echo - Grafana: http://localhost:3000
    echo - Prometheus: http://localhost:9090
)
echo.

REM عرض حالة الحاويات
echo حالة الحاويات:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo اضغط أي مفتاح للخروج...
pause >nul
