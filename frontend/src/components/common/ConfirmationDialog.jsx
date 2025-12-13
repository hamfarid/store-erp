import React, { createContext, useContext, useState, useCallback } from 'react'
import { createPortal } from 'react-dom'
import './ConfirmationDialog.css'

// Confirmation Context
const ConfirmationContext = createContext()

// Confirmation Provider
export const ConfirmationProvider = ({ children }) => {
  const [dialogs, setDialogs] = useState([])

  const showConfirmation = useCallback((options) => {
    return new Promise((resolve) => {
      const id = Date.now() + Math.random()
      const dialog = {
        id,
        resolve,
        type: 'confirm',
        title: 'تأكيد العملية',
        message: 'هل أنت متأكد من هذا الإجراء؟',
        confirmText: 'تأكيد',
        cancelText: 'إلغاء',
        variant: 'primary',
        icon: 'fas fa-question-circle',
        ...options
      }

      setDialogs(prev => [...prev, dialog])
    })
  }, [])

  const hideDialog = useCallback((id, result = false) => {
    setDialogs(prev => {
      const dialog = prev.find(d => d.id === id)
      if (dialog) {
        dialog.resolve(result)
      }
      return prev.filter(d => d.id !== id)
    })
  }, [])

  // Convenience methods
  const confirmDelete = useCallback((itemName = 'العنصر') => {
    return showConfirmation({
      type: 'delete',
      title: 'تأكيد الحذف',
      message: `هل أنت متأكد من حذف ${itemName}؟`,
      description: 'لا يمكن التراجع عن هذا الإجراء.',
      confirmText: 'حذف',
      cancelText: 'إلغاء',
      variant: 'danger',
      icon: 'fas fa-trash-alt'
    })
  }, [showConfirmation])

  const confirmSave = useCallback((message = 'هل تريد حفظ التغييرات؟') => {
    return showConfirmation({
      type: 'save',
      title: 'حفظ التغييرات',
      message,
      confirmText: 'حفظ',
      cancelText: 'إلغاء',
      variant: 'success',
      icon: 'fas fa-save'
    })
  }, [showConfirmation])

  const confirmDiscard = useCallback(() => {
    return showConfirmation({
      type: 'discard',
      title: 'تجاهل التغييرات',
      message: 'هل تريد تجاهل التغييرات غير المحفوظة؟',
      description: 'ستفقد جميع التغييرات التي لم يتم حفظها.',
      confirmText: 'تجاهل',
      cancelText: 'إلغاء',
      variant: 'warning',
      icon: 'fas fa-exclamation-triangle'
    })
  }, [showConfirmation])

  const confirmLogout = useCallback(() => {
    return showConfirmation({
      type: 'logout',
      title: 'تسجيل الخروج',
      message: 'هل تريد تسجيل الخروج من النظام؟',
      confirmText: 'تسجيل الخروج',
      cancelText: 'إلغاء',
      variant: 'secondary',
      icon: 'fas fa-sign-out-alt'
    })
  }, [showConfirmation])

  const alert = useCallback((message, options = {}) => {
    return showConfirmation({
      type: 'alert',
      title: 'تنبيه',
      message,
      confirmText: 'موافق',
      cancelText: null, // No cancel button for alerts
      variant: 'info',
      icon: 'fas fa-info-circle',
      ...options
    })
  }, [showConfirmation])

  const value = {
    showConfirmation,
    confirmDelete,
    confirmSave,
    confirmDiscard,
    confirmLogout,
    alert
  }

  return (
    <ConfirmationContext.Provider value={value}>
      {children}
      {dialogs.map(dialog => (
        <ConfirmationDialog
          key={dialog.id}
          dialog={dialog}
          onClose={(result) => hideDialog(dialog.id, result)}
        />
      ))}
    </ConfirmationContext.Provider>
  )
}

// Individual Confirmation Dialog Component
const ConfirmationDialog = ({ dialog, onClose }) => {
  const [isVisible, setIsVisible] = useState(false)

  React.useEffect(() => {
    // Trigger entrance animation
    const timer = setTimeout(() => setIsVisible(true), 10)
    return () => clearTimeout(timer)
  }, [])

  const handleConfirm = () => {
    setIsVisible(false)
    setTimeout(() => onClose(true), 200)
  }

  const handleCancel = () => {
    setIsVisible(false)
    setTimeout(() => onClose(false), 200)
  }

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      handleCancel()
    }
  }

  const dialogClass = `
    confirmation-dialog
    confirmation-dialog--${dialog.variant}
    ${isVisible ? 'confirmation-dialog--visible' : ''}
  `.trim()

  return createPortal(
    <div className="confirmation-backdrop" onClick={handleBackdropClick}>
      <div className={dialogClass} role="dialog" aria-modal="true">
        <div className="confirmation-dialog__header">
          {dialog.icon && (
            <div className="confirmation-dialog__icon">
              <i className={dialog.icon}></i>
            </div>
          )}
          <h3 className="confirmation-dialog__title">{dialog.title}</h3>
        </div>

        <div className="confirmation-dialog__body">
          <p className="confirmation-dialog__message">{dialog.message}</p>
          {dialog.description && (
            <p className="confirmation-dialog__description">{dialog.description}</p>
          )}
        </div>

        <div className="confirmation-dialog__footer">
          {dialog.cancelText && (
            <button
              className="confirmation-dialog__button confirmation-dialog__button--cancel"
              onClick={handleCancel}
              autoFocus={dialog.type === 'alert'}
            >
              {dialog.cancelText}
            </button>
          )}
          <button
            className={`confirmation-dialog__button confirmation-dialog__button--confirm confirmation-dialog__button--${dialog.variant}`}
            onClick={handleConfirm}
            autoFocus={dialog.type !== 'alert'}
          >
            {dialog.confirmText}
          </button>
        </div>
      </div>
    </div>,
    document.body
  )
}

// Hook to use confirmation
export const useConfirmation = () => {
  const context = useContext(ConfirmationContext)
  if (!context) {
    throw new Error('useConfirmation must be used within a ConfirmationProvider')
  }
  return context
}

// Higher-order component for confirmation
export const withConfirmation = (Component) => {
  return function ConfirmationWrappedComponent(props) {
    const confirmation = useConfirmation()
    return <Component {...props} confirmation={confirmation} />
  }
}

// Hook for confirming async operations
export const useConfirmedAction = () => {
  const { showConfirmation } = useConfirmation()

  return useCallback(async (action, confirmationOptions) => {
    const confirmed = await showConfirmation(confirmationOptions)
    if (confirmed && typeof action === 'function') {
      return await action()
    }
    return false
  }, [showConfirmation])
}

export default ConfirmationProvider
