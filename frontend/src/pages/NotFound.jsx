import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';

const NotFound = () => {
  const navigate = useNavigate();

  const getPageContent = () => {
    switch ('NotFound') {
      case 'NotFound':
        return {
          title: '404 - الصفحة غير موجودة',
          message: 'عذراً، الصفحة التي تبحث عنها غير موجودة.',
          icon: '🔍',
          showHomeButton: true
        };
      case 'Unauthorized':
        return {
          title: '403 - غير مصرح',
          message: 'عذراً، ليس لديك صلاحية للوصول إلى هذه الصفحة.',
          icon: '🔒',
          showHomeButton: true
        };
      case 'ServerError':
        return {
          title: '500 - خطأ في الخادم',
          message: 'عذراً، حدث خطأ في الخادم. يرجى المحاولة لاحقاً.',
          icon: '⚠️',
          showHomeButton: true
        };
      case 'Maintenance':
        return {
          title: 'صيانة النظام',
          message: 'النظام قيد الصيانة حالياً. سيعود قريباً.',
          icon: '🔧',
          showHomeButton: false
        };
      case 'ComingSoon':
        return {
          title: 'قريباً',
          message: 'هذه الميزة قيد التطوير وستكون متاحة قريباً.',
          icon: '🚀',
          showHomeButton: true
        };
      default:
        return {
          title: 'NotFound',
          message: 'صفحة NotFound',
          icon: '📄',
          showHomeButton: true
        };
    }
  };

  const content = getPageContent();

  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/50">
      <div className="max-w-md w-full bg-primary shadow-lg rounded-lg p-8 text-center">
        <div className="text-6xl mb-4">{content.icon}</div>
        
        <h1 className="text-2xl font-bold text-foreground mb-4">
          {content.title}
        </h1>
        
        <p className="text-muted-foreground mb-8">
          {content.message}
        </p>
        
        <div className="space-y-3">
          {content.showHomeButton && (
            <Button
              onClick={() => navigate('/')}
              className="w-full"
            >
              العودة للرئيسية
            </Button>
          )}
          
          <Button
            variant="outline"
            onClick={() => navigate(-1)}
            className="w-full"
          >
            رجوع
          </Button>
          
          <Button
            variant="ghost"
            onClick={() => window.location.reload()}
            className="w-full"
          >
            إعادة تحميل
          </Button>
        </div>
      </div>
    </div>
  );
};

export default NotFound;