import React from 'react'
import { Server } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error500 = () => {
  const suggestions = [
    "انتظر بضع دقائق ثم أعد المحاولة",
    "تحديث الصفحة قد يحل المشكلة",
    "تحقق من اتصالك بالإنترنت",
    "امسح ذاكرة التخزين المؤقت للمتصفح",
    "جرب استخدام متصفح آخر",
    "اتصل بفريق الدعم الفني إذا استمرت المشكلة"
  ]

  return (
    <ErrorPageBase
      errorCode="500"
      title="خطأ في الخادم الداخلي"
      description="حدث خطأ غير متوقع في الخادم. نحن نعمل على إصلاح هذه المشكلة. يرجى المحاولة مرة أخرى لاحقاً."
      suggestions={suggestions}
      icon={Server}
      bgColor="bg-destructive/10"
      iconColor="text-destructive"
      buttonColor="bg-destructive hover:bg-red-700"
    />
  )
}

export default Error500
