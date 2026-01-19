/**
 * Setup Wizard Page
 * =================
 * Initial setup for new users/organizations
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Leaf, Check, ChevronRight, ChevronLeft, Building, User, 
  MapPin, Settings, Loader, Upload, Globe, Bell, Shield
} from 'lucide-react';

import ApiService from '../services/ApiService';
import { Input, TextArea, Select, FileUpload } from '../src/components/Form';
import { Button } from '../components/UI/button';

const SetupWizard = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    // Organization
    companyName: '',
    companyType: 'farm',
    industry: 'agriculture',
    employeeCount: '',
    logo: null,
    
    // Location
    country: '',
    city: '',
    address: '',
    timezone: '',
    
    // Profile
    firstName: '',
    lastName: '',
    role: 'admin',
    phone: '',
    avatar: null,
    
    // Preferences
    language: 'en',
    notifications: true,
    emailAlerts: true,
    theme: 'light',
    measurementUnit: 'metric'
  });

  const steps = [
    { 
      id: 'organization', 
      title: isRTL ? 'المؤسسة' : 'Organization',
      icon: Building,
      description: isRTL ? 'معلومات المؤسسة الأساسية' : 'Basic organization details'
    },
    { 
      id: 'location', 
      title: isRTL ? 'الموقع' : 'Location',
      icon: MapPin,
      description: isRTL ? 'موقع المؤسسة' : 'Organization location'
    },
    { 
      id: 'profile', 
      title: isRTL ? 'الملف الشخصي' : 'Profile',
      icon: User,
      description: isRTL ? 'معلوماتك الشخصية' : 'Your personal information'
    },
    { 
      id: 'preferences', 
      title: isRTL ? 'التفضيلات' : 'Preferences',
      icon: Settings,
      description: isRTL ? 'إعدادات النظام' : 'System settings'
    }
  ];

  const handleChange = (field, value) => {
    setData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = async () => {
    setLoading(true);
    try {
      await ApiService.completeSetup(data);
      navigate('/dashboard');
    } catch (err) {
      console.error('Setup failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const companyTypes = [
    { value: 'farm', label: isRTL ? 'مزرعة' : 'Farm' },
    { value: 'cooperative', label: isRTL ? 'تعاونية' : 'Cooperative' },
    { value: 'research', label: isRTL ? 'مركز بحثي' : 'Research Center' },
    { value: 'company', label: isRTL ? 'شركة زراعية' : 'Agricultural Company' },
    { value: 'individual', label: isRTL ? 'مزارع فردي' : 'Individual Farmer' }
  ];

  const timezones = [
    { value: 'Africa/Cairo', label: 'Cairo (GMT+2)' },
    { value: 'Asia/Riyadh', label: 'Riyadh (GMT+3)' },
    { value: 'Asia/Dubai', label: 'Dubai (GMT+4)' },
    { value: 'Europe/London', label: 'London (GMT+0)' },
    { value: 'America/New_York', label: 'New York (GMT-5)' }
  ];

  const languages = [
    { value: 'en', label: 'English' },
    { value: 'ar', label: 'العربية' }
  ];

  const themes = [
    { value: 'light', label: isRTL ? 'فاتح' : 'Light' },
    { value: 'dark', label: isRTL ? 'داكن' : 'Dark' },
    { value: 'system', label: isRTL ? 'تلقائي' : 'System' }
  ];

  const renderStepContent = () => {
    switch (steps[currentStep].id) {
      case 'organization':
        return (
          <div className="space-y-4">
            <Input
              label={isRTL ? 'اسم المؤسسة' : 'Organization Name'}
              value={data.companyName}
              onChange={(v) => handleChange('companyName', v)}
              icon={Building}
              required
            />
            <Select
              label={isRTL ? 'نوع المؤسسة' : 'Organization Type'}
              value={data.companyType}
              onChange={(v) => handleChange('companyType', v)}
              options={companyTypes}
            />
            <Input
              label={isRTL ? 'عدد الموظفين' : 'Number of Employees'}
              type="number"
              value={data.employeeCount}
              onChange={(v) => handleChange('employeeCount', v)}
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {isRTL ? 'شعار المؤسسة' : 'Organization Logo'}
              </label>
              <FileUpload
                accept="image/*"
                onChange={(f) => handleChange('logo', f)}
                preview={data.logo}
              />
            </div>
          </div>
        );

      case 'location':
        return (
          <div className="space-y-4">
            <Input
              label={isRTL ? 'الدولة' : 'Country'}
              value={data.country}
              onChange={(v) => handleChange('country', v)}
              icon={Globe}
            />
            <Input
              label={isRTL ? 'المدينة' : 'City'}
              value={data.city}
              onChange={(v) => handleChange('city', v)}
              icon={MapPin}
            />
            <TextArea
              label={isRTL ? 'العنوان' : 'Address'}
              value={data.address}
              onChange={(v) => handleChange('address', v)}
              rows={3}
            />
            <Select
              label={isRTL ? 'المنطقة الزمنية' : 'Timezone'}
              value={data.timezone}
              onChange={(v) => handleChange('timezone', v)}
              options={timezones}
            />
          </div>
        );

      case 'profile':
        return (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input
                label={isRTL ? 'الاسم الأول' : 'First Name'}
                value={data.firstName}
                onChange={(v) => handleChange('firstName', v)}
                required
              />
              <Input
                label={isRTL ? 'الاسم الأخير' : 'Last Name'}
                value={data.lastName}
                onChange={(v) => handleChange('lastName', v)}
                required
              />
            </div>
            <Input
              label={isRTL ? 'رقم الهاتف' : 'Phone Number'}
              type="tel"
              value={data.phone}
              onChange={(v) => handleChange('phone', v)}
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {isRTL ? 'الصورة الشخصية' : 'Profile Picture'}
              </label>
              <FileUpload
                accept="image/*"
                onChange={(f) => handleChange('avatar', f)}
                preview={data.avatar}
              />
            </div>
          </div>
        );

      case 'preferences':
        return (
          <div className="space-y-4">
            <Select
              label={isRTL ? 'اللغة' : 'Language'}
              value={data.language}
              onChange={(v) => handleChange('language', v)}
              options={languages}
              icon={Globe}
            />
            <Select
              label={isRTL ? 'المظهر' : 'Theme'}
              value={data.theme}
              onChange={(v) => handleChange('theme', v)}
              options={themes}
            />
            <Select
              label={isRTL ? 'وحدة القياس' : 'Measurement Unit'}
              value={data.measurementUnit}
              onChange={(v) => handleChange('measurementUnit', v)}
              options={[
                { value: 'metric', label: isRTL ? 'متري' : 'Metric' },
                { value: 'imperial', label: isRTL ? 'إمبراطوري' : 'Imperial' }
              ]}
            />
            
            {/* Notifications */}
            <div className="pt-4 space-y-3">
              <h4 className="font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
                <Bell className="w-4 h-4" />
                {isRTL ? 'الإشعارات' : 'Notifications'}
              </h4>
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={data.notifications}
                  onChange={(e) => handleChange('notifications', e.target.checked)}
                  className="w-4 h-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {isRTL ? 'تفعيل إشعارات التطبيق' : 'Enable push notifications'}
                </span>
              </label>
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={data.emailAlerts}
                  onChange={(e) => handleChange('emailAlerts', e.target.checked)}
                  className="w-4 h-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {isRTL ? 'تفعيل تنبيهات البريد' : 'Enable email alerts'}
                </span>
              </label>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 text-white mb-4">
            <Leaf className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">
            {isRTL ? 'مرحباً بك في Gaara Scan AI' : 'Welcome to Gaara Scan AI'}
          </h1>
          <p className="text-gray-500 mt-2">
            {isRTL ? 'دعنا نعد حسابك في بضع خطوات بسيطة' : "Let's set up your account in a few simple steps"}
          </p>
        </div>

        {/* Progress Steps */}
        <div className="flex justify-between mb-8">
          {steps.map((step, index) => (
            <div key={step.id} className="flex-1 flex items-center">
              <div className="flex flex-col items-center flex-1">
                <div className={`
                  w-10 h-10 rounded-full flex items-center justify-center
                  ${index < currentStep 
                    ? 'bg-emerald-500 text-white' 
                    : index === currentStep 
                      ? 'bg-emerald-500 text-white ring-4 ring-emerald-200 dark:ring-emerald-900' 
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-500'
                  }
                `}>
                  {index < currentStep ? (
                    <Check className="w-5 h-5" />
                  ) : (
                    <step.icon className="w-5 h-5" />
                  )}
                </div>
                <span className={`mt-2 text-xs font-medium ${
                  index <= currentStep ? 'text-emerald-600' : 'text-gray-400'
                }`}>
                  {step.title}
                </span>
              </div>
              {index < steps.length - 1 && (
                <div className={`h-0.5 flex-1 mx-2 ${
                  index < currentStep ? 'bg-emerald-500' : 'bg-gray-200 dark:bg-gray-700'
                }`} />
              )}
            </div>
          ))}
        </div>

        {/* Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          {/* Step Header */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white">
              {steps[currentStep].title}
            </h2>
            <p className="text-gray-500 text-sm mt-1">
              {steps[currentStep].description}
            </p>
          </div>

          {/* Step Content */}
          {renderStepContent()}

          {/* Navigation */}
          <div className="flex justify-between mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
            <Button
              variant="outline"
              onClick={handlePrev}
              disabled={currentStep === 0}
              className={currentStep === 0 ? 'invisible' : ''}
            >
              {isRTL ? (
                <>
                  <ChevronRight className="w-4 h-4 mr-2" />
                  {isRTL ? 'السابق' : 'Previous'}
                </>
              ) : (
                <>
                  <ChevronLeft className="w-4 h-4 mr-2" />
                  Previous
                </>
              )}
            </Button>

            {currentStep < steps.length - 1 ? (
              <Button onClick={handleNext}>
                {isRTL ? 'التالي' : 'Next'}
                {isRTL ? (
                  <ChevronLeft className="w-4 h-4 ml-2" />
                ) : (
                  <ChevronRight className="w-4 h-4 ml-2" />
                )}
              </Button>
            ) : (
              <Button onClick={handleComplete} loading={loading}>
                {loading ? (
                  <>
                    <Loader className="w-4 h-4 mr-2 animate-spin" />
                    {isRTL ? 'جاري الإعداد...' : 'Setting up...'}
                  </>
                ) : (
                  <>
                    <Check className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                    {isRTL ? 'إكمال الإعداد' : 'Complete Setup'}
                  </>
                )}
              </Button>
            )}
          </div>
        </div>

        {/* Skip */}
        <p className="text-center text-sm text-gray-500 mt-6">
          <button 
            onClick={() => navigate('/dashboard')} 
            className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400"
          >
            {isRTL ? 'تخطي الإعداد' : 'Skip setup for now'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default SetupWizard;
