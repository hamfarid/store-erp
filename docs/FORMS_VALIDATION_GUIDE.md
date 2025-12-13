# 📝 Gaara Store - Forms & Validation Guide

**Version**: 1.0  
**Date**: 2025-10-27  
**Status**: ✅ **ACTIVE**

---

## 🎯 FORMS OVERVIEW

The application uses React Hook Form for form management with Pydantic validators on the backend.

---

## 📦 FORM COMPONENTS

### 1. ProductForm
**Location**: `frontend/src/components/forms/ProductForm.jsx`

**Fields**:
- `name` - Product name (required, min 3 chars)
- `sku` - Product SKU (required, unique)
- `category_id` - Category (required)
- `cost_price` - Cost price (required, positive)
- `sale_price` - Sale price (required, positive)
- `quantity` - Quantity (required, positive)
- `description` - Description (optional)

**Validation**:
- Name: required, min 3 chars, max 100 chars
- SKU: required, unique, alphanumeric
- Price: required, positive number
- Quantity: required, positive integer

### 2. CustomerForm
**Location**: `frontend/src/components/forms/CustomerForm.jsx`

**Fields**:
- `name` - Customer name (required)
- `email` - Email (required, valid email)
- `phone` - Phone (required, valid format)
- `address` - Address (required)
- `city` - City (required)
- `country` - Country (required)
- `credit_limit` - Credit limit (optional, positive)

**Validation**:
- Name: required, min 3 chars
- Email: required, valid email format
- Phone: required, valid phone format
- Address: required, min 5 chars
- Credit limit: positive number

### 3. InvoiceForm
**Location**: `frontend/src/components/forms/InvoiceForm.jsx`

**Fields**:
- `customer_id` - Customer (required)
- `invoice_date` - Invoice date (required)
- `due_date` - Due date (required)
- `items` - Invoice items (required, min 1)
- `notes` - Notes (optional)
- `discount` - Discount (optional, 0-100)
- `tax` - Tax (optional, 0-100)

**Validation**:
- Customer: required
- Dates: required, valid date
- Items: required, min 1 item
- Discount/Tax: 0-100 percentage

### 4. SettingsForm
**Location**: `frontend/src/components/forms/SettingsForm.jsx`

**Fields**:
- `company_name` - Company name (required)
- `email` - Email (required, valid)
- `phone` - Phone (required)
- `address` - Address (required)
- `currency` - Currency (required)
- `language` - Language (required)
- `timezone` - Timezone (required)

**Validation**:
- Company name: required, min 3 chars
- Email: required, valid email
- Phone: required, valid format
- Currency: required, valid code
- Language: required, valid code
- Timezone: required, valid timezone

---

## 🔧 FORM IMPLEMENTATION

### Basic Form Structure
```jsx
import { useForm } from 'react-hook-form'
import { apiClient } from '../api/client'

const ProductForm = ({ onSuccess }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      name: '',
      sku: '',
      cost_price: 0,
      sale_price: 0,
      quantity: 0
    }
  })

  const onSubmit = async (data) => {
    try {
      const response = await apiClient.createProduct(data)
      onSuccess(response.data)
    } catch (error) {
      console.error('Form submission error:', error)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name', { required: 'Name is required' })} />
      {errors.name && <span>{errors.name.message}</span>}
      
      <button type="submit">Submit</button>
    </form>
  )
}
```

---

## ✅ VALIDATION RULES

### Text Fields
- Required: `{ required: 'Field is required' }`
- Min length: `{ minLength: { value: 3, message: 'Min 3 chars' } }`
- Max length: `{ maxLength: { value: 100, message: 'Max 100 chars' } }`
- Pattern: `{ pattern: { value: /^[a-z]+$/i, message: 'Invalid format' } }`

### Email Fields
- Required: `{ required: 'Email is required' }`
- Pattern: `{ pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: 'Invalid email' } }`

### Number Fields
- Required: `{ required: 'Number is required' }`
- Min: `{ min: { value: 0, message: 'Must be positive' } }`
- Max: `{ max: { value: 100, message: 'Max 100' } }`

### Date Fields
- Required: `{ required: 'Date is required' }`
- Validate: `{ validate: (value) => new Date(value) > new Date() || 'Date must be in future' }`

### Select Fields
- Required: `{ required: 'Please select an option' }`

---

## 🎨 FORM STYLING

### Input Styling
```jsx
<input
  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
  {...register('name')}
/>
```

### Error Styling
```jsx
{errors.name && (
  <span className="text-red-600 text-sm mt-1">{errors.name.message}</span>
)}
```

### Form Container
```jsx
<form className="space-y-6 bg-white p-6 rounded-lg shadow">
  {/* Form fields */}
</form>
```

---

## 🔄 FORM STATES

### Loading State
```jsx
const { isSubmitting } = formState

<button disabled={isSubmitting}>
  {isSubmitting ? 'Submitting...' : 'Submit'}
</button>
```

### Error State
```jsx
const { errors } = formState

{Object.keys(errors).length > 0 && (
  <div className="bg-red-50 p-4 rounded">
    <p>Please fix the errors below</p>
  </div>
)}
```

### Success State
```jsx
const [success, setSuccess] = useState(false)

{success && (
  <div className="bg-green-50 p-4 rounded">
    <p>Form submitted successfully!</p>
  </div>
)}
```

---

## 📤 FORM SUBMISSION

### Submit Handler
```jsx
const onSubmit = async (data) => {
  try {
    const response = await apiClient.createProduct(data)
    addNotification({
      type: 'success',
      message: 'Product created successfully'
    })
    onSuccess(response.data)
  } catch (error) {
    addNotification({
      type: 'error',
      message: error.message
    })
  }
}
```

---

## 🔗 FORM INTEGRATION

### With API Client
```jsx
const response = await apiClient.createProduct(formData)
const response = await apiClient.updateProduct(id, formData)
const response = await apiClient.deleteProduct(id)
```

### With State Management
```jsx
const { addNotification } = useApp()

addNotification({
  type: 'success',
  message: 'Form submitted successfully'
})
```

---

## ✅ BEST PRACTICES

### Do's ✅
- Validate on both client and server
- Show clear error messages
- Provide loading states
- Use React Hook Form
- Implement proper error handling
- Use semantic HTML
- Provide success feedback
- Clear form after submission

### Don'ts ❌
- Don't skip validation
- Don't show cryptic errors
- Don't leave users without feedback
- Don't submit multiple times
- Don't ignore server errors
- Don't use non-semantic HTML
- Don't forget error handling
- Don't leave form data after error

---

## 📚 RESOURCES

- **React Hook Form**: https://react-hook-form.com/
- **Form Components**: `frontend/src/components/forms/`
- **API Client**: `frontend/src/api/client.ts`
- **State Management**: `frontend/src/context/AppContext.jsx`

---

**Status**: ✅ **ACTIVE**  
**Last Updated**: 2025-10-27  
**Maintained By**: Augment Agent

📝 **Follow this guide for consistent form implementation!** 📝

