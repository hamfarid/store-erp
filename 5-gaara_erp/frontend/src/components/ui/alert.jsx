// -*- javascript -*-
// FILE: frontend/src/components/ui/alert.jsx
// PURPOSE: Alert component with multiple variants
// OWNER: Frontend | LAST-AUDITED: 2025-12-08

import * as React from "react"
import { cva } from "class-variance-authority";
import { AlertCircle, CheckCircle2, Info, AlertTriangle, X } from "lucide-react";

import { cn } from "@/lib/utils"

/**
 * Alert Component
 * Display important messages with various severity levels
 * 
 * @example
 * <Alert variant="success">
 *   <AlertTitle>نجاح</AlertTitle>
 *   <AlertDescription>تم الحفظ بنجاح</AlertDescription>
 * </Alert>
 */
const alertVariants = cva(
  "relative w-full rounded-lg border px-4 py-3 text-sm grid has-[>svg]:grid-cols-[calc(var(--spacing)*4)_1fr] grid-cols-[0_1fr] has-[>svg]:gap-x-3 gap-y-0.5 items-start [&>svg]:size-4 [&>svg]:translate-y-0.5 [&>svg]:text-current",
  {
    variants: {
      variant: {
        default: "bg-card text-card-foreground border-border",
        destructive:
          "border-destructive/50 text-destructive bg-destructive/5 [&>svg]:text-destructive *:data-[slot=alert-description]:text-destructive/90",
        success:
          "border-emerald-500/50 text-emerald-800 bg-emerald-50 dark:bg-emerald-950/30 dark:text-emerald-400 [&>svg]:text-emerald-600",
        warning:
          "border-amber-500/50 text-amber-800 bg-amber-50 dark:bg-amber-950/30 dark:text-amber-400 [&>svg]:text-amber-600",
        info:
          "border-blue-500/50 text-blue-800 bg-blue-50 dark:bg-blue-950/30 dark:text-blue-400 [&>svg]:text-blue-600",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

// Icon mapping for auto-icon feature
const alertIcons = {
  default: null,
  destructive: AlertCircle,
  success: CheckCircle2,
  warning: AlertTriangle,
  info: Info,
}

function Alert({
  className,
  variant = "default",
  icon: CustomIcon,
  dismissible = false,
  onDismiss,
  children,
  ...props
}) {
  const [dismissed, setDismissed] = React.useState(false);

  if (dismissed) return null;

  // Auto-select icon based on variant if no custom icon provided
  const IconComponent = CustomIcon ?? alertIcons[variant];

  const handleDismiss = () => {
    setDismissed(true);
    onDismiss?.();
  };

  return (
    <div
      data-slot="alert"
      role="alert"
      className={cn(alertVariants({ variant }), className)}
      {...props}
    >
      {IconComponent && <IconComponent className="h-4 w-4" />}
      {children}
      {dismissible && (
        <button
          onClick={handleDismiss}
          className="absolute top-3 left-3 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          aria-label="إغلاق"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}

function AlertTitle({
  className,
  ...props
}) {
  return (
    <div
      data-slot="alert-title"
      className={cn("col-start-2 line-clamp-1 min-h-4 font-medium tracking-tight", className)}
      {...props} />
  );
}

function AlertDescription({
  className,
  ...props
}) {
  return (
    <div
      data-slot="alert-description"
      className={cn(
        "text-muted-foreground col-start-2 grid justify-items-start gap-1 text-sm [&_p]:leading-relaxed",
        className
      )}
      {...props} />
  );
}

export { Alert, AlertTitle, AlertDescription, alertVariants }
