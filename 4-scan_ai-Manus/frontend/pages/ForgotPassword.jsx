/**
 * Forgot Password Page
 * ====================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, ArrowLeft, Check, Loader, Leaf } from 'lucide-react';

import ApiService from '../services/ApiService';
import { Input } from '../src/components/Form';
import { Button } from '../components/UI/button';

const ForgotPassword = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      setError(isRTL ? 'البريد الإلكتروني مطلوب' : 'Email is required');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await ApiService.forgotPassword(email);
      setSent(true);
    } catch (err) {
      setError(err.message || (isRTL ? 'حدث خطأ' : 'An error occurred'));
    } finally {
      setLoading(false);
    }
  };

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
          {sent ? (
            // Success State
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                <Check className="w-8 h-8 text-emerald-500" />
              </div>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
                {isRTL ? 'تم إرسال الرابط' : 'Reset Link Sent'}
              </h2>
              <p className="text-gray-500 mb-6">
                {isRTL 
                  ? `تم إرسال رابط إعادة تعيين كلمة المرور إلى ${email}`
                  : `A password reset link has been sent to ${email}`
                }
              </p>
              <p className="text-sm text-gray-400 mb-6">
                {isRTL 
                  ? 'تحقق من مجلد الرسائل غير المرغوب فيها إذا لم تجد الرسالة'
                  : 'Check your spam folder if you don\'t see the email'
                }
              </p>
              <Link to="/login">
                <Button variant="outline" className="w-full">
                  <ArrowLeft className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2 rtl:rotate-180" />
                  {isRTL ? 'العودة لتسجيل الدخول' : 'Back to Login'}
                </Button>
              </Link>
            </div>
          ) : (
            // Form State
            <>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-2 text-center">
                {isRTL ? 'نسيت كلمة المرور؟' : 'Forgot Password?'}
              </h2>
              <p className="text-gray-500 text-center mb-6">
                {isRTL 
                  ? 'أدخل بريدك الإلكتروني وسنرسل لك رابط إعادة التعيين'
                  : 'Enter your email and we\'ll send you a reset link'
                }
              </p>

              <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                  label={isRTL ? 'البريد الإلكتروني' : 'Email Address'}
                  type="email"
                  value={email}
                  onChange={setEmail}
                  placeholder={isRTL ? 'أدخل بريدك الإلكتروني' : 'Enter your email'}
                  icon={Mail}
                  error={error}
                />

                <Button type="submit" className="w-full" loading={loading}>
                  {loading ? (
                    <>
                      <Loader className="w-4 h-4 mr-2 animate-spin" />
                      {isRTL ? 'جاري الإرسال...' : 'Sending...'}
                    </>
                  ) : (
                    <>
                      <Mail className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                      {isRTL ? 'إرسال رابط إعادة التعيين' : 'Send Reset Link'}
                    </>
                  )}
                </Button>
              </form>

              <div className="mt-6 text-center">
                <Link 
                  to="/login" 
                  className="text-sm text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 inline-flex items-center gap-1"
                >
                  <ArrowLeft className="w-4 h-4 rtl:rotate-180" />
                  {isRTL ? 'العودة لتسجيل الدخول' : 'Back to Login'}
                </Link>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-6">
          {isRTL ? 'ليس لديك حساب؟ ' : 'Don\'t have an account? '}
          <Link to="/register" className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 font-medium">
            {isRTL ? 'سجل الآن' : 'Sign up'}
          </Link>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;
