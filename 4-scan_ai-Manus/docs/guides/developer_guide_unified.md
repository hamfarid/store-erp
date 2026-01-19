# دليل المطور الموحد لنظام Gaara Scan AI

هذا الدليل الموحد يجمع جميع المعلومات اللازمة لتطوير وتعديل نظام Gaara Scan AI، بما في ذلك بنية النظام، تطوير الوحدات، وأفضل الممارسات.

## المحتويات

1. [مقدمة](#مقدمة)
2. [بنية المشروع](#بنية-المشروع)
3. [بيئة التطوير](#بيئة-التطوير)
4. [تطوير الوحدات](#تطوير-الوحدات)
   - [واجهة الإدارة](#واجهة-الإدارة)
   - [وحدة إدارة الذكاء الاصطناعي](#وحدة-إدارة-الذكاء-الاصطناعي)
   - [الوحدات الزراعية](#الوحدات-الزراعية)
5. [إدارة قواعد البيانات](#إدارة-قواعد-البيانات)
6. [اختبار النظام](#اختبار-النظام)
7. [النشر والتوزيع](#النشر-والتوزيع)
8. [أفضل الممارسات](#أفضل-الممارسات)
9. [استكشاف الأخطاء وإصلاحها](#استكشاف-الأخطاء-وإصلاحها)

## مقدمة

نظام Gaara Scan AI هو منصة متكاملة للتحليل والمعالجة باستخدام الذكاء الاصطناعي، مع تركيز خاص على التطبيقات الزراعية. يتكون النظام من عدة وحدات مترابطة تعمل معًا لتوفير تجربة مستخدم متكاملة.

## بنية المشروع

```
gaara-scan-ai/
├── docs/                    # التوثيق
├── scripts/                 # سكريبتات التشغيل والأدوات المساعدة
├── src/                     # كود المصدر
│   ├── modules/             # وحدات النظام
│   │   ├── ai_management/   # وحدة إدارة الذكاء الاصطناعي
│   │   ├── image_search/    # وحدة البحث عن الصور
│   │   └── ...              # وحدات أخرى
│   ├── core/                # وحدات النواة
│   │   ├── permissions/     # نظام الصلاحيات
│   │   ├── users_accounts/  # إدارة المستخدمين
│   │   └── ...              # وحدات نواة أخرى
│   └── web_interface/       # واجهة الويب
│       ├── admin_panel/     # لوحة الإدارة
│       └── api/             # واجهة برمجة التطبيقات
├── tests/                   # اختبارات النظام
├── .env-example             # نموذج ملف البيئة
├── docker-compose.yml       # تكوين Docker Compose
├── Dockerfile               # تعريف صورة Docker
└── README.md                # ملف القراءة الرئيسي
```

## بيئة التطوير

### المتطلبات

- Python 3.9+
- Node.js 16+
- Docker و Docker Compose
- Git

### إعداد بيئة التطوير المحلية

1. استنساخ المستودع:
   ```bash
   git clone https://github.com/your-organization/gaara-scan-ai.git
   cd gaara-scan-ai
   ```

2. إنشاء بيئة Python افتراضية:
   ```bash
   python -m venv venv
   source venv/bin/activate  # على Linux/macOS
   venv\Scripts\activate     # على Windows
   ```

3. تثبيت التبعيات:
   ```bash
   pip install -r requirements.txt
   cd src/web_interface/admin_panel
   npm install
   ```

4. إنشاء ملف البيئة:
   ```bash
   cp .env-example .env
   ```

5. تعديل ملف `.env` حسب بيئة التطوير المحلية.

### تشغيل النظام في بيئة التطوير

#### باستخدام Docker

```bash
docker-compose up -d
```

#### بدون Docker

1. تشغيل الخادم الخلفي:
   ```bash
   cd src
   python main.py
   ```

2. تشغيل واجهة الإدارة:
   ```bash
   cd src/web_interface/admin_panel
   npm run dev
   ```

## تطوير الوحدات

### واجهة الإدارة

واجهة الإدارة مبنية باستخدام React و TypeScript. لتطوير واجهة الإدارة:

1. انتقل إلى مجلد واجهة الإدارة:
   ```bash
   cd src/web_interface/admin_panel
   ```

2. قم بتثبيت التبعيات إذا لم تكن مثبتة:
   ```bash
   npm install
   ```

3. قم بتشغيل خادم التطوير:
   ```bash
   npm run dev
   ```

4. افتح المتصفح على `http://localhost:3000`.

#### هيكل واجهة الإدارة

```
admin_panel/
├── public/              # الملفات العامة
├── src/                 # كود المصدر
│   ├── components/      # مكونات واجهة المستخدم
│   ├── contexts/        # سياقات React
│   ├── hooks/           # خطافات React المخصصة
│   ├── pages/           # صفحات التطبيق
│   ├── services/        # خدمات الاتصال بالخادم
│   ├── styles/          # أنماط CSS
│   ├── types/           # تعريفات TypeScript
│   ├── utils/           # أدوات مساعدة
│   ├── App.tsx          # مكون التطبيق الرئيسي
│   └── index.tsx        # نقطة الدخول
├── package.json         # تكوين NPM
└── tsconfig.json        # تكوين TypeScript
```

#### إضافة صفحة جديدة

1. أنشئ ملف الصفحة في مجلد `src/pages`:
   ```tsx
   // src/pages/NewFeaturePage.tsx
   import React from 'react';
   
   const NewFeaturePage: React.FC = () => {
     return (
       <div>
         <h1>ميزة جديدة</h1>
         {/* محتوى الصفحة */}
       </div>
     );
   };
   
   export default NewFeaturePage;
   ```

2. أضف الصفحة إلى نظام التوجيه في `src/App.tsx`:
   ```tsx
   import NewFeaturePage from './pages/NewFeaturePage';
   
   // داخل مكون App
   <Route path="/new-feature" element={<NewFeaturePage />} />
   ```

3. أضف رابطًا للصفحة في القائمة الجانبية.

### وحدة إدارة الذكاء الاصطناعي

وحدة إدارة الذكاء الاصطناعي مسؤولة عن إدارة نماذج الذكاء الاصطناعي وتدريبها وتقييمها.

#### هيكل الوحدة

```
ai_management/
├── __init__.py          # ملف التهيئة
├── models/              # تعريفات نماذج قاعدة البيانات
├── services/            # خدمات الوحدة
│   ├── __init__.py
│   ├── model_service.py # خدمة إدارة النماذج
│   └── training_service.py # خدمة التدريب
├── controllers/         # وحدات التحكم
│   ├── __init__.py
│   └── ai_controller.py # وحدة تحكم الذكاء الاصطناعي
└── utils/               # أدوات مساعدة
```

#### إضافة نموذج ذكاء اصطناعي جديد

1. أضف تعريف النموذج في `models/ai_model.py`:
   ```python
   class NewAIModel(BaseModel):
       """نموذج ذكاء اصطناعي جديد."""
       
       name = CharField(max_length=100)
       version = CharField(max_length=20)
       description = TextField(null=True)
       model_path = CharField(max_length=255)
       created_at = DateTimeField(auto_now_add=True)
       updated_at = DateTimeField(auto_now=True)
       
       class Meta:
           db_table = 'new_ai_models'
   ```

2. أضف خدمة للنموذج في `services/new_model_service.py`:
   ```python
   class NewModelService:
       """خدمة للنموذج الجديد."""
       
       def __init__(self):
           """تهيئة الخدمة."""
           self.model = None
           
       def load_model(self, model_path):
           """تحميل النموذج من المسار المحدد."""
           # كود تحميل النموذج
           
       def predict(self, input_data):
           """التنبؤ باستخدام النموذج."""
           # كود التنبؤ
           
       def evaluate(self, test_data):
           """تقييم النموذج."""
           # كود التقييم
   ```

3. أضف وحدة تحكم في `controllers/new_model_controller.py`:
   ```python
   class NewModelController:
       """وحدة تحكم للنموذج الجديد."""
       
       def __init__(self):
           """تهيئة وحدة التحكم."""
           self.service = NewModelService()
           
       def handle_prediction_request(self, request):
           """معالجة طلب التنبؤ."""
           # كود معالجة الطلب
           
       def handle_evaluation_request(self, request):
           """معالجة طلب التقييم."""
           # كود معالجة الطلب
   ```

### الوحدات الزراعية

الوحدات الزراعية تشمل مجموعة من الأدوات المتخصصة للتطبيقات الزراعية.

#### هيكل الوحدات الزراعية

```
agricultural_modules/
├── __init__.py
├── disease_diagnosis/   # تشخيص الأمراض النباتية
├── farms/               # إدارة المزارع
├── variety_trials/      # تجارب الأصناف
└── common/              # مكونات مشتركة
```

#### إضافة وحدة زراعية جديدة

1. أنشئ مجلدًا للوحدة الجديدة:
   ```bash
   mkdir -p src/modules/agricultural_modules/new_module
   ```

2. أنشئ ملف التهيئة:
   ```python
   # src/modules/agricultural_modules/new_module/__init__.py
   """وحدة زراعية جديدة."""
   ```

3. أضف الوحدة إلى قائمة الوحدات في `src/modules/agricultural_modules/__init__.py`.

## إدارة قواعد البيانات

### هيكل قاعدة البيانات

نظام Gaara Scan AI يستخدم PostgreSQL كقاعدة بيانات رئيسية. يتم تعريف نماذج قاعدة البيانات باستخدام ORM.

### ترحيل قاعدة البيانات

لإنشاء ترحيل جديد:

```bash
python manage.py makemigrations
```

لتطبيق الترحيلات:

```bash
python manage.py migrate
```

### استعلامات قاعدة البيانات

استخدم ORM للتعامل مع قاعدة البيانات:

```python
# مثال لاستعلام
users = User.objects.filter(is_active=True)

# مثال لإنشاء سجل
new_user = User(
    username='new_user',
    email='user@example.com',
    is_active=True
)
new_user.save()
```

## اختبار النظام

### اختبارات الوحدة

اختبارات الوحدة تستخدم pytest. لتشغيل اختبارات الوحدة:

```bash
pytest tests/unit
```

### اختبارات التكامل

اختبارات التكامل تختبر تفاعل الوحدات مع بعضها البعض:

```bash
pytest tests/integration
```

### اختبارات الواجهة

اختبارات الواجهة تستخدم Playwright:

```bash
cd src/web_interface/admin_panel
npm run test:e2e
```

## النشر والتوزيع

### النشر باستخدام Docker

1. بناء صور Docker:
   ```bash
   docker-compose build
   ```

2. تشغيل الحاويات:
   ```bash
   docker-compose up -d
   ```

### النشر المرحلي

النظام يدعم النشر المرحلي باستخدام ملفات docker-compose مختلفة:

```bash
# المرحلة 1: البنية الأساسية
docker-compose -f docker-compose.stage1.yml up -d

# المرحلة 2: الخدمات الأساسية
docker-compose -f docker-compose.stage2.yml up -d

# المرحلة 3: الخدمات المتقدمة
docker-compose -f docker-compose.stage3.yml up -d
```

## أفضل الممارسات

### توثيق الكود

استخدم docstrings لتوثيق جميع الوحدات والدوال والفئات:

```python
def process_image(image_path, options=None):
    """
    معالجة الصورة باستخدام الخوارزميات المحددة.
    
    Args:
        image_path (str): مسار الصورة المراد معالجتها.
        options (dict, optional): خيارات المعالجة. الافتراضي هو None.
        
    Returns:
        dict: نتائج المعالجة.
        
    Raises:
        FileNotFoundError: إذا لم يتم العثور على الصورة.
        ValueError: إذا كانت الصورة غير صالحة.
    """
    # كود المعالجة
```

### تقسيم الأكواد الكبيرة

قسم الأكواد الكبيرة إلى وحدات صغيرة لتسهيل الصيانة والاختبار.

### توثيق الأخطاء

وثق الأخطاء التي تواجهها في ملف `docs/fix_this_error.md` لتجنب تكرارها في المستقبل.

### استخدام أدوات فحص الكود

استخدم أدوات مثل flake8 و autopep8 للتحقق من جودة الكود:

```bash
flake8 src
autopep8 --in-place --recursive src
```

## استكشاف الأخطاء وإصلاحها

### مشكلة: خطأ في تثبيت التبعيات

**الحل**:
1. تحقق من إصدار Python:
   ```bash
   python --version
   ```
2. تحقق من تثبيت pip:
   ```bash
   pip --version
   ```
3. حاول تثبيت التبعيات بشكل منفصل:
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

### مشكلة: خطأ في بناء صورة Docker

**الحل**:
1. تحقق من تثبيت Docker:
   ```bash
   docker --version
   ```
2. تحقق من سجلات البناء:
   ```bash
   docker-compose build --no-cache
   ```
3. إذا واجهت خطأ "Cannot find module 'ajv/dist/compile/codegen'"، أضف:
   ```dockerfile
   # تثبيت حزم ajv وajv-keywords لحل المشكلة
   RUN npm install ajv@8.12.0 ajv-keywords@5.1.0 --legacy-peer-deps
   ```

### مشكلة: تعارض في إصدارات TypeScript

**الحل**:
1. تحقق من إصدار TypeScript المثبت:
   ```bash
   npm list typescript
   ```
2. استخدم خيار `--legacy-peer-deps` عند تثبيت الحزم:
   ```bash
   npm install --legacy-peer-deps
   ```
3. أو قم بتحديث إصدار TypeScript:
   ```bash
   npm install typescript@5.0.0
   ```

---

تم توحيد هذا الدليل من المستندات التالية:
- developer_guide.md
- developer_guide_admin_interface.md
- developer_guide_ai_management.md
- developer_guide_module_shutdown.md
- technical_guide_agricultural_modules.md
- technical_guide_agricultural_modules_updated.md
