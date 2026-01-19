/**
 * Register Page - Modern Registration UI
 * @file pages/Register.jsx
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import {
  UserPlus,
  Mail,
  Phone,
  Lock,
  Eye,
  EyeOff,
  CheckCircle,
  XCircle,
  ArrowRight,
  Scan,
  Sparkles,
  Shield,
  Leaf
} from 'lucide-react';

// UI Components
import { Button } from '../components/UI/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/UI/card';
import { Input, FormField } from '../components/UI/input';
import { Badge } from '../components/UI/badge';
import { cn } from '../lib/utils';

// Services
import ApiService from '../services/ApiService';

// ============================================
// Password Strength Indicator
// ============================================
const PasswordStrengthIndicator = ({ password }) => {
  const calculateStrength = (pwd) => {
    let strength = 0;
    if (pwd.length >= 8) strength += 20;
    if (pwd.length >= 12) strength += 20;
    if (/[A-Z]/.test(pwd)) strength += 20;
    if (/[a-z]/.test(pwd)) strength += 10;
    if (/[0-9]/.test(pwd)) strength += 15;
    if (/[^A-Za-z0-9]/.test(pwd)) strength += 15;
    return Math.min(strength, 100);
  };

  const strength = calculateStrength(password);
  const getStrengthInfo = () => {
    if (strength < 40) return { label: 'ضعيفة', color: 'red', variant: 'destructive' };
    if (strength < 70) return { label: 'متوسطة', color: 'amber', variant: 'warning' };
    return { label: 'قوية', color: 'emerald', variant: 'success' };
  };

  const info = getStrengthInfo();

  if (!password) return null;

  return (
    <div className="mt-2 space-y-2">
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-500">قوة كلمة المرور:</span>
        <Badge variant={info.variant}>{info.label}</Badge>
      </div>
      <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div
          className={cn(
            "h-full rounded-full transition-all duration-300",
            info.color === 'red' ? 'bg-red-500' :
            info.color === 'amber' ? 'bg-amber-500' : 'bg-emerald-500'
          )}
          style={{ width: `${strength}%` }}
        />
      </div>
      <p className="text-xs text-gray-500">
        12 حرفاً على الأقل، تتضمن حروف كبيرة وصغيرة وأرقام ورموز
      </p>
    </div>
  );
};

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
// Main Register Page
// ============================================
const Register = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    agreeToTerms: false,
  });
  const [errors, setErrors] = useState({});

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'الاسم مطلوب';
    }
    if (!formData.email.trim()) {
      newErrors.email = 'البريد الإلكتروني مطلوب';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'البريد الإلكتروني غير صالح';
    }
    if (formData.password.length < 12) {
      newErrors.password = 'كلمة المرور يجب أن تكون 12 حرفاً على الأقل';
    }
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'كلمتا المرور غير متطابقتين';
    }
    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'يجب الموافقة على الشروط والأحكام';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast.error('يرجى تصحيح الأخطاء في النموذج');
      return;
    }

    setLoading(true);
    try {
      const response = await ApiService.post('/api/v1/auth/register', {
        name: formData.name,
        email: formData.email,
        phone: formData.phone || null,
        password: formData.password
      });
      
      if (response.data?.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        
        toast.success('تم إنشاء الحساب بنجاح!');
        navigate('/dashboard');
      }
    } catch (err) {
      const errorDetail = err.response?.data?.detail;
      const errorMessage = typeof errorDetail === 'object' 
        ? errorDetail.message || 'حدث خطأ في إنشاء الحساب'
        : errorDetail || 'حدث خطأ في إنشاء الحساب';
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
            انضم إلى مجتمع<br />
            المزارعين الذكيين
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

      {/* Right Side - Register Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gray-50 dark:bg-gray-900">
        <div className="w-full max-w-md">
          {/* Mobile Logo */}
          <div className="lg:hidden flex items-center justify-center gap-3 mb-8">
            <div className="w-12 h-12 rounded-xl bg-emerald-500 flex items-center justify-center text-white">
              <Scan className="h-6 w-6" />
            </div>
            <span className="text-2xl font-bold text-gray-900 dark:text-gray-100">Gaara Scan</span>
          </div>

          <Card className="shadow-xl">
            <CardHeader className="text-center">
              <div className="w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center mx-auto mb-4">
                <UserPlus className="h-8 w-8 text-emerald-600 dark:text-emerald-400" />
              </div>
              <CardTitle className="text-2xl">إنشاء حساب جديد</CardTitle>
              <CardDescription>انضم إلى Gaara Scan AI وابدأ رحلتك</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <FormField label="الاسم الكامل" required error={errors.name}>
                  <Input
                    type="text"
                    value={formData.name}
                    onChange={(e) => handleChange('name', e.target.value)}
                    placeholder="أدخل اسمك الكامل"
                    leftIcon={UserPlus}
                    error={errors.name}
                    disabled={loading}
                  />
                </FormField>

                <FormField label="البريد الإلكتروني" required error={errors.email}>
                  <Input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    placeholder="example@email.com"
                    leftIcon={Mail}
                    error={errors.email}
                    disabled={loading}
                    dir="ltr"
                  />
                </FormField>

                <FormField label="رقم الهاتف (اختياري)">
                  <Input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => handleChange('phone', e.target.value)}
                    placeholder="+966 5XX XXX XXXX"
                    leftIcon={Phone}
                    disabled={loading}
                    dir="ltr"
                  />
                </FormField>

                <FormField label="كلمة المرور" required error={errors.password}>
                  <div className="relative">
                    <Input
                      type={showPassword ? "text" : "password"}
                      value={formData.password}
                      onChange={(e) => handleChange('password', e.target.value)}
                      placeholder="••••••••••••"
                      leftIcon={Lock}
                      error={errors.password}
                      disabled={loading}
                      minLength={12}
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
                  <PasswordStrengthIndicator password={formData.password} />
                </FormField>

                <FormField label="تأكيد كلمة المرور" required error={errors.confirmPassword}>
                  <div className="relative">
                    <Input
                      type={showConfirmPassword ? "text" : "password"}
                      value={formData.confirmPassword}
                      onChange={(e) => handleChange('confirmPassword', e.target.value)}
                      placeholder="••••••••••••"
                      leftIcon={Lock}
                      error={errors.confirmPassword}
                      disabled={loading}
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      tabIndex={-1}
                    >
                      {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                    </button>
                  </div>
                </FormField>

                <div className="flex items-start gap-2">
                  <input
                    type="checkbox"
                    id="terms"
                    checked={formData.agreeToTerms}
                    onChange={(e) => handleChange('agreeToTerms', e.target.checked)}
                    className="mt-1 h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
                    disabled={loading}
                  />
                  <label htmlFor="terms" className="text-sm text-gray-600 dark:text-gray-400">
                    أوافق على{' '}
                    <a href="/terms" className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400">
                      شروط الاستخدام
                    </a>
                    {' '}و{' '}
                    <a href="/privacy" className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400">
                      سياسة الخصوصية
                    </a>
                    {errors.agreeToTerms && (
                      <span className="block text-red-500 text-xs mt-1">{errors.agreeToTerms}</span>
                    )}
                  </label>
                </div>

                <Button
                  type="submit"
                  className="w-full"
                  size="lg"
                  loading={loading}
                >
                  {loading ? (
                    'جاري إنشاء الحساب...'
                  ) : (
                    <>
                      إنشاء حساب
                      <ArrowRight className="h-5 w-5" />
                    </>
                  )}
                </Button>
              </form>

              <div className="mt-6 text-center">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  لديك حساب بالفعل؟{' '}
                  <Link 
                    to="/login" 
                    className="font-medium text-emerald-600 hover:text-emerald-700 dark:text-emerald-400"
                  >
                    تسجيل الدخول
                  </Link>
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Register;
