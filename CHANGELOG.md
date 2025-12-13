# Changelog

جميع التغييرات المهمة في هذا المستودع سيتم توثيقها في هذا الملف.

التنسيق مبني على [Keep a Changelog](https://keepachangelog.com/ar/1.0.0/)،
وهذا المشروع يلتزم بـ [Semantic Versioning](https://semver.org/lang/ar/).

## [1.1.0] - 2025-10-21

### Added
- إضافة `.github/workflows/ci.yml` - GitHub Actions للـ CI/CD الكامل
- إضافة `.markdownlint.json` - تكوين Markdown Lint
- إضافة `templates/Dockerfile` - قالب Docker للمشاريع
- إضافة `templates/docker-compose.yml` - قالب Docker Compose شامل
- إضافة `templates/.env.example` - قالب المتغيرات البيئية
- إضافة `scripts/backup.sh` - سكريبت النسخ الاحتياطي الآلي
- إضافة `examples/simple-api/` - مثال مشروع API بسيط

### Enhanced
- تحسين CI/CD مع اختبارات آلية
- إضافة ShellCheck و Markdown Lint
- إضافة Security Scan مع Trivy
- إضافة اختبارات السكريبتات
- إضافة إنشاء Releases تلقائياً

### Documentation
- توثيق قوالب Docker
- توثيق النسخ الاحتياطي
- إضافة أمثلة عملية

## [1.0.0] - 2025-10-21

### Added
- إضافة `GLOBAL_GUIDELINES.txt` - البرومبت الشامل مع جميع التوجيهات والسياسات
- إضافة `setup_project_structure.sh` - سكريبت إنشاء هيكل المشروع الكامل
- إضافة `Solution_Tradeoff_Log.md` - قالب توثيق القرارات التقنية مع OSF_Score
- إضافة `download_and_setup.sh` - سكريبت التحميل والتشغيل السريع
- إضافة `validate_project.sh` - سكريبت التحقق من صحة المشروع
- إضافة `README.md` - توثيق شامل للمستودع وطريقة الاستخدام
- إضافة `.gitignore` - استبعاد الملفات غير المطلوبة
- إضافة `CHANGELOG.md` - سجل التغييرات
- إضافة `CONTRIBUTING.md` - دليل المساهمة
- إضافة `LICENSE` - ترخيص المستودع
- إضافة `.github/ISSUE_TEMPLATE/bug_report.md` - قالب تقرير الأخطاء
- إضافة `.github/ISSUE_TEMPLATE/feature_request.md` - قالب طلب الميزات

### Features
- هيكل مجلدات شامل مع 17+ ملف توثيق
- دعم APPEND-ONLY للملفات التوثيقية
- معايير OSF (Optimal & Safe Over Easy/Fast)
- نموذج RBAC للصلاحيات
- قوالب جاهزة للتوثيق التقني
- التحقق الآلي من صحة المشروع

### Documentation
- دليل استخدام شامل بثلاث طرق مختلفة
- أمثلة عملية للاستخدام
- توثيق معادلة OSF_Score
- شرح المبادئ الأساسية

## [Unreleased]

### Planned
- إضافة قوالب اختبارات (unit, integration, e2e)
- إضافة قوالب توثيق API (OpenAPI/Swagger)
- إضافة سكريبتات صيانة إضافية
- إضافة دعم Kubernetes
- إضافة قوالب Infrastructure as Code (Terraform)

---

## أنواع التغييرات

- `Added` للميزات الجديدة
- `Changed` للتغييرات في الميزات الموجودة
- `Deprecated` للميزات التي ستُحذف قريباً
- `Removed` للميزات المحذوفة
- `Fixed` لإصلاح الأخطاء
- `Security` لإصلاحات الأمان
- `Enhanced` للتحسينات والتطويرات

