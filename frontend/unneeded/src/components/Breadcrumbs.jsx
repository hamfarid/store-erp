import React from 'react'
import { ChevronLeft, Home } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'

const Breadcrumbs = () => {
  const location = useLocation()
  
  // خريطة المسارات والأسماء العربية
  const pathNames = {
    '': 'الرئيسية',
    'products': 'المنتجات',
    'customers': 'العملاء',
    'suppliers': 'الموردين',
    'sales-invoices': 'فواتير المبيعات',
    'purchase-invoices': 'فواتير المشتريات',
    'reports': 'التقارير',
    'settings': 'الإعدادات',
    'admin': 'الإدارة',
    'accounting': 'المحاسبة',
    'currencies': 'العملات',
    'cash-boxes': 'الصناديق',
    'vouchers': 'قسائم الدفع',
    'profit-loss': 'الأرباح والخسائر',
    'sales': 'المبيعات',
    'inventory': 'المخزون',
    'financial': 'المالية',
    'users': 'المستخدمين',
    'roles': 'الأدوار',
    'security': 'الأمان',
    'company': 'الشركة',
    'system': 'النظام',
    'categories': 'الفئات',
    'warehouses': 'المخازن',
    'stock-movements': 'حركات المخزون',
    'lots': 'اللوطات',
    'import-export': 'الاستيراد والتصدير',
    'print-export': 'الطباعة والتصدير'
  }

  // تقسيم المسار إلى أجزاء
  const pathSegments = location.pathname.split('/').filter(segment => segment !== '')
  
  // إنشاء مصفوفة breadcrumbs
  const breadcrumbs = [
    { path: '/', name: 'الرئيسية', icon: Home }
  ]

  let currentPath = ''
  pathSegments.forEach((segment, index) => {
    currentPath += `/${segment}`
    const name = pathNames[segment] || segment
    breadcrumbs.push({
      path: currentPath,
      name: name,
      isLast: index === pathSegments.length - 1
    })
  })

  // إذا كنا في الصفحة الرئيسية، لا نعرض breadcrumbs
  if (location.pathname === '/') {
    return null
  }

  return (
    <nav className="flex items-center space-x-2 space-x-reverse text-sm text-muted-foreground mb-6" dir="rtl">
      {breadcrumbs.map((breadcrumb, index) => (
        <div key={breadcrumb.path} className="flex items-center">
          {index > 0 && (
            <ChevronLeft className="w-4 h-4 mx-2 text-gray-400" />
          )}
          
          {breadcrumb.isLast ? (
            <span className="flex items-center font-medium text-foreground">
              {breadcrumb.icon && <breadcrumb.icon className="w-4 h-4 ml-1" />}
              {breadcrumb.name}
            </span>
          ) : (
            <Link
              to={breadcrumb.path}
              className="flex items-center hover:text-primary-600 transition-colors"
            >
              {breadcrumb.icon && <breadcrumb.icon className="w-4 h-4 ml-1" />}
              {breadcrumb.name}
            </Link>
          )}
        </div>
      ))}
    </nav>
  )
}

export default Breadcrumbs

