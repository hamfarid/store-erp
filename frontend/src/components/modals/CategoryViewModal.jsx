import React, { useEffect, useRef } from 'react';
import { X, Tag, Layers, Package, Calendar } from 'lucide-react';

/**
 * CategoryViewModal - عرض تفاصيل الفئة
 * Category details view modal
 * 
 * @component
 * @param {Object} props
 * @param {boolean} props.isOpen - Modal visibility
 * @param {Function} props.onClose - Close handler
 * @param {Object} props.category - Category data
 */
const CategoryViewModal = ({ isOpen, onClose, category }) => {
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

  if (!isOpen || !category) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={onClose} role="dialog" aria-modal="true" aria-labelledby="category-modal-title">
      <div 
        ref={modalRef}
        className="bg-white rounded-lg shadow-xl w-full max-w-xl max-h-[90vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3 rtl:space-x-reverse">
            <Tag className="w-6 h-6" />
            <h2 id="category-modal-title" className="text-xl font-bold">تفاصيل الفئة</h2>
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
          {/* Basic Info */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              المعلومات الأساسية
            </h3>
            <div className="space-y-4">
              <InfoItem
                icon={<Tag className="w-5 h-5 text-green-600" />}
                label="اسم الفئة (عربي)"
                value={category.name || '-'}
              />
              <InfoItem
                icon={<Tag className="w-5 h-5 text-green-600" />}
                label="اسم الفئة (English)"
                value={category.nameEn || category.name_en || '-'}
              />
              <InfoItem
                icon={<Layers className="w-5 h-5 text-green-600" />}
                label="الفئة الأم"
                value={category.parentName || category.parent_name || 'فئة رئيسية'}
              />
              <InfoItem
                icon={<Package className="w-5 h-5 text-green-600" />}
                label="عدد المنتجات"
                value={category.productsCount || category.products_count || '0'}
              />
            </div>
          </div>

          {/* Description */}
          {category.description && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                الوصف
              </h3>
              <p className="text-gray-700 bg-gray-50 p-4 rounded-lg">
                {category.description}
              </p>
            </div>
          )}

          {/* Hierarchy */}
          {category.level !== undefined && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                التسلسل الهرمي
              </h3>
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <Layers className="w-5 h-5 text-green-600" />
                <span className="text-gray-900">
                  المستوى: <span className="font-medium">{category.level}</span>
                </span>
              </div>
            </div>
          )}

          {/* Status */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
              الحالة
            </h3>
            <span className={`px-4 py-2 rounded-full text-sm font-medium inline-block ${
              category.status === 'نشط' || category.is_active
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}>
              {category.status || (category.is_active ? 'نشط' : 'غير نشط')}
            </span>
          </div>

          {/* Timestamps */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-500">
            {category.created_at && (
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <Calendar className="w-4 h-4" />
                <div>
                  <span className="font-medium">تاريخ الإنشاء:</span>{' '}
                  {new Date(category.created_at).toLocaleDateString('ar-EG')}
                </div>
              </div>
            )}
            {category.updated_at && (
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <Calendar className="w-4 h-4" />
                <div>
                  <span className="font-medium">آخر تحديث:</span>{' '}
                  {new Date(category.updated_at).toLocaleDateString('ar-EG')}
                </div>
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
 * InfoItem - Single info row
 */
const InfoItem = ({ icon, label, value }) => (
  <div className="flex items-start space-x-3 rtl:space-x-reverse">
    <div className="flex-shrink-0 mt-0.5">
      {icon}
    </div>
    <div className="flex-grow">
      <p className="text-sm font-medium text-gray-600 mb-1">{label}</p>
      <p className="text-base text-gray-900 font-medium">{value}</p>
    </div>
  </div>
);

export default CategoryViewModal;
