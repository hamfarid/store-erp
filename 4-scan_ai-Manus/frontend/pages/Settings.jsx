/**
 * Settings Page - Application Settings Management
 * ================================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect } from 'react';
import {
  Settings as SettingsIcon, User, Bell, Shield, Globe, Palette,
  Database, Mail, Key, Eye, EyeOff, Save, RefreshCw, AlertTriangle,
  Moon, Sun, Monitor, Check, X, Smartphone, Lock, Unlock
} from 'lucide-react';

import ApiService from '../services/ApiService';
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import { Input, Select, Switch, TextArea } from '../src/components/Form';
import Modal from '../src/components/Modal';

// ============================================
// Settings Section Component
// ============================================
const SettingsSection = ({ title, titleAr, description, descriptionAr, icon: Icon, children }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  return (
    <Card>
      <CardHeader className="border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-emerald-100 dark:bg-emerald-900/30">
            <Icon className="w-5 h-5 text-emerald-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 dark:text-white">
              {isRTL ? titleAr : title}
            </h3>
            <p className="text-sm text-gray-500">
              {isRTL ? descriptionAr : description}
            </p>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-6">{children}</CardContent>
    </Card>
  );
};

// ============================================
// Setting Row Component
// ============================================
const SettingRow = ({ label, labelAr, description, descriptionAr, children }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  return (
    <div className="flex flex-col md:flex-row md:items-center justify-between py-4 border-b border-gray-100 dark:border-gray-800 last:border-0">
      <div className="mb-3 md:mb-0">
        <h4 className="font-medium text-gray-800 dark:text-white">
          {isRTL ? labelAr : label}
        </h4>
        {(description || descriptionAr) && (
          <p className="text-sm text-gray-500 mt-0.5">
            {isRTL ? descriptionAr : description}
          </p>
        )}
      </div>
      <div className="md:w-1/3">{children}</div>
    </div>
  );
};

// ============================================
// Main Settings Page
// ============================================
const Settings = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const [activeTab, setActiveTab] = useState('general');

  // Settings State
  const [settings, setSettings] = useState({
    // General
    language: 'ar',
    timezone: 'Asia/Riyadh',
    dateFormat: 'DD/MM/YYYY',
    
    // Appearance
    theme: 'system',
    compactMode: false,
    animations: true,
    
    // Notifications
    emailNotifications: true,
    pushNotifications: true,
    diagnosisAlerts: true,
    weeklyReport: true,
    marketingEmails: false,
    
    // Privacy
    profileVisibility: 'public',
    activityStatus: true,
    dataSharing: false,
    
    // Security
    twoFactorEnabled: false,
    sessionTimeout: 30,
    loginAlerts: true
  });

  const [show2FAModal, setShow2FAModal] = useState(false);

  const tabs = [
    { id: 'general', label: 'General', labelAr: 'عام', icon: SettingsIcon },
    { id: 'appearance', label: 'Appearance', labelAr: 'المظهر', icon: Palette },
    { id: 'notifications', label: 'Notifications', labelAr: 'الإشعارات', icon: Bell },
    { id: 'privacy', label: 'Privacy', labelAr: 'الخصوصية', icon: Eye },
    { id: 'security', label: 'Security', labelAr: 'الأمان', icon: Shield }
  ];

  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    setSaved(false);
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      await ApiService.updateSettings(settings);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error('Error saving settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general':
        return (
          <SettingsSection
            title="General Settings"
            titleAr="الإعدادات العامة"
            description="Basic application preferences"
            descriptionAr="التفضيلات الأساسية للتطبيق"
            icon={SettingsIcon}
          >
            <SettingRow
              label="Language"
              labelAr="اللغة"
              description="Select your preferred language"
              descriptionAr="اختر لغتك المفضلة"
            >
              <Select
                value={settings.language}
                onChange={(v) => handleChange('language', v)}
                options={[
                  { value: 'ar', label: 'العربية' },
                  { value: 'en', label: 'English' }
                ]}
              />
            </SettingRow>

            <SettingRow
              label="Timezone"
              labelAr="المنطقة الزمنية"
              description="Your local timezone"
              descriptionAr="منطقتك الزمنية المحلية"
            >
              <Select
                value={settings.timezone}
                onChange={(v) => handleChange('timezone', v)}
                options={[
                  { value: 'Asia/Riyadh', label: '(GMT+3) Riyadh' },
                  { value: 'Asia/Dubai', label: '(GMT+4) Dubai' },
                  { value: 'Africa/Cairo', label: '(GMT+2) Cairo' },
                  { value: 'Europe/London', label: '(GMT+0) London' },
                  { value: 'America/New_York', label: '(GMT-5) New York' }
                ]}
              />
            </SettingRow>

            <SettingRow
              label="Date Format"
              labelAr="تنسيق التاريخ"
              description="How dates are displayed"
              descriptionAr="كيف يتم عرض التواريخ"
            >
              <Select
                value={settings.dateFormat}
                onChange={(v) => handleChange('dateFormat', v)}
                options={[
                  { value: 'DD/MM/YYYY', label: 'DD/MM/YYYY' },
                  { value: 'MM/DD/YYYY', label: 'MM/DD/YYYY' },
                  { value: 'YYYY-MM-DD', label: 'YYYY-MM-DD' }
                ]}
              />
            </SettingRow>
          </SettingsSection>
        );

      case 'appearance':
        return (
          <SettingsSection
            title="Appearance"
            titleAr="المظهر"
            description="Customize how the app looks"
            descriptionAr="خصص مظهر التطبيق"
            icon={Palette}
          >
            <SettingRow
              label="Theme"
              labelAr="السمة"
              description="Choose light, dark, or system theme"
              descriptionAr="اختر السمة الفاتحة أو الداكنة أو النظام"
            >
              <div className="flex gap-2">
                {[
                  { value: 'light', icon: Sun, label: 'Light' },
                  { value: 'dark', icon: Moon, label: 'Dark' },
                  { value: 'system', icon: Monitor, label: 'System' }
                ].map(({ value, icon: Icon, label }) => (
                  <button
                    key={value}
                    onClick={() => handleChange('theme', value)}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-lg border transition-all
                      ${settings.theme === value
                        ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600'
                        : 'border-gray-200 dark:border-gray-700 hover:border-gray-300'
                      }
                    `}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="text-sm">{label}</span>
                  </button>
                ))}
              </div>
            </SettingRow>

            <SettingRow
              label="Compact Mode"
              labelAr="الوضع المضغوط"
              description="Use less space for elements"
              descriptionAr="استخدام مساحة أقل للعناصر"
            >
              <Switch
                checked={settings.compactMode}
                onChange={(v) => handleChange('compactMode', v)}
              />
            </SettingRow>

            <SettingRow
              label="Animations"
              labelAr="الرسوم المتحركة"
              description="Enable smooth animations"
              descriptionAr="تفعيل الرسوم المتحركة السلسة"
            >
              <Switch
                checked={settings.animations}
                onChange={(v) => handleChange('animations', v)}
              />
            </SettingRow>
          </SettingsSection>
        );

      case 'notifications':
        return (
          <SettingsSection
            title="Notifications"
            titleAr="الإشعارات"
            description="Manage your notification preferences"
            descriptionAr="إدارة تفضيلات الإشعارات"
            icon={Bell}
          >
            <SettingRow
              label="Email Notifications"
              labelAr="إشعارات البريد"
              description="Receive notifications via email"
              descriptionAr="استلام الإشعارات عبر البريد"
            >
              <Switch
                checked={settings.emailNotifications}
                onChange={(v) => handleChange('emailNotifications', v)}
              />
            </SettingRow>

            <SettingRow
              label="Push Notifications"
              labelAr="الإشعارات الفورية"
              description="Browser push notifications"
              descriptionAr="إشعارات المتصفح الفورية"
            >
              <Switch
                checked={settings.pushNotifications}
                onChange={(v) => handleChange('pushNotifications', v)}
              />
            </SettingRow>

            <SettingRow
              label="Diagnosis Alerts"
              labelAr="تنبيهات التشخيص"
              description="Get notified for critical diagnoses"
              descriptionAr="التنبيه عند التشخيصات الحرجة"
            >
              <Switch
                checked={settings.diagnosisAlerts}
                onChange={(v) => handleChange('diagnosisAlerts', v)}
              />
            </SettingRow>

            <SettingRow
              label="Weekly Report"
              labelAr="التقرير الأسبوعي"
              description="Receive weekly summary"
              descriptionAr="استلام ملخص أسبوعي"
            >
              <Switch
                checked={settings.weeklyReport}
                onChange={(v) => handleChange('weeklyReport', v)}
              />
            </SettingRow>

            <SettingRow
              label="Marketing Emails"
              labelAr="رسائل التسويق"
              description="Receive promotional content"
              descriptionAr="استلام المحتوى الترويجي"
            >
              <Switch
                checked={settings.marketingEmails}
                onChange={(v) => handleChange('marketingEmails', v)}
              />
            </SettingRow>
          </SettingsSection>
        );

      case 'privacy':
        return (
          <SettingsSection
            title="Privacy"
            titleAr="الخصوصية"
            description="Control your data and visibility"
            descriptionAr="التحكم في بياناتك وظهورك"
            icon={Eye}
          >
            <SettingRow
              label="Profile Visibility"
              labelAr="ظهور الملف الشخصي"
              description="Who can see your profile"
              descriptionAr="من يمكنه رؤية ملفك الشخصي"
            >
              <Select
                value={settings.profileVisibility}
                onChange={(v) => handleChange('profileVisibility', v)}
                options={[
                  { value: 'public', label: isRTL ? 'عام' : 'Public' },
                  { value: 'team', label: isRTL ? 'الفريق فقط' : 'Team Only' },
                  { value: 'private', label: isRTL ? 'خاص' : 'Private' }
                ]}
              />
            </SettingRow>

            <SettingRow
              label="Activity Status"
              labelAr="حالة النشاط"
              description="Show when you're online"
              descriptionAr="إظهار عندما تكون متصلاً"
            >
              <Switch
                checked={settings.activityStatus}
                onChange={(v) => handleChange('activityStatus', v)}
              />
            </SettingRow>

            <SettingRow
              label="Data Sharing"
              labelAr="مشاركة البيانات"
              description="Share anonymous usage data"
              descriptionAr="مشاركة بيانات الاستخدام المجهولة"
            >
              <Switch
                checked={settings.dataSharing}
                onChange={(v) => handleChange('dataSharing', v)}
              />
            </SettingRow>
          </SettingsSection>
        );

      case 'security':
        return (
          <SettingsSection
            title="Security"
            titleAr="الأمان"
            description="Protect your account"
            descriptionAr="حماية حسابك"
            icon={Shield}
          >
            <SettingRow
              label="Two-Factor Authentication"
              labelAr="المصادقة الثنائية"
              description="Add an extra layer of security"
              descriptionAr="إضافة طبقة أمان إضافية"
            >
              <div className="flex items-center gap-3">
                <Badge variant={settings.twoFactorEnabled ? 'emerald' : 'gray'}>
                  {settings.twoFactorEnabled ? (isRTL ? 'مفعل' : 'Enabled') : (isRTL ? 'معطل' : 'Disabled')}
                </Badge>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShow2FAModal(true)}
                >
                  {settings.twoFactorEnabled ? (isRTL ? 'تعطيل' : 'Disable') : (isRTL ? 'تفعيل' : 'Enable')}
                </Button>
              </div>
            </SettingRow>

            <SettingRow
              label="Session Timeout"
              labelAr="مهلة الجلسة"
              description="Auto logout after inactivity"
              descriptionAr="تسجيل الخروج التلقائي بعد عدم النشاط"
            >
              <Select
                value={settings.sessionTimeout}
                onChange={(v) => handleChange('sessionTimeout', parseInt(v))}
                options={[
                  { value: 15, label: '15 ' + (isRTL ? 'دقيقة' : 'minutes') },
                  { value: 30, label: '30 ' + (isRTL ? 'دقيقة' : 'minutes') },
                  { value: 60, label: '1 ' + (isRTL ? 'ساعة' : 'hour') },
                  { value: 120, label: '2 ' + (isRTL ? 'ساعات' : 'hours') }
                ]}
              />
            </SettingRow>

            <SettingRow
              label="Login Alerts"
              labelAr="تنبيهات تسجيل الدخول"
              description="Get notified on new logins"
              descriptionAr="التنبيه عند تسجيل دخول جديد"
            >
              <Switch
                checked={settings.loginAlerts}
                onChange={(v) => handleChange('loginAlerts', v)}
              />
            </SettingRow>

            <div className="pt-4 border-t">
              <Button variant="danger">
                <Key className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                {isRTL ? 'تغيير كلمة المرور' : 'Change Password'}
              </Button>
            </div>
          </SettingsSection>
        );

      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'الإعدادات' : 'Settings'}
        description={isRTL ? 'إدارة تفضيلات حسابك' : 'Manage your account preferences'}
        icon={SettingsIcon}
      >
        <Button onClick={handleSave} loading={loading}>
          {saved ? <Check className="w-4 h-4 mr-2" /> : <Save className="w-4 h-4 mr-2" />}
          {saved ? (isRTL ? 'تم الحفظ' : 'Saved') : (isRTL ? 'حفظ التغييرات' : 'Save Changes')}
        </Button>
      </PageHeader>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar Navigation */}
        <div className="lg:w-64 flex-shrink-0">
          <Card className="sticky top-6">
            <nav className="p-2">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium
                    transition-colors
                    ${activeTab === tab.id
                      ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600'
                      : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }
                  `}
                >
                  <tab.icon className="w-5 h-5" />
                  {isRTL ? tab.labelAr : tab.label}
                </button>
              ))}
            </nav>
          </Card>
        </div>

        {/* Content */}
        <div className="flex-1">{renderTabContent()}</div>
      </div>

      {/* 2FA Modal */}
      <Modal
        isOpen={show2FAModal}
        onClose={() => setShow2FAModal(false)}
        title={isRTL ? 'المصادقة الثنائية' : 'Two-Factor Authentication'}
        size="sm"
      >
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
            <Shield className="w-8 h-8 text-emerald-500" />
          </div>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            {isRTL
              ? 'سيتم إرسال رمز التحقق إلى هاتفك عند كل تسجيل دخول'
              : 'A verification code will be sent to your phone on each login'
            }
          </p>
          <div className="flex justify-center gap-3">
            <Button variant="secondary" onClick={() => setShow2FAModal(false)}>
              {isRTL ? 'إلغاء' : 'Cancel'}
            </Button>
            <Button onClick={() => {
              handleChange('twoFactorEnabled', !settings.twoFactorEnabled);
              setShow2FAModal(false);
            }}>
              {settings.twoFactorEnabled ? (isRTL ? 'تعطيل' : 'Disable') : (isRTL ? 'تفعيل' : 'Enable')}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Settings;
