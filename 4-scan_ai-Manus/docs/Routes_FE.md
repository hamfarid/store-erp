# مسارات الواجهة الأمامية (Frontend Routes)

هذا المستند يوثق جميع المسارات المستخدمة في الواجهة الأمامية لنظام Gaara AI، مع وصف لكل مسار والمكون المرتبط به.

| المسار (Path) | المكون (Component) | الوصف | يتطلب مصادقة؟ |
| :--- | :--- | :--- | :--- |
| `/login` | `Login` | صفحة تسجيل الدخول | لا |
| `/dashboard` | `Dashboard` | لوحة التحكم الرئيسية | نعم |
| `/profile` | `Profile` | صفحة الملف الشخصي للمستخدم | نعم |
| `/farms` | `Farms` | عرض قائمة المزارع | نعم |
| `/farms/new` | `CreateFarm` | إنشاء مزرعة جديدة | نعم |
| `/farms/:id` | `FarmDetails` | عرض تفاصيل مزرعة | نعم |
| `/farms/:id/edit` | `EditFarm` | تعديل بيانات مزرعة | نعم |
| `/plants` | `Plants` | عرض قائمة النباتات | نعم |
| `/plants/new` | `CreatePlant` | إضافة نبات جديد | نعم |
| `/plants/:id` | `PlantDetails` | عرض تفاصيل نبات | نعم |
| `/plants/:id/edit` | `EditPlant` | تعديل بيانات نبات | نعم |
| `/diseases` | `Diseases` | عرض قائمة الأمراض | نعم |
| `/diseases/new` | `CreateDisease` | إضافة مرض جديد | نعم |
| `/diseases/:id` | `DiseaseDetails` | عرض تفاصيل مرض | نعم |
| `/diseases/:id/edit` | `EditDisease` | تعديل بيانات مرض | نعم |
| `/diagnosis` | `Diagnosis` | صفحة التشخيص الرئيسية | نعم |
| `/diagnosis/new` | `CreateDiagnosis` | إجراء تشخيص جديد | نعم |
| `/diagnosis/history` | `DiagnosisHistory` | عرض سجل التشخيصات | نعم |
| `/diagnosis/:id` | `DiagnosisDetails` | عرض تفاصيل تشخيص | نعم |
| `/sensors` | `Sensors` | عرض قائمة أجهزة الاستشعار | نعم |
| `/sensors/new` | `CreateSensor` | إضافة جهاز استشعار جديد | نعم |
| `/sensors/:id` | `SensorDetails` | عرض تفاصيل جهاز استشعار | نعم |
| `/sensors/:id/edit` | `EditSensor` | تعديل بيانات جهاز استشعار | نعم |
| `/reports` | `Reports` | صفحة التقارير | نعم |
| `/analytics` | `Analytics` | صفحة التحليلات | نعم |
| `/users` | `Users` | إدارة المستخدمين | نعم (Admin) |
| `/settings` | `SystemSettings` | إعدادات النظام | نعم (Admin) |
| `*` | `NotFound` | صفحة الخطأ 404 | N/A |
