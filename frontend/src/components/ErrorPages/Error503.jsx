import React from 'react'
import { Shield } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error503 = () => {
  const suggestions = [
    "الخدمة قيد الصيانة المجدولة - انتظر حتى انتهاء الصيانة",
    "تحقق من إعلانات الصيانة على الموقع الرسمي",
    "جرب الوصول إلى الخدمة لاحقاً",
    "تأكد من أن حسابك نشط وله الصلاحيات المناسبة",
    "اتصل بفريق الدعم للحصول على معلومات حول موعد عودة الخدمة",
    "احفظ عملك وأعد المحاولة بعد فترة"
  ]

  return (
    <ErrorPageBase
      errorCode="503"
      title="الخدمة غير متاحة"
      description="الخدمة غير متاحة حالياً. قد تكون قيد الصيانة أو مشغولة بطلبات أخرى. يرجى المحاولة مرة أخرى لاحقاً."
      suggestions={suggestions}
      icon={Shield}
      bgColor="bg-purple-50"
      iconColor="text-purple-600"
      buttonColor="bg-purple-600 hover:bg-purple-700"
    />
  )
}

export default Error503
