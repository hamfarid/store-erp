import React from 'react'
import PropTypes from 'prop-types'
import { Package, FileText, Users, ShoppingCart, AlertCircle } from 'lucide-react'

/**
 * EmptyState Component - عرض حالة فارغة جميلة وواضحة
 * 
 * @param {string} icon - نوع الأيقونة (package, file, users, cart, alert)
 * @param {string} title - العنوان الرئيسي
 * @param {string} description - الوصف التفصيلي
 * @param {string} actionText - نص زر الإجراء
 * @param {function} onAction - دالة تنفذ عند الضغط على الزر
 * @param {boolean} showAction - إظهار/إخفاء زر الإجراء
 * @param {string} secondaryActionText - نص الزر الثانوي (اختياري)
 * @param {function} onSecondaryAction - دالة الزر الثانوي (اختياري)
 */
const EmptyState = ({
  icon = 'package',
  title = 'لا توجد بيانات',
  description = 'لم يتم إضافة أي بيانات بعد',
  actionText = 'إضافة الآن',
  onAction,
  showAction = true,
  secondaryActionText,
  onSecondaryAction,
  className = ''
}) => {
  // اختيار الأيقونة المناسبة
  const getIcon = () => {
    const iconProps = {
      className: 'w-24 h-24 text-gray-300',
      strokeWidth: 1.5
    }

    switch (icon) {
      case 'package':
        return <Package {...iconProps} />
      case 'file':
        return <FileText {...iconProps} />
      case 'users':
        return <Users {...iconProps} />
      case 'cart':
        return <ShoppingCart {...iconProps} />
      case 'alert':
        return <AlertCircle {...iconProps} />
      default:
        return <Package {...iconProps} />
    }
  }

  return (
    <div className={`flex flex-col items-center justify-center py-16 px-4 ${className}`}>
      {/* الأيقونة */}
      <div className="mb-6 opacity-50">
        {getIcon()}
      </div>

      {/* العنوان */}
      <h3 className="text-2xl font-bold text-foreground mb-3 text-center">
        {title}
      </h3>

      {/* الوصف */}
      <p className="text-muted-foreground text-center max-w-md mb-8 leading-relaxed">
        {description}
      </p>

      {/* الأزرار */}
      {showAction && (
        <div className="flex flex-col sm:flex-row gap-3">
          {/* الزر الرئيسي */}
          {onAction && (
            <button
              onClick={onAction}
              className="bg-primary-600 text-white px-8 py-3 rounded-lg hover:bg-primary-700 transition-all duration-200 font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
            >
              <Package className="w-5 h-5" />
              {actionText}
            </button>
          )}

          {/* الزر الثانوي */}
          {onSecondaryAction && secondaryActionText && (
            <button
              onClick={onSecondaryAction}
              className="bg-white text-gray-700 border-2 border-gray-300 px-8 py-3 rounded-lg hover:bg-gray-50 transition-all duration-200 font-medium"
            >
              {secondaryActionText}
            </button>
          )}
        </div>
      )}

      {/* خط فاصل زخرفي */}
      <div className="mt-12 flex items-center gap-4 opacity-30">
        <div className="h-px w-16 bg-gray-300"></div>
        <div className="w-2 h-2 rounded-full bg-gray-300"></div>
        <div className="h-px w-16 bg-gray-300"></div>
      </div>
    </div>
  )
}

EmptyState.propTypes = {
  icon: PropTypes.oneOf(['package', 'file', 'users', 'cart', 'alert']),
  title: PropTypes.string,
  description: PropTypes.string,
  actionText: PropTypes.string,
  onAction: PropTypes.func,
  showAction: PropTypes.bool,
  secondaryActionText: PropTypes.string,
  onSecondaryAction: PropTypes.func,
  className: PropTypes.string
}

export default EmptyState

