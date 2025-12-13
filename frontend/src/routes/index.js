// Routes Configuration
import { lazy } from 'react'

// Lazy load components
const Dashboard = lazy(() => import('../components/Dashboard'))
const Products = lazy(() => import('../components/Products'))
const Batches = lazy(() => import('../components/Batches'))
const Reports = lazy(() => import('../components/Reports'))
const Settings = lazy(() => import('../components/Settings'))
const CompanySettings = lazy(() => import('../components/CompanySettings'))

// Error Pages
const Error404 = lazy(() => import('../components/ErrorPages/Error404'))
const Error500 = lazy(() => import('../components/ErrorPages/Error500'))
const Error502 = lazy(() => import('../components/ErrorPages/Error502'))
const Error503 = lazy(() => import('../components/ErrorPages/Error503'))
const Error504 = lazy(() => import('../components/ErrorPages/Error504'))
const Error505 = lazy(() => import('../components/ErrorPages/Error505'))

export const routes = [
  {
    path: '/',
    element: Dashboard,
    name: 'لوحة التحكم'
  },
  {
    path: '/dashboard',
    element: Dashboard,
    name: 'لوحة التحكم'
  },
  {
    path: '/products',
    element: Products,
    name: 'المنتجات'
  },
  {
    path: '/batches',
    element: Batches,
    name: 'اللوطات'
  },
  {
    path: '/reports',
    element: Reports,
    name: 'التقارير'
  },
  {
    path: '/settings',
    element: Settings,
    name: 'الإعدادات'
  },
  {
    path: '/company-settings',
    element: CompanySettings,
    name: 'إعدادات الشركة'
  },
  // Error Pages
  {
    path: '/error/404',
    element: Error404,
    name: 'صفحة غير موجودة'
  },
  {
    path: '/error/500',
    element: Error500,
    name: 'خطأ في الخادم'
  },
  {
    path: '/error/502',
    element: Error502,
    name: 'خطأ في البوابة'
  },
  {
    path: '/error/503',
    element: Error503,
    name: 'الخدمة غير متاحة'
  },
  {
    path: '/error/504',
    element: Error504,
    name: 'انتهت مهلة البوابة'
  },
  {
    path: '/error/505',
    element: Error505,
    name: 'إصدار HTTP غير مدعوم'
  }
]

export default routes
