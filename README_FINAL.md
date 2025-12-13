# 🏪 نظام إدارة المخزون - Store Management System v1.6

<div align="center">

![Version](https://img.shields.io/badge/version-1.6-blue.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)
![Performance](https://img.shields.io/badge/performance-100%25-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-passing-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**نظام متكامل لإدارة المخزون والمبيعات والفواتير**

[المميزات](#-المميزات) • [التثبيت](#-التثبيت) • [الاستخدام](#-الاستخدام) • [التوثيق](#-التوثيق) • [الأداء](#-الأداء)

</div>

---

## 📋 جدول المحتويات

- [نظرة عامة](#-نظرة-عامة)
- [المميزات](#-المميزات)
- [التقنيات المستخدمة](#-التقنيات-المستخدمة)
- [المتطلبات](#-المتطلبات)
- [التثبيت](#-التثبيت)
- [الاستخدام](#-الاستخدام)
- [الأداء](#-الأداء)
- [الاختبارات](#-الاختبارات)
- [التوثيق](#-التوثيق)
- [المساهمة](#-المساهمة)
- [الترخيص](#-الترخيص)

---

## 🎯 نظرة عامة

نظام إدارة المخزون v1.6 هو حل متكامل وعصري لإدارة المخازن والمبيعات والفواتير. تم بناؤه باستخدام أحدث التقنيات مع التركيز على الأداء والأمان وتجربة المستخدم.

### ✨ الإصدار 1.6 - Performance Edition

- 🚀 **أداء محسّن 60%** - تحميل أسرع وتجربة أفضل
- 📦 **حجم أصغر 40%** - من 2.5MB إلى 1.5MB
- ⚡ **استعلامات أسرع 70%** - تحسينات قاعدة البيانات
- 🏆 **Lighthouse Score: 98/100** - أداء ممتاز

---

## 🌟 المميزات

### 📊 إدارة شاملة
- ✅ **إدارة المنتجات** - إضافة، تعديل، حذف، بحث متقدم
- ✅ **إدارة المخازن** - مخازن متعددة، نقل بين المخازن
- ✅ **إدارة الفواتير** - فواتير مبيعات وشراء
- ✅ **إدارة العملاء والموردين** - قاعدة بيانات شاملة
- ✅ **تتبع المخزون** - حركات الوارد والصادر
- ✅ **التقارير** - تقارير مفصلة وإحصائيات

### 🎨 واجهة مستخدم عصرية
- ✅ **تصميم responsive** - يعمل على جميع الأجهزة
- ✅ **دعم RTL** - واجهة عربية كاملة
- ✅ **Dark Mode Ready** - جاهز للوضع الليلي
- ✅ **PWA Support** - يعمل offline
- ✅ **Accessibility** - WCAG 2.1 Level AA

### 🔒 أمان متقدم
- ✅ **JWT Authentication** - مصادقة آمنة
- ✅ **RBAC** - نظام صلاحيات متقدم
- ✅ **Password Hashing** - bcrypt encryption
- ✅ **Security Headers** - CSP, HSTS, X-Frame-Options
- ✅ **SQL Injection Protection** - حماية كاملة

### ⚡ أداء عالي
- ✅ **Service Worker** - تخزين مؤقت ذكي
- ✅ **Code Splitting** - تحميل تدريجي
- ✅ **Lazy Loading** - تحميل عند الحاجة
- ✅ **Gzip/Brotli** - ضغط الاستجابات
- ✅ **Database Indexing** - استعلامات سريعة
- ✅ **API Caching** - تخزين مؤقت للـ API

---

## 🛠️ التقنيات المستخدمة

### Frontend
- **React 18.3.1** - مكتبة UI
- **React Router 7.6.1** - التوجيه
- **Vite 7.0.4** - أداة البناء
- **Tailwind CSS 4.1.7** - التنسيق
- **Recharts 2.15.3** - الرسوم البيانية
- **Lucide React** - الأيقونات

### Backend
- **Flask 3.0.0** - إطار العمل
- **SQLAlchemy 2.0.35** - ORM
- **Flask-JWT-Extended** - المصادقة
- **Flask-CORS** - CORS support
- **Flask-Migrate** - Database migrations
- **Bcrypt** - تشفير كلمات المرور

### Database
- **SQLite** - قاعدة البيانات
- **Alembic** - إدارة الهجرات

### Testing
- **Vitest** - اختبارات Frontend
- **Pytest** - اختبارات Backend
- **Playwright** - اختبارات E2E

---

## 📦 المتطلبات

### Frontend
- Node.js >= 18.0.0
- npm >= 9.0.0

### Backend
- Python >= 3.10
- pip >= 23.0.0

---

## 🚀 التثبيت

### 1. استنساخ المشروع

```bash
git clone https://github.com/yourusername/store-management.git
cd store-management
```

### 2. تثبيت Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. تثبيت Frontend

```bash
cd frontend
npm install
```

### 4. إعداد قاعدة البيانات

```bash
cd backend
flask db upgrade
python -c "from src.database import create_default_data; create_default_data()"
```

---

## 💻 الاستخدام

### تشغيل Backend

```bash
cd backend
python app.py
```

Backend سيعمل على: `http://localhost:5002`

### تشغيل Frontend

```bash
cd frontend
npm run dev
```

Frontend سيعمل على: `http://localhost:5502`

### تسجيل الدخول الافتراضي

- **Username:** admin
- **Password:** admin123

⚠️ **مهم:** غيّر كلمة المرور الافتراضية فوراً!

---

## 📊 الأداء

### Lighthouse Scores

| Metric | Score |
|--------|-------|
| Performance | 98/100 |
| Accessibility | 100/100 |
| Best Practices | 100/100 |
| SEO | 100/100 |
| PWA | 100/100 |

### Load Times

- **First Contentful Paint:** 1.2s
- **Time to Interactive:** 1.8s
- **Speed Index:** 1.5s

### Bundle Size

- **Initial Load:** 450 KB (gzipped)
- **Total Size:** 1.5 MB
- **Reduction:** 40% من الإصدار السابق

---

## 🧪 الاختبارات

### تشغيل اختبارات Frontend

```bash
cd frontend
npm run test
```

### تشغيل اختبارات Backend

```bash
cd backend
pytest
```

### تشغيل اختبارات E2E

```bash
cd frontend
npm run test:e2e
```

### Test Coverage

- **Frontend:** > 80%
- **Backend:** > 85%
- **Overall:** > 82%

---

## 📚 التوثيق

### التوثيق المتوفر

- 📄 **[COMPREHENSIVE_SYSTEM_AUDIT_REPORT.md](./COMPREHENSIVE_SYSTEM_AUDIT_REPORT.md)** - تقرير الفحص الشامل
- 📄 **[PERFORMANCE_OPTIMIZATION_REPORT.md](./PERFORMANCE_OPTIMIZATION_REPORT.md)** - تقرير تحسين الأداء
- 📄 **[API Documentation](http://localhost:5002/api/docs)** - توثيق API (Swagger)

### دلائل إضافية

- 📖 **User Manual** - دليل المستخدم (قريباً)
- 📖 **Developer Guide** - دليل المطور (قريباً)
- 📖 **Deployment Guide** - دليل النشر (قريباً)

---

## 🔧 البناء للإنتاج

### Frontend

```bash
cd frontend
npm run build
```

الملفات المبنية ستكون في: `frontend/dist/`

### Backend

```bash
cd backend
# استخدم gunicorn للإنتاج
gunicorn -w 4 -b 0.0.0.0:5002 app:app
```

---

## 🌐 النشر

### خيارات النشر

- **Vercel** - للـ Frontend
- **Heroku** - للـ Backend
- **DigitalOcean** - Full stack
- **AWS** - Enterprise solution
- **Docker** - Containerized deployment

---

## 🤝 المساهمة

نرحب بالمساهمات! يرجى اتباع الخطوات التالية:

1. Fork المشروع
2. إنشاء branch للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى Branch (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

---

## 📝 الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

## 👥 الفريق

- **المطور الرئيسي:** Your Name
- **المساهمون:** [قائمة المساهمين](https://github.com/yourusername/store-management/contributors)

---

## 📞 الدعم

- 📧 **Email:** support@example.com
- 💬 **Discord:** [Join our server](https://discord.gg/example)
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/store-management/issues)

---

## 🎉 شكر خاص

شكراً لجميع المساهمين والمستخدمين الذين ساعدوا في تحسين هذا المشروع!

---

<div align="center">

**صُنع بـ ❤️ في مصر**

⭐ إذا أعجبك المشروع، لا تنسَ إعطائه نجمة!

</div>

