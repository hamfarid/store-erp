import React from 'react'
import { ArrowLeft, Construction, Home } from 'lucide-react'
import PropTypes from 'prop-types'
import { useNavigate } from 'react-router-dom'

const ComingSoon = ({ title = "قريباً", description = "هذه الصفحة قيد التطوير" }) => {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-muted/50 flex items-center justify-center p-4" dir="rtl">
      <div className="max-w-md w-full text-center">
        {/* Icon */}
        <div className="bg-primary-100 rounded-full w-24 h-24 mx-auto mb-6 flex items-center justify-center">
          <Construction className="w-12 h-12 text-primary-600" />
        </div>

        {/* Title */}
        <h1 className="text-3xl font-bold text-foreground mb-4">{title}</h1>
        
        {/* Description */}
        <p className="text-lg text-muted-foreground mb-8 leading-relaxed">{description}</p>

        {/* Features Coming Soon */}
        <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-8 text-right">
          <h3 className="text-lg font-semibold text-foreground mb-4">🚀 الميزات القادمة:</h3>
          <ul className="space-y-2 text-foreground">
            <li className="flex items-start">
              <span className="text-primary-600 ml-2">•</span>
              <span>واجهة مستخدم متقدمة وسهلة الاستخدام</span>
            </li>
            <li className="flex items-start">
              <span className="text-primary-600 ml-2">•</span>
              <span>تقارير وتحليلات شاملة</span>
            </li>
            <li className="flex items-start">
              <span className="text-primary-600 ml-2">•</span>
              <span>تكامل مع الأنظمة الأخرى</span>
            </li>
            <li className="flex items-start">
              <span className="text-primary-600 ml-2">•</span>
              <span>إشعارات فورية ومتابعة مستمرة</span>
            </li>
          </ul>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate(-1)}
            className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg transition-colors flex items-center justify-center"
          >
            <ArrowLeft className="w-5 h-5 ml-2" />
            العودة للخلف
          </button>
          
          <button
            onClick={() => navigate('/')}
            className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg transition-colors flex items-center justify-center"
          >
            <Home className="w-5 h-5 ml-2" />
            العودة للرئيسية
          </button>
        </div>

        {/* Additional Info */}
        <div className="mt-8 text-sm text-gray-500">
          <p>نعمل بجد لتوفير أفضل تجربة لك</p>
          <p className="mt-2">شكراً لصبرك وتفهمك</p>
        </div>
      </div>
    </div>
  )
}

ComingSoon.propTypes = {
  title: PropTypes.string,
  description: PropTypes.string
}

export default ComingSoon

