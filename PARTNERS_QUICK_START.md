# دليل البدء السريع - مسارات العملاء والموردين
# Quick Start Guide - Partners Routes

## 🚀 البدء السريع | Quick Start

### 1. التحقق من التثبيت | Verify Installation

```bash
# التحقق من وجود الملفات
ls backend/src/routes/partners_unified.py
ls backend/test_partners_unified.py
```

### 2. تشغيل الاختبارات | Run Tests

```bash
cd backend
python test_partners_unified.py
```

**النتيجة المتوقعة:**
```
✅ نجح: 10
❌ فشل: 0
📈 نسبة النجاح: 100.0%
```

### 3. استخدام API | Use API

#### الحصول على قائمة العملاء
```bash
curl -X GET "http://localhost:5000/api/customers" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### إنشاء عميل جديد
```bash
curl -X POST "http://localhost:5000/api/customers" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "عميل جديد",
    "email": "customer@example.com",
    "phone": "123456789"
  }'
```

---

## 📋 المسارات المتاحة | Available Routes

### العملاء | Customers

| الطريقة | المسار | الوصف |
|---------|--------|-------|
| GET | `/api/customers` | قائمة العملاء |
| GET | `/api/customers/<id>` | عميل محدد |
| POST | `/api/customers` | إنشاء عميل |
| PUT | `/api/customers/<id>` | تحديث عميل |
| DELETE | `/api/customers/<id>` | حذف عميل |
| GET | `/api/customers/stats` | إحصائيات |
| GET | `/api/customers/search` | بحث سريع |
| GET | `/api/customers/export` | تصدير |

### الموردين | Suppliers

| الطريقة | المسار | الوصف |
|---------|--------|-------|
| GET | `/api/suppliers` | قائمة الموردين |
| GET | `/api/suppliers/<id>` | مورد محدد |
| POST | `/api/suppliers` | إنشاء مورد |
| PUT | `/api/suppliers/<id>` | تحديث مورد |
| DELETE | `/api/suppliers/<id>` | حذف مورد |
| GET | `/api/suppliers/stats` | إحصائيات |
| GET | `/api/suppliers/search` | بحث سريع |
| GET | `/api/suppliers/export` | تصدير |

---

## 🔐 المصادقة | Authentication

جميع المسارات تتطلب JWT Token:

```bash
Authorization: Bearer YOUR_TOKEN
```

للحصول على Token:
```bash
curl -X POST "http://localhost:5000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_password"
  }'
```

---

## 📝 أمثلة الاستخدام | Usage Examples

### 1. قائمة العملاء مع الترقيم

```bash
curl -X GET "http://localhost:5000/api/customers?page=1&per_page=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**الاستجابة:**
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

### 2. البحث في العملاء

```bash
curl -X GET "http://localhost:5000/api/customers/search?q=test&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. إحصائيات العملاء

```bash
curl -X GET "http://localhost:5000/api/customers/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**الاستجابة:**
```json
{
  "success": true,
  "data": {
    "total_customers": 100,
    "active_customers": 85,
    "inactive_customers": 15,
    "by_category": {
      "RETAIL": 50,
      "WHOLESALE": 30
    }
  }
}
```

### 4. تحديث عميل

```bash
curl -X PUT "http://localhost:5000/api/customers/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "اسم محدث",
    "email": "updated@example.com"
  }'
```

### 5. حذف عميل (يتطلب صلاحيات المدير)

```bash
curl -X DELETE "http://localhost:5000/api/customers/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## ⚠️ رموز الأخطاء | Error Codes

| الكود | الوصف | الحل |
|-------|-------|------|
| 200 | نجح | - |
| 201 | تم الإنشاء | - |
| 400 | طلب غير صحيح | تحقق من البيانات |
| 401 | غير مصرح | تحقق من Token |
| 404 | غير موجود | تحقق من ID |
| 500 | خطأ في الخادم | راجع السجلات |
| 501 | غير مدعوم | الميزة غير متاحة |

---

## 🧪 الاختبار | Testing

### تشغيل جميع الاختبارات

```bash
python test_partners_unified.py
```

### اختبار مسار محدد

استخدم Postman أو cURL لاختبار المسارات بشكل فردي.

---

## 📚 التوثيق الكامل | Full Documentation

للحصول على التوثيق الكامل، راجع:

1. **API Documentation**
   ```
   backend/docs/API_PARTNERS_UNIFIED.md
   ```

2. **README**
   ```
   backend/docs/PARTNERS_UNIFIED_README.md
   ```

3. **Summary**
   ```
   backend/PARTNERS_UNIFIED_SUMMARY.md
   ```

4. **Final Report**
   ```
   backend/PARTNERS_UNIFIED_FINAL_REPORT.md
   ```

---

## 🔧 استكشاف الأخطاء | Troubleshooting

### المشكلة: 401 Unauthorized

**الحل:**
- تأكد من وجود Token صحيح
- تحقق من صلاحية Token
- تأكد من إضافة Header بشكل صحيح

### المشكلة: 404 Not Found

**الحل:**
- تحقق من صحة المسار
- تأكد من وجود العنصر بالـ ID المحدد

### المشكلة: 500 Server Error

**الحل:**
- راجع سجلات الخادم
- تحقق من اتصال قاعدة البيانات
- تأكد من وجود النماذج المطلوبة

---

## 💡 نصائح | Tips

1. **استخدم Pagination** للقوائم الكبيرة
2. **استخدم البحث السريع** للعثور على العناصر
3. **راجع الإحصائيات** للحصول على نظرة عامة
4. **استخدم التصدير** للحصول على البيانات الكاملة

---

## 📞 الدعم | Support

للحصول على المساعدة:
1. راجع التوثيق الكامل
2. شغل الاختبارات للتحقق
3. تواصل مع فريق التطوير

---

## ✅ قائمة التحقق السريعة | Quick Checklist

- [ ] تم تثبيت المسارات
- [ ] الاختبارات تعمل بنجاح
- [ ] لديك Token صحيح
- [ ] راجعت التوثيق
- [ ] جربت الأمثلة

---

**آخر تحديث:** 2025-10-08  
**الإصدار:** 2.0  
**الحالة:** ✅ جاهز للاستخدام

