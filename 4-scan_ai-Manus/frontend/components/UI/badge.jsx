/**
 * Enhanced Badge Component with shadcn/ui
 * @file components/UI/badge.jsx
 */

import * as React from "react";
import { cva } from "class-variance-authority";
import { cn } from "../../lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        default:
          "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400",
        secondary:
          "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300",
        destructive:
          "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
        warning:
          "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400",
        success:
          "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
        info:
          "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
        purple:
          "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400",
        outline:
          "border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300",
      },
      size: {
        default: "px-2.5 py-0.5 text-xs",
        sm: "px-2 py-0.5 text-[10px]",
        lg: "px-3 py-1 text-sm",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

const Badge = React.forwardRef(({ className, variant, size, ...props }, ref) => (
  <span
    ref={ref}
    className={cn(badgeVariants({ variant, size }), className)}
    {...props}
  />
));

Badge.displayName = "Badge";

// Status Badge with dot indicator
const StatusBadge = React.forwardRef(({ status, label, className, ...props }, ref) => {
  const statusConfig = {
    active: { variant: "success", dot: "bg-green-500", label: label || "نشط" },
    inactive: { variant: "secondary", dot: "bg-gray-400", label: label || "غير نشط" },
    pending: { variant: "warning", dot: "bg-amber-500", label: label || "قيد الانتظار" },
    error: { variant: "destructive", dot: "bg-red-500", label: label || "خطأ" },
    processing: { variant: "info", dot: "bg-blue-500 animate-pulse", label: label || "جاري المعالجة" },
  };

  const config = statusConfig[status] || statusConfig.inactive;

  return (
    <Badge ref={ref} variant={config.variant} className={cn("gap-1.5", className)} {...props}>
      <span className={cn("w-1.5 h-1.5 rounded-full", config.dot)} />
      {config.label}
    </Badge>
  );
});

StatusBadge.displayName = "StatusBadge";

export { Badge, badgeVariants, StatusBadge };
