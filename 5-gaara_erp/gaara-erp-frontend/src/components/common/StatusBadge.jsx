import { Badge } from "@/components/ui/badge"
import { CheckCircle2, XCircle, Clock, AlertCircle } from "lucide-react"
import { cn } from "@/lib/utils"

/**
 * StatusBadge Component
 * A reusable status badge with icons and colors
 */

const STATUS_CONFIG = {
  active: {
    label: "نشط",
    variant: "default",
    icon: CheckCircle2,
    className: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400",
  },
  inactive: {
    label: "معطل",
    variant: "secondary",
    icon: XCircle,
    className: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-400",
  },
  pending: {
    label: "قيد الانتظار",
    variant: "outline",
    icon: Clock,
    className: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
  },
  error: {
    label: "خطأ",
    variant: "destructive",
    icon: AlertCircle,
    className: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  },
  online: {
    label: "متصل",
    variant: "default",
    icon: CheckCircle2,
    className: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400",
  },
  offline: {
    label: "غير متصل",
    variant: "secondary",
    icon: XCircle,
    className: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-400",
  },
  paid: {
    label: "مدفوع",
    variant: "default",
    icon: CheckCircle2,
    className: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400",
  },
  unpaid: {
    label: "غير مدفوع",
    variant: "outline",
    icon: Clock,
    className: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
  },
  overdue: {
    label: "متأخر",
    variant: "destructive",
    icon: AlertCircle,
    className: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
  },
}

export function StatusBadge({ status, customLabel, className, showIcon = true, size = "default" }) {
  const config = STATUS_CONFIG[status?.toLowerCase()] || STATUS_CONFIG.inactive
  const Icon = config.icon
  const label = customLabel || config.label

  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    default: "text-sm px-2.5 py-1",
    lg: "text-base px-3 py-1.5",
  }

  return (
    <Badge
      variant={config.variant}
      className={cn(
        "inline-flex items-center gap-1.5",
        config.className,
        sizeClasses[size],
        className
      )}
    >
      {showIcon && <Icon className="w-3 h-3" />}
      {label}
    </Badge>
  )
}
