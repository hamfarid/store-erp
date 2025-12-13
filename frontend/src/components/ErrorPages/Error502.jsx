import React from 'react'
import { Wifi } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error502 = () => {
  const suggestions = [
    "تحقق من اتصالك بالإنترنت",
    "انتظر بضع دقائق ثم أعد المحاولة",
    "تحديث الصفحة قد يحل المشكلة",
    "تأكد من أن الخادم يعمل بشكل صحيح",
    "جرب الوصول إلى صفحات أخرى في الموقع",
    "اتصل بمدير النظام إذا استمرت المشكلة"
  ]

  return (
    <ErrorPageBase
      errorCode="502"
      title="خطأ في البوابة"
      description="لا يمكن الوصول إلى الخادم حالياً. قد يكون الخادم مشغولاً أو قيد الصيانة. يرجى المحاولة مرة أخرى لاحقاً."
      suggestions={suggestions}
      icon={Wifi}
      bgColor="bg-accent/10"
      iconColor="text-accent"
      buttonColor="bg-yellow-600 hover:bg-yellow-700"
    />
  )
}

export default Error502
