import { toast } from "sonner"
import { ApiError } from "@/services/api"

/**
 * Error Handler Utilities
 * Centralized error handling and user-friendly error messages
 */

// Error message mappings
const ERROR_MESSAGES = {
  // Network errors
  NETWORK_ERROR: "فشل الاتصال بالخادم. يرجى التحقق من اتصالك بالإنترنت",
  TIMEOUT: "انتهت مهلة الاتصال. يرجى المحاولة مرة أخرى",

  // HTTP errors
  400: "طلب غير صحيح. يرجى التحقق من البيانات المدخلة",
  401: "غير مصرح لك. يرجى تسجيل الدخول مرة أخرى",
  403: "ليس لديك صلاحية للوصول إلى هذا المورد",
  404: "المورد المطلوب غير موجود",
  422: "البيانات المدخلة غير صحيحة",
  429: "تم تجاوز عدد الطلبات المسموح بها. يرجى المحاولة لاحقاً",
  500: "حدث خطأ في الخادم. يرجى المحاولة لاحقاً",
  502: "الخادم غير متاح حالياً",
  503: "الخدمة غير متاحة حالياً",

  // Generic
  UNKNOWN_ERROR: "حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى",
}

/**
 * Get user-friendly error message
 * @param {Error|ApiError|string} error - The error object or message
 * @returns {string} - User-friendly error message
 */
export function getErrorMessage(error) {
  if (!error) return ERROR_MESSAGES.UNKNOWN_ERROR

  // If it's a string, return it
  if (typeof error === "string") return error

  // If it's an ApiError
  if (error instanceof ApiError) {
    // Check for custom message
    if (error.message) return error.message

    // Check for status code
    if (error.status && ERROR_MESSAGES[error.status]) {
      return ERROR_MESSAGES[error.status]
    }

    // Check for validation errors
    if (error.status === 422 && error.data?.errors) {
      const firstError = Object.values(error.data.errors)[0]
      if (Array.isArray(firstError)) {
        return firstError[0]
      }
      return firstError
    }
  }

  // If it's a standard Error
  if (error instanceof Error) {
    // Network errors
    if (error.message.includes("Network") || error.message.includes("network")) {
      return ERROR_MESSAGES.NETWORK_ERROR
    }

    if (error.message.includes("timeout") || error.message.includes("Timeout")) {
      return ERROR_MESSAGES.TIMEOUT
    }

    // Return the error message if it's user-friendly
    if (error.message && !error.message.includes("Error:")) {
      return error.message
    }
  }

  return ERROR_MESSAGES.UNKNOWN_ERROR
}

/**
 * Handle error and show toast notification
 * @param {Error|ApiError|string} error - The error to handle
 * @param {Object} options - Options for error handling
 * @param {boolean} options.showToast - Whether to show toast (default: true)
 * @param {string} options.fallbackMessage - Fallback message if error message not found
 * @param {Function} options.onError - Callback function to execute on error
 */
export function handleError(error, options = {}) {
  const {
    showToast = true,
    fallbackMessage = ERROR_MESSAGES.UNKNOWN_ERROR,
    onError,
  } = options

  const message = getErrorMessage(error) || fallbackMessage

  if (showToast) {
    toast.error(message, {
      duration: 5000,
    })
  }

  // Log error to console in development
  if (import.meta.env.DEV) {
    console.error("Error:", error)
  }

  // Execute callback if provided
  if (onError && typeof onError === "function") {
    onError(error, message)
  }

  return message
}

/**
 * Handle API error with retry logic
 * @param {Function} apiCall - The API function to retry
 * @param {Object} options - Retry options
 * @param {number} options.maxRetries - Maximum retry attempts (default: 3)
 * @param {number} options.delay - Delay between retries in ms (default: 1000)
 * @param {Function} options.onRetry - Callback before retry
 * @returns {Promise} - The API call result
 */
export async function handleApiErrorWithRetry(apiCall, options = {}) {
  const { maxRetries = 3, delay = 1000, onRetry } = options
  let lastError

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await apiCall()
    } catch (error) {
      lastError = error

      // Don't retry on client errors (4xx)
      if (error instanceof ApiError && error.status >= 400 && error.status < 500) {
        throw error
      }

      // Don't retry on last attempt
      if (attempt === maxRetries) {
        break
      }

      // Call onRetry callback
      if (onRetry) {
        onRetry(attempt + 1, error)
      }

      // Wait before retrying
      await new Promise((resolve) => setTimeout(resolve, delay * (attempt + 1)))
    }
  }

  throw lastError
}

/**
 * Format validation errors from API response
 * @param {Object} errors - Validation errors object
 * @returns {string} - Formatted error message
 */
export function formatValidationErrors(errors) {
  if (!errors || typeof errors !== "object") {
    return ERROR_MESSAGES.UNKNOWN_ERROR
  }

  const errorMessages = Object.entries(errors)
    .map(([field, messages]) => {
      const message = Array.isArray(messages) ? messages[0] : messages
      return `${field}: ${message}`
    })
    .join("\n")

  return errorMessages || ERROR_MESSAGES.UNKNOWN_ERROR
}

export default {
  getErrorMessage,
  handleError,
  handleApiErrorWithRetry,
  formatValidationErrors,
  ERROR_MESSAGES,
}
