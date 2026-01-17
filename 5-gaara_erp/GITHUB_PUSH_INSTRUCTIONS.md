# 🚀 دليل رفع الملفات إلى GitHub

## الطريقة السريعة (Windows)

### الطريقة 1: استخدام السكريبت

```cmd
scripts\push-to-github.bat
```

هذا السكريبت سيقوم بـ:
1. التحقق من تثبيت Git
2. تهيئة المستودع (إن لم يكن موجوداً)
3. إضافة جميع الملفات
4. إنشاء commit
5. رفع الملفات إلى GitHub

### الطريقة 2: استخدام PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File scripts\git-push.ps1
```

## الطريقة اليدوية

### 1. تهيئة Git (إن لم يكن موجوداً)

```bash
git init
```

### 2. إضافة Remote Repository

```bash
git remote add origin https://github.com/yourusername/gaara-erp.git
```

أو باستخدام SSH:
```bash
git remote add origin git@github.com:yourusername/gaara-erp.git
```

### 3. إضافة الملفات

```bash
git add .
```

### 4. إنشاء Commit

```bash
git commit -m "feat: Add comprehensive backend infrastructure, Docker setup, API documentation, and configuration modules"
```

### 5. رفع إلى GitHub

```bash
git push -u origin main
```

أو إذا كان الفرع اسمه `master`:
```bash
git push -u origin master
```

## 📝 رسائل Commit المقترحة

```bash
# للملفات الجديدة
git commit -m "feat: Add comprehensive backend infrastructure and Docker configuration"

# للتحديثات
git commit -m "chore: Update Docker configurations and documentation"

# للإصلاحات
git commit -m "fix: Correct frontend port configuration and CORS settings"

# للوثائق
git commit -m "docs: Add API documentation and configuration guides"
```

## ✅ الملفات التي سيتم رفعها

- ✅ جميع ملفات Docker (Dockerfile, docker-compose.yml)
- ✅ ملفات الإعدادات (config/)
- ✅ السكريبتات (scripts/)
- ✅ الوثائق (*.md)
- ✅ ملفات CI/CD (.github/workflows/)
- ✅ ملفات المراقبة (monitoring/)
- ✅ ملفات Frontend (gaara-erp-frontend/)

## ❌ الملفات التي لن يتم رفعها (في .gitignore)

- ❌ ملفات .env (استخدم .env.example)
- ❌ node_modules/
- ❌ __pycache__/
- ❌ ملفات .log
- ❌ قاعدة البيانات
- ❌ الملفات المؤقتة

## 🔍 التحقق من الحالة

```bash
# عرض الحالة
git status

# عرض الملفات المعدلة
git status --short

# عرض الـ remote
git remote -v
```

## 🆘 حل المشاكل

### المشكلة: "remote origin already exists"

```bash
# تحديث الـ remote
git remote set-url origin https://github.com/yourusername/gaara-erp.git
```

### المشكلة: "Push rejected"

```bash
# سحب التغييرات أولاً
git pull origin main --rebase

# ثم الرفع
git push origin main
```

### المشكلة: "Branch not found"

```bash
# إنشاء فرع جديد
git checkout -b main

# أو استخدام master
git checkout -b master
```

## 📚 المزيد من المعلومات

راجع ملف `GIT_GUIDE.md` للحصول على دليل شامل لاستخدام Git.

---

**ملاحظة**: تأكد من أن لديك حساب GitHub وأن المستودع موجود قبل الرفع.
