/**
 * Profile Page Component
 * @file frontend/src/pages/Profile.jsx
 * 
 * صفحة الملف الشخصي مع إدارة الحساب
 */

import React, { useState, useCallback } from 'react';
import { 
  User, 
  Mail, 
  Phone, 
  Shield, 
  Key, 
  Bell, 
  Camera,
  Save,
  Lock,
  Smartphone,
  Clock,
  Settings,
  LogOut,
  AlertCircle
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Switch } from '../components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { Separator } from '../components/ui/separator';
import { Badge } from '../components/ui/badge';
import { useAuth } from '../contexts/AuthContext';
import { authService } from '../services/authService';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('profile');
  
  // Profile form state
  const [profileData, setProfileData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  // Notification settings
  const [notifications, setNotifications] = useState({
    email_notifications: true,
    push_notifications: true,
    low_stock_alerts: true,
    expiry_alerts: true,
    login_alerts: true
  });

  // Handle profile update
  const handleProfileUpdate = useCallback(async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      updateUser?.({
        ...user,
        full_name: profileData.full_name,
        email: profileData.email,
        phone: profileData.phone
      });
      
      toast.success('تم تحديث الملف الشخصي بنجاح');
    } catch (error) {
      toast.error('فشل في تحديث الملف الشخصي');
      console.error('Profile update error:', error);
    } finally {
      setIsLoading(false);
    }
  }, [profileData, user, updateUser]);

  // Handle password change
  const handlePasswordChange = useCallback(async (e) => {
    e.preventDefault();
    
    if (profileData.new_password !== profileData.confirm_password) {
      toast.error('كلمتا المرور غير متطابقتين');
      return;
    }
    
    if (profileData.new_password.length < 8) {
      toast.error('كلمة المرور يجب أن تكون 8 أحرف على الأقل');
      return;
    }
    
    setIsLoading(true);
    
    try {
      await authService.changePassword(
        profileData.current_password,
        profileData.new_password
      );
      
      toast.success('تم تغيير كلمة المرور بنجاح');
      setProfileData(prev => ({
        ...prev,
        current_password: '',
        new_password: '',
        confirm_password: ''
      }));
    } catch (error) {
      toast.error(error.message || 'فشل في تغيير كلمة المرور');
    } finally {
      setIsLoading(false);
    }
  }, [profileData]);

  // Get user initials
  const getInitials = (name) => {
    if (!name) return 'U';
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl" dir="rtl">
      {/* Header */}
      <div className="flex items-center gap-6 mb-8">
        <div className="relative">
          <Avatar className="h-24 w-24">
            <AvatarImage src={user?.avatar_url} />
            <AvatarFallback className="text-2xl bg-primary/10 text-primary">
              {getInitials(user?.full_name)}
            </AvatarFallback>
          </Avatar>
          <Button 
            size="icon" 
            variant="outline"
            className="absolute bottom-0 left-0 h-8 w-8 rounded-full"
          >
            <Camera className="h-4 w-4" />
          </Button>
        </div>
        
        <div className="flex-1">
          <h1 className="text-2xl font-bold">{user?.full_name || 'المستخدم'}</h1>
          <p className="text-muted-foreground">{user?.email}</p>
          <div className="flex items-center gap-2 mt-2">
            <Badge variant="secondary">
              {user?.role === 'admin' ? 'مدير' : 
               user?.role === 'manager' ? 'مشرف' : 
               user?.role === 'cashier' ? 'كاشير' : 'مستخدم'}
            </Badge>
            {user?.is_verified && (
              <Badge variant="outline" className="text-green-600">
                <Shield className="h-3 w-3 mr-1" />
                موثق
              </Badge>
            )}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4 mb-6">
          <TabsTrigger value="profile">
            <User className="h-4 w-4 ml-2" />
            الملف الشخصي
          </TabsTrigger>
          <TabsTrigger value="security">
            <Shield className="h-4 w-4 ml-2" />
            الأمان
          </TabsTrigger>
          <TabsTrigger value="notifications">
            <Bell className="h-4 w-4 ml-2" />
            الإشعارات
          </TabsTrigger>
          <TabsTrigger value="sessions">
            <Clock className="h-4 w-4 ml-2" />
            الجلسات
          </TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>المعلومات الشخصية</CardTitle>
              <CardDescription>
                قم بتحديث معلومات ملفك الشخصي
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleProfileUpdate} className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="full_name">الاسم الكامل</Label>
                    <Input
                      id="full_name"
                      value={profileData.full_name}
                      onChange={(e) => setProfileData(prev => ({ 
                        ...prev, 
                        full_name: e.target.value 
                      }))}
                      placeholder="أدخل اسمك الكامل"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="email">البريد الإلكتروني</Label>
                    <Input
                      id="email"
                      type="email"
                      value={profileData.email}
                      onChange={(e) => setProfileData(prev => ({ 
                        ...prev, 
                        email: e.target.value 
                      }))}
                      placeholder="example@domain.com"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="phone">رقم الهاتف</Label>
                    <Input
                      id="phone"
                      value={profileData.phone}
                      onChange={(e) => setProfileData(prev => ({ 
                        ...prev, 
                        phone: e.target.value 
                      }))}
                      placeholder="05XXXXXXXX"
                      dir="ltr"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label>اسم المستخدم</Label>
                    <Input
                      value={user?.username || ''}
                      disabled
                      className="bg-muted"
                    />
                    <p className="text-xs text-muted-foreground">
                      لا يمكن تغيير اسم المستخدم
                    </p>
                  </div>
                </div>
                
                <div className="flex justify-end">
                  <Button type="submit" disabled={isLoading}>
                    <Save className="h-4 w-4 ml-2" />
                    {isLoading ? 'جاري الحفظ...' : 'حفظ التغييرات'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Security Tab */}
        <TabsContent value="security">
          <div className="space-y-6">
            {/* Password Change */}
            <Card>
              <CardHeader>
                <CardTitle>تغيير كلمة المرور</CardTitle>
                <CardDescription>
                  تأكد من استخدام كلمة مرور قوية
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handlePasswordChange} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="current_password">كلمة المرور الحالية</Label>
                    <Input
                      id="current_password"
                      type="password"
                      value={profileData.current_password}
                      onChange={(e) => setProfileData(prev => ({ 
                        ...prev, 
                        current_password: e.target.value 
                      }))}
                    />
                  </div>
                  
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="new_password">كلمة المرور الجديدة</Label>
                      <Input
                        id="new_password"
                        type="password"
                        value={profileData.new_password}
                        onChange={(e) => setProfileData(prev => ({ 
                          ...prev, 
                          new_password: e.target.value 
                        }))}
                      />
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="confirm_password">تأكيد كلمة المرور</Label>
                      <Input
                        id="confirm_password"
                        type="password"
                        value={profileData.confirm_password}
                        onChange={(e) => setProfileData(prev => ({ 
                          ...prev, 
                          confirm_password: e.target.value 
                        }))}
                      />
                    </div>
                  </div>
                  
                  <div className="flex justify-end">
                    <Button type="submit" disabled={isLoading}>
                      <Key className="h-4 w-4 ml-2" />
                      تغيير كلمة المرور
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>

            {/* Two Factor Auth */}
            <Card>
              <CardHeader>
                <CardTitle>المصادقة الثنائية</CardTitle>
                <CardDescription>
                  أضف طبقة حماية إضافية لحسابك
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="p-3 rounded-lg bg-primary/10">
                      <Smartphone className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                      <p className="font-medium">المصادقة عبر التطبيق</p>
                      <p className="text-sm text-muted-foreground">
                        استخدم تطبيق Google Authenticator أو مشابه
                      </p>
                    </div>
                  </div>
                  <Button variant="outline">
                    {user?.two_factor_enabled ? 'تعطيل' : 'تفعيل'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications">
          <Card>
            <CardHeader>
              <CardTitle>إعدادات الإشعارات</CardTitle>
              <CardDescription>
                تحكم في الإشعارات التي تصلك
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">إشعارات البريد الإلكتروني</p>
                  <p className="text-sm text-muted-foreground">
                    استلم إشعارات عبر البريد
                  </p>
                </div>
                <Switch 
                  checked={notifications.email_notifications}
                  onCheckedChange={(checked) => 
                    setNotifications(prev => ({ ...prev, email_notifications: checked }))
                  }
                />
              </div>
              
              <Separator />
              
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">تنبيهات المخزون المنخفض</p>
                  <p className="text-sm text-muted-foreground">
                    عند انخفاض المخزون عن الحد الأدنى
                  </p>
                </div>
                <Switch 
                  checked={notifications.low_stock_alerts}
                  onCheckedChange={(checked) => 
                    setNotifications(prev => ({ ...prev, low_stock_alerts: checked }))
                  }
                />
              </div>
              
              <Separator />
              
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">تنبيهات انتهاء الصلاحية</p>
                  <p className="text-sm text-muted-foreground">
                    عند اقتراب انتهاء صلاحية المنتجات
                  </p>
                </div>
                <Switch 
                  checked={notifications.expiry_alerts}
                  onCheckedChange={(checked) => 
                    setNotifications(prev => ({ ...prev, expiry_alerts: checked }))
                  }
                />
              </div>
              
              <Separator />
              
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">تنبيهات تسجيل الدخول</p>
                  <p className="text-sm text-muted-foreground">
                    عند تسجيل الدخول من جهاز جديد
                  </p>
                </div>
                <Switch 
                  checked={notifications.login_alerts}
                  onCheckedChange={(checked) => 
                    setNotifications(prev => ({ ...prev, login_alerts: checked }))
                  }
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Sessions Tab */}
        <TabsContent value="sessions">
          <Card>
            <CardHeader>
              <CardTitle>الجلسات النشطة</CardTitle>
              <CardDescription>
                إدارة الأجهزة المتصلة بحسابك
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Current Session */}
                <div className="flex items-center justify-between p-4 border rounded-lg bg-green-50 dark:bg-green-950/20">
                  <div className="flex items-center gap-4">
                    <div className="p-2 rounded-lg bg-green-100 dark:bg-green-900/30">
                      <Shield className="h-5 w-5 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium">الجلسة الحالية</p>
                      <p className="text-sm text-muted-foreground">
                        هذا الجهاز - {navigator.userAgent.split('(')[1]?.split(')')[0]}
                      </p>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-green-600">
                    نشط الآن
                  </Badge>
                </div>
                
                {/* Info */}
                <div className="flex items-center gap-2 p-4 border rounded-lg bg-muted/50">
                  <AlertCircle className="h-5 w-5 text-muted-foreground" />
                  <p className="text-sm text-muted-foreground">
                    إذا لاحظت أي نشاط مشبوه، قم بتغيير كلمة المرور فوراً
                  </p>
                </div>
                
                <div className="flex justify-end">
                  <Button variant="destructive">
                    <LogOut className="h-4 w-4 ml-2" />
                    تسجيل الخروج من جميع الأجهزة
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Profile;
