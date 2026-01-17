/**
 * Two-Factor Authentication Verification Page
 * @file frontend/src/pages/TwoFactorVerify.jsx
 * 
 * صفحة التحقق من المصادقة الثنائية
 */

import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Shield, Loader2, AlertCircle, KeyRound } from 'lucide-react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Alert, AlertDescription } from '../components/ui/alert';
import { useAuth } from '../contexts/AuthContext';
import authService from '../services/authService';

const TwoFactorVerify = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  // 6-digit code input
  const [code, setCode] = useState(['', '', '', '', '', '']);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [useBackupCode, setUseBackupCode] = useState(false);
  const [backupCode, setBackupCode] = useState('');

  // Refs for digit inputs
  const inputRefs = useRef([]);

  // Get the pending user from location state
  const pendingUser = location.state?.pendingUser;

  useEffect(() => {
    // Redirect if no pending user
    if (!pendingUser) {
      navigate('/login');
    }
    // Focus first input
    inputRefs.current[0]?.focus();
  }, [pendingUser, navigate]);

  const handleDigitChange = (index, value) => {
    // Only allow numbers
    if (!/^\d*$/.test(value)) return;

    const newCode = [...code];
    newCode[index] = value.slice(-1); // Only take last digit
    setCode(newCode);

    // Auto-focus next input
    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }

    // Auto-submit when all digits are filled
    if (newCode.every(d => d !== '') && !isLoading) {
      handleSubmit(newCode.join(''));
    }
  };

  const handleKeyDown = (index, e) => {
    // Handle backspace
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    if (pastedData.length === 6) {
      const newCode = pastedData.split('');
      setCode(newCode);
      inputRefs.current[5]?.focus();
      handleSubmit(pastedData);
    }
  };

  const handleSubmit = async (codeToVerify = code.join('')) => {
    if (codeToVerify.length !== 6) {
      setError('يرجى إدخال الرمز المكون من 6 أرقام');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const result = await authService.verify2FA(codeToVerify);
      
      if (result.success) {
        // Login with the verified tokens
        login(result.user, result.access_token);
        navigate('/');
      } else {
        setError('رمز التحقق غير صحيح');
        setCode(['', '', '', '', '', '']);
        inputRefs.current[0]?.focus();
      }
    } catch (err) {
      setError(err.message || 'حدث خطأ أثناء التحقق');
      setCode(['', '', '', '', '', '']);
      inputRefs.current[0]?.focus();
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackupCodeSubmit = async (e) => {
    e.preventDefault();
    
    if (!backupCode.trim()) {
      setError('يرجى إدخال رمز الاسترداد');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const result = await authService.verify2FA(backupCode.trim());
      
      if (result.success) {
        login(result.user, result.access_token);
        navigate('/');
      } else {
        setError('رمز الاسترداد غير صحيح');
      }
    } catch (err) {
      setError(err.message || 'حدث خطأ أثناء التحقق');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendCode = async () => {
    // Implement resend logic if needed
    setError('تم إرسال رمز جديد إلى تطبيق المصادقة');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-primary/5 via-background to-secondary/10" dir="rtl">
      <Card className="w-full max-w-md border-0 shadow-2xl bg-card/95 backdrop-blur-sm">
        <CardHeader className="text-center space-y-2">
          <div className="mx-auto h-16 w-16 bg-gradient-to-br from-primary to-primary/80 rounded-2xl flex items-center justify-center mb-4">
            <Shield className="h-8 w-8 text-primary-foreground" />
          </div>
          <CardTitle className="text-2xl">التحقق بخطوتين</CardTitle>
          <CardDescription className="text-base">
            {useBackupCode 
              ? 'أدخل أحد رموز الاسترداد'
              : 'أدخل الرمز من تطبيق المصادقة'
            }
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {!useBackupCode ? (
            // 6-digit code input
            <div className="space-y-4">
              <div className="flex justify-center gap-2" dir="ltr">
                {code.map((digit, index) => (
                  <Input
                    key={index}
                    ref={el => inputRefs.current[index] = el}
                    type="text"
                    inputMode="numeric"
                    maxLength={1}
                    value={digit}
                    onChange={(e) => handleDigitChange(index, e.target.value)}
                    onKeyDown={(e) => handleKeyDown(index, e)}
                    onPaste={handlePaste}
                    className="w-12 h-14 text-center text-2xl font-bold"
                    disabled={isLoading}
                  />
                ))}
              </div>

              <p className="text-center text-sm text-muted-foreground">
                افتح تطبيق Google Authenticator وأدخل الرمز المعروض
              </p>

              <Button
                onClick={() => handleSubmit()}
                className="w-full h-11"
                disabled={isLoading || code.some(d => d === '')}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    جاري التحقق...
                  </>
                ) : (
                  'تحقق'
                )}
              </Button>
            </div>
          ) : (
            // Backup code input
            <form onSubmit={handleBackupCodeSubmit} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="backupCode" className="text-sm font-medium text-foreground">
                  رمز الاسترداد
                </label>
                <div className="relative">
                  <KeyRound className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="backupCode"
                    type="text"
                    value={backupCode}
                    onChange={(e) => {
                      setBackupCode(e.target.value);
                      if (error) setError('');
                    }}
                    className="pr-10"
                    placeholder="XXXX-XXXX-XXXX"
                    disabled={isLoading}
                  />
                </div>
              </div>

              <Button
                type="submit"
                className="w-full h-11"
                disabled={isLoading || !backupCode.trim()}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    جاري التحقق...
                  </>
                ) : (
                  'تحقق برمز الاسترداد'
                )}
              </Button>
            </form>
          )}
        </CardContent>

        <CardFooter className="flex-col gap-2">
          <Button
            variant="ghost"
            className="w-full text-sm"
            onClick={() => {
              setUseBackupCode(!useBackupCode);
              setError('');
              setCode(['', '', '', '', '', '']);
              setBackupCode('');
            }}
          >
            {useBackupCode 
              ? 'استخدام تطبيق المصادقة'
              : 'استخدام رمز الاسترداد'
            }
          </Button>

          <Button
            variant="link"
            className="text-sm text-muted-foreground"
            onClick={() => navigate('/login')}
          >
            العودة لتسجيل الدخول
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default TwoFactorVerify;
