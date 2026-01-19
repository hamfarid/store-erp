/**
 * Login Page - Modern Authentication UI
 * @file pages/Login.jsx
 */

import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import {
  Leaf,
  Lock,
  Mail,
  Eye,
  EyeOff,
  ArrowRight,
  Loader2,
  Scan,
  Shield,
  Sparkles
} from 'lucide-react';

// UI Components
import { Button } from '../components/UI/button';
import { Input, FormField } from '../components/UI/input';
import { cn } from '../lib/utils';

// Services
import ApiService from '../services/ApiService';

// ============================================
// Feature Item Component
// ============================================
const FeatureItem = ({ icon: Icon, title, description }) => (
  <div className="flex items-start gap-3 text-white/90">
    <div className="w-10 h-10 rounded-lg bg-white/10 backdrop-blur-sm flex items-center justify-center flex-shrink-0">
      <Icon className="h-5 w-5" />
    </div>
    <div>
      <h4 className="font-medium">{title}</h4>
      <p className="text-sm text-white/70">{description}</p>
    </div>
  </div>
);

// ============================================
// Main Login Page
// ============================================
const Login = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    remember: false,
  });
  const [errors, setErrors] = useState({});

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user types
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.email) {
      newErrors.email = 'البريد الإلكتروني مطلوب';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'البريد الإلكتروني غير صالح';
    }
    if (!formData.password) {
      newErrors.password = 'كلمة المرور مطلوبة';
    } else if (formData.password.length < 6) {
      newErrors.password = 'كلمة المرور يجب أن تكون 6 أحرف على الأقل';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      // Call actual backend API
      const response = await ApiService.login({
        username: formData.email,
        password: formData.password
      });
      
      // Store auth data
      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify({ 
        email: formData.email, 
        name: formData.email.split('@')[0] 
      }));
      
      toast.success('تم تسجيل الدخول بنجاح');
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      const errorMessage = error.response?.data?.detail || 'فشل في تسجيل الدخول. تحقق من بياناتك.';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-emerald-600 via-emerald-500 to-teal-500 p-12 flex-col justify-between relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-teal-400/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
        
        {/* Logo */}
        <div className="relative z-10">
          <div className="flex items-center gap-3 text-white">
            <div className="w-14 h-14 rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
              <Scan className="h-8 w-8" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Gaara Scan</h1>
              <p className="text-white/80 text-sm">الزراعة الذكية</p>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="relative z-10 space-y-6">
          <h2 className="text-3xl font-bold text-white mb-8">
            نظام تشخيص أمراض النباتات<br />
            بالذكاء الاصطناعي
          </h2>
          
          <div className="space-y-6">
            <FeatureItem
              icon={Sparkles}
              title="تشخيص فوري"
              description="تحليل صور النباتات والتشخيص خلال ثوانٍ"
            />
            <FeatureItem
              icon={Leaf}
              title="قاعدة بيانات شاملة"
              description="أكثر من 50 مرض وآفة زراعية مغطاة"
            />
            <FeatureItem
              icon={Shield}
              title="دقة عالية"
              description="نسبة دقة تصل إلى 95% في التشخيص"
            />
          </div>
        </div>

        {/* Footer */}
        <div className="relative z-10 text-white/60 text-sm">
          © 2024 Gaara Scan AI. جميع الحقوق محفوظة.
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gray-50 dark:bg-gray-900">
        <div className="w-full max-w-md">
          {/* Mobile Logo */}
          <div className="lg:hidden flex items-center justify-center gap-3 mb-8">
            <div className="w-12 h-12 rounded-xl bg-emerald-500 flex items-center justify-center text-white">
              <Scan className="h-6 w-6" />
            </div>
            <span className="text-2xl font-bold text-gray-900 dark:text-gray-100">Gaara Scan</span>
          </div>

          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">مرحباً بعودتك</h2>
            <p className="text-gray-500 dark:text-gray-400 mt-2">سجل دخولك للمتابعة</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <FormField label="البريد الإلكتروني" error={errors.email}>
              <Input
                type="email"
                value={formData.email}
                onChange={(e) => handleChange('email', e.target.value)}
                placeholder="example@email.com"
                leftIcon={Mail}
                error={errors.email}
                disabled={loading}
              />
            </FormField>

            <FormField label="كلمة المرور" error={errors.password}>
              <div className="relative">
                <Input
                  type={showPassword ? "text" : "password"}
                  value={formData.password}
                  onChange={(e) => handleChange('password', e.target.value)}
                  placeholder="أدخل كلمة المرور"
                  leftIcon={Lock}
                  error={errors.password}
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </FormField>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.remember}
                  onChange={(e) => handleChange('remember', e.target.checked)}
                  className="w-4 h-4 rounded border-gray-300 text-emerald-500 focus:ring-emerald-500"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">تذكرني</span>
              </label>
              <Link 
                to="/forgot-password" 
                className="text-sm text-emerald-600 hover:text-emerald-700 dark:text-emerald-400"
              >
                نسيت كلمة المرور؟
              </Link>
            </div>

            <Button
              type="submit"
              className="w-full"
              size="lg"
              loading={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  جاري تسجيل الدخول...
                </>
              ) : (
                <>
                  تسجيل الدخول
                  <ArrowRight className="h-5 w-5" />
                </>
              )}
            </Button>
          </form>

          <div className="mt-8">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200 dark:border-gray-700" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-gray-50 dark:bg-gray-900 text-gray-500">أو</span>
              </div>
            </div>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                ليس لديك حساب؟{' '}
                <Link 
                  to="/register" 
                  className="font-medium text-emerald-600 hover:text-emerald-700 dark:text-emerald-400"
                >
                  إنشاء حساب جديد
                </Link>
              </p>
            </div>
          </div>

          {/* Demo credentials */}
          <div className="mt-8 p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl">
            <p className="text-sm text-amber-800 dark:text-amber-200 font-medium mb-2">بيانات تجريبية:</p>
            <p className="text-sm text-amber-700 dark:text-amber-300">
              البريد: <code className="bg-amber-100 dark:bg-amber-900/50 px-1 rounded">admin</code>
            </p>
            <p className="text-sm text-amber-700 dark:text-amber-300">
              كلمة المرور: <code className="bg-amber-100 dark:bg-amber-900/50 px-1 rounded">admin123</code>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
