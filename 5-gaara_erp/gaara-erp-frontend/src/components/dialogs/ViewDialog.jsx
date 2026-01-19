/**
 * View Dialog Component - مكون عرض التفاصيل
 * Gaara ERP v12
 *
 * Reusable view dialog for displaying item details.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

import { X, Loader2 } from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'

/**
 * Detail Row Component
 */
function DetailRow({ label, value, valueClassName = '' }) {
  if (value === undefined || value === null) return null

  return (
    <div className="flex justify-between items-start py-2">
      <span className="text-muted-foreground text-sm">{label}</span>
      <span className={`font-medium text-sm text-left ${valueClassName}`}>
        {value}
      </span>
    </div>
  )
}

/**
 * Detail Section Component
 */
function DetailSection({ title, children }) {
  return (
    <div className="space-y-1">
      <h4 className="font-semibold text-sm text-primary">{title}</h4>
      <div className="bg-muted/30 rounded-lg p-3">{children}</div>
    </div>
  )
}

/**
 * ViewDialog Component
 */
export function ViewDialog({
  open,
  onOpenChange,
  title,
  subtitle,
  children,
  isLoading = false,
  size = 'md',
  actions,
  badge,
}) {
  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-[90vw]',
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className={sizeClasses[size]}>
        <DialogHeader className="space-y-3">
          <div className="flex items-start justify-between">
            <div>
              <DialogTitle className="flex items-center gap-2">
                {title}
                {badge && (
                  <Badge variant={badge.variant || 'default'}>
                    {badge.text}
                  </Badge>
                )}
              </DialogTitle>
              {subtitle && (
                <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>
              )}
            </div>
            {actions && <div className="flex gap-2">{actions}</div>}
          </div>
        </DialogHeader>

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
          </div>
        ) : (
          <ScrollArea className="max-h-[70vh]">
            <div className="space-y-4 pr-4">{children}</div>
          </ScrollArea>
        )}
      </DialogContent>
    </Dialog>
  )
}

ViewDialog.Row = DetailRow
ViewDialog.Section = DetailSection

export default ViewDialog
