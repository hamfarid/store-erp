@echo off
REM 🚀 سكريبت تشغيل نظام إدارة المتجر - Windows
REM Store Management System Quick Launcher for Windows

title نظام إدارة المتجر v1.5

echo ================================================================================================
echo                           🚀 نظام إدارة المتجر v1.5 🚀
echo ================================================================================================
echo.

REM فحص Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت. يرجى تثبيت Python من https://python.org
    pause
    exit /b 1
)

REM فحص Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js غير مثبت. يرجى تثبيت Node.js من https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Python و Node.js مثبتان
echo.

REM إنشاء البيئة الافتراضية
echo 📋 إعداد البيئة الافتراضية...
cd backend
if not exist "venv" (
    python -m venv venv
    echo ✅ تم إنشاء البيئة الافتراضية
) else (
    echo ℹ️ البيئة الافتراضية موجودة مسبقاً
)

REM تفعيل البيئة الافتراضية
call venv\Scripts\activate.bat

REM تثبيت المتطلبات
echo 📋 تثبيت متطلبات Python...
pip install --upgrade pip
pip install -r requirements.txt

REM إعداد قاعدة البيانات
echo 📋 إعداد قاعدة البيانات...
if not exist "instance" mkdir instance
python -c "from src.database import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ قاعدة البيانات جاهزة')"

cd ..

REM تثبيت متطلبات الواجهة الأمامية
echo 📋 تثبيت متطلبات الواجهة الأمامية...
cd frontend
npm install
cd ..

echo.
echo ================================================================================================
echo                           🎉 تم إعداد النظام بنجاح! 🎉
echo ================================================================================================
echo.
echo 🌐 لتشغيل النظام:
echo    1. تشغيل الواجهة الخلفية: cd backend ^&^& venv\Scripts\activate ^&^& python app.py
echo    2. تشغيل الواجهة الأمامية: cd frontend ^&^& npm run dev
echo.
echo 📊 الروابط:
echo    - الواجهة الأمامية: http://localhost:3004
echo    - الواجهة الخلفية: http://localhost:5001
echo    - API الصحة: http://localhost:5001/api/health
echo.
echo 👑 معلومات Admin:
echo    - اسم المستخدم: admin
echo    - كلمة المرور: موجودة في admin_credentials.json
echo.
pause
