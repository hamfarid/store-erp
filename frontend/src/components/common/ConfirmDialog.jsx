/**
 * ConfirmDialog Component
 * @file frontend/src/components/common/ConfirmDialog.jsx
 * 
 * مربع حوار التأكيد
 */

import React, { useState, useCallback, createContext, useContext } from 'react';
import { AlertTriangle, Trash2, Check, X, Info, AlertCircle } from 'lucide-react';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '../ui/alert-dialog';
import { Button } from '../ui/button';
import { cn } from '../../lib/utils';

/**
 * أنواع مربعات الحوار
 */
const DIALOG_TYPES = {
  confirm: {
    icon: Info,
    iconColor: 'text-blue-500',
    confirmVariant: 'default'
  },
  warning: {
    icon: AlertTriangle,
    iconColor: 'text-yellow-500',
    confirmVariant: 'default'
  },
  danger: {
    icon: AlertCircle,
    iconColor: 'text-red-500',
    confirmVariant: 'destructive'
  },
  delete: {
    icon: Trash2,
    iconColor: 'text-red-500',
    confirmVariant: 'destructive'
  },
  success: {
    icon: Check,
    iconColor: 'text-green-500',
    confirmVariant: 'default'
  }
};

/**
 * ConfirmDialog Component
 */
export function ConfirmDialog({
  open,
  onOpenChange,
  title = 'تأكيد',
  description = 'هل أنت متأكد من هذا الإجراء؟',
  type = 'confirm',
  confirmText = 'تأكيد',
  cancelText = 'إلغاء',
  onConfirm,
  onCancel,
  loading = false,
  children
}) {
  const config = DIALOG_TYPES[type] || DIALOG_TYPES.confirm;
  const Icon = config.icon;

  const handleConfirm = useCallback(async () => {
    try {
      await onConfirm?.();
      onOpenChange?.(false);
    } catch (error) {
      console.error('Confirm action failed:', error);
    }
  }, [onConfirm, onOpenChange]);

  const handleCancel = useCallback(() => {
    onCancel?.();
    onOpenChange?.(false);
  }, [onCancel, onOpenChange]);

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent dir="rtl">
        <AlertDialogHeader>
          <div className="flex items-center gap-3">
            <div className={cn('p-2 rounded-full bg-muted', config.iconColor)}>
              <Icon className="w-5 h-5" />
            </div>
            <AlertDialogTitle>{title}</AlertDialogTitle>
          </div>
          <AlertDialogDescription className="text-right">
            {description}
          </AlertDialogDescription>
        </AlertDialogHeader>
        
        {children && (
          <div className="py-4">
            {children}
          </div>
        )}
        
        <AlertDialogFooter className="flex-row-reverse gap-2">
          <AlertDialogAction
            onClick={handleConfirm}
            disabled={loading}
            className={cn(
              config.confirmVariant === 'destructive' && 'bg-red-600 hover:bg-red-700'
            )}
          >
            {loading ? 'جاري...' : confirmText}
          </AlertDialogAction>
          <AlertDialogCancel onClick={handleCancel} disabled={loading}>
            {cancelText}
          </AlertDialogCancel>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

/**
 * DeleteConfirmDialog - مربع حوار تأكيد الحذف
 */
export function DeleteConfirmDialog({
  open,
  onOpenChange,
  itemName = 'هذا العنصر',
  onConfirm,
  loading = false
}) {
  return (
    <ConfirmDialog
      open={open}
      onOpenChange={onOpenChange}
      type="delete"
      title="تأكيد الحذف"
      description={`هل أنت متأكد من حذف ${itemName}؟ لا يمكن التراجع عن هذا الإجراء.`}
      confirmText="حذف"
      onConfirm={onConfirm}
      loading={loading}
    />
  );
}

/**
 * Context للتأكيد العام
 */
const ConfirmContext = createContext(null);

export function ConfirmProvider({ children }) {
  const [state, setState] = useState({
    open: false,
    config: {}
  });

  const confirm = useCallback((config) => {
    return new Promise((resolve) => {
      setState({
        open: true,
        config: {
          ...config,
          onConfirm: () => {
            resolve(true);
            setState((prev) => ({ ...prev, open: false }));
          },
          onCancel: () => {
            resolve(false);
            setState((prev) => ({ ...prev, open: false }));
          }
        }
      });
    });
  }, []);

  return (
    <ConfirmContext.Provider value={{ confirm }}>
      {children}
      <ConfirmDialog
        open={state.open}
        onOpenChange={(open) => {
          if (!open) {
            state.config.onCancel?.();
          }
        }}
        {...state.config}
      />
    </ConfirmContext.Provider>
  );
}

/**
 * Hook للتأكيد
 */
export function useConfirm() {
  const context = useContext(ConfirmContext);
  
  if (!context) {
    throw new Error('useConfirm must be used within a ConfirmProvider');
  }
  
  return context;
}

/**
 * Hook للتأكيد السريع
 */
export function useQuickConfirm() {
  const { confirm } = useConfirm();

  const confirmDelete = useCallback((itemName) => {
    return confirm({
      type: 'delete',
      title: 'تأكيد الحذف',
      description: `هل أنت متأكد من حذف ${itemName}؟`,
      confirmText: 'حذف'
    });
  }, [confirm]);

  const confirmAction = useCallback((message) => {
    return confirm({
      type: 'confirm',
      title: 'تأكيد',
      description: message,
      confirmText: 'تأكيد'
    });
  }, [confirm]);

  const confirmWarning = useCallback((message) => {
    return confirm({
      type: 'warning',
      title: 'تحذير',
      description: message,
      confirmText: 'متابعة'
    });
  }, [confirm]);

  return {
    confirm,
    confirmDelete,
    confirmAction,
    confirmWarning
  };
}

export default ConfirmDialog;
