/**
 * Two-Factor Authentication Setup Page
 * @file frontend/src/pages/TwoFactorSetup.jsx
 * 
 * صفحة إعداد المصادقة الثنائية
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Loader2, AlertCircle, CheckCircle, Copy, RefreshCw, Eye, EyeOff } from 'lucide-react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Alert, AlertDescription } from '../components/ui/alert';
import { useAuth } from '../contexts/AuthContext';
import { API_BASE_URL } from '../config/api';

const TwoFactorSetup = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [step, setStep] = useState(1); // 1: Setup, 2: Verify, 3: Complete
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // 2FA data
  const [qrCode, setQrCode] = useState('');
  const [backupCodes, setBackupCodes] = useState([]);
  const [verificationCode, setVerificationCode] = useState('');
  const [showBackupCodes, setShowBackupCodes] = useState(false);
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);
  const [backupCodesRemaining, setBackupCodesRemaining] = useState(0);

  // Check current 2FA status on mount
  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/2fa/status`, {
        credentials: 'include',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      const data = await res.json();
      if (data.success) {
        setTwoFactorEnabled(data.data.enabled);
        setBackupCodesRemaining(data.data.backup_codes_remaining);
      }
    } catch {
      // Ignore errors
    }
  };

  const enableTwoFactor = async () => {
    setIsLoading(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE_URL}/api/2fa/enable`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await res.json();

      if (data.success) {
        setQrCode(data.data.qr_code);
        setBackupCodes(data.data.backup_codes);
        setStep(2);
      } else {
        setError(data.error || 'فشل في تفعيل المصادقة الثنائية');
      }
    } catch (err) {
      setError('حدث خطأ في الاتصال بالخادم');
    } finally {
      setIsLoading(false);
    }
  };

  const verifyAndComplete = async () => {
    if (verificationCode.length !== 6) {
      setError('يرجى إدخال الرمز المكون من 6 أرقام');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE_URL}/api/2fa/verify`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: verificationCode })
      });

      const data = await res.json();

      if (data.success) {
        setStep(3);
        setSuccess('تم تفعيل المصادقة الثنائية بنجاح!');
        setTwoFactorEnabled(true);
      } else {
        setError('الرمز غير صحيح. يرجى المحاولة مرة أخرى.');
      }
    } catch (err) {
      setError('حدث خطأ في الاتصال بالخادم');
    } finally {
      setIsLoading(false);
    }
  };

  const disableTwoFactor = async () => {
    const code = prompt('أدخل رمز المصادقة من التطبيق:');
    const password = prompt('أدخل كلمة المرور للتأكيد:');

    if (!code || !password) return;

    setIsLoading(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE_URL}/api/2fa/disable`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code, password })
      });

      const data = await res.json();

      if (data.success) {
        setTwoFactorEnabled(false);
        setStep(1);
        setSuccess('تم تعطيل المصادقة الثنائية');
      } else {
        setError(data.error || 'فشل في تعطيل المصادقة الثنائية');
      }
    } catch (err) {
      setError('حدث خطأ في الاتصال بالخادم');
    } finally {
      setIsLoading(false);
    }
  };

  const regenerateBackupCodes = async () => {
    const code = prompt('أدخل رمز المصادقة من التطبيق لتأكيد الهوية:');
    if (!code) return;

    setIsLoading(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE_URL}/api/2fa/regenerate-backup-codes`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code })
      });

      const data = await res.json();

      if (data.success) {
        setBackupCodes(data.data.backup_codes);
        setBackupCodesRemaining(data.data.backup_codes.length);
        setShowBackupCodes(true);
        setSuccess('تم إنشاء رموز استرداد جديدة');
      } else {
        setError(data.error || 'فشل في إنشاء رموز الاسترداد');
      }
    } catch (err) {
      setError('حدث خطأ في الاتصال بالخادم');
    } finally {
      setIsLoading(false);
    }
  };

  const copyBackupCodes = () => {
    navigator.clipboard.writeText(backupCodes.join('\n'));
    setSuccess('تم نسخ رموز الاسترداد');
    setTimeout(() => setSuccess(''), 3000);
  };

  // Render based on 2FA status and step
  if (twoFactorEnabled && step === 1) {
    return (
      <div className="container max-w-2xl mx-auto py-8 px-4" dir="rtl">
        <Card className="border-0 shadow-xl">
          <CardHeader className="text-center">
            <div className="mx-auto h-16 w-16 bg-gradient-to-br from-primary to-primary/80 rounded-2xl flex items-center justify-center mb-4">
              <Shield className="h-8 w-8 text-primary-foreground" />
            </div>
            <CardTitle className="text-2xl">المصادقة الثنائية مفعلة</CardTitle>
            <CardDescription>حسابك محمي بالمصادقة الثنائية</CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {success && (
              <Alert className="bg-primary/10 border-primary/20">
                <CheckCircle className="h-4 w-4 text-primary" />
                <AlertDescription className="text-primary">{success}</AlertDescription>
              </Alert>
            )}

            <div className="bg-muted/50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-foreground">رموز الاسترداد المتبقية</p>
                  <p className="text-sm text-muted-foreground">
                    {backupCodesRemaining} رموز متبقية من 10
                  </p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={regenerateBackupCodes}
                  disabled={isLoading}
                >
                  <RefreshCw className={`h-4 w-4 ml-2 ${isLoading ? 'animate-spin' : ''}`} />
                  إنشاء رموز جديدة
                </Button>
              </div>
            </div>

            {backupCodes.length > 0 && showBackupCodes && (
              <div className="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4 border border-amber-200 dark:border-amber-800">
                <div className="flex items-center justify-between mb-3">
                  <p className="font-medium text-amber-800 dark:text-amber-200">رموز الاسترداد الجديدة</p>
                  <div className="flex gap-2">
                    <Button variant="ghost" size="sm" onClick={copyBackupCodes}>
                      <Copy className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowBackupCodes(false)}
                    >
                      <EyeOff className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {backupCodes.map((code, index) => (
                    <code
                      key={index}
                      className="bg-white dark:bg-gray-800 px-3 py-2 rounded text-center font-mono text-sm"
                    >
                      {code}
                    </code>
                  ))}
                </div>
              </div>
            )}
          </CardContent>

          <CardFooter className="flex-col gap-3">
            <Button
              variant="destructive"
              className="w-full"
              onClick={disableTwoFactor}
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 ml-2 animate-spin" />
                  جاري التعطيل...
                </>
              ) : (
                'تعطيل المصادقة الثنائية'
              )}
            </Button>
            <Button
              variant="ghost"
              className="w-full"
              onClick={() => navigate('/settings')}
            >
              العودة للإعدادات
            </Button>
          </CardFooter>
        </Card>
      </div>
    );
  }

  return (
    <div className="container max-w-2xl mx-auto py-8 px-4" dir="rtl">
      <Card className="border-0 shadow-xl">
        <CardHeader className="text-center">
          <div className="mx-auto h-16 w-16 bg-gradient-to-br from-primary to-primary/80 rounded-2xl flex items-center justify-center mb-4">
            <Shield className="h-8 w-8 text-primary-foreground" />
          </div>
          <CardTitle className="text-2xl">
            {step === 1 && 'إعداد المصادقة الثنائية'}
            {step === 2 && 'مسح رمز QR'}
            {step === 3 && 'تم الإعداد بنجاح!'}
          </CardTitle>
          <CardDescription>
            {step === 1 && 'أضف طبقة حماية إضافية لحسابك'}
            {step === 2 && 'امسح رمز QR باستخدام تطبيق Google Authenticator'}
            {step === 3 && 'حسابك محمي الآن بالمصادقة الثنائية'}
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert className="bg-primary/10 border-primary/20">
              <CheckCircle className="h-4 w-4 text-primary" />
              <AlertDescription className="text-primary">{success}</AlertDescription>
            </Alert>
          )}

          {/* Step 1: Introduction */}
          {step === 1 && (
            <div className="space-y-4">
              <div className="bg-muted/50 rounded-lg p-4">
                <h3 className="font-semibold text-foreground mb-2">ما هي المصادقة الثنائية؟</h3>
                <p className="text-sm text-muted-foreground">
                  المصادقة الثنائية تضيف طبقة أمان إضافية لحسابك. بعد إدخال كلمة المرور،
                  ستحتاج إلى إدخال رمز من تطبيق المصادقة على هاتفك.
                </p>
              </div>

              <div className="bg-muted/50 rounded-lg p-4">
                <h3 className="font-semibold text-foreground mb-2">ماذا تحتاج؟</h3>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• تطبيق Google Authenticator أو Authy على هاتفك</li>
                  <li>• بضع دقائق لإكمال الإعداد</li>
                </ul>
              </div>

              <Button
                className="w-full h-12"
                onClick={enableTwoFactor}
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 ml-2 animate-spin" />
                    جاري التحميل...
                  </>
                ) : (
                  'بدء الإعداد'
                )}
              </Button>
            </div>
          )}

          {/* Step 2: QR Code */}
          {step === 2 && (
            <div className="space-y-6">
              {/* QR Code */}
              <div className="flex justify-center">
                {qrCode && (
                  <img
                    src={qrCode}
                    alt="QR Code"
                    className="w-48 h-48 border rounded-lg"
                  />
                )}
              </div>

              <p className="text-center text-sm text-muted-foreground">
                امسح هذا الرمز باستخدام تطبيق Google Authenticator
              </p>

              {/* Verification Code Input */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  أدخل الرمز من التطبيق
                </label>
                <Input
                  type="text"
                  inputMode="numeric"
                  maxLength={6}
                  value={verificationCode}
                  onChange={(e) => {
                    const val = e.target.value.replace(/\D/g, '');
                    setVerificationCode(val);
                    setError('');
                  }}
                  placeholder="000000"
                  className="text-center text-2xl font-mono tracking-widest"
                />
              </div>

              {/* Backup Codes Preview */}
              <div className="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4 border border-amber-200 dark:border-amber-800">
                <div className="flex items-center justify-between mb-3">
                  <p className="font-medium text-amber-800 dark:text-amber-200">رموز الاسترداد</p>
                  <Button variant="ghost" size="sm" onClick={copyBackupCodes}>
                    <Copy className="h-4 w-4 ml-2" />
                    نسخ
                  </Button>
                </div>
                <p className="text-sm text-amber-700 dark:text-amber-300 mb-3">
                  احفظ هذه الرموز في مكان آمن. يمكنك استخدامها لتسجيل الدخول إذا فقدت هاتفك.
                </p>
                <div className="grid grid-cols-2 gap-2">
                  {backupCodes.map((code, index) => (
                    <code
                      key={index}
                      className="bg-white dark:bg-gray-800 px-3 py-2 rounded text-center font-mono text-sm"
                    >
                      {code}
                    </code>
                  ))}
                </div>
              </div>

              <Button
                className="w-full h-12"
                onClick={verifyAndComplete}
                disabled={isLoading || verificationCode.length !== 6}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 ml-2 animate-spin" />
                    جاري التحقق...
                  </>
                ) : (
                  'تأكيد وتفعيل'
                )}
              </Button>
            </div>
          )}

          {/* Step 3: Complete */}
          {step === 3 && (
            <div className="space-y-6 text-center">
              <div className="mx-auto h-20 w-20 bg-primary/10 rounded-full flex items-center justify-center">
                <CheckCircle className="h-10 w-10 text-primary" />
              </div>

              <div>
                <h3 className="text-lg font-semibold text-foreground mb-2">
                  تم تفعيل المصادقة الثنائية!
                </h3>
                <p className="text-sm text-muted-foreground">
                  حسابك محمي الآن. في المرة القادمة التي تسجل فيها الدخول،
                  ستحتاج إلى إدخال رمز من تطبيق المصادقة.
                </p>
              </div>

              <Button
                className="w-full"
                onClick={() => navigate('/settings')}
              >
                العودة للإعدادات
              </Button>
            </div>
          )}
        </CardContent>

        {step !== 3 && (
          <CardFooter>
            <Button
              variant="ghost"
              className="w-full"
              onClick={() => navigate(-1)}
            >
              إلغاء
            </Button>
          </CardFooter>
        )}
      </Card>
    </div>
  );
};

export default TwoFactorSetup;
