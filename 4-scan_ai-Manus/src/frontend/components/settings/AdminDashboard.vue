<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/AdminDashboard.vue
الوصف: لوحة تحكم المسؤول الرئيسية
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
-->

<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1>{{ $t('admin.dashboard.title') }}</h1>
      <div class="dashboard-actions">
        <button class="btn btn-primary" @click="refreshData">
          <i class="fas fa-sync-alt"></i> {{ $t('admin.dashboard.refresh') }}
        </button>
        <LanguageSwitcher class="language-switcher" />
      </div>
    </div>

    <div class="system-status-card">
      <div class="card-header">
        <h2>{{ $t('admin.dashboard.systemStatus') }}</h2>
        <span :class="['status-badge', `status-${systemStatus.status}`]">
          {{ getStatusText(systemStatus.status) }}
        </span>
      </div>
      <div class="card-body">
        <div class="status-grid">
          <div class="status-item">
            <div class="status-label">{{ $t('admin.dashboard.cpuUsage') }}</div>
            <div class="status-value">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${systemStatus.cpu}%` }"></div>
              </div>
              <span>{{ systemStatus.cpu }}%</span>
            </div>
          </div>
          <div class="status-item">
            <div class="status-label">{{ $t('admin.dashboard.memoryUsage') }}</div>
            <div class="status-value">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${systemStatus.memory}%` }"></div>
              </div>
              <span>{{ systemStatus.memory }}%</span>
            </div>
          </div>
          <div class="status-item">
            <div class="status-label">{{ $t('admin.dashboard.diskUsage') }}</div>
            <div class="status-value">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${systemStatus.disk}%` }"></div>
              </div>
              <span>{{ systemStatus.disk }}%</span>
            </div>
          </div>
          <div class="status-item">
            <div class="status-label">{{ $t('admin.dashboard.uptime') }}</div>
            <div class="status-value">{{ formatUptime(systemStatus.uptime) }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-grid">
      <div class="dashboard-card users-card">
        <div class="card-header">
          <h2>{{ $t('admin.dashboard.users') }}</h2>
          <router-link :to="{ name: 'userManagement' }" class="card-action">
            {{ $t('admin.dashboard.manage') }} <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
        <div class="card-body">
          <div class="stat-grid">
            <div class="stat-item">
              <div class="stat-value">{{ userStats.total }}</div>
              <div class="stat-label">{{ $t('admin.dashboard.totalUsers') }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ userStats.active }}</div>
              <div class="stat-label">{{ $t('admin.dashboard.activeUsers') }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ userStats.online }}</div>
              <div class="stat-label">{{ $t('admin.dashboard.onlineNow') }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ userStats.blocked }}</div>
              <div class="stat-label">{{ $t('admin.dashboard.blockedUsers') }}</div>
            </div>
          </div>
          <div class="recent-activity">
            <h3>{{ $t('admin.dashboard.recentUserActivity') }}</h3>
            <div v-if="recentUserActivity.length > 0" class="activity-list">
              <div v-for="(activity, index) in recentUserActivity" :key="index" class="activity-item">
                <div class="activity-icon">
                  <i :class="getActivityIcon(activity.action)"></i>
                </div>
                <div class="activity-details">
                  <div class="activity-user">{{ activity.username }}</div>
                  <div class="activity-action">{{ getActivityText(activity.action) }}</div>
                  <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
                </div>
              </div>
            </div>
            <div v-else class="no-data">
              {{ $t('admin.dashboard.noRecentActivity') }}
            </div>
          </div>
        </div>
      </div>

      <div class="dashboard-card security-card">
        <div class="card-header">
          <h2>{{ $t('admin.dashboard.security') }}</h2>
          <router-link :to="{ name: 'securitySettings' }" class="card-action">
            {{ $t('admin.dashboard.manage') }} <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
        <div class="card-body">
          <div class="security-alerts">
            <h3>{{ $t('admin.dashboard.securityAlerts') }}</h3>
            <div v-if="securityAlerts.length > 0" class="alerts-list">
              <div v-for="(alert, index) in securityAlerts" :key="index" 
                   :class="['alert-item', `alert-${alert.severity}`]">
                <div class="alert-icon">
                  <i :class="getAlertIcon(alert.type)"></i>
                </div>
                <div class="alert-details">
                  <div class="alert-title">{{ alert.title }}</div>
                  <div class="alert-message">{{ alert.message }}</div>
                  <div class="alert-time">{{ formatTime(alert.timestamp) }}</div>
                </div>
                <div class="alert-actions">
                  <button class="btn btn-sm" @click="resolveAlert(alert.id)">
                    {{ $t('admin.dashboard.resolve') }}
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="no-data">
              {{ $t('admin.dashboard.noSecurityAlerts') }}
            </div>
          </div>
          <div class="security-stats">
            <div class="stat-item">
              <div class="stat-label">{{ $t('admin.dashboard.failedLogins') }}</div>
              <div class="stat-value">{{ securityStats.failedLogins }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">{{ $t('admin.dashboard.blockedAttempts') }}</div>
              <div class="stat-value">{{ securityStats.blockedAttempts }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="dashboard-card backup-card">
        <div class="card-header">
          <h2>{{ $t('admin.dashboard.backups') }}</h2>
          <router-link :to="{ name: 'backupRestore' }" class="card-action">
            {{ $t('admin.dashboard.manage') }} <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
        <div class="card-body">
          <div class="last-backup">
            <h3>{{ $t('admin.dashboard.lastBackup') }}</h3>
            <div v-if="backupInfo.lastBackup" class="backup-info">
              <div class="backup-date">{{ formatDate(backupInfo.lastBackup.date) }}</div>
              <div class="backup-size">{{ formatSize(backupInfo.lastBackup.size) }}</div>
              <div class="backup-status">
                <span :class="['status-badge', `status-${backupInfo.lastBackup.status}`]">
                  {{ getBackupStatusText(backupInfo.lastBackup.status) }}
                </span>
              </div>
            </div>
            <div v-else class="no-data">
              {{ $t('admin.dashboard.noBackupsFound') }}
            </div>
          </div>
          <div class="backup-actions">
            <button class="btn btn-primary" @click="createBackup">
              <i class="fas fa-save"></i> {{ $t('admin.dashboard.createBackup') }}
            </button>
            <button class="btn btn-outline" @click="scheduleBackup">
              <i class="fas fa-calendar"></i> {{ $t('admin.dashboard.scheduleBackup') }}
            </button>
          </div>
        </div>
      </div>

      <div class="dashboard-card ai-card">
        <div class="card-header">
          <h2>{{ $t('admin.dashboard.aiAgents') }}</h2>
          <router-link :to="{ name: 'aiAgentManagement' }" class="card-action">
            {{ $t('admin.dashboard.manage') }} <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
        <div class="card-body">
          <div class="ai-stats">
            <div class="stat-item">
              <div class="stat-value">{{ aiStats.totalAgents }}</div>
              <div class="stat-label">{{ $t('admin.dashboard.totalAgents') }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ aiStats.activeAgents }}</div>
              <div class="stat-label">{{ $t('admin.dashboard.activeAgents') }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ aiStats.totalInteractions }}</div>
              <div class="stat-label">{{ $t('admin.dashboard.totalInteractions') }}</div>
            </div>
          </div>
          <div class="ai-usage">
            <h3>{{ $t('admin.dashboard.aiUsageToday') }}</h3>
            <div class="chart-container">
              <canvas ref="aiUsageChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>{{ $t('admin.dashboard.quickActions') }}</h2>
      <div class="actions-grid">
        <div class="action-item" @click="navigateTo('userManagement')">
          <div class="action-icon"><i class="fas fa-users"></i></div>
          <div class="action-label">{{ $t('admin.dashboard.manageUsers') }}</div>
        </div>
        <div class="action-item" @click="navigateTo('moduleManager')">
          <div class="action-icon"><i class="fas fa-puzzle-piece"></i></div>
          <div class="action-label">{{ $t('admin.dashboard.manageModules') }}</div>
        </div>
        <div class="action-item" @click="navigateTo('backupRestore')">
          <div class="action-icon"><i class="fas fa-database"></i></div>
          <div class="action-label">{{ $t('admin.dashboard.backupRestore') }}</div>
        </div>
        <div class="action-item" @click="navigateTo('systemSettings')">
          <div class="action-icon"><i class="fas fa-cogs"></i></div>
          <div class="action-label">{{ $t('admin.dashboard.systemSettings') }}</div>
        </div>
        <div class="action-item" @click="navigateTo('activityLog')">
          <div class="action-icon"><i class="fas fa-history"></i></div>
          <div class="action-label">{{ $t('admin.dashboard.activityLog') }}</div>
        </div>
        <div class="action-item" @click="navigateTo('importExport')">
          <div class="action-icon"><i class="fas fa-exchange-alt"></i></div>
          <div class="action-label">{{ $t('admin.dashboard.importExport') }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast';
import adminService from '@/services/adminService';
import Chart from 'chart.js/auto';
import { onMounted, onUnmounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import LanguageSwitcher from '../common/LanguageSwitcher.vue';

export default {
  name: 'AdminDashboard',
  components: {
    LanguageSwitcher
  },
  setup() {
    const { t } = useI18n();
    const router = useRouter();
    const { showToast } = useToast();
    
    // المراجع
    const aiUsageChart = ref(null);
    let chart = null;
    let refreshInterval = null;
    
    // بيانات النظام
    const systemStatus = ref({
      status: 'healthy', // healthy, warning, critical
      cpu: 25,
      memory: 40,
      disk: 60,
      uptime: 1209600 // بالثواني (14 يوم)
    });
    
    // إحصائيات المستخدمين
    const userStats = ref({
      total: 0,
      active: 0,
      online: 0,
      blocked: 0
    });
    
    // نشاط المستخدمين الأخير
    const recentUserActivity = ref([]);
    
    // تنبيهات الأمان
    const securityAlerts = ref([]);
    
    // إحصائيات الأمان
    const securityStats = ref({
      failedLogins: 0,
      blockedAttempts: 0
    });
    
    // معلومات النسخ الاحتياطي
    const backupInfo = ref({
      lastBackup: null,
      scheduledBackups: []
    });
    
    // إحصائيات الذكاء الاصطناعي
    const aiStats = ref({
      totalAgents: 0,
      activeAgents: 0,
      totalInteractions: 0
    });
    
    // تحديث البيانات
    const refreshData = async () => {
      try {
        // تحديث حالة النظام
        const systemData = await adminService.getSystemStatus();
        systemStatus.value = systemData;
        
        // تحديث إحصائيات المستخدمين
        const userData = await adminService.getUserStats();
        userStats.value = userData;
        
        // تحديث نشاط المستخدمين الأخير
        const activityData = await adminService.getRecentUserActivity();
        recentUserActivity.value = activityData;
        
        // تحديث تنبيهات الأمان
        const alertsData = await adminService.getSecurityAlerts();
        securityAlerts.value = alertsData;
        
        // تحديث إحصائيات الأمان
        const securityData = await adminService.getSecurityStats();
        securityStats.value = securityData;
        
        // تحديث معلومات النسخ الاحتياطي
        const backupData = await adminService.getBackupInfo();
        backupInfo.value = backupData;
        
        // تحديث إحصائيات الذكاء الاصطناعي
        const aiData = await adminService.getAIStats();
        aiStats.value = aiData;
        
        // تحديث مخطط استخدام الذكاء الاصطناعي
        updateAIUsageChart();
        
        showToast(t('admin.dashboard.dataRefreshed'), 'success');
      } catch (error) {
        console.error('Failed to refresh dashboard data:', error);
        showToast(t('admin.dashboard.refreshError'), 'error');
      }
    };
    
    // تحديث مخطط استخدام الذكاء الاصطناعي
    const updateAIUsageChart = async () => {
      try {
        const usageData = await adminService.getAIUsageData();
        
        if (chart) {
          chart.destroy();
        }
        
        const ctx = aiUsageChart.value.getContext('2d');
        chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: usageData.labels,
            datasets: [{
              label: t('admin.dashboard.aiUsage'),
              data: usageData.data,
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 2,
              tension: 0.4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      } catch (error) {
        console.error('Failed to update AI usage chart:', error);
      }
    };
    
    // إنشاء نسخة احتياطية
    const createBackup = async () => {
      try {
        showToast(t('admin.dashboard.backupStarted'), 'info');
        const result = await adminService.createBackup();
        showToast(t('admin.dashboard.backupCreated'), 'success');
        
        // تحديث معلومات النسخ الاحتياطي
        const backupData = await adminService.getBackupInfo();
        backupInfo.value = backupData;
      } catch (error) {
        console.error('Failed to create backup:', error);
        showToast(t('admin.dashboard.backupError'), 'error');
      }
    };
    
    // جدولة نسخة احتياطية
    const scheduleBackup = async () => {
      try {
        // هنا يمكن إضافة منطق لفتح نافذة منبثقة لجدولة النسخ الاحتياطي
        router.push({ name: 'backupSchedule' });
      } catch (error) {
        console.error('Failed to schedule backup:', error);
        showToast(t('admin.dashboard.scheduleError'), 'error');
      }
    };
    
    // حل تنبيه أمان
    const resolveAlert = async (alertId) => {
      try {
        await adminService.resolveSecurityAlert(alertId);
        showToast(t('admin.dashboard.alertResolved'), 'success');
        
        // تحديث تنبيهات الأمان
        const alertsData = await adminService.getSecurityAlerts();
        securityAlerts.value = alertsData;
      } catch (error) {
        console.error('Failed to resolve alert:', error);
        showToast(t('admin.dashboard.resolveError'), 'error');
      }
    };
    
    // الانتقال إلى صفحة
    const navigateTo = (routeName) => {
      router.push({ name: routeName });
    };
    
    // تنسيق وقت التشغيل
    const formatUptime = (seconds) => {
      const days = Math.floor(seconds / 86400);
      const hours = Math.floor((seconds % 86400) / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      
      let result = '';
      if (days > 0) {
        result += `${days} ${t('admin.dashboard.days')} `;
      }
      if (hours > 0 || days > 0) {
        result += `${hours} ${t('admin.dashboard.hours')} `;
      }
      result += `${minutes} ${t('admin.dashboard.minutes')}`;
      
      return result;
    };
    
    // تنسيق الوقت
    const formatTime = (timestamp) => {
      const date = new Date(timestamp);
      return new Intl.DateTimeFormat(document.documentElement.lang, {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }).format(date);
    };
    
    // تنسيق التاريخ
    const formatDate = (timestamp) => {
      const date = new Date(timestamp);
      return new Intl.DateTimeFormat(document.documentElement.lang, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };
    
    // تنسيق حجم الملف
    const formatSize = (bytes) => {
      if (bytes === 0) return '0 Bytes';
      
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    // الحصول على نص الحالة
    const getStatusText = (status) => {
      switch (status) {
        case 'healthy':
          return t('admin.dashboard.statusHealthy');
        case 'warning':
          return t('admin.dashboard.statusWarning');
        case 'critical':
          return t('admin.dashboard.statusCritical');
        default:
          return t('admin.dashboard.statusUnknown');
      }
    };
    
    // الحصول على نص حالة النسخ الاحتياطي
    const getBackupStatusText = (status) => {
      switch (status) {
        case 'success':
          return t('admin.dashboard.backupSuccess');
        case 'warning':
          return t('admin.dashboard.backupWarning');
        case 'error':
          return t('admin.dashboard.backupError');
        default:
          return t('admin.dashboard.backupUnknown');
      }
    };
    
    // الحصول على أيقونة النشاط
    const getActivityIcon = (action) => {
      switch (action) {
        case 'login':
          return 'fas fa-sign-in-alt';
        case 'logout':
          return 'fas fa-sign-out-alt';
        case 'create':
          return 'fas fa-plus-circle';
        case 'update':
          return 'fas fa-edit';
        case 'delete':
          return 'fas fa-trash-alt';
        case 'view':
          return 'fas fa-eye';
        default:
          return 'fas fa-info-circle';
      }
    };
    
    // الحصول على نص النشاط
    const getActivityText = (action) => {
      switch (action) {
        case 'login':
          return t('admin.dashboard.actionLogin');
        case 'logout':
          return t('admin.dashboard.actionLogout');
        case 'create':
          return t('admin.dashboard.actionCreate');
        case 'update':
          return t('admin.dashboard.actionUpdate');
        case 'delete':
          return t('admin.dashboard.actionDelete');
        case 'view':
          return t('admin.dashboard.actionView');
        default:
          return action;
      }
    };
    
    // الحصول على أيقونة التنبيه
    const getAlertIcon = (type) => {
      switch (type) {
        case 'login_attempt':
          return 'fas fa-user-shield';
        case 'permission':
          return 'fas fa-lock';
        case 'system':
          return 'fas fa-server';
        case 'database':
          return 'fas fa-database';
        default:
          return 'fas fa-exclamation-triangle';
      }
    };
    
    // دورة حياة المكون
    onMounted(async () => {
      await refreshData();
      
      // تحديث البيانات كل دقيقة
      refreshInterval = setInterval(refreshData, 60000);
    });
    
    onUnmounted(() => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
      
      if (chart) {
        chart.destroy();
      }
    });
    
    return {
      systemStatus,
      userStats,
      recentUserActivity,
      securityAlerts,
      securityStats,
      backupInfo,
      aiStats,
      aiUsageChart,
      refreshData,
      createBackup,
      scheduleBackup,
      resolveAlert,
      navigateTo,
      formatUptime,
      formatTime,
      formatDate,
      formatSize,
      getStatusText,
      getBackupStatusText,
      getActivityIcon,
      getActivityText,
      getAlertIcon
    };
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

.dashboard-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.language-switcher {
  margin-left: 1rem;
}

.system-status-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.card-body {
  padding: 1.5rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-healthy {
  background-color: #d4edda;
  color: #155724;
}

.status-warning {
  background-color: #fff3cd;
  color: #856404;
}

.status-critical {
  background-color: #f8d7da;
  color: #721c24;
}

.status-success {
  background-color: #d4edda;
  color: #155724;
}

.status-error {
  background-color: #f8d7da;
  color: #721c24;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-label {
  font-size: 0.875rem;
  color: #6c757d;
}

.status-value {
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #007bff;
  border-radius: 4px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.dashboard-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-action {
  font-size: 0.875rem;
  color: #007bff;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.card-action:hover {
  text-decoration: underline;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
}

.recent-activity h3,
.security-alerts h3,
.last-backup h3,
.ai-usage h3 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.activity-list,
.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item,
.alert-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.activity-icon,
.alert-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #e9ecef;
  border-radius: 50%;
  font-size: 1.25rem;
}

.activity-details,
.alert-details {
  flex: 1;
}

.activity-user,
.alert-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.activity-action,
.alert-message {
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.activity-time,
.alert-time {
  font-size: 0.75rem;
  color: #6c757d;
}

.alert-actions {
  display: flex;
  align-items: center;
}

.alert-high {
  border-left: 4px solid #dc3545;
}

.alert-medium {
  border-left: 4px solid #ffc107;
}

.alert-low {
  border-left: 4px solid #17a2b8;
}

.no-data {
  padding: 1rem;
  text-align: center;
  color: #6c757d;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.security-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 1.5rem;
}

.backup-info {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.backup-date {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.backup-size {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.backup-actions {
  display: flex;
  gap: 1rem;
}

.chart-container {
  height: 200px;
  margin-top: 1rem;
}

.quick-actions {
  margin-top: 2rem;
}

.quick-actions h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.action-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #007bff;
}

.action-label {
  text-align: center;
  font-weight: 500;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  border: none;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0069d9;
}

.btn-outline {
  background-color: transparent;
  color: #007bff;
  border: 1px solid #007bff;
}

.btn-outline:hover {
  background-color: #f0f7ff;
}

/* تعديلات للغة العربية */
:global([dir="rtl"]) .card-action {
  flex-direction: row-reverse;
}

:global([dir="rtl"]) .alert-high {
  border-left: none;
  border-right: 4px solid #dc3545;
}

:global([dir="rtl"]) .alert-medium {
  border-left: none;
  border-right: 4px solid #ffc107;
}

:global([dir="rtl"]) .alert-low {
  border-left: none;
  border-right: 4px solid #17a2b8;
}

/* تعديلات للشاشات الصغيرة */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .dashboard-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .status-grid,
  .stat-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
