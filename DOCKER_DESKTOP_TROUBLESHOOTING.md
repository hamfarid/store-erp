# حل مشكلة Docker Desktop - 500 Internal Server Error
**التاريخ:** 2026-01-23  
**المشكلة:** `request returned 500 Internal Server Error for API route and version`

## 🔍 المشكلة

```
request returned 500 Internal Server Error for API route and version 
http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping
```

هذا الخطأ يعني أن Docker Desktop غير قيد التشغيل أو لا يستجيب.

## ✅ الحلول

### الحل 1: التحقق من Docker Desktop

1. **افتح Docker Desktop**
   - ابحث عن "Docker Desktop" في قائمة Start
   - تأكد من أن Docker Desktop قيد التشغيل
   - انتظر حتى يظهر "Docker Desktop is running" في شريط المهام

2. **تحقق من الحالة**
   ```powershell
   # في PowerShell
   docker ps
   ```

### الحل 2: إعادة تشغيل Docker Desktop

1. **أغلق Docker Desktop**
   - انقر بزر الماوس الأيمن على أيقونة Docker في شريط المهام
   - اختر "Quit Docker Desktop"

2. **انتظر 10 ثوانٍ**

3. **افتح Docker Desktop مرة أخرى**
   - ابحث عن "Docker Desktop" وافتحه
   - انتظر حتى يبدأ بالكامل (عادة 30-60 ثانية)

4. **تحقق من الحالة**
   ```powershell
   docker ps
   ```

### الحل 3: إعادة تشغيل Docker Service

```powershell
# في PowerShell (كمسؤول)
Restart-Service docker
```

أو:

```powershell
# إعادة تشغيل Docker Desktop
Stop-Process -Name "Docker Desktop" -Force
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### الحل 4: إعادة تشغيل WSL (إذا كنت تستخدم WSL 2)

```powershell
# في PowerShell (كمسؤول)
wsl --shutdown
# ثم افتح Docker Desktop مرة أخرى
```

### الحل 5: التحقق من إعدادات Docker Desktop

1. **افتح Docker Desktop**
2. **Settings → General**
   - تأكد من تفعيل "Use the WSL 2 based engine" (إذا كنت تستخدم WSL 2)
   - تأكد من تفعيل "Start Docker Desktop when you log in"

3. **Settings → Resources**
   - تأكد من تخصيص موارد كافية (RAM, CPU)

## 🔧 بعد إصلاح المشكلة

### 1. تحقق من Docker
```powershell
docker ps
docker version
```

### 2. بناء الحاوية
```powershell
cd D:\Ai_Project\4-scan_ai-Manus
docker-compose build ml_service
```

### 3. تشغيل الحاوية
```powershell
docker-compose up -d ml_service
```

### 4. التحقق من الحالة
```powershell
docker-compose ps ml_service
docker logs scan_ai-Manus-ml
```

## 📝 ملاحظات

- إذا استمرت المشكلة، جرب إعادة تشغيل الكمبيوتر
- تأكد من أن Windows Update محدث
- تأكد من أن Docker Desktop محدث إلى آخر إصدار

## ✅ التحقق النهائي

بعد إصلاح المشكلة، يجب أن ترى:

```powershell
PS D:\Ai_Project\4-scan_ai-Manus> docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED       STATUS          PORTS                    NAMES
...
```

بدون أي أخطاء 500.

---
**Last Updated:** 2026-01-23
