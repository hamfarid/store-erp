/**
 * Error 500 Page - Internal Server Error
 * @file pages/errors/Error500.jsx
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertTriangle, RefreshCw, Home, AlertCircle } from 'lucide-react';

// UI Components
import { Button } from '../../components/UI/button';
import { Card, CardContent } from '../../components/UI/card';

// ============================================
// Main Error 500 Component
// ============================================
const Error500 = () => {
  const navigate = useNavigate();
  const errorId = Math.random().toString(36).substring(7).toUpperCase();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-600 via-red-700 to-orange-600 p-8">
      <div className="max-w-2xl w-full text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-32 h-32 bg-white/20 backdrop-blur-sm rounded-full mb-8 shadow-2xl animate-pulse">
          <AlertTriangle className="h-16 w-16 text-white" />
        </div>

        {/* Error Code */}
        <h1 className="text-9xl font-bold text-white mb-4 drop-shadow-2xl">500</h1>

        {/* Title */}
        <h2 className="text-3xl font-bold text-white mb-4">خطأ في الخادم</h2>

        {/* Description */}
        <p className="text-white/90 text-lg mb-8 max-w-md mx-auto">
          حدث خطأ داخلي في الخادم.
          <br />
          فريقنا التقني يعمل على إصلاح المشكلة. يرجى المحاولة لاحقاً.
        </p>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <Button
            size="lg"
            onClick={() => window.location.reload()}
            className="bg-white text-red-600 hover:bg-red-50"
          >
            <RefreshCw className="h-5 w-5" />
            إعادة المحاولة
          </Button>
          <Button
            variant="outline"
            size="lg"
            onClick={() => navigate('/dashboard')}
            className="border-white text-white hover:bg-white/10"
          >
            <Home className="h-5 w-5" />
            الصفحة الرئيسية
          </Button>
        </div>

        {/* Error Details */}
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardContent className="p-4">
            <div className="space-y-2">
              <div className="flex items-center justify-center gap-2 text-white/80">
                <AlertCircle className="h-4 w-4" />
                <p className="text-sm font-mono">HTTP 500 - Internal Server Error</p>
              </div>
              <p className="text-white/60 text-xs">
                Reference ID: {errorId}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Error500;
