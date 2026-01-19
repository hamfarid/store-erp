/**
 * Pagination Component - Advanced Pagination System
 * ==================================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useMemo } from 'react';
import { 
  ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight,
  MoreHorizontal
} from 'lucide-react';

// ============================================
// Pagination Utils
// ============================================
const getPageNumbers = (currentPage, totalPages, maxVisible = 7) => {
  const pages = [];
  
  if (totalPages <= maxVisible) {
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }

  // Always show first page
  pages.push(1);

  // Calculate start and end of visible range
  let start = Math.max(2, currentPage - 2);
  let end = Math.min(totalPages - 1, currentPage + 2);

  // Adjust if near the start
  if (currentPage <= 4) {
    end = Math.min(maxVisible - 1, totalPages - 1);
  }

  // Adjust if near the end
  if (currentPage >= totalPages - 3) {
    start = Math.max(2, totalPages - maxVisible + 2);
  }

  // Add ellipsis or pages
  if (start > 2) {
    pages.push('ellipsis-start');
  }

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }

  if (end < totalPages - 1) {
    pages.push('ellipsis-end');
  }

  // Always show last page
  if (totalPages > 1) {
    pages.push(totalPages);
  }

  return pages;
};

// ============================================
// Simple Pagination (Prev/Next only)
// ============================================
export const SimplePagination = ({
  page,
  totalPages,
  onChange,
  size = 'md',
  showInfo = true,
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';

  const sizes = {
    sm: 'text-xs py-1 px-2',
    md: 'text-sm py-1.5 px-3',
    lg: 'text-base py-2 px-4'
  };

  const PrevIcon = isRTL ? ChevronRight : ChevronLeft;
  const NextIcon = isRTL ? ChevronLeft : ChevronRight;

  return (
    <div className={`flex items-center justify-center gap-3 ${className}`}>
      <button
        onClick={() => onChange?.(page - 1)}
        disabled={page <= 1}
        className={`
          inline-flex items-center gap-1 rounded-lg border border-gray-300 dark:border-gray-600
          ${sizes[size]}
          ${page <= 1 
            ? 'opacity-50 cursor-not-allowed bg-gray-50 dark:bg-gray-800' 
            : 'hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer'
          }
          transition-colors
        `}
      >
        <PrevIcon className="w-4 h-4" />
        {isRTL ? 'التالي' : 'Previous'}
      </button>

      {showInfo && (
        <span className="text-sm text-gray-500">
          {page} / {totalPages}
        </span>
      )}

      <button
        onClick={() => onChange?.(page + 1)}
        disabled={page >= totalPages}
        className={`
          inline-flex items-center gap-1 rounded-lg border border-gray-300 dark:border-gray-600
          ${sizes[size]}
          ${page >= totalPages 
            ? 'opacity-50 cursor-not-allowed bg-gray-50 dark:bg-gray-800' 
            : 'hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer'
          }
          transition-colors
        `}
      >
        {isRTL ? 'السابق' : 'Next'}
        <NextIcon className="w-4 h-4" />
      </button>
    </div>
  );
};

// ============================================
// Full Pagination (With page numbers)
// ============================================
export const Pagination = ({
  page,
  totalPages,
  total,
  limit,
  onChange,
  onLimitChange,
  showFirstLast = true,
  showInfo = true,
  showLimitSelector = false,
  limitOptions = [10, 20, 50, 100],
  size = 'md',
  variant = 'default', // default, rounded, bordered
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';

  const pages = useMemo(() => 
    getPageNumbers(page, totalPages), 
    [page, totalPages]
  );

  const startItem = (page - 1) * limit + 1;
  const endItem = Math.min(page * limit, total);

  const sizes = {
    sm: { button: 'w-7 h-7 text-xs', nav: 'w-7 h-7' },
    md: { button: 'w-9 h-9 text-sm', nav: 'w-9 h-9' },
    lg: { button: 'w-11 h-11 text-base', nav: 'w-11 h-11' }
  };

  const variants = {
    default: {
      button: 'rounded-lg',
      active: 'bg-emerald-500 text-white',
      inactive: 'hover:bg-gray-100 dark:hover:bg-gray-700'
    },
    rounded: {
      button: 'rounded-full',
      active: 'bg-emerald-500 text-white',
      inactive: 'hover:bg-gray-100 dark:hover:bg-gray-700'
    },
    bordered: {
      button: 'rounded-lg border border-gray-300 dark:border-gray-600',
      active: 'bg-emerald-500 text-white border-emerald-500',
      inactive: 'hover:bg-gray-100 dark:hover:bg-gray-700'
    }
  };

  const currentVariant = variants[variant];
  const currentSize = sizes[size];

  const FirstIcon = isRTL ? ChevronsRight : ChevronsLeft;
  const LastIcon = isRTL ? ChevronsLeft : ChevronsRight;
  const PrevIcon = isRTL ? ChevronRight : ChevronLeft;
  const NextIcon = isRTL ? ChevronLeft : ChevronRight;

  if (totalPages <= 1 && !showInfo) return null;

  return (
    <div className={`flex flex-col sm:flex-row items-center justify-between gap-4 ${className}`}>
      {/* Info Section */}
      {showInfo && (
        <div className="text-sm text-gray-500 dark:text-gray-400">
          {isRTL 
            ? `عرض ${startItem} - ${endItem} من ${total}`
            : `Showing ${startItem} - ${endItem} of ${total}`
          }
        </div>
      )}

      {/* Pagination Controls */}
      <div className="flex items-center gap-1">
        {/* First Page */}
        {showFirstLast && (
          <button
            onClick={() => onChange?.(1)}
            disabled={page <= 1}
            className={`
              ${currentSize.nav} inline-flex items-center justify-center
              ${currentVariant.button}
              ${page <= 1 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer'
              }
              transition-colors
            `}
            title={isRTL ? 'الأول' : 'First'}
          >
            <FirstIcon className="w-4 h-4" />
          </button>
        )}

        {/* Previous Page */}
        <button
          onClick={() => onChange?.(page - 1)}
          disabled={page <= 1}
          className={`
            ${currentSize.nav} inline-flex items-center justify-center
            ${currentVariant.button}
            ${page <= 1 
              ? 'opacity-50 cursor-not-allowed' 
              : 'hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer'
            }
            transition-colors
          `}
          title={isRTL ? 'السابق' : 'Previous'}
        >
          <PrevIcon className="w-4 h-4" />
        </button>

        {/* Page Numbers */}
        {pages.map((pageNum, index) => {
          if (typeof pageNum === 'string') {
            return (
              <span 
                key={pageNum} 
                className={`${currentSize.button} inline-flex items-center justify-center text-gray-400`}
              >
                <MoreHorizontal className="w-4 h-4" />
              </span>
            );
          }

          const isActive = pageNum === page;
          return (
            <button
              key={pageNum}
              onClick={() => onChange?.(pageNum)}
              className={`
                ${currentSize.button} inline-flex items-center justify-center font-medium
                ${currentVariant.button}
                ${isActive ? currentVariant.active : currentVariant.inactive}
                transition-colors
              `}
            >
              {pageNum}
            </button>
          );
        })}

        {/* Next Page */}
        <button
          onClick={() => onChange?.(page + 1)}
          disabled={page >= totalPages}
          className={`
            ${currentSize.nav} inline-flex items-center justify-center
            ${currentVariant.button}
            ${page >= totalPages 
              ? 'opacity-50 cursor-not-allowed' 
              : 'hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer'
            }
            transition-colors
          `}
          title={isRTL ? 'التالي' : 'Next'}
        >
          <NextIcon className="w-4 h-4" />
        </button>

        {/* Last Page */}
        {showFirstLast && (
          <button
            onClick={() => onChange?.(totalPages)}
            disabled={page >= totalPages}
            className={`
              ${currentSize.nav} inline-flex items-center justify-center
              ${currentVariant.button}
              ${page >= totalPages 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer'
              }
              transition-colors
            `}
            title={isRTL ? 'الأخير' : 'Last'}
          >
            <LastIcon className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Limit Selector */}
      {showLimitSelector && (
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">
            {isRTL ? 'عرض' : 'Show'}
          </span>
          <select
            value={limit}
            onChange={(e) => onLimitChange?.(Number(e.target.value))}
            className="py-1 px-2 text-sm bg-gray-100 dark:bg-gray-800 rounded-lg border-0 focus:ring-2 focus:ring-emerald-500"
          >
            {limitOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
          <span className="text-sm text-gray-500">
            {isRTL ? 'لكل صفحة' : 'per page'}
          </span>
        </div>
      )}
    </div>
  );
};

// ============================================
// Load More Button (Alternative to Pagination)
// ============================================
export const LoadMore = ({
  hasMore,
  loading,
  onLoadMore,
  loadedCount,
  totalCount,
  size = 'md',
  className = ''
}) => {
  const isRTL = document.documentElement.dir === 'rtl';

  const sizes = {
    sm: 'py-2 px-4 text-sm',
    md: 'py-2.5 px-6 text-sm',
    lg: 'py-3 px-8 text-base'
  };

  if (!hasMore) return null;

  return (
    <div className={`text-center ${className}`}>
      <button
        onClick={onLoadMore}
        disabled={loading}
        className={`
          inline-flex items-center justify-center gap-2 rounded-lg
          bg-emerald-500 hover:bg-emerald-600 text-white font-medium
          disabled:opacity-50 disabled:cursor-not-allowed
          transition-colors
          ${sizes[size]}
        `}
      >
        {loading ? (
          <>
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            {isRTL ? 'جاري التحميل...' : 'Loading...'}
          </>
        ) : (
          <>
            {isRTL ? 'تحميل المزيد' : 'Load More'}
          </>
        )}
      </button>
      
      {totalCount && (
        <p className="mt-2 text-sm text-gray-500">
          {isRTL 
            ? `تم تحميل ${loadedCount} من ${totalCount}`
            : `Loaded ${loadedCount} of ${totalCount}`
          }
        </p>
      )}
    </div>
  );
};

// ============================================
// Infinite Scroll Trigger
// ============================================
export const InfiniteScrollTrigger = ({
  hasMore,
  loading,
  onLoadMore,
  threshold = 100,
  children
}) => {
  const triggerRef = React.useRef(null);

  React.useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loading) {
          onLoadMore?.();
        }
      },
      { rootMargin: `${threshold}px` }
    );

    if (triggerRef.current) {
      observer.observe(triggerRef.current);
    }

    return () => observer.disconnect();
  }, [hasMore, loading, onLoadMore, threshold]);

  return (
    <>
      {children}
      <div ref={triggerRef} className="h-1" />
      {loading && (
        <div className="py-4 text-center">
          <div className="w-6 h-6 mx-auto border-2 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin" />
        </div>
      )}
    </>
  );
};

export default { SimplePagination, Pagination, LoadMore, InfiniteScrollTrigger };
