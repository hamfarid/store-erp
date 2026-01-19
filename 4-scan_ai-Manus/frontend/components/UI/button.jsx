/**
 * Enhanced Button Component with shadcn/ui + Radix
 * @file components/UI/button.jsx
 */

import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva } from "class-variance-authority";
import { Loader2 } from "lucide-react";
import { cn } from "../../lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-200 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:ring-2 focus-visible:ring-offset-2 active:scale-[0.98]",
  {
    variants: {
      variant: {
        default:
          "bg-emerald-600 text-white shadow-md hover:bg-emerald-700 focus-visible:ring-emerald-500 dark:bg-emerald-500 dark:hover:bg-emerald-600",
        destructive:
          "bg-red-600 text-white shadow-md hover:bg-red-700 focus-visible:ring-red-500 dark:bg-red-500 dark:hover:bg-red-600",
        outline:
          "border-2 border-emerald-600 text-emerald-600 bg-transparent hover:bg-emerald-50 focus-visible:ring-emerald-500 dark:border-emerald-400 dark:text-emerald-400 dark:hover:bg-emerald-950",
        secondary:
          "bg-gray-100 text-gray-900 shadow-sm hover:bg-gray-200 focus-visible:ring-gray-500 dark:bg-gray-800 dark:text-gray-100 dark:hover:bg-gray-700",
        ghost:
          "text-gray-600 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-100",
        link: 
          "text-emerald-600 underline-offset-4 hover:underline dark:text-emerald-400",
        success:
          "bg-green-600 text-white shadow-md hover:bg-green-700 focus-visible:ring-green-500 dark:bg-green-500 dark:hover:bg-green-600",
        warning:
          "bg-amber-500 text-white shadow-md hover:bg-amber-600 focus-visible:ring-amber-500 dark:bg-amber-400 dark:hover:bg-amber-500",
        info:
          "bg-blue-600 text-white shadow-md hover:bg-blue-700 focus-visible:ring-blue-500 dark:bg-blue-500 dark:hover:bg-blue-600",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-8 rounded-md gap-1.5 px-3 text-xs",
        lg: "h-12 rounded-lg px-8 text-base",
        xl: "h-14 rounded-xl px-10 text-lg",
        icon: "h-10 w-10 p-0",
        "icon-sm": "h-8 w-8 p-0",
        "icon-lg": "h-12 w-12 p-0",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

const Button = React.forwardRef(({
  className,
  variant,
  size,
  asChild = false,
  loading = false,
  leftIcon,
  rightIcon,
  children,
  disabled,
  ...props
}, ref) => {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp
      ref={ref}
      data-slot="button"
      disabled={disabled || loading}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    >
      {loading && <Loader2 className="h-4 w-4 animate-spin" />}
      {!loading && leftIcon}
      {children}
      {!loading && rightIcon}
    </Comp>
  );
});

Button.displayName = "Button";

export { Button, buttonVariants };
