import * as z from "zod"
import { VALIDATION } from "@/config/constants"

/**
 * Common Zod validation schemas
 * Reusable validation schemas for forms
 */

// Email validation
export const emailSchema = z
  .string()
  .min(1, "البريد الإلكتروني مطلوب")
  .email("البريد الإلكتروني غير صحيح")
  .max(VALIDATION.EMAIL_MAX_LENGTH, `الحد الأقصى ${VALIDATION.EMAIL_MAX_LENGTH} حرف`)

// Password validation
export const passwordSchema = z
  .string()
  .min(VALIDATION.PASSWORD_MIN_LENGTH, `كلمة المرور يجب أن تكون ${VALIDATION.PASSWORD_MIN_LENGTH} أحرف على الأقل`)
  .max(VALIDATION.PASSWORD_MAX_LENGTH, `الحد الأقصى ${VALIDATION.PASSWORD_MAX_LENGTH} حرف`)
  .regex(
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
    "كلمة المرور يجب أن تحتوي على حرف كبير وصغير ورقم"
  )

// Phone validation
export const phoneSchema = z
  .string()
  .min(VALIDATION.PHONE_MIN_LENGTH, `رقم الهاتف يجب أن يكون ${VALIDATION.PHONE_MIN_LENGTH} أرقام على الأقل`)
  .max(VALIDATION.PHONE_MAX_LENGTH, `الحد الأقصى ${VALIDATION.PHONE_MAX_LENGTH} رقم`)
  .regex(/^\+?[0-9]+$/, "رقم الهاتف غير صحيح")

// Name validation
export const nameSchema = z
  .string()
  .min(VALIDATION.NAME_MIN_LENGTH, `الاسم يجب أن يكون ${VALIDATION.NAME_MIN_LENGTH} أحرف على الأقل`)
  .max(VALIDATION.NAME_MAX_LENGTH, `الحد الأقصى ${VALIDATION.NAME_MAX_LENGTH} حرف`)
  .regex(/^[\u0600-\u06FFa-zA-Z\s]+$/, "الاسم يجب أن يحتوي على أحرف فقط")

// SKU validation
export const skuSchema = z
  .string()
  .min(VALIDATION.SKU_MIN_LENGTH, `رمز المنتج يجب أن يكون ${VALIDATION.SKU_MIN_LENGTH} أحرف على الأقل`)
  .max(VALIDATION.SKU_MAX_LENGTH, `الحد الأقصى ${VALIDATION.SKU_MAX_LENGTH} حرف`)
  .regex(/^[A-Z0-9-]+$/, "رمز المنتج يجب أن يحتوي على أحرف كبيرة وأرقام وشرطات فقط")

// Positive number validation
export const positiveNumberSchema = z
  .number()
  .positive("يجب أن يكون الرقم موجب")
  .or(z.string().transform((val) => {
    const num = parseFloat(val)
    if (isNaN(num) || num <= 0) {
      throw new Error("يجب أن يكون الرقم موجب")
    }
    return num
  }))

// Currency validation
export const currencySchema = z
  .number()
  .nonnegative("يجب أن يكون المبلغ موجب أو صفر")
  .or(z.string().transform((val) => {
    const num = parseFloat(val.replace(/[^\d.]/g, ""))
    if (isNaN(num) || num < 0) {
      throw new Error("المبلغ غير صحيح")
    }
    return num
  }))

// Date validation
export const dateSchema = z
  .string()
  .or(z.date())
  .refine((val) => {
    const date = val instanceof Date ? val : new Date(val)
    return !isNaN(date.getTime())
  }, "التاريخ غير صحيح")

// URL validation
export const urlSchema = z
  .string()
  .url("الرابط غير صحيح")
  .optional()
  .or(z.literal(""))

// File validation
export const fileSchema = (maxSize = 5 * 1024 * 1024, allowedTypes = []) => {
  return z
    .instanceof(File)
    .refine((file) => file.size <= maxSize, `حجم الملف يجب أن يكون أقل من ${maxSize / 1024 / 1024}MB`)
    .refine(
      (file) => allowedTypes.length === 0 || allowedTypes.includes(file.type),
      "نوع الملف غير مدعوم"
    )
}

// Common form schemas
export const loginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, "كلمة المرور مطلوبة"),
  rememberMe: z.boolean().optional(),
})

export const registerSchema = z.object({
  firstName: nameSchema,
  lastName: nameSchema,
  email: emailSchema,
  phone: phoneSchema,
  password: passwordSchema,
  confirmPassword: z.string(),
  companyName: z.string().min(2, "اسم الشركة مطلوب"),
  industry: z.string().min(1, "يجب اختيار القطاع"),
  agreeToTerms: z.boolean().refine((val) => val === true, "يجب الموافقة على الشروط"),
}).refine((data) => data.password === data.confirmPassword, {
  message: "كلمات المرور غير متطابقة",
  path: ["confirmPassword"],
})

export const forgotPasswordSchema = z.object({
  email: emailSchema,
})

export const resetPasswordSchema = z.object({
  password: passwordSchema,
  confirmPassword: z.string(),
  token: z.string().min(1, "رمز التحقق مطلوب"),
}).refine((data) => data.password === data.confirmPassword, {
  message: "كلمات المرور غير متطابقة",
  path: ["confirmPassword"],
})

export const changePasswordSchema = z.object({
  currentPassword: z.string().min(1, "كلمة المرور الحالية مطلوبة"),
  newPassword: passwordSchema,
  confirmPassword: z.string(),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "كلمات المرور غير متطابقة",
  path: ["confirmPassword"],
})

export default {
  emailSchema,
  passwordSchema,
  phoneSchema,
  nameSchema,
  skuSchema,
  positiveNumberSchema,
  currencySchema,
  dateSchema,
  urlSchema,
  fileSchema,
  loginSchema,
  registerSchema,
  forgotPasswordSchema,
  resetPasswordSchema,
  changePasswordSchema,
}
