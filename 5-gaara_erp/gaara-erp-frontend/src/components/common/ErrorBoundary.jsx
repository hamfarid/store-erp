import React from "react"
import { AlertTriangle, RefreshCw, Home } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

/**
 * ErrorBoundary Component
 * Catches JavaScript errors anywhere in the child component tree
 */
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo)
    this.setState({
      error,
      errorInfo,
    })
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null })
  }

  render() {
    if (this.state.hasError) {
      const { fallback, showDetails = false } = this.props

      if (fallback) {
        return fallback(this.state.error, this.handleReset)
      }

      return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
          <Card className="max-w-2xl w-full border-red-200 dark:border-red-800">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-3 rounded-full bg-red-100 dark:bg-red-900/30">
                  <AlertTriangle className="w-6 h-6 text-red-600 dark:text-red-400" />
                </div>
                <div>
                  <CardTitle className="text-red-600 dark:text-red-400">
                    حدث خطأ غير متوقع
                  </CardTitle>
                  <CardDescription>
                    عذراً، حدث خطأ أثناء تحميل هذه الصفحة
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {showDetails && this.state.error && (
                <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
                  <p className="font-mono text-sm text-red-800 dark:text-red-200 break-all">
                    {this.state.error.toString()}
                  </p>
                  {this.state.errorInfo && (
                    <details className="mt-2">
                      <summary className="cursor-pointer text-sm font-medium text-red-700 dark:text-red-300">
                        تفاصيل الخطأ
                      </summary>
                      <pre className="mt-2 text-xs text-red-600 dark:text-red-400 overflow-auto">
                        {this.state.errorInfo.componentStack}
                      </pre>
                    </details>
                  )}
                </div>
              )}

              <div className="flex flex-wrap gap-3">
                <Button onClick={this.handleReset} className="gap-2">
                  <RefreshCw className="w-4 h-4" />
                  إعادة المحاولة
                </Button>
                <Button variant="outline" onClick={() => (window.location.href = "/dashboard")} className="gap-2">
                  <Home className="w-4 h-4" />
                  العودة للوحة التحكم
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
