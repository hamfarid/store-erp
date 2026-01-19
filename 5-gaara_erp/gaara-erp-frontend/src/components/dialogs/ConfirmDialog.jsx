/**
 * Confirm Dialog Component - مكون تأكيد الإجراء
 * Gaara ERP v12
 *
 * Reusable confirmation dialog for delete/dangerous operations.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import { AlertTriangle, Trash2, XCircle, CheckCircle } from 'lucide-react'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'

/**
 * Variant configurations
 */
const variants = {
  danger: {
    icon: Trash2,
    iconClass: 'text-red-500',
    buttonClass: 'bg-red-600 hover:bg-red-700',
    confirmText: 'حذف',
  },
  warning: {
    icon: AlertTriangle,
    iconClass: 'text-yellow-500',
    buttonClass: 'bg-yellow-600 hover:bg-yellow-700',
    confirmText: 'تأكيد',
  },
  info: {
    icon: CheckCircle,
    iconClass: 'text-blue-500',
    buttonClass: 'bg-blue-600 hover:bg-blue-700',
    confirmText: 'موافق',
  },
}

/**
 * ConfirmDialog Component
 */
export function ConfirmDialog({
  open,
  onOpenChange,
  title = 'هل أنت متأكد؟',
  description,
  variant = 'danger',
  confirmText,
  cancelText = 'إلغاء',
  onConfirm,
  isLoading = false,
}) {
  const config = variants[variant] || variants.danger
  const Icon = config.icon

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-full bg-opacity-10 ${config.iconClass.replace('text-', 'bg-')}`}>
              <Icon className={`w-6 h-6 ${config.iconClass}`} />
            </div>
            <AlertDialogTitle>{title}</AlertDialogTitle>
          </div>
          {description && (
            <AlertDialogDescription className="mt-3">
              {description}
            </AlertDialogDescription>
          )}
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel disabled={isLoading}>{cancelText}</AlertDialogCancel>
          <AlertDialogAction
            onClick={onConfirm}
            disabled={isLoading}
            className={config.buttonClass}
          >
            {isLoading ? 'جاري...' : confirmText || config.confirmText}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

export default ConfirmDialog
