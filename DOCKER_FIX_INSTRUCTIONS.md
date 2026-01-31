# إصلاح مشكلة Docker Desktop - تعليمات سريعة
**التاريخ:** 2026-01-23

## 🔴 المشكلة الحالية

```
request returned 500 Internal Server Error for API route and version 
http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping
```

**السبب:** Docker Desktop غير قيد التشغيل

## ✅ الحل السريع (3 خطوات)

### الخطوة 1: افتح Docker Desktop
1. اضغط `Windows Key` واكتب "Docker Desktop"
2. انقر على "Docker Desktop" لفتحه
3. انتظر حتى يظهر "Docker Desktop is running" في شريط المهام (أسفل يمين الشاشة)

### الخطوة 2: تحقق من الحالة
افتح PowerShell واكتب:
```powershell
docker ps
```

إذا ظهرت قائمة بالحاويات (حتى لو كانت فارغة)، فالمشكلة حُلت ✅

### الخطوة 3: بناء الحاوية
```powershell
cd D:\Ai_Project\4-scan_ai-Manus
docker-compose build ml_service
docker-compose up -d ml_service
```

## 🔧 إذا لم يعمل Docker Desktop

### الحل 1: إعادة تشغيل Docker Desktop
1. انقر بزر الماوس الأيمن على أيقونة Docker في شريط المهام
2. اختر "Quit Docker Desktop"
3. انتظر 10 ثوانٍ
4. افتح Docker Desktop مرة أخرى

### الحل 2: استخدام السكريبت التلقائي
```powershell
# في PowerShell
cd D:\Ai_Project
.\QUICK_DOCKER_FIX.ps1
```

### الحل 3: إعادة تشغيل الكمبيوتر
إذا لم تعمل الحلول السابقة، أعد تشغيل الكمبيوتر ثم:
1. افتح Docker Desktop
2. انتظر حتى يبدأ بالكامل
3. جرب `docker ps` مرة أخرى

## 📝 بعد إصلاح المشكلة

بعد أن يعمل Docker Desktop، قم بتنفيذ:

```powershell
# الانتقال إلى مجلد المشروع
cd D:\Ai_Project\4-scan_ai-Manus

# بناء الحاوية
docker-compose build ml_service

# تشغيل الحاوية
docker-compose up -d ml_service

# التحقق من الحالة
docker-compose ps ml_service

# عرض السجلات
docker logs scan_ai-Manus-ml
```

## ✅ التحقق من نجاح العملية

بعد بناء وتشغيل الحاوية، يجب أن ترى:

```powershell
PS D:\Ai_Project\4-scan_ai-Manus> docker-compose ps ml_service
NAME               IMAGE                    COMMAND           SERVICE      CREATED      STATUS                  PORTS
scan_ai-Manus-ml   gaara-ml-service:4.3.1  "uvicorn main:…" ml_service   X seconds ago   Up X seconds (healthy)   0.0.0.0:4101->4101/tcp
```

## 🆘 إذا استمرت المشكلة

1. **تأكد من تحديث Docker Desktop**
   - افتح Docker Desktop
   - Settings → Software Updates
   - تحقق من وجود تحديثات

2. **تحقق من WSL 2** (إذا كنت تستخدمه)
   ```powershell
   wsl --status
   ```

3. **أعد تثبيت Docker Desktop** (كحل أخير)
   - Uninstall Docker Desktop
   - أعد تثبيته من الموقع الرسمي
   - أعد تشغيل الكمبيوتر

---
**Last Updated:** 2026-01-23
