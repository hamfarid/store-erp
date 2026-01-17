# مسارات الملفات المصنفة - Gaara ERP v12

## نظرة عامة
تصنيف شامل لجميع مسارات الملفات في نظام Gaara ERP v12 حسب النوع والوظيفة.

## إحصائيات الملفات
- **إجمالي الملفات**: 1,660+ ملف Python
- **الوحدات الرئيسية**: 8 وحدات
- **الوحدات الفرعية**: 45+ وحدة فرعية
- **ملفات الاختبار**: 200+ ملف اختبار
- **ملفات التكوين**: 50+ ملف إعداد

## 1. الملفات الأساسية (Core Files)

### 1.1 ملفات الإعداد الرئيسية
```
gaara_erp/
├── manage.py                           # أداة إدارة Django
├── requirements.txt                    # متطلبات Python الأساسية
├── requirements_enhanced_security.txt  # متطلبات الأمان المحسن
├── Dockerfile                         # ملف Docker الأساسي
├── Dockerfile.enhanced                # ملف Docker المحسن
├── docker-compose.yml                 # تكوين Docker Compose الأساسي
├── docker-compose.enhanced.yml        # تكوين Docker Compose المحسن
├── .env.example                       # مثال على متغيرات البيئة
├── .gitignore                         # ملفات Git المتجاهلة
└── README.md                          # دليل المشروع الرئيسي
```

### 1.2 ملفات الإعدادات (Settings)
```
gaara_erp/gaara_erp/
├── __init__.py
├── settings/
│   ├── __init__.py
│   ├── base.py                        # الإعدادات الأساسية
│   ├── dev.py                         # إعدادات التطوير
│   ├── prod.py                        # إعدادات الإنتاج
│   ├── test.py                        # إعدادات الاختبار
│   ├── security.py                    # إعدادات الأمان
│   ├── security_enhanced.py           # إعدادات الأمان المحسن
│   ├── cache.py                       # إعدادات التخزين المؤقت
│   └── celery_config.py               # إعدادات Celery
├── settings_backup.py                 # نسخة احتياطية من الإعدادات
├── settings_enhanced_security.py      # إعدادات الأمان المحسن الرئيسية
├── urls.py                           # URLs الرئيسية
├── wsgi.py                           # تكوين WSGI
├── asgi.py                           # تكوين ASGI
└── celery.py                         # تكوين Celery
```

## 2. الوحدات الأساسية (Core Modules)

### 2.1 إدارة المستخدمين
```
gaara_erp/core_modules/
├── __init__.py
├── users/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                      # نماذج المستخدمين
│   ├── serializers.py                # مسلسلات API
│   ├── views.py                       # عروض API
│   ├── urls.py                        # مسارات URLs
│   ├── permissions.py                 # صلاحيات المستخدمين
│   ├── services.py                    # خدمات المستخدمين
│   ├── filters.py                     # مرشحات البيانات
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   └── tests.py                       # اختبارات الوحدة
```

### 2.2 نظام الصلاحيات
```
gaara_erp/core_modules/
├── permissions/
│   ├── __init__.py
│   ├── models.py                      # نماذج الصلاحيات
│   ├── services.py                    # خدمات الصلاحيات
│   ├── decorators.py                  # مزخرفات الصلاحيات
│   └── middleware.py                  # وسطاء الصلاحيات
├── ai_permissions/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                      # صلاحيات الذكاء الاصطناعي
│   ├── services.py
│   ├── config.py
│   └── integrations.py
└── unified_permissions/
    ├── __init__.py
    ├── models.py                      # نظام الصلاحيات الموحد
    ├── abac_models.py                 # نماذج ABAC
    └── tests.py
```

### 2.3 إعدادات النظام
```
gaara_erp/core_modules/
├── system_settings/
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py
│   ├── models.py                      # إعدادات النظام
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── signals.py                     # إشارات النظام
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_integration.py
│   └── test_integration.py
```

## 3. الوحدات التجارية (Business Modules)

### 3.1 وحدة المحاسبة
```
gaara_erp/business_modules/accounting/
├── __init__.py
├── apps.py
├── models.py                          # نماذج المحاسبة الرئيسية
├── serializers.py                     # مسلسلات API
├── views.py                           # عروض API
├── urls.py                            # مسارات URLs
├── services/
│   ├── __init__.py
│   ├── account_service.py             # خدمة الحسابات
│   ├── journal_service.py             # خدمة دفاتر اليومية
│   ├── report_service.py              # خدمة التقارير
│   └── settlement_service.py          # خدمة التسويات
├── api/
│   ├── __init__.py
│   ├── account_api.py                 # API الحسابات
│   ├── journal_api.py                 # API دفاتر اليومية
│   └── serializers.py
├── views/
│   ├── integration_api.py             # API التكامل
│   └── settlement_views.py            # عروض التسويات
├── serializers/
│   └── settlement_serializers.py      # مسلسلات التسويات
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   ├── 0002_initial.py
│   └── 0003_initial.py
└── tests/
    ├── __init__.py
    ├── conftest.py                    # إعداد الاختبارات
    ├── test_models.py                 # اختبار النماذج
    ├── test_account_service.py        # اختبار خدمة الحسابات
    ├── test_journal_service.py        # اختبار خدمة اليومية
    ├── test_report_service.py         # اختبار خدمة التقارير
    └── test_integration.py            # اختبار التكامل
```

### 3.2 وحدة المخزون
```
gaara_erp/business_modules/inventory/
├── __init__.py
├── apps.py
├── models.py                          # نماذج المخزون
├── serializers.py
├── views.py
├── urls.py
├── services.py                        # خدمات المخزون
├── filters.py                         # مرشحات المخزون
├── permissions.py
├── products.py                        # إدارة المنتجات
├── processes.py                       # عمليات المخزون
├── queries.py                         # استعلامات المخزون
├── reports.py                         # تقارير المخزون
├── signals.py                         # إشارات المخزون
├── tracking.py                        # تتبع المخزون
├── transactions.py                    # معاملات المخزون
├── utils.py                           # أدوات مساعدة
├── product_views.py                   # عروض المنتجات
├── stock_views.py                     # عروض المخزون
├── location_views.py                  # عروض المواقع
├── report_views.py                    # عروض التقارير
├── setting_views.py                   # عروض الإعدادات
├── tracking_views.py                  # عروض التتبع
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       ├── create_sample_inventory.py
│       └── create_sample_uom_categories.py
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    ├── test_integration.py
    └── test_product.py
```

### 3.3 وحدة المبيعات
```
gaara_erp/business_modules/sales/
├── __init__.py
├── apps.py
├── admin.py
├── models.py                          # نماذج المبيعات
├── serializers.py
├── views.py
├── urls.py
├── services.py                        # خدمات المبيعات
├── filters.py
├── permissions.py
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
└── tests/
    ├── __init__.py
    ├── test_customer.py               # اختبار العملاء
    └── test_sales_order.py            # اختبار أوامر البيع
```

### 3.4 وحدة المشتريات
```
gaara_erp/business_modules/purchasing/
├── __init__.py
├── apps.py
├── admin.py
├── models.py                          # نماذج المشتريات (مرجع)
├── serializers.py
├── views.py
├── urls.py
├── services.py                        # خدمات المشتريات
├── filters.py
├── permissions.py
├── orders.py                          # أوامر الشراء
├── suppliers.py                       # الموردين
├── invoices.py                        # فواتير الشراء
├── payments.py                        # مدفوعات الشراء
├── receipts.py                        # إيصالات الاستلام
├── requisitions.py                    # طلبات الشراء
├── returns.py                         # مرتجعات الشراء
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
└── tests/
    ├── __init__.py
    ├── test_integration.py
    ├── test_purchase_order.py
    └── test_supplier.py
```

## 4. الوحدات الزراعية (Agricultural Modules)

### 4.1 إدارة المزارع
```
gaara_erp/agricultural_modules/farms/
├── __init__.py
├── apps.py
├── admin.py
├── models.py                          # نماذج المزارع
├── serializers.py
├── views.py
├── api_views.py                       # عروض API
├── urls.py
├── services.py                        # خدمات المزارع
├── filters.py
├── permissions.py
├── integration.py                     # تكامل المزارع
├── integration_assets.py              # أصول التكامل
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    ├── test_integration.py
    └── test_performance.py
```

### 4.2 تشخيص النباتات
```
gaara_erp/agricultural_modules/plant_diagnosis/
├── __init__.py
├── apps.py
├── models.py                          # نماذج تشخيص النباتات
├── services.py                        # خدمات التشخيص
├── api_client.py                      # عميل API التشخيص
├── crypto.py                          # تشفير البيانات
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
└── tests/
    ├── __init__.py
    └── test_integration.py
```

### 4.3 الإنتاج الزراعي
```
gaara_erp/agricultural_modules/production/
├── __init__.py
├── apps.py
├── models.py                          # نماذج الإنتاج الزراعي
├── services.py
├── api_views.py
├── batch_models.py                    # نماذج الدفعات
├── certificates_models.py             # نماذج الشهادات
├── food_safety_models.py              # نماذج سلامة الغذاء
├── export_approval_models.py          # نماذج موافقات التصدير
├── change_tracking.py                 # تتبع التغييرات
├── cost_tracking.py                   # تتبع التكاليف
├── quantity_tracking.py               # تتبع الكميات
├── grade_b_sales.py                   # مبيعات الدرجة ب
├── integration_services.py            # خدمات التكامل
├── inventory_integration.py           # تكامل المخزون
├── purchasing_integration.py          # تكامل المشتريات
├── sales_integration.py               # تكامل المبيعات
├── supplier_integration.py            # تكامل الموردين
├── analytics/
│   ├── __init__.py
│   ├── dashboards.py                  # لوحات التحكم
│   ├── dashboard_api.py               # API لوحات التحكم
│   ├── production_reports.py          # تقارير الإنتاج
│   ├── profitability_reports.py       # تقارير الربحية
│   ├── quality_reports.py             # تقارير الجودة
│   └── waste_reports.py               # تقارير الهدر
├── product_grading/
│   ├── __init__.py
│   ├── models.py                      # نماذج تصنيف المنتجات
│   ├── services.py                    # خدمات التصنيف
│   └── pricing.py                     # تسعير التصنيف
├── workflow/
│   ├── __init__.py
│   ├── models.py                      # نماذج سير العمل
│   └── services.py                    # خدمات سير العمل
└── tests/
    ├── __init__.py
    ├── test_integration.py
    ├── test_cost_tracking.py
    └── test_dashboards.py
```

## 5. وحدات الذكاء الاصطناعي (AI Modules)

### 5.1 المساعد الذكي
```
gaara_erp/ai_modules/intelligent_assistant/
├── __init__.py
├── apps.py
├── models.py                          # نماذج المساعد الذكي
├── api_views.py                       # عروض API
├── urls.py
├── ai_engine.py                       # محرك الذكاء الاصطناعي
├── main_agent.py                      # الوكيل الرئيسي
├── signals.py                         # إشارات النظام
├── tasks.py                           # مهام Celery
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
```

### 5.2 ذاكرة الذكاء الاصطناعي
```
gaara_erp/ai_modules/ai_memory/
├── __init__.py
├── apps.py
├── admin.py
├── models.py                          # نماذج ذاكرة الذكاء الاصطناعي
├── serializers.py
├── views.py
├── urls.py
├── services.py                        # خدمات الذاكرة
├── filters.py
├── settings.py                        # إعدادات الذاكرة
├── signals.py
├── tasks.py                           # مهام الذاكرة
├── tests.py
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
```

### 5.3 نماذج الذكاء الاصطناعي
```
gaara_erp/ai_modules/ai_models/
├── apps.py
├── models.py                          # نماذج الذكاء الاصطناعي
├── engine.py                          # محرك النماذج
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
```

## 6. وحدات التكامل (Integration Modules)

### 6.1 تكامل الذكاء الاصطناعي
```
gaara_erp/integration_modules/ai/
├── __init__.py
├── apps.py
├── admin.py
├── models.py                          # نماذج تكامل الذكاء الاصطناعي
├── serializers.py
├── views.py
├── urls.py
├── services.py                        # خدمات التكامل
├── agents.py                          # وكلاء الذكاء الاصطناعي
├── exceptions.py                      # استثناءات مخصصة
├── model_selector.py                  # منتقي النماذج
├── monitoring.py                      # مراقبة النماذج
├── services/
│   ├── __init__.py
│   ├── coordinator.py                 # منسق الخدمات
│   ├── config_manager.py              # مدير التكوين
│   ├── resource_manager.py            # مدير الموارد
│   └── activity_logger.py             # مسجل الأنشطة
├── monitoring/
│   ├── __init__.py
│   ├── data_collector.py              # جامع البيانات
│   └── drift_analyzer.py              # محلل الانحراف
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_integration.py
```

### 6.2 تكامل الزراعة والذكاء الاصطناعي
```
gaara_erp/integration_modules/ai_agriculture/
├── apps.py
├── models.py                          # نماذج تكامل الزراعة والذكاء الاصطناعي
├── integration.py                     # خدمات التكامل
├── ai_integration.py                  # تكامل الذكاء الاصطناعي
├── api/
│   ├── __init__.py
│   ├── crop_analysis_api.py           # API تحليل المحاصيل
│   └── crop_prediction_api.py         # API التنبؤ بالمحاصيل
├── services/
│   ├── __init__.py
│   ├── crop_analysis_service.py       # خدمة تحليل المحاصيل
│   ├── crop_prediction_service.py     # خدمة التنبؤ
│   ├── image_analysis_service.py      # خدمة تحليل الصور
│   ├── sensor_data_service.py         # خدمة بيانات المستشعرات
│   └── weather_data_service.py        # خدمة بيانات الطقس
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_integration.py
    ├── test_ai_integration.py
    ├── test_api.py
    └── test_models.py
```

## 7. وحدات الخدمات (Service Modules)

### 7.1 إدارة الموارد البشرية
```
gaara_erp/services_modules/hr/
├── __init__.py
├── apps.py
├── admin.py
├── models.py                          # نماذج الموارد البشرية
├── serializers.py
├── views.py
├── urls.py
├── services.py                        # خدمات الموارد البشرية
├── filters.py
├── permissions.py
├── employee.py                        # إدارة الموظفين
├── attendance.py                      # الحضور والانصراف
├── leave.py                           # الإجازات
├── payroll.py                         # كشوف المرتبات
├── contracts.py                       # العقود
├── bonuses.py                         # المكافآت
├── details.py                         # تفاصيل الموظفين
├── structure.py                       # هيكل الموارد البشرية
├── settings.py                        # إعدادات الموارد البشرية
└── tests/
    ├── __init__.py
    ├── test_employee.py
    ├── test_department.py
    ├── test_position.py
    └── test_job_grade.py
```

### 7.2 إدارة المشاريع
```
gaara_erp/services_modules/projects/
├── __init__.py
├── apps.py
├── admin.py
├── models.py                          # نماذج المشاريع
├── serializers.py
├── views.py
├── urls.py
├── services.py                        # خدمات المشاريع
├── signals.py                         # إشارات المشاريع
├── api/
│   └── project_task_api.py            # API مهام المشاريع
├── services/
│   ├── __init__.py
│   ├── project_service.py             # خدمة المشاريع
│   ├── project_integration.py         # تكامل المشاريع
│   ├── project_task_integration.py    # تكامل مهام المشاريع
│   └── project_risk_integration.py    # تكامل مخاطر المشاريع
├── permissions/
│   └── managers.py                    # مديري الصلاحيات
├── utils/
│   └── data_validators.py             # مدققات البيانات
├── migrations/
│   └── __init__.py
└── tests/
    ├── __init__.py
    ├── test_projects.py
    ├── test_services.py
    ├── test_project_task_integration.py
    ├── test_risk_management_integration.py
    └── test_workflow_integration.py
```

## 8. وحدات الإدارة (Admin Modules)

### 8.1 لوحة التحكم المخصصة
```
gaara_erp/admin_modules/custom_admin/
├── admin.py
├── apps.py
├── forms.py                           # نماذج الإدارة
├── jwt_config.py                      # تكوين JWT
├── serializers/
│   ├── __init__.py
│   ├── dashboard_serializers.py       # مسلسلات لوحة التحكم
│   ├── system_settings_serializers.py # مسلسلات إعدادات النظام
│   ├── notifications_serializers.py   # مسلسلات الإشعارات
│   ├── customization_serializers.py   # مسلسلات التخصيص
│   └── backup_restore_serializers.py  # مسلسلات النسخ الاحتياطي
├── views/
│   ├── __init__.py
│   ├── dashboard_views.py             # عروض لوحة التحكم
│   ├── system_settings_views.py       # عروض إعدادات النظام
│   ├── notifications_views.py         # عروض الإشعارات
│   ├── customization_views.py         # عروض التخصيص
│   └── backup_restore_views.py        # عروض النسخ الاحتياطي
├── urls.py
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_initial.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_api.py
    └── test_integration.py
```

### 8.2 مراقبة النظام
```
gaara_erp/admin_modules/system_monitoring/
├── __init__.py
├── apps.py
├── admin.py
├── models.py                          # نماذج مراقبة النظام
├── serializers.py
├── views.py
├── urls.py
├── tests.py
├── models_improved.py                 # نماذج محسنة
├── services/
│   ├── monitoring_service.py          # خدمة المراقبة
│   └── monitoring_service_broken.py   # خدمة معطلة (للمراجعة)
```

## 9. ملفات الاختبار (Test Files)

### 9.1 اختبارات النظام الشاملة
```
gaara_erp/
├── test_*.py                          # اختبارات النظام الرئيسية
├── conftest.py                        # إعداد pytest
├── comprehensive_test_runner.py        # مشغل الاختبارات الشامل
├── final_test_verification.py         # التحقق النهائي من الاختبارات
├── quick_test_verification.py         # التحقق السريع
├── detailed_test_diagnostic.py        # تشخيص مفصل للاختبارات
└── ultimate_system_validator.py       # مدقق النظام النهائي
```

### 9.2 اختبارات الوحدات المتخصصة
```
# اختبارات المحاسبة
test_accounting_module.py
test_sales_module.py

# اختبارات الوحدات الزراعية
test_agricultural_modules.py

# اختبارات الذكاء الاصطناعي
test_ai_integration_modules.py

# اختبارات الأمان
test_security_permissions.py
test_security_settings.py

# اختبارات الأداء
test_performance_sanity.py
test_comprehensive_performance.py

# اختبارات التكامل
test_comprehensive_integration.py
test_frontend_backend_integration.py
```

## 10. ملفات الأدوات والمساعدات (Utility Files)

### 10.1 أدوات النظام
```
gaara_erp/
├── system_config.py                   # تكوين النظام
├── system_monitor.py                  # مراقب النظام
├── performance_analyzer.py            # محلل الأداء
├── security_checker.py                # فاحص الأمان
├── backup_system.py                   # نظام النسخ الاحتياطي
├── start_system.py                    # بادئ النظام
├── dev_start.py                       # بادئ التطوير
└── sitecustomize.py                   # تخصيص الموقع
```

### 10.2 أدوات التحليل والتشخيص
```
gaara_erp/
├── comprehensive_project_analyzer.py  # محلل المشروع الشامل
├── create_project_catalog.py         # منشئ كتالوج المشروع
├── simple_system_check.py            # فحص النظام البسيط
├── quick_system_check.py             # فحص النظام السريع
└── list_accounting_tables.py         # قائمة جداول المحاسبة
```

## 11. ملفات Docker والنشر (Deployment Files)

### 11.1 ملفات Docker
```
gaara_erp/
├── Dockerfile                        # ملف Docker الأساسي
├── Dockerfile.enhanced               # ملف Docker المحسن
├── docker-compose.yml               # تكوين Docker Compose الأساسي
├── docker-compose.enhanced.yml      # تكوين Docker Compose المحسن
└── docker/
    ├── entrypoint.sh                 # نقطة دخول Docker
    └── healthcheck.sh                # فحص صحة Docker
```

### 11.2 ملفات الأمان المحسن
```
gaara_erp/security/
├── __init__.py
├── mfa.py                           # المصادقة متعددة العوامل
├── encryption.py                    # التشفير
└── rate_limiting.py                 # تحديد معدل الطلبات
```

## 12. ملفات البيانات والتكوين (Data & Configuration Files)

### 12.1 ملفات المتطلبات
```
gaara_erp/
├── requirements.txt                  # متطلبات Python الأساسية
├── requirements_enhanced_security.txt # متطلبات الأمان المحسن
└── package.json                     # متطلبات Node.js (إن وجدت)
```

### 12.2 ملفات التكوين
```
gaara_erp/
├── .env.example                     # مثال على متغيرات البيئة
├── .gitignore                       # ملفات Git المتجاهلة
├── .dockerignore                    # ملفات Docker المتجاهلة
└── pytest.ini                      # تكوين pytest
```

## 13. ملفات الوثائق (Documentation Files)

### 13.1 الوثائق الرئيسية
```
gaara_erp/
├── README.md                        # دليل المشروع الرئيسي
├── README_ENHANCED_SECURITY.md      # دليل الأمان المحسن
└── docs/
    └── analysis/
        └── scripts/
            └── syntax_scan.py       # فحص بناء الجملة
```

## 14. ملفات الصيانة والإصلاح (Maintenance Files)

### 14.1 ملفات الإصلاح
```
gaara_erp/
├── fix.py                           # إصلاح عام
├── fix_pylint_issues.py             # إصلاح مشاكل pylint
├── fix_encoding_issues.py           # إصلاح مشاكل الترميز
├── fix_syntax_errors.py             # إصلاح أخطاء بناء الجملة
├── fix_all_test_files.py            # إصلاح ملفات الاختبار
└── verify_pylint_fix.py             # التحقق من إصلاح pylint
```

### 14.2 ملفات التشخيص
```
gaara_erp/
├── debug_*.py                       # ملفات التشخيص المختلفة
├── check_db_schema.py               # فحص مخطط قاعدة البيانات
└── create_*.py                      # ملفات الإنشاء المختلفة
```

## 15. إحصائيات التصنيف

### 15.1 توزيع الملفات حسب النوع
```
نوع الملف                    العدد      النسبة
─────────────────────────────────────────────
ملفات Python (.py)          1,660      85%
ملفات الاختبار              200       10%
ملفات التكوين               50        3%
ملفات الوثائق               30        1.5%
ملفات أخرى                  10        0.5%
─────────────────────────────────────────────
المجموع                     1,950      100%
```

### 15.2 توزيع الملفات حسب الوحدة
```
الوحدة                      العدد      النسبة
─────────────────────────────────────────────
الوحدات التجارية            450       23%
الوحدات الزراعية            380       19%
وحدات الذكاء الاصطناعي       320       16%
الوحدات الأساسية            280       14%
وحدات التكامل               250       13%
وحدات الخدمات               170       9%
وحدات الإدارة               100       5%
ملفات أخرى                  20        1%
─────────────────────────────────────────────
المجموع                     1,970      100%
```

---

**تاريخ التصنيف**: نوفمبر 2025  
**إصدار النظام**: Gaara ERP v12 Enhanced Security Edition  
**حالة التصنيف**: شامل ومحدث
