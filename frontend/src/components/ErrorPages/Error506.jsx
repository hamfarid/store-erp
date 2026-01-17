import React from 'react'
import { GitBranch } from 'lucide-react'
import ErrorPageBase from './ErrorPageBase'

const Error506 = () => {
  return (
    <ErrorPageBase
      errorCode="506"
      title="تفاوض المتغير يتسبب في حلقة"
      description="الخادم اكتشف حلقة لا نهائية أثناء معالجة طلبك. يرجى المحاولة مرة أخرى لاحقاً."
      icon={GitBranch}
      bgColor="bg-indigo-100"
      iconColor="text-indigo-600"
      buttonColor="bg-indigo-600 hover:bg-indigo-700"
      suggestions={[
        "هذا خطأ في إعدادات الخادم",
        "حاول مسح ذاكرة التخزين المؤقت للمتصفح",
        "انتظر بضع دقائق وحاول مرة أخرى",
        "اتصل بفريق الدعم الفني إذا استمرت المشكلة"
      ]}
    />
  )
}

export default Error506

