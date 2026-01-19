/**
 * Enhanced Input Component with shadcn/ui
 * @file components/UI/input.jsx
 */

import * as React from "react";
import { cn } from "../../lib/utils";
import { Search, Eye, EyeOff, X } from "lucide-react";

const Input = React.forwardRef(({ 
  className, 
  type = "text",
  error,
  leftIcon: LeftIcon,
  rightIcon: RightIcon,
  clearable = false,
  onClear,
  ...props 
}, ref) => {
  const [showPassword, setShowPassword] = React.useState(false);
  const isPassword = type === "password";
  const inputType = isPassword && showPassword ? "text" : type;

  return (
    <div className="relative w-full">
      {LeftIcon && (
        <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
          <LeftIcon className="h-5 w-5" />
        </div>
      )}
      <input
        type={inputType}
        className={cn(
          "flex h-11 w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm ring-offset-white transition-all duration-200",
          "placeholder:text-gray-400 dark:placeholder:text-gray-500",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 focus-visible:border-emerald-500",
          "disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-gray-50",
          "dark:border-gray-700 dark:bg-gray-800 dark:ring-offset-gray-900 dark:text-gray-100",
          error && "border-red-500 focus-visible:ring-red-500 focus-visible:border-red-500",
          LeftIcon && "pr-10",
          (isPassword || RightIcon || clearable) && "pl-10",
          className
        )}
        ref={ref}
        {...props}
      />
      {isPassword && (
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
        </button>
      )}
      {!isPassword && RightIcon && (
        <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
          <RightIcon className="h-5 w-5" />
        </div>
      )}
      {clearable && props.value && (
        <button
          type="button"
          onClick={onClear}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <X className="h-4 w-4" />
        </button>
      )}
      {error && (
        <p className="mt-1.5 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
});

Input.displayName = "Input";

// Search Input Component
const SearchInput = React.forwardRef(({ 
  className, 
  placeholder = "بحث...",
  onSearch,
  ...props 
}, ref) => {
  return (
    <div className="relative">
      <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
      <input
        type="search"
        className={cn(
          "flex h-11 w-full rounded-lg border border-gray-200 bg-white pr-10 pl-4 py-2 text-sm",
          "placeholder:text-gray-400 dark:placeholder:text-gray-500",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:border-emerald-500",
          "dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100",
          className
        )}
        placeholder={placeholder}
        ref={ref}
        {...props}
      />
    </div>
  );
});

SearchInput.displayName = "SearchInput";

// Textarea Component
const Textarea = React.forwardRef(({ 
  className, 
  error,
  ...props 
}, ref) => {
  return (
    <div className="w-full">
      <textarea
        className={cn(
          "flex min-h-[100px] w-full rounded-lg border border-gray-200 bg-white px-4 py-3 text-sm",
          "placeholder:text-gray-400 dark:placeholder:text-gray-500",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:border-emerald-500",
          "disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-gray-50",
          "dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100",
          "resize-y",
          error && "border-red-500 focus-visible:ring-red-500",
          className
        )}
        ref={ref}
        {...props}
      />
      {error && (
        <p className="mt-1.5 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
});

Textarea.displayName = "Textarea";

// Form Field Wrapper
const FormField = React.forwardRef(({ 
  className, 
  label,
  required,
  hint,
  error,
  children,
  ...props 
}, ref) => {
  return (
    <div className={cn("space-y-2", className)} ref={ref} {...props}>
      {label && (
        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
          {label}
          {required && <span className="text-red-500 mr-1">*</span>}
        </label>
      )}
      {children}
      {hint && !error && (
        <p className="text-xs text-gray-500 dark:text-gray-400">{hint}</p>
      )}
    </div>
  );
});

FormField.displayName = "FormField";

export { Input, SearchInput, Textarea, FormField };
