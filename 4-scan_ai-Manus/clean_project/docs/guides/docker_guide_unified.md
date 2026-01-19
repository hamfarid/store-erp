# دليل Docker الموحد

هذا الدليل يجمع جميع المعلومات المتعلقة بـ Docker في نظام Gaara Scan AI، بما في ذلك التثبيت، التكوين، التشغيل، وحل المشكلات.

## المحتويات

1. [مقدمة](#مقدمة)
2. [متطلبات النظام](#متطلبات-النظام)
3. [التثبيت](#التثبيت)
4. [التكوين](#التكوين)
5. [التشغيل](#التشغيل)
6. [التحسين](#التحسين)
7. [الاختبار](#الاختبار)
8. [حل المشكلات الشائعة](#حل-المشكلات-الشائعة)
9. [النشر المرحلي](#النشر-المرحلي)

## مقدمة

يستخدم نظام Gaara Scan AI تقنية Docker لتوفير بيئة تشغيل موحدة ومعزولة. يتكون النظام من عدة حاويات Docker تعمل معًا لتوفير الوظائف المختلفة للنظام.

## متطلبات النظام

- Docker Engine 20.10.0 أو أحدث
- Docker Compose 2.0.0 أو أحدث
- وحدة معالجة مركزية (CPU) بـ 4 أنوية على الأقل
- ذاكرة وصول عشوائي (RAM) 8 جيجابايت على الأقل
- مساحة تخزين 50 جيجابايت على الأقل

## التثبيت

1. قم بتثبيت Docker و Docker Compose على نظامك:
   ```bash
   # لأنظمة Ubuntu/Debian
   sudo apt update
   sudo apt install docker.io docker-compose
   
   # لأنظمة Windows
   # قم بتنزيل وتثبيت Docker Desktop من الموقع الرسمي
   ```

2. تحقق من التثبيت:
   ```bash
   docker --version
   docker-compose --version
   ```

3. قم بتنزيل مشروع Gaara Scan AI:
   ```bash
   git clone https://github.com/your-organization/gaara-scan-ai.git
   cd gaara-scan-ai
   ```

## التكوين

1. قم بنسخ ملف البيئة النموذجي:
   ```bash
   cp .env-example .env
   ```

2. قم بتعديل ملف `.env` حسب احتياجاتك:
   ```
   # مثال لتكوين البيئة
   APP_PORT=8000
   DB_HOST=postgres
   DB_PORT=5432
   DB_NAME=gaaradb
   DB_USER=gaarauser
   DB_PASSWORD=your_secure_password
   ```

## التشغيل

### التشغيل العادي

استخدم السكريبت المناسب لنظام التشغيل الخاص بك:

- **Windows (PowerShell)**:
  ```powershell
  .\start-services.ps1
  ```

- **Linux/macOS**:
  ```bash
  ./start_services.sh
  ```

### التشغيل اليدوي

1. بناء الحاويات:
   ```bash
   docker-compose build
   ```

2. تشغيل الحاويات:
   ```bash
   docker-compose up -d
   ```

3. التحقق من حالة الحاويات:
   ```bash
   docker-compose ps
   ```

## التحسين

لتحسين أداء Docker في نظام Gaara Scan AI:

1. **تحسين الذاكرة المؤقتة**:
   - استخدم نظام التخزين المؤقت للصور
   - قم بتكوين حدود الذاكرة المناسبة لكل حاوية

2. **تحسين الصور**:
   - استخدم صور أساسية أصغر حجمًا
   - قم بتقليل عدد الطبقات في Dockerfile

3. **تحسين الشبكة**:
   - استخدم شبكات Docker المخصصة
   - قم بتكوين DNS بشكل صحيح

## الاختبار

لاختبار حاويات Docker:

1. اختبار الاتصال:
   ```bash
   docker-compose exec app ping db
   ```

2. اختبار قاعدة البيانات:
   ```bash
   docker-compose exec db psql -U gaarauser -d gaaradb -c "SELECT version();"
   ```

3. اختبار واجهة API:
   ```bash
   curl http://localhost:8000/api/health
   ```

## حل المشكلات الشائعة

### مشكلة: الحاوية لا تبدأ

**الحل**:
1. تحقق من سجلات الحاوية:
   ```bash
   docker-compose logs app
   ```
2. تحقق من وجود تعارضات في المنافذ:
   ```bash
   netstat -tuln | grep 8000
   ```

### مشكلة: خطأ في الاتصال بقاعدة البيانات

**الحل**:
1. تحقق من تكوين قاعدة البيانات في ملف `.env`
2. تحقق من حالة حاوية قاعدة البيانات:
   ```bash
   docker-compose ps db
   ```

### مشكلة: خطأ "Cannot find module 'ajv/dist/compile/codegen'"

**الحل**:
1. أضف تثبيت حزم ajv وajv-keywords في Dockerfile:
   ```dockerfile
   # تثبيت حزم ajv وajv-keywords لحل مشكلة "Cannot find module 'ajv/dist/compile/codegen'"
   RUN npm install ajv@8.12.0 ajv-keywords@5.1.0 --no-save
   ```
2. أضف المكتبات إلى package.json:
   ```json
   "dependencies": {
     "ajv": "^8.12.0",
     "ajv-keywords": "^5.1.0"
   }
   ```

## النشر المرحلي

لتنفيذ النشر المرحلي:

1. قم بتكوين بيئات مختلفة:
   ```bash
   cp .env-example .env.development
   cp .env-example .env.staging
   cp .env-example .env.production
   ```

2. استخدم ملفات docker-compose المختلفة:
   ```bash
   docker-compose -f docker-compose.stage1.yml up -d
   docker-compose -f docker-compose.stage2.yml up -d
   ```

3. اختبر كل مرحلة قبل الانتقال إلى المرحلة التالية.

---

تم توحيد هذا الدليل من المستندات التالية:
- DEPLOYMENT_GUIDE.md
- docker_optimization_guide.md
- docker_testing_guide.md
- comprehensive_docker_guide.md
- docker_manager_user_guide.md
- README_STAGED_DEPLOYMENT.md
