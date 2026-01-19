<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/common/LanguageSwitcher.vue
الوصف: مكون تبديل اللغة لدعم تعدد اللغات في النظام
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
-->

<template>
  <div class="language-switcher">
    <div class="language-dropdown">
      <button class="language-button" @click="toggleDropdown">
        <i class="fas fa-globe"></i>
        <span class="current-language">{{ currentLanguageLabel }}</span>
        <i class="fas fa-chevron-down"></i>
      </button>
      <div class="language-options" v-if="showDropdown">
        <div 
          v-for="lang in availableLanguages" 
          :key="lang.code" 
          class="language-option"
          :class="{ 'active': currentLanguage === lang.code }"
          @click="changeLanguage(lang.code)"
        >
          <span class="language-flag">{{ lang.flag }}</span>
          <span class="language-name">{{ lang.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'LanguageSwitcher',
  setup() {
    const { locale } = useI18n();
    const { showToast } = useToast();
    
    const currentLanguage = computed(() => locale.value);
    const showDropdown = ref(false);
    
    const availableLanguages = [
      { code: 'ar', name: 'العربية', flag: '🇸🇦' },
      { code: 'en', name: 'English', flag: '🇬🇧' }
    ];
    
    const currentLanguageLabel = computed(() => {
      const lang = availableLanguages.find(lang => lang.code === currentLanguage.value);
      return lang ? lang.name : '';
    });
    
    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value;
    };
    
    const changeLanguage = (langCode) => {
      if (langCode !== currentLanguage.value) {
        // تغيير اتجاه الصفحة حسب اللغة
        document.documentElement.dir = langCode === 'ar' ? 'rtl' : 'ltr';
        
        // تغيير اللغة
        locale.value = langCode;
        
        // حفظ اللغة المفضلة في التخزين المحلي
        localStorage.setItem('preferredLanguage', langCode);
        
        // إظهار رسالة نجاح
        const message = langCode === 'ar' ? 'تم تغيير اللغة إلى العربية' : 'Language changed to English';
        showToast(message, 'success');
      }
      
      // إغلاق القائمة المنسدلة
      showDropdown.value = false;
    };
    
    // إغلاق القائمة المنسدلة عند النقر خارجها
    const handleClickOutside = (event) => {
      const dropdown = document.querySelector('.language-dropdown');
      if (dropdown && !dropdown.contains(event.target)) {
        showDropdown.value = false;
      }
    };
    
    onMounted(() => {
      // تحميل اللغة المفضلة من التخزين المحلي
      const preferredLanguage = localStorage.getItem('preferredLanguage');
      if (preferredLanguage && preferredLanguage !== currentLanguage.value) {
        changeLanguage(preferredLanguage);
      }
      
      // إضافة مستمع للنقر خارج القائمة المنسدلة
      document.addEventListener('click', handleClickOutside);
    });
    
    onUnmounted(() => {
      // إزالة مستمع النقر عند تدمير المكون
      document.removeEventListener('click', handleClickOutside);
    });
    
    return {
      currentLanguage,
      currentLanguageLabel,
      availableLanguages,
      showDropdown,
      toggleDropdown,
      changeLanguage
    };
  }
};
</script>

<style scoped>
.language-switcher {
  position: relative;
  display: inline-block;
}

.language-button {
  display: flex;
  align-items: center;
  background-color: transparent;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 6px 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.language-button:hover {
  background-color: #f5f5f5;
}

.language-button i {
  margin-right: 6px;
}

.language-button i.fa-chevron-down {
  margin-left: 6px;
  margin-right: 0;
  font-size: 0.8em;
}

.current-language {
  font-weight: 500;
}

.language-options {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 1000;
  min-width: 150px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-top: 5px;
}

.language-option {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.language-option:hover {
  background-color: #f5f5f5;
}

.language-option.active {
  background-color: #e6f7ff;
  font-weight: 500;
}

.language-flag {
  margin-right: 8px;
  font-size: 1.2em;
}

/* تعديلات للغة العربية */
:global([dir="rtl"]) .language-button i {
  margin-right: 0;
  margin-left: 6px;
}

:global([dir="rtl"]) .language-button i.fa-chevron-down {
  margin-right: 6px;
  margin-left: 0;
}

:global([dir="rtl"]) .language-options {
  right: auto;
  left: 0;
}

:global([dir="rtl"]) .language-flag {
  margin-right: 0;
  margin-left: 8px;
}
</style>
