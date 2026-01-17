import React from 'react'
import { Clock } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error504 = () => {
  const suggestions = [
    "انتظر بضع دقائق ثم أعد المحاولة",
    "تحقق من سرعة اتصالك بالإنترنت",
    "أعد تحميل الصفحة",
    "جرب تقليل حجم البيانات المطلوبة",
    "تأكد من أن الخادم لا يواجه حمولة عالية",
    "اتصل بمدير النظام إذا كانت المشكلة متكررة"
  ]

  return (
    <ErrorPageBase
      errorCode="504"
      title="انتهت مهلة البوابة"
      description="انتهت مهلة الاستجابة من الخادم. قد يكون الخادم بطيئاً أو مشغولاً حالياً. يرجى المحاولة مرة أخرى."
      suggestions={suggestions}
      icon={Clock}
      bgColor="bg-secondary/10"
      iconColor="text-indigo-600"
      buttonColor="bg-secondary hover:bg-secondary/90"
    />
  )
}

export default Error504
