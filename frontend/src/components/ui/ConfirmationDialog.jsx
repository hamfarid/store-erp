/**
 * Enhanced Confirmation Dialog Component
 * 
 * Provides a reusable confirmation dialog for destructive actions
 * with better UX and Arabic support
 * 
 * Date: 2025-01-25
 * Phase: 2 - Component Improvements
 */

import React, { useState } from 'react';
import { AlertTriangle, Trash2, X, CheckCircle, Info } from 'lucide-react';

/**
 * Confirmation Dialog Component
 * 
 * @param {boolean} isOpen - Whether the dialog is open
 * @param {function} onClose - Function to close the dialog
 * @param {function} onConfirm - Function to call when confirmed
 * @param {string} title - Dialog title
 * @param {string} message - Dialog message
 * @param {string} confirmText - Confirm button text
 * @param {string} cancelText - Cancel button text
 * @param {string} variant - Dialog variant (danger, warning, info, success)
 * @param {boolean} requireConfirmation - Require typing confirmation text
 * @param {string} confirmationText - Text to type for confirmation
 */
export const ConfirmationDialog = ({
  isOpen,
  onClose,
  onConfirm,
  title = 'تأكيد العملية',
  message = 'هل أنت متأكد من أنك تريد المتابعة؟',
  confirmText = 'تأكيد',
  cancelText = 'إلغاء',
  variant = 'danger', // danger, warning, info, success
  requireConfirmation = false,
  confirmationText = 'حذف',
  isLoading = false
}) => {
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleConfirm = () => {
    if (requireConfirmation && inputValue !== confirmationText) {
      setError(`يرجى كتابة "${confirmationText}" للتأكيد`);
      return;
    }
    onConfirm();
    setInputValue('');
    setError('');
  };

  const handleClose = () => {
    setInputValue('');
    setError('');
    onClose();
  };

  // Variant configurations
  const variants = {
    danger: {
      icon: Trash2,
      iconBg: 'bg-red-100 dark:bg-red-900/20',
      iconColor: 'text-red-600 dark:text-red-400',
      confirmBg: 'bg-red-600 hover:bg-red-700',
      confirmText: 'text-white'
    },
    warning: {
      icon: AlertTriangle,
      iconBg: 'bg-yellow-100 dark:bg-yellow-900/20',
      iconColor: 'text-yellow-600 dark:text-yellow-400',
      confirmBg: 'bg-yellow-600 hover:bg-yellow-700',
      confirmText: 'text-white'
    },
    info: {
      icon: Info,
      iconBg: 'bg-blue-100 dark:bg-blue-900/20',
      iconColor: 'text-blue-600 dark:text-blue-400',
      confirmBg: 'bg-blue-600 hover:bg-blue-700',
      confirmText: 'text-white'
    },
    success: {
      icon: CheckCircle,
      iconBg: 'bg-green-100 dark:bg-green-900/20',
      iconColor: 'text-green-600 dark:text-green-400',
      confirmBg: 'bg-green-600 hover:bg-green-700',
      confirmText: 'text-white'
    }
  };

  const config = variants[variant] || variants.danger;
  const Icon = config.icon;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6 animate-in fade-in zoom-in duration-200">
        {/* Icon */}
        <div className="flex justify-center mb-4">
          <div className={`${config.iconBg} rounded-full p-3`}>
            <Icon className={`w-8 h-8 ${config.iconColor}`} />
          </div>
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold text-gray-900 dark:text-white text-center mb-2">
          {title}
        </h3>

        {/* Message */}
        <p className="text-gray-600 dark:text-gray-400 text-center mb-6">
          {message}
        </p>

        {/* Confirmation Input */}
        {requireConfirmation && (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              اكتب "{confirmationText}" للتأكيد:
            </label>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => {
                setInputValue(e.target.value);
                setError('');
              }}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder={confirmationText}
              autoFocus
            />
            {error && (
              <p className="mt-2 text-sm text-red-600 dark:text-red-400">
                {error}
              </p>
            )}
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={handleClose}
            disabled={isLoading}
            className="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {cancelText}
          </button>
          <button
            onClick={handleConfirm}
            disabled={isLoading || (requireConfirmation && inputValue !== confirmationText)}
            className={`flex-1 px-4 py-2 ${config.confirmBg} ${config.confirmText} rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {isLoading ? 'جاري المعالجة...' : confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationDialog;

