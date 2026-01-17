/**
 * Network Error Page Component
 * 
 * Displays when "Failed to fetch" or network errors occur
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  WifiOff, 
  RefreshCw, 
  Server, 
  AlertTriangle,
  CheckCircle,
  Loader2,
  Home,
  Settings
} from 'lucide-react';
import { checkServerStatus, PORTS } from '../config/api';

const NetworkErrorPage = ({ 
  error = null, 
  onRetry = null,
  showBackButton = true 
}) => {
  const navigate = useNavigate();
  const [isChecking, setIsChecking] = useState(false);
  const [serverStatus, setServerStatus] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  // Check server status on mount
  useEffect(() => {
    handleCheckServer();
  }, []);

  const handleCheckServer = async () => {
    setIsChecking(true);
    try {
      const isOnline = await checkServerStatus();
      setServerStatus(isOnline);
      if (isOnline && onRetry) {
        // Server is back online, trigger retry
        onRetry();
      }
    } catch {
      setServerStatus(false);
    }
    setIsChecking(false);
  };

  const handleRetry = () => {
    setRetryCount(prev => prev + 1);
    if (onRetry) {
      onRetry();
    } else {
      window.location.reload();
    }
  };

  const handleGoHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4" dir="rtl">
      <div className="max-w-lg w-full">
        {/* Main Card */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 shadow-2xl">
          {/* Icon */}
          <div className="flex justify-center mb-6">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center animate-pulse">
              <WifiOff className="w-12 h-12 text-white" />
            </div>
          </div>

          {/* Title */}
          <h1 className="text-3xl font-bold text-white text-center mb-4">
            تعذر الاتصال بالخادم
          </h1>
          <p className="text-gray-300 text-center mb-6">
            لا يمكن الوصول إلى الخادم. تأكد من تشغيل الخدمات التالية:
          </p>

          {/* Server Status */}
          <div className="space-y-3 mb-8">
            {/* Backend Status */}
            <div className="flex items-center justify-between bg-white/5 rounded-lg p-4">
              <div className="flex items-center gap-3">
                <Server className="w-5 h-5 text-blue-400" />
                <div>
                  <p className="text-white font-medium">خادم API</p>
                  <p className="text-gray-400 text-sm">المنفذ {PORTS.BACKEND}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {isChecking ? (
                  <Loader2 className="w-5 h-5 text-yellow-400 animate-spin" />
                ) : serverStatus ? (
                  <CheckCircle className="w-5 h-5 text-green-400" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-red-400" />
                )}
                <span className={`text-sm ${serverStatus ? 'text-green-400' : 'text-red-400'}`}>
                  {isChecking ? 'جاري الفحص...' : serverStatus ? 'متصل' : 'غير متصل'}
                </span>
              </div>
            </div>

            {/* Redis Status */}
            <div className="flex items-center justify-between bg-white/5 rounded-lg p-4">
              <div className="flex items-center gap-3">
                <Server className="w-5 h-5 text-red-400" />
                <div>
                  <p className="text-white font-medium">Redis Cache</p>
                  <p className="text-gray-400 text-sm">المنفذ {PORTS.REDIS}</p>
                </div>
              </div>
              <span className="text-gray-400 text-sm">اختياري</span>
            </div>

            {/* Database Status */}
            <div className="flex items-center justify-between bg-white/5 rounded-lg p-4">
              <div className="flex items-center gap-3">
                <Server className="w-5 h-5 text-green-400" />
                <div>
                  <p className="text-white font-medium">قاعدة البيانات</p>
                  <p className="text-gray-400 text-sm">المنفذ {PORTS.DATABASE}</p>
                </div>
              </div>
              <span className="text-gray-400 text-sm">SQLite/PostgreSQL</span>
            </div>
          </div>

          {/* Error Details */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6">
              <p className="text-red-300 text-sm">
                <strong>تفاصيل الخطأ:</strong> {error.message || error}
              </p>
            </div>
          )}

          {/* Actions */}
          <div className="space-y-3">
            <button
              onClick={handleRetry}
              className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white py-3 px-6 rounded-xl font-medium transition-all duration-200 shadow-lg hover:shadow-blue-500/25"
            >
              <RefreshCw className={`w-5 h-5 ${isChecking ? 'animate-spin' : ''}`} />
              إعادة المحاولة {retryCount > 0 && `(${retryCount})`}
            </button>

            <button
              onClick={handleCheckServer}
              disabled={isChecking}
              className="w-full flex items-center justify-center gap-2 bg-white/10 hover:bg-white/20 text-white py-3 px-6 rounded-xl font-medium transition-all duration-200 disabled:opacity-50"
            >
              <Server className="w-5 h-5" />
              فحص حالة الخادم
            </button>

            {showBackButton && (
              <button
                onClick={handleGoHome}
                className="w-full flex items-center justify-center gap-2 bg-transparent border border-white/20 hover:bg-white/10 text-white py-3 px-6 rounded-xl font-medium transition-all duration-200"
              >
                <Home className="w-5 h-5" />
                العودة للرئيسية
              </button>
            )}
          </div>

          {/* Help Text */}
          <div className="mt-8 p-4 bg-white/5 rounded-lg">
            <h3 className="text-white font-medium mb-2 flex items-center gap-2">
              <Settings className="w-4 h-4" />
              كيفية تشغيل الخادم:
            </h3>
            <div className="text-gray-400 text-sm space-y-2">
              <p className="font-mono bg-black/30 p-2 rounded">
                cd backend && python -m src.main
              </p>
              <p>أو</p>
              <p className="font-mono bg-black/30 p-2 rounded">
                docker-compose up -d
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-gray-500 text-sm mt-6">
          نظام إدارة المخزون v1.5.0
        </p>
      </div>
    </div>
  );
};

export default NetworkErrorPage;

