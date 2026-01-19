<template>
  <div class="permissions-dashboard">
    <h1>لوحة تحكم الصلاحيات</h1>
    
    <!-- بطاقات الإحصائيات الرئيسية -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-users"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ usersCount }}</div>
          <div class="stat-label">المستخدمين</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-users-cog"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ rolesCount }}</div>
          <div class="stat-label">الأدوار</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-key"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ permissionsCount }}</div>
          <div class="stat-label">الصلاحيات</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-building"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ organizationsCount }}</div>
          <div class="stat-label">المؤسسات</div>
        </div>
      </div>
    </div>
    
    <!-- الرسوم البيانية -->
    <div class="charts-container">
      <div class="chart-card">
        <h3>توزيع المستخدمين حسب الأدوار</h3>
        <div class="chart-container">
          <canvas ref="userRolesChart"></canvas>
        </div>
      </div>
      
      <div class="chart-card">
        <h3>توزيع الصلاحيات حسب نوع الإجراء</h3>
        <div class="chart-container">
          <canvas ref="permissionsByActionChart"></canvas>
        </div>
      </div>
      
      <div class="chart-card">
        <h3>توزيع الصلاحيات حسب نوع المورد</h3>
        <div class="chart-container">
          <canvas ref="permissionsByResourceChart"></canvas>
        </div>
      </div>
      
      <div class="chart-card">
        <h3>نشاط المستخدمين (آخر 30 يوم)</h3>
        <div class="chart-container">
          <canvas ref="userActivityChart"></canvas>
        </div>
      </div>
    </div>
    
    <!-- جدول أكثر المستخدمين نشاطاً -->
    <div class="table-section">
      <h3>أكثر المستخدمين نشاطاً</h3>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>المستخدم</th>
              <th>عدد الأدوار</th>
              <th>عدد الصلاحيات</th>
              <th>آخر تسجيل دخول</th>
              <th>عدد العمليات (30 يوم)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in topActiveUsers" :key="user.id">
              <td>{{ user.full_name }}</td>
              <td>{{ user.roles_count }}</td>
              <td>{{ user.permissions_count }}</td>
              <td>{{ formatDate(user.last_login) }}</td>
              <td>{{ user.operations_count }}</td>
            </tr>
            <tr v-if="topActiveUsers.length === 0">
              <td colspan="5" class="no-data">لا توجد بيانات</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- جدول أكثر الصلاحيات استخداماً -->
    <div class="table-section">
      <h3>أكثر الصلاحيات استخداماً</h3>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>الصلاحية</th>
              <th>نوع المورد</th>
              <th>الإجراء</th>
              <th>عدد المستخدمين</th>
              <th>عدد العمليات (30 يوم)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="permission in topUsedPermissions" :key="permission.id">
              <td>{{ permission.name }}</td>
              <td>{{ permission.resource_type }}</td>
              <td>
                <span :class="['action-type', permission.action]">
                  {{ getActionLabel(permission.action) }}
                </span>
              </td>
              <td>{{ permission.users_count }}</td>
              <td>{{ permission.operations_count }}</td>
            </tr>
            <tr v-if="topUsedPermissions.length === 0">
              <td colspan="5" class="no-data">لا توجد بيانات</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- إحصائيات الأمان -->
    <div class="security-stats">
      <h3>إحصائيات الأمان</h3>
      <div class="security-cards">
        <div class="security-card">
          <div class="security-icon"><i class="fas fa-shield-alt"></i></div>
          <div class="security-content">
            <div class="security-value">{{ securityStats.failed_login_attempts }}</div>
            <div class="security-label">محاولات تسجيل دخول فاشلة (30 يوم)</div>
          </div>
        </div>
        <div class="security-card">
          <div class="security-icon"><i class="fas fa-user-lock"></i></div>
          <div class="security-content">
            <div class="security-value">{{ securityStats.locked_accounts }}</div>
            <div class="security-label">حسابات مقفلة</div>
          </div>
        </div>
        <div class="security-card">
          <div class="security-icon"><i class="fas fa-exclamation-triangle"></i></div>
          <div class="security-content">
            <div class="security-value">{{ securityStats.permission_violations }}</div>
            <div class="security-label">انتهاكات الصلاحيات (30 يوم)</div>
          </div>
        </div>
        <div class="security-card">
          <div class="security-icon"><i class="fas fa-user-shield"></i></div>
          <div class="security-content">
            <div class="security-value">{{ securityStats.admin_operations }}</div>
            <div class="security-label">عمليات المشرفين (30 يوم)</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- الروابط السريعة -->
    <div class="quick-links">
      <h3>روابط سريعة</h3>
      <div class="links-container">
        <router-link to="/permissions/roles" class="quick-link">
          <i class="fas fa-users-cog"></i>
          <span>إدارة الأدوار</span>
        </router-link>
        <router-link to="/permissions/users" class="quick-link">
          <i class="fas fa-user-shield"></i>
          <span>صلاحيات المستخدمين</span>
        </router-link>
        <router-link to="/activity-log" class="quick-link">
          <i class="fas fa-clipboard-list"></i>
          <span>سجل النشاط</span>
        </router-link>
        <router-link to="/security/audit" class="quick-link">
          <i class="fas fa-shield-alt"></i>
          <span>تدقيق الأمان</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * @component PermissionsDashboard
 * @description لوحة تحكم تعرض إحصائيات النظام حسب الصلاحيات
 * 
 * يوفر هذا المكون لوحة تحكم متكاملة تعرض إحصائيات النظام المتعلقة بالصلاحيات،
 * بما في ذلك توزيع المستخدمين حسب الأدوار، وتوزيع الصلاحيات حسب نوع الإجراء والمورد،
 * ونشاط المستخدمين، وإحصائيات الأمان.
 * 
 * @author فريق Scan AI
 * @date 30 مايو 2025
 */
import { useActivityLogService } from '@/composables/useActivityLogService';
import { useOrganizationService } from '@/composables/useOrganizationService';
import { usePermissionService } from '@/composables/usePermissionService';
import { useSecurityService } from '@/composables/useSecurityService';
import { useUserService } from '@/composables/useUserService';
import Chart from 'chart.js/auto';
import { defineComponent, onMounted, ref } from 'vue';

export default defineComponent({
  name: 'PermissionsDashboard',
  
  setup() {
    // الخدمات
    const permissionService = usePermissionService();
    const userService = useUserService();
    const organizationService = useOrganizationService();
    const activityLogService = useActivityLogService();
    const securityService = useSecurityService();
    
    // مراجع الرسوم البيانية
    const userRolesChart = ref(null);
    const permissionsByActionChart = ref(null);
    const permissionsByResourceChart = ref(null);
    const userActivityChart = ref(null);
    
    // بيانات الإحصائيات
    const usersCount = ref(0);
    const rolesCount = ref(0);
    const permissionsCount = ref(0);
    const organizationsCount = ref(0);
    
    // بيانات الجداول
    const topActiveUsers = ref([]);
    const topUsedPermissions = ref([]);
    
    // بيانات إحصائيات الأمان
    const securityStats = ref({
      failed_login_attempts: 0,
      locked_accounts: 0,
      permission_violations: 0,
      admin_operations: 0
    });
    
    // بيانات الرسوم البيانية
    const userRolesData = ref({
      labels: [],
      datasets: []
    });
    
    const permissionsByActionData = ref({
      labels: [],
      datasets: []
    });
    
    const permissionsByResourceData = ref({
      labels: [],
      datasets: []
    });
    
    const userActivityData = ref({
      labels: [],
      datasets: []
    });
    
    // الرسوم البيانية
    let userRolesChartInstance = null;
    let permissionsByActionChartInstance = null;
    let permissionsByResourceChartInstance = null;
    let userActivityChartInstance = null;
    
    /**
     * تنسيق التاريخ
     * @param {string} dateString - سلسلة التاريخ
     * @returns {string} - التاريخ المنسق
     */
    const formatDate = (dateString) => {
      if (!dateString) return 'غير متوفر';
      
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };
    
    /**
     * الحصول على تسمية الإجراء
     * @param {string} action - رمز الإجراء
     * @returns {string} - تسمية الإجراء
     */
    const getActionLabel = (action) => {
      const actionLabels = {
        'create': 'إنشاء',
        'read': 'قراءة',
        'update': 'تعديل',
        'delete': 'حذف',
        'view': 'اطلاع',
        'admin': 'أدمن',
        'approve': 'موافقة'
      };
      
      return actionLabels[action] || action;
    };
    
    /**
     * تحميل بيانات الإحصائيات
     */
    const loadStats = async () => {
      try {
        // تحميل إحصائيات المستخدمين
        const usersResponse = await userService.getUsersStats();
        usersCount.value = usersResponse.data.total_count;
        
        // تحميل إحصائيات الأدوار
        const rolesResponse = await permissionService.getRolesStats();
        rolesCount.value = rolesResponse.data.total_count;
        
        // تحميل إحصائيات الصلاحيات
        const permissionsResponse = await permissionService.getPermissionsStats();
        permissionsCount.value = permissionsResponse.data.total_count;
        
        // تحميل إحصائيات المؤسسات
        const organizationsResponse = await organizationService.getOrganizationsStats();
        organizationsCount.value = organizationsResponse.data.total_count;
      } catch (error) {
        console.error('Error loading stats:', error);
      }
    };
    
    /**
     * تحميل بيانات الرسوم البيانية
     */
    const loadChartData = async () => {
      try {
        // تحميل بيانات توزيع المستخدمين حسب الأدوار
        const userRolesResponse = await permissionService.getUserRolesDistribution();
        userRolesData.value = {
          labels: userRolesResponse.data.map(item => item.role_name),
          datasets: [{
            label: 'عدد المستخدمين',
            data: userRolesResponse.data.map(item => item.users_count),
            backgroundColor: [
              '#4a6cf7',
              '#f44336',
              '#ff9800',
              '#4caf50',
              '#9c27b0',
              '#2196f3',
              '#ff5722',
              '#795548',
              '#607d8b'
            ],
            borderWidth: 1
          }]
        };
        
        // تحميل بيانات توزيع الصلاحيات حسب نوع الإجراء
        const permissionsByActionResponse = await permissionService.getPermissionsByActionDistribution();
        permissionsByActionData.value = {
          labels: permissionsByActionResponse.data.map(item => getActionLabel(item.action)),
          datasets: [{
            label: 'عدد الصلاحيات',
            data: permissionsByActionResponse.data.map(item => item.count),
            backgroundColor: [
              '#4caf50', // إنشاء
              '#2196f3', // قراءة
              '#ff9800', // تعديل
              '#f44336', // حذف
              '#9c27b0', // اطلاع
              '#e91e63', // أدمن
              '#00bcd4'  // موافقة
            ],
            borderWidth: 1
          }]
        };
        
        // تحميل بيانات توزيع الصلاحيات حسب نوع المورد
        const permissionsByResourceResponse = await permissionService.getPermissionsByResourceDistribution();
        permissionsByResourceData.value = {
          labels: permissionsByResourceResponse.data.map(item => item.resource_type),
          datasets: [{
            label: 'عدد الصلاحيات',
            data: permissionsByResourceResponse.data.map(item => item.count),
            backgroundColor: [
              '#4a6cf7',
              '#f44336',
              '#ff9800',
              '#4caf50',
              '#9c27b0',
              '#2196f3',
              '#ff5722',
              '#795548',
              '#607d8b',
              '#e91e63',
              '#00bcd4',
              '#ffeb3b'
            ],
            borderWidth: 1
          }]
        };
        
        // تحميل بيانات نشاط المستخدمين
        const userActivityResponse = await activityLogService.getUserActivityLast30Days();
        userActivityData.value = {
          labels: userActivityResponse.data.map(item => item.date),
          datasets: [{
            label: 'عدد العمليات',
            data: userActivityResponse.data.map(item => item.operations_count),
            backgroundColor: 'rgba(74, 108, 247, 0.2)',
            borderColor: '#4a6cf7',
            borderWidth: 2,
            tension: 0.4,
            fill: true
          }]
        };
      } catch (error) {
        console.error('Error loading chart data:', error);
      }
    };
    
    /**
     * تحميل بيانات الجداول
     */
    const loadTableData = async () => {
      try {
        // تحميل بيانات أكثر المستخدمين نشاطاً
        const topUsersResponse = await activityLogService.getTopActiveUsers();
        topActiveUsers.value = topUsersResponse.data;
        
        // تحميل بيانات أكثر الصلاحيات استخداماً
        const topPermissionsResponse = await activityLogService.getTopUsedPermissions();
        topUsedPermissions.value = topPermissionsResponse.data;
      } catch (error) {
        console.error('Error loading table data:', error);
      }
    };
    
    /**
     * تحميل إحصائيات الأمان
     */
    const loadSecurityStats = async () => {
      try {
        const securityResponse = await securityService.getSecurityStats();
        securityStats.value = securityResponse.data;
      } catch (error) {
        console.error('Error loading security stats:', error);
      }
    };
    
    /**
     * إنشاء الرسوم البيانية
     */
    const createCharts = () => {
      // إنشاء رسم توزيع المستخدمين حسب الأدوار
      if (userRolesChartInstance) {
        userRolesChartInstance.destroy();
      }
      
      userRolesChartInstance = new Chart(userRolesChart.value, {
        type: 'pie',
        data: userRolesData.value,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                font: {
                  family: 'Tajawal, sans-serif'
                }
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw || 0;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = Math.round((value / total) * 100);
                  return `${label}: ${value} (${percentage}%)`;
                }
              }
            }
          }
        }
      });
      
      // إنشاء رسم توزيع الصلاحيات حسب نوع الإجراء
      if (permissionsByActionChartInstance) {
        permissionsByActionChartInstance.destroy();
      }
      
      permissionsByActionChartInstance = new Chart(permissionsByActionChart.value, {
        type: 'doughnut',
        data: permissionsByActionData.value,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                font: {
                  family: 'Tajawal, sans-serif'
                }
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw || 0;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = Math.round((value / total) * 100);
                  return `${label}: ${value} (${percentage}%)`;
                }
              }
            }
          }
        }
      });
      
      // إنشاء رسم توزيع الصلاحيات حسب نوع المورد
      if (permissionsByResourceChartInstance) {
        permissionsByResourceChartInstance.destroy();
      }
      
      permissionsByResourceChartInstance = new Chart(permissionsByResourceChart.value, {
        type: 'bar',
        data: permissionsByResourceData.value,
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            },
            x: {
              ticks: {
                font: {
                  family: 'Tajawal, sans-serif'
                }
              }
            }
          }
        }
      });
      
      // إنشاء رسم نشاط المستخدمين
      if (userActivityChartInstance) {
        userActivityChartInstance.destroy();
      }
      
      userActivityChartInstance = new Chart(userActivityChart.value, {
        type: 'line',
        data: userActivityData.value,
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            },
            x: {
              ticks: {
                font: {
                  family: 'Tajawal, sans-serif'
                },
                maxRotation: 45,
                minRotation: 45
              }
            }
          }
        }
      });
    };
    
    // دورة حياة المكون
    
    onMounted(async () => {
      // تحميل البيانات
      await Promise.all([
        loadStats(),
        loadChartData(),
        loadTableData(),
        loadSecurityStats()
      ]);
      
      // إنشاء الرسوم البيانية
      createCharts();
      
      // تحديث البيانات كل 5 دقائق
      const updateInterval = setInterval(async () => {
        await Promise.all([
          loadStats(),
          loadChartData(),
          loadTableData(),
          loadSecurityStats()
        ]);
        
        createCharts();
      }, 5 * 60 * 1000);
      
      // تنظيف عند تدمير المكون
      return () => {
        clearInterval(updateInterval);
        
        if (userRolesChartInstance) {
          userRolesChartInstance.destroy();
        }
        
        if (permissionsByActionChartInstance) {
          permissionsByActionChartInstance.destroy();
        }
        
        if (permissionsByResourceChartInstance) {
          permissionsByResourceChartInstance.destroy();
        }
        
        if (userActivityChartInstance) {
          userActivityChartInstance.destroy();
        }
      };
    });
    
    return {
      // مراجع الرسوم البيانية
      userRolesChart,
      permissionsByActionChart,
      permissionsByResourceChart,
      userActivityChart,
      
      // بيانات الإحصائيات
      usersCount,
      rolesCount,
      permissionsCount,
      organizationsCount,
      
      // بيانات الجداول
      topActiveUsers,
      topUsedPermissions,
      
      // بيانات إحصائيات الأمان
      securityStats,
      
      // دوال المساعدة
      formatDate,
      getActionLabel
    };
  }
});
</script>

<style scoped>
.permissions-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

h3 {
  margin-bottom: 15px;
  color: #333;
}

/* بطاقات الإحصائيات */
.stats-cards {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.stat-card {
  flex: 1;
  min-width: 200px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin: 0 10px 10px 0;
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 2rem;
  color: #4a6cf7;
  margin-left: 15px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

/* الرسوم البيانية */
.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.chart-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  text-align: center;
  font-size: 1.1rem;
}

.chart-container {
  height: 250px;
  position: relative;
}

/* الجداول */
.table-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 30px;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px 15px;
  text-align: right;
  border-bottom: 1px solid #ddd;
}

.data-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.data-table tr:hover {
  background-color: #f9f9f9;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #666;
}

/* إحصائيات الأمان */
.security-stats {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 30px;
}

.security-cards {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.security-card {
  flex: 1;
  min-width: 200px;
  padding: 15px;
  margin: 0 10px 10px 0;
  border-radius: 8px;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
}

.security-icon {
  font-size: 1.5rem;
  color: #f44336;
  margin-left: 15px;
}

.security-content {
  flex: 1;
}

.security-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.security-label {
  font-size: 0.8rem;
  color: #666;
}

/* الروابط السريعة */
.quick-links {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.links-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.quick-link {
  flex: 1;
  min-width: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  margin: 0 10px 10px 0;
  border-radius: 8px;
  background-color: #f5f5f5;
  text-decoration: none;
  color: #333;
  transition: all 0.3s;
}

.quick-link:hover {
  background-color: #e3f2fd;
  transform: translateY(-5px);
}

.quick-link i {
  font-size: 2rem;
  color: #4a6cf7;
  margin-bottom: 10px;
}

/* العلامات والأيقونات */
.action-type {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.action-type.create {
  background-color: #e8f5e9;
  color: #388e3c;
}

.action-type.read {
  background-color: #e3f2fd;
  color: #1976d2;
}

.action-type.update {
  background-color: #fff3e0;
  color: #f57c00;
}

.action-type.delete {
  background-color: #ffebee;
  color: #d32f2f;
}

.action-type.view {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.action-type.admin {
  background-color: #fce4ec;
  color: #c2185b;
}

.action-type.approve {
  background-color: #e0f7fa;
  color: #00acc1;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .stat-card,
  .security-card,
  .quick-link {
    margin: 0 0 10px 0;
  }
}
</style>
