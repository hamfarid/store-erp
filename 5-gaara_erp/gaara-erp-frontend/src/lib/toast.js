import { toast as sonnerToast } from "sonner"
import { CheckCircle2, XCircle, AlertCircle, Info, Loader2 } from "lucide-react"

/**
 * Toast Notification Utilities
 * Wrapper around sonner with consistent styling and icons
 */

/**
 * Show success toast
 * @param {string} message - Success message
 * @param {Object} options - Toast options
 */
export function toastSuccess(message, options = {}) {
  return sonnerToast.success(message, {
    icon: <CheckCircle2 className="w-5 h-5" />,
    duration: 3000,
    ...options,
  })
}

/**
 * Show error toast
 * @param {string} message - Error message
 * @param {Object} options - Toast options
 */
export function toastError(message, options = {}) {
  return sonnerToast.error(message, {
    icon: <XCircle className="w-5 h-5" />,
    duration: 5000,
    ...options,
  })
}

/**
 * Show warning toast
 * @param {string} message - Warning message
 * @param {Object} options - Toast options
 */
export function toastWarning(message, options = {}) {
  return sonnerToast.warning(message, {
    icon: <AlertCircle className="w-5 h-5" />,
    duration: 4000,
    ...options,
  })
}

/**
 * Show info toast
 * @param {string} message - Info message
 * @param {Object} options - Toast options
 */
export function toastInfo(message, options = {}) {
  return sonnerToast.info(message, {
    icon: <Info className="w-5 h-5" />,
    duration: 3000,
    ...options,
  })
}

/**
 * Show loading toast
 * @param {string} message - Loading message
 * @param {Object} options - Toast options
 * @returns {string|number} - Toast ID for dismissing
 */
export function toastLoading(message, options = {}) {
  return sonnerToast.loading(message, {
    icon: <Loader2 className="w-5 h-5 animate-spin" />,
    duration: Infinity,
    ...options,
  })
}

/**
 * Show promise toast (loading -> success/error)
 * @param {Promise} promise - The promise to track
 * @param {Object} messages - Messages for different states
 * @param {string} messages.loading - Loading message
 * @param {string} messages.success - Success message
 * @param {string} messages.error - Error message
 * @param {Object} options - Toast options
 */
export function toastPromise(promise, messages, options = {}) {
  return sonnerToast.promise(promise, {
    loading: messages.loading || "جاري المعالجة...",
    success: messages.success || "تم بنجاح",
    error: messages.error || "حدث خطأ",
    ...options,
  })
}

/**
 * Dismiss toast by ID
 * @param {string|number} toastId - Toast ID
 */
export function toastDismiss(toastId) {
  sonnerToast.dismiss(toastId)
}

/**
 * Dismiss all toasts
 */
export function toastDismissAll() {
  sonnerToast.dismiss()
}

// Re-export sonner toast for advanced usage
export { toast as toastCustom } from "sonner"

export default {
  success: toastSuccess,
  error: toastError,
  warning: toastWarning,
  info: toastInfo,
  loading: toastLoading,
  promise: toastPromise,
  dismiss: toastDismiss,
  dismissAll: toastDismissAll,
}
