import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Error Pages
import Error401 from './Error401';
import Error402 from './Error402';
import Error403 from './Error403';
import Error404 from './Error404';
import Error405 from './Error405';
import Error406 from './Error406';
import Error500 from './Error500';
import Error501 from './Error501';
import Error502 from './Error502';
import Error503 from './Error503';
import Error504 from './Error504';
import Error505 from './Error505';
import Error506 from './Error506';

/**
 * Error Routes Component
 * 
 * Renders all error page routes.
 * Import this in your main App or Router component:
 * 
 * <ErrorRoutes />
 */
const ErrorRoutes = () => {
  return (
    <Routes>
      {/* 4xx Client Errors */}
      <Route path="/401" element={<Error401 />} />
      <Route path="/402" element={<Error402 />} />
      <Route path="/403" element={<Error403 />} />
      <Route path="/404" element={<Error404 />} />
      <Route path="/405" element={<Error405 />} />
      <Route path="/406" element={<Error406 />} />
      
      {/* 5xx Server Errors */}
      <Route path="/500" element={<Error500 />} />
      <Route path="/501" element={<Error501 />} />
      <Route path="/502" element={<Error502 />} />
      <Route path="/503" element={<Error503 />} />
      <Route path="/504" element={<Error504 />} />
      <Route path="/505" element={<Error505 />} />
      <Route path="/506" element={<Error506 />} />
      
      {/* Catch-all for 404 */}
      <Route path="*" element={<Error404 />} />
    </Routes>
  );
};

export default ErrorRoutes;

/**
 * Error Routes Configuration
 * 
 * Use this array to add error routes to your main router configuration.
 */
export const errorRouteConfig = [
  { path: '/401', element: Error401, title: 'غير مصرح - 401' },
  { path: '/402', element: Error402, title: 'الدفع مطلوب - 402' },
  { path: '/403', element: Error403, title: 'ممنوع الوصول - 403' },
  { path: '/404', element: Error404, title: 'الصفحة غير موجودة - 404' },
  { path: '/405', element: Error405, title: 'طريقة غير مسموحة - 405' },
  { path: '/406', element: Error406, title: 'غير مقبول - 406' },
  { path: '/500', element: Error500, title: 'خطأ في الخادم - 500' },
  { path: '/501', element: Error501, title: 'غير منفذ - 501' },
  { path: '/502', element: Error502, title: 'بوابة خاطئة - 502' },
  { path: '/503', element: Error503, title: 'الخدمة غير متاحة - 503' },
  { path: '/504', element: Error504, title: 'انتهت مهلة البوابة - 504' },
  { path: '/505', element: Error505, title: 'إصدار HTTP غير مدعوم - 505' },
  { path: '/506', element: Error506, title: 'تفاوض متغير - 506' },
];

