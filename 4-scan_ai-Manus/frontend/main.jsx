// FILE: frontend/main.jsx | PURPOSE: Frontend application entry point | OWNER: Frontend Team | LAST-AUDITED: 2025-11-18
// نقطة دخول التطبيق المحدثة لنظام Gaara AI
// الإصدار: 3.0.0 (Canonical)
// تم التحديث: 2025-11-18
// المطور: Gaara Group & Autonomous AI Agent

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

// استيراد الأنماط العامة
import './index.css';

// إعداد متغيرات البيئة
if (import.meta.env.DEV) {
  console.log('🚀 تشغيل نظام Gaara AI في وضع التطوير');
  console.log('📡 API URL:', import.meta.env.VITE_API_URL || 'http://localhost:8000/api');
  console.log('🔧 Version:', import.meta.env.VITE_APP_VERSION || '3.0.0');
}

// إعداد Service Worker للـ PWA
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('✅ Service Worker مسجل بنجاح:', registration.scope);
      })
      .catch((error) => {
        console.log('❌ فشل تسجيل Service Worker:', error);
      });
  });
}

// إعداد معالجة الأخطاء العامة
window.addEventListener('error', (event) => {
  console.error('خطأ عام في التطبيق:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Promise مرفوض غير معالج:', event.reason);
});

// إنشاء جذر التطبيق وتشغيله
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// إعداد Hot Module Replacement للتطوير
if (import.meta.hot) {
  import.meta.hot.accept();
}

