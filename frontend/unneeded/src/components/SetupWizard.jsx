import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { CheckCircle, Circle, Settings, Database, Users, Package } from 'lucide-react'

const SetupWizard = () => {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(1)
  const [setupData, setSetupData] = useState({
    company: {
      name: '',
      address: '',
      phone: '',
      email: ''
    },
    admin: {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    },
    database: {
      initialized: false
    },
    inventory: {
      defaultWarehouse: '',
      currency: 'EGP'
    }
  })

  const steps = [
    { id: 1, title: 'معلومات الشركة', icon: Settings },
    { id: 2, title: 'حساب المدير', icon: Users },
    { id: 3, title: 'إعداد قاعدة البيانات', icon: Database },
    { id: 4, title: 'إعدادات المخزون', icon: Package }
  ]

  const handleInputChange = (section, field, value) => {
    setSetupData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }))
  }

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleComplete = () => {
    // TODO: Send setup data to backend
    console.log('Setup completed:', setupData)
    navigate('/dashboard')
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-foreground mb-4">معلومات الشركة</h3>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                اسم الشركة
              </label>
              <input
                type="text"
                value={setupData.company.name}
                onChange={(e) => handleInputChange('company', 'name', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="أدخل اسم الشركة"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                العنوان
              </label>
              <input
                type="text"
                value={setupData.company.address}
                onChange={(e) => handleInputChange('company', 'address', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="أدخل عنوان الشركة"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                رقم الهاتف
              </label>
              <input
                type="tel"
                value={setupData.company.phone}
                onChange={(e) => handleInputChange('company', 'phone', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="أدخل رقم الهاتف"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                البريد الإلكتروني
              </label>
              <input
                type="email"
                value={setupData.company.email}
                onChange={(e) => handleInputChange('company', 'email', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="أدخل البريد الإلكتروني"
              />
            </div>
          </div>
        )

      case 2:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-foreground mb-4">حساب المدير الرئيسي</h3>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                اسم المستخدم
              </label>
              <input
                type="text"
                value={setupData.admin.username}
                onChange={(e) => handleInputChange('admin', 'username', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="أدخل اسم المستخدم"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                البريد الإلكتروني
              </label>
              <input
                type="email"
                value={setupData.admin.email}
                onChange={(e) => handleInputChange('admin', 'email', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="أدخل البريد الإلكتروني"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                كلمة المرور
              </label>
              <input
                type="password"
                value={setupData.admin.password}
                onChange={(e) => handleInputChange('admin', 'password', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="أدخل كلمة المرور"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                تأكيد كلمة المرور
              </label>
              <input
                type="password"
                value={setupData.admin.confirmPassword}
                onChange={(e) => handleInputChange('admin', 'confirmPassword', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="أعد إدخال كلمة المرور"
              />
            </div>
          </div>
        )

      case 3:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-foreground mb-4">إعداد قاعدة البيانات</h3>
            <div className="bg-muted p-6 rounded-lg text-center">
              <Database className="w-16 h-16 mx-auto mb-4 text-primary" />
              <p className="text-foreground mb-4">
                سيتم تهيئة قاعدة البيانات تلقائياً مع الجداول والبيانات الأساسية
              </p>
              <button
                onClick={() => handleInputChange('database', 'initialized', true)}
                className="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
              >
                {setupData.database.initialized ? 'تم التهيئة ✓' : 'تهيئة قاعدة البيانات'}
              </button>
            </div>
          </div>
        )

      case 4:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-foreground mb-4">إعدادات المخزون الأساسية</h3>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                اسم المخزن الافتراضي
              </label>
              <input
                type="text"
                value={setupData.inventory.defaultWarehouse}
                onChange={(e) => handleInputChange('inventory', 'defaultWarehouse', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="مثال: المخزن الرئيسي"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                العملة الافتراضية
              </label>
              <select
                value={setupData.inventory.currency}
                onChange={(e) => handleInputChange('inventory', 'currency', e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="EGP">جنيه مصري (EGP)</option>
                <option value="USD">دولار أمريكي (USD)</option>
                <option value="EUR">يورو (EUR)</option>
                <option value="EGP">ريال سعودي (EGP)</option>
              </select>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/10 to-secondary/20 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-foreground mb-2">معالج إعداد النظام</h1>
          <p className="text-muted-foreground">قم بإعداد نظام إدارة المخزون خطوة بخطوة</p>
        </div>

        {/* Progress Steps */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-8">
            {steps.map((step, index) => {
              const StepIcon = step.icon
              const isCompleted = currentStep > step.id
              const isCurrent = currentStep === step.id

              return (
                <React.Fragment key={step.id}>
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 ${
                        isCompleted
                          ? 'bg-primary text-white'
                          : isCurrent
                          ? 'bg-primary/20 text-primary border-2 border-primary'
                          : 'bg-gray-200 text-gray-400'
                      }`}
                    >
                      {isCompleted ? (
                        <CheckCircle className="w-6 h-6" />
                      ) : (
                        <StepIcon className="w-6 h-6" />
                      )}
                    </div>
                    <span
                      className={`text-sm font-medium ${
                        isCurrent ? 'text-primary' : 'text-muted-foreground'
                      }`}
                    >
                      {step.title}
                    </span>
                  </div>
                  {index < steps.length - 1 && (
                    <div
                      className={`flex-1 h-1 mx-4 ${
                        isCompleted ? 'bg-primary' : 'bg-gray-200'
                      }`}
                    />
                  )}
                </React.Fragment>
              )
            })}
          </div>

          {/* Step Content */}
          <div className="min-h-[400px]">{renderStepContent()}</div>

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8 pt-6 border-t border-border">
            <button
              onClick={handlePrevious}
              disabled={currentStep === 1}
              className="px-6 py-2 border border-border rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              السابق
            </button>
            <div className="flex gap-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="px-6 py-2 border border-border rounded-md hover:bg-gray-50"
              >
                تخطي
              </button>
              {currentStep < steps.length ? (
                <button
                  onClick={handleNext}
                  className="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
                >
                  التالي
                </button>
              ) : (
                <button
                  onClick={handleComplete}
                  className="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
                >
                  إنهاء الإعداد
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SetupWizard
