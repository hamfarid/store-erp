# دليل استخدام Response Helper

## نظرة عامة

تم إنشاء `responseHelper.js` لتوحيد التعامل مع ردود API في الواجهة الأمامية. يدعم كلاً من:
- **الصيغة الجديدة**: `{ status: 'success'|'error', data: {...}, message: '...' }`
- **الصيغة القديمة**: `{ success: true|false, data: {...}, message: '...' }` (للتوافق العكسي)

## التثبيت

```javascript
import { isSuccess, getData, getErrorMessage, handleApiCall } from '@/utils/responseHelper';
// أو
import responseHelper from '@/utils/responseHelper';
```

## الدوال المتاحة

### 1. `isSuccess(response)`
التحقق من نجاح الرد

```javascript
// قبل
if (response.success) {
  // ...
}

// بعد
if (isSuccess(response)) {
  // ...
}
```

### 2. `isError(response)`
التحقق من فشل الرد

```javascript
if (isError(response)) {
  console.error('فشلت العملية');
}
```

### 3. `getData(response, defaultValue)`
الحصول على البيانات من الرد

```javascript
// قبل
const products = response.data || [];

// بعد
const products = getData(response, []);
```

### 4. `getErrorMessage(response, defaultMessage)`
الحصول على رسالة الخطأ

```javascript
// قبل
const errorMsg = response.message || response.error || 'حدث خطأ';

// بعد
const errorMsg = getErrorMessage(response, 'حدث خطأ');
```

### 5. `normalizeResponse(response)`
تحويل الرد إلى الصيغة الموحدة

```javascript
const normalized = normalizeResponse(response);
// دائماً يرجع { status: 'success'|'error', ... }
```

### 6. `handleResponse(response, { onSuccess, onError })`
معالج عام للردود

```javascript
handleResponse(response, {
  onSuccess: (data) => {
    console.log('نجحت العملية:', data);
  },
  onError: (errorMsg) => {
    console.error('فشلت العملية:', errorMsg);
  }
});
```

### 7. `handleApiCall(promise, { onSuccess, onError, onFinally })`
معالج للردود مع Promise

```javascript
await handleApiCall(
  fetch('/api/products'),
  {
    onSuccess: (data) => {
      setProducts(data);
    },
    onError: (errorMsg) => {
      toast.error(errorMsg);
    },
    onFinally: () => {
      setLoading(false);
    }
  }
);
```

## أمثلة عملية

### مثال 1: جلب البيانات

```javascript
// قبل
const fetchProducts = async () => {
  try {
    const response = await api.get('/products');
    if (response.success) {
      setProducts(response.data);
    } else {
      toast.error(response.message || 'فشل تحميل المنتجات');
    }
  } catch (error) {
    toast.error('حدث خطأ في الاتصال');
  }
};

// بعد
const fetchProducts = async () => {
  await handleApiCall(
    api.get('/products'),
    {
      onSuccess: (data) => setProducts(data),
      onError: (msg) => toast.error(msg)
    }
  );
};
```

### مثال 2: إرسال نموذج

```javascript
// قبل
const handleSubmit = async (formData) => {
  setLoading(true);
  try {
    const response = await api.post('/products', formData);
    if (response.success) {
      toast.success('تم الحفظ بنجاح');
      navigate('/products');
    } else {
      toast.error(response.message || 'فشل الحفظ');
    }
  } catch (error) {
    toast.error('حدث خطأ');
  } finally {
    setLoading(false);
  }
};

// بعد
const handleSubmit = async (formData) => {
  setLoading(true);
  await handleApiCall(
    api.post('/products', formData),
    {
      onSuccess: () => {
        toast.success('تم الحفظ بنجاح');
        navigate('/products');
      },
      onError: (msg) => toast.error(msg),
      onFinally: () => setLoading(false)
    }
  );
};
```

### مثال 3: معالجة متقدمة

```javascript
const loadData = async () => {
  try {
    const response = await api.get('/dashboard/stats');
    
    // تطبيع الرد
    const normalized = normalizeResponse(response);
    
    // التحقق من النجاح
    if (isSuccess(normalized)) {
      const stats = getData(normalized);
      setStats(stats);
    } else {
      const errorMsg = getErrorMessage(normalized);
      toast.error(errorMsg);
    }
  } catch (error) {
    toast.error('فشل تحميل الإحصائيات');
  }
};
```

## خطة الترحيل

### المرحلة 1: إضافة الدوال المساعدة (✅ مكتملة)
- تم إنشاء `responseHelper.js`
- جاهز للاستخدام في جميع المكونات

### المرحلة 2: تحديث المكونات الرئيسية
الملفات ذات الأولوية:
1. `src/services/api.js` - خدمة API الرئيسية
2. `src/components/Login.jsx` - تسجيل الدخول
3. `src/components/Products.jsx` - إدارة المنتجات
4. `src/components/Dashboard.jsx` - لوحة التحكم

### المرحلة 3: تحديث بقية المكونات
- استخدام البحث والاستبدال التدريجي
- اختبار كل مكون بعد التحديث

## ملاحظات مهمة

1. **التوافق العكسي**: جميع الدوال تدعم الصيغة القديمة والجديدة
2. **لا حاجة لتحديث Backend أولاً**: يمكن البدء بتحديث Frontend فوراً
3. **تدريجي**: يمكن تحديث المكونات واحداً تلو الآخر
4. **آمن**: لن يكسر الكود الحالي

## الخطوات التالية

1. ✅ إنشاء `responseHelper.js`
2. ⏳ تحديث `src/services/api.js`
3. ⏳ تحديث المكونات الرئيسية
4. ⏳ تحديث بقية المكونات
5. ⏳ إزالة الصيغة القديمة تدريجياً

## أسئلة شائعة

**س: هل يجب تحديث جميع الملفات دفعة واحدة؟**
ج: لا، يمكن التحديث تدريجياً. الدوال المساعدة تدعم كلا الصيغتين.

**س: ماذا لو كان Backend لا يزال يرسل `success`؟**
ج: لا مشكلة! الدوال المساعدة تتعامل مع كلا الصيغتين تلقائياً.

**س: هل هناك تأثير على الأداء؟**
ج: لا، الدوال المساعدة خفيفة جداً ولا تؤثر على الأداء.

