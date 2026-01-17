# Form Validation System - README

## 🎯 نظام التحقق من صحة النماذج

نظام شامل وقابل لإعادة الاستخدام للتحقق من صحة بيانات النماذج مع دعم كامل للغة العربية والتصميم المتجاوب.

## ✨ المميزات

- ✅ **6 مكونات جاهزة للاستخدام** - FormField, FormSelect, FormTextarea, FormCheckbox, FormRadio, FormContainer
- ✅ **16+ قاعدة تحقق مدمجة** - required, email, phone, password, وغيرها
- ✅ **دعم RTL كامل** - واجهة عربية احترافية
- ✅ **تحقق في الوقت الفعلي** - التحقق أثناء الكتابة
- ✅ **حالات بصرية غنية** - valid, invalid, focused, disabled
- ✅ **رسائل خطأ واضحة** - بالعربية وسهلة الفهم
- ✅ **دعم الوضع الليلي** - Dark Mode
- ✅ **معايير الوصول** - WCAG compliant
- ✅ **تصميم متجاوب** - Responsive Design
- ✅ **أيقونات بصرية** - ✓ و ✕ للنتائج

## 📁 الملفات الرئيسية

### المكونات
- `frontend/src/components/FormValidation.jsx` - المكونات الستة الأساسية

### الأدوات
- `frontend/src/utils/validationRules.js` - قواعل التحقق والمدققات

### الأنماط
- `frontend/src/styles/FormValidation.css` - تصاميم CSS احترافية

### الأمثلة والتوثيق
- `frontend/src/components/FormValidationExample.jsx` - مثال عملي شامل
- `frontend/docs/FORM_VALIDATION_GUIDE.md` - دليل الاستخدام الكامل
- `frontend/docs/FORM_VALIDATION_SUMMARY.md` - ملخص شامل
- `frontend/docs/INTEGRATION_EXAMPLES.js` - أمثلة تطبيقية
- `frontend/docs/QUICK_REFERENCE.js` - بطاقة مرجعية سريعة

## 🚀 البدء السريع

### 1. استيراد المكونات
```jsx
import { FormField, FormContainer } from '@/components/FormValidation';
import { validationRules } from '@/utils/validationRules';
```

### 2. إنشاء نموذج
```jsx
function MyForm() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [touched, setTouched] = useState({});
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
  };

  return (
    <FormContainer onSubmit={handleSubmit}>
      <FormField
        label="البريد الإلكتروني"
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.email}
        touched={touched.email}
        validators={[validationRules.required, validationRules.email]}
        required
      />
    </FormContainer>
  );
}
```

## 📚 المكونات المتاحة

### FormField
حقل إدخال نصي مع التحقق من الصحة
```jsx
<FormField
  label="البريد الإلكتروني"
  name="email"
  type="email"
  value={value}
  onChange={handleChange}
  onBlur={handleBlur}
  error={error}
  touched={touched}
  required
  validators={[validationRules.email]}
/>
```

### FormSelect
حقل اختيار من قائمة
```jsx
<FormSelect
  label="الفئة"
  name="category"
  value={value}
  onChange={handleChange}
  options={[
    { value: 'a', label: 'الفئة الأولى' }
  ]}
/>
```

### FormTextarea
حقل نصي متعدد الأسطر
```jsx
<FormTextarea
  label="الوصف"
  name="description"
  value={value}
  onChange={handleChange}
  maxLength={500}
  rows={5}
/>
```

### FormCheckbox
مربع اختيار واحد
```jsx
<FormCheckbox
  label="أوافق على الشروط"
  name="acceptTerms"
  checked={checked}
  onChange={handleChange}
  required
/>
```

### FormRadio
مجموعة أزرار اختيار
```jsx
<FormRadio
  label="نوع المستخدم"
  name="userType"
  value={value}
  onChange={handleChange}
  options={[
    { value: 'customer', label: 'عميل' },
    { value: 'vendor', label: 'بائع' }
  ]}
/>
```

### FormContainer
حاوية النموذج
```jsx
<FormContainer onSubmit={handleSubmit}>
  {/* جميع الحقول هنا */}
</FormContainer>
```

## ✓ قواعل التحقق المدمجة

| القاعدة | الاستخدام | الوصف |
|--------|----------|--------|
| required | `validationRules.required(value)` | مطلوب |
| email | `validationRules.email(value)` | بريد إلكتروني |
| phone | `validationRules.phone(value)` | رقم جوال سعودي |
| password | `validationRules.password(value)` | كلمة مرور قوية |
| number | `validationRules.number(value)` | رقم صحيح |
| positiveNumber | `validationRules.positiveNumber(value)` | رقم موجب |
| url | `validationRules.url(value)` | رابط ويب |
| date | `validationRules.date(value)` | تاريخ صحيح |
| minLength(n) | `validationRules.minLength(10)(value)` | طول أدنى |
| maxLength(n) | `validationRules.maxLength(50)(value)` | طول أقصى |
| min(n) | `validationRules.min(0)(value)` | قيمة دنيا |
| max(n) | `validationRules.max(100)(value)` | قيمة عليا |
| range(a,b) | `validationRules.range(0,100)(value)` | نطاق |
| username | `validationRules.username(value)` | اسم مستخدم |
| match(val) | `validationRules.match(pwd)(value)` | تطابق |
| pattern(rx, msg) | `validationRules.pattern(regex, msg)` | تعبير نمطي |

## 🎨 حالات الحقول

الحقل يتغير تلقائياً بناءً على الحالة:

```
الافتراضي:    حدود رمادية
المركز:       أخضر مع ظل
الصحيح:       أخضر مع أيقونة ✓
غير صحيح:    أحمر مع أيقونة ✕
معطل:        رمادي شفاف
```

## 📝 الخصائص الرئيسية

### FormField Properties
```typescript
{
  label?: string              // عنوان الحقل
  name: string                // معرّف الحقل
  type?: string               // نوع الحقل (email, password, etc)
  value: any                  // القيمة الحالية
  onChange: (e) => void       // معالج التغيير
  onBlur?: (e) => void        // معالج مغادرة الحقل
  error?: string              // رسالة الخطأ
  touched?: boolean           // هل تم لمس الحقل؟
  disabled?: boolean          // هل الحقل معطل؟
  placeholder?: string        // النص المساعد
  required?: boolean          // هل الحقل مطلوب؟
  validators?: Function[]     // دوال التحقق
  hint?: string               // تلميح للمستخدم
  className?: string          // فئة CSS إضافية
}
```

## 🔧 إنشاء مدقق مخصص

```javascript
const customValidator = (value) => {
  // يجب أن تعيد true إذا صحيحة
  // أو رسالة خطأ بالعربية إذا خاطئة
  
  if (value.length < 3) {
    return 'يجب أن يكون الطول 3 أحرف على الأقل';
  }
  
  return true;
};

// الاستخدام
validators={[customValidator]}
```

## 📱 توافقية الأجهزة

- ✅ سطح المكتب (Chrome, Firefox, Safari, Edge)
- ✅ الهواتف الذكية (iOS, Android)
- ✅ الأجهزة اللوحية
- ✅ الشاشات العريضة

## ♿ إمكانية الوصول

- قارئات الشاشة (Screen Readers)
- الملاحة بلوحة المفاتيح
- تسميات ARIA صحيحة
- رسائل الخطأ معلنة بشكل صحيح
- ألوان متباينة (High Contrast)

## 🌙 دعم الوضع الليلي

الأنماط تتكيف تلقائياً مع:
- `prefers-color-scheme: dark`

## 📊 معايير الأداء

- استخدام `useCallback` لتحسين الأداء
- عدم إعادة العرض غير الضرورية
- تحقق فعال بدون تأخير

## 📖 المراجع والموارد

اقرأ الملفات التالية للمزيد:

1. **FORM_VALIDATION_GUIDE.md** - دليل شامل مفصل
2. **FormValidationExample.jsx** - مثال عملي كامل
3. **INTEGRATION_EXAMPLES.js** - أمثلة متعددة
4. **QUICK_REFERENCE.js** - بطاقة مرجعية سريعة

## 💡 نصائح مفيدة

### 1. استخدم Hook مخصص
```jsx
const form = useForm(initialData, onSubmit);
```

### 2. جمّع المدققات
```jsx
validators={[
  validationRules.required,
  validationRules.email,
  customValidator
]}
```

### 3. استخدم تلميحات واضحة
```jsx
hint="استخدم صيغة البريد الصحيحة"
```

### 4. عطّل الزر أثناء الإرسال
```jsx
<button disabled={isLoading}>
  {isLoading ? 'جاري الإرسال...' : 'إرسال'}
</button>
```

## 🐛 استكشاف الأخطاء

| المشكلة | الحل |
|-------|-----|
| الحقل لا يعرض خطأ | تأكد من `touched={true}` و `error` موجود |
| التحقق لا يعمل | تأكد من وجود `validators` |
| الأيقونات لا تظهر | تأكد من استيراد CSS الصحيح |
| المحاذاة خاطئة | تأكد من `direction: rtl` في الـ CSS |

## 🎁 الميزات الإضافية

قريباً:
- [ ] تحقق غير متزامن (Async Validation)
- [ ] تحقق متبادل (Cross-field Validation)
- [ ] حفظ تلقائي (Auto-save)
- [ ] معاينة الملفات
- [ ] منتقي التاريخ المتقدم
- [ ] اختيار متعدد مع بحث

## 📞 الدعم

للأسئلة والمشاكل:
1. راجع الدليل (FORM_VALIDATION_GUIDE.md)
2. انظر الأمثلة (FormValidationExample.jsx)
3. تحقق من قواعل التحقق (validationRules.js)
4. استخدم DevTools للتصحيح

## 📄 الترخيص

هذا المشروع مرخص تحت MIT License

---

**الإصدار:** 1.0.0  
**آخر تحديث:** 2024  
**الحالة:** جاهز للإنتاج ✅  
**الدعم:** كامل ✅
