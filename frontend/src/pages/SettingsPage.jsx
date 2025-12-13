/**
 * Settings Page
 */

import React, { useState } from 'react';
import {
  Settings, Building2, Globe, Bell, Shield, Palette, Database,
  Mail, Printer, CreditCard, Save, ChevronLeft
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const SettingSection = ({ icon: Icon, title, description, children }) => (
  <div className="card-standard">
    <div className="card-header">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center shadow-lg">
          <Icon className="text-white" size={22} />
        </div>
        <div>
          <h3 className="card-title">{title}</h3>
          <p className="text-gray-500 text-sm mt-1">{description}</p>
        </div>
      </div>
    </div>
    <div className="card-content">
      {children}
    </div>
  </div>
);

const Toggle = ({ enabled, onChange, label }) => (
  <label className="flex items-center justify-between cursor-pointer">
    <span className="text-gray-700">{label}</span>
    <div className="relative">
      <input type="checkbox" checked={enabled} onChange={onChange} className="sr-only" />
      <div className={`w-12 h-6 rounded-full transition-colors ${enabled ? 'bg-teal-500' : 'bg-gray-200'}`}>
        <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${enabled ? 'translate-x-6' : 'translate-x-0.5'}`} />
      </div>
    </div>
  </label>
);

const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    darkMode: false,
    notifications: true,
    emailAlerts: true,
    autoBackup: true,
    twoFactor: false,
  });

  const tabs = [
    { id: 'general', label: 'عام', icon: Settings },
    { id: 'company', label: 'بيانات الشركة', icon: Building2 },
    { id: 'notifications', label: 'الإشعارات', icon: Bell },
    { id: 'security', label: 'الأمان', icon: Shield },
    { id: 'appearance', label: 'المظهر', icon: Palette },
    { id: 'integrations', label: 'التكاملات', icon: Globe },
    { id: 'backup', label: 'النسخ الاحتياطي', icon: Database },
  ];

  return (
    <div className="page-container" dir="rtl">
      <div className="page-header">
        <div>
          <h1 className="page-title">الإعدادات</h1>
          <p className="text-gray-500 mt-1">إدارة إعدادات النظام</p>
        </div>
        <div className="page-actions">
          <Button variant="primary" icon={Save}>حفظ التغييرات</Button>
        </div>
      </div>

      <div className="flex gap-8">
        {/* Sidebar */}
        <div className="w-64 shrink-0">
          <nav className="bg-white rounded-2xl border border-gray-100 p-3 space-y-1">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-teal-50 text-teal-700'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <tab.icon size={18} />
                {tab.label}
                <ChevronLeft size={16} className="mr-auto opacity-50" />
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="flex-1 space-y-6">
          {activeTab === 'general' && (
            <>
              <SettingSection icon={Globe} title="اللغة والمنطقة" description="إعدادات اللغة والتوقيت">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label">اللغة</label>
                    <select className="form-input-standard">
                      <option>العربية</option>
                      <option>English</option>
                    </select>
                  </div>
                  <div>
                    <label className="form-label">المنطقة الزمنية</label>
                    <select className="form-input-standard">
                      <option>الرياض (GMT+3)</option>
                      <option>جدة (GMT+3)</option>
                    </select>
                  </div>
                </div>
              </SettingSection>

              <SettingSection icon={CreditCard} title="العملة" description="إعدادات العملة الافتراضية">
                <div className="form-grid form-grid-2">
                  <div className="form-group">
                    <label className="form-label">العملة</label>
                    <select className="form-input-standard">
                      <option>ريال سعودي (SAR)</option>
                      <option>دولار أمريكي (USD)</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">تنسيق الأرقام</label>
                    <select className="form-input-standard">
                      <option>1,234.56</option>
                      <option>1.234,56</option>
                    </select>
                  </div>
                </div>
              </SettingSection>
            </>
          )}

          {activeTab === 'company' && (
            <SettingSection icon={Building2} title="بيانات الشركة" description="معلومات الشركة الأساسية">
              <div className="form-container">
                <div className="form-group">
                  <label className="form-label">اسم الشركة</label>
                  <input type="text" defaultValue="شركة التقنية للتجارة" className="form-input-standard" />
                </div>
                <div className="form-grid form-grid-2">
                  <div className="form-group">
                    <label className="form-label">السجل التجاري</label>
                    <input type="text" defaultValue="1234567890" className="form-input-standard" />
                  </div>
                  <div className="form-group">
                    <label className="form-label">الرقم الضريبي</label>
                    <input type="text" defaultValue="300012345600003" className="form-input-standard" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">العنوان</label>
                  <textarea rows={3} defaultValue="الرياض، حي العليا، شارع الملك فهد" className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500" />
                </div>
              </div>
            </SettingSection>
          )}

          {activeTab === 'notifications' && (
            <SettingSection icon={Bell} title="إعدادات الإشعارات" description="تحكم في الإشعارات التي تصلك">
              <div className="space-y-4">
                <Toggle label="إشعارات النظام" enabled={settings.notifications} onChange={() => setSettings({...settings, notifications: !settings.notifications})} />
                <Toggle label="إشعارات البريد الإلكتروني" enabled={settings.emailAlerts} onChange={() => setSettings({...settings, emailAlerts: !settings.emailAlerts})} />
                <Toggle label="تنبيهات المخزون المنخفض" enabled={true} onChange={() => {}} />
                <Toggle label="تنبيهات الفواتير المستحقة" enabled={true} onChange={() => {}} />
              </div>
            </SettingSection>
          )}

          {activeTab === 'security' && (
            <SettingSection icon={Shield} title="إعدادات الأمان" description="حماية حسابك وبياناتك">
              <div className="space-y-4">
                <Toggle label="المصادقة الثنائية (2FA)" enabled={settings.twoFactor} onChange={() => setSettings({...settings, twoFactor: !settings.twoFactor})} />
                <div className="pt-4 border-t border-gray-100">
                  <Button variant="secondary">تغيير كلمة المرور</Button>
                </div>
              </div>
            </SettingSection>
          )}

          {activeTab === 'appearance' && (
            <SettingSection icon={Palette} title="المظهر" description="تخصيص مظهر التطبيق">
              <div className="space-y-4">
                <Toggle label="الوضع الداكن" enabled={settings.darkMode} onChange={() => setSettings({...settings, darkMode: !settings.darkMode})} />
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">لون التمييز</label>
                  <div className="flex gap-2">
                    {['bg-teal-500', 'bg-blue-500', 'bg-purple-500', 'bg-rose-500', 'bg-amber-500'].map(color => (
                      <button key={color} className={`w-8 h-8 rounded-full ${color} ring-2 ring-offset-2 ring-transparent hover:ring-gray-300`} />
                    ))}
                  </div>
                </div>
              </div>
            </SettingSection>
          )}

          {activeTab === 'backup' && (
            <SettingSection icon={Database} title="النسخ الاحتياطي" description="إدارة النسخ الاحتياطية">
              <div className="space-y-4">
                <Toggle label="النسخ الاحتياطي التلقائي" enabled={settings.autoBackup} onChange={() => setSettings({...settings, autoBackup: !settings.autoBackup})} />
                <div className="flex gap-3">
                  <Button variant="primary">إنشاء نسخة احتياطية</Button>
                  <Button variant="secondary">استعادة من نسخة</Button>
                </div>
              </div>
            </SettingSection>
          )}
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;

