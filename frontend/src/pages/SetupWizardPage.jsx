/**
 * Setup Wizard Page
 * 
 * Initial system configuration wizard for new installations.
 */

import React, { useState } from 'react';
import {
  Building2, User, Settings, CheckCircle, ChevronLeft, ChevronRight,
  Globe, Mail, Phone, MapPin, CreditCard, Shield, Database, Sparkles,
  Upload, Eye, EyeOff
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const steps = [
  { id: 1, title: 'مرحباً', icon: Sparkles },
  { id: 2, title: 'بيانات الشركة', icon: Building2 },
  { id: 3, title: 'حساب المدير', icon: User },
  { id: 4, title: 'الإعدادات', icon: Settings },
  { id: 5, title: 'اكتمل', icon: CheckCircle },
];

const SetupWizardPage = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const [companyData, setCompanyData] = useState({
    name: '',
    nameAr: '',
    email: '',
    phone: '',
    address: '',
    taxNumber: '',
    commercialRegister: '',
    logo: null
  });

  const [adminData, setAdminData] = useState({
    name: '',
    username: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });

  const [settingsData, setSettingsData] = useState({
    currency: 'SAR',
    timezone: 'Asia/Riyadh',
    language: 'ar',
    fiscalYearStart: '1'
  });

  const handleNext = () => {
    if (currentStep < 5) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = async () => {
    setIsLoading(true);
    // In production, make API calls here
    await new Promise(resolve => setTimeout(resolve, 2000));
    setCurrentStep(5);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-teal-900 to-slate-900 flex" dir="rtl">
      {/* Sidebar */}
      <div className="w-80 bg-black/20 backdrop-blur p-8 flex flex-col">
        <div className="mb-12">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-teal-400 to-teal-600 flex items-center justify-center mb-4">
            <Database className="text-white" size={24} />
          </div>
          <h1 className="text-2xl font-bold text-white">Store Pro</h1>
          <p className="text-teal-200/70">معالج الإعداد الأولي</p>
        </div>

        <nav className="flex-1">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = step.id === currentStep;
            const isCompleted = step.id < currentStep;
            
            return (
              <div key={step.id} className="flex items-center gap-4 mb-6">
                <div className={`
                  w-10 h-10 rounded-xl flex items-center justify-center transition-all
                  ${isCompleted ? 'bg-teal-500 text-white' : 
                    isActive ? 'bg-white text-teal-900' : 'bg-white/10 text-white/50'}
                `}>
                  {isCompleted ? <CheckCircle size={20} /> : <Icon size={20} />}
                </div>
                <span className={`font-medium ${isActive ? 'text-white' : 'text-white/50'}`}>
                  {step.title}
                </span>
                {index < steps.length - 1 && (
                  <div className={`absolute right-[2.1rem] mt-16 w-0.5 h-6 ${isCompleted ? 'bg-teal-500' : 'bg-white/10'}`} />
                )}
              </div>
            );
          })}
        </nav>

        <div className="text-white/40 text-sm">
          الخطوة {currentStep} من {steps.length}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="bg-white rounded-3xl shadow-2xl w-full max-w-2xl overflow-hidden">
          {/* Step 1: Welcome */}
          {currentStep === 1 && (
            <div className="p-12 text-center">
              <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-teal-400 to-teal-600 flex items-center justify-center mx-auto mb-8">
                <Sparkles className="text-white" size={48} />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">مرحباً بك في Store Pro</h2>
              <p className="text-gray-500 text-lg mb-8 max-w-md mx-auto">
                سنقوم بمساعدتك في إعداد نظامك خطوة بخطوة. لن يستغرق الأمر سوى بضع دقائق.
              </p>
              <Button variant="primary" size="lg" onClick={handleNext}>
                ابدأ الآن
                <ChevronLeft size={20} />
              </Button>
            </div>
          )}

          {/* Step 2: Company Info */}
          {currentStep === 2 && (
            <div className="p-8">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
                  <Building2 className="text-teal-600" size={24} />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">بيانات الشركة</h2>
                  <p className="text-gray-500">أدخل معلومات شركتك الأساسية</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">اسم الشركة (عربي)</label>
                    <input
                      type="text"
                      value={companyData.nameAr}
                      onChange={(e) => setCompanyData({...companyData, nameAr: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="شركة التقنية للتجارة"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">اسم الشركة (English)</label>
                    <input
                      type="text"
                      value={companyData.name}
                      onChange={(e) => setCompanyData({...companyData, name: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="Tech Trading Co."
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Mail size={14} className="inline ml-1" /> البريد الإلكتروني
                    </label>
                    <input
                      type="email"
                      value={companyData.email}
                      onChange={(e) => setCompanyData({...companyData, email: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="info@company.com"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Phone size={14} className="inline ml-1" /> الهاتف
                    </label>
                    <input
                      type="tel"
                      value={companyData.phone}
                      onChange={(e) => setCompanyData({...companyData, phone: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="+966 5x xxx xxxx"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <MapPin size={14} className="inline ml-1" /> العنوان
                  </label>
                  <textarea
                    value={companyData.address}
                    onChange={(e) => setCompanyData({...companyData, address: e.target.value})}
                    rows={2}
                    className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                    placeholder="الرياض، حي العليا..."
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">الرقم الضريبي</label>
                    <input
                      type="text"
                      value={companyData.taxNumber}
                      onChange={(e) => setCompanyData({...companyData, taxNumber: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="300000000000000"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">السجل التجاري</label>
                    <input
                      type="text"
                      value={companyData.commercialRegister}
                      onChange={(e) => setCompanyData({...companyData, commercialRegister: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="1234567890"
                    />
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between mt-8 pt-6 border-t border-gray-100">
                <Button variant="ghost" onClick={handlePrev}>
                  <ChevronRight size={20} /> السابق
                </Button>
                <Button variant="primary" onClick={handleNext}>
                  التالي <ChevronLeft size={20} />
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Admin Account */}
          {currentStep === 3 && (
            <div className="p-8">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
                  <Shield className="text-purple-600" size={24} />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">حساب المدير</h2>
                  <p className="text-gray-500">إنشاء حساب مدير النظام</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">الاسم الكامل</label>
                    <input
                      type="text"
                      value={adminData.name}
                      onChange={(e) => setAdminData({...adminData, name: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="أحمد محمد"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">اسم المستخدم</label>
                    <input
                      type="text"
                      value={adminData.username}
                      onChange={(e) => setAdminData({...adminData, username: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="admin"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">البريد الإلكتروني</label>
                    <input
                      type="email"
                      value={adminData.email}
                      onChange={(e) => setAdminData({...adminData, email: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="admin@company.com"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">رقم الهاتف</label>
                    <input
                      type="tel"
                      value={adminData.phone}
                      onChange={(e) => setAdminData({...adminData, phone: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="+966 5x xxx xxxx"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">كلمة المرور</label>
                    <div className="relative">
                      <input
                        type={showPassword ? 'text' : 'password'}
                        value={adminData.password}
                        onChange={(e) => setAdminData({...adminData, password: e.target.value})}
                        className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                        placeholder="••••••••"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      >
                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">تأكيد كلمة المرور</label>
                    <input
                      type="password"
                      value={adminData.confirmPassword}
                      onChange={(e) => setAdminData({...adminData, confirmPassword: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                      placeholder="••••••••"
                    />
                  </div>
                </div>

                <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mt-4">
                  <p className="text-amber-800 text-sm">
                    <strong>ملاحظة:</strong> هذا الحساب سيكون له صلاحيات كاملة على النظام. تأكد من استخدام كلمة مرور قوية.
                  </p>
                </div>
              </div>

              <div className="flex items-center justify-between mt-8 pt-6 border-t border-gray-100">
                <Button variant="ghost" onClick={handlePrev}>
                  <ChevronRight size={20} /> السابق
                </Button>
                <Button variant="primary" onClick={handleNext}>
                  التالي <ChevronLeft size={20} />
                </Button>
              </div>
            </div>
          )}

          {/* Step 4: Settings */}
          {currentStep === 4 && (
            <div className="p-8">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
                  <Settings className="text-blue-600" size={24} />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">الإعدادات</h2>
                  <p className="text-gray-500">تخصيص إعدادات النظام الأساسية</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <CreditCard size={14} className="inline ml-1" /> العملة الافتراضية
                    </label>
                    <select
                      value={settingsData.currency}
                      onChange={(e) => setSettingsData({...settingsData, currency: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                    >
                      <option value="SAR">ريال سعودي (SAR)</option>
                      <option value="AED">درهم إماراتي (AED)</option>
                      <option value="USD">دولار أمريكي (USD)</option>
                      <option value="EUR">يورو (EUR)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Globe size={14} className="inline ml-1" /> المنطقة الزمنية
                    </label>
                    <select
                      value={settingsData.timezone}
                      onChange={(e) => setSettingsData({...settingsData, timezone: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                    >
                      <option value="Asia/Riyadh">الرياض (GMT+3)</option>
                      <option value="Asia/Dubai">دبي (GMT+4)</option>
                      <option value="Asia/Kuwait">الكويت (GMT+3)</option>
                      <option value="Africa/Cairo">القاهرة (GMT+2)</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">اللغة الافتراضية</label>
                    <select
                      value={settingsData.language}
                      onChange={(e) => setSettingsData({...settingsData, language: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                    >
                      <option value="ar">العربية</option>
                      <option value="en">English</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">بداية السنة المالية</label>
                    <select
                      value={settingsData.fiscalYearStart}
                      onChange={(e) => setSettingsData({...settingsData, fiscalYearStart: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
                    >
                      <option value="1">يناير</option>
                      <option value="4">أبريل</option>
                      <option value="7">يوليو</option>
                      <option value="10">أكتوبر</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between mt-8 pt-6 border-t border-gray-100">
                <Button variant="ghost" onClick={handlePrev}>
                  <ChevronRight size={20} /> السابق
                </Button>
                <Button variant="primary" onClick={handleComplete} isLoading={isLoading}>
                  إكمال الإعداد <CheckCircle size={20} />
                </Button>
              </div>
            </div>
          )}

          {/* Step 5: Complete */}
          {currentStep === 5 && (
            <div className="p-12 text-center">
              <div className="w-24 h-24 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-8">
                <CheckCircle className="text-emerald-600" size={48} />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">تم الإعداد بنجاح!</h2>
              <p className="text-gray-500 text-lg mb-8 max-w-md mx-auto">
                تم إعداد نظامك بنجاح. يمكنك الآن تسجيل الدخول والبدء في استخدام Store Pro.
              </p>
              <Button variant="primary" size="lg" onClick={() => window.location.href = '/login'}>
                الذهاب إلى تسجيل الدخول
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SetupWizardPage;

