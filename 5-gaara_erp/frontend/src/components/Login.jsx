// -*- javascript -*-
// FILE: frontend/src/components/Login.jsx
// PURPOSE: Modern Login page with shadcn/ui components
// OWNER: Frontend | LAST-AUDITED: 2025-12-08

/**
 * Login Page Component
 * Modern authentication page with shadcn/ui styling
 * 
 * Features:
 * - Beautiful gradient background
 * - Form validation
 * - Loading states
 * - Error handling
 * - Theme toggle
 * - RTL support
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Lock, LogIn, User, Loader2, Leaf } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { isSuccess, getErrorMessage } from '../utils/responseHelper';

// Import shadcn/ui components
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';
import { ThemeToggle } from './ui/theme-toggle';
import { cn } from '@/lib/utils';

const Login = () => {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const result = await login(credentials.username, credentials.password);

      if (isSuccess(result)) {
        navigate('/');
      } else {
        setError(getErrorMessage(result, 'خطأ في تسجيل الدخول'));
      }
    } catch (err) {
      setError(err.message || 'حدث خطأ أثناء تسجيل الدخول');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user types
    if (error) setError('');
  };

  return (
    <div className="min-h-screen flex flex-col" dir="rtl">
      {/* Background with gradient and pattern */}
      <div className="fixed inset-0 bg-gradient-to-br from-primary/5 via-background to-secondary/10 -z-10" />
      <div 
        className="fixed inset-0 -z-10 opacity-30"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2380AA45' fill-opacity='0.08'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />

      {/* Theme Toggle - Top Right */}
      <div className="absolute top-4 left-4">
        <ThemeToggle variant="default" />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-md animate-fade-in-up">
          <Card className="border-0 shadow-2xl bg-card/95 backdrop-blur-sm">
            <CardHeader className="space-y-1 text-center pb-2">
              {/* Logo */}
              <div className="mx-auto h-16 w-16 bg-gradient-to-br from-primary to-primary/80 rounded-2xl flex items-center justify-center mb-4 shadow-lg animate-scale-in">
                <Leaf className="h-8 w-8 text-primary-foreground" />
              </div>
              <CardTitle className="text-2xl font-bold">مرحباً بك</CardTitle>
              <CardDescription className="text-base">
                نظام إدارة المخزون الزراعي
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4 pt-4">
              {/* Error Message */}
              {error && (
                <Alert variant="destructive" className="animate-shake" dismissible onDismiss={() => setError('')}>
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {/* Login Form */}
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Username Field */}
                <div className="space-y-2">
                  <label htmlFor="username" className="text-sm font-medium text-foreground">
                    اسم المستخدم
                  </label>
                  <div className="relative">
                    <User className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="username"
                      name="username"
                      type="text"
                      required
                      autoComplete="username"
                      data-testid="username-input"
                      value={credentials.username}
                      onChange={handleInputChange}
                      className="pr-10"
                      placeholder="أدخل اسم المستخدم"
                      disabled={isLoading}
                    />
                  </div>
                </div>

                {/* Password Field */}
                <div className="space-y-2">
                  <label htmlFor="password" className="text-sm font-medium text-foreground">
                    كلمة المرور
                  </label>
                  <div className="relative">
                    <Lock className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      required
                      autoComplete="current-password"
                      data-testid="password-input"
                      value={credentials.password}
                      onChange={handleInputChange}
                      className="pr-10 pl-10"
                      placeholder="أدخل كلمة المرور"
                      disabled={isLoading}
                    />
                    <button
                      type="button"
                      className={cn(
                        "absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground",
                        "hover:text-foreground transition-colors",
                        "focus:outline-none focus:text-foreground"
                      )}
                      onClick={() => setShowPassword(!showPassword)}
                      tabIndex={-1}
                      aria-label={showPassword ? 'إخفاء كلمة المرور' : 'إظهار كلمة المرور'}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Submit Button */}
                <Button
                  type="submit"
                  className="w-full h-11 text-base gap-2"
                  disabled={isLoading}
                  loading={isLoading}
                >
                  {!isLoading && <LogIn className="h-4 w-4" />}
                  {isLoading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
                </Button>
              </form>
            </CardContent>

            <CardFooter className="flex flex-col gap-4 pt-2">
              {/* Demo Credentials */}
              <div className="w-full p-3 bg-muted/50 rounded-lg border border-border/50">
                <p className="text-xs text-center text-muted-foreground">
                  <span className="font-semibold text-primary">بيانات تجريبية:</span>
                  {' '}admin / admin123
                </p>
              </div>

              {/* Forgot Password Link */}
              <button 
                type="button"
                className="text-sm text-primary hover:underline focus:outline-none"
                onClick={() => navigate('/forgot-password')}
              >
                نسيت كلمة المرور؟
              </button>
            </CardFooter>
          </Card>

          {/* Footer */}
          <p className="text-center text-xs text-muted-foreground mt-6">
            © {new Date().getFullYear()} نظام إدارة المخزون. جميع الحقوق محفوظة.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
