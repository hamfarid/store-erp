/**
 * useDebounce Hook
 * @file frontend/src/hooks/useDebounce.js
 * 
 * Hook لتأخير تنفيذ القيم أو الدوال
 */

import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Hook لتأخير قيمة
 * @param {any} value - القيمة المراد تأخيرها
 * @param {number} delay - وقت التأخير بالمللي ثانية
 * @returns {any} - القيمة المؤجلة
 */
export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook لتأخير دالة
 * @param {Function} callback - الدالة المراد تأخيرها
 * @param {number} delay - وقت التأخير بالمللي ثانية
 * @returns {Function} - الدالة المؤجلة
 */
export function useDebouncedCallback(callback, delay = 300) {
  const callbackRef = useRef(callback);
  const timerRef = useRef(null);

  // Update ref when callback changes
  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  const debouncedCallback = useCallback((...args) => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }

    timerRef.current = setTimeout(() => {
      callbackRef.current(...args);
    }, delay);
  }, [delay]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, []);

  // Cancel function
  const cancel = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  // Flush function - execute immediately
  const flush = useCallback((...args) => {
    cancel();
    callbackRef.current(...args);
  }, [cancel]);

  return { debouncedCallback, cancel, flush };
}

/**
 * Hook للبحث المؤجل
 * @param {string} searchTerm - مصطلح البحث
 * @param {number} delay - وقت التأخير
 * @returns {Object} - القيمة المؤجلة وحالة التحميل
 */
export function useDebouncedSearch(searchTerm, delay = 300) {
  const [debouncedTerm, setDebouncedTerm] = useState(searchTerm);
  const [isDebouncing, setIsDebouncing] = useState(false);

  useEffect(() => {
    if (searchTerm !== debouncedTerm) {
      setIsDebouncing(true);
    }

    const timer = setTimeout(() => {
      setDebouncedTerm(searchTerm);
      setIsDebouncing(false);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [searchTerm, delay]);

  return { debouncedTerm, isDebouncing };
}

export default useDebounce;
