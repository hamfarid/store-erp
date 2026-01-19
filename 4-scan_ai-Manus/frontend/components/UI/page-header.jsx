/**
 * Page Header Component - Reusable Header for All Pages
 * @file components/UI/page-header.jsx
 */

import * as React from "react";
import { cn } from "../../lib/utils";
import { Button } from "./button";
import { Badge } from "./badge";
import { ArrowRight, Plus, Download, RefreshCw, Filter, Settings } from "lucide-react";
import { useNavigate } from "react-router-dom";

const PageHeader = React.forwardRef(({
  className,
  title,
  description,
  icon: Icon,
  iconColor = "emerald",
  badge,
  badgeVariant = "secondary",
  backUrl,
  actions,
  children,
  ...props
}, ref) => {
  const navigate = useNavigate();
  
  const iconColors = {
    emerald: "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400",
    blue: "bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400",
    amber: "bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400",
    red: "bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400",
    purple: "bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400",
    gray: "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400",
  };

  return (
    <div
      ref={ref}
      className={cn(
        "flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6",
        className
      )}
      {...props}
    >
      <div className="flex items-start gap-4">
        {backUrl && (
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate(backUrl)}
            className="mt-1"
          >
            <ArrowRight className="h-5 w-5" />
          </Button>
        )}
        <div className="flex items-center gap-3">
          {Icon && (
            <div className={cn("w-12 h-12 rounded-xl flex items-center justify-center", iconColors[iconColor])}>
              <Icon className="h-6 w-6" />
            </div>
          )}
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {title}
              </h1>
              {badge && (
                <Badge variant={badgeVariant} size="lg">{badge}</Badge>
              )}
            </div>
            {description && (
              <p className="text-gray-500 dark:text-gray-400 mt-1">{description}</p>
            )}
          </div>
        </div>
      </div>
      
      {(actions || children) && (
        <div className="flex items-center gap-2">
          {actions}
          {children}
        </div>
      )}
    </div>
  );
});

PageHeader.displayName = "PageHeader";

// Page Actions Component
const PageActions = React.forwardRef(({
  onAdd,
  onExport,
  onRefresh,
  onFilter,
  onSettings,
  addLabel = "إضافة جديد",
  showAdd = true,
  showExport = false,
  showRefresh = false,
  showFilter = false,
  showSettings = false,
  loading = false,
  customActions,
  className,
  ...props
}, ref) => {
  return (
    <div ref={ref} className={cn("flex items-center gap-2", className)} {...props}>
      {showRefresh && onRefresh && (
        <Button variant="ghost" size="icon-sm" onClick={onRefresh} disabled={loading}>
          <RefreshCw className={cn("h-4 w-4", loading && "animate-spin")} />
        </Button>
      )}
      {showFilter && onFilter && (
        <Button variant="outline" size="sm" onClick={onFilter}>
          <Filter className="h-4 w-4" />
          <span className="hidden sm:inline">تصفية</span>
        </Button>
      )}
      {showExport && onExport && (
        <Button variant="outline" size="sm" onClick={onExport}>
          <Download className="h-4 w-4" />
          <span className="hidden sm:inline">تصدير</span>
        </Button>
      )}
      {showSettings && onSettings && (
        <Button variant="ghost" size="icon-sm" onClick={onSettings}>
          <Settings className="h-4 w-4" />
        </Button>
      )}
      {customActions}
      {showAdd && onAdd && (
        <Button onClick={onAdd}>
          <Plus className="h-4 w-4" />
          {addLabel}
        </Button>
      )}
    </div>
  );
});

PageActions.displayName = "PageActions";

// Page Container Component
const PageContainer = React.forwardRef(({
  className,
  children,
  maxWidth = "full",
  padding = true,
  ...props
}, ref) => {
  const maxWidths = {
    sm: "max-w-2xl",
    md: "max-w-4xl",
    lg: "max-w-6xl",
    xl: "max-w-7xl",
    full: "max-w-full",
  };

  return (
    <div
      ref={ref}
      className={cn(
        "mx-auto",
        maxWidths[maxWidth],
        padding && "px-4 sm:px-6 lg:px-8 py-6",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
});

PageContainer.displayName = "PageContainer";

// Section Component
const Section = React.forwardRef(({
  className,
  title,
  description,
  actions,
  children,
  collapsible = false,
  defaultCollapsed = false,
  ...props
}, ref) => {
  const [collapsed, setCollapsed] = React.useState(defaultCollapsed);

  return (
    <div ref={ref} className={cn("space-y-4", className)} {...props}>
      {(title || description || actions) && (
        <div className="flex items-center justify-between">
          <div>
            {title && (
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                {title}
              </h2>
            )}
            {description && (
              <p className="text-sm text-gray-500 dark:text-gray-400">{description}</p>
            )}
          </div>
          {actions}
        </div>
      )}
      {(!collapsible || !collapsed) && children}
    </div>
  );
});

Section.displayName = "Section";

// Empty State Component
const EmptyState = React.forwardRef(({
  className,
  icon: Icon,
  title = "لا توجد بيانات",
  description = "لم يتم العثور على أي سجلات",
  action,
  actionLabel = "إضافة جديد",
  ...props
}, ref) => {
  return (
    <div
      ref={ref}
      className={cn(
        "flex flex-col items-center justify-center py-16 text-center",
        className
      )}
      {...props}
    >
      {Icon && (
        <div className="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
          <Icon className="h-8 w-8 text-gray-400" />
        </div>
      )}
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
        {title}
      </h3>
      <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-sm">
        {description}
      </p>
      {action && (
        <Button onClick={action}>
          <Plus className="h-4 w-4" />
          {actionLabel}
        </Button>
      )}
    </div>
  );
});

EmptyState.displayName = "EmptyState";

// Loading State Component
const LoadingState = React.forwardRef(({
  className,
  text = "جاري التحميل...",
  ...props
}, ref) => {
  return (
    <div
      ref={ref}
      className={cn(
        "flex flex-col items-center justify-center py-16 text-center",
        className
      )}
      {...props}
    >
      <div className="w-12 h-12 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin mb-4" />
      <p className="text-gray-500 dark:text-gray-400">{text}</p>
    </div>
  );
});

LoadingState.displayName = "LoadingState";

export {
  PageHeader,
  PageActions,
  PageContainer,
  Section,
  EmptyState,
  LoadingState,
};

