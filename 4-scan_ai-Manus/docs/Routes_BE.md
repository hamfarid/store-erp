# مسارات الواجهة الخلفية (Backend Routes)

هذا المستند يوثق جميع المسارات المستخدمة في الواجهة الخلفية لنظام Gaara AI، مع وصف لكل مسار والدالة المرتبطة به.

| الطريقة (Method) | المسار (Path) | الدالة (Function) | الوصف | يتطلب مصادقة؟ |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/` | `index` | صفحة رئيسية بسيطة للتحقق من أن الواجهة الخلفية تعمل | لا |
| GET | `/api/health` | `health_check` | فحص صحة الواجهة الخلفية | لا |
| POST | `/api/auth/register` | `register` | تسجيل مستخدم جديد | لا |
| POST | `/api/auth/login` | `login` | تسجيل دخول المستخدم | لا |
| GET | `/api/auth/profile` | `get_profile` | الحصول على ملف المستخدم الحالي | نعم |
| GET | `/api/farms` | `get_farms` | الحصول على قائمة المزارع | نعم |
| POST | `/api/farms` | `create_farm` | إنشاء مزرعة جديدة | نعم |
| GET | `/api/farms/<int:farm_id>` | `get_farm` | الحصول على تفاصيل مزرعة محددة | نعم |
| GET | `/api/plants` | `get_plants` | الحصول على قائمة النباتات | نعم |
| POST | `/api/plants` | `create_plant` | إنشاء نبات جديد | نعم |
| GET | `/api/diseases` | `get_diseases` | الحصول على قائمة الأمراض | نعم |
| POST | `/api/diagnosis` | `create_diagnosis` | إنشاء طلب تشخيص جديد | نعم |
| GET | `/api/diagnosis/<int:diagnosis_id>` | `get_diagnosis` | الحصول على تفاصيل تشخيص محدد | نعم |
| GET | `/api/diagnosis` | `get_all_diagnoses` | الحصول على كل التشخيصات | نعم |
| POST | `/api/sensors` | `create_sensor` | إنشاء حساس جديد | نعم |
| POST | `/api/sensors/<int:sensor_id>/readings` | `add_sensor_reading` | إضافة قراءة حساس جديدة | نعم |
| GET | `/api/stats/dashboard` | `get_dashboard_stats` | الحصول على إحصائيات لوحة التحكم | نعم |
| GET | `/uploads/<filename>` | `uploaded_file` | عرض ملف تم رفعه | لا |
