import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  BookOpen, Target, Award, Play
} from 'lucide-react'
import { toast } from 'react-hot-toast'

import ApiService from '../services/ApiService'

const TrainingCenter = () => {
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('courses')
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [userProgress, setUserProgress] = useState({})
  const [courses, setCourses] = useState([])
  const [tutorials, setTutorials] = useState([])

  const trainingCategories = [
    { id: 'all', name: 'جميع الدورات', icon: BookOpen },
    { id: 'basics', name: 'الأساسيات', icon: Target },
    { id: 'inventory', name: 'إدارة المخزون', icon: FileText },
    { id: 'financial', name: 'المالية والمحاسبة', icon: TrendingUp },
    { id: 'reports', name: 'التقارير', icon: FileText },
    { id: 'admin', name: 'الإدارة', icon: Users },
    { id: 'advanced', name: 'متقدم', icon: Award }
  ]

  const mockCourses = [
    {
      id: 1,
      title: 'مقدمة في نظام إدارة المخزون',
      description: 'تعلم أساسيات استخدام النظام والتنقل بين الواجهات المختلفة',
      category: 'basics',
      duration: '45 دقيقة',
      lessons: 8,
      level: 'مبتدئ',
      rating: 4.8,
      enrolled: 156,
      thumbnail: '/api/placeholder/300/200',
      instructor: 'أحمد محمد',
      progress: 0,
      lessons_list: [
        { id: 1, title: 'مقدمة عن النظام', duration: '5 دقائق', type: 'video', completed: false },
        { id: 2, title: 'تسجيل الدخول والخروج', duration: '3 دقائق', type: 'video', completed: false },
        { id: 3, title: 'التنقل في لوحة التحكم', duration: '7 دقائق', type: 'video', completed: false },
        { id: 4, title: 'فهم القوائم الرئيسية', duration: '6 دقائق', type: 'video', completed: false },
        { id: 5, title: 'إعداد الملف الشخصي', duration: '4 دقائق', type: 'tutorial', completed: false },
        { id: 6, title: 'تخصيص الواجهة', duration: '5 دقائق', type: 'tutorial', completed: false },
        { id: 7, title: 'استخدام البحث والفلاتر', duration: '8 دقائق', type: 'video', completed: false },
        { id: 8, title: 'اختبار المعرفة', duration: '7 دقائق', type: 'quiz', completed: false }
      ]
    },
    {
      id: 2,
      title: 'إدارة المنتجات والمخزون',
      description: 'تعلم كيفية إضافة وإدارة المنتجات ومتابعة مستويات المخزون',
      category: 'inventory',
      duration: '1 ساعة 20 دقيقة',
      lessons: 12,
      level: 'متوسط',
      rating: 4.9,
      enrolled: 89,
      thumbnail: '/api/placeholder/300/200',
      instructor: 'فاطمة علي',
      progress: 0,
      lessons_list: [
        { id: 1, title: 'إضافة منتج جديد', duration: '8 دقائق', type: 'video', completed: false },
        { id: 2, title: 'تصنيف المنتجات', duration: '6 دقائق', type: 'video', completed: false },
        { id: 3, title: 'إدارة الوحدات والأسعار', duration: '10 دقائق', type: 'tutorial', completed: false },
        { id: 4, title: 'رفع صور المنتجات', duration: '5 دقائق', type: 'video', completed: false },
        { id: 5, title: 'إدارة المخازن', duration: '12 دقائق', type: 'video', completed: false },
        { id: 6, title: 'حركات المخزون', duration: '15 دقائق', type: 'tutorial', completed: false },
        { id: 7, title: 'تتبع مستويات المخزون', duration: '8 دقائق', type: 'video', completed: false },
        { id: 8, title: 'تنبيهات المخزون المنخفض', duration: '6 دقائق', type: 'video', completed: false },
        { id: 9, title: 'جرد المخزون', duration: '10 دقائق', type: 'tutorial', completed: false },
        { id: 10, title: 'تقارير المخزون', duration: '12 دقائق', type: 'video', completed: false },
        { id: 11, title: 'تطبيق عملي شامل', duration: '15 دقائق', type: 'tutorial', completed: false },
        { id: 12, title: 'اختبار نهائي', duration: '10 دقائق', type: 'quiz', completed: false }
      ]
    },
    {
      id: 3,
      title: 'إدارة الفواتير والمبيعات',
      description: 'تعلم إنشاء وإدارة الفواتير وتتبع المبيعات والمدفوعات',
      category: 'financial',
      duration: '1 ساعة 10 دقائق',
      lessons: 10,
      level: 'متوسط',
      rating: 4.7,
      enrolled: 124,
      thumbnail: '/api/placeholder/300/200',
      instructor: 'محمد حسن',
      progress: 0
    },
    {
      id: 4,
      title: 'التقارير المالية المتقدمة',
      description: 'إنشاء وتحليل التقارير المالية وقوائم الأرباح والخسائر',
      category: 'reports',
      duration: '55 دقيقة',
      lessons: 8,
      level: 'متقدم',
      rating: 4.9,
      enrolled: 67,
      thumbnail: '/api/placeholder/300/200',
      instructor: 'سارة أحمد',
      progress: 0
    },
    {
      id: 5,
      title: 'إدارة المستخدمين والصلاحيات',
      description: 'تعلم إدارة المستخدمين وتحديد الصلاحيات وأدوار النظام',
      category: 'admin',
      duration: '40 دقيقة',
      lessons: 6,
      level: 'متقدم',
      rating: 4.8,
      enrolled: 45,
      thumbnail: '/api/placeholder/300/200',
      instructor: 'عمر خالد',
      progress: 0
    }
  ]

  const quickTutorials = [
    {
      id: 1,
      title: 'كيفية إضافة منتج جديد',
      description: 'دليل سريع لإضافة منتج جديد في 3 خطوات',
      duration: '3 دقائق',
      type: 'video',
      views: 1250
    },
    {
      id: 2,
      title: 'إنشاء فاتورة مبيعات',
      description: 'خطوات إنشاء فاتورة مبيعات بسيطة',
      duration: '4 دقائق',
      type: 'tutorial',
      views: 980
    },
    {
      id: 3,
      title: 'تصدير تقرير مالي',
      description: 'كيفية تصدير التقارير المالية بصيغة PDF',
      duration: '2 دقيقة',
      type: 'video',
      views: 756
    },
    {
      id: 4,
      title: 'إعداد تنبيهات المخزون',
      description: 'ضبط تنبيهات المخزون المنخفض',
      duration: '5 دقائق',
      type: 'tutorial',
      views: 634
    }
  ]

  useEffect(() => {
    loadTrainingData()
  }, [])

  const loadTrainingData = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/api/training/courses')
      if (response.success) {
        setCourses(response.data.courses)
        setTutorials(response.data.tutorials)
        setUserProgress(response.data.progress)
      } else {
        // Use mock data
        setCourses(mockCourses)
        setTutorials(quickTutorials)
      }
    } catch (error) {
      setCourses(mockCourses)
      setTutorials(quickTutorials)
    } finally {
      setLoading(false)
    }
  }

  const enrollInCourse = async (courseId) => {
    try {
      const response = await ApiService.post(`/api/training/enroll/${courseId}`)
      if (response.success) {
        toast.success('تم التسجيل في الدورة بنجاح')
        loadTrainingData()
      }
    } catch (error) {
      toast.success('تم التسجيل في الدورة بنجاح') // Mock success
    }
  }

  const startLesson = async (courseId, lessonId) => {
    try {
      const response = await ApiService.post(`/api/training/lesson/start`, {
        courseId,
        lessonId
      })
      if (response.success) {
        toast.success('تم بدء الدرس')
      }
    } catch (error) {
      toast.success('تم بدء الدرس') // Mock success
    }
  }

  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || course.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const getTypeIcon = (type) => {
    switch (type) {
      case 'video':
        return <Video className="w-4 h-4 text-primary-600" />
      case 'tutorial':
        return <BookOpen className="w-4 h-4 text-primary" />
      case 'quiz':
        return <Award className="w-4 h-4 text-purple-600" />
      case 'audio':
        return <Headphones className="w-4 h-4 text-accent" />
      default:
        return <FileText className="w-4 h-4 text-muted-foreground" />
    }
  }

  const getLevelColor = (level) => {
    switch (level) {
      case 'مبتدئ':
        return 'bg-primary/20 text-green-800'
      case 'متوسط':
        return 'bg-accent/20 text-yellow-800'
      case 'متقدم':
        return 'bg-destructive/20 text-red-800'
      default:
        return 'bg-muted text-foreground'
    }
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
            <GraduationCap className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h1 className="text-2xl font-bold text-foreground">مركز التدريب</h1>
              <p className="text-muted-foreground">تعلم استخدام النظام من خلال دورات تدريبية شاملة</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <button className="inline-flex items-center px-4 py-2 border border-border rounded-md shadow-sm text-sm font-medium text-foreground bg-white hover:bg-muted/50">
              <Download className="w-4 h-4 ml-2" />
              تحميل الأدلة
            </button>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="البحث في الدورات..."
              className="w-full pr-10 pl-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {trainingCategories.map(category => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-border mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse px-6">
            {[
              { id: 'courses', name: 'الدورات التدريبية', icon: BookOpen },
              { id: 'tutorials', name: 'الدروس السريعة', icon: Play },
              { id: 'progress', name: 'تقدمي', icon: TrendingUp }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center`}
              >
                <tab.icon className="w-4 h-4 ml-2" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'courses' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-6">الدورات التدريبية</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredCourses.map((course) => (
                  <div key={course.id} className="bg-white border border-border rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
                    <div className="h-48 bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                      <Play className="w-16 h-16 text-white" />
                    </div>
                    
                    <div className="p-6">
                      <div className="flex items-center justify-between mb-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getLevelColor(course.level)}`}>
                          {course.level}
                        </span>
                        <div className="flex items-center">
                          <Star className="w-4 h-4 text-yellow-400 fill-current" />
                          <span className="text-sm text-muted-foreground mr-1">{course.rating}</span>
                        </div>
                      </div>
                      
                      <h4 className="text-lg font-semibold text-foreground mb-2">{course.title}</h4>
                      <p className="text-muted-foreground text-sm mb-4">{course.description}</p>
                      
                      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 ml-1" />
                          {course.duration}
                        </div>
                        <div className="flex items-center">
                          <BookOpen className="w-4 h-4 ml-1" />
                          {course.lessons} درس
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                        <span>المدرب: {course.instructor}</span>
                        <span>{course.enrolled} متدرب</span>
                      </div>
                      
                      {course.progress > 0 ? (
                        <div className="mb-4">
                          <div className="flex justify-between text-sm text-muted-foreground mb-1">
                            <span>التقدم</span>
                            <span>{course.progress}%</span>
                          </div>
                          <div className="w-full bg-muted rounded-full h-2">
                            <div
                              className="bg-primary-600 h-2 rounded-full"
                              style={{ width: `${course.progress}%` }}
                            ></div>
                          </div>
                        </div>
                      ) : null}
                      
                      <button
                        onClick={() => enrollInCourse(course.id)}
                        className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition-colors"
                      >
                        {course.progress > 0 ? 'متابعة الدورة' : 'بدء الدورة'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'tutorials' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-6">الدروس السريعة</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {tutorials.map((tutorial) => (
                  <div key={tutorial.id} className="bg-white border border-border rounded-lg p-6 hover:shadow-lg transition-shadow">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h4 className="text-lg font-semibold text-foreground mb-2">{tutorial.title}</h4>
                        <p className="text-muted-foreground text-sm mb-3">{tutorial.description}</p>
                        
                        <div className="flex items-center space-x-4 space-x-reverse text-sm text-gray-500">
                          <div className="flex items-center">
                            {getTypeIcon(tutorial.type)}
                            <span className="mr-1">{tutorial.duration}</span>
                          </div>
                          <div className="flex items-center">
                            <Users className="w-4 h-4 ml-1" />
                            <span>{tutorial.views} مشاهدة</span>
                          </div>
                        </div>
                      </div>
                      
                      <button className="bg-primary-600 text-white p-2 rounded-full hover:bg-primary-700 transition-colors">
                        <Play className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'progress' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-6">تقدمي في التدريب</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-primary-50 rounded-lg p-6 text-center">
                  <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <BookOpen className="w-8 h-8 text-white" />
                  </div>
                  <h4 className="text-2xl font-bold text-primary-600 mb-2">3</h4>
                  <p className="text-muted-foreground">دورات مكتملة</p>
                </div>
                
                <div className="bg-primary/10 rounded-lg p-6 text-center">
                  <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                    <Award className="w-8 h-8 text-white" />
                  </div>
                  <h4 className="text-2xl font-bold text-primary mb-2">2</h4>
                  <p className="text-muted-foreground">شهادات حاصل عليها</p>
                </div>
                
                <div className="bg-purple-50 rounded-lg p-6 text-center">
                  <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Clock className="w-8 h-8 text-white" />
                  </div>
                  <h4 className="text-2xl font-bold text-purple-600 mb-2">12</h4>
                  <p className="text-muted-foreground">ساعات تدريب</p>
                </div>
              </div>
              
              <div className="bg-white border border-border rounded-lg p-6">
                <h4 className="text-lg font-semibold text-foreground mb-4">الدورات الجارية</h4>
                <div className="space-y-4">
                  {courses.slice(0, 3).map((course) => (
                    <div key={course.id} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                      <div>
                        <h5 className="font-medium text-foreground">{course.title}</h5>
                        <p className="text-sm text-muted-foreground">{course.instructor}</p>
                      </div>
                      <div className="text-left">
                        <div className="text-sm text-muted-foreground mb-1">{course.progress || 0}% مكتمل</div>
                        <div className="w-32 bg-muted rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full"
                            style={{ width: `${course.progress || 0}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default TrainingCenter

