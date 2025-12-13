// -*- javascript -*-
// FILE: frontend/src/components/ui/input.jsx
// PURPOSE: Enhanced Input Component with RTL & validation support
// OWNER: Frontend | LAST-AUDITED: 2025-12-08

import * as React from "react"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const inputVariants = cva(
  [
    // Base styles
    "flex w-full min-w-0 rounded-md border bg-background px-3 py-2 text-sm",
    "transition-all duration-200 outline-none",
    // Placeholder & file styles
    "placeholder:text-muted-foreground",
    "file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground",
    // Selection styles
    "selection:bg-primary selection:text-primary-foreground",
    // Focus styles
    "focus-visible:border-ring focus-visible:ring-2 focus-visible:ring-ring/30",
    // Disabled styles
    "disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-muted",
    // Invalid styles
    "aria-invalid:border-destructive aria-invalid:ring-destructive/20",
    // Dark mode adjustments
    "dark:bg-input/30",
  ],
  {
    variants: {
      size: {
        default: "h-10",
        sm: "h-9 text-xs",
        lg: "h-11 text-base",
      },
      variant: {
        default: "border-input",
        filled: "border-transparent bg-muted",
        ghost: "border-transparent hover:bg-accent",
      },
    },
    defaultVariants: {
      size: "default",
      variant: "default",
    },
  }
);

/**
 * Enhanced Input Component
 * 
 * @example
 * // Basic usage
 * <Input placeholder="أدخل النص هنا..." />
 * 
 * @example
 * // With validation state
 * <Input aria-invalid={!!error} />
 * 
 * @example
 * // Different sizes
 * <Input size="sm" />
 * <Input size="lg" />
 * 
 * @example
 * // With icon
 * <div className="relative">
 *   <Search className="absolute right-3 top-3 h-4 w-4 text-muted-foreground" />
 *   <Input className="pr-9" placeholder="بحث..." />
 * </div>
 */
const Input = React.forwardRef(({
  className,
  type = "text",
  size,
  variant,
  ...props
}, ref) => {
  return (
    <input
      ref={ref}
      type={type}
      data-slot="input"
      className={cn(inputVariants({ size, variant }), className)}
      {...props}
    />
  );
});

Input.displayName = "Input";

export { Input, inputVariants }
