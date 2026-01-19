# /home/ubuntu/image_search_integration/auto_learning/README.md
# مديول البحث الذاتي الذكي (Auto Learning Module)

## نظرة عامة

مديول البحث الذاتي الذكي هو جزء من نظام Gaara ERP يهدف إلى تحسين عمليات البحث عن الصور وتعلم النظام ذاتياً من خلال إدارة الكلمات المفتاحية والمصادر الموثوقة ومحركات البحث. يوفر المديول واجهات إدارة متقدمة للمستخدمين مع نظام صلاحيات متكامل وتكامل مع الذاكرة المركزية ونظام A2A.

## المميزات الرئيسية

### إدارة الكلمات المفتاحية
- تصنيف متقدم للكلمات المفتاحية حسب نوع النبات وأنواع الإصابات وأجزاء النبات
- دعم العلاقات الدلالية بين الكلمات المفتاحية (مرادفات، علاقات هرمية، إلخ)
- تحليل أداء الكلمات المفتاحية وإحصائيات متقدمة
- تكامل مع الذاكرة المركزية لتحسين التعلم

### إدارة المصادر الموثوقة
- آلية تقييم ديناميكية لمستويات الثقة
- نظام القائمة السوداء للمصادر غير الموثوقة
- آلية التحقق من المصادر وتوثيقها
- تسجيل استخدام المصادر وتحليل أدائها

### إدارة محركات البحث
- نظام توزيع الحمل المتقدم مع دعم استراتيجيات متعددة
- مراقبة أداء محركات البحث وتسجيل الإحصائيات
- دعم إضافة وتعديل وحذف محركات البحث من واجهة الإعدادات

## المتطلبات التقنية

### متطلبات النظام
- Python 3.11+
- PostgreSQL 14+
- Redis (للتخزين المؤقت وإدارة المهام)

### المكتبات الرئيسية
- FastAPI
- SQLAlchemy
- Pydantic
- TensorFlow/PyTorch (للتعلم الآلي)
- Vue.js (للواجهة الأمامية)

## التثبيت والإعداد

### باستخدام Docker
1. تأكد من تثبيت Docker و Docker Compose على نظامك
2. انسخ المستودع إلى جهازك المحلي
3. انتقل إلى مجلد المشروع
4. قم بتشغيل الأمر التالي:
```bash
docker-compose up -d
```

### التثبيت اليدوي
1. قم بإنشاء بيئة Python افتراضية:
```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
venv\Scripts\activate  # على Windows
```

2. قم بتثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

3. قم بإعداد متغيرات البيئة:
```bash
cp .env.example .env
# قم بتعديل ملف .env حسب إعدادات بيئتك
```

4. قم بتشغيل الخدمة:
```bash
uvicorn main:app --reload
```

## هيكل المشروع

```
auto_learning/
├── __init__.py
├── config.py
├── api.py
├── memory_integration.py
├── a2a_integration.py
├── keyword_management/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   ├── service.py
│   └── api.py
├── source_management/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   ├── service.py
│   └── api.py
├── search_engine_management/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   ├── service.py
│   └── api.py
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   ├── helpers.py
│   └── constants.py
├── frontend/
│   ├── AutoLearningDashboard.vue
│   ├── KeywordManager.vue
│   ├── SourceManager.vue
│   ├── SearchEngineManager.vue
│   └── charts/
│       └── KeywordPerformanceChart.vue
├── services/
│   ├── ApiService.js
│   ├── KeywordApiService.js
│   ├── SourceApiService.js
│   ├── SearchEngineApiService.js
│   └── PermissionService.js
├── tests/
│   ├── test_keyword_service.py
│   ├── integration_test.js
│   └── e2e_test.js
└── docs/
    ├── user_guide.md
    └── developer_guide.md
```

## التوثيق

للمزيد من المعلومات، يرجى الاطلاع على:
- [دليل المستخدم](./docs/user_guide.md)
- [دليل المطور](./docs/developer_guide.md)

## المساهمة

نرحب بمساهماتكم في تطوير هذا المديول. يرجى اتباع إرشادات المساهمة الموجودة في [CONTRIBUTING.md](../CONTRIBUTING.md).

## الترخيص

هذا المشروع مرخص تحت [رخصة MIT](../LICENSE).
