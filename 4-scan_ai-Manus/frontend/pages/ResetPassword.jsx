/**
 * Reset Password Page
 * ====================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Lock, Check, Loader, Leaf, AlertTriangle, Eye, EyeOff } from 'lucide-react';

import ApiService from '../services/ApiService';
import { Input } from '../src/components/Form';
import { Button } from '../components/UI/button';

const ResetPassword = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [validToken, setValidToken] = useState(true);

  // Validate token on mount
  useEffect(() => {
    if (!token) {
      setValidToken(false);
    }
  }, [token]);

  const validatePassword = (password) => {
    const requirements = {
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /[0-9]/.test(password),
      special: /[!@#$%^&*]/.test(password)
    };
    return requirements;
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.password) {
      setError(isRTL ? 'كلمة المرور مطلوبة' : 'Password is required');
      return;
    }

    const reqs = validatePassword(formData.password);
    if (!reqs.length || !reqs.uppercase || !reqs.lowercase || !reqs.number) {
      setError(isRTL ? 'كلمة المرور لا تستوفي المتطلبات' : 'Password does not meet requirements');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError(isRTL ? 'كلمات المرور غير متطابقة' : 'Passwords do not match');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await ApiService.resetPassword(token, formData.password);
      setSuccess(true);
      setTimeout(() => navigate('/login'), 3000);
    } catch (err) {
      setError(err.message || (isRTL ? 'حدث خطأ' : 'An error occurred'));
    } finally {
      setLoading(false);
    }
  };

  const passwordReqs = validatePassword(formData.password);

  // Invalid Token State
  if (!validToken) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
        <div className="w-full max-w-md">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
              <AlertTriangle className="w-8 h-8 text-red-500" />
            </div>
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
              {isRTL ? 'رابط غير صالح' : 'Invalid Link'}
            </h2>
            <p className="text-gray-500 mb-6">
              {isRTL 
                ? 'رابط إعادة تعيين كلمة المرور غير صالح أو منتهي الصلاحية'
                : 'This password reset link is invalid or has expired'
              }
            </p>
            <Link to="/forgot-password">
              <Button className="w-full">
                {isRTL ? 'طلب رابط جديد' : 'Request New Link'}
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 text-white mb-4">
            <Leaf className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Gaara Scan AI</h1>
        </div>

        {/* Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          {success ? (
            // Success State
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                <Check className="w-8 h-8 text-emerald-500" />
              </div>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
                {isRTL ? 'تم إعادة التعيين' : 'Password Reset'}
              </h2>
              <p className="text-gray-500 mb-6">
                {isRTL 
                  ? 'تم تغيير كلمة المرور بنجاح. جاري تحويلك...'
                  : 'Your password has been changed successfully. Redirecting...'
                }
              </p>
              <div className="flex justify-center">
                <Loader className="w-6 h-6 text-emerald-500 animate-spin" />
              </div>
            </div>
          ) : (
            // Form State
            <>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-2 text-center">
                {isRTL ? 'إعادة تعيين كلمة المرور' : 'Reset Password'}
              </h2>
              <p className="text-gray-500 text-center mb-6">
                {isRTL ? 'أدخل كلمة المرور الجديدة' : 'Enter your new password'}
              </p>

              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Password */}
                <div className="relative">
                  <Input
                    label={isRTL ? 'كلمة المرور الجديدة' : 'New Password'}
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={(v) => handleChange('password', v)}
                    icon={Lock}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 rtl:right-auto rtl:left-3 top-9 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>

                {/* Password Requirements */}
                <div className="p-3 bg-gray-50 dark:bg-gray-900 rounded-lg space-y-1">
                  <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">
                    {isRTL ? 'متطلبات كلمة المرور:' : 'Password requirements:'}
                  </p>
                  {[
                    { key: 'length', text: isRTL ? '8 أحرف على الأقل' : 'At least 8 characters' },
                    { key: 'uppercase', text: isRTL ? 'حرف كبير واحد' : 'One uppercase letter' },
                    { key: 'lowercase', text: isRTL ? 'حرف صغير واحد' : 'One lowercase letter' },
                    { key: 'number', text: isRTL ? 'رقم واحد' : 'One number' }
                  ].map(req => (
                    <div key={req.key} className={`flex items-center gap-2 text-xs ${passwordReqs[req.key] ? 'text-emerald-600' : 'text-gray-400'}`}>
                      <Check className={`w-3 h-3 ${passwordReqs[req.key] ? 'opacity-100' : 'opacity-30'}`} />
                      {req.text}
                    </div>
                  ))}
                </div>

                {/* Confirm Password */}
                <div className="relative">
                  <Input
                    label={isRTL ? 'تأكيد كلمة المرور' : 'Confirm Password'}
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={formData.confirmPassword}
                    onChange={(v) => handleChange('confirmPassword', v)}
                    icon={Lock}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 rtl:right-auto rtl:left-3 top-9 text-gray-400 hover:text-gray-600"
                  >
                    {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>

                {/* Error */}
                {error && (
                  <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg text-red-600 text-sm flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                    {error}
                  </div>
                )}

                <Button type="submit" className="w-full" loading={loading}>
                  {loading ? (
                    <>
                      <Loader className="w-4 h-4 mr-2 animate-spin" />
                      {isRTL ? 'جاري إعادة التعيين...' : 'Resetting...'}
                    </>
                  ) : (
                    <>
                      <Lock className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                      {isRTL ? 'إعادة تعيين كلمة المرور' : 'Reset Password'}
                    </>
                  )}
                </Button>
              </form>
            </>
          )}
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-6">
          {isRTL ? 'تذكرت كلمة المرور؟ ' : 'Remember your password? '}
          <Link to="/login" className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 font-medium">
            {isRTL ? 'تسجيل الدخول' : 'Sign in'}
          </Link>
        </p>
      </div>
    </div>
  );
};

export default ResetPassword;
