import React, { useEffect, useRef } from 'react';
import { X, User, Mail, Phone, MapPin, Building, Calendar, DollarSign } from 'lucide-react';

/**
 * CustomerViewModal - عرض تفاصيل العميل بشكل احترافي
 * Professional customer details view modal
 * 
 * @component
 * @param {Object} props
 * @param {boolean} props.isOpen - Modal visibility state
 * @param {Function} props.onClose - Close handler
 * @param {Object} props.customer - Customer data object
 */
const CustomerViewModal = ({ isOpen, onClose, customer }) => {
  const modalRef = useRef(null);
  const closeButtonRef = useRef(null);

  // ESC key handler & Focus management
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      setTimeout(() => closeButtonRef.current?.focus(), 100);
    }

    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  // Focus trap
  useEffect(() => {
    if (!isOpen || !modalRef.current) return;

    const focusableElements = modalRef.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    const handleTab = (e) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    modalRef.current.addEventListener('keydown', handleTab);
    return () => modalRef.current?.removeEventListener('keydown', handleTab);
  }, [isOpen]);

  if (!isOpen || !customer) return null;

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" 
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="customer-modal-title"
    >
      <div 
        ref={modalRef}
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <User className="w-6 h-6" />
            <h2 id="customer-modal-title" className="text-xl font-bold">تفاصيل العميل</h2>
          </div>
          <button
            ref={closeButtonRef}
            onClick={onClose}
            className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2 transition-colors"
            aria-label="إغلاق النافذة"
            title="إغلاق (ESC)"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-80px)]">
          {/* Basic Information */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              المعلومات الأساسية
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InfoItem
                icon={<User className="w-5 h-5 text-blue-600" />}
                label="الاسم"
                value={customer.name || '-'}
              />
              <InfoItem
                icon={<Building className="w-5 h-5 text-blue-600" />}
                label="الاسم بالإنجليزية"
                value={customer.nameEn || customer.name_en || '-'}
              />
              <InfoItem
                icon={<Mail className="w-5 h-5 text-blue-600" />}
                label="البريد الإلكتروني"
                value={customer.email || '-'}
              />
              <InfoItem
                icon={<Phone className="w-5 h-5 text-blue-600" />}
                label="الهاتف"
                value={customer.phone || '-'}
              />
            </div>
          </div>

          {/* Address Information */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              معلومات العنوان
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InfoItem
                icon={<MapPin className="w-5 h-5 text-blue-600" />}
                label="العنوان"
                value={customer.address || '-'}
                fullWidth
              />
              <InfoItem
                icon={<MapPin className="w-5 h-5 text-blue-600" />}
                label="المدينة"
                value={customer.city || '-'}
              />
              <InfoItem
                icon={<MapPin className="w-5 h-5 text-blue-600" />}
                label="المنطقة"
                value={customer.region || '-'}
              />
            </div>
          </div>

          {/* Business Information */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              المعلومات التجارية
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InfoItem
                icon={<Building className="w-5 h-5 text-blue-600" />}
                label="النوع"
                value={customer.type || customer.customer_type || 'عميل عادي'}
              />
              <InfoItem
                icon={<User className="w-5 h-5 text-blue-600" />}
                label="مهندس المبيعات"
                value={customer.salesEngineer || customer.sales_engineer || '-'}
              />
              <InfoItem
                icon={<DollarSign className="w-5 h-5 text-blue-600" />}
                label="إجمالي المشتريات"
                value={customer.totalPurchases ? `${parseFloat(customer.totalPurchases).toLocaleString('ar-EG')} جنيه` : '0 جنيه'}
              />
              <InfoItem
                icon={<Calendar className="w-5 h-5 text-blue-600" />}
                label="آخر عملية شراء"
                value={customer.lastPurchase ? new Date(customer.lastPurchase).toLocaleDateString('ar-EG') : '-'}
              />
            </div>
          </div>

          {/* Status Badge */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              الحالة
            </h3>
            <div className="flex items-center space-x-2 rtl:space-x-reverse">
              <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                customer.status === 'نشط' || customer.is_active
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {customer.status || (customer.is_active ? 'نشط' : 'غير نشط')}
              </span>
            </div>
          </div>

          {/* Additional Notes */}
          {customer.notes && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                ملاحظات
              </h3>
              <p className="text-gray-700 bg-gray-50 p-4 rounded-lg">
                {customer.notes}
              </p>
            </div>
          )}

          {/* Timestamps */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-500">
            {customer.created_at && (
              <div>
                <span className="font-medium">تاريخ الإنشاء:</span>{' '}
                {new Date(customer.created_at).toLocaleString('ar-EG')}
              </div>
            )}
            {customer.updated_at && (
              <div>
                <span className="font-medium">آخر تحديث:</span>{' '}
                {new Date(customer.updated_at).toLocaleString('ar-EG')}
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 flex justify-end space-x-3 rtl:space-x-reverse border-t">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            إغلاق
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * InfoItem - عنصر معلومة واحدة
 * Single information item component
 */
const InfoItem = ({ icon, label, value, fullWidth = false }) => (
  <div className={`flex items-start space-x-3 rtl:space-x-reverse ${fullWidth ? 'md:col-span-2' : ''}`}>
    <div className="flex-shrink-0 mt-0.5">
      {icon}
    </div>
    <div className="flex-grow">
      <p className="text-sm font-medium text-gray-600 mb-1">{label}</p>
      <p className="text-base text-gray-900">{value}</p>
    </div>
  </div>
);

export default CustomerViewModal;
