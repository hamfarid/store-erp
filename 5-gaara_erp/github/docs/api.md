# توثيق API الشامل - Gaara ERP v12

## نظرة عامة
توثيق شامل لجميع نقاط النهاية (API Endpoints) في نظام Gaara ERP v12 مع الطرق والأوصاف التفصيلية.

## معلومات عامة عن API

### Base URL
```
Production: https://api.gaara-erp.com/v1
Development: http://localhost:8000/api/v1
```

### Authentication
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Accept: application/json
```

### Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "errors": [],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## 1. APIs المصادقة والمستخدمين (Authentication & Users)

### 1.1 المصادقة
```http
POST   /auth/login/                    # تسجيل الدخول
POST   /auth/logout/                   # تسجيل الخروج
POST   /auth/refresh/                  # تجديد الرمز المميز
POST   /auth/register/                 # تسجيل مستخدم جديد
POST   /auth/forgot-password/          # نسيان كلمة المرور
POST   /auth/reset-password/           # إعادة تعيين كلمة المرور
POST   /auth/verify-email/             # التحقق من البريد الإلكتروني
POST   /auth/mfa/setup/                # إعداد المصادقة متعددة العوامل
POST   /auth/mfa/verify/               # التحقق من MFA
```

### 1.2 إدارة المستخدمين
```http
GET    /users/                         # قائمة المستخدمين
POST   /users/                         # إنشاء مستخدم جديد
GET    /users/{id}/                    # تفاصيل مستخدم
PUT    /users/{id}/                    # تحديث مستخدم
DELETE /users/{id}/                    # حذف مستخدم
GET    /users/profile/                 # ملف المستخدم الحالي
PUT    /users/profile/                 # تحديث الملف الشخصي
POST   /users/{id}/activate/           # تفعيل مستخدم
POST   /users/{id}/deactivate/         # إلغاء تفعيل مستخدم
```

### 1.3 الأدوار والصلاحيات
```http
GET    /roles/                         # قائمة الأدوار
POST   /roles/                         # إنشاء دور جديد
GET    /roles/{id}/                    # تفاصيل دور
PUT    /roles/{id}/                    # تحديث دور
DELETE /roles/{id}/                    # حذف دور
GET    /permissions/                   # قائمة الصلاحيات
POST   /users/{id}/assign-role/        # تعيين دور لمستخدم
DELETE /users/{id}/remove-role/        # إزالة دور من مستخدم
```

## 2. APIs المحاسبة (Accounting)

### 2.1 إدارة الحسابات
```http
GET    /accounting/accounts/            # قائمة الحسابات
POST   /accounting/accounts/            # إنشاء حساب جديد
GET    /accounting/accounts/{id}/       # تفاصيل حساب
PUT    /accounting/accounts/{id}/       # تحديث حساب
DELETE /accounting/accounts/{id}/       # حذف حساب
GET    /accounting/accounts/tree/       # شجرة الحسابات
GET    /accounting/accounts/balance/    # أرصدة الحسابات
```

### 2.2 دفاتر اليومية
```http
GET    /accounting/journals/            # قائمة دفاتر اليومية
POST   /accounting/journals/            # إنشاء دفتر يومية
GET    /accounting/journals/{id}/       # تفاصيل دفتر يومية
PUT    /accounting/journals/{id}/       # تحديث دفتر يومية
DELETE /accounting/journals/{id}/       # حذف دفتر يومية
```

### 2.3 قيود اليومية
```http
GET    /accounting/journal-entries/     # قائمة قيود اليومية
POST   /accounting/journal-entries/     # إنشاء قيد يومية
GET    /accounting/journal-entries/{id}/ # تفاصيل قيد يومية
PUT    /accounting/journal-entries/{id}/ # تحديث قيد يومية
DELETE /accounting/journal-entries/{id}/ # حذف قيد يومية
POST   /accounting/journal-entries/{id}/post/ # ترحيل قيد
POST   /accounting/journal-entries/{id}/unpost/ # إلغاء ترحيل
```

### 2.4 التقارير المالية
```http
GET    /accounting/reports/trial-balance/     # ميزان المراجعة
GET    /accounting/reports/balance-sheet/     # الميزانية العمومية
GET    /accounting/reports/income-statement/  # قائمة الدخل
GET    /accounting/reports/cash-flow/         # التدفق النقدي
GET    /accounting/reports/general-ledger/    # دفتر الأستاذ العام
GET    /accounting/reports/aged-receivables/  # أعمار الذمم المدينة
GET    /accounting/reports/aged-payables/     # أعمار الذمم الدائنة
```

### 2.5 الضرائب والدفع
```http
GET    /accounting/taxes/               # قائمة الضرائب
POST   /accounting/taxes/               # إنشاء ضريبة جديدة
GET    /accounting/taxes/{id}/          # تفاصيل ضريبة
PUT    /accounting/taxes/{id}/          # تحديث ضريبة
DELETE /accounting/taxes/{id}/          # حذف ضريبة
GET    /accounting/payment-terms/       # شروط الدفع
POST   /accounting/payment-terms/       # إنشاء شرط دفع جديد
```

## 3. APIs المخزون (Inventory)

### 3.1 إدارة المنتجات
```http
GET    /inventory/products/             # قائمة المنتجات
POST   /inventory/products/             # إنشاء منتج جديد
GET    /inventory/products/{id}/        # تفاصيل منتج
PUT    /inventory/products/{id}/        # تحديث منتج
DELETE /inventory/products/{id}/        # حذف منتج
GET    /inventory/products/search/      # البحث في المنتجات
POST   /inventory/products/bulk-import/ # استيراد مجمع للمنتجات
```

### 3.2 فئات المنتجات
```http
GET    /inventory/categories/           # قائمة فئات المنتجات
POST   /inventory/categories/           # إنشاء فئة جديدة
GET    /inventory/categories/{id}/      # تفاصيل فئة
PUT    /inventory/categories/{id}/      # تحديث فئة
DELETE /inventory/categories/{id}/      # حذف فئة
GET    /inventory/categories/tree/      # شجرة الفئات
```

### 3.3 إدارة المستودعات
```http
GET    /inventory/warehouses/           # قائمة المستودعات
POST   /inventory/warehouses/           # إنشاء مستودع جديد
GET    /inventory/warehouses/{id}/      # تفاصيل مستودع
PUT    /inventory/warehouses/{id}/      # تحديث مستودع
DELETE /inventory/warehouses/{id}/      # حذف مستودع
GET    /inventory/warehouses/{id}/stock/ # مخزون المستودع
```

### 3.4 حركات المخزون
```http
GET    /inventory/stock-moves/          # قائمة حركات المخزون
POST   /inventory/stock-moves/          # إنشاء حركة مخزون
GET    /inventory/stock-moves/{id}/     # تفاصيل حركة مخزون
PUT    /inventory/stock-moves/{id}/     # تحديث حركة مخزون
POST   /inventory/stock-moves/{id}/confirm/ # تأكيد حركة المخزون
POST   /inventory/stock-moves/{id}/cancel/  # إلغاء حركة المخزون
```

### 3.5 الجرد والتقارير
```http
GET    /inventory/stock-levels/         # مستويات المخزون
GET    /inventory/stock-valuation/      # تقييم المخزون
POST   /inventory/physical-inventory/   # الجرد الفعلي
GET    /inventory/reports/stock-aging/  # تقرير أعمار المخزون
GET    /inventory/reports/movement/     # تقرير حركة المخزون
GET    /inventory/reports/reorder/      # تقرير إعادة الطلب
```

## 4. APIs المبيعات (Sales)

### 4.1 إدارة العملاء
```http
GET    /sales/customers/                # قائمة العملاء
POST   /sales/customers/                # إنشاء عميل جديد
GET    /sales/customers/{id}/           # تفاصيل عميل
PUT    /sales/customers/{id}/           # تحديث عميل
DELETE /sales/customers/{id}/           # حذف عميل
GET    /sales/customers/{id}/orders/    # أوامر العميل
GET    /sales/customers/{id}/invoices/  # فواتير العميل
```

### 4.2 أوامر البيع
```http
GET    /sales/orders/                   # قائمة أوامر البيع
POST   /sales/orders/                   # إنشاء أمر بيع جديد
GET    /sales/orders/{id}/              # تفاصيل أمر البيع
PUT    /sales/orders/{id}/              # تحديث أمر البيع
DELETE /sales/orders/{id}/              # حذف أمر البيع
POST   /sales/orders/{id}/confirm/      # تأكيد أمر البيع
POST   /sales/orders/{id}/cancel/       # إلغاء أمر البيع
POST   /sales/orders/{id}/deliver/      # تسليم أمر البيع
```

### 4.3 عروض الأسعار
```http
GET    /sales/quotations/               # قائمة عروض الأسعار
POST   /sales/quotations/               # إنشاء عرض سعر جديد
GET    /sales/quotations/{id}/          # تفاصيل عرض السعر
PUT    /sales/quotations/{id}/          # تحديث عرض السعر
DELETE /sales/quotations/{id}/          # حذف عرض السعر
POST   /sales/quotations/{id}/send/     # إرسال عرض السعر
POST   /sales/quotations/{id}/convert/  # تحويل إلى أمر بيع
```

### 4.4 الفواتير والدفع
```http
GET    /sales/invoices/                 # قائمة فواتير البيع
POST   /sales/invoices/                 # إنشاء فاتورة بيع
GET    /sales/invoices/{id}/            # تفاصيل فاتورة البيع
PUT    /sales/invoices/{id}/            # تحديث فاتورة البيع
POST   /sales/invoices/{id}/send/       # إرسال الفاتورة
POST   /sales/invoices/{id}/pay/        # تسجيل دفعة
GET    /sales/payments/                 # قائمة المدفوعات
```

## 5. APIs المشتريات (Purchasing)

### 5.1 إدارة الموردين
```http
GET    /purchasing/suppliers/           # قائمة الموردين
POST   /purchasing/suppliers/           # إنشاء مورد جديد
GET    /purchasing/suppliers/{id}/      # تفاصيل مورد
PUT    /purchasing/suppliers/{id}/      # تحديث مورد
DELETE /purchasing/suppliers/{id}/      # حذف مورد
GET    /purchasing/suppliers/{id}/orders/ # أوامر المورد
```

### 5.2 أوامر الشراء
```http
GET    /purchasing/orders/              # قائمة أوامر الشراء
POST   /purchasing/orders/              # إنشاء أمر شراء جديد
GET    /purchasing/orders/{id}/         # تفاصيل أمر الشراء
PUT    /purchasing/orders/{id}/         # تحديث أمر الشراء
DELETE /purchasing/orders/{id}/         # حذف أمر الشراء
POST   /purchasing/orders/{id}/confirm/ # تأكيد أمر الشراء
POST   /purchasing/orders/{id}/receive/ # استلام أمر الشراء
```

### 5.3 طلبات الشراء
```http
GET    /purchasing/requisitions/        # قائمة طلبات الشراء
POST   /purchasing/requisitions/        # إنشاء طلب شراء جديد
GET    /purchasing/requisitions/{id}/   # تفاصيل طلب الشراء
PUT    /purchasing/requisitions/{id}/   # تحديث طلب الشراء
POST   /purchasing/requisitions/{id}/approve/ # الموافقة على الطلب
POST   /purchasing/requisitions/{id}/convert/ # تحويل إلى أمر شراء
```

### 5.4 الاستلام والفواتير
```http
GET    /purchasing/receipts/            # قائمة إيصالات الاستلام
POST   /purchasing/receipts/            # إنشاء إيصال استلام
GET    /purchasing/receipts/{id}/       # تفاصيل إيصال الاستلام
GET    /purchasing/invoices/            # قائمة فواتير الشراء
POST   /purchasing/invoices/            # إنشاء فاتورة شراء
POST   /purchasing/invoices/{id}/pay/   # دفع فاتورة الشراء
```

## 6. APIs الزراعة (Agricultural)

### 6.1 إدارة المزارع
```http
GET    /agricultural/farms/             # قائمة المزارع
POST   /agricultural/farms/             # إنشاء مزرعة جديدة
GET    /agricultural/farms/{id}/        # تفاصيل مزرعة
PUT    /agricultural/farms/{id}/        # تحديث مزرعة
DELETE /agricultural/farms/{id}/        # حذف مزرعة
GET    /agricultural/farms/{id}/fields/ # حقول المزرعة
GET    /agricultural/farms/{id}/crops/  # محاصيل المزرعة
```

### 6.2 إدارة المحاصيل
```http
GET    /agricultural/crops/             # قائمة المحاصيل
POST   /agricultural/crops/             # إنشاء محصول جديد
GET    /agricultural/crops/{id}/        # تفاصيل محصول
PUT    /agricultural/crops/{id}/        # تحديث محصول
DELETE /agricultural/crops/{id}/        # حذف محصول
GET    /agricultural/crops/{id}/stages/ # مراحل نمو المحصول
POST   /agricultural/crops/{id}/harvest/ # حصاد المحصول
```

### 6.3 تشخيص النباتات
```http
POST   /agricultural/plant-diagnosis/   # تشخيص نبات بالصورة
GET    /agricultural/diagnosis-history/ # تاريخ التشخيصات
GET    /agricultural/diagnosis/{id}/    # تفاصيل تشخيص
POST   /agricultural/diagnosis/{id}/treatment/ # علاج مقترح
GET    /agricultural/diseases/          # قائمة الأمراض
GET    /agricultural/treatments/        # قائمة العلاجات
```

### 6.4 البحوث والتجارب
```http
GET    /agricultural/experiments/       # قائمة التجارب
POST   /agricultural/experiments/       # إنشاء تجربة جديدة
GET    /agricultural/experiments/{id}/  # تفاصيل تجربة
PUT    /agricultural/experiments/{id}/  # تحديث تجربة
POST   /agricultural/experiments/{id}/results/ # نتائج التجربة
GET    /agricultural/research-projects/ # مشاريع البحث
POST   /agricultural/research-projects/ # إنشاء مشروع بحث جديد
```

### 6.5 تهجين البذور
```http
GET    /agricultural/seed-hybridization/ # قائمة تهجين البذور
POST   /agricultural/seed-hybridization/ # إنشاء عملية تهجين
GET    /agricultural/seed-hybridization/{id}/ # تفاصيل التهجين
PUT    /agricultural/seed-hybridization/{id}/ # تحديث التهجين
GET    /agricultural/variety-trials/    # تجارب الأصناف
POST   /agricultural/variety-trials/    # إنشاء تجربة صنف جديد
```

## 7. APIs الذكاء الاصطناعي (AI)

### 7.1 المساعد الذكي
```http
POST   /ai/chat/                        # محادثة مع المساعد الذكي
GET    /ai/conversation-history/        # تاريخ المحادثات
POST   /ai/analyze-data/                # تحليل البيانات بالذكاء الاصطناعي
POST   /ai/generate-report/             # إنتاج تقرير ذكي
POST   /ai/predict/                     # التنبؤ بالبيانات
GET    /ai/suggestions/                 # اقتراحات ذكية
```

### 7.2 إدارة النماذج
```http
GET    /ai/models/                      # قائمة نماذج الذكاء الاصطناعي
POST   /ai/models/                      # إنشاء نموذج جديد
GET    /ai/models/{id}/                 # تفاصيل نموذج
PUT    /ai/models/{id}/                 # تحديث نموذج
DELETE /ai/models/{id}/                 # حذف نموذج
POST   /ai/models/{id}/train/           # تدريب نموذج
GET    /ai/models/{id}/performance/     # أداء النموذج
```

### 7.3 تحليلات الذكاء الاصطناعي
```http
GET    /ai/analytics/usage/             # تحليلات استخدام الذكاء الاصطناعي
GET    /ai/analytics/performance/       # تحليلات أداء النماذج
GET    /ai/analytics/accuracy/          # دقة النماذج
GET    /ai/analytics/trends/            # اتجاهات البيانات
POST   /ai/analytics/custom-report/     # تقرير مخصص
```

### 7.4 ذاكرة الذكاء الاصطناعي
```http
GET    /ai/memory/                      # ذاكرة الذكاء الاصطناعي
POST   /ai/memory/                      # إضافة ذكرى جديدة
GET    /ai/memory/{id}/                 # تفاصيل ذكرى
PUT    /ai/memory/{id}/                 # تحديث ذكرى
DELETE /ai/memory/{id}/                 # حذف ذكرى
POST   /ai/memory/search/               # البحث في الذاكرة
```

## 8. APIs الإدارة والإعدادات (Administration)

### 8.1 إعدادات النظام
```http
GET    /admin/settings/                 # إعدادات النظام
PUT    /admin/settings/                 # تحديث الإعدادات
GET    /admin/settings/company/         # إعدادات الشركة
PUT    /admin/settings/company/         # تحديث إعدادات الشركة
GET    /admin/settings/localization/    # إعدادات التوطين
PUT    /admin/settings/localization/    # تحديث التوطين
```

### 8.2 النسخ الاحتياطي والاستعادة
```http
POST   /admin/backup/create/            # إنشاء نسخة احتياطية
GET    /admin/backup/list/              # قائمة النسخ الاحتياطية
POST   /admin/backup/restore/           # استعادة نسخة احتياطية
DELETE /admin/backup/{id}/              # حذف نسخة احتياطية
GET    /admin/backup/{id}/download/     # تحميل نسخة احتياطية
```

### 8.3 مراقبة النظام
```http
GET    /admin/system/health/            # صحة النظام
GET    /admin/system/performance/       # أداء النظام
GET    /admin/system/logs/              # سجلات النظام
GET    /admin/system/statistics/        # إحصائيات النظام
POST   /admin/system/maintenance/       # وضع الصيانة
```

### 8.4 إدارة البيانات
```http
POST   /admin/data/import/              # استيراد البيانات
POST   /admin/data/export/              # تصدير البيانات
GET    /admin/data/templates/           # قوالب البيانات
POST   /admin/data/validate/            # التحقق من صحة البيانات
POST   /admin/data/cleanup/             # تنظيف البيانات
```

## 9. APIs التقارير (Reports)

### 9.1 التقارير المالية
```http
GET    /reports/financial/summary/      # ملخص مالي
GET    /reports/financial/detailed/     # تقرير مالي مفصل
GET    /reports/financial/comparison/   # مقارنة مالية
POST   /reports/financial/custom/       # تقرير مالي مخصص
```

### 9.2 تقارير المخزون
```http
GET    /reports/inventory/stock/        # تقرير المخزون
GET    /reports/inventory/movement/     # تقرير حركة المخزون
GET    /reports/inventory/valuation/    # تقرير تقييم المخزون
GET    /reports/inventory/aging/        # تقرير أعمار المخزون
```

### 9.3 تقارير المبيعات
```http
GET    /reports/sales/summary/          # ملخص المبيعات
GET    /reports/sales/detailed/         # تقرير مبيعات مفصل
GET    /reports/sales/customer/         # تقرير العملاء
GET    /reports/sales/product/          # تقرير المنتجات
```

### 9.4 التقارير الزراعية
```http
GET    /reports/agricultural/production/ # تقرير الإنتاج الزراعي
GET    /reports/agricultural/yield/     # تقرير الإنتاجية
GET    /reports/agricultural/costs/     # تقرير التكاليف الزراعية
GET    /reports/agricultural/weather/   # تقرير الطقس
```

## 10. APIs الإشعارات والتنبيهات (Notifications)

### 10.1 الإشعارات
```http
GET    /notifications/                  # قائمة الإشعارات
POST   /notifications/                  # إنشاء إشعار جديد
GET    /notifications/{id}/             # تفاصيل إشعار
PUT    /notifications/{id}/read/        # تحديد إشعار كمقروء
DELETE /notifications/{id}/             # حذف إشعار
POST   /notifications/mark-all-read/    # تحديد جميع الإشعارات كمقروءة
```

### 10.2 التنبيهات
```http
GET    /alerts/                         # قائمة التنبيهات
POST   /alerts/                         # إنشاء تنبيه جديد
GET    /alerts/{id}/                    # تفاصيل تنبيه
PUT    /alerts/{id}/                    # تحديث تنبيه
DELETE /alerts/{id}/                    # حذف تنبيه
POST   /alerts/{id}/acknowledge/        # الإقرار بالتنبيه
```

## رموز الاستجابة (Response Codes)

### رموز النجاح
- **200 OK**: طلب ناجح
- **201 Created**: تم إنشاء المورد بنجاح
- **204 No Content**: طلب ناجح بدون محتوى

### رموز الأخطاء
- **400 Bad Request**: طلب غير صحيح
- **401 Unauthorized**: غير مصرح
- **403 Forbidden**: ممنوع
- **404 Not Found**: غير موجود
- **422 Unprocessable Entity**: بيانات غير صالحة
- **500 Internal Server Error**: خطأ في الخادم

## أمثلة على الاستخدام

### مثال: إنشاء منتج جديد
```http
POST /api/v1/inventory/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "name": "طماطم حمراء",
  "code": "TOM001",
  "category_id": 1,
  "unit_price": 5.50,
  "cost_price": 3.00,
  "description": "طماطم حمراء طازجة عالية الجودة",
  "unit_of_measure": "كيلوجرام",
  "barcode": "1234567890123"
}
```

### مثال: البحث في المنتجات
```http
GET /api/v1/inventory/products/?search=طماطم&category=1&page=1&per_page=20
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### مثال: إنشاء قيد يومية
```http
POST /api/v1/accounting/journal-entries/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "journal_id": 1,
  "date": "2025-11-01",
  "reference": "JE001",
  "description": "قيد بيع بضاعة",
  "lines": [
    {
      "account_id": 101,
      "debit": 1000.00,
      "credit": 0.00,
      "description": "النقدية"
    },
    {
      "account_id": 401,
      "debit": 0.00,
      "credit": 1000.00,
      "description": "المبيعات"
    }
  ]
}
```

---

**تاريخ التوثيق**: نوفمبر 2025  
**إصدار API**: v1.0  
**إجمالي Endpoints**: 157+ نقطة نهاية
