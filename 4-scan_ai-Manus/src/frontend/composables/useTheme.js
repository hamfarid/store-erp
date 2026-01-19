/*
 * مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/composables/useTheme.js
 * الوصف: مكون قابل للاستخدام لإدارة سمات وألوان التطبيق
 * المؤلف: فريق تطوير Gaara ERP
 * تاريخ الإنشاء: 30 مايو 2025
 */

import { useStorage } from '@vueuse/core';
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

// تعريف السمات المتاحة
const themes = {
  gaaragroup: {
    name: 'Gaara Group',
    primaryColor: '#2c3e50',
    primaryDarkColor: '#1a2530',
    secondaryColor: '#e74c3c',
    secondaryDarkColor: '#c0392b',
    accentColor: '#3498db',
    successColor: '#2ecc71',
    warningColor: '#f39c12',
    dangerColor: '#e74c3c',
    infoColor: '#3498db',
    bgColor: '#f5f7fa',
    textColor: '#333333',
    textMutedColor: '#6c757d',
    borderColor: '#dee2e6',
    sidebarBgColor: '#ffffff',
    footerBgColor: '#ffffff',
    hoverBgColor: '#f8f9fa',
    activeBgColor: 'rgba(44, 62, 80, 0.1)',
    linkColor: '#2c3e50',
    linkHoverColor: '#1a2530',
    fontFamily: '"Cairo", "Roboto", sans-serif',
    logoPath: '/assets/logos/gaaragroup-logo.png',
    logoPathDark: '/assets/logos/gaaragroup-logo-dark.png',
    favicon: '/assets/favicon/gaaragroup-favicon.ico'
  },
  magseeds: {
    name: 'Mag Seeds',
    primaryColor: '#006838',
    primaryDarkColor: '#004d2a',
    secondaryColor: '#f7941d',
    secondaryDarkColor: '#d67b16',
    accentColor: '#8dc63f',
    successColor: '#8dc63f',
    warningColor: '#f7941d',
    dangerColor: '#ed1c24',
    infoColor: '#00a9e0',
    bgColor: '#f8f9f6',
    textColor: '#333333',
    textMutedColor: '#6c757d',
    borderColor: '#e2e8d8',
    sidebarBgColor: '#ffffff',
    footerBgColor: '#ffffff',
    hoverBgColor: '#f0f4eb',
    activeBgColor: 'rgba(0, 104, 56, 0.1)',
    linkColor: '#006838',
    linkHoverColor: '#004d2a',
    fontFamily: '"Tajawal", "Roboto", sans-serif',
    logoPath: '/assets/logos/magseeds-logo.png',
    logoPathDark: '/assets/logos/magseeds-logo-dark.png',
    favicon: '/assets/favicon/magseeds-favicon.ico'
  },
  custom: {
    name: 'Custom',
    primaryColor: '#007bff',
    primaryDarkColor: '#0069d9',
    secondaryColor: '#6c757d',
    secondaryDarkColor: '#5a6268',
    accentColor: '#28a745',
    successColor: '#28a745',
    warningColor: '#ffc107',
    dangerColor: '#dc3545',
    infoColor: '#17a2b8',
    bgColor: '#f5f7fa',
    textColor: '#333333',
    textMutedColor: '#6c757d',
    borderColor: '#dee2e6',
    sidebarBgColor: '#ffffff',
    footerBgColor: '#ffffff',
    hoverBgColor: '#f8f9fa',
    activeBgColor: 'rgba(0, 123, 255, 0.1)',
    linkColor: '#007bff',
    linkHoverColor: '#0056b3',
    fontFamily: '"Roboto", sans-serif',
    logoPath: '/assets/logos/default-logo.png',
    logoPathDark: '/assets/logos/default-logo-dark.png',
    favicon: '/assets/favicon/default-favicon.ico'
  }
};

export function useTheme() {
  const { locale } = useI18n();

  // استخدام التخزين المحلي للحفاظ على السمة المختارة
  const selectedTheme = useStorage('selectedTheme', 'gaaragroup');
  const isDarkMode = useStorage('isDarkMode', false);
  const customTheme = useStorage('customTheme', {});

  // حالة تحميل الشعار
  const isLogoLoaded = ref(false);

  // الحصول على السمة الحالية
  const currentTheme = computed(() => {
    if (selectedTheme.value === 'custom' && Object.keys(customTheme.value).length > 0) {
      return {
        ...themes.custom,
        ...customTheme.value
      };
    }
    return themes[selectedTheme.value] || themes.gaaragroup;
  });

  // الحصول على شعار العلامة التجارية
  const brandLogo = computed(() => {
    if (isDarkMode.value && currentTheme.value.logoPathDark) {
      return currentTheme.value.logoPathDark;
    }
    return currentTheme.value.logoPath;
  });

  // الحصول على اسم العلامة التجارية
  const brandName = computed(() => {
    return currentTheme.value.name;
  });

  // تغيير السمة
  const changeTheme = (themeName) => {
    if (themes[themeName] || themeName === 'custom') {
      selectedTheme.value = themeName;
      applyTheme();
    }
  };

  // تخصيص السمة
  const customizeTheme = (themeOptions) => {
    customTheme.value = {
      ...customTheme.value,
      ...themeOptions
    };

    if (selectedTheme.value !== 'custom') {
      selectedTheme.value = 'custom';
    }

    applyTheme();
  };

  // تبديل وضع الظلام
  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value;
    applyTheme();
  };

  // تطبيق السمة على الصفحة
  const applyTheme = () => {
    const theme = currentTheme.value;
    const root = document.documentElement;

    // تطبيق متغيرات CSS
    root.style.setProperty('--primary-color', theme.primaryColor);
    root.style.setProperty('--primary-dark-color', theme.primaryDarkColor);
    root.style.setProperty('--secondary-color', theme.secondaryColor);
    root.style.setProperty('--secondary-dark-color', theme.secondaryDarkColor);
    root.style.setProperty('--accent-color', theme.accentColor);
    root.style.setProperty('--success-color', theme.successColor);
    root.style.setProperty('--warning-color', theme.warningColor);
    root.style.setProperty('--danger-color', theme.dangerColor);
    root.style.setProperty('--info-color', theme.infoColor);

    if (isDarkMode.value) {
      // وضع الظلام
      root.style.setProperty('--bg-color', '#121212');
      root.style.setProperty('--text-color', '#e0e0e0');
      root.style.setProperty('--text-muted-color', '#a0a0a0');
      root.style.setProperty('--border-color', '#333333');
      root.style.setProperty('--sidebar-bg-color', '#1e1e1e');
      root.style.setProperty('--footer-bg-color', '#1e1e1e');
      root.style.setProperty('--hover-bg-color', '#2a2a2a');
      root.style.setProperty('--active-bg-color', 'rgba(255, 255, 255, 0.1)');
      document.body.classList.add('dark-mode');
    } else {
      // وضع النهار
      root.style.setProperty('--bg-color', theme.bgColor);
      root.style.setProperty('--text-color', theme.textColor);
      root.style.setProperty('--text-muted-color', theme.textMutedColor);
      root.style.setProperty('--border-color', theme.borderColor);
      root.style.setProperty('--sidebar-bg-color', theme.sidebarBgColor);
      root.style.setProperty('--footer-bg-color', theme.footerBgColor);
      root.style.setProperty('--hover-bg-color', theme.hoverBgColor);
      root.style.setProperty('--active-bg-color', theme.activeBgColor);
      document.body.classList.remove('dark-mode');
    }

    root.style.setProperty('--link-color', theme.linkColor);
    root.style.setProperty('--link-hover-color', theme.linkHoverColor);

    // تطبيق الخط
    root.style.setProperty('--font-family', theme.fontFamily);
    document.body.style.fontFamily = theme.fontFamily;

    // تحديث الأيقونة المفضلة
    const favicon = document.querySelector('link[rel="icon"]');
    if (favicon) {
      favicon.href = theme.favicon;
    }
  };

  // تحميل الخطوط المطلوبة
  const loadFonts = () => {
    const fontLinks = [
      { href: 'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap', id: 'roboto-font' },
      { href: 'https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap', id: 'cairo-font' },
      { href: 'https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap', id: 'tajawal-font' }
    ];

    fontLinks.forEach(font => {
      if (!document.getElementById(font.id)) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = font.href;
        link.id = font.id;
        document.head.appendChild(link);
      }
    });
  };

  // تحميل أيقونات Font Awesome
  const loadIcons = () => {
    if (!document.getElementById('fontawesome')) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';
      link.id = 'fontawesome';
      document.head.appendChild(link);
    }
  };

  // مراقبة تغيير اللغة لتحديث اتجاه الصفحة
  watch(locale, (newLocale) => {
    const dir = ['ar', 'he', 'ur'].includes(newLocale) ? 'rtl' : 'ltr';
    document.documentElement.dir = dir;
    document.documentElement.lang = newLocale;
  }, { immediate: true });

  // تهيئة السمة عند استخدام المكون
  const initTheme = () => {
    loadFonts();
    loadIcons();
    applyTheme();
  };

  // استدعاء التهيئة
  initTheme();

  return {
    currentTheme,
    selectedTheme,
    isDarkMode,
    brandLogo,
    brandName,
    isLogoLoaded,
    changeTheme,
    customizeTheme,
    toggleDarkMode,
    themes: Object.keys(themes)
  };
}
