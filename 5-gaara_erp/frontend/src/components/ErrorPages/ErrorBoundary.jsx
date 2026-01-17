import React from 'react'
import { AlertTriangle } from 'lucide-react'
import PropTypes from 'prop-types'
import Error500 from './Error500'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    }
  }

  static getDerivedStateFromError(error) {
    // تحديث state ليظهر UI الخطأ
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    // تسجيل تفاصيل الخطأ
    this.setState({
      error: error,
      errorInfo: errorInfo
    })

    // تسجيل الخطأ للمطورين
    // يمكن إضافة إرسال الخطأ لخدمة تسجيل الأخطاء هنا
    // مثل Sentry أو LogRocket
  }

  render() {
    if (this.state.hasError) {
      const _suggestions = [
        "أعد تحميل الصفحة",
        "امسح ذاكرة التخزين المؤقت للمتصفح",
        "تحقق من اتصالك بالإنترنت",
        "جرب استخدام متصفح آخر",
        "تأكد من أن JavaScript مفعل في المتصفح",
        "اتصل بفريق الدعم الفني مع تفاصيل الخطأ"
      ]

      return (
        <>
          <Error500 />
          
          {/* معلومات الخطأ للمطورين (في وضع التطوير فقط) */}
          {import.meta.env.DEV && this.state.errorInfo && (
            <div className="fixed bottom-4 right-4 max-w-md bg-white border border-destructive/30 rounded-lg shadow-lg p-4 text-sm" dir="ltr">
              <h4 className="font-bold text-destructive mb-2">Error Details (Dev Mode):</h4>
              <div className="text-foreground mb-2">
                <strong>Error:</strong> {this.state.error && this.state.error.toString()}
              </div>
              <div className="text-foreground max-h-32 overflow-y-auto">
                <strong>Stack:</strong>
                <pre className="text-xs mt-1 whitespace-pre-wrap">
                  {this.state.errorInfo && this.state.errorInfo.componentStack}
                </pre>
              </div>
            </div>
          )}
        </>
      )
    }

    return this.props.children
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired
}

export default ErrorBoundary
