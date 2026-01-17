// FILE: frontend/src/components/ui/AccessibleButton.jsx | PURPOSE: WCAG AA Compliant Button Component | OWNER: Frontend | RELATED: accessibility.css | LAST-AUDITED: 2025-10-21

import React, { forwardRef } from 'react';
import { cn } from '../../lib/utils';

/**
 * Accessible Button Component - WCAG AA Compliant
 * 
 * P2 Fixes Applied:
 * - P2.1: WCAG AA color contrast ratios
 * - P2.2: Proper ARIA attributes
 * - P2.3: Keyboard navigation support
 * - P2.4: Screen reader compatibility
 */

const AccessibleButton = forwardRef(({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  ariaLabel,
  ariaDescribedBy,
  onClick,
  type = 'button',
  className,
  ...props
}, ref) => {

  const baseClasses = "btn-accessible inline-flex items-center justify-center font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50";

  const variants = {
    primary: "bg-primary text-primary-foreground hover:bg-primary/90 focus-visible:ring-primary",
    secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80 focus-visible:ring-secondary",
    destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90 focus-visible:ring-destructive",
    outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground focus-visible:ring-ring",
    ghost: "hover:bg-accent hover:text-accent-foreground focus-visible:ring-ring",
    link: "text-primary underline-offset-4 hover:underline focus-visible:ring-primary"
  };

  const sizes = {
    small: "h-9 px-3 text-sm",
    medium: "h-11 px-4 py-2",
    large: "h-12 px-6 py-3 text-lg",
    icon: "h-10 w-10"
  };

  const buttonClasses = cn(
    baseClasses,
    variants[variant],
    sizes[size],
    className
  );

  const handleClick = (e) => {
    if (disabled || loading) {
      e.preventDefault();
      return;
    }
    onClick?.(e);
  };

  const handleKeyDown = (e) => {
    // Enhanced keyboard support
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick(e);
    }
  };

  return (
    <button
      ref={ref}
      type={type}
      className={buttonClasses}
      disabled={disabled || loading}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      aria-label={ariaLabel}
      aria-describedby={ariaDescribedBy}
      aria-disabled={disabled || loading}
      role="button"
      tabIndex={disabled ? -1 : 0}
      {...props}
    >
      {loading && (
        <div className="loading-spinner mr-2 h-4 w-4" aria-hidden="true" />
      )}
      {children}
      {loading && <span className="sr-only">جاري التحميل...</span>}
    </button>
  );
});

AccessibleButton.displayName = "AccessibleButton";

export default AccessibleButton;
