// مكتبة التحقق من صحة البيانات
export const validators = {
  // التحقق من أن القيمة غير فارغة
  required: (value, fieldName = 'الحقل') => {
    if (!value || (typeof value === 'string' && value.trim() === '')) {
      return `${fieldName} مطلوب`
    }
    return null
  },

  // التحقق من الحد الأدنى لطول النص
  minLength: (value, min, fieldName = 'الحقل') => {
    if (value && value.length < min) {
      return `${fieldName} يجب أن يكون ${min} أحرف على الأقل`
    }
    return null
  },

  // التحقق من الحد الأقصى لطول النص
  maxLength: (value, max, fieldName = 'الحقل') => {
    if (value && value.length > max) {
      return `${fieldName} يجب أن يكون ${max} أحرف كحد أقصى`
    }
    return null
  },

  // التحقق من صحة البريد الإلكتروني
  email: (value, fieldName = 'البريد الإلكتروني') => {
    if (value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(value)) {
        return `${fieldName} غير صحيح`
      }
    }
    return null
  },

  // التحقق من صحة رقم الهاتف
  phone: (value, fieldName = 'رقم الهاتف') => {
    if (value) {
      const phoneRegex = /^[0-9+\-\s()]+$/
      if (!phoneRegex.test(value) || value.length < 10) {
        return `${fieldName} غير صحيح`
      }
    }
    return null
  },

  // التحقق من أن القيمة رقم موجب
  positiveNumber: (value, fieldName = 'الرقم') => {
    if (value !== undefined && value !== null && value !== '') {
      const num = parseFloat(value)
      if (isNaN(num) || num < 0) {
        return `${fieldName} يجب أن يكون رقم موجب`
      }
    }
    return null
  },

  // التحقق من أن القيمة رقم صحيح موجب
  positiveInteger: (value, fieldName = 'الرقم') => {
    if (value !== undefined && value !== null && value !== '') {
      const num = parseInt(value)
      if (isNaN(num) || num < 0 || !Number.isInteger(parseFloat(value))) {
        return `${fieldName} يجب أن يكون رقم صحيح موجب`
      }
    }
    return null
  },

  // التحقق من أن القيمة أكبر من قيمة معينة
  greaterThan: (value, min, fieldName = 'الرقم') => {
    if (value !== undefined && value !== null && value !== '') {
      const num = parseFloat(value)
      if (isNaN(num) || num <= min) {
        return `${fieldName} يجب أن يكون أكبر من ${min}`
      }
    }
    return null
  },

  // التحقق من أن القيمة أقل من قيمة معينة
  lessThan: (value, max, fieldName = 'الرقم') => {
    if (value !== undefined && value !== null && value !== '') {
      const num = parseFloat(value)
      if (isNaN(num) || num >= max) {
        return `${fieldName} يجب أن يكون أقل من ${max}`
      }
    }
    return null
  },

  // التحقق من أن القيمة ضمن نطاق معين
  range: (value, min, max, fieldName = 'الرقم') => {
    if (value !== undefined && value !== null && value !== '') {
      const num = parseFloat(value)
      if (isNaN(num) || num < min || num > max) {
        return `${fieldName} يجب أن يكون بين ${min} و ${max}`
      }
    }
    return null
  },

  // التحقق من أن رمز المنتج فريد
  uniqueSku: (value, existingSkus = [], fieldName = 'رمز المنتج') => {
    if (value && existingSkus.includes(value.toUpperCase())) {
      return `${fieldName} موجود مسبقاً`
    }
    return null
  }
}

// دالة للتحقق من صحة نموذج المنتج
export const validateProduct = (product, existingProducts = []) => {
  const errors = {}
  const existingBarcodes = existingProducts
    .filter(p => p.id !== product.id && p.barcode)
    .map(p => p.barcode?.toUpperCase())

  // التحقق من اسم المنتج
  const nameError = validators.required(product.name, 'اسم المنتج') ||
                   validators.minLength(product.name, 2, 'اسم المنتج') ||
                   validators.maxLength(product.name, 200, 'اسم المنتج')
  if (nameError) errors.name = nameError

  // التحقق من المرتبة
  const rankError = validators.required(product.rank_id, 'المرتبة')
  if (rankError) errors.rank_id = rankError

  // التحقق من الوحدة
  const unitError = validators.required(product.unit, 'الوحدة') ||
                   validators.maxLength(product.unit, 50, 'الوحدة')
  if (unitError) errors.unit = unitError

  // التحقق من الباركود (اختياري ولكن يجب أن يكون فريد)
  if (product.barcode) {
    const barcodeError = validators.uniqueSku(product.barcode, existingBarcodes, 'الباركود')
    if (barcodeError) errors.barcode = barcodeError
  }

  // التحقق من سعر التكلفة (اختياري)
  if (product.cost_price) {
    const costPriceError = validators.positiveNumber(product.cost_price, 'سعر التكلفة')
    if (costPriceError) errors.cost_price = costPriceError
  }

  // التحقق من سعر البيع (اختياري)
  if (product.selling_price) {
    const sellingPriceError = validators.positiveNumber(product.selling_price, 'سعر البيع')
    if (sellingPriceError) errors.selling_price = sellingPriceError
  }

  // التحقق من أن سعر البيع أكبر من سعر التكلفة
  if (product.cost_price && product.selling_price) {
    const costPrice = parseFloat(product.cost_price)
    const sellingPrice = parseFloat(product.selling_price)
    if (!isNaN(costPrice) && !isNaN(sellingPrice) && sellingPrice <= costPrice) {
      errors.selling_price = 'سعر البيع يجب أن يكون أكبر من سعر التكلفة'
    }
  }

  // التحقق من كمية إعادة الطلب (اختياري)
  if (product.reorder_quantity) {
    const reorderError = validators.positiveNumber(product.reorder_quantity, 'كمية إعادة الطلب')
    if (reorderError) errors.reorder_quantity = reorderError
  }

  // التحقق من الحد الأدنى
  const minQuantityError = validators.required(product.min_quantity, 'الحد الأدنى') ||
                          validators.positiveInteger(product.min_quantity, 'الحد الأدنى')
  if (minQuantityError) errors.min_quantity = minQuantityError

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

// دالة للتحقق من صحة نموذج العميل
export const validateCustomer = (customer) => {
  const errors = {}

  // التحقق من اسم العميل
  const nameError = validators.required(customer.name, 'اسم العميل') ||
                   validators.minLength(customer.name, 2, 'اسم العميل') ||
                   validators.maxLength(customer.name, 200, 'اسم العميل')
  if (nameError) errors.name = nameError

  // التحقق من الشخص المسؤول
  const contactPersonError = validators.required(customer.contact_person, 'الشخص المسؤول') ||
                            validators.maxLength(customer.contact_person, 100, 'الشخص المسؤول')
  if (contactPersonError) errors.contact_person = contactPersonError

  // التحقق من رقم الهاتف
  const phoneError = validators.required(customer.phone, 'رقم الهاتف') ||
                    validators.phone(customer.phone, 'رقم الهاتف')
  if (phoneError) errors.phone = phoneError

  // التحقق من البريد الإلكتروني (اختياري)
  if (customer.email) {
    const emailError = validators.email(customer.email, 'البريد الإلكتروني')
    if (emailError) errors.email = emailError
  }

  // التحقق من العنوان (اختياري)
  if (customer.address) {
    const addressError = validators.maxLength(customer.address, 500, 'العنوان')
    if (addressError) errors.address = addressError
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

// دالة للتحقق من صحة نموذج المورد
export const validateSupplier = (supplier) => {
  const errors = {}

  // التحقق من اسم المورد
  const nameError = validators.required(supplier.name, 'اسم المورد') ||
                   validators.minLength(supplier.name, 2, 'اسم المورد') ||
                   validators.maxLength(supplier.name, 200, 'اسم المورد')
  if (nameError) errors.name = nameError

  // التحقق من الشخص المسؤول
  const contactPersonError = validators.required(supplier.contact_person, 'الشخص المسؤول') ||
                            validators.maxLength(supplier.contact_person, 100, 'الشخص المسؤول')
  if (contactPersonError) errors.contact_person = contactPersonError

  // التحقق من رقم الهاتف
  const phoneError = validators.required(supplier.phone, 'رقم الهاتف') ||
                    validators.phone(supplier.phone, 'رقم الهاتف')
  if (phoneError) errors.phone = phoneError

  // التحقق من التخصص
  const categoryError = validators.required(supplier.category, 'التخصص')
  if (categoryError) errors.category = categoryError

  // التحقق من البريد الإلكتروني (اختياري)
  if (supplier.email) {
    const emailError = validators.email(supplier.email, 'البريد الإلكتروني')
    if (emailError) errors.email = emailError
  }

  // التحقق من العنوان (اختياري)
  if (supplier.address) {
    const addressError = validators.maxLength(supplier.address, 500, 'العنوان')
    if (addressError) errors.address = addressError
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

