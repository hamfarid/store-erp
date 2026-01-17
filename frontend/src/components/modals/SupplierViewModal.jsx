import React, { useEffect, useRef } from 'react';
import { X, Building, Mail, Phone, MapPin, Package, DollarSign, Calendar, Star } from 'lucide-react';

/**
 * SupplierViewModal - عرض تفاصيل المورد بشكل احترافي
 * Professional supplier details view modal
 * 
 * @component
 * @param {Object} props
 * @param {boolean} props.isOpen - Modal visibility state
 * @param {Function} props.onClose - Close handler
 * @param {Object} props.supplier - Supplier data object
 */
const SupplierViewModal = ({ isOpen, onClose, supplier }) => {
  const modalRef = useRef(null);
  const closeButtonRef = useRef(null);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) onClose();
    };
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      setTimeout(() => closeButtonRef.current?.focus(), 100);
    }
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

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
      } else if (document.activeElement === lastElement) {
        e.preventDefault();
        firstElement?.focus();
      }
    };
    modalRef.current.addEventListener('keydown', handleTab);
    return () => modalRef.current?.removeEventListener('keydown', handleTab);
  }, [isOpen]);

  if (!isOpen || !supplier) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={onClose} role="dialog" aria-modal="true" aria-labelledby="supplier-modal-title">
      <div 
        ref={modalRef}
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-purple-700 text-white px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <Building className="w-6 h-6" />
            <h2 id="supplier-modal-title" className="text-xl font-bold">تفاصيل المورد</h2>
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
                icon={<Building className="w-5 h-5 text-purple-600" />}
                label="اسم المورد"
                value={supplier.name || '-'}
              />
              <InfoItem
                icon={<Building className="w-5 h-5 text-purple-600" />}
                label="الاسم بالإنجليزية"
                value={supplier.nameEn || supplier.name_en || '-'}
              />
              <InfoItem
                icon={<Mail className="w-5 h-5 text-purple-600" />}
                label="البريد الإلكتروني"
                value={supplier.email || '-'}
              />
              <InfoItem
                icon={<Phone className="w-5 h-5 text-purple-600" />}
                label="الهاتف"
                value={supplier.phone || '-'}
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
                icon={<MapPin className="w-5 h-5 text-purple-600" />}
                label="العنوان"
                value={supplier.address || '-'}
                fullWidth
              />
              <InfoItem
                icon={<MapPin className="w-5 h-5 text-purple-600" />}
                label="المدينة"
                value={supplier.city || '-'}
              />
              <InfoItem
                icon={<MapPin className="w-5 h-5 text-purple-600" />}
                label="المنطقة"
                value={supplier.region || '-'}
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
                icon={<Package className="w-5 h-5 text-purple-600" />}
                label="نوع المورد"
                value={supplier.type || supplier.supplier_type || '-'}
              />
              <InfoItem
                icon={<Building className="w-5 h-5 text-purple-600" />}
                label="الشركة"
                value={supplier.company || '-'}
              />
              <InfoItem
                icon={<DollarSign className="w-5 h-5 text-purple-600" />}
                label="إجمالي الطلبات"
                value={supplier.totalOrders || supplier.total_orders || '0'}
              />
              <InfoItem
                icon={<DollarSign className="w-5 h-5 text-purple-600" />}
                label="إجمالي المبلغ"
                value={supplier.totalAmount ? `${parseFloat(supplier.totalAmount).toLocaleString('ar-EG')} جنيه` : '0 جنيه'}
              />
            </div>
          </div>

          {/* Rating & Performance */}
          {supplier.rating && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                التقييم والأداء
              </h3>
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <Star className="w-5 h-5 text-yellow-500 fill-current" />
                <span className="text-lg font-medium text-gray-900">
                  {supplier.rating} / 5.0
                </span>
                <span className="text-sm text-gray-500">
                  ({supplier.reviewCount || 0} تقييم)
                </span>
              </div>
            </div>
          )}

          {/* Status Badge */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              الحالة
            </h3>
            <div className="flex items-center space-x-2 rtl:space-x-reverse">
              <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                supplier.status === 'نشط' || supplier.is_active
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {supplier.status || (supplier.is_active ? 'نشط' : 'غير نشط')}
              </span>
            </div>
          </div>

          {/* Additional Notes */}
          {supplier.notes && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                ملاحظات
              </h3>
              <p className="text-gray-700 bg-gray-50 p-4 rounded-lg">
                {supplier.notes}
              </p>
            </div>
          )}

          {/* Timestamps */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-500">
            {supplier.created_at && (
              <div>
                <span className="font-medium">تاريخ الإنشاء:</span>{' '}
                {new Date(supplier.created_at).toLocaleString('ar-EG')}
              </div>
            )}
            {supplier.updated_at && (
              <div>
                <span className="font-medium">آخر تحديث:</span>{' '}
                {new Date(supplier.updated_at).toLocaleString('ar-EG')}
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

export default SupplierViewModal;
