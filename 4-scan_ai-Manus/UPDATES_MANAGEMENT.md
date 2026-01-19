# دليل إدارة التحديثات - Gaara Scan AI v4.3.1

## نظرة عامة

هذا الدليل يوضح كيفية إدارة وتحديث جميع الأدوات والمكتبات في المشروع.

---

## الأدوات الرئيسية

### Backend (Python)

**الملف:** `backend/requirements.txt`

**الأدوات الأساسية:**
- FastAPI: 0.109.0
- Uvicorn: 0.27.0
- SQLAlchemy: 2.0.25
- Alembic: 1.13.1
- PostgreSQL: psycopg2-binary 2.9.9
- Redis: redis 5.0.1

**أدوات الأمان:**
- python-jose: 3.3.0
- passlib: 1.7.4
- pyotp: 2.9.0 (2FA)
- qrcode: 7.4.2 (2FA QR codes)
- bcrypt: 4.1.2
- cryptography: 45.0.4

**أدوات AI/ML:**
- tensorflow: 2.15.0
- torch: 2.1.2
- ultralytics: 8.1.0 (YOLO)
- opencv-python: 4.9.0.80
- pillow: 10.2.0

**التحديث:**
```bash
cd backend
pip install --upgrade -r requirements.txt
pip list --outdated
```

---

### Frontend (Node.js)

**الملف:** `frontend/package.json`

**الأدوات الأساسية:**
- React: 18.2.0
- Vite: 5.0.8
- React Router: 6.21.1
- Axios: 1.6.5
- TailwindCSS: 3.4.1

**مكتبات UI:**
- @radix-ui/*: مكونات UI متقدمة
- @heroicons/react: أيقونات
- chart.js: رسوم بيانية
- leaflet: خرائط

**أدوات التطوير:**
- @testing-library/react: 14.3.1
- vitest: 1.1.3
- eslint: 8.56.0
- prettier: 3.1.1

**التحديث:**
```bash
cd frontend
npm outdated
npm update
npm audit fix
```

---

### ML Service (Python)

**الملف:** `ml_service/requirements.txt`

**الأدوات الأساسية:**
- FastAPI: 0.109.0
- tensorflow: 2.15.0
- torch: 2.1.2
- ultralytics: 8.1.0
- opencv-python-headless: 4.9.0.80

**التحديث:**
```bash
cd ml_service
pip install --upgrade -r requirements.txt
```

---

### Image Crawler (Python)

**الملف:** `image_crawler/requirements.txt`

**الأدوات الأساسية:**
- FastAPI: 0.109.0
- httpx: 0.26.0
- beautifulsoup4: 4.12.3
- selenium: 4.17.2
- playwright: 1.41.0
- openai: 1.10.0
- psycopg2-binary: 2.9.9

**التحديث:**
```bash
cd image_crawler
pip install --upgrade -r requirements.txt
```

---

## جدول التحديثات الموصى به

### تحديثات أمنية (فورية)
- عند اكتشاف ثغرات أمنية
- تشغيل: `npm audit` و `pip-audit`

### تحديثات صغيرة (شهرية)
- Patch updates (x.x.X)
- تحديثات الأمان
- إصلاحات الأخطاء

### تحديثات متوسطة (ربع سنوية)
- Minor updates (x.X.x)
- ميزات جديدة
- تحسينات الأداء

### تحديثات كبيرة (سنوية)
- Major updates (X.x.x)
- تغييرات جذرية
- تتطلب اختبار شامل

---

## أوامر التحديث السريع

### فحص التحديثات المتاحة

**Backend:**
```bash
cd backend
pip list --outdated
```

**Frontend:**
```bash
cd frontend
npm outdated
```

**جميع الخدمات:**
```bash
# Backend
cd backend && pip list --outdated

# Frontend
cd frontend && npm outdated

# ML Service
cd ml_service && pip list --outdated

# Image Crawler
cd image_crawler && pip list --outdated
```

---

### تحديث الأدوات

**Backend (تحديث آمن):**
```bash
cd backend
pip install --upgrade pip
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

**Frontend (تحديث آمن):**
```bash
cd frontend
npm update
npm audit fix
npm outdated
```

**تحديث شامل (حذر!):**
```bash
# Frontend
cd frontend
npm update --save
npm install

# Backend
cd backend
pip install --upgrade -r requirements.txt
```

---

## فحص الثغرات الأمنية

### Backend (Python)

```bash
cd backend
pip install pip-audit
pip-audit

# أو استخدام safety
pip install safety
safety check
```

### Frontend (Node.js)

```bash
cd frontend
npm audit
npm audit fix

# للإصلاح القوي
npm audit fix --force
```

---

## الاختبار بعد التحديث

### 1. اختبار Backend

```bash
cd backend
source venv/bin/activate
pytest tests/
python -m pytest --cov=src tests/
```

### 2. اختبار Frontend

```bash
cd frontend
npm test
npm run test:coverage
```

### 3. اختبار التكامل

```bash
# تشغيل جميع الخدمات
docker-compose up -d

# فحص الصحة
curl http://localhost:1005/api/v1/health
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:1505/health
```

---

## التوافق بين الإصدارات

### Python

- **الإصدار الحالي:** 3.11.0
- **الحد الأدنى:** 3.10
- **الموصى به:** 3.11+

### Node.js

- **الإصدار الحالي:** 22.13.0
- **الحد الأدنى:** 18.0.0
- **الموصى به:** 20.0.0+

### PostgreSQL

- **الإصدار الحالي:** 16-alpine
- **الحد الأدنى:** 14
- **الموصى به:** 16+

### Redis

- **الإصدار الحالي:** 7-alpine
- **الحد الأدنى:** 6
- **الموصى به:** 7+

---

## نصائح مهمة

### قبل التحديث

1. ✅ إنشاء نسخة احتياطية
2. ✅ قراءة CHANGELOG للأدوات
3. ✅ فحص التوافق
4. ✅ الاختبار في بيئة تطوير

### أثناء التحديث

1. ✅ تحديث أداة واحدة في كل مرة
2. ✅ الاختبار بعد كل تحديث
3. ✅ توثيق التغييرات
4. ✅ commit بعد كل تحديث ناجح

### بعد التحديث

1. ✅ تشغيل جميع الاختبارات
2. ✅ فحص الأداء
3. ✅ مراقبة السجلات
4. ✅ تحديث التوثيق

---

## أدوات مساعدة

### Dependabot (GitHub)

تفعيل Dependabot للتحديثات التلقائية:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
```

### Renovate Bot

بديل لـ Dependabot مع ميزات أكثر.

### npm-check-updates

```bash
npm install -g npm-check-updates
ncu -u
npm install
```

---

## سجل التحديثات

| التاريخ | الأداة | من | إلى | الملاحظات |
|---------|--------|-----|-----|-----------|
| 2025-12-14 | FastAPI | 0.108.0 | 0.109.0 | تحديث أمني |
| 2025-12-14 | React | 18.2.0 | 18.2.0 | مستقر |
| 2025-12-14 | YOLO | - | 8.1.0 | إضافة جديدة |
| 2025-12-14 | pyotp | - | 2.9.0 | 2FA support |

---

## الدعم والمساعدة

للحصول على المساعدة في التحديثات:
- GitHub Issues: https://github.com/hamfarid/gaara-Scan-system/issues
- التوثيق: راجع README.md
- السجلات: راجع logs/ في كل خدمة

---

**آخر تحديث:** 14 ديسمبر 2025  
**الإصدار:** v4.3.1
