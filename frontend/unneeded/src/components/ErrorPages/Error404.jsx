import React from 'react'
import { FileX } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error404 = () => {
  const suggestions = [
    "تحقق من صحة الرابط المكتوب في شريط العنوان",
    "استخدم القائمة الجانبية للتنقل إلى الصفحة المطلوبة",
    "ابحث عن الصفحة باستخدام مربع البحث",
    "تأكد من أن لديك الصلاحيات اللازمة للوصول إلى هذه الصفحة",
    "جرب العودة إلى الصفحة الرئيسية والتنقل من هناك"
  ]

  return (
    <ErrorPageBase
      errorCode="404"
      title="الصفحة غير موجودة"
      description="عذراً، لا يمكننا العثور على الصفحة التي تبحث عنها. قد تكون الصفحة قد تم نقلها أو حذفها أو أن الرابط غير صحيح."
      suggestions={suggestions}
      icon={FileX}
      bgColor="bg-accent/10"
      iconColor="text-accent"
      buttonColor="bg-orange-600 hover:bg-orange-700"
      showRefresh={false}
    />
  )
}

export default Error404
