/**
 * P3.90: Empty State Component
 * 
 * Empty state placeholders for various scenarios.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  secondaryAction?: React.ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

// =============================================================================
// Default Icons
// =============================================================================

const EmptyBoxIcon: React.FC<{ className?: string }> = ({ className = '' }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
      d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
  </svg>
);

const SearchIcon: React.FC<{ className?: string }> = ({ className = '' }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
);

const DocumentIcon: React.FC<{ className?: string }> = ({ className = '' }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
);

const ShoppingCartIcon: React.FC<{ className?: string }> = ({ className = '' }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
      d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
  </svg>
);

const UsersIcon: React.FC<{ className?: string }> = ({ className = '' }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
      d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>
);

const ErrorIcon: React.FC<{ className?: string }> = ({ className = '' }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
  </svg>
);

// =============================================================================
// Empty State Component
// =============================================================================

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  action,
  secondaryAction,
  className = '',
  size = 'md',
}) => {
  const sizeClasses = {
    sm: {
      container: 'py-8',
      icon: 'w-12 h-12',
      title: 'text-base',
      description: 'text-sm',
    },
    md: {
      container: 'py-12',
      icon: 'w-16 h-16',
      title: 'text-lg',
      description: 'text-sm',
    },
    lg: {
      container: 'py-16',
      icon: 'w-20 h-20',
      title: 'text-xl',
      description: 'text-base',
    },
  };

  const sizes = sizeClasses[size];

  return (
    <div className={`text-center ${sizes.container} ${className}`} dir="rtl">
      {/* Icon */}
      <div className="mx-auto mb-4 text-gray-400">
        {icon || <EmptyBoxIcon className={sizes.icon} />}
      </div>

      {/* Title */}
      <h3 className={`font-medium text-gray-900 ${sizes.title}`}>
        {title}
      </h3>

      {/* Description */}
      {description && (
        <p className={`mt-2 text-gray-500 max-w-md mx-auto ${sizes.description}`}>
          {description}
        </p>
      )}

      {/* Actions */}
      {(action || secondaryAction) && (
        <div className="mt-6 flex items-center justify-center gap-3">
          {action}
          {secondaryAction}
        </div>
      )}
    </div>
  );
};

// =============================================================================
// Pre-built Empty States
// =============================================================================

interface PrebuiltEmptyStateProps {
  action?: React.ReactNode;
  className?: string;
}

export const NoResults: React.FC<PrebuiltEmptyStateProps> = ({ action, className }) => (
  <EmptyState
    icon={<SearchIcon className="w-16 h-16" />}
    title="لا توجد نتائج"
    description="لم يتم العثور على نتائج تطابق بحثك. حاول تغيير كلمات البحث أو تصفية النتائج."
    action={action}
    className={className}
  />
);

export const NoData: React.FC<PrebuiltEmptyStateProps> = ({ action, className }) => (
  <EmptyState
    icon={<DocumentIcon className="w-16 h-16" />}
    title="لا توجد بيانات"
    description="لم يتم إضافة أي بيانات بعد. ابدأ بإضافة بيانات جديدة."
    action={action}
    className={className}
  />
);

export const NoProducts: React.FC<PrebuiltEmptyStateProps> = ({ action, className }) => (
  <EmptyState
    icon={<EmptyBoxIcon className="w-16 h-16" />}
    title="لا توجد منتجات"
    description="لم يتم إضافة أي منتجات بعد. ابدأ بإضافة منتجاتك الأولى."
    action={action}
    className={className}
  />
);

export const EmptyCart: React.FC<PrebuiltEmptyStateProps> = ({ action, className }) => (
  <EmptyState
    icon={<ShoppingCartIcon className="w-16 h-16" />}
    title="سلة التسوق فارغة"
    description="لم تقم بإضافة أي منتجات إلى سلة التسوق بعد."
    action={action}
    className={className}
  />
);

export const NoCustomers: React.FC<PrebuiltEmptyStateProps> = ({ action, className }) => (
  <EmptyState
    icon={<UsersIcon className="w-16 h-16" />}
    title="لا يوجد عملاء"
    description="لم يتم إضافة أي عملاء بعد. قم بإضافة عملائك للبدء."
    action={action}
    className={className}
  />
);

export const ErrorState: React.FC<PrebuiltEmptyStateProps & { message?: string }> = ({ 
  action, 
  className,
  message 
}) => (
  <EmptyState
    icon={<ErrorIcon className="w-16 h-16 text-red-400" />}
    title="حدث خطأ"
    description={message || "حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى."}
    action={action}
    className={className}
  />
);

export const NoAccess: React.FC<PrebuiltEmptyStateProps> = ({ action, className }) => (
  <EmptyState
    icon={
      <svg className="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
    }
    title="لا يوجد صلاحية"
    description="ليس لديك صلاحية للوصول إلى هذه الصفحة."
    action={action}
    className={className}
  />
);

export const ComingSoon: React.FC<PrebuiltEmptyStateProps> = ({ action, className }) => (
  <EmptyState
    icon={
      <svg className="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
      </svg>
    }
    title="قريباً"
    description="هذه الميزة قيد التطوير وستكون متاحة قريباً."
    action={action}
    className={className}
  />
);

// =============================================================================
// Export
// =============================================================================

export default EmptyState;

