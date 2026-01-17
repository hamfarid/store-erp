/**
 * usePagination Hook
 * @file frontend/src/hooks/usePagination.js
 * 
 * Hook لإدارة التصفح بين الصفحات
 */

import { useState, useMemo, useCallback } from 'react';

/**
 * Hook لإدارة التصفح بين الصفحات
 * @param {Object} options - خيارات التصفح
 * @param {number} options.totalItems - إجمالي العناصر
 * @param {number} options.initialPage - الصفحة الأولى (افتراضي: 1)
 * @param {number} options.initialPageSize - حجم الصفحة الافتراضي
 * @param {number[]} options.pageSizeOptions - خيارات حجم الصفحة
 */
export function usePagination({
  totalItems = 0,
  initialPage = 1,
  initialPageSize = 10,
  pageSizeOptions = [5, 10, 20, 50, 100]
} = {}) {
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [pageSize, setPageSize] = useState(initialPageSize);

  // حساب إجمالي الصفحات
  const totalPages = useMemo(() => {
    return Math.ceil(totalItems / pageSize) || 1;
  }, [totalItems, pageSize]);

  // التأكد من أن الصفحة الحالية صالحة
  const validPage = useMemo(() => {
    if (currentPage < 1) return 1;
    if (currentPage > totalPages) return totalPages;
    return currentPage;
  }, [currentPage, totalPages]);

  // حساب نطاق العناصر الحالية
  const itemRange = useMemo(() => {
    const start = (validPage - 1) * pageSize + 1;
    const end = Math.min(validPage * pageSize, totalItems);
    return { start, end };
  }, [validPage, pageSize, totalItems]);

  // حساب الـ offset للـ API
  const offset = useMemo(() => {
    return (validPage - 1) * pageSize;
  }, [validPage, pageSize]);

  // الانتقال لصفحة محددة
  const goToPage = useCallback((page) => {
    const pageNumber = Math.max(1, Math.min(page, totalPages));
    setCurrentPage(pageNumber);
  }, [totalPages]);

  // الصفحة التالية
  const nextPage = useCallback(() => {
    if (validPage < totalPages) {
      setCurrentPage(validPage + 1);
    }
  }, [validPage, totalPages]);

  // الصفحة السابقة
  const prevPage = useCallback(() => {
    if (validPage > 1) {
      setCurrentPage(validPage - 1);
    }
  }, [validPage]);

  // الصفحة الأولى
  const firstPage = useCallback(() => {
    setCurrentPage(1);
  }, []);

  // الصفحة الأخيرة
  const lastPage = useCallback(() => {
    setCurrentPage(totalPages);
  }, [totalPages]);

  // تغيير حجم الصفحة
  const changePageSize = useCallback((newSize) => {
    setPageSize(newSize);
    // إعادة التعيين للصفحة الأولى عند تغيير الحجم
    setCurrentPage(1);
  }, []);

  // إعادة التعيين
  const reset = useCallback(() => {
    setCurrentPage(initialPage);
    setPageSize(initialPageSize);
  }, [initialPage, initialPageSize]);

  // حساب أرقام الصفحات للعرض
  const pageNumbers = useMemo(() => {
    const delta = 2; // عدد الصفحات على كل جانب
    const range = [];
    const rangeWithDots = [];

    for (
      let i = Math.max(2, validPage - delta);
      i <= Math.min(totalPages - 1, validPage + delta);
      i++
    ) {
      range.push(i);
    }

    if (validPage - delta > 2) {
      rangeWithDots.push(1, '...');
    } else {
      rangeWithDots.push(1);
    }

    rangeWithDots.push(...range);

    if (validPage + delta < totalPages - 1) {
      rangeWithDots.push('...', totalPages);
    } else if (totalPages > 1) {
      rangeWithDots.push(totalPages);
    }

    return rangeWithDots;
  }, [validPage, totalPages]);

  // معلومات الحالة
  const canGoPrev = validPage > 1;
  const canGoNext = validPage < totalPages;
  const isFirstPage = validPage === 1;
  const isLastPage = validPage === totalPages;

  return {
    // الحالة
    currentPage: validPage,
    pageSize,
    totalPages,
    totalItems,
    
    // النطاق
    itemRange,
    offset,
    limit: pageSize,
    
    // الدوال
    goToPage,
    nextPage,
    prevPage,
    firstPage,
    lastPage,
    changePageSize,
    reset,
    
    // معلومات إضافية
    pageNumbers,
    pageSizeOptions,
    canGoPrev,
    canGoNext,
    isFirstPage,
    isLastPage,
    
    // للـ API
    paginationParams: {
      page: validPage,
      limit: pageSize,
      offset
    }
  };
}

/**
 * Hook للتصفح مع البيانات المحلية
 * @param {Array} data - البيانات الكاملة
 * @param {Object} options - خيارات التصفح
 */
export function useLocalPagination(data = [], options = {}) {
  const pagination = usePagination({
    totalItems: data.length,
    ...options
  });

  // تقطيع البيانات حسب الصفحة الحالية
  const paginatedData = useMemo(() => {
    const start = pagination.offset;
    const end = start + pagination.pageSize;
    return data.slice(start, end);
  }, [data, pagination.offset, pagination.pageSize]);

  return {
    ...pagination,
    data: paginatedData,
    allData: data
  };
}

export default usePagination;
