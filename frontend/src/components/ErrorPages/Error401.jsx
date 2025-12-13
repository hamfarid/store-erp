import React from 'react'
import { Lock } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error401 = () => {
  return (
    <ErrorPageBase
      errorCode="401"
      title="غير مصرح"
      description="يجب تسجيل الدخول للوصول إلى هذه الصفحة. يرجى تسجيل الدخول والمحاولة مرة أخرى."
      icon={Lock}
      bgColor="bg-yellow-100"
      iconColor="text-yellow-600"
      buttonColor="bg-yellow-600 hover:bg-yellow-700"
      suggestions={[
        "تأكد من تسجيل الدخول إلى حسابك",
        "قد تكون جلستك انتهت - حاول تسجيل الدخول مرة أخرى",
        "تحقق من صحة بيانات الاعتماد الخاصة بك",
        "إذا نسيت كلمة المرور، استخدم خيار استعادة كلمة المرور"
      ]}
    />
  )
}

export default Error401

