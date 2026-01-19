# دليل استخدام متغيرات البيئة في النظام الزراعي المتكامل

## مقدمة

يوفر النظام الزراعي المتكامل دعمًا شاملاً لمتغيرات البيئة (Environment Variables) لتسهيل تكوين النظام في بيئات مختلفة دون الحاجة إلى تعديل الكود المصدري. يتيح هذا النهج:

- فصل الإعدادات عن الكود
- تخزين المعلومات الحساسة (مثل مفاتيح API وكلمات المرور) بشكل آمن
- تكوين النظام لبيئات مختلفة (تطوير، اختبار، إنتاج)
- تسهيل نشر النظام في حاويات Docker

## كيفية استخدام متغيرات البيئة

### 1. إنشاء ملف `.env`

انسخ ملف `.env.example` إلى ملف جديد باسم `.env` في المجلد الرئيسي للمشروع:

```bash
cp .env.example .env
```

ثم قم بتعديل القيم حسب احتياجاتك.

### 2. الوصول إلى متغيرات البيئة في الكود

يمكن الوصول إلى متغيرات البيئة في الكود باستخدام وحدة `EnvLoader`:

```python
from src.utils.config.env_loader import get_env_loader

# الحصول على مثيل EnvLoader
env_loader = get_env_loader()

# الحصول على قيمة متغير بيئة
app_name = env_loader.get('APP_NAME', 'Agricultural AI System')  # القيمة الافتراضية هي 'Agricultural AI System'

# الحصول على قيمة متغير بيئة مع تحويل النوع
debug_mode = env_loader.get_bool('APP_DEBUG', False)
port = env_loader.get_int('APP_PORT', 8000)
hosts = env_loader.get_list('SECURITY_ALLOWED_HOSTS', ['localhost'])
```

### 3. استخدام متغيرات البيئة في ملفات التكوين

يمكن استخدام متغيرات البيئة في ملفات التكوين YAML/JSON باستخدام الصيغة `${VARIABLE_NAME}`:

```yaml
app:
  name: ${APP_NAME}
  debug: ${APP_DEBUG}
  url: ${APP_URL}
  port: ${APP_PORT}
  host: ${APP_HOST}
  secret_key: ${APP_SECRET_KEY}
```

يمكن أيضًا تحديد قيمة افتراضية في حالة عدم وجود المتغير:

```yaml
app:
  name: ${APP_NAME:Agricultural AI System}
  debug: ${APP_DEBUG:false}
  url: ${APP_URL:http://localhost:8000}
```

### 4. تحميل ملفات التكوين

يمكن تحميل ملفات التكوين باستخدام وحدة `ConfigLoader`:

```python
from src.utils.config.config_loader import load_config

# تحميل التكوين الافتراضي
config = load_config()

# تحميل التكوين مع تحديد البيئة
config = load_config(env='production')

# تحميل ملف تكوين محدد
config = load_config(config_file='custom_config.yaml')

# تحميل التكوين مع تجاوز بعض القيم
override_vars = {
    'app': {
        'debug': False,
        'port': 9000
    }
}
config = load_config(override_vars=override_vars)

# تحميل التكوين مع إعادة التحميل التلقائي
config = load_config(auto_reload=True)
```

## فئات متغيرات البيئة المدعومة

يدعم النظام الفئات التالية من متغيرات البيئة:

### معلومات عامة

| المتغير | الوصف | القيمة الافتراضية |
|---------|-------|------------------|
| APP_NAME | اسم التطبيق | AgriculturalAISystem |
| APP_ENV | بيئة التشغيل | development |
| APP_DEBUG | وضع التصحيح | true |
| APP_LOG_LEVEL | مستوى السجل | debug |
| APP_URL | عنوان URL للتطبيق | http://localhost:8000 |
| APP_PORT | منفذ التطبيق | 8000 |
| APP_HOST | مضيف التطبيق | 0.0.0.0 |
| APP_SECRET_KEY | مفتاح سري للتطبيق | randomly_generated_secret_key |

### قاعدة البيانات

| المتغير | الوصف | القيمة الافتراضية |
|---------|-------|------------------|
| DB_CONNECTION | نوع اتصال قاعدة البيانات | sqlite |
| DB_HOST | مضيف قاعدة البيانات | localhost |
| DB_PORT | منفذ قاعدة البيانات | 3306 |
| DB_DATABASE | اسم/مسار قاعدة البيانات | /home/ubuntu/agricultural_ai_system/data/database.sqlite |
| DB_USERNAME | اسم مستخدم قاعدة البيانات | root |
| DB_PASSWORD | كلمة مرور قاعدة البيانات | |
| DB_PREFIX | بادئة جداول قاعدة البيانات | |
| DB_CHARSET | مجموعة أحرف قاعدة البيانات | utf8mb4 |
| DB_COLLATION | ترتيب قاعدة البيانات | utf8mb4_unicode_ci |

### مسارات الملفات

| المتغير | الوصف | القيمة الافتراضية |
|---------|-------|------------------|
| DATA_DIR | مجلد البيانات | /home/ubuntu/agricultural_ai_system/data |
| MODELS_DIR | مجلد النماذج | /home/ubuntu/agricultural_ai_system/models |
| UPLOADS_DIR | مجلد التحميلات | /home/ubuntu/agricultural_ai_system/uploads |
| TEMP_DIR | المجلد المؤقت | /home/ubuntu/agricultural_ai_system/temp |
| LOGS_DIR | مجلد السجلات | /home/ubuntu/agricultural_ai_system/logs |

### مفاتيح API

| المتغير | الوصف |
|---------|-------|
| GOOGLE_API_KEY | مفتاح API لخدمات Google |
| BING_API_KEY | مفتاح API لخدمات Bing |
| WEATHER_API_KEY | مفتاح API لخدمات الطقس |
| MAPBOX_API_KEY | مفتاح API لخدمات Mapbox |
| PLANT_ID_API_KEY | مفتاح API لخدمات تحديد النباتات |
| SOIL_API_KEY | مفتاح API لخدمات تحليل التربة |

### إعدادات Docker

| المتغير | الوصف | القيمة الافتراضية |
|---------|-------|------------------|
| DOCKER_REGISTRY | سجل Docker | |
| DOCKER_IMAGE_PREFIX | بادئة صورة Docker | agricultural-ai |
| DOCKER_TAG | علامة Docker | latest |
| DOCKER_API_SERVER_REPLICAS | عدد نسخ خادم API | 2 |
| DOCKER_IMAGE_PROCESSOR_REPLICAS | عدد نسخ معالج الصور | 2 |
| DOCKER_NETWORK_NAME | اسم شبكة Docker | agricultural-ai-network |
| DOCKER_VOLUME_NAME | اسم مجلد Docker | agricultural-ai-data |

## ميزات متقدمة

### إعادة التحميل التلقائي

يدعم النظام إعادة التحميل التلقائي لملف `.env` وملفات التكوين عند تغييرها:

```python
# إعادة التحميل التلقائي لمتغيرات البيئة
env_loader = get_env_loader(auto_reload=True)

# إعادة التحميل التلقائي للتكوين
config_loader = get_config_loader(auto_reload=True)
```

### تصدير متغيرات البيئة

يمكن تصدير متغيرات البيئة إلى ملف:

```python
env_loader = get_env_loader()
env_loader.export_to_file('/path/to/exported.env', include_system=True)
```

### التحقق من صحة التكوين

يمكن التحقق من صحة التكوين باستخدام مخطط JSON:

```python
config_loader = get_config_loader()
schema = {
    "type": "object",
    "properties": {
        "app": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "debug": {"type": "boolean"},
                "port": {"type": "integer"}
            },
            "required": ["name", "port"]
        }
    }
}
is_valid = config_loader.validate_config(config, schema)
```

## أفضل الممارسات

1. **لا تقم أبدًا بتضمين ملف `.env` في نظام التحكم في الإصدار**. استخدم ملف `.env.example` كقالب.
2. **استخدم متغيرات البيئة للمعلومات الحساسة** مثل مفاتيح API وكلمات المرور وبيانات الاعتماد.
3. **استخدم القيم الافتراضية** عند الوصول إلى متغيرات البيئة لتجنب الأخطاء.
4. **استخدم أنواع البيانات المناسبة** عند الوصول إلى متغيرات البيئة (`get_int`، `get_bool`، إلخ).
5. **استخدم متغيرات البيئة للإعدادات المتغيرة** بين البيئات المختلفة (تطوير، اختبار، إنتاج).
6. **استخدم ملفات تكوين منفصلة** للإعدادات الثابتة والمشتركة بين جميع البيئات.
7. **استخدم الإشارات المرجعية** في ملفات YAML لتجنب التكرار (مثل `&reference` و `*reference`).

## استكشاف الأخطاء وإصلاحها

### مشكلة: متغير البيئة غير موجود

إذا كنت تواجه أخطاء بسبب متغيرات بيئة مفقودة، تأكد من:
- وجود ملف `.env` في المجلد الصحيح
- تعريف المتغير في ملف `.env`
- استخدام القيم الافتراضية عند الوصول إلى المتغيرات

### مشكلة: تنسيق متغير البيئة غير صحيح

إذا كنت تواجه أخطاء في تحويل النوع، تأكد من:
- استخدام الدالة الصحيحة للحصول على القيمة (`get_int`، `get_bool`، إلخ)
- تنسيق القيمة بشكل صحيح في ملف `.env`

### مشكلة: عدم استبدال متغيرات البيئة في ملفات التكوين

إذا لم يتم استبدال متغيرات البيئة في ملفات التكوين، تأكد من:
- استخدام الصيغة الصحيحة: `${VARIABLE_NAME}`
- تحميل التكوين باستخدام `ConfigLoader`
- تعريف المتغير في ملف `.env` أو استخدام قيمة افتراضية: `${VARIABLE_NAME:default_value}`
