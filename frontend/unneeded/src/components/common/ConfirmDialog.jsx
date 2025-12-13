import React from 'react';
import { AlertTriangle, X, Trash2, Check } from 'lucide-react';

const ConfirmDialog = ({
  isOpen,
  onClose,
  onConfirm,
  title = "تأكيد العملية",
  message = "هل أنت متأكد من تنفيذ هذه العملية؟",
  confirmText = "تأكيد",
  cancelText = "إلغاء",
  type = "warning", // warning, danger, info, success
  loading = false,
  icon: CustomIcon
}) => {
  if (!isOpen) return null;

  const typeConfig = {
    warning: {
      icon: AlertTriangle,
      iconColor: 'text-accent',
      iconBg: 'bg-accent/20',
      confirmButton: 'bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500'
    },
    danger: {
      icon: Trash2,
      iconColor: 'text-destructive',
      iconBg: 'bg-destructive/20',
      confirmButton: 'bg-destructive hover:bg-red-700 focus:ring-red-500'
    },
    info: {
      icon: AlertTriangle,
      iconColor: 'text-primary-600',
      iconBg: 'bg-primary-100',
      confirmButton: 'bg-primary-600 hover:bg-primary-700 focus:ring-primary-500'
    },
    success: {
      icon: Check,
      iconColor: 'text-primary',
      iconBg: 'bg-primary/20',
      confirmButton: 'bg-primary hover:bg-green-700 focus:ring-green-500'
    }
  };

  const config = typeConfig[type] || typeConfig.warning;
  const Icon = CustomIcon || config.icon;

  const handleConfirm = () => {
    if (!loading && onConfirm) {
      onConfirm();
    }
  };

  const handleClose = () => {
    if (!loading && onClose) {
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center">
            <div className={`p-2 rounded-full ${config.iconBg} ml-3`}>
              <Icon className={`w-6 h-6 ${config.iconColor}`} />
            </div>
            <h3 className="text-lg font-semibold text-foreground" dir="rtl">
              {title}
            </h3>
          </div>
          <button
            onClick={handleClose}
            disabled={loading}
            className="p-2 hover:bg-muted rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="إغلاق"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <p className="text-foreground text-center" dir="rtl">
            {message}
          </p>
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-3 rtl:space-x-reverse p-6 border-t bg-muted/50">
          <button
            onClick={handleClose}
            disabled={loading}
            className="px-4 py-2 text-foreground bg-white border border-border rounded-lg hover:bg-muted/50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {cancelText}
          </button>
          <button
            onClick={handleConfirm}
            disabled={loading}
            className={`px-4 py-2 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center min-w-[100px] justify-center ${config.confirmButton}`}
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white ml-2"></div>
                جاري التنفيذ...
              </>
            ) : (
              confirmText
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

// مكونات محددة للاستخدامات الشائعة
export const DeleteConfirmDialog = ({ isOpen, onClose, onConfirm, itemName, loading }) => (
  <ConfirmDialog
    isOpen={isOpen}
    onClose={onClose}
    onConfirm={onConfirm}
    title="تأكيد الحذف"
    message={`هل أنت متأكد من حذف ${itemName || 'هذا العنصر'}؟ لا يمكن التراجع عن هذه العملية.`}
    confirmText="حذف"
    cancelText="إلغاء"
    type="danger"
    loading={loading}
  />
);

export const SaveConfirmDialog = ({ isOpen, onClose, onConfirm, loading }) => (
  <ConfirmDialog
    isOpen={isOpen}
    onClose={onClose}
    onConfirm={onConfirm}
    title="تأكيد الحفظ"
    message="هل تريد حفظ التغييرات؟"
    confirmText="حفظ"
    cancelText="إلغاء"
    type="success"
    loading={loading}
  />
);

export const LogoutConfirmDialog = ({ isOpen, onClose, onConfirm, loading }) => (
  <ConfirmDialog
    isOpen={isOpen}
    onClose={onClose}
    onConfirm={onConfirm}
    title="تأكيد تسجيل الخروج"
    message="هل تريد تسجيل الخروج من النظام؟"
    confirmText="تسجيل الخروج"
    cancelText="إلغاء"
    type="warning"
    loading={loading}
  />
);

export const ResetConfirmDialog = ({ isOpen, onClose, onConfirm, loading }) => (
  <ConfirmDialog
    isOpen={isOpen}
    onClose={onClose}
    onConfirm={onConfirm}
    title="تأكيد إعادة التعيين"
    message="هل تريد إعادة تعيين جميع البيانات؟ ستفقد جميع التغييرات غير المحفوظة."
    confirmText="إعادة تعيين"
    cancelText="إلغاء"
    type="warning"
    loading={loading}
  />
);

export const SubmitConfirmDialog = ({ isOpen, onClose, onConfirm, loading, message }) => (
  <ConfirmDialog
    isOpen={isOpen}
    onClose={onClose}
    onConfirm={onConfirm}
    title="تأكيد الإرسال"
    message={message || "هل تريد إرسال البيانات؟"}
    confirmText="إرسال"
    cancelText="إلغاء"
    type="info"
    loading={loading}
  />
);

export default ConfirmDialog;

