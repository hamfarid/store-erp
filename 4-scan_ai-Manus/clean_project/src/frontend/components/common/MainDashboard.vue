<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/common/MainDashboard.vue
الوصف: مكون الصفحة الرئيسية المعاد تنظيمها مع فصل الإعدادات عن المديولات
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="main-dashboard" :class="{ 'rtl-support': isRtl }">
    <div class="dashboard-header">
      <div class="brand-container">
        <img :src="brandLogo" alt="شعار الشركة" class="brand-logo" />
        <h1 class="brand-name">{{ brandName }}</h1>
      </div>
      <div class="header-actions">
        <div class="search-container">
          <input 
            type="text" 
            v-model="searchQuery" 
            :placeholder="$t('dashboard.searchModules')" 
            @input="filterModules"
          />
          <i class="fas fa-search"></i>
        </div>
        <div class="user-info" @click="toggleUserMenu">
          <div class="user-avatar">
            <img v-if="userAvatar" :src="userAvatar" :alt="userName" />
            <i v-else class="fas fa-user"></i>
          </div>
          <div class="user-name">{{ userName }}</div>
          <i class="fas fa-chevron-down"></i>
          
          <!-- User Menu -->
          <div class="user-menu" v-if="showUserMenu">
            <div class="menu-item" @click="navigateTo('/profile')">
              <i class="fas fa-user-circle"></i>
              <span>{{ $t('dashboard.profile') }}</span>
            </div>
            <div class="menu-item" @click="navigateTo('/settings')">
              <i class="fas fa-cog"></i>
              <span>{{ $t('dashboard.settings') }}</span>
            </div>
            <div class="menu-item" @click="changeEntity">
              <i class="fas fa-exchange-alt"></i>
              <span>{{ $t('dashboard.changeEntity') }}</span>
            </div>
            <div class="menu-divider"></div>
            <div class="menu-item" @click="logout">
              <i class="fas fa-sign-out-alt"></i>
              <span>{{ $t('dashboard.logout') }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="sidebar" :class="{ 'collapsed': sidebarCollapsed }">
        <div class="sidebar-toggle" @click="toggleSidebar">
          <i :class="sidebarCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
        </div>
        
        <div class="sidebar-sections">
          <!-- الأقسام الرئيسية -->
          <div class="sidebar-section">
            <div class="section-title">{{ $t('dashboard.mainSections') }}</div>
            <div 
              v-for="section in mainSections" 
              :key="section.id"
              :class="['section-item', { active: activeSection === section.id }]"
              @click="setActiveSection(section.id)"
            >
              <i :class="section.icon"></i>
              <span v-if="!sidebarCollapsed">{{ $t(section.name) }}</span>
            </div>
          </div>
          
          <!-- المديولات -->
          <div class="sidebar-section">
            <div class="section-title">{{ $t('dashboard.modules') }}</div>
            <div 
              v-for="module in visibleModules" 
              :key="module.id"
              :class="['section-item', { active: activeModule === module.id }]"
              @click="setActiveModule(module.id)"
            >
              <i :class="module.icon"></i>
              <span v-if="!sidebarCollapsed">{{ $t(module.name) }}</span>
              <span v-if="!sidebarCollapsed && module.status === 'new'" class="status-badge new">
                {{ $t('dashboard.new') }}
              </span>
            </div>
          </div>
          
          <!-- الإعدادات -->
          <div class="sidebar-section">
            <div class="section-title">{{ $t('dashboard.settings') }}</div>
            <div 
              v-for="setting in settingsItems" 
              :key="setting.id"
              :class="['section-item', { active: activeSetting === setting.id }]"
              @click="setActiveSetting(setting.id)"
            >
              <i :class="setting.icon"></i>
              <span v-if="!sidebarCollapsed">{{ $t(setting.name) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="main-content">
        <!-- عرض القسم النشط -->
        <div v-if="activeSection && !activeModule && !activeSetting" class="content-section">
          <component 
            :is="getActiveComponent()" 
            :key="activeSection"
          ></component>
        </div>
        
        <!-- عرض المديول النشط -->
        <div v-if="activeModule && !activeSection && !activeSetting" class="content-section">
          <component 
            :is="getActiveComponent()" 
            :key="activeModule"
          ></component>
        </div>
        
        <!-- عرض الإعداد النشط -->
        <div v-if="activeSetting && !activeSection && !activeModule" class="content-section">
          <component 
            :is="getActiveComponent()" 
            :key="activeSetting"
          ></component>
        </div>
      </div>
    </div>

    <div class="dashboard-footer">
      <div class="footer-info">
        <span>{{ brandName }} &copy; {{ currentYear }}</span>
        <span>{{ $t('dashboard.version') }}: {{ appVersion }}</span>
      </div>
      <div class="footer-links">
        <a href="#" @click.prevent="showHelp">{{ $t('dashboard.help') }}</a>
        <a href="#" @click.prevent="showAbout">{{ $t('dashboard.about') }}</a>
        <a href="#" @click.prevent="showPrivacyPolicy">{{ $t('dashboard.privacyPolicy') }}</a>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuth } from '@/composables/useAuth';
import { useTheme } from '@/composables/useTheme';
import { useToast } from '@/composables/useToast';
import dashboardService from '@/services/dashboardService';
import { computed, defineAsyncComponent, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

// تعريف الأقسام الرئيسية
const mainSectionsList = [
  { id: 'overview', name: 'dashboard.sections.overview', icon: 'fas fa-home', component: 'OverviewDashboard' },
  { id: 'analytics', name: 'dashboard.sections.analytics', icon: 'fas fa-chart-bar', component: 'AnalyticsDashboard' },
  { id: 'reports', name: 'dashboard.sections.reports', icon: 'fas fa-file-alt', component: 'ReportsDashboard' },
  { id: 'notifications', name: 'dashboard.sections.notifications', icon: 'fas fa-bell', component: 'NotificationCenter' },
];

// تعريف عناصر الإعدادات
const settingsItemsList = [
  { id: 'user_settings', name: 'dashboard.settings.user', icon: 'fas fa-user-cog', component: 'UserSettings' },
  { id: 'system_settings', name: 'dashboard.settings.system', icon: 'fas fa-cogs', component: 'SystemSettings' },
  { id: 'appearance', name: 'dashboard.settings.appearance', icon: 'fas fa-palette', component: 'AppearanceSettings' },
  { id: 'permissions', name: 'dashboard.settings.permissions', icon: 'fas fa-user-shield', component: 'PermissionsDashboard' },
  { id: 'backup_restore', name: 'dashboard.settings.backupRestore', icon: 'fas fa-database', component: 'BackupRestoreSettings' },
];

export default {
  name: 'MainDashboard',
  components: {
    // تحميل المكونات الرئيسية
    OverviewDashboard: defineAsyncComponent(() => import('@/components/dashboard/OverviewDashboard.vue')),
    AnalyticsDashboard: defineAsyncComponent(() => import('@/components/dashboard/AnalyticsDashboard.vue')),
    ReportsDashboard: defineAsyncComponent(() => import('@/components/dashboard/ReportsDashboard.vue')),
    NotificationCenter: defineAsyncComponent(() => import('@/components/dashboard/NotificationCenter.vue')),
    
    // تحميل مكونات الإعدادات
    UserSettings: defineAsyncComponent(() => import('@/components/settings/UserSettings.vue')),
    SystemSettings: defineAsyncComponent(() => import('@/components/settings/SystemSettings.vue')),
    AppearanceSettings: defineAsyncComponent(() => import('@/components/settings/AppearanceSettings.vue')),
    PermissionsDashboard: defineAsyncComponent(() => import('@/components/permissions/PermissionsDashboard.vue')),
    BackupRestoreSettings: defineAsyncComponent(() => import('@/components/settings/BackupRestoreSettings.vue')),
    
    // مكونات المديولات سيتم تحميلها ديناميكياً
  },
  setup() {
    const { t, locale } = useI18n();
    const router = useRouter();
    const { showToast } = useToast();
    const { brandLogo, brandName } = useTheme();
    const { user, logout: authLogout } = useAuth();
    
    // الحالة
    const searchQuery = ref('');
    const sidebarCollapsed = ref(false);
    const showUserMenu = ref(false);
    const activeSection = ref('overview'); // القسم النشط افتراضياً
    const activeModule = ref(null);
    const activeSetting = ref(null);
    const modules = ref([]);
    const filteredModules = ref([]);
    
    // الخصائص المحسوبة
    const isRtl = computed(() => locale.value === 'ar');
    const userName = computed(() => user.value?.name || 'المستخدم');
    const userAvatar = computed(() => user.value?.avatar || null);
    const appVersion = computed(() => import.meta.env.VITE_APP_VERSION || '1.0.0');
    const currentYear = computed(() => new Date().getFullYear());
    
    const mainSections = computed(() => mainSectionsList);
    const settingsItems = computed(() => settingsItemsList);
    
    const visibleModules = computed(() => {
      if (!searchQuery.value) return filteredModules.value;
      
      const query = searchQuery.value.toLowerCase();
      return filteredModules.value.filter(module => 
        t(module.name).toLowerCase().includes(query) || 
        (module.description && t(module.description).toLowerCase().includes(query))
      );
    });
    
    // جلب المديولات
    const fetchModules = async () => {
      try {
        const response = await dashboardService.getModules();
        modules.value = response.data.map(module => ({
          ...module,
          icon: module.icon || 'fas fa-puzzle-piece' // أيقونة افتراضية
        }));
        filteredModules.value = [...modules.value];
      } catch (error) {
        console.error('Error fetching modules:', error);
        showToast(t('dashboard.errorLoadingModules'), 'error');
      }
    };
    
    // تصفية المديولات
    const filterModules = () => {
      if (!searchQuery.value) {
        filteredModules.value = [...modules.value];
        return;
      }
      
      const query = searchQuery.value.toLowerCase();
      filteredModules.value = modules.value.filter(module => 
        t(module.name).toLowerCase().includes(query) || 
        (module.description && t(module.description).toLowerCase().includes(query))
      );
    };
    
    // تبديل حالة الشريط الجانبي
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value;
      localStorage.setItem('sidebarCollapsed', sidebarCollapsed.value);
    };
    
    // تبديل قائمة المستخدم
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value;
    };
    
    // تعيين القسم النشط
    const setActiveSection = (sectionId) => {
      activeSection.value = sectionId;
      activeModule.value = null;
      activeSetting.value = null;
    };
    
    // تعيين المديول النشط
    const setActiveModule = (moduleId) => {
      activeModule.value = moduleId;
      activeSection.value = null;
      activeSetting.value = null;
    };
    
    // تعيين الإعداد النشط
    const setActiveSetting = (settingId) => {
      activeSetting.value = settingId;
      activeSection.value = null;
      activeModule.value = null;
    };
    
    // الحصول على المكون النشط
    const getActiveComponent = () => {
      if (activeSection.value) {
        const section = mainSectionsList.find(s => s.id === activeSection.value);
        return section ? section.component : null;
      }
      
      if (activeModule.value) {
        const module = modules.value.find(m => m.id === activeModule.value);
        return module ? module.component : null;
      }
      
      if (activeSetting.value) {
        const setting = settingsItemsList.find(s => s.id === activeSetting.value);
        return setting ? setting.component : null;
      }
      
      return null;
    };
    
    // تغيير الكيان (قاعدة البيانات، الشركة، الدولة)
    const changeEntity = () => {
      router.push('/entity-selector');
    };
    
    // تسجيل الخروج
    const logout = async () => {
      try {
        await authLogout();
        router.push('/login');
      } catch (error) {
        console.error('Error during logout:', error);
        showToast(t('dashboard.errorDuringLogout'), 'error');
      }
    };
    
    // التنقل إلى مسار
    const navigateTo = (path) => {
      router.push(path);
    };
    
    // عرض المساعدة
    const showHelp = () => {
      // تنفيذ منطق عرض المساعدة
    };
    
    // عرض معلومات حول التطبيق
    const showAbout = () => {
      // تنفيذ منطق عرض معلومات حول التطبيق
    };
    
    // عرض سياسة الخصوصية
    const showPrivacyPolicy = () => {
      // تنفيذ منطق عرض سياسة الخصوصية
    };
    
    // إغلاق قائمة المستخدم عند النقر خارجها
    const handleClickOutside = (event) => {
      const userInfo = document.querySelector('.user-info');
      if (userInfo && !userInfo.contains(event.target) && showUserMenu.value) {
        showUserMenu.value = false;
      }
    };
    
    // دورة الحياة
    onMounted(async () => {
      // استعادة حالة الشريط الجانبي
      const savedSidebarState = localStorage.getItem('sidebarCollapsed');
      if (savedSidebarState !== null) {
        sidebarCollapsed.value = savedSidebarState === 'true';
      }
      
      // إضافة مستمع للنقر لإغلاق قائمة المستخدم
      document.addEventListener('click', handleClickOutside);
      
      // جلب المديولات
      await fetchModules();
    });
    
    // مراقبة تغيير اللغة
    watch(locale, () => {
      // إعادة تصفية المديولات عند تغيير اللغة
      filterModules();
    });
    
    return {
      searchQuery,
      sidebarCollapsed,
      showUserMenu,
      activeSection,
      activeModule,
      activeSetting,
      mainSections,
      settingsItems,
      visibleModules,
      isRtl,
      userName,
      userAvatar,
      brandLogo,
      brandName,
      appVersion,
      currentYear,
      toggleSidebar,
      toggleUserMenu,
      setActiveSection,
      setActiveModule,
      setActiveSetting,
      getActiveComponent,
      changeEntity,
      logout,
      navigateTo,
      filterModules,
      showHelp,
      showAbout,
      showPrivacyPolicy
    };
  }
};
</script>

<style scoped>
.main-dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--bg-color, #f5f7fa);
  color: var(--text-color, #333);
  direction: ltr;
}

.main-dashboard.rtl-support {
  direction: rtl;
}

/* Header Styles */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color, #007bff);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.brand-container {
  display: flex;
  align-items: center;
}

.brand-logo {
  height: 40px;
  margin-right: 1rem;
}

.rtl-support .brand-logo {
  margin-right: 0;
  margin-left: 1rem;
}

.brand-name {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
}

.search-container {
  margin-right: 0.75rem;
  flex: 1;
}

.rtl-support .search-container {
  margin-left: 0.75rem;
  margin-right: 0;
}

.search-container input {
  width: 100%;
}

.search-container input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.search-container input:focus {
  outline: none;
  width: 250px;
  background-color: rgba(255, 255, 255, 0.3);
}

.search-container i {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.7);
}

.rtl-support .search-container i {
  right: auto;
  left: 0.75rem;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 0.75rem;
  overflow: hidden;
}

.rtl-support .user-avatar {
  margin-right: 0;
  margin-left: 0.75rem;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar i {
  font-size: 1.2rem;
}

.user-name {
  margin-right: 0.5rem;
  font-weight: 500;
}

.rtl-support .user-name {
  margin-right: 0;
  margin-left: 0.5rem;
}

/* User Menu */
.user-menu {
  position: absolute;
  top: 100%;
  right: 0;
  width: 200px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
  margin-top: 0.5rem;
  overflow: hidden;
}

.rtl-support .user-menu {
  right: auto;
  left: 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: var(--text-color, #333);
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: var(--hover-bg-color, #f5f5f5);
}

.menu-item i {
  margin-right: 0.75rem;
  width: 1.25rem;
  text-align: center;
  color: var(--primary-color, #007bff);
}

.rtl-support .menu-item i {
  margin-right: 0;
  margin-left: 0.75rem;
}

.menu-divider {
  height: 1px;
  background-color: var(--border-color, #eee);
  margin: 0.25rem 0;
}

/* Content Styles */
.dashboard-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  background-color: var(--sidebar-bg-color, #fff);
  border-right: 1px solid var(--border-color, #eee);
  transition: width 0.3s;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
}

.rtl-support .sidebar {
  border-right: none;
  border-left: 1px solid var(--border-color, #eee);
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-toggle {
  position: absolute;
  top: 1rem;
  right: 0.5rem;
  width: 24px;
  height: 24px;
  background-color: var(--primary-color, #007bff);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 10;
}

.rtl-support .sidebar-toggle {
  right: auto;
  left: 0.5rem;
}

.sidebar-sections {
  padding: 1rem 0;
}

.sidebar-section {
  margin-bottom: 1.5rem;
}

.section-title {
  padding: 0 1.25rem;
  margin-bottom: 0.5rem;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted-color, #6c757d);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar.collapsed .section-title {
  text-align: center;
  font-size: 0.6rem;
}

.section-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  transition: background-color 0.2s;
  color: var(--text-color, #333);
  position: relative;
}

.section-item:hover {
  background-color: var(--hover-bg-color, #f5f5f5);
}

.section-item.active {
  background-color: var(--active-bg-color, rgba(0, 123, 255, 0.1));
  color: var(--primary-color, #007bff);
  font-weight: 500;
}

.section-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: var(--primary-color, #007bff);
}

.rtl-support .section-item.active::before {
  left: auto;
  right: 0;
}

.section-item i {
  margin-right: 0.75rem;
  width: 1.25rem;
  text-align: center;
}

.rtl-support .section-item i {
  margin-right: 0;
  margin-left: 0.75rem;
}

.sidebar.collapsed .section-item {
  padding: 0.75rem 0;
  justify-content: center;
}

.sidebar.collapsed .section-item i {
  margin-right: 0;
  margin-left: 0;
  font-size: 1.25rem;
}

.status-badge {
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  border-radius: 10px;
  margin-left: 0.5rem;
}

.rtl-support .status-badge {
  margin-left: 0;
  margin-right: 0.5rem;
}

.status-badge.new {
  background-color: var(--success-color, #28a745);
  color: white;
}

.main-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

.content-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  min-height: calc(100vh - 180px);
}

/* Footer Styles */
.dashboard-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background-color: var(--footer-bg-color, #fff);
  border-top: 1px solid var(--border-color, #eee);
  font-size: 0.85rem;
  color: var(--text-muted-color, #6c757d);
}

.footer-links a {
  color: var(--link-color, #007bff);
  text-decoration: none;
  margin-left: 1rem;
  transition: color 0.2s;
}

.rtl-support .footer-links a {
  margin-left: 0;
  margin-right: 1rem;
}

.footer-links a:hover {
  color: var(--link-hover-color, #0056b3);
  text-decoration: underline;
}

/* Responsive Styles */
@media (max-width: 992px) {
  .sidebar {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 0.75rem;
  }
  
  .brand-container {
    margin-bottom: 0.75rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .search-container {
    margin-right: 0;
    flex: 1;
    margin-right: 0.75rem;
  }
  
  .rtl-support .search-container {
    margin-left: 0.75rem;
  }
  
  .search-container input {
    width: 100%;
  }
  
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
  
  .rtl-support .sidebar {
    left: auto;
    right: 0;
    transform: translateX(100%);
  }
  
  .sidebar.active {
    transform: translateX(0);
  }
  
  .sidebar-toggle {
    display: none;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .dashboard-footer {
    flex-direction: column;
    text-align: center;
  }
  
  .footer-links {
    margin-top: 0.5rem;
  }
  
  .footer-links a {
    margin: 0 0.5rem;
  }
}

@media (max-width: 576px) {
  .user-name {
    display: none;
  }
}
</style>
