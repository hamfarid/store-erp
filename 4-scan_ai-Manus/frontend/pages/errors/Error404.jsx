/**
 * Error 404 Page - Not Found
 * @file pages/errors/Error404.jsx
 */

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Home, ArrowRight, AlertCircle } from 'lucide-react';

// UI Components
import { Button } from '../../components/UI/button';
import { Card, CardContent } from '../../components/UI/card';

// ============================================
// Main Error 404 Component
// ============================================
const Error404 = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 p-8">
      <div className="max-w-2xl w-full text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-32 h-32 bg-white/20 backdrop-blur-sm rounded-full mb-8 shadow-2xl">
          <Search className="h-16 w-16 text-white" />
        </div>

        {/* Error Code */}
        <h1 className="text-9xl font-bold text-white mb-4 drop-shadow-2xl">404</h1>

        {/* Title */}
        <h2 className="text-3xl font-bold text-white mb-4">الصفحة غير موجودة</h2>

        {/* Description */}
        <p className="text-white/90 text-lg mb-8 max-w-md mx-auto">
          عذراً، الصفحة التي تبحث عنها غير موجودة أو تم نقلها.
          <br />
          تأكد من صحة الرابط وحاول مرة أخرى.
        </p>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <Button
            size="lg"
            onClick={() => navigate('/dashboard')}
            className="bg-white text-blue-600 hover:bg-blue-50"
          >
            <Home className="h-5 w-5" />
            الصفحة الرئيسية
          </Button>
          <Button
            variant="outline"
            size="lg"
            onClick={() => window.history.back()}
            className="border-white text-white hover:bg-white/10"
          >
            <ArrowRight className="h-5 w-5" />
            العودة للخلف
          </Button>
        </div>

        {/* Error Details */}
        <Card className="bg-white/10 backdrop-blur-sm border-white/20">
          <CardContent className="p-4">
            <div className="flex items-center justify-center gap-2 text-white/80">
              <AlertCircle className="h-4 w-4" />
              <p className="text-sm font-mono">HTTP 404 - Not Found</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Error404;
