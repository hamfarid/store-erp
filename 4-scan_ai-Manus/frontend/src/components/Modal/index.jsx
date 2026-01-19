/**
 * Modal Component
 * =================
 * 
 * Reusable modal dialog with animations and accessibility.
 * 
 * Features:
 * - Smooth animations
 * - Click outside to close
 * - ESC key to close
 * - Focus trap
 * - Multiple sizes
 * - Header/Footer slots
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useEffect, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { X, AlertTriangle, CheckCircle, Info, AlertCircle } from 'lucide-react';

/**
 * Modal Component
 */
const Modal = ({
  isOpen = false,
  onClose,
  title,
  titleAr,
  children,
  footer,
  size = 'md',
  closeOnOverlay = true,
  closeOnEsc = true,
  showCloseButton = true,
  className = ''
}) => {
  const modalRef = useRef(null);
  const isRTL = document.documentElement.dir === 'rtl';
  const displayTitle = isRTL ? (titleAr || title) : title;

  // Size classes
  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
    '3xl': 'max-w-3xl',
    full: 'max-w-full mx-4'
  };

  // Handle ESC key
  const handleKeyDown = useCallback((e) => {
    if (closeOnEsc && e.key === 'Escape') {
      onClose?.();
    }
  }, [closeOnEsc, onClose]);

  // Handle overlay click
  const handleOverlayClick = (e) => {
    if (closeOnOverlay && e.target === e.currentTarget) {
      onClose?.();
    }
  };

  // Lock body scroll and add event listener
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      document.addEventListener('keydown', handleKeyDown);
      
      // Focus the modal
      modalRef.current?.focus();
    }
    
    return () => {
      document.body.style.overflow = '';
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, handleKeyDown]);

  if (!isOpen) return null;

  const modalContent = (
    <div
      className="
        fixed inset-0 z-50 flex items-center justify-center p-4
        bg-black/50 backdrop-blur-sm
        animate-fadeIn
      "
      onClick={handleOverlayClick}
    >
      <div
        ref={modalRef}
        tabIndex={-1}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className={`
          relative w-full ${sizes[size]}
          bg-white dark:bg-gray-800
          rounded-2xl shadow-2xl
          transform transition-all duration-300
          animate-scaleIn
          ${className}
        `}
      >
        {/* Header */}
        {(displayTitle || showCloseButton) && (
          <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
            {displayTitle && (
              <h2 id="modal-title" className="text-lg font-semibold text-gray-800 dark:text-white">
                {displayTitle}
              </h2>
            )}
            {showCloseButton && (
              <button
                onClick={onClose}
                className="
                  p-2 rounded-lg
                  text-gray-400 hover:text-gray-600 dark:hover:text-gray-200
                  hover:bg-gray-100 dark:hover:bg-gray-700
                  transition-colors
                "
                aria-label="Close"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        )}

        {/* Body */}
        <div className="p-4 max-h-[70vh] overflow-y-auto">
          {children}
        </div>

        {/* Footer */}
        {footer && (
          <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3">
            {footer}
          </div>
        )}
      </div>
    </div>
  );

  return createPortal(modalContent, document.body);
};

/**
 * Confirm Dialog
 */
export const ConfirmDialog = ({
  isOpen = false,
  onClose,
  onConfirm,
  title,
  titleAr,
  message,
  messageAr,
  confirmText = 'Confirm',
  confirmTextAr = 'تأكيد',
  cancelText = 'Cancel',
  cancelTextAr = 'إلغاء',
  variant = 'danger',
  loading = false
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  const displayTitle = isRTL ? (titleAr || title) : title;
  const displayMessage = isRTL ? (messageAr || message) : message;
  const displayConfirm = isRTL ? confirmTextAr : confirmText;
  const displayCancel = isRTL ? cancelTextAr : cancelText;

  const variants = {
    danger: {
      icon: AlertTriangle,
      iconColor: 'text-red-500',
      iconBg: 'bg-red-100 dark:bg-red-900/30',
      buttonClass: 'bg-red-500 hover:bg-red-600 text-white'
    },
    warning: {
      icon: AlertCircle,
      iconColor: 'text-amber-500',
      iconBg: 'bg-amber-100 dark:bg-amber-900/30',
      buttonClass: 'bg-amber-500 hover:bg-amber-600 text-white'
    },
    info: {
      icon: Info,
      iconColor: 'text-blue-500',
      iconBg: 'bg-blue-100 dark:bg-blue-900/30',
      buttonClass: 'bg-blue-500 hover:bg-blue-600 text-white'
    },
    success: {
      icon: CheckCircle,
      iconColor: 'text-emerald-500',
      iconBg: 'bg-emerald-100 dark:bg-emerald-900/30',
      buttonClass: 'bg-emerald-500 hover:bg-emerald-600 text-white'
    }
  };

  const config = variants[variant];
  const Icon = config.icon;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="sm"
      showCloseButton={false}
    >
      <div className="text-center py-4">
        <div className={`w-16 h-16 mx-auto mb-4 rounded-full ${config.iconBg} flex items-center justify-center`}>
          <Icon className={`w-8 h-8 ${config.iconColor}`} />
        </div>
        
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          {displayTitle}
        </h3>
        
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          {displayMessage}
        </p>
        
        <div className="flex justify-center gap-3">
          <button
            onClick={onClose}
            disabled={loading}
            className="
              px-4 py-2 rounded-lg font-medium
              text-gray-700 dark:text-gray-200
              bg-gray-100 dark:bg-gray-700
              hover:bg-gray-200 dark:hover:bg-gray-600
              disabled:opacity-50
              transition-colors
            "
          >
            {displayCancel}
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className={`
              px-4 py-2 rounded-lg font-medium
              ${config.buttonClass}
              disabled:opacity-50
              transition-colors
              flex items-center gap-2
            `}
          >
            {loading && (
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            )}
            {displayConfirm}
          </button>
        </div>
      </div>
    </Modal>
  );
};

/**
 * Alert Dialog
 */
export const AlertDialog = ({
  isOpen = false,
  onClose,
  title,
  titleAr,
  message,
  messageAr,
  buttonText = 'OK',
  buttonTextAr = 'حسناً',
  variant = 'info'
}) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  const displayTitle = isRTL ? (titleAr || title) : title;
  const displayMessage = isRTL ? (messageAr || message) : message;
  const displayButton = isRTL ? buttonTextAr : buttonText;

  const variants = {
    success: { icon: CheckCircle, color: 'text-emerald-500', bg: 'bg-emerald-100 dark:bg-emerald-900/30' },
    error: { icon: AlertTriangle, color: 'text-red-500', bg: 'bg-red-100 dark:bg-red-900/30' },
    warning: { icon: AlertCircle, color: 'text-amber-500', bg: 'bg-amber-100 dark:bg-amber-900/30' },
    info: { icon: Info, color: 'text-blue-500', bg: 'bg-blue-100 dark:bg-blue-900/30' }
  };

  const config = variants[variant];
  const Icon = config.icon;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="sm"
      showCloseButton={false}
    >
      <div className="text-center py-4">
        <div className={`w-16 h-16 mx-auto mb-4 rounded-full ${config.bg} flex items-center justify-center`}>
          <Icon className={`w-8 h-8 ${config.color}`} />
        </div>
        
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
          {displayTitle}
        </h3>
        
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          {displayMessage}
        </p>
        
        <button
          onClick={onClose}
          className="
            px-6 py-2 rounded-lg font-medium
            bg-emerald-500 hover:bg-emerald-600 text-white
            transition-colors
          "
        >
          {displayButton}
        </button>
      </div>
    </Modal>
  );
};

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  @keyframes scaleIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
  }
  .animate-fadeIn { animation: fadeIn 0.2s ease-out; }
  .animate-scaleIn { animation: scaleIn 0.2s ease-out; }
`;
if (!document.getElementById('modal-animations')) {
  style.id = 'modal-animations';
  document.head.appendChild(style);
}

export default Modal;
