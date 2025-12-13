/**
 * ==========================================
 * نظام التحقق من صحة النماذج - بطاقة مرجعية سريعة
 * Form Validation System - Quick Reference
 * 
 * NOTE: This is a documentation/reference file with code examples.
 * It is not meant to be imported as a component.
 * ==========================================
 */

/* eslint-disable react-hooks/rules-of-hooks, no-unused-vars, no-undef */

// ============================================================================
// 1. الاستيراد والمتطلبات الأساسية
// ============================================================================

import React, { useState } from 'react';
import {
  FormField,
  FormSelect,
  FormTextarea,
  FormCheckbox,
  FormRadio,
  FormContainer
} from '@/components/FormValidation';
import { validationRules } from '@/utils/validationRules';

// ============================================================================
// 2. إعداد حالة النموذج
// ============================================================================

const formData_Example = {
  email: '',
  password: '',
  phone: '',
  category: '',
  description: '',
  acceptTerms: false
};

// Example: const [formData, setFormData] = useState(formData_Example);
// Example: const [touched, setTouched] = useState({});
// Example: const [errors, setErrors] = useState({});

// ============================================================================
// 3. معالجات الأحداث الأساسية
// ============================================================================

const _handleChange = (e) => {
  const { name, value } = e.target;
  // setFormData(prev => ({ ...prev, [name]: value }));
  
  // مسح الخطأ عند تغيير القيمة
  // if (errors[name]) {
  //   setErrors(prev => ({ ...prev, [name]: '' }));
  // }
};

const _handleBlur = (e) => {
  const { name } = e.target;
  // setTouched(prev => ({ ...prev, [name]: true }));
};

const _handleCheckboxChange = (e) => {
  const { name, value } = e.target;
  // setFormData(prev => ({ ...prev, [name]: value }));
};

// ============================================================================
// DOCUMENTATION EXAMPLES - Use these patterns in your components
// ============================================================================

// Example 1: Form Field
// <FormField
//   label="البريد الإلكتروني"
//   name="email"
//   type="email"
//   value={formData.email}
//   onChange={handleChange}
//   onBlur={handleBlur}
//   error={errors.email}
//   touched={touched.email}
//   placeholder="example@email.com"
//   required
//   validators={[validationRules.required, validationRules.email]}
//   hint="استخدم بريد إلكتروني صحيح"
// />

// Example 2: Form Select
// <FormSelect
//   label="الفئة"
//   name="category"
//   value={formData.category}
//   onChange={handleChange}
//   error={errors.category}
//   touched={touched.category}
//   options={[
//     { value: '', label: 'اختر فئة' },
//     { value: 'cat1', label: 'الفئة الأولى' }
//   ]}
//   required
// />

// Example 3: Form Textarea
// <FormTextarea
//   label="الوصف"
//   name="description"
//   value={formData.description}
//   onChange={handleChange}
//   placeholder="أدخل الوصف..."
//   maxLength={500}
//   rows={5}
//   validators={[validationRules.minLength(10)]}
// />

// Example 4: Form Checkbox
// <FormCheckbox
//   label="أوافق على الشروط"
//   name="acceptTerms"
//   checked={formData.acceptTerms}
//   onChange={handleCheckboxChange}
//   error={errors.acceptTerms}
//   touched={touched.acceptTerms}
//   required
// />

// Example 5: Form Radio
// <FormRadio
//   label="نوع المستخدم"
//   name="userType"
//   value={formData.userType}
//   onChange={handleChange}
//   options={[
//     { value: 'customer', label: 'عميل' },
//     { value: 'vendor', label: 'بائع' }
//   ]}
//   required
// />

// ============================================================================
// 10. جدول قواعل التحقق
// ============================================================================

/*
VALIDATION RULES QUICK TABLE:

┌─────────────────────┬──────────────────────────────────────┐
│ Rule Name           │ Example Usage                        │
├─────────────────────┼──────────────────────────────────────┤
│ required            │ validationRules.required(value)      │
│ email               │ validationRules.email(value)         │
│ phone               │ validationRules.phone(value)         │
│ password            │ validationRules.password(value)      │
│ number              │ validationRules.number(value)        │
│ positiveNumber      │ validationRules.positiveNumber(value)│
│ url                 │ validationRules.url(value)           │
│ date                │ validationRules.date(value)          │
│ minLength(n)        │ validationRules.minLength(8)(value)  │
│ maxLength(n)        │ validationRules.maxLength(50)(value) │
│ min(n)              │ validationRules.min(0)(value)        │
│ max(n)              │ validationRules.max(100)(value)      │
│ range(min,max)      │ validationRules.range(0,100)(value)  │
│ username            │ validationRules.username(value)      │
│ match(val)          │ validationRules.match(pwd)(cpwd)     │
│ pattern(regex, msg) │ validationRules.pattern(/.../, 'msg')│
└─────────────────────┴──────────────────────────────────────┘
*/

// ============================================================================
// 11. نموذج كامل لـ Hook
// ============================================================================

/*
function useForm(initialData, onSubmit) {
  const [formData, setFormData] = useState(initialData);
  const [touched, setTouched] = useState({});
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await onSubmit(formData);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    formData,
    touched,
    errors,
    handleChange,
    handleBlur,
    handleSubmit,
    isLoading
  };
}
*/

// ============================================================================
// 12. أمثلة على المدققات المخصصة
// ============================================================================

/*
// مدقق مخصص - التحقق من العمر
const validateAge = (age) => {
  const numAge = parseInt(age);
  if (isNaN(numAge) || numAge < 18) {
    return 'يجب أن تكون 18 سنة فأكثر';
  }
  return true;
};

// مدقق مخصص - التحقق من تطابق كلمات المرور
const validatePasswordMatch = (confirmPassword) => {
  if (confirmPassword !== formData.password) {
    return 'كلمات المرور غير متطابقة';
  }
  return true;
};

// الاستخدام:
validators={[validationRules.required, validateAge]}
validators={[validatePasswordMatch]}
*/

// ============================================================================
// 13. CSS Classes للتصميم المخصص
// ============================================================================

/*
AVAILABLE CSS CLASSES:

.form-container       - حاوية النموذج الرئيسية
.form-group           - مجموعة الحقل
.form-label           - عنوان الحقل
.form-field-wrapper   - محيط الحقل
.form-input           - الحقل النصي
.form-input.input-valid    - حقل صحيح
.form-input.input-invalid  - حقل غير صحيح
.form-input:disabled  - حقل معطل
.form-select          - حقل الاختيار
.form-textarea        - الحقل النصي متعدد الأسطر
.form-checkbox        - مربع الاختيار
.form-radio           - زر الاختيار
.form-error           - رسالة الخطأ
.form-error-icon      - أيقونة الخطأ
.form-success         - رسالة النجاح
.form-success-icon    - أيقونة النجاح
.form-warning         - رسالة التحذير
.form-hint            - التلميح
.required-indicator   - مؤشر الحقل المطلوب
*/

// ============================================================================
// 14. نصائح الأداء
// ============================================================================

/*
PERFORMANCE TIPS:

1. استخدم useCallback للدوال المعقدة:
   const handleChange = useCallback((e) => {
     // معالجة
   }, [dependencies]);

2. فرّق بين TouchedFields والErrors:
   - touched: يتبع ما إذا تم لمس الحقل
   - errors: يتبع رسائل الخطأ

3. تجنب التحقق المتكرر غير الضروري:
   - تحقق فقط عند الحاجة
   - مسح الأخطاء عند التغيير

4. استخدم التحقق غير المتزامن للفحوصات الثقيلة:
   - التحقق من توفر اسم المستخدم
   - التحقق من البريد الإلكتروني المسجل
*/

// ============================================================================
// 15. أمثلة على رسائل الخطأ
// ============================================================================

/*
ERROR MESSAGES:

Required Field:
  "هذا الحقل مطلوب"

Invalid Email:
  "يرجى إدخال بريد إلكتروني صحيح"

Invalid Phone:
  "يرجى إدخال رقم جوال صحيح"

Weak Password:
  "كلمة المرور يجب أن تكون 8 أحرف على الأقل"
  "يجب أن تحتوي على حرف كبير واحد على الأقل"
  "يجب أن تحتوي على حرف صغير واحد على الأقل"
  "يجب أن تحتوي على رقم واحد على الأقل"

Min Length:
  "يجب أن يكون الطول 10 أحرف على الأقل"

Max Length:
  "يجب ألا يتجاوز الطول 50 أحرف"
*/

// ============================================================================
// 16. القائمة النهائية
// ============================================================================

/*
CHECKLIST BEFORE SUBMISSION:

□ جميع الحقول المطلوبة معلمة بـ required={true}
□ جميع الحقول لها قيمة مبدئية في formData
□ جميع الحقول لديها setState/setErrors
□ معالجات الأحداث connected بشكل صحيح
□ التحقق من الصحة يعمل على blur و change
□ رسائل الخطأ بالعربية واضحة
□ الأيقونات البصرية معروضة بشكل صحيح
□ الزر معطل أثناء الإرسال
□ رسالة النجاح/الفشل معروضة
□ النموذج يعود للحالة الابتدائية بعد الإرسال
*/

// This is a reference guide, not a component to export
