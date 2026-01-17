import React from 'react'
import { Shield } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error403 = () => {
  const suggestions = [
    "تواصل مع مدير النظام لطلب الصلاحيات اللازمة",
    "تأكد من أنك مسجل دخول بالحساب الصحيح",
    "راجع دليل المستخدم لمعرفة الصلاحيات المطلوبة",
    "جرب تسجيل الخروج وإعادة تسجيل الدخول",
    "تحقق من انتهاء صلاحية جلسة العمل"
  ]

  return (
    <ErrorPageBase
      errorCode="403"
      title="غير مصرح لك بالوصول"
      description="عذراً، ليس لديك الصلاحية للوصول إلى هذه الصفحة. يرجى التواصل مع مدير النظام للحصول على الصلاحيات اللازمة."
      suggestions={suggestions}
      icon={Shield}
      bgColor="bg-destructive/10"
      iconColor="text-destructive"
      buttonColor="bg-destructive hover:bg-red-700"
      showRefresh={false}
    />
  )
}

export default Error403
