/**
 * Theme Settings Page
 * Allows users to change theme (Light/Dark/System)
 */

import React from 'react';
import { useTheme, ThemeToggle, ThemeSelector } from '../contexts/ThemeContext';
import { Sun, Moon, Monitor } from 'lucide-react';

const ThemeSettings = () => {
  const { theme, resolvedTheme, isLight, isDark, isSystem } = useTheme();

  return (
    <div className="min-h-screen bg-background-secondary p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-text-primary mb-2">
            إعدادات المظهر
          </h1>
          <p className="text-lg text-text-secondary">
            اختر المظهر المفضل لديك (فاتح، داكن، أو حسب النظام)
          </p>
        </div>

        {/* Current Theme Info */}
        <div className="bg-background-primary border border-border-base rounded-xl p-6 mb-6 shadow-md">
          <h2 className="text-2xl font-bold text-text-primary mb-4">
            المظهر الحالي
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center gap-3 p-4 bg-background-secondary rounded-lg">
              <div className={`p-3 rounded-lg ${isLight ? 'bg-primary-500 text-white' : 'bg-background-tertiary text-text-secondary'}`}>
                <Sun className="h-6 w-6" />
              </div>
              <div>
                <p className="font-semibold text-text-primary">فاتح</p>
                <p className="text-sm text-text-tertiary">
                  {isLight && !isSystem ? 'نشط' : 'غير نشط'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-4 bg-background-secondary rounded-lg">
              <div className={`p-3 rounded-lg ${isDark ? 'bg-primary-500 text-white' : 'bg-background-tertiary text-text-secondary'}`}>
                <Moon className="h-6 w-6" />
              </div>
              <div>
                <p className="font-semibold text-text-primary">داكن</p>
                <p className="text-sm text-text-tertiary">
                  {isDark && !isSystem ? 'نشط' : 'غير نشط'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-4 bg-background-secondary rounded-lg">
              <div className={`p-3 rounded-lg ${isSystem ? 'bg-primary-500 text-white' : 'bg-background-tertiary text-text-secondary'}`}>
                <Monitor className="h-6 w-6" />
              </div>
              <div>
                <p className="font-semibold text-text-primary">النظام</p>
                <p className="text-sm text-text-tertiary">
                  {isSystem ? 'نشط' : 'غير نشط'}
                </p>
              </div>
            </div>
          </div>

          <div className="mt-4 p-4 bg-background-tertiary rounded-lg">
            <p className="text-sm text-text-secondary">
              <span className="font-semibold">الإعداد:</span> {theme === 'light' ? 'فاتح' : theme === 'dark' ? 'داكن' : 'حسب النظام'}
            </p>
            <p className="text-sm text-text-secondary mt-1">
              <span className="font-semibold">المظهر الفعلي:</span> {resolvedTheme === 'light' ? 'فاتح' : 'داكن'}
            </p>
          </div>
        </div>

        {/* Theme Selector */}
        <div className="bg-background-primary border border-border-base rounded-xl p-6 mb-6 shadow-md">
          <h2 className="text-2xl font-bold text-text-primary mb-4">
            اختر المظهر
          </h2>
          
          <ThemeSelector className="mb-4" />
          
          <p className="text-sm text-text-tertiary mt-4">
            💡 <strong>نصيحة:</strong> اختر "النظام" لتطبيق مظهر نظام التشغيل تلقائياً
          </p>
        </div>

        {/* Quick Toggle */}
        <div className="bg-background-primary border border-border-base rounded-xl p-6 shadow-md">
          <h2 className="text-2xl font-bold text-text-primary mb-4">
            تبديل سريع
          </h2>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="font-semibold text-text-primary">
                تبديل بين الفاتح والداكن
              </p>
              <p className="text-sm text-text-tertiary">
                انقر على الزر للتبديل السريع
              </p>
            </div>
            
            <ThemeToggle className="scale-125" />
          </div>
        </div>

        {/* Preview Section */}
        <div className="mt-8 bg-background-primary border border-border-base rounded-xl p-6 shadow-md">
          <h2 className="text-2xl font-bold text-text-primary mb-4">
            معاينة المظهر
          </h2>
          
          <div className="space-y-4">
            {/* Buttons Preview */}
            <div>
              <p className="text-sm font-semibold text-text-primary mb-2">الأزرار:</p>
              <div className="flex gap-3 flex-wrap">
                <button className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-all">
                  زر أساسي
                </button>
                <button className="px-4 py-2 bg-background-secondary hover:bg-background-tertiary text-text-primary border border-border-base rounded-lg transition-all">
                  زر ثانوي
                </button>
                <button className="px-4 py-2 bg-danger-500 hover:bg-danger-600 text-white rounded-lg transition-all">
                  زر خطر
                </button>
              </div>
            </div>

            {/* Input Preview */}
            <div>
              <p className="text-sm font-semibold text-text-primary mb-2">حقول الإدخال:</p>
              <input
                type="text"
                placeholder="مثال على حقل إدخال"
                className="w-full px-4 py-3 rounded-lg border border-border-base bg-background-primary text-text-primary placeholder:text-text-tertiary focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {/* Card Preview */}
            <div>
              <p className="text-sm font-semibold text-text-primary mb-2">البطاقات:</p>
              <div className="bg-background-secondary border border-border-base rounded-lg p-4">
                <h3 className="text-lg font-bold text-text-primary mb-2">
                  عنوان البطاقة
                </h3>
                <p className="text-text-secondary">
                  هذا مثال على بطاقة في المظهر الحالي
                </p>
              </div>
            </div>

            {/* Text Preview */}
            <div>
              <p className="text-sm font-semibold text-text-primary mb-2">النصوص:</p>
              <div className="space-y-2">
                <p className="text-text-primary">نص أساسي (Primary Text)</p>
                <p className="text-text-secondary">نص ثانوي (Secondary Text)</p>
                <p className="text-text-tertiary">نص ثالثي (Tertiary Text)</p>
              </div>
            </div>
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-8 bg-info-500 bg-opacity-10 border border-info-500 rounded-xl p-6">
          <h3 className="text-lg font-bold text-info-500 mb-2">
            ℹ️ معلومات
          </h3>
          <ul className="space-y-2 text-sm text-text-secondary">
            <li>• يتم حفظ اختيارك تلقائياً في المتصفح</li>
            <li>• المظهر يطبق على جميع صفحات النظام</li>
            <li>• يمكنك التبديل في أي وقت</li>
            <li>• خيار "النظام" يتبع إعدادات نظام التشغيل</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ThemeSettings;

