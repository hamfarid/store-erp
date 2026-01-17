# دليل البدء السريع - Quick Start Guide

**Store Management System v1.5**

---

## 🚀 البدء السريع (5 دقائق)

### المتطلبات الأساسية:
- ✅ Node.js 18+ 
- ✅ Python 3.9+
- ✅ PostgreSQL (اختياري - SQLite يعمل افتراضياً)
- ✅ Redis (اختياري - للكاش)

---

## 📦 التثبيت

### 1. استنساخ المشروع:
```bash
git clone <repository-url>
cd Store
```

### 2. إعداد Backend:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 3. إعداد Frontend:
```bash
cd frontend
npm install
```

### 4. إعداد متغيرات البيئة:
```bash
# من المجلد الرئيسي
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# عدّل ملف .env حسب احتياجاتك
```

---

## ▶️ التشغيل

### الطريقة السريعة (بدء جميع الخدمات):
```powershell
# Windows PowerShell
.\scripts\start-all.ps1
```

### الطريقة اليدوية:

#### 1. Backend:
```bash
cd backend
python main.py
# أو
python -m flask run --port=5506
```

#### 2. Frontend (في نافذة منفصلة):
```bash
cd frontend
npm run dev
```

---

## ✅ التحقق من الحالة

### فحص حالة الخدمات:
```powershell
.\scripts\check-services.ps1
```

### فحص منفذ معين:
```powershell
.\scripts\port-manager.ps1 -Port 5505
```

---

## 🌐 الوصول للتطبيق

- **Frontend:** http://localhost:5505
- **Backend API:** http://localhost:5506
- **API Docs:** http://localhost:5506/api/docs

---

## 🔧 حل المشاكل الشائعة

### مشكلة: EADDRINUSE (المنفذ مستخدم)
```powershell
# ابحث عن العملية
.\scripts\port-manager.ps1 -Port 5505

# أوقف العملية
.\scripts\port-manager.ps1 -Port 5505 -Kill
```

### مشكلة: قاعدة البيانات
```bash
cd backend
python init_db.py
```

### مشكلة: التبعيات
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## 📚 الملفات المهمة

- **إعدادات المنافذ:** `config/ports.json`
- **متغيرات البيئة:** `.env` (أنشئه من `.env.example`)
- **إدارة المنافذ:** `scripts/port-manager.ps1`
- **فحص الخدمات:** `scripts/check-services.ps1`
- **بدء الخدمات:** `scripts/start-all.ps1`

---

## 🧪 الاختبارات

### اختبارات E2E:
```bash
cd frontend
npm run test:e2e
npm run test:e2e:report
```

### تنسيق الكود:
```bash
# Backend
cd backend
python -m black src/
python -m flake8 src/

# Frontend
cd frontend
npm run lint
```

---

## 📖 التوثيق الكامل

- **تقرير الإكمال:** `docs/PROJECT_COMPLETION_REPORT.md`
- **إدارة المنافذ:** `docs/PORT_MANAGEMENT.md`
- **تنسيق الكود:** `backend/docs/CODE_FORMATTING_REPORT.md`
- **اختبارات E2E:** `frontend/docs/E2E_TEST_SUMMARY.md`

---

## 🎯 الخطوات التالية

1. ✅ تأكد من أن جميع الخدمات تعمل
2. ✅ افتح http://localhost:5505
3. ✅ سجّل الدخول (أنشئ مستخدم admin أولاً)
4. ✅ ابدأ استخدام التطبيق!

---

## 💡 نصائح

- استخدم `.\scripts\check-services.ps1` للتحقق من حالة الخدمات
- استخدم `.\scripts\port-manager.ps1` لحل مشاكل المنافذ
- راجع `docs/PORT_MANAGEMENT.md` لمزيد من المعلومات

---

**جاهز للبدء! 🚀**
