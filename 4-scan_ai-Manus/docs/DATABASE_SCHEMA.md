# مخطط قاعدة البيانات (Database Schema)

هذا المستند يوثق مخطط قاعدة البيانات الكامل لنظام Gaara AI، بما في ذلك الجداول، الحقول، العلاقات، والفهارس.

## جدول: `users` (المستخدمون)

| اسم الحقل | نوع البيانات | القيود | الوصف |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | المعرف الرئيسي |
| `username` | `String(80)` | `Unique`, `Not Null` | اسم المستخدم |
| `email` | `String(120)` | `Unique`, `Not Null` | البريد الإلكتروني |
| `password_hash` | `String(255)` | `Not Null` | هاش كلمة المرور |
| `role` | `String(20)` | `Default: 'user'` | دور المستخدم (admin, user, etc.) |
| `is_active` | `Boolean` | `Default: True` | هل الحساب نشط؟ |
| `created_at` | `DateTime` | `Default: now()` | تاريخ إنشاء الحساب |

## جدول: `farms` (المزارع)

| اسم الحقل | نوع البيانات | القيود | الوصف |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | المعرف الرئيسي |
| `name` | `String(100)` | `Not Null` | اسم المزرعة |
| `location` | `String(200)` | | موقع المزرعة |
| `area` | `Float` | | مساحة المزرعة |
| `owner_id` | `Integer` | `FK(users.id)` | مالك المزرعة |
| `company_id` | `Integer` | `FK(companies.id)` | الشركة المالكة |
| `created_at` | `DateTime` | `Default: now()` | تاريخ إنشاء المزرعة |

## جدول: `plants` (النباتات)

| اسم الحقل | نوع البيانات | القيود | الوصف |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | المعرف الرئيسي |
| `name` | `String(100)` | `Not Null` | اسم النبات |
| `scientific_name` | `String(150)` | | الاسم العلمي |
| `description` | `Text` | | وصف النبات |
| `created_at` | `DateTime` | `Default: now()` | تاريخ الإضافة |

## جدول: `diseases` (الأمراض)

| اسم الحقل | نوع البيانات | القيود | الوصف |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | المعرف الرئيسي |
| `name` | `String(100)` | `Not Null` | اسم المرض |
| `description` | `Text` | | وصف المرض |
| `symptoms` | `Text` | | الأعراض |
| `treatment` | `Text` | | العلاج |
| `created_at` | `DateTime` | `Default: now()` | تاريخ الإضافة |

## جدول: `diagnosis` (التشخيصات)

| اسم الحقل | نوع البيانات | القيود | الوصف |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | المعرف الرئيسي |
| `image_url` | `String(255)` | `Not Null` | رابط صورة التشخيص |
| `result` | `JSON` | | نتيجة التشخيص |
| `confidence` | `Float` | | درجة الثقة |
| `user_id` | `Integer` | `FK(users.id)` | المستخدم الذي أجرى التشخيص |
| `plant_id` | `Integer` | `FK(plants.id)` | النبات المشخص |
| `disease_id` | `Integer` | `FK(diseases.id)` | المرض المشخص |
| `created_at` | `DateTime` | `Default: now()` | تاريخ التشخيص |

## جدول: `sensors` (أجهزة الاستشعار)

| اسم الحقل | نوع البيانات | القيود | الوصف |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | المعرف الرئيسي |
| `type` | `String(50)` | `Not Null` | نوع الحساس (حرارة، رطوبة، ..) |
| `location` | `String(100)` | | موقع الحساس |
| `farm_id` | `Integer` | `FK(farms.id)` | المزرعة التابع لها |
| `created_at` | `DateTime` | `Default: now()` | تاريخ التركيب |

## جدول: `sensor_readings` (قراءات أجهزة الاستشعار)

| اسم الحقل | نوع البيانات | القيود | الوصف |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | المعرف الرئيسي |
| `value` | `Float` | `Not Null` | قيمة القراءة |
| `timestamp` | `DateTime` | `Default: now()` | وقت القراءة |
| `sensor_id` | `Integer` | `FK(sensors.id)` | الحساس المرتبط |

## جداول الربط

*   `plant_diseases`: لربط النباتات بالأمراض (علاقة كثير إلى كثير).
*   `user_permissions`: لربط المستخدمين بالصلاحيات (علاقة كثير إلى كثير).
