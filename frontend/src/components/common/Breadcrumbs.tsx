/**
 * P3.80: Breadcrumbs Navigation
 * 
 * Accessible breadcrumb navigation component.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

export interface BreadcrumbItem {
  label: string;
  href?: string;
  icon?: React.ReactNode;
  current?: boolean;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
  separator?: React.ReactNode;
  className?: string;
  homeIcon?: boolean;
  maxItems?: number;
  itemsBeforeCollapse?: number;
  itemsAfterCollapse?: number;
  onNavigate?: (href: string) => void;
}

// =============================================================================
// Default Separator
// =============================================================================

const DefaultSeparator = () => (
  <svg
    className="w-4 h-4 text-gray-400 rtl:rotate-180"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M9 5l7 7-7 7"
    />
  </svg>
);

// =============================================================================
// Home Icon
// =============================================================================

const HomeIcon = () => (
  <svg
    className="w-4 h-4"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
    />
  </svg>
);

// =============================================================================
// Ellipsis
// =============================================================================

const Ellipsis = () => (
  <span className="px-2 py-1 text-gray-400 cursor-default">...</span>
);

// =============================================================================
// Breadcrumb Item Component
// =============================================================================

interface BreadcrumbItemProps {
  item: BreadcrumbItem;
  isFirst: boolean;
  isLast: boolean;
  homeIcon: boolean;
  onNavigate?: (href: string) => void;
}

const BreadcrumbItemComponent: React.FC<BreadcrumbItemProps> = ({
  item,
  isFirst,
  isLast,
  homeIcon,
  onNavigate,
}) => {
  const handleClick = (e: React.MouseEvent) => {
    if (item.href && onNavigate) {
      e.preventDefault();
      onNavigate(item.href);
    }
  };

  const content = (
    <>
      {item.icon || (isFirst && homeIcon && <HomeIcon />)}
      {(!isFirst || !homeIcon) && (
        <span className={item.icon || (isFirst && homeIcon) ? 'mr-1' : ''}>
          {item.label}
        </span>
      )}
    </>
  );

  if (isLast || !item.href) {
    return (
      <span
        className={`
          inline-flex items-center text-sm font-medium
          ${isLast ? 'text-gray-700' : 'text-gray-500'}
        `}
        aria-current={isLast ? 'page' : undefined}
      >
        {content}
      </span>
    );
  }

  return (
    <a
      href={item.href}
      onClick={handleClick}
      className={`
        inline-flex items-center text-sm font-medium
        text-gray-500 hover:text-indigo-600
        transition-colors duration-150
      `}
    >
      {content}
    </a>
  );
};

// =============================================================================
// Main Component
// =============================================================================

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  items,
  separator,
  className = '',
  homeIcon = true,
  maxItems,
  itemsBeforeCollapse = 1,
  itemsAfterCollapse = 1,
  onNavigate,
}) => {
  // Collapse items if needed
  let displayItems = items;
  let collapsed = false;

  if (maxItems && items.length > maxItems) {
    const before = items.slice(0, itemsBeforeCollapse);
    const after = items.slice(-itemsAfterCollapse);
    displayItems = [...before, { label: '...', current: false }, ...after];
    collapsed = true;
  }

  const separatorElement = separator || <DefaultSeparator />;

  return (
    <nav
      className={`flex ${className}`}
      aria-label="Breadcrumb"
      dir="rtl"
    >
      <ol className="inline-flex items-center gap-2">
        {displayItems.map((item, index) => {
          const isFirst = index === 0;
          const isLast = index === displayItems.length - 1;
          const isEllipsis = collapsed && item.label === '...';

          return (
            <li
              key={isEllipsis ? 'ellipsis' : item.href || item.label}
              className="inline-flex items-center gap-2"
            >
              {!isFirst && (
                <span className="text-gray-400" aria-hidden="true">
                  {separatorElement}
                </span>
              )}
              
              {isEllipsis ? (
                <Ellipsis />
              ) : (
                <BreadcrumbItemComponent
                  item={item}
                  isFirst={isFirst}
                  isLast={isLast}
                  homeIcon={homeIcon}
                  onNavigate={onNavigate}
                />
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
};

// =============================================================================
// Page Header with Breadcrumbs
// =============================================================================

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: BreadcrumbItem[];
  actions?: React.ReactNode;
  className?: string;
  onNavigate?: (href: string) => void;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  subtitle,
  breadcrumbs,
  actions,
  className = '',
  onNavigate,
}) => {
  return (
    <div className={`mb-6 ${className}`}>
      {breadcrumbs && breadcrumbs.length > 0 && (
        <Breadcrumbs
          items={breadcrumbs}
          className="mb-3"
          onNavigate={onNavigate}
        />
      )}
      
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
          {subtitle && (
            <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
          )}
        </div>
        
        {actions && (
          <div className="flex items-center gap-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
};

// =============================================================================
// Auto Breadcrumbs (from route)
// =============================================================================

interface AutoBreadcrumbsProps {
  pathname: string;
  labels?: Record<string, string>;
  homePath?: string;
  homeLabel?: string;
  className?: string;
  onNavigate?: (href: string) => void;
}

export const AutoBreadcrumbs: React.FC<AutoBreadcrumbsProps> = ({
  pathname,
  labels = {},
  homePath = '/',
  homeLabel = 'الرئيسية',
  className = '',
  onNavigate,
}) => {
  // Parse pathname into breadcrumb items
  const segments = pathname.split('/').filter(Boolean);
  
  const items: BreadcrumbItem[] = [
    { label: homeLabel, href: homePath },
  ];

  let currentPath = '';
  segments.forEach((segment, index) => {
    currentPath += `/${segment}`;
    const isLast = index === segments.length - 1;
    
    // Get label from labels map or capitalize segment
    const label = labels[segment] || labels[currentPath] || 
      segment.charAt(0).toUpperCase() + segment.slice(1).replace(/-/g, ' ');
    
    items.push({
      label,
      href: isLast ? undefined : currentPath,
      current: isLast,
    });
  });

  return (
    <Breadcrumbs
      items={items}
      className={className}
      onNavigate={onNavigate}
    />
  );
};

// =============================================================================
// Export
// =============================================================================

export default Breadcrumbs;

