/**
 * Logout Page Component
 * @file frontend/src/pages/Logout.jsx
 * 
 * صفحة تسجيل الخروج مع رسالة وداع
 */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, CheckCircle, Loader2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { useAuth } from '../contexts/AuthContext';

const Logout = () => {
  const navigate = useNavigate();
  const { logout, user } = useAuth();
  const [isLoggingOut, setIsLoggingOut] = useState(true);
  const [logoutComplete, setLogoutComplete] = useState(false);

  useEffect(() => {
    const performLogout = async () => {
      try {
        await logout();
        setLogoutComplete(true);
        
        // Auto-redirect after 3 seconds
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } catch (error) {
        console.error('Logout error:', error);
        // Still redirect on error
        setLogoutComplete(true);
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } finally {
        setIsLoggingOut(false);
      }
    };

    performLogout();
  }, [logout, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-primary/5 via-background to-secondary/10" dir="rtl">
      <Card className="w-full max-w-md border-0 shadow-2xl bg-card/95 backdrop-blur-sm">
        <CardHeader className="text-center space-y-2">
          <div className={`mx-auto h-16 w-16 rounded-2xl flex items-center justify-center mb-4 transition-all duration-500 ${
            logoutComplete 
              ? 'bg-gradient-to-br from-green-500 to-green-600' 
              : 'bg-gradient-to-br from-primary to-primary/80'
          }`}>
            {isLoggingOut ? (
              <Loader2 className="h-8 w-8 text-white animate-spin" />
            ) : (
              <CheckCircle className="h-8 w-8 text-white" />
            )}
          </div>

          <CardTitle className="text-2xl">
            {isLoggingOut ? 'جاري تسجيل الخروج...' : 'تم تسجيل الخروج'}
          </CardTitle>

          <CardDescription className="text-base">
            {isLoggingOut 
              ? 'يرجى الانتظار قليلاً...'
              : `وداعاً${user?.full_name ? ` ${user.full_name}` : ''}، نتمنى لك يوماً سعيداً!`
            }
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          {logoutComplete && (
            <>
              <div className="p-4 bg-muted/50 rounded-lg text-center">
                <p className="text-sm text-muted-foreground">
                  سيتم توجيهك لصفحة تسجيل الدخول خلال ثوانٍ...
                </p>
              </div>

              <div className="flex gap-3">
                <Button 
                  variant="outline" 
                  className="flex-1"
                  onClick={() => navigate('/login')}
                >
                  تسجيل الدخول مجدداً
                </Button>
                <Button 
                  variant="ghost" 
                  className="flex-1"
                  onClick={() => window.close()}
                >
                  إغلاق
                </Button>
              </div>
            </>
          )}

          {/* Session info */}
          {!isLoggingOut && (
            <div className="mt-6 pt-4 border-t border-border/50">
              <p className="text-xs text-center text-muted-foreground">
                تم إنهاء جلستك بنجاح وحذف جميع البيانات المؤقتة
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Logout;
