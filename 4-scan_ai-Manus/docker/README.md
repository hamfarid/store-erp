# دليل استخدام حاويات Docker للنظام الزراعي المتكامل

## مقدمة

يوفر هذا الدليل معلومات حول كيفية استخدام حاويات Docker لتشغيل نظام الذكاء الاصطناعي الزراعي المتكامل. تم تصميم النظام ليعمل باستخدام عدة حاويات متخصصة تتواصل مع بعضها البعض، مما يسمح بتشغيل نسخ متعددة (replicas) من الخدمات لتحقيق التوازن في الحمل والتوافر العالي.

## متطلبات النظام

- Docker (الإصدار 20.10.0 أو أحدث)
- Docker Compose (الإصدار 2.0.0 أو أحدث)
- مساحة تخزين: 10 جيجابايت على الأقل
- ذاكرة: 8 جيجابايت على الأقل

## هيكل الحاويات

يتكون النظام من الحاويات التالية:

1. **api_server**: خادم API مبني على FastAPI وDjango، يوفر واجهة برمجة التطبيقات للنظام.
2. **image_processor**: خدمة معالجة الصور مبنية على PyTorch، تقوم بتحليل الصور وكشف الأمراض.
3. **load_balancer**: موازن الحمل (Nginx) الذي يوزع الطلبات على نسخ متعددة من خادم API.
4. **database**: قاعدة بيانات PostgreSQL لتخزين بيانات النظام.

## ملفات التكوين

- **Dockerfile.api_server**: ملف بناء حاوية خادم API.
- **Dockerfile.image_processor**: ملف بناء حاوية معالجة الصور.
- **docker-compose.yml**: ملف تكوين Docker Compose لتشغيل جميع الحاويات معًا.
- **nginx.conf**: ملف تكوين Nginx لموازنة الحمل.
- **deploy.sh**: نص برمجي لبناء ونشر الحاويات.

## متغيرات البيئة

يستخدم النظام ملف `.env` لتكوين متغيرات البيئة. يجب إنشاء هذا الملف في المجلد الرئيسي للمشروع باستخدام `.env.example` كقالب. فيما يلي المتغيرات الرئيسية:

```
# متغيرات قاعدة البيانات
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=agricultural_ai
DB_HOST=database

# متغيرات خادم API
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1,api_server
LOG_LEVEL=INFO

# متغيرات معالجة الصور
MODEL_DIR=/app/models
DATA_DIR=/app/data
```

## كيفية التشغيل

1. تأكد من تثبيت Docker و Docker Compose.
2. انسخ ملف `.env.example` إلى `.env` وقم بتعديل القيم حسب احتياجاتك.
3. قم بتنفيذ النص البرمجي `deploy.sh`:

```bash
cd /path/to/agricultural_ai_system
chmod +x docker/deploy.sh
./docker/deploy.sh
```

4. بعد التشغيل بنجاح، يمكن الوصول إلى النظام على:
   - واجهة المستخدم: http://localhost
   - واجهة برمجة التطبيقات: http://localhost/api/
   - خدمة معالجة الصور: http://localhost/image/

## توسيع النظام

### زيادة عدد النسخ (Replicas)

يمكن زيادة عدد نسخ خادم API لتحسين الأداء والتوافر العالي عن طريق تعديل قيمة `replicas` في ملف `docker-compose.yml`:

```yaml
api_server:
  # ... تكوين آخر
  deploy:
    replicas: 4  # زيادة عدد النسخ حسب الحاجة
```

### تخصيص موارد الحاويات

يمكن تخصيص موارد CPU والذاكرة لكل حاوية عن طريق تعديل قسم `resources` في ملف `docker-compose.yml`:

```yaml
image_processor:
  # ... تكوين آخر
  deploy:
    resources:
      limits:
        cpus: '4'       # زيادة عدد وحدات المعالجة
        memory: 8G      # زيادة الذاكرة المخصصة
```

## استكشاف الأخطاء وإصلاحها

### عرض سجلات الحاويات

```bash
docker-compose -f docker/docker-compose.yml logs -f [اسم_الخدمة]
```

### إعادة تشغيل خدمة معينة

```bash
docker-compose -f docker/docker-compose.yml restart [اسم_الخدمة]
```

### التحقق من حالة الخدمات

```bash
docker-compose -f docker/docker-compose.yml ps
```

## الأمان

- تأكد من تغيير كلمات المرور الافتراضية في ملف `.env`.
- قم بتقييد الوصول إلى منافذ Docker في بيئة الإنتاج.
- استخدم شبكة خاصة لاتصالات الحاويات في بيئة الإنتاج.
