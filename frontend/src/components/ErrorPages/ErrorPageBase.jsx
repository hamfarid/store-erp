import React from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  FileX, Server, Wifi, Shield, Clock, AlertTriangle, RefreshCw, Home, ArrowLeft
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const ErrorPageBase = ({ 
  errorCode, 
  title, 
  description, 
  suggestions = [], 
  showRefresh = true,
  showHome = true,
  showBack = true,
  icon: CustomIcon,
  bgColor = "bg-destructive/10",
  iconColor = "text-destructive",
  buttonColor = "bg-destructive hover:bg-red-700"
}) => {
  const navigate = useNavigate()

  const getDefaultIcon = () => {
    switch (errorCode) {
      case '404': return FileX
      case '500': return Server
      case '502': return Wifi
      case '503': return Shield
      case '504': return Clock
      case '505': return AlertTriangle
      default: return AlertTriangle
    }
  }

  const IconComponent = CustomIcon || getDefaultIcon()

  const handleRefresh = () => {
    window.location.reload()
  }

  const handleGoHome = () => {
    navigate('/')
  }

  const handleGoBack = () => {
    navigate(-1)
  }

  return (
    <div className="min-h-screen bg-muted/50 flex items-center justify-center px-4 py-8" dir="rtl">
      <div className="max-w-3xl w-full mx-auto text-center">
        {/* Error Icon and Code */}
        <div className={`${bgColor} rounded-full w-24 h-24 mx-auto mb-6 flex items-center justify-center shadow-lg`}>
          <IconComponent className={`w-12 h-12 ${iconColor}`} />
        </div>

        {/* Error Code */}
        <div className="mb-6">
          <h1 className="text-6xl md:text-7xl font-bold text-gray-300 mb-3">{errorCode}</h1>
          <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-3">{title}</h2>
          <p className="text-base md:text-lg text-muted-foreground mb-6 leading-relaxed px-4">{description}</p>
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div className="bg-white rounded-lg shadow-md border border-border p-5 md:p-6 mb-6 text-right max-w-2xl mx-auto">
            <h3 className="text-base md:text-lg font-semibold text-foreground mb-3">💡 اقتراحات للحل:</h3>
            <ul className="space-y-2 text-sm md:text-base text-foreground">
              {suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-primary-600 ml-2 mt-0.5">•</span>
                  <span className="flex-1">{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center items-center max-w-xl mx-auto">
          {showRefresh && (
            <button
              onClick={handleRefresh}
              className={`${buttonColor} text-white px-5 py-2.5 rounded-lg transition-colors flex items-center justify-center w-full sm:w-auto text-sm md:text-base font-medium shadow-sm hover:shadow-md`}
            >
              <RefreshCw className="w-4 h-4 ml-2" />
              إعادة المحاولة
            </button>
          )}
          
          {showHome && (
            <button
              onClick={handleGoHome}
              className="bg-primary-600 hover:bg-primary-700 text-white px-5 py-2.5 rounded-lg transition-colors flex items-center justify-center w-full sm:w-auto text-sm md:text-base font-medium shadow-sm hover:shadow-md"
            >
              <Home className="w-4 h-4 ml-2" />
              العودة للرئيسية
            </button>
          )}
          
          {showBack && (
            <button
              onClick={handleGoBack}
              className="bg-gray-600 hover:bg-gray-700 text-white px-5 py-2.5 rounded-lg transition-colors flex items-center justify-center w-full sm:w-auto text-sm md:text-base font-medium shadow-sm hover:shadow-md"
            >
              <ArrowLeft className="w-4 h-4 ml-2" />
              العودة للخلف
            </button>
          )}
        </div>

        {/* Additional Info */}
        <div className="mt-8 text-xs md:text-sm text-gray-500 px-4">
          <p className="mb-2">إذا استمرت المشكلة، يرجى الاتصال بفريق الدعم الفني</p>
          <p className="text-xs text-gray-400">
            <span className="font-medium">رمز الخطأ:</span> {errorCode} | 
            <span className="font-medium"> الوقت:</span> {new Date().toLocaleString('ar-EG')}
          </p>
        </div>
      </div>
    </div>
  )
}

export default ErrorPageBase

