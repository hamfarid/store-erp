import React from 'react'
import { AlertCircle } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error400 = () => {
  return (
    <ErrorPageBase
      errorCode="400"
      title="طلب غير صالح"
      description="الطلب الذي أرسلته غير صالح أو يحتوي على بيانات خاطئة. يرجى التحقق من البيانات المدخلة والمحاولة مرة أخرى."
      icon={AlertCircle}
      bgColor="bg-orange-100"
      iconColor="text-orange-600"
      buttonColor="bg-orange-600 hover:bg-orange-700"
      suggestions={[
        "تحقق من صحة البيانات المدخلة في النموذج",
        "تأكد من أن جميع الحقول المطلوبة مملوءة بشكل صحيح",
        "تحقق من تنسيق البريد الإلكتروني والأرقام",
        "حاول مسح ذاكرة التخزين المؤقت للمتصفح",
        "إذا استمرت المشكلة، اتصل بالدعم الفني"
      ]}
    />
  )
}

export default Error400

