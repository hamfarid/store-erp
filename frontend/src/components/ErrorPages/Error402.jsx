import React from 'react'
import { CreditCard } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error402 = () => {
  return (
    <ErrorPageBase
      errorCode="402"
      title="الدفع مطلوب"
      description="هذه الخدمة تتطلب اشتراكاً أو دفعاً للوصول إليها. يرجى ترقية حسابك للمتابعة."
      icon={CreditCard}
      bgColor="bg-purple-100"
      iconColor="text-purple-600"
      buttonColor="bg-purple-600 hover:bg-purple-700"
      suggestions={[
        "تحقق من حالة اشتراكك",
        "قم بترقية خطتك للوصول إلى هذه الميزة",
        "اتصل بفريق المبيعات للحصول على المزيد من المعلومات",
        "تحقق من طريقة الدفع المسجلة في حسابك"
      ]}
    />
  )
}

export default Error402

