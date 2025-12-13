/**
 * Modern Modal Component
 * 
 * A beautiful, accessible modal/dialog component with modern UI/UX.
 */

import React, { useEffect, useRef } from 'react';
import { X, AlertTriangle, CheckCircle, Info, AlertCircle } from 'lucide-react';

// ============================================================================
// Modal Backdrop
// ============================================================================

const ModalBackdrop = ({ onClick, isOpen }) => (
  <div
    className={`
      fixed inset-0 bg-black/50 backdrop-blur-sm z-50
      transition-opacity duration-300
      ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}
    `}
    onClick={onClick}
  />
);

// ============================================================================
// Modal Container
// ============================================================================

const ModalContainer = ({ children, isOpen, size = 'md' }) => {
  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-full mx-4',
  };

  return (
    <div
      className={`
        fixed inset-0 z-50 flex items-center justify-center p-4
        transition-all duration-300
        ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}
      `}
    >
      <div
        className={`
          bg-white rounded-2xl shadow-2xl w-full ${sizeClasses[size]}
          transform transition-all duration-300
          ${isOpen ? 'scale-100 translate-y-0' : 'scale-95 -translate-y-4'}
        `}
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>
  );
};

// ============================================================================
// Modal Header
// ============================================================================

const ModalHeader = ({ title, subtitle, onClose, icon: Icon, iconColor = 'teal' }) => {
  const iconColorClasses = {
    teal: 'bg-teal-100 text-teal-600',
    amber: 'bg-amber-100 text-amber-600',
    rose: 'bg-rose-100 text-rose-600',
    blue: 'bg-blue-100 text-blue-600',
    emerald: 'bg-emerald-100 text-emerald-600',
    purple: 'bg-purple-100 text-purple-600',
  };

  return (
    <div className="flex items-start justify-between p-6 border-b border-gray-100">
      <div className="flex items-center gap-4">
        {Icon && (
          <div className={`w-12 h-12 rounded-xl ${iconColorClasses[iconColor]} flex items-center justify-center`}>
            <Icon size={24} />
          </div>
        )}
        <div>
          <h2 className="text-xl font-bold text-gray-900">{title}</h2>
          {subtitle && <p className="text-sm text-gray-500 mt-0.5">{subtitle}</p>}
        </div>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-100 rounded-xl transition-colors"
        >
          <X size={20} className="text-gray-400" />
        </button>
      )}
    </div>
  );
};

// ============================================================================
// Modal Body
// ============================================================================

const ModalBody = ({ children, className = '' }) => (
  <div className={`p-6 ${className}`}>
    {children}
  </div>
);

// ============================================================================
// Modal Footer
// ============================================================================

const ModalFooter = ({ children, className = '' }) => (
  <div className={`flex items-center justify-end gap-3 p-6 border-t border-gray-100 bg-gray-50 rounded-b-2xl ${className}`}>
    {children}
  </div>
);

// ============================================================================
// Main Modal Component
// ============================================================================

const ModernModal = ({
  isOpen,
  onClose,
  title,
  subtitle,
  icon,
  iconColor,
  size = 'md',
  children,
  footer,
  closeOnBackdrop = true,
  closeOnEscape = true,
}) => {
  const modalRef = useRef(null);

  // Handle escape key
  useEffect(() => {
    if (!closeOnEscape) return;

    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose?.();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose, closeOnEscape]);

  // Lock body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  // Focus trap
  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalRef.current.focus();
    }
  }, [isOpen]);

  const handleBackdropClick = () => {
    if (closeOnBackdrop) {
      onClose?.();
    }
  };

  return (
    <>
      <ModalBackdrop onClick={handleBackdropClick} isOpen={isOpen} />
      <ModalContainer isOpen={isOpen} size={size}>
        <div ref={modalRef} tabIndex={-1} className="outline-none">
          {title && (
            <ModalHeader
              title={title}
              subtitle={subtitle}
              onClose={onClose}
              icon={icon}
              iconColor={iconColor}
            />
          )}
          <ModalBody>{children}</ModalBody>
          {footer && <ModalFooter>{footer}</ModalFooter>}
        </div>
      </ModalContainer>
    </>
  );
};

// ============================================================================
// Confirm Modal
// ============================================================================

export const ConfirmModal = ({
  isOpen,
  onClose,
  onConfirm,
  title = 'تأكيد',
  message,
  confirmText = 'تأكيد',
  cancelText = 'إلغاء',
  type = 'warning', // 'warning' | 'danger' | 'info' | 'success'
  isLoading = false,
}) => {
  const typeConfig = {
    warning: { icon: AlertTriangle, color: 'amber', buttonClass: 'from-amber-500 to-amber-600' },
    danger: { icon: AlertCircle, color: 'rose', buttonClass: 'from-rose-500 to-rose-600' },
    info: { icon: Info, color: 'blue', buttonClass: 'from-blue-500 to-blue-600' },
    success: { icon: CheckCircle, color: 'emerald', buttonClass: 'from-emerald-500 to-emerald-600' },
  };

  const config = typeConfig[type];

  return (
    <ModernModal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      icon={config.icon}
      iconColor={config.color}
      size="sm"
      footer={
        <>
          <button
            onClick={onClose}
            className="px-6 py-2.5 border-2 border-gray-200 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition-colors"
            disabled={isLoading}
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className={`px-6 py-2.5 bg-gradient-to-l ${config.buttonClass} text-white font-medium rounded-xl shadow-lg hover:shadow-xl transition-all flex items-center gap-2`}
            disabled={isLoading}
          >
            {isLoading && (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            )}
            {confirmText}
          </button>
        </>
      }
    >
      <p className="text-gray-600">{message}</p>
    </ModernModal>
  );
};

// ============================================================================
// Alert Modal
// ============================================================================

export const AlertModal = ({
  isOpen,
  onClose,
  title,
  message,
  buttonText = 'حسناً',
  type = 'info', // 'warning' | 'danger' | 'info' | 'success'
}) => {
  const typeConfig = {
    warning: { icon: AlertTriangle, color: 'amber' },
    danger: { icon: AlertCircle, color: 'rose' },
    info: { icon: Info, color: 'blue' },
    success: { icon: CheckCircle, color: 'emerald' },
  };

  const config = typeConfig[type];

  return (
    <ModernModal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      icon={config.icon}
      iconColor={config.color}
      size="sm"
      footer={
        <button
          onClick={onClose}
          className="px-6 py-2.5 bg-gradient-to-l from-teal-500 to-teal-600 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transition-all"
        >
          {buttonText}
        </button>
      }
    >
      <p className="text-gray-600">{message}</p>
    </ModernModal>
  );
};

// Export components
ModernModal.Header = ModalHeader;
ModernModal.Body = ModalBody;
ModernModal.Footer = ModalFooter;

export default ModernModal;

