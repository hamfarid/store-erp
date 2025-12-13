import React from 'react'
import { Construction } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error501 = () => {
  return (
    <ErrorPageBase
      errorCode="501"
      title="غير مُنفَّذ"
      description="الخادم لا يدعم الوظيفة المطلوبة لتنفيذ الطلب. هذه الميزة قيد التطوير."
      icon={Construction}
      bgColor="bg-amber-100"
      iconColor="text-amber-600"
      buttonColor="bg-amber-600 hover:bg-amber-700"
      suggestions={[
        "هذه الميزة قد تكون قيد التطوير",
        "حاول استخدام ميزة بديلة",
        "تحقق من التحديثات القادمة",
        "اتصل بفريق الدعم للاستفسار عن موعد توفر هذه الميزة"
      ]}
    />
  )
}

export default Error501

