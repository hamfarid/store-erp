/**
 * Enhanced Card Component with shadcn/ui
 * @file components/UI/card.jsx
 */

import * as React from "react";
import { cn } from "../../lib/utils";

const Card = React.forwardRef(({ className, variant = "default", ...props }, ref) => {
  const variants = {
    default: "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700",
    elevated: "bg-white dark:bg-gray-800 shadow-lg dark:shadow-gray-900/50",
    glass: "bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg border border-gray-200/50 dark:border-gray-700/50",
    gradient: "bg-gradient-to-br from-emerald-500/10 to-teal-500/10 dark:from-emerald-900/20 dark:to-teal-900/20 border border-emerald-200 dark:border-emerald-800",
    outlined: "bg-transparent border-2 border-gray-200 dark:border-gray-700",
  };

  return (
    <div
      ref={ref}
      className={cn(
        "rounded-xl transition-all duration-200",
        variants[variant],
        className
      )}
      {...props}
    />
  );
});
Card.displayName = "Card";

const CardHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6 pb-4", className)}
    {...props}
  />
));
CardHeader.displayName = "CardHeader";

const CardTitle = React.forwardRef(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-xl font-semibold leading-none tracking-tight text-gray-900 dark:text-gray-100",
      className
    )}
    {...props}
  />
));
CardTitle.displayName = "CardTitle";

const CardDescription = React.forwardRef(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-gray-500 dark:text-gray-400", className)}
    {...props}
  />
));
CardDescription.displayName = "CardDescription";

const CardContent = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
));
CardContent.displayName = "CardContent";

const CardFooter = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "flex items-center p-6 pt-0 border-t border-gray-100 dark:border-gray-700 mt-4",
      className
    )}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";

// Stats Card Component
const StatsCard = React.forwardRef(({ 
  className, 
  title, 
  value, 
  description, 
  icon: Icon, 
  trend,
  trendValue,
  variant = "default",
  ...props 
}, ref) => {
  const iconBgColors = {
    default: "bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400",
    blue: "bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400",
    amber: "bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400",
    red: "bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400",
    purple: "bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400",
  };

  return (
    <Card ref={ref} className={cn("p-6", className)} {...props}>
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-gray-100">{value}</p>
          {description && (
            <p className="text-xs text-gray-500 dark:text-gray-400">{description}</p>
          )}
          {trend && (
            <div className={cn(
              "flex items-center gap-1 text-sm font-medium",
              trend === 'up' ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
            )}>
              {trend === 'up' ? '↑' : '↓'} {trendValue}
            </div>
          )}
        </div>
        {Icon && (
          <div className={cn("p-3 rounded-xl", iconBgColors[variant])}>
            <Icon className="h-6 w-6" />
          </div>
        )}
      </div>
    </Card>
  );
});
StatsCard.displayName = "StatsCard";

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent, StatsCard };
