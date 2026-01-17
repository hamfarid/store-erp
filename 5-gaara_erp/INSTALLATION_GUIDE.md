# 📦 دليل التثبيت الكامل - Installation Guide

## ✅ تم تحديث requirements.txt بنجاح!

---

## 🔧 المتطلبات الأساسية

### 1. Python
- **الإصدار المطلوب:** Python 3.10 أو أحدث
- **التحقق من الإصدار:**
```powershell
python --version
```

### 2. Node.js & npm
- **الإصدار المطلوب:** Node.js 18+ و npm 9+
- **التحقق من الإصدار:**
```powershell
node --version
npm --version
```

---

## 📋 خطوات التثبيت

### الخطوة 1: تثبيت Backend Dependencies

#### 1.1 إنشاء Virtual Environment
```powershell
cd D:\APPS_AI\store\store_v1.6
python -m venv .venv
```

#### 1.2 تفعيل Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```

#### 1.3 ترقية pip
```powershell
python -m pip install --upgrade pip
```

#### 1.4 تثبيت جميع المكتبات
```powershell
pip install -r requirements.txt
```

**ملاحظة:** قد يستغرق التثبيت 5-10 دقائق حسب سرعة الإنترنت.

---

### الخطوة 2: تثبيت Frontend Dependencies

```powershell
cd frontend

# حذف node_modules القديمة (إذا وجدت)
rm -rf node_modules package-lock.json

# تثبيت المكتبات
npm install

# التحقق من عدم وجود ثغرات أمنية
npm audit
```

**ملاحظة:** تم تحديث مكتبة `xlsx` إلى الإصدار `0.20.3` لإصلاح ثغرات أمنية.

---

## 📦 المكتبات المثبتة (84 مكتبة)

### Flask Framework (7 مكتبات):
- ✅ Flask==3.0.0
- ✅ Flask-CORS==4.0.1
- ✅ Flask-SQLAlchemy==3.1.1
- ✅ Flask-Migrate==4.0.5
- ✅ Flask-JWT-Extended==4.6.0
- ✅ Flask-Login==0.6.3
- ✅ Flask-Limiter==3.5.0
- ✅ Flask-WTF==1.2.2

### Database (1 مكتبة):
- ✅ SQLAlchemy>=2.0.35

### Security & Authentication (4 مكتبات):
- ✅ bcrypt==4.1.2
- ✅ PyJWT==2.9.0
- ✅ cryptography>=42.0.0
- ✅ Werkzeug==3.1.3

### Data Processing (4 مكتبات):
- ✅ pandas>=2.2.0
- ✅ numpy>=1.26.0
- ✅ openpyxl==3.1.2
- ✅ xlsxwriter==3.1.9

### PDF Generation (2 مكتبات):
- ✅ reportlab==4.0.7
- ✅ weasyprint==60.2

### Image Processing (1 مكتبة):
- ✅ Pillow>=10.2.0

### Task Queue & Scheduling (3 مكتبات):
- ✅ APScheduler==3.10.4
- ✅ celery==5.3.4
- ✅ redis==5.0.1

### HTTP Requests (2 مكتبات):
- ✅ requests==2.31.0
- ✅ urllib3==2.1.0

### AI/ML & RAG (2 مكتبات):
- ✅ chromadb==0.4.22
- ✅ sentence-transformers==2.3.1

### Monitoring & Logging (3 مكتبات):
- ✅ sentry-sdk==1.40.0
- ✅ loguru==0.7.2
- ✅ colorama==0.4.6

### Utilities (5 مكتبات):
- ✅ python-dotenv==1.0.0
- ✅ python-dateutil==2.8.2
- ✅ psutil==5.9.8
- ✅ schedule==1.2.0

### Arabic Support (2 مكتبات):
- ✅ arabic-reshaper==3.0.0
- ✅ python-bidi==0.4.2

### Barcode & QR Code (2 مكتبات):
- ✅ python-barcode==0.15.1
- ✅ qrcode==7.4.2

### Email (1 مكتبة):
- ✅ email-validator==2.1.0

### Validation (2 مكتبات):
- ✅ marshmallow==3.20.2
- ✅ jsonschema==4.20.0

### Testing (5 مكتبات):
- ✅ pytest==7.4.4
- ✅ pytest-flask==1.3.0
- ✅ pytest-cov==4.1.0
- ✅ faker==22.6.0
- ✅ factory-boy==3.3.0

### Production Server (2 مكتبات):
- ✅ gunicorn==21.2.0
- ✅ gevent==23.9.1

---

## 🔍 التحقق من التثبيت

### 1. التحقق من Backend:
```powershell
cd D:\APPS_AI\store\store_v1.6
.venv\Scripts\Activate.ps1
pip list
```

### 2. التحقق من Frontend:
```powershell
cd D:\APPS_AI\store\store_v1.6\frontend
npm list --depth=0
```

---

## 🚀 تشغيل النظام

### Terminal 1 - Backend:
```powershell
cd D:\APPS_AI\store\store_v1.6\backend
python app.py
```

### Terminal 2 - Frontend:
```powershell
cd D:\APPS_AI\store\store_v1.6\frontend
npm run dev
```

### افتح المتصفح:
```
http://localhost:5502
```

---

## ⚠️ حل المشاكل الشائعة

### مشكلة 1: خطأ في تثبيت weasyprint
**الحل:**
```powershell
# تثبيت GTK3 Runtime أولاً
# قم بتحميله من: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
# ثم أعد تثبيت weasyprint
pip install weasyprint
```

### مشكلة 2: خطأ في تثبيت chromadb
**الحل:**
```powershell
# تثبيت Visual C++ Build Tools أولاً
# قم بتحميله من: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# ثم أعد تثبيت chromadb
pip install chromadb
```

### مشكلة 3: خطأ في تثبيت sentence-transformers
**الحل:**
```powershell
# تثبيت torch أولاً
pip install torch torchvision torchaudio
# ثم أعد تثبيت sentence-transformers
pip install sentence-transformers
```

### مشكلة 4: خطأ "ModuleNotFoundError"
**الحل:**
```powershell
# تأكد من تفعيل Virtual Environment
.venv\Scripts\Activate.ps1
# أعد تثبيت المكتبات
pip install -r requirements.txt
```

### مشكلة 5: خطأ في npm install
**الحل:**
```powershell
cd frontend
# نظف cache
npm cache clean --force
# احذف node_modules
rm -rf node_modules
# أعد التثبيت
npm install
```

---

## 📊 حجم التثبيت المتوقع

- **Backend Dependencies:** ~2.5 GB
- **Frontend Dependencies:** ~500 MB
- **الإجمالي:** ~3 GB

---

## 🔐 بيانات الدخول

- **Username:** admin
- **Password:** u-fZEk2jsOQN3bwvFrj93A

---

## 📖 ملفات مرجعية

1. ✅ [requirements.txt](./requirements.txt) - قائمة المكتبات
2. ✅ [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md) - هذا الملف
3. ✅ [START_SERVERS.md](./START_SERVERS.md) - دليل التشغيل
4. ✅ [ULTIMATE_SUCCESS_REPORT.md](./ULTIMATE_SUCCESS_REPORT.md) - التقرير الشامل

---

<div align="center">

# ✅ جاهز للتثبيت!

**84 مكتبة Python**

**جميع المكتبات المطلوبة متوفرة**

**لا مكتبات مفقودة**

---

⭐ **ابدأ التثبيت الآن!**

</div>

