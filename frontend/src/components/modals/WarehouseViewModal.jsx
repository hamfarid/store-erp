import React, { useEffect, useRef } from 'react';
import { X, Warehouse, MapPin, User, Phone, Package, TrendingUp, AlertCircle } from 'lucide-react';

/**
 * WarehouseViewModal - عرض تفاصيل المخزن
 * Warehouse details view modal
 * 
 * @component
 * @param {Object} props
 * @param {boolean} props.isOpen - Modal visibility
 * @param {Function} props.onClose - Close handler
 * @param {Object} props.warehouse - Warehouse data
 */
const WarehouseViewModal = ({ isOpen, onClose, warehouse }) => {
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

  if (!isOpen || !warehouse) return null;

  // Calculate capacity percentage
  const capacityPercentage = warehouse.capacity && warehouse.currentStock
    ? Math.round((warehouse.currentStock / warehouse.capacity) * 100)
    : 0;

  // Determine capacity color
  const getCapacityColor = (percentage) => {
    if (percentage >= 90) return 'text-red-600 bg-red-100';
    if (percentage >= 75) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={onClose} role="dialog" aria-modal="true" aria-labelledby="warehouse-modal-title">
      <div 
        ref={modalRef}
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <Warehouse className="w-6 h-6" />
            <h2 id="warehouse-modal-title" className="text-xl font-bold">تفاصيل المخزن</h2>
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
                icon={<Warehouse className="w-5 h-5 text-indigo-600" />}
                label="اسم المخزن"
                value={warehouse.name || '-'}
              />
              <InfoItem
                icon={<Warehouse className="w-5 h-5 text-indigo-600" />}
                label="الاسم بالإنجليزية"
                value={warehouse.nameEn || warehouse.name_en || '-'}
              />
            </div>
          </div>

          {/* Location Information */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              معلومات الموقع
            </h3>
            <div className="space-y-4">
              <InfoItem
                icon={<MapPin className="w-5 h-5 text-indigo-600" />}
                label="الموقع"
                value={warehouse.location || '-'}
              />
              <InfoItem
                icon={<MapPin className="w-5 h-5 text-indigo-600" />}
                label="العنوان الكامل"
                value={warehouse.address || '-'}
              />
              <InfoItem
                icon={<MapPin className="w-5 h-5 text-indigo-600" />}
                label="المنطقة"
                value={warehouse.region || '-'}
              />
            </div>
          </div>

          {/* Management Information */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              معلومات الإدارة
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InfoItem
                icon={<User className="w-5 h-5 text-indigo-600" />}
                label="مدير المخزن"
                value={warehouse.manager || warehouse.manager_name || '-'}
              />
              <InfoItem
                icon={<Phone className="w-5 h-5 text-indigo-600" />}
                label="الهاتف"
                value={warehouse.phone || '-'}
              />
            </div>
          </div>

          {/* Capacity & Stock */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              السعة والمخزون
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <Package className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                <p className="text-sm text-gray-600 mb-1">السعة الكلية</p>
                <p className="text-2xl font-bold text-gray-900">
                  {warehouse.capacity || '0'}
                </p>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <TrendingUp className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <p className="text-sm text-gray-600 mb-1">المخزون الحالي</p>
                <p className="text-2xl font-bold text-gray-900">
                  {warehouse.currentStock || warehouse.current_stock || '0'}
                </p>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <Package className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                <p className="text-sm text-gray-600 mb-1">عدد المنتجات</p>
                <p className="text-2xl font-bold text-gray-900">
                  {warehouse.productsCount || warehouse.products_count || '0'}
                </p>
              </div>
            </div>

            {/* Capacity Bar */}
            {warehouse.capacity && (
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">نسبة الامتلاء</span>
                  <span className={`text-sm font-bold px-2 py-1 rounded ${getCapacityColor(capacityPercentage)}`}>
                    {capacityPercentage}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                  <div
                    className={`h-full transition-all duration-300 ${
                      capacityPercentage >= 90
                        ? 'bg-red-500'
                        : capacityPercentage >= 75
                        ? 'bg-yellow-500'
                        : 'bg-green-500'
                    }`}
                    style={{ width: `${Math.min(capacityPercentage, 100)}%` }}
                  />
                </div>
                {capacityPercentage >= 90 && (
                  <div className="flex items-center space-x-2 rtl:space-x-reverse mt-2 text-red-600 text-sm">
                    <AlertCircle className="w-4 h-4" />
                    <span>تحذير: المخزن شبه ممتلئ</span>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Status */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              الحالة
            </h3>
            <span className={`px-4 py-2 rounded-full text-sm font-medium inline-block ${
              warehouse.status === 'نشط' || warehouse.is_active
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}>
              {warehouse.status || (warehouse.is_active ? 'نشط' : 'غير نشط')}
            </span>
          </div>

          {/* Timestamps */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-500">
            {warehouse.created_at && (
              <div>
                <span className="font-medium">تاريخ الإنشاء:</span>{' '}
                {new Date(warehouse.created_at).toLocaleString('ar-EG')}
              </div>
            )}
            {warehouse.updated_at && (
              <div>
                <span className="font-medium">آخر تحديث:</span>{' '}
                {new Date(warehouse.updated_at).toLocaleString('ar-EG')}
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 flex justify-end border-t">
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
 * InfoItem - Single information item
 */
const InfoItem = ({ icon, label, value }) => (
  <div className="flex items-start space-x-3 rtl:space-x-reverse">
    <div className="flex-shrink-0 mt-0.5">
      {icon}
    </div>
    <div className="flex-grow">
      <p className="text-sm font-medium text-gray-600 mb-1">{label}</p>
      <p className="text-base text-gray-900">{value}</p>
    </div>
  </div>
);

export default WarehouseViewModal;
