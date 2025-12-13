import React from 'react'
import { Ban } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error405 = () => {
  return (
    <ErrorPageBase
      errorCode="405"
      title="الطريقة غير مسموحة"
      description="طريقة الطلب المستخدمة غير مدعومة لهذا المورد. يرجى التحقق من طريقة الطلب والمحاولة مرة أخرى."
      icon={Ban}
      bgColor="bg-red-100"
      iconColor="text-red-600"
      buttonColor="bg-red-600 hover:bg-red-700"
      suggestions={[
        "تحقق من أنك تستخدم طريقة HTTP الصحيحة (GET, POST, PUT, DELETE)",
        "قد يكون هذا المورد للقراءة فقط",
        "راجع وثائق API للتحقق من الطرق المدعومة",
        "اتصل بفريق الدعم الفني إذا كنت تعتقد أن هذا خطأ"
      ]}
    />
  )
}

export default Error405

