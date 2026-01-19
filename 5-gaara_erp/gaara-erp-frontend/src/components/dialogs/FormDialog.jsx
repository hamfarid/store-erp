/**
 * Form Dialog Component - مكون نموذج الحوار
 * Gaara ERP v12
 *
 * Reusable form dialog wrapper with loading and error states.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import { Loader2 } from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'

/**
 * FormDialog Component
 */
export function FormDialog({
  open,
  onOpenChange,
  title,
  description,
  children,
  onSubmit,
  submitText = 'حفظ',
  cancelText = 'إلغاء',
  isLoading = false,
  isSubmitting = false,
  error = null,
  size = 'md',
  showFooter = true,
  footerContent,
}) {
  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-[90vw]',
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (onSubmit) {
      onSubmit(e)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className={sizeClasses[size]}>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>

        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <ScrollArea className="max-h-[60vh] px-1">
              {error && (
                <div className="mb-4 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm">
                  {error}
                </div>
              )}
              {children}
            </ScrollArea>

            {showFooter && (
              <DialogFooter className="mt-6">
                {footerContent || (
                  <>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => onOpenChange(false)}
                      disabled={isSubmitting}
                    >
                      {cancelText}
                    </Button>
                    <Button type="submit" disabled={isSubmitting}>
                      {isSubmitting ? (
                        <>
                          <Loader2 className="w-4 h-4 ml-2 animate-spin" />
                          جاري الحفظ...
                        </>
                      ) : (
                        submitText
                      )}
                    </Button>
                  </>
                )}
              </DialogFooter>
            )}
          </form>
        )}
      </DialogContent>
    </Dialog>
  )
}

export default FormDialog
