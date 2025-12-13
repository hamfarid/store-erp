import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Code, Video, AlertTriangle, Lightbulb, HelpCircle
} from 'lucide-react'
import { toast } from 'react-hot-toast'

import ApiService from '../services/ApiService'

const SystemDocumentation = () => {
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [activeCategory, setActiveCategory] = useState('user-guide')
  const [expandedSections, setExpandedSections] = useState(new Set(['getting-started']))
  const [_documentation, setDocumentation] = useState({})

  const documentationCategories = [
    {
      id: 'user-guide',
      name: 'دليل المستخدم',
      icon: Users,
      description: 'دليل شامل لاستخدام النظام'
    },
    {
      id: 'admin-guide',
      name: 'دليل الإدارة',
      icon: Settings,
      description: 'دليل إدارة النظام والإعدادات'
    },
    {
      id: 'api-docs',
      name: 'توثيق APIs',
      icon: Code,
      description: 'توثيق تقني لواجهات البرمجة'
    },
    {
      id: 'tutorials',
      name: 'الدروس التعليمية',
      icon: Video,
      description: 'دروس تفاعلية وفيديوهات تعليمية'
    },
    {
      id: 'faq',
      name: 'الأسئلة الشائعة',
      icon: HelpCircle,
      description: 'إجابات على الأسئلة الأكثر شيوعاً'
    },
    {
      id: 'troubleshooting',
      name: 'حل المشاكل',
      icon: AlertTriangle,
      description: 'دليل حل المشاكل الشائعة'
    }
  ]

  const userGuideStructure = {
    'getting-started': {
      title: 'البدء السريع',
      icon: Lightbulb,
      sections: [
        { id: 'login', title: 'تسجيل الدخول', type: 'text' },
        { id: 'dashboard', title: 'لوحة التحكم الرئيسية', type: 'text' },
        { id: 'navigation', title: 'التنقل في النظام', type: 'video' },
        { id: 'first-steps', title: 'الخطوات الأولى', type: 'tutorial' }
      ]
    },
    'inventory-management': {
      title: 'إدارة المخزون',
      icon: FileText,
      sections: [
        { id: 'products', title: 'إدارة المنتجات', type: 'text' },
        { id: 'categories', title: 'إدارة الفئات', type: 'text' },
        { id: 'warehouses', title: 'إدارة المخازن', type: 'text' },
        { id: 'stock-movements', title: 'حركات المخزون', type: 'video' },
        { id: 'inventory-reports', title: 'تقارير المخزون', type: 'tutorial' }
      ]
    },
    'invoicing': {
      title: 'إدارة الفواتير',
      icon: FileText,
      sections: [
        { id: 'create-invoice', title: 'إنشاء فاتورة جديدة', type: 'tutorial' },
        { id: 'invoice-types', title: 'أنواع الفواتير', type: 'text' },
        { id: 'payment-tracking', title: 'تتبع المدفوعات', type: 'text' },
        { id: 'invoice-reports', title: 'تقارير الفواتير', type: 'video' }
      ]
    },
    'customers-suppliers': {
      title: 'العملاء والموردين',
      icon: Users,
      sections: [
        { id: 'customer-management', title: 'إدارة العملاء', type: 'text' },
        { id: 'supplier-management', title: 'إدارة الموردين', type: 'text' },
        { id: 'contact-management', title: 'إدارة جهات الاتصال', type: 'tutorial' }
      ]
    },
    'reports': {
      title: 'التقارير والتحليلات',
      icon: FileText,
      sections: [
        { id: 'financial-reports', title: 'التقارير المالية', type: 'text' },
        { id: 'inventory-reports', title: 'تقارير المخزون', type: 'text' },
        { id: 'sales-reports', title: 'تقارير المبيعات', type: 'video' },
        { id: 'custom-reports', title: 'التقارير المخصصة', type: 'tutorial' }
      ]
    }
  }

  const faqData = [
    {
      question: 'كيف يمكنني إعادة تعيين كلمة المرور؟',
      answer: 'يمكنك إعادة تعيين كلمة المرور من خلال النقر على "نسيت كلمة المرور" في صفحة تسجيل الدخول، ثم اتباع التعليمات المرسلة إلى بريدك الإلكتروني.'
    },
    {
      question: 'كيف يمكنني إضافة منتج جديد؟',
      answer: 'انتقل إلى قسم "المنتجات" من القائمة الجانبية، ثم انقر على "إضافة منتج جديد" واملأ البيانات المطلوبة.'
    },
    {
      question: 'كيف يمكنني تصدير التقارير؟',
      answer: 'في صفحة التقارير، اختر التقرير المطلوب ثم انقر على زر "تصدير" واختر الصيغة المناسبة (PDF، Excel، CSV).'
    },
    {
      question: 'كيف يمكنني تغيير إعدادات الشركة؟',
      answer: 'انتقل إلى "الإعدادات" > "إعدادات الشركة" من القائمة الرئيسية، ثم قم بتعديل البيانات المطلوبة واحفظ التغييرات.'
    },
    {
      question: 'كيف يمكنني إنشاء نسخة احتياطية من البيانات؟',
      answer: 'انتقل إلى "الإعدادات" > "النسخ الاحتياطي" وانقر على "إنشاء نسخة احتياطية جديدة".'
    }
  ]

  const troubleshootingData = [
    {
      problem: 'لا يمكنني تسجيل الدخول',
      solutions: [
        'تأكد من صحة اسم المستخدم وكلمة المرور',
        'تحقق من اتصال الإنترنت',
        'امسح ذاكرة التخزين المؤقت للمتصفح',
        'تواصل مع مدير النظام إذا استمرت المشكلة'
      ]
    },
    {
      problem: 'النظام بطيء في الاستجابة',
      solutions: [
        'تحقق من سرعة الإنترنت',
        'أغلق التطبيقات الأخرى غير المستخدمة',
        'امسح ذاكرة التخزين المؤقت',
        'أعد تشغيل المتصفح'
      ]
    },
    {
      problem: 'لا تظهر البيانات في التقارير',
      solutions: [
        'تأكد من اختيار النطاق الزمني الصحيح',
        'تحقق من وجود بيانات في الفترة المحددة',
        'تأكد من صلاحياتك لعرض التقرير',
        'جرب تحديث الصفحة'
      ]
    }
  ]

  useEffect(() => {
    loadDocumentation()
  }, [])

  const loadDocumentation = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/api/documentation')
      if (response.success) {
        setDocumentation(response.data)
      }
    } catch (error) {
      } finally {
      setLoading(false)
    }
  }

  const toggleSection = (sectionId) => {
    setExpandedSections(prev => {
      const newSet = new Set(prev)
      if (newSet.has(sectionId)) {
        newSet.delete(sectionId)
      } else {
        newSet.add(sectionId)
      }
      return newSet
    })
  }

  const downloadDocumentation = async (format) => {
    try {
      const response = await ApiService.get(`/api/documentation/export?format=${format}`)
      if (response.success) {
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `system-documentation.${format}`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        toast.success('تم تحميل التوثيق بنجاح')
      }
    } catch (error) {
      toast.error('خطأ في تحميل التوثيق')
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'video':
        return <Video className="w-4 h-4 text-primary-600" />
      case 'tutorial':
        return <Lightbulb className="w-4 h-4 text-accent" />
      case 'image':
        return <Image className="w-4 h-4 text-primary" />
      default:
        return <FileText className="w-4 h-4 text-muted-foreground" />
    }
  }

  const filteredContent = () => {
    if (!searchTerm) return null
    
    // Simple search implementation
    const results = []
    Object.entries(userGuideStructure).forEach(([key, category]) => {
      category.sections.forEach(section => {
        if (section.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            category.title.toLowerCase().includes(searchTerm.toLowerCase())) {
          results.push({
            categoryId: key,
            categoryTitle: category.title,
            sectionId: section.id,
            sectionTitle: section.title,
            type: section.type
          })
        }
      })
    })
    
    return results
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Book className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h1 className="text-2xl font-bold text-foreground">توثيق النظام</h1>
              <p className="text-muted-foreground">دليل شامل لاستخدام وإدارة النظام</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <button
              onClick={() => downloadDocumentation('pdf')}
              className="inline-flex items-center px-4 py-2 border border-border rounded-md shadow-sm text-sm font-medium text-foreground bg-white hover:bg-muted/50"
            >
              <Download className="w-4 h-4 ml-2" />
              تحميل PDF
            </button>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="relative">
          <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="البحث في التوثيق..."
            className="w-full pr-10 pl-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
        
        {searchTerm && (
          <div className="mt-4">
            <h3 className="text-sm font-medium text-foreground mb-2">نتائج البحث:</h3>
            <div className="space-y-2">
              {filteredContent()?.map((result, index) => (
                <div key={index} className="flex items-center p-2 hover:bg-muted/50 rounded-md cursor-pointer">
                  {getTypeIcon(result.type)}
                  <span className="mr-2 text-sm text-foreground">{result.sectionTitle}</span>
                  <span className="text-xs text-gray-500">في {result.categoryTitle}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border border-border p-4">
            <h3 className="text-lg font-semibold text-foreground mb-4">الأقسام</h3>
            <nav className="space-y-2">
              {documentationCategories.map((category) => {
                const IconComponent = category.icon
                return (
                  <button
                    key={category.id}
                    onClick={() => setActiveCategory(category.id)}
                    className={`w-full flex items-center p-3 text-right rounded-md transition-colors ${
                      activeCategory === category.id
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-foreground hover:bg-muted'
                    }`}
                  >
                    <IconComponent className="w-5 h-5 ml-2" />
                    <span className="text-sm font-medium">{category.name}</span>
                  </button>
                )
              })}
            </nav>
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow-sm border border-border">
            {activeCategory === 'user-guide' && (
              <div className="p-6">
                <h2 className="text-xl font-bold text-foreground mb-6">دليل المستخدم</h2>
                
                <div className="space-y-4">
                  {Object.entries(userGuideStructure).map(([key, category]) => {
                    const IconComponent = category.icon
                    const isExpanded = expandedSections.has(key)
                    
                    return (
                      <div key={key} className="border border-border rounded-lg">
                        <button
                          onClick={() => toggleSection(key)}
                          className="w-full flex items-center justify-between p-4 text-right hover:bg-muted/50"
                        >
                          <div className="flex items-center">
                            <IconComponent className="w-5 h-5 text-primary-600 ml-2" />
                            <span className="font-medium text-foreground">{category.title}</span>
                          </div>
                          {isExpanded ? (
                            <ChevronDown className="w-5 h-5 text-gray-400" />
                          ) : (
                            <ChevronRight className="w-5 h-5 text-gray-400" />
                          )}
                        </button>
                        
                        {isExpanded && (
                          <div className="border-t border-border p-4">
                            <div className="space-y-2">
                              {category.sections.map((section) => (
                                <div key={section.id} className="flex items-center justify-between p-2 hover:bg-muted/50 rounded-md">
                                  <div className="flex items-center">
                                    {getTypeIcon(section.type)}
                                    <span className="mr-2 text-sm text-foreground">{section.title}</span>
                                  </div>
                                  <ExternalLink className="w-4 h-4 text-gray-400" />
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {activeCategory === 'faq' && (
              <div className="p-6">
                <h2 className="text-xl font-bold text-foreground mb-6">الأسئلة الشائعة</h2>
                
                <div className="space-y-4">
                  {faqData.map((faq, index) => (
                    <div key={index} className="border border-border rounded-lg p-4">
                      <h3 className="font-medium text-foreground mb-2">{faq.question}</h3>
                      <p className="text-muted-foreground text-sm">{faq.answer}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeCategory === 'troubleshooting' && (
              <div className="p-6">
                <h2 className="text-xl font-bold text-foreground mb-6">حل المشاكل</h2>
                
                <div className="space-y-6">
                  {troubleshootingData.map((item, index) => (
                    <div key={index} className="border border-border rounded-lg p-4">
                      <h3 className="font-medium text-foreground mb-3 flex items-center">
                        <AlertTriangle className="w-5 h-5 text-accent ml-2" />
                        {item.problem}
                      </h3>
                      <div className="space-y-2">
                        <p className="text-sm font-medium text-foreground">الحلول المقترحة:</p>
                        <ul className="list-disc list-inside space-y-1">
                          {item.solutions.map((solution, sIndex) => (
                            <li key={sIndex} className="text-sm text-muted-foreground">{solution}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {!['user-guide', 'faq', 'troubleshooting'].includes(activeCategory) && (
              <div className="p-6">
                <div className="text-center py-12">
                  <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-foreground mb-2">
                    {documentationCategories.find(c => c.id === activeCategory)?.name}
                  </h3>
                  <p className="text-muted-foreground">
                    {documentationCategories.find(c => c.id === activeCategory)?.description}
                  </p>
                  <p className="text-sm text-gray-500 mt-4">
                    هذا القسم قيد التطوير وسيتم إضافة المحتوى قريباً
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default SystemDocumentation

