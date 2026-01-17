# /speckit.tasks - قائمة المهام الشاملة

## 📅 التاريخ: 2026-01-16

---

# 🔴 المرحلة 1: إصلاح الأخطاء الحرجة (233 خطأ)

## 📊 توزيع الأخطاء

| النوع | العدد | النسبة | الوصف |
|-------|-------|--------|-------|
| **F821** | ~140 | 60% | متغيرات/دوال غير معرفة (Undefined Name) |
| **F811** | ~82 | 35% | إعادة تعريف (Redefinition) |
| **E9** | ~11 | 5% | أخطاء صياغة (Syntax Error) |

---

## 🔧 مهام إصلاح الأخطاء

### Task 1.1: إصلاح أخطاء E9 (Syntax Errors) - الأولوية القصوى
**الحالة:** ⏳ قيد التنفيذ

| الملف | السطر | الخطأ |
|-------|-------|-------|
| `agricultural_modules/production/workflow/models.py` | 231 | IndentationError |

**الإجراء:** إصلاح المسافات البادئة

---

### Task 1.2: إصلاح أخطاء F821 في ملفات الاختبارات
**الحالة:** ⏳ قيد التنفيذ

| الملف | عدد الأخطاء | الـ imports المفقودة |
|-------|-------------|---------------------|
| `business_modules/contacts/tests/test_contacts.py` | 25 | CommunicationLog, CommunicationType |
| `business_modules/contacts/tests/test_models.py` | 15 | PaymentMethod, ContactType, SupplierContactPerson |
| `business_modules/contacts/tests/test_settlement_logic.py` | 10 | SettlementService, SettlementTransaction |
| `business_modules/accounting/tests/test_account_service.py` | 10 | JournalEntry, JournalItem |
| `agricultural_modules/farms/tests/test_integration.py` | 2 | AgriculturalActivityTypeService |

**الإجراء:** إضافة الـ imports المفقودة

---

### Task 1.3: إصلاح أخطاء F811 (Redefinition)
**الحالة:** ⏳ قيد التنفيذ

| الملف | المشكلة |
|-------|---------|
| `admin_modules/dashboard/models/__init__.py` | Meta redefinition |
| `admin_modules/data_import_export/modles/import_export_tasks.py` | json, ET, csv redefinition |
| `admin_modules/internal_diagnosis_module/models.py` | Meta redefinition |
| `admin_modules/notifications/backup_files/models.py` | Meta redefinition |
| `ai_modules/ai_memory/services.py` | objects redefinition (×8) |
| Multiple agricultural models | Meta redefinition |

**الإجراء:** إزالة التعريفات المكررة

---

# 🟢 المرحلة 2: إنشاء الواجهات الأمامية (37 مديول)

## 📁 core_modules (20 مديول) - الأولوية: عالية

### Task 2.1: Activity Log Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/activity-log/
├── ActivityLogList.jsx        # عرض سجل الأنشطة
├── ActivityLogDetails.jsx     # تفاصيل النشاط
├── ActivityLogFilters.jsx     # فلاتر البحث
└── index.jsx                  # تصدير المكونات
```

**API Endpoints:**
- `GET /api/activity-log/` - قائمة الأنشطة
- `GET /api/activity-log/{id}/` - تفاصيل نشاط

---

### Task 2.2: AI Permissions Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/ai-permissions/
├── AIPermissionsList.jsx      # قائمة صلاحيات الذكاء الاصطناعي
├── AIPermissionForm.jsx       # نموذج إضافة/تعديل
└── index.jsx
```

---

### Task 2.3: API Keys Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/api-keys/
├── APIKeysList.jsx            # قائمة المفاتيح
├── APIKeyForm.jsx             # إنشاء مفتاح جديد
├── APIKeyUsage.jsx            # إحصائيات الاستخدام
└── index.jsx
```

---

### Task 2.4: Authorization Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/authorization/
├── RolesList.jsx              # قائمة الأدوار
├── RoleForm.jsx               # نموذج الدور
├── PermissionMatrix.jsx       # مصفوفة الصلاحيات
└── index.jsx
```

---

### Task 2.5: Backup Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/backup/
├── BackupList.jsx             # قائمة النسخ الاحتياطية
├── BackupCreate.jsx           # إنشاء نسخة
├── BackupRestore.jsx          # استعادة نسخة
├── BackupSchedule.jsx         # جدولة النسخ
└── index.jsx
```

---

### Task 2.6: Companies Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/companies/
├── CompaniesList.jsx          # قائمة الشركات
├── CompanyForm.jsx            # نموذج الشركة
├── CompanyDetails.jsx         # تفاصيل الشركة
├── BranchesList.jsx           # قائمة الفروع
├── BranchForm.jsx             # نموذج الفرع
├── DepartmentsList.jsx        # قائمة الأقسام
└── index.jsx
```

---

### Task 2.7: Database Management Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/database/
├── DatabaseStatus.jsx         # حالة قاعدة البيانات
├── MigrationsList.jsx         # قائمة الترحيلات
├── OptimizationTools.jsx      # أدوات التحسين
└── index.jsx
```

---

### Task 2.8: Encryption Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/encryption/
├── EncryptionStatus.jsx       # حالة التشفير
├── KeyRotation.jsx            # تدوير المفاتيح
├── EncryptionSettings.jsx     # إعدادات التشفير
└── index.jsx
```

---

### Task 2.9: Import/Export Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/import-export/
├── ImportWizard.jsx           # معالج الاستيراد
├── ExportWizard.jsx           # معالج التصدير
├── ImportHistory.jsx          # سجل الاستيراد
├── ExportHistory.jsx          # سجل التصدير
├── TemplateManager.jsx        # إدارة القوالب
└── index.jsx
```

---

### Task 2.10: Memory Management Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/memory/
├── MemoryUsage.jsx            # استخدام الذاكرة
├── CacheManagement.jsx        # إدارة الكاش
├── MemoryOptimization.jsx     # تحسين الذاكرة
└── index.jsx
```

---

### Task 2.11: Multi-Tenancy Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/multi-tenancy/
├── TenantsList.jsx            # قائمة المستأجرين
├── TenantForm.jsx             # نموذج المستأجر
├── TenantSettings.jsx         # إعدادات المستأجر
├── TenantUsers.jsx            # مستخدمو المستأجر
└── index.jsx
```

---

### Task 2.12: Organization Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/organization/
├── OrganizationChart.jsx      # الهيكل التنظيمي
├── OrganizationSettings.jsx   # إعدادات المنظمة
└── index.jsx
```

---

### Task 2.13: Permissions Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/permissions/
├── PermissionsList.jsx        # قائمة الصلاحيات
├── PermissionForm.jsx         # نموذج الصلاحية
├── PermissionGroups.jsx       # مجموعات الصلاحيات
└── index.jsx
```

---

### Task 2.14: Permissions Manager Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/permissions-manager/
├── RolePermissions.jsx        # صلاحيات الأدوار
├── UserPermissions.jsx        # صلاحيات المستخدمين
├── ModulePermissions.jsx      # صلاحيات الوحدات
└── index.jsx
```

---

### Task 2.15: System Health Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/system-health/
├── HealthDashboard.jsx        # لوحة صحة النظام
├── ServiceStatus.jsx          # حالة الخدمات
├── HealthAlerts.jsx           # تنبيهات الصحة
└── index.jsx
```

---

### Task 2.16: System Settings Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/system-settings/
├── GeneralSettings.jsx        # الإعدادات العامة
├── SecuritySettings.jsx       # إعدادات الأمان
├── EmailSettings.jsx          # إعدادات البريد
├── NotificationSettings.jsx   # إعدادات الإشعارات
└── index.jsx
```

---

### Task 2.17: Test Management Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/tests/
├── TestRunner.jsx             # تشغيل الاختبارات
├── TestResults.jsx            # نتائج الاختبارات
├── TestCoverage.jsx           # تغطية الاختبارات
└── index.jsx
```

---

### Task 2.18: User Management Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/user-management/
├── UsersList.jsx              # قائمة المستخدمين
├── UserForm.jsx               # نموذج المستخدم
├── UserDetails.jsx            # تفاصيل المستخدم
├── UserRoles.jsx              # أدوار المستخدم
└── index.jsx
```

---

### Task 2.19: Users Accounts Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/users-accounts/
├── AccountsList.jsx           # قائمة الحسابات
├── AccountSettings.jsx        # إعدادات الحساب
├── ProfileSettings.jsx        # إعدادات الملف الشخصي
└── index.jsx
```

---

### Task 2.20: Users Permissions Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/core/users-permissions/
├── UserPermissionsList.jsx    # قائمة صلاحيات المستخدم
├── AssignPermissions.jsx      # تعيين الصلاحيات
└── index.jsx
```

---

## 📁 agricultural_modules (8 مديولات) - الأولوية: عالية

### Task 3.1: Experiments Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/agricultural/experiments/
├── ExperimentsList.jsx        # قائمة التجارب
├── ExperimentForm.jsx         # نموذج التجربة
├── ExperimentDetails.jsx      # تفاصيل التجربة
├── ExperimentResults.jsx      # نتائج التجربة
└── index.jsx
```

---

### Task 3.2: Farms Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/agricultural/farms/
├── FarmsList.jsx              # قائمة المزارع
├── FarmForm.jsx               # نموذج المزرعة
├── FarmDetails.jsx            # تفاصيل المزرعة
├── FarmMap.jsx                # خريطة المزرعة
├── FarmStatistics.jsx         # إحصائيات المزرعة
└── index.jsx
```

---

### Task 3.3: Nurseries Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/agricultural/nurseries/
├── NurseriesList.jsx          # قائمة المشاتل
├── NurseryForm.jsx            # نموذج المشتل
├── NurseryInventory.jsx       # مخزون المشتل
└── index.jsx
```

---

### Task 3.4: Production Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/agricultural/production/
├── ProductionOrders.jsx       # أوامر الإنتاج
├── ProductionTracking.jsx     # تتبع الإنتاج
├── QualityControl.jsx         # ضبط الجودة
├── Certificates.jsx           # الشهادات
└── index.jsx
```

---

### Task 3.5: Research Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/agricultural/research/
├── ResearchProjects.jsx       # مشاريع البحث
├── ResearchForm.jsx           # نموذج البحث
├── ResearchFindings.jsx       # نتائج البحث
└── index.jsx
```

---

### Task 3.6: Seed Hybridization Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/agricultural/seed-hybridization/
├── HybridizationPrograms.jsx  # برامج التهجين
├── HybridizationForm.jsx      # نموذج التهجين
├── GeneticData.jsx            # البيانات الوراثية
├── CostTracking.jsx           # تتبع التكاليف
└── index.jsx
```

---

### Task 3.7: Seed Production Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/agricultural/seed-production/
├── SeedLots.jsx               # دفعات البذور
├── SeedInventory.jsx          # مخزون البذور
├── QualityTests.jsx           # اختبارات الجودة
└── index.jsx
```

---

### Task 3.8: Variety Trials Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/agricultural/variety-trials/
├── TrialsList.jsx             # قائمة التجارب
├── TrialForm.jsx              # نموذج التجربة
├── TrialResults.jsx           # نتائج التجربة
├── ComparisonCharts.jsx       # مخططات المقارنة
└── index.jsx
```

---

## 📁 utility_modules (4 مديولات) - الأولوية: متوسطة

### Task 4.1: Health Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/utility/health/
├── HealthCheck.jsx            # فحص الصحة
├── SystemMetrics.jsx          # مقاييس النظام
└── index.jsx
```

---

### Task 4.2: Item Research Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/utility/item-research/
├── ResearchTool.jsx           # أداة البحث
├── SearchResults.jsx          # نتائج البحث
└── index.jsx
```

---

### Task 4.3: Locale Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/utility/locale/
├── LanguageSettings.jsx       # إعدادات اللغة
├── TranslationManager.jsx     # إدارة الترجمات
└── index.jsx
```

---

### Task 4.4: Utilities Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/utility/utilities/
├── UtilityTools.jsx           # أدوات مساعدة
├── DataCleanup.jsx            # تنظيف البيانات
└── index.jsx
```

---

## 📁 services_modules (2 مديول) - الأولوية: متوسطة

### Task 5.1: Archiving System Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/services/archiving/
├── ArchivesList.jsx           # قائمة الأرشيف
├── ArchiveForm.jsx            # نموذج الأرشفة
├── ArchiveSearch.jsx          # بحث الأرشيف
└── index.jsx
```

---

### Task 5.2: Compliance Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/services/compliance/
├── ComplianceChecks.jsx       # فحوصات الامتثال
├── ComplianceReports.jsx      # تقارير الامتثال
├── AuditLog.jsx               # سجل المراجعة
└── index.jsx
```

---

## 📁 admin_modules (1 مديول) - الأولوية: عالية

### Task 6.1: AI Dashboard Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/admin/ai-dashboard/
├── AIDashboard.jsx            # لوحة الذكاء الاصطناعي
├── AIMetrics.jsx              # مقاييس الذكاء الاصطناعي
├── AIModels.jsx               # نماذج الذكاء الاصطناعي
├── AIUsage.jsx                # استخدام الذكاء الاصطناعي
└── index.jsx
```

---

## 📁 business_modules (1 مديول) - الأولوية: منخفضة

### Task 7.1: Solar Station Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/business/solar-station/
├── SolarDashboard.jsx         # لوحة الطاقة الشمسية
├── PowerGeneration.jsx        # توليد الطاقة
├── MaintenanceLog.jsx         # سجل الصيانة
└── index.jsx
```

---

## 📁 ai_modules (1 مديول) - الأولوية: عالية

### Task 8.1: AI Services Frontend
**الحالة:** ⬜ معلق

**الملفات المطلوبة:**
```
frontend/src/pages/ai/services/
├── AIServicesList.jsx         # قائمة خدمات الذكاء الاصطناعي
├── AIServiceConfig.jsx        # تهيئة الخدمة
├── AIServiceLogs.jsx          # سجلات الخدمة
└── index.jsx
```

---

# 📊 ملخص المهام

| الفئة | عدد المهام | الأولوية |
|-------|-----------|---------|
| إصلاح الأخطاء | 3 | 🔴 حرجة |
| core_modules | 20 | 🟠 عالية |
| agricultural_modules | 8 | 🟠 عالية |
| utility_modules | 4 | 🟡 متوسطة |
| services_modules | 2 | 🟡 متوسطة |
| admin_modules | 1 | 🟠 عالية |
| business_modules | 1 | 🟢 منخفضة |
| ai_modules | 1 | 🟠 عالية |
| **المجموع** | **40** | - |

---

# 🚀 خطة التنفيذ

## الأسبوع 1: إصلاح الأخطاء الحرجة
- [ ] Task 1.1: إصلاح E9 Syntax Errors
- [ ] Task 1.2: إصلاح F821 في ملفات الاختبارات
- [ ] Task 1.3: إصلاح F811 Redefinitions

## الأسبوع 2-3: core_modules (الجزء 1)
- [ ] Task 2.1-2.10: أول 10 واجهات أمامية

## الأسبوع 4-5: core_modules (الجزء 2) + agricultural_modules
- [ ] Task 2.11-2.20: باقي core_modules
- [ ] Task 3.1-3.4: أول 4 واجهات زراعية

## الأسبوع 6: agricultural_modules (الجزء 2) + AI
- [ ] Task 3.5-3.8: باقي الواجهات الزراعية
- [ ] Task 6.1 + 8.1: AI Dashboard + AI Services

## الأسبوع 7: utility_modules + services_modules
- [ ] Task 4.1-4.4: utility_modules
- [ ] Task 5.1-5.2: services_modules

## الأسبوع 8: business_modules + الاختبارات
- [ ] Task 7.1: Solar Station
- [ ] اختبارات E2E لجميع الواجهات

---

*تم إنشاء هذا الملف بواسطة /speckit.tasks*
*التاريخ: 2026-01-16*
