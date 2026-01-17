/**
 * useClickOutside Hook
 * @file frontend/src/hooks/useClickOutside.js
 * 
 * Hook للكشف عن النقر خارج عنصر معين
 */

import { useEffect, useRef, useCallback } from 'react';

/**
 * Hook للكشف عن النقر خارج عنصر
 * @param {Function} callback - الدالة المراد تنفيذها عند النقر خارج العنصر
 * @param {boolean} enabled - تفعيل/تعطيل الكشف (افتراضي: true)
 * @returns {React.RefObject} - المرجع للربط بالعنصر
 */
export function useClickOutside(callback, enabled = true) {
  const ref = useRef(null);
  const callbackRef = useRef(callback);

  // Update callback ref
  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    if (!enabled) return;

    const handleClick = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        callbackRef.current(event);
      }
    };

    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        callbackRef.current(event);
      }
    };

    document.addEventListener('mousedown', handleClick);
    document.addEventListener('touchstart', handleClick);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('mousedown', handleClick);
      document.removeEventListener('touchstart', handleClick);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [enabled]);

  return ref;
}

/**
 * Hook للكشف عن النقر خارج عدة عناصر
 * @param {Function} callback - الدالة المراد تنفيذها
 * @param {boolean} enabled - تفعيل/تعطيل الكشف
 * @returns {Function} - دالة لإنشاء مراجع جديدة
 */
export function useClickOutsideMultiple(callback, enabled = true) {
  const refs = useRef([]);
  const callbackRef = useRef(callback);

  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    if (!enabled) return;

    const handleClick = (event) => {
      const isOutside = refs.current.every(
        (ref) => ref && !ref.contains(event.target)
      );
      
      if (isOutside) {
        callbackRef.current(event);
      }
    };

    document.addEventListener('mousedown', handleClick);
    document.addEventListener('touchstart', handleClick);

    return () => {
      document.removeEventListener('mousedown', handleClick);
      document.removeEventListener('touchstart', handleClick);
    };
  }, [enabled]);

  const addRef = useCallback((element) => {
    if (element && !refs.current.includes(element)) {
      refs.current.push(element);
    }
  }, []);

  const removeRef = useCallback((element) => {
    refs.current = refs.current.filter((ref) => ref !== element);
  }, []);

  return { addRef, removeRef, refs: refs.current };
}

/**
 * Hook لإدارة حالة القائمة المنسدلة
 * @param {boolean} initialState - الحالة الأولية
 * @returns {Object} - { isOpen, open, close, toggle, ref }
 */
export function useDropdown(initialState = false) {
  const [isOpen, setIsOpen] = useState(initialState);

  const close = useCallback(() => setIsOpen(false), []);
  const open = useCallback(() => setIsOpen(true), []);
  const toggle = useCallback(() => setIsOpen((prev) => !prev), []);

  const ref = useClickOutside(close, isOpen);

  return { isOpen, open, close, toggle, ref };
}

// Import useState for useDropdown
import { useState } from 'react';

export default useClickOutside;
