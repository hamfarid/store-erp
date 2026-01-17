/**
 * Quick Integration Guide - Form Validation System
 * 
 * This file shows how to integrate the form validation system
 * into existing forms throughout the application.
 */

// ============================================================================
// 1. BASIC INTEGRATION - Login Form Example
// ============================================================================

import React, { useState } from 'react';
import { FormField, FormContainer } from '@/components/FormValidation';
import { validationRules } from '@/utils/validationRules';

function LoginForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [touched, setTouched] = useState({});
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error on change
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Mark all as touched
    const newTouched = {};
    Object.keys(formData).forEach(key => {
      newTouched[key] = true;
    });
    setTouched(newTouched);

    // Validate email
    const emailValidation = validationRules.required(formData.email);
    if (emailValidation !== true) {
      setErrors(prev => ({ ...prev, email: emailValidation }));
      return;
    }

    const emailFormatValidation = validationRules.email(formData.email);
    if (emailFormatValidation !== true) {
      setErrors(prev => ({ ...prev, email: emailFormatValidation }));
      return;
    }

    // Validate password
    const passwordValidation = validationRules.required(formData.password);
    if (passwordValidation !== true) {
      setErrors(prev => ({ ...prev, password: passwordValidation }));
      return;
    }

    if (Object.keys(errors).length === 0) {
      setIsLoading(true);
      try {
        // Call login API
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });

        if (response.ok) {
          // Redirect or update state
          console.log('Login successful');
        } else {
          setErrors(prev => ({
            ...prev,
            submit: 'بيانات الدخول غير صحيحة'
          }));
        }
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <FormContainer onSubmit={handleSubmit}>
      <h2>تسجيل الدخول</h2>

      <FormField
        label="البريد الإلكتروني"
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.email}
        touched={touched.email}
        placeholder="your@email.com"
        required
        validators={[
          validationRules.required,
          validationRules.email
        ]}
      />

      <FormField
        label="كلمة المرور"
        name="password"
        type="password"
        value={formData.password}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.password}
        touched={touched.password}
        required
        validators={[validationRules.required]}
      />

      {errors.submit && (
        <div className="form-error" style={{ margin: '10px 0' }}>
          {errors.submit}
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        style={{
          width: '100%',
          padding: '10px',
          backgroundColor: isLoading ? '#ccc' : '#80AA45',
          color: '#fff',
          border: 'none',
          borderRadius: '6px',
          cursor: isLoading ? 'not-allowed' : 'pointer'
        }}
      >
        {isLoading ? 'جاري الدخول...' : 'دخول'}
      </button>
    </FormContainer>
  );
}

// ============================================================================
// 2. PRODUCT FORM - Registration Example
// ============================================================================

import { FormField, FormSelect, FormTextarea, FormCheckbox } from '@/components/FormValidation';

function ProductRegistrationForm() {
  const [formData, setFormData] = useState({
    productName: '',
    sku: '',
    category: '',
    price: '',
    description: '',
    inStock: false
  });

  const [touched, setTouched] = useState({});
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
  };

  const handleCheckboxChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const newTouched = {};
    Object.keys(formData).forEach(key => {
      newTouched[key] = true;
    });
    setTouched(newTouched);

    const newErrors = {};

    // Validate product name
    const nameValidation = validationRules.required(formData.productName);
    if (nameValidation !== true) {
      newErrors.productName = nameValidation;
    }

    // Validate price
    const priceValidation = validationRules.positiveNumber(formData.price);
    if (priceValidation !== true) {
      newErrors.price = priceValidation;
    }

    // Validate category
    if (!formData.category) {
      newErrors.category = 'يرجى اختيار فئة';
    }

    // Validate description
    const descValidation = validationRules.minLength(20)(formData.description);
    if (descValidation !== true) {
      newErrors.description = descValidation;
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      // Submit to API
      console.log('Form data:', formData);
    }
  };

  const categoryOptions = [
    { value: '', label: 'اختر فئة' },
    { value: 'electronics', label: 'الإلكترونيات' },
    { value: 'clothing', label: 'الملابس' },
    { value: 'books', label: 'الكتب' }
  ];

  return (
    <FormContainer onSubmit={handleSubmit}>
      <h2>إضافة منتج جديد</h2>

      <FormField
        label="اسم المنتج"
        name="productName"
        type="text"
        value={formData.productName}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.productName}
        touched={touched.productName}
        placeholder="مثال: هاتف ذكي"
        required
        validators={[validationRules.required]}
      />

      <FormField
        label="رمز المنتج (SKU)"
        name="sku"
        type="text"
        value={formData.sku}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.sku}
        touched={touched.sku}
        placeholder="مثال: PHONE-001"
      />

      <FormSelect
        label="الفئة"
        name="category"
        value={formData.category}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.category}
        touched={touched.category}
        options={categoryOptions}
        required
      />

      <FormField
        label="السعر"
        name="price"
        type="number"
        value={formData.price}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.price}
        touched={touched.price}
        placeholder="0.00"
        required
        validators={[validationRules.positiveNumber]}
      />

      <FormTextarea
        label="الوصف"
        name="description"
        value={formData.description}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.description}
        touched={touched.description}
        placeholder="وصف المنتج التفصيلي..."
        maxLength={1000}
        rows={5}
        validators={[validationRules.minLength(20)]}
      />

      <FormCheckbox
        label="المنتج متاح في المخزن"
        name="inStock"
        checked={formData.inStock}
        onChange={handleCheckboxChange}
      />

      <button type="submit" style={{ marginTop: '20px' }}>
        حفظ المنتج
      </button>
    </FormContainer>
  );
}

// ============================================================================
// 3. PROFILE FORM - Edit User Profile
// ============================================================================

import { FormField, FormRadio } from '@/components/FormValidation';

function UserProfileForm({ user }) {
  const [formData, setFormData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
    phone: user?.phone || '',
    gender: user?.gender || ''
  });

  const [touched, setTouched] = useState({});
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const newTouched = {};
    Object.keys(formData).forEach(key => {
      newTouched[key] = true;
    });
    setTouched(newTouched);

    const newErrors = {};

    // Validate name
    if (!formData.firstName) {
      newErrors.firstName = 'الاسم الأول مطلوب';
    }

    if (!formData.lastName) {
      newErrors.lastName = 'اسم العائلة مطلوب';
    }

    // Validate email
    const emailCheck = validationRules.email(formData.email);
    if (emailCheck !== true) {
      newErrors.email = emailCheck;
    }

    // Validate phone
    const phoneCheck = validationRules.phone(formData.phone);
    if (phoneCheck !== true) {
      newErrors.phone = phoneCheck;
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      // Update profile
      console.log('Update profile:', formData);
    }
  };

  const genderOptions = [
    { value: 'male', label: 'ذكر' },
    { value: 'female', label: 'أنثى' }
  ];

  return (
    <FormContainer onSubmit={handleSubmit}>
      <h2>تعديل الملف الشخصي</h2>

      <FormField
        label="الاسم الأول"
        name="firstName"
        type="text"
        value={formData.firstName}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.firstName}
        touched={touched.firstName}
        required
      />

      <FormField
        label="اسم العائلة"
        name="lastName"
        type="text"
        value={formData.lastName}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.lastName}
        touched={touched.lastName}
        required
      />

      <FormField
        label="البريد الإلكتروني"
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.email}
        touched={touched.email}
        required
        validators={[validationRules.email]}
      />

      <FormField
        label="رقم الجوال"
        name="phone"
        type="tel"
        value={formData.phone}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.phone}
        touched={touched.phone}
        validators={[validationRules.phone]}
      />

      <FormRadio
        label="النوع"
        name="gender"
        value={formData.gender}
        onChange={handleChange}
        options={genderOptions}
      />

      <button type="submit" style={{ marginTop: '20px' }}>
        حفظ التغييرات
      </button>
    </FormContainer>
  );
}

// ============================================================================
// 4. FORM HOOK - Reusable Logic
// ============================================================================

/**
 * Custom hook for form management
 * Handles state, validation, and submission
 */
function useForm(initialData, onSubmit) {
  const [formData, setFormData] = useState(initialData);
  const [touched, setTouched] = useState({});
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
  };

  const setFieldError = (fieldName, errorMessage) => {
    setErrors(prev => ({
      ...prev,
      [fieldName]: errorMessage
    }));
    setTouched(prev => ({
      ...prev,
      [fieldName]: true
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Mark all as touched
    const newTouched = {};
    Object.keys(formData).forEach(key => {
      newTouched[key] = true;
    });
    setTouched(newTouched);

    setIsLoading(true);
    try {
      await onSubmit(formData, setFieldError);
    } finally {
      setIsLoading(false);
    }
  };

  const reset = () => {
    setFormData(initialData);
    setTouched({});
    setErrors({});
  };

  return {
    formData,
    setFormData,
    touched,
    errors,
    setFieldError,
    handleChange,
    handleBlur,
    handleSubmit,
    reset,
    isLoading
  };
}

// Usage:
// const form = useForm({ email: '', password: '' }, onSubmit);
// <FormField {...form} />

export {
  LoginForm,
  ProductRegistrationForm,
  UserProfileForm,
  useForm
};
