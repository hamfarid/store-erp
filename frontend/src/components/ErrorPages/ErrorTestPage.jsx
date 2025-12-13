import React, { useState } from 'react'

const ErrorTestPage = () => {
  const [boom, setBoom] = useState(false)

  if (boom) {
    // This will be caught by ErrorBoundary and render Error500
    throw new Error('Intentional test error from ErrorTestPage')
  }

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">صفحة اختبار الأخطاء</h1>
      <p className="text-muted-foreground mb-6">استخدم هذه الصفحة لاختبار ErrorBoundary. عند الضغط على الزر سيتم إطلاق خطأ متعمد.</p>
      <button
        onClick={() => setBoom(true)}
        className="px-4 py-2 rounded-md bg-destructive text-white hover:bg-red-700"
      >
        إطلاق خطأ تجريبي
      </button>
    </div>
  )
}

export default ErrorTestPage

