<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/AppearanceSettings.vue
الوصف: مكون إعدادات المظهر والهوية البصرية
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="appearance-settings">
    <div class="page-header">
      <h1>{{ $t("settings.appearance.title") }}</h1>
      <p>{{ $t("settings.appearance.description") }}</p>
    </div>

    <div class="settings-sections">
      <!-- اختيار السمة -->
      <div class="card">
        <h2>{{ $t("settings.appearance.theme") }}</h2>
        <div class="theme-selector">
          <div 
            v-for="theme in availableThemes" 
            :key="theme"
            :class="['theme-option', { active: selectedTheme === theme }]"
            @click="selectTheme(theme)"
          >
            <div class="theme-preview" :class="theme">
              <div class="preview-header"></div>
              <div class="preview-sidebar"></div>
              <div class="preview-content"></div>
            </div>
            <div class="theme-name">{{ getThemeName(theme) }}</div>
          </div>
        </div>
      </div>

      <!-- وضع الظلام -->
      <div class="card">
        <h2>{{ $t("settings.appearance.displayMode") }}</h2>
        <div class="mode-selector">
          <div 
            :class="['mode-option', { active: !isDarkMode }]"
            @click="setDarkMode(false)"
          >
            <div class="mode-icon">
              <i class="fas fa-sun"></i>
            </div>
            <div class="mode-name">{{ $t("settings.appearance.lightMode") }}</div>
          </div>
          <div 
            :class="['mode-option', { active: isDarkMode }]"
            @click="setDarkMode(true)"
          >
            <div class="mode-icon">
              <i class="fas fa-moon"></i>
            </div>
            <div class="mode-name">{{ $t("settings.appearance.darkMode") }}</div>
          </div>
        </div>
      </div>

      <!-- تخصيص السمة -->
      <div class="card" v-if="selectedTheme === 'custom'">
        <h2>{{ $t("settings.appearance.customizeTheme") }}</h2>
        <div class="custom-theme-settings">
          <div class="form-group">
            <label for="themeName">{{ $t("settings.appearance.themeName") }}</label>
            <input id="themeName" type="text" v-model="customThemeSettings.name" />
          </div>
          
          <div class="color-section">
            <h3>{{ $t("settings.appearance.primaryColors") }}</h3>
            <div class="color-row">
              <div class="color-field">
                <label for="primaryColor">{{ $t("settings.appearance.primaryColor") }}</label>
                <div class="color-picker">
                  <input id="primaryColor" type="color" v-model="customThemeSettings.primaryColor" />
                  <span>{{ customThemeSettings.primaryColor }}</span>
                </div>
              </div>
              <div class="color-field">
                <label for="primaryDarkColor">{{ $t("settings.appearance.primaryDarkColor") }}</label>
                <div class="color-picker">
                  <input id="primaryDarkColor" type="color" v-model="customThemeSettings.primaryDarkColor" />
                  <span>{{ customThemeSettings.primaryDarkColor }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="color-section">
            <h3>{{ $t("settings.appearance.secondaryColors") }}</h3>
            <div class="color-row">
              <div class="color-field">
                <label for="secondaryColor">{{ $t("settings.appearance.secondaryColor") }}</label>
                <div class="color-picker">
                  <input id="secondaryColor" type="color" v-model="customThemeSettings.secondaryColor" />
                  <span>{{ customThemeSettings.secondaryColor }}</span>
                </div>
              </div>
              <div class="color-field">
                <label for="secondaryDarkColor">{{ $t("settings.appearance.secondaryDarkColor") }}</label>
                <div class="color-picker">
                  <input id="secondaryDarkColor" type="color" v-model="customThemeSettings.secondaryDarkColor" />
                  <span>{{ customThemeSettings.secondaryDarkColor }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="color-section">
            <h3>{{ $t("settings.appearance.accentColors") }}</h3>
            <div class="color-row">
              <div class="color-field">
                <label for="accentColor">{{ $t("settings.appearance.accentColor") }}</label>
                <div class="color-picker">
                  <input id="accentColor" type="color" v-model="customThemeSettings.accentColor" />
                  <span>{{ customThemeSettings.accentColor }}</span>
                </div>
              </div>
              <div class="color-field">
                <label for="successColor">{{ $t("settings.appearance.successColor") }}</label>
                <div class="color-picker">
                  <input id="successColor" type="color" v-model="customThemeSettings.successColor" />
                  <span>{{ customThemeSettings.successColor }}</span>
                </div>
              </div>
            </div>
            <div class="color-row">
              <div class="color-field">
                <label for="warningColor">{{ $t("settings.appearance.warningColor") }}</label>
                <div class="color-picker">
                  <input id="warningColor" type="color" v-model="customThemeSettings.warningColor" />
                  <span>{{ customThemeSettings.warningColor }}</span>
                </div>
              </div>
              <div class="color-field">
                <label for="dangerColor">{{ $t("settings.appearance.dangerColor") }}</label>
                <div class="color-picker">
                  <input id="dangerColor" type="color" v-model="customThemeSettings.dangerColor" />
                  <span>{{ customThemeSettings.dangerColor }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="color-section">
            <h3>{{ $t("settings.appearance.backgroundColors") }}</h3>
            <div class="color-row">
              <div class="color-field">
                <label for="bgColor">{{ $t("settings.appearance.bgColor") }}</label>
                <div class="color-picker">
                  <input id="bgColor" type="color" v-model="customThemeSettings.bgColor" />
                  <span>{{ customThemeSettings.bgColor }}</span>
                </div>
              </div>
              <div class="color-field">
                <label for="textColor">{{ $t("settings.appearance.textColor") }}</label>
                <div class="color-picker">
                  <input id="textColor" type="color" v-model="customThemeSettings.textColor" />
                  <span>{{ customThemeSettings.textColor }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="fontFamily">{{ $t("settings.appearance.fontFamily") }}</label>
            <select id="fontFamily" v-model="customThemeSettings.fontFamily">
              <option value='"Cairo", "Roboto", sans-serif'>Cairo</option>
              <option value='"Tajawal", "Roboto", sans-serif'>Tajawal</option>
              <option value='"Roboto", sans-serif'>Roboto</option>
              <option value='"Almarai", sans-serif'>Almarai</option>
              <option value='"Noto Sans Arabic", sans-serif'>Noto Sans Arabic</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="logoUpload">{{ $t("settings.appearance.logo") }}</label>
            <div class="logo-upload">
              <div class="current-logo" v-if="customThemeSettings.logoPreview">
                <img :src="customThemeSettings.logoPreview" alt="Logo" />
              </div>
              <div class="upload-buttons">
                <button class="btn btn-secondary" @click="triggerLogoUpload">
                  {{ $t("settings.appearance.uploadLogo") }}
                </button>
                <input 
                  id="logoUpload"
                  type="file" 
                  ref="logoInput" 
                  style="display: none" 
                  accept="image/*" 
                  @change="handleLogoUpload" 
                />
                <button 
                  class="btn btn-outline" 
                  @click="resetLogo" 
                  v-if="customThemeSettings.logoPreview"
                >
                  {{ $t("settings.appearance.resetLogo") }}
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="form-actions">
          <button class="btn btn-secondary" @click="resetCustomTheme">
            {{ $t("common.reset") }}
          </button>
          <button class="btn btn-primary" @click="saveCustomTheme">
            {{ $t("common.save") }}
          </button>
        </div>
      </div>

      <!-- معاينة السمة -->
      <div class="card">
        <h2>{{ $t("settings.appearance.preview") }}</h2>
        <div class="theme-preview-container">
          <div class="preview-header">
            <div class="preview-logo"></div>
            <div class="preview-nav"></div>
            <div class="preview-user"></div>
          </div>
          <div class="preview-body">
            <div class="preview-sidebar">
              <div class="preview-menu-item active"></div>
              <div class="preview-menu-item"></div>
              <div class="preview-menu-item"></div>
              <div class="preview-menu-item"></div>
            </div>
            <div class="preview-content">
              <div class="preview-title"></div>
              <div class="preview-card">
                <div class="preview-card-header"></div>
                <div class="preview-card-body">
                  <div class="preview-text-line"></div>
                  <div class="preview-text-line"></div>
                  <div class="preview-text-line short"></div>
                </div>
              </div>
              <div class="preview-buttons">
                <div class="preview-button primary"></div>
                <div class="preview-button secondary"></div>
                <div class="preview-button success"></div>
                <div class="preview-button danger"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Processing Modal -->
    <div class="modal" v-if="isProcessing">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ processingTitle }}</h2>
        </div>
        <div class="modal-body">
          <div class="loading-spinner"></div>
          <p>{{ processingMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useTheme } from "@/composables/useTheme";
import { useToast } from "@/composables/useToast";
import settingsService from "@/services/settingsService";
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useI18n } from "vue-i18n";

export default {
  name: "AppearanceSettings",
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    const { 
      currentTheme, 
      selectedTheme, 
      isDarkMode, 
      changeTheme, 
      customizeTheme, 
      toggleDarkMode,
      themes
    } = useTheme();
    
    // المراجع
    const logoInput = ref(null);
    
    // الحالة
    const isProcessing = ref(false);
    const processingTitle = ref("");
    const processingMessage = ref("");
    
    // السمات المتاحة
    const availableThemes = computed(() => themes);
    
    // إعدادات السمة المخصصة
    const customThemeSettings = reactive({
      name: "Custom",
      primaryColor: "#007bff",
      primaryDarkColor: "#0069d9",
      secondaryColor: "#6c757d",
      secondaryDarkColor: "#5a6268",
      accentColor: "#28a745",
      successColor: "#28a745",
      warningColor: "#ffc107",
      dangerColor: "#dc3545",
      infoColor: "#17a2b8",
      bgColor: "#f5f7fa",
      textColor: "#333333",
      textMutedColor: "#6c757d",
      borderColor: "#dee2e6",
      fontFamily: '"Cairo", "Roboto", sans-serif',
      logoPath: null,
      logoPreview: null
    });
    
    // جلب إعدادات المظهر
    const fetchAppearanceSettings = async () => {
      isProcessing.value = true;
      processingTitle.value = t("settings.appearance.loadingSettings");
      processingMessage.value = t("settings.appearance.loadingSettingsMessage");
      
      try {
        const response = await settingsService.getAppearanceSettings();
        
        // تحديث الإعدادات المحلية
        if (response.data.customTheme) {
          Object.assign(customThemeSettings, response.data.customTheme);
        }
        
      } catch (error) {
        console.error("Error fetching appearance settings:", error);
        showToast(t("settings.appearance.errorLoadingSettings"), "error");
      } finally {
        isProcessing.value = false;
      }
    };
    
    // اختيار سمة
    const selectTheme = (theme) => {
      changeTheme(theme);
    };
    
    // تعيين وضع الظلام
    const setDarkMode = (value) => {
      if (isDarkMode.value !== value) {
        toggleDarkMode();
      }
    };
    
    // الحصول على اسم السمة
    const getThemeName = (theme) => {
      switch (theme) {
        case "gaaragroup":
          return "Gaara Group";
        case "magseeds":
          return "Mag Seeds";
        case "custom":
          return customThemeSettings.name || "Custom";
        default:
          return theme;
      }
    };
    
    // تفعيل نافذة اختيار الشعار
    const triggerLogoUpload = () => {
      logoInput.value.click();
    };
    
    // معالجة تحميل الشعار
    const handleLogoUpload = (event) => {
      const file = event.target.files[0];
      if (!file) return;
      
      // التحقق من نوع الملف
      if (!file.type.match('image.*')) {
        showToast(t("settings.appearance.invalidImageType"), "error");
        return;
      }
      
      // التحقق من حجم الملف (الحد الأقصى 2 ميجابايت)
      if (file.size > 2 * 1024 * 1024) {
        showToast(t("settings.appearance.imageTooLarge"), "error");
        return;
      }
      
      // إنشاء معاينة للصورة
      const reader = new FileReader();
      reader.onload = (e) => {
        customThemeSettings.logoPreview = e.target.result;
        customThemeSettings.logoFile = file;
      };
      reader.readAsDataURL(file);
    };
    
    // إعادة تعيين الشعار
    const resetLogo = () => {
      customThemeSettings.logoPreview = null;
      customThemeSettings.logoFile = null;
      logoInput.value.value = "";
    };
    
    // إعادة تعيين السمة المخصصة
    const resetCustomTheme = () => {
      Object.assign(customThemeSettings, {
        name: "Custom",
        primaryColor: "#007bff",
        primaryDarkColor: "#0069d9",
        secondaryColor: "#6c757d",
        secondaryDarkColor: "#5a6268",
        accentColor: "#28a745",
        successColor: "#28a745",
        warningColor: "#ffc107",
        dangerColor: "#dc3545",
        infoColor: "#17a2b8",
        bgColor: "#f5f7fa",
        textColor: "#333333",
        textMutedColor: "#6c757d",
        borderColor: "#dee2e6",
        fontFamily: '"Cairo", "Roboto", sans-serif',
        logoPreview: null,
        logoFile: null
      });
      
      if (logoInput.value) {
        logoInput.value.value = "";
      }
    };
    
    // حفظ السمة المخصصة
    const saveCustomTheme = async () => {
      isProcessing.value = true;
      processingTitle.value = t("settings.appearance.savingSettings");
      processingMessage.value = t("settings.appearance.savingSettingsMessage");
      
      try {
        // تحميل الشعار إذا تم تحديده
        let logoPath = customThemeSettings.logoPath;
        
        if (customThemeSettings.logoFile) {
          const formData = new FormData();
          formData.append("logo", customThemeSettings.logoFile);
          
          const uploadResponse = await settingsService.uploadLogo(formData);
          logoPath = uploadResponse.data.path;
        }
        
        // تحديث السمة المخصصة
        const themeData = {
          ...customThemeSettings,
          logoPath
        };
        
        delete themeData.logoFile;
        delete themeData.logoPreview;
        
        // حفظ السمة المخصصة
        await settingsService.saveAppearanceSettings({
          theme: "custom",
          darkMode: isDarkMode.value,
          customTheme: themeData
        });
        
        // تطبيق السمة المخصصة
        customizeTheme(themeData);
        
        showToast(t("settings.appearance.settingsSaved"), "success");
      } catch (error) {
        console.error("Error saving appearance settings:", error);
        showToast(t("settings.appearance.errorSavingSettings"), "error");
      } finally {
        isProcessing.value = false;
      }
    };
    
    // مراقبة تغيير السمة
    watch(selectedTheme, (newTheme) => {
      if (newTheme === "custom") {
        // تحديث إعدادات السمة المخصصة من السمة الحالية
        const theme = currentTheme.value;
        Object.assign(customThemeSettings, {
          name: theme.name || "Custom",
          primaryColor: theme.primaryColor,
          primaryDarkColor: theme.primaryDarkColor,
          secondaryColor: theme.secondaryColor,
          secondaryDarkColor: theme.secondaryDarkColor,
          accentColor: theme.accentColor,
          successColor: theme.successColor,
          warningColor: theme.warningColor,
          dangerColor: theme.dangerColor,
          infoColor: theme.infoColor,
          bgColor: theme.bgColor,
          textColor: theme.textColor,
          textMutedColor: theme.textMutedColor,
          borderColor: theme.borderColor,
          fontFamily: theme.fontFamily,
          logoPath: theme.logoPath
        });
      }
    });
    
    // دورة الحياة
    onMounted(async () => {
      await fetchAppearanceSettings();
    });
    
    return {
      selectedTheme,
      isDarkMode,
      availableThemes,
      customThemeSettings,
      isProcessing,
      processingTitle,
      processingMessage,
      logoInput,
      selectTheme,
      setDarkMode,
      getThemeName,
      triggerLogoUpload,
      handleLogoUpload,
      resetLogo,
      resetCustomTheme,
      saveCustomTheme
    };
  }
};
</script>

<style scoped>
.appearance-settings {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  margin-bottom: 0.5rem;
  color: var(--primary-color, #007bff);
}

.settings-sections {
  display: grid;
  gap: 2rem;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
}

.card h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: var(--primary-color, #007bff);
  font-size: 1.5rem;
}

/* اختيار السمة */
.theme-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.theme-option {
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.theme-option:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.theme-option.active {
  box-shadow: 0 0 0 2px var(--primary-color, #007bff);
}

.theme-preview {
  height: 150px;
  position: relative;
  overflow: hidden;
}

.theme-preview.gaaragroup .preview-header {
  background-color: #2c3e50;
}

.theme-preview.gaaragroup .preview-sidebar {
  background-color: #ffffff;
  border-right: 1px solid #dee2e6;
}

.theme-preview.gaaragroup .preview-content {
  background-color: #f5f7fa;
}

.theme-preview.magseeds .preview-header {
  background-color: #006838;
}

.theme-preview.magseeds .preview-sidebar {
  background-color: #ffffff;
  border-right: 1px solid #e2e8d8;
}

.theme-preview.magseeds .preview-content {
  background-color: #f8f9f6;
}

.theme-preview.custom .preview-header {
  background-color: var(--primary-color, #007bff);
}

.theme-preview.custom .preview-sidebar {
  background-color: var(--sidebar-bg-color, #ffffff);
  border-right: 1px solid var(--border-color, #dee2e6);
}

.theme-preview.custom .preview-content {
  background-color: var(--bg-color, #f5f7fa);
}

.preview-header {
  background-color: v-bind('previewTheme.headerBg');
  color: v-bind('previewTheme.headerText');
  padding: 1rem;
  border-bottom: 1px solid v-bind('previewTheme.border');
}

.preview-sidebar {
  background-color: v-bind('previewTheme.sidebarBg');
  color: v-bind('previewTheme.sidebarText');
  width: 250px;
  border-right: 1px solid v-bind('previewTheme.border');
}

.preview-content {
  background-color: v-bind('previewTheme.contentBg');
  color: v-bind('previewTheme.contentText');
  padding: 1rem;
}

.theme-name {
  padding: 0.75rem;
  text-align: center;
  font-weight: 500;
  background-color: white;
}

/* اختيار الوضع */
.mode-selector {
  display: flex;
  gap: 1.5rem;
}

.mode-option {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: #f8f9fa;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.mode-option:hover {
  background-color: #f0f0f0;
  transform: translateY(-3px);
}

.mode-option.active {
  background-color: rgba(0, 123, 255, 0.1);
  border: 2px solid var(--primary-color, #007bff);
}

.mode-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.mode-option:first-child .mode-icon {
  color: #f39c12;
}

.mode-option:last-child .mode-icon {
  color: #3498db;
}

.mode-name {
  font-weight: 500;
}

/* تخصيص السمة */
.custom-theme-settings {
  display: grid;
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input[type="text"],
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.color-section {
  margin-bottom: 1.5rem;
}

.color-section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: var(--text-color, #333);
}

.color-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.color-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.color-picker {
  display: flex;
  align-items: center;
}

.color-picker input[type="color"] {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 4px;
  margin-right: 0.5rem;
  cursor: pointer;
}

.logo-upload {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.current-logo {
  width: 100px;
  height: 100px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.current-logo img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.upload-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

/* معاينة السمة */
.theme-preview-container {
  height: 300px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.preview-logo {
  width: 100px;
  height: 30px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.preview-nav {
  flex: 1;
  margin: 0 1rem;
}

.preview-user {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
}

.preview-body {
  display: flex;
  height: calc(100% - 50px);
}

.preview-sidebar {
  width: 60px;
  background-color: var(--sidebar-bg-color, #fff);
  border-right: 1px solid var(--border-color, #eee);
  padding: 1rem 0;
}

.preview-menu-item {
  width: 40px;
  height: 40px;
  margin: 0 auto 0.5rem;
  border-radius: 4px;
  background-color: #f0f0f0;
}

.preview-menu-item.active {
  background-color: var(--active-bg-color, rgba(0, 123, 255, 0.1));
  border-left: 3px solid var(--primary-color, #007bff);
}

.preview-title {
  height: 30px;
  width: 200px;
  background-color: #e0e0e0;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.preview-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 1rem;
}

.preview-card-header {
  height: 40px;
  background-color: #f8f9fa;
  border-bottom: 1px solid var(--border-color, #eee);
}

.preview-card-body {
  padding: 1rem;
}

.preview-text-line {
  height: 12px;
  background-color: #e0e0e0;
  border-radius: 2px;
  margin-bottom: 0.5rem;
}

.preview-text-line.short {
  width: 60%;
}

.preview-buttons {
  display: flex;
  gap: 0.5rem;
}

.preview-button {
  width: 80px;
  height: 30px;
  border-radius: 4px;
}

.preview-button.primary {
  background-color: var(--primary-color, #007bff);
}

.preview-button.secondary {
  background-color: var(--secondary-color, #6c757d);
}

.preview-button.success {
  background-color: var(--success-color, #28a745);
}

.preview-button.danger {
  background-color: var(--danger-color, #dc3545);
}

/* أزرار */
.btn {
  cursor: pointer;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: var(--primary-color, #007bff);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark-color, #0069d9);
}

.btn-secondary {
  background-color: var(--secondary-color, #6c757d);
  color: white;
}

.btn-secondary:hover {
  background-color: var(--secondary-dark-color, #5a6268);
}

.btn-outline {
  background-color: transparent;
  border: 1px solid var(--border-color, #ddd);
  color: var(--text-color, #333);
}

.btn-outline:hover {
  background-color: #f8f9fa;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ddd;
}

.modal-body {
  padding: 20px;
  text-align: center;
}

/* Loading spinner */
.loading-spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-radius: 50%;
  border-top: 5px solid var(--primary-color, #007bff);
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Responsive styles */
@media (max-width: 768px) {
  .color-row {
    grid-template-columns: 1fr;
  }
  
  .theme-selector {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  
  .mode-selector {
    flex-direction: column;
  }
  
  .logo-upload {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
