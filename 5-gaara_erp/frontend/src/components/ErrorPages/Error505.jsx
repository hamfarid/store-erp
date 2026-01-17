import React from 'react'
import { AlertTriangle } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error505 = () => {
  const suggestions = [
    "تحديث المتصفح إلى أحدث إصدار",
    "تحقق من إعدادات المتصفح",
    "جرب استخدام متصفح آخر",
    "امسح ذاكرة التخزين المؤقت وملفات تعريف الارتباط",
    "تأكد من أن النظام يدعم إصدار HTTP المطلوب",
    "اتصل بفريق الدعم الفني للمساعدة"
  ]

  return (
    <ErrorPageBase
      errorCode="505"
      title="إصدار HTTP غير مدعوم"
      description="الخادم لا يدعم إصدار بروتوكول HTTP المستخدم في الطلب. قد تحتاج إلى تحديث المتصفح أو استخدام إصدار مختلف."
      suggestions={suggestions}
      icon={AlertTriangle}
      bgColor="bg-muted/50"
      iconColor="text-muted-foreground"
      buttonColor="bg-gray-600 hover:bg-gray-700"
    />
  )
}

export default Error505
