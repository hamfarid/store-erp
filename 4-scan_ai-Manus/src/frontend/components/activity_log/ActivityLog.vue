<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/activity_log/ActivityLog.vue
الوصف: مكون واجهة المستخدم الرئيسي لسجل النشاط
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
-->

<template>
  <div class="activity-log-container">
    <div class="header">
      <h1>{{ $t('activity_log.title') }}</h1>
      <div class="actions">
        <button class="btn btn-primary" @click="exportLogs">
          <i class="fas fa-file-export"></i> {{ $t('activity_log.export') }}
        </button>
        <button class="btn btn-secondary" @click="refreshLogs">
          <i class="fas fa-sync"></i> {{ $t('activity_log.refresh') }}
        </button>
      </div>
    </div>

    <div class="filters">
      <div class="filter-group">
        <label for="log-type">نوع السجل</label>
        <select 
          id="log-type"
          v-model="filters.type"
        >
          <option value="">الكل</option>
          <option value="info">معلومات</option>
          <option value="warning">تحذير</option>
          <option value="error">خطأ</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="log-module">الوحدة</label>
        <select 
          id="log-module"
          v-model="filters.module"
        >
          <option value="">الكل</option>
          <option value="system">النظام</option>
          <option value="ml">التعلم الآلي</option>
          <option value="database">قاعدة البيانات</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="log-action">الإجراء</label>
        <select 
          id="log-action"
          v-model="filters.action"
        >
          <option value="">الكل</option>
          <option value="create">إنشاء</option>
          <option value="update">تحديث</option>
          <option value="delete">حذف</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="log-user">المستخدم</label>
        <select 
          id="log-user"
          v-model="filters.user"
        >
          <option value="">الكل</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.name }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="log-date-range">النطاق الزمني</label>
        <div class="date-range">
          <input 
            id="log-date-from"
            type="date" 
            v-model="filters.dateFrom"
          />
          <span>إلى</span>
          <input 
            id="log-date-to"
            type="date" 
            v-model="filters.dateTo"
          />
        </div>
      </div>
      
      <div class="filter-group">
        <label for="log-search">بحث</label>
        <input 
          id="log-search"
          type="text" 
          v-model="filters.search" 
          placeholder="ابحث في السجلات..."
        />
      </div>
    </div>

    <div class="log-tabs">
      <div 
        class="tab" 
        :class="{ active: activeTab === 'system' }" 
        @click="setActiveTab('system')"
      >
        <i class="fas fa-server"></i> {{ $t('activity_log.system_logs') }}
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'user' }" 
        @click="setActiveTab('user')"
      >
        <i class="fas fa-users"></i> {{ $t('activity_log.user_logs') }}
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'ai' }" 
        @click="setActiveTab('ai')"
      >
        <i class="fas fa-robot"></i> {{ $t('activity_log.ai_logs') }}
      </div>
    </div>

    <div class="logs-container">
      <div v-if="loading" class="loading">
        <i class="fas fa-spinner fa-spin"></i> {{ $t('activity_log.loading') }}
      </div>
      
      <div v-else-if="filteredLogs.length === 0" class="no-logs">
        <i class="fas fa-info-circle"></i> {{ $t('activity_log.no_logs_found') }}
      </div>
      
      <div v-else class="logs-table">
        <table>
          <thead>
            <tr>
              <th @click="sortBy('timestamp')">
                {{ $t('activity_log.timestamp') }}
                <i v-if="sortKey === 'timestamp'" :class="sortIconClass"></i>
              </th>
              <th @click="sortBy('type')">
                {{ $t('activity_log.type') }}
                <i v-if="sortKey === 'type'" :class="sortIconClass"></i>
              </th>
              <th @click="sortBy('module')">
                {{ $t('activity_log.module') }}
                <i v-if="sortKey === 'module'" :class="sortIconClass"></i>
              </th>
              <th @click="sortBy('action')">
                {{ $t('activity_log.action') }}
                <i v-if="sortKey === 'action'" :class="sortIconClass"></i>
              </th>
              <th @click="sortBy('user')">
                {{ $t('activity_log.user') }}
                <i v-if="sortKey === 'user'" :class="sortIconClass"></i>
              </th>
              <th>{{ $t('activity_log.description') }}</th>
              <th>{{ $t('activity_log.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in paginatedLogs" :key="log.id" :class="getLogClass(log)">
              <td>{{ formatDate(log.timestamp) }}</td>
              <td>
                <span class="log-type" :class="log.type">
                  <i :class="getTypeIcon(log.type)"></i>
                  {{ getTypeLabel(log.type) }}
                </span>
              </td>
              <td>{{ log.module }}</td>
              <td>{{ log.action }}</td>
              <td>{{ log.user }}</td>
              <td>{{ log.description }}</td>
              <td>
                <button class="btn btn-sm btn-info" @click="viewDetails(log)">
                  <i class="fas fa-eye"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination">
        <button 
          class="btn btn-sm" 
          :disabled="currentPage === 1" 
          @click="currentPage--"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        
        <span>{{ $t('activity_log.page', { current: currentPage, total: totalPages }) }}</span>
        
        <button 
          class="btn btn-sm" 
          :disabled="currentPage === totalPages" 
          @click="currentPage++"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- مودال تفاصيل السجل -->
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ $t('activity_log.log_details') }}</h2>
          <button class="close-btn" @click="showModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="selectedLog">
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.timestamp') }}:</div>
              <div class="detail-value">{{ formatDate(selectedLog.timestamp, true) }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.type') }}:</div>
              <div class="detail-value">
                <span class="log-type" :class="selectedLog.type">
                  <i :class="getTypeIcon(selectedLog.type)"></i>
                  {{ getTypeLabel(selectedLog.type) }}
                </span>
              </div>
            </div>
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.module') }}:</div>
              <div class="detail-value">{{ selectedLog.module }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.action') }}:</div>
              <div class="detail-value">{{ selectedLog.action }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.user') }}:</div>
              <div class="detail-value">{{ selectedLog.user }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.description') }}:</div>
              <div class="detail-value">{{ selectedLog.description }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.ip_address') }}:</div>
              <div class="detail-value">{{ selectedLog.ipAddress }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.user_agent') }}:</div>
              <div class="detail-value">{{ selectedLog.userAgent }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">{{ $t('activity_log.status') }}:</div>
              <div class="detail-value">
                <span class="status" :class="selectedLog.status">
                  {{ getStatusLabel(selectedLog.status) }}
                </span>
              </div>
            </div>
            <div class="detail-row" v-if="selectedLog.details">
              <div class="detail-label">{{ $t('activity_log.additional_details') }}:</div>
              <div class="detail-value">
                <pre>{{ JSON.stringify(selectedLog.details, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary" @click="showModal = false">{{ $t('activity_log.close') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast';
import activityLogService from '@/services/activityLogService';
import { debounce } from 'lodash';
import { computed, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'ActivityLog',
  
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    
    // حالة البيانات
    const logs = ref([]);
    const loading = ref(true);
    const modules = ref([]);
    const actions = ref([]);
    const users = ref([]);
    
    // حالة التصفية
    const filters = ref({
      type: '',
      module: '',
      action: '',
      user: '',
      dateFrom: '',
      dateTo: '',
      search: ''
    });
    
    // حالة الصفحات
    const currentPage = ref(1);
    const itemsPerPage = ref(20);
    
    // حالة الفرز
    const sortKey = ref('timestamp');
    const sortDirection = ref('desc');
    
    // حالة التبويب النشط
    const activeTab = ref('system');
    
    // حالة المودال
    const showModal = ref(false);
    const selectedLog = ref(null);
    
    // تحميل البيانات
    const loadLogs = async () => {
      try {
        loading.value = true;
        const response = await activityLogService.getLogs(filters.value);
        logs.value = response.data;
        loading.value = false;
      } catch (error) {
        console.error('Error loading logs:', error);
        showToast('error', t('activity_log.error_loading_logs'));
        loading.value = false;
      }
    };
    
    // تحميل البيانات المرجعية
    const loadReferenceData = async () => {
      try {
        const [modulesResponse, actionsResponse, usersResponse] = await Promise.all([
          activityLogService.getModules(),
          activityLogService.getActions(),
          activityLogService.getUsers()
        ]);
        
        modules.value = modulesResponse.data;
        actions.value = actionsResponse.data;
        users.value = usersResponse.data;
      } catch (error) {
        console.error('Error loading reference data:', error);
        showToast('error', t('activity_log.error_loading_reference_data'));
      }
    };
    
    // تطبيق التصفية
    const applyFilters = () => {
      currentPage.value = 1;
      loadLogs();
    };
    
    // تأخير البحث
    const debounceSearch = debounce(() => {
      applyFilters();
    }, 500);
    
    // تحديث السجلات
    const refreshLogs = () => {
      loadLogs();
    };
    
    // تصدير السجلات
    const exportLogs = async () => {
      try {
        loading.value = true;
        await activityLogService.exportLogs(filters.value);
        showToast('success', t('activity_log.export_success'));
        loading.value = false;
      } catch (error) {
        console.error('Error exporting logs:', error);
        showToast('error', t('activity_log.error_exporting_logs'));
        loading.value = false;
      }
    };
    
    // عرض تفاصيل السجل
    const viewDetails = (log) => {
      selectedLog.value = log;
      showModal.value = true;
    };
    
    // تعيين التبويب النشط
    const setActiveTab = (tab) => {
      activeTab.value = tab;
      filters.value.type = tab;
      applyFilters();
    };
    
    // فرز السجلات
    const sortBy = (key) => {
      if (sortKey.value === key) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortKey.value = key;
        sortDirection.value = 'asc';
      }
    };
    
    // تنسيق التاريخ
    const formatDate = (timestamp, includeTime = false) => {
      if (!timestamp) return '';
      
      const date = new Date(timestamp);
      const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      };
      
      if (includeTime) {
        options.hour = '2-digit';
        options.minute = '2-digit';
        options.second = '2-digit';
      }
      
      return new Intl.DateTimeFormat('ar-SA', options).format(date);
    };
    
    // الحصول على أيقونة النوع
    const getTypeIcon = (type) => {
      switch (type) {
        case 'system':
          return 'fas fa-server';
        case 'user':
          return 'fas fa-user';
        case 'ai':
          return 'fas fa-robot';
        default:
          return 'fas fa-info-circle';
      }
    };
    
    // الحصول على تسمية النوع
    const getTypeLabel = (type) => {
      switch (type) {
        case 'system':
          return t('activity_log.system');
        case 'user':
          return t('activity_log.user');
        case 'ai':
          return t('activity_log.ai');
        default:
          return type;
      }
    };
    
    // الحصول على تسمية الحالة
    const getStatusLabel = (status) => {
      switch (status) {
        case 'success':
          return t('activity_log.success');
        case 'error':
          return t('activity_log.error');
        case 'warning':
          return t('activity_log.warning');
        case 'info':
          return t('activity_log.info');
        default:
          return status;
      }
    };
    
    // الحصول على صنف السجل
    const getLogClass = (log) => {
      return {
        'log-row': true,
        'log-error': log.status === 'error',
        'log-warning': log.status === 'warning',
        'log-success': log.status === 'success',
        'log-info': log.status === 'info'
      };
    };
    
    // السجلات المصفاة
    const filteredLogs = computed(() => {
      let result = [...logs.value];
      
      // فرز السجلات
      result.sort((a, b) => {
        let valueA = a[sortKey.value];
        let valueB = b[sortKey.value];
        
        if (sortKey.value === 'timestamp') {
          valueA = new Date(valueA).getTime();
          valueB = new Date(valueB).getTime();
        }
        
        if (valueA < valueB) {
          return sortDirection.value === 'asc' ? -1 : 1;
        }
        if (valueA > valueB) {
          return sortDirection.value === 'asc' ? 1 : -1;
        }
        return 0;
      });
      
      return result;
    });
    
    // السجلات المقسمة إلى صفحات
    const paginatedLogs = computed(() => {
      const startIndex = (currentPage.value - 1) * itemsPerPage.value;
      const endIndex = startIndex + itemsPerPage.value;
      return filteredLogs.value.slice(startIndex, endIndex);
    });
    
    // إجمالي عدد الصفحات
    const totalPages = computed(() => {
      return Math.ceil(filteredLogs.value.length / itemsPerPage.value);
    });
    
    // أيقونة الفرز
    const sortIconClass = computed(() => {
      return sortDirection.value === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
    });
    
    // مراقبة التغييرات في الصفحة الحالية
    watch(currentPage, (newPage, oldPage) => {
      if (newPage < 1) {
        currentPage.value = 1;
      } else if (newPage > totalPages.value) {
        currentPage.value = totalPages.value;
      }
    });
    
    // تحميل البيانات عند تركيب المكون
    onMounted(() => {
      loadReferenceData();
      loadLogs();
    });
    
    return {
      logs,
      loading,
      modules,
      actions,
      users,
      filters,
      currentPage,
      itemsPerPage,
      sortKey,
      sortDirection,
      activeTab,
      showModal,
      selectedLog,
      filteredLogs,
      paginatedLogs,
      totalPages,
      sortIconClass,
      loadLogs,
      applyFilters,
      debounceSearch,
      refreshLogs,
      exportLogs,
      viewDetails,
      setActiveTab,
      sortBy,
      formatDate,
      getTypeIcon,
      getTypeLabel,
      getStatusLabel,
      getLogClass
    };
  }
};
</script>

<style scoped>
.activity-log-container {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.actions {
  display: flex;
  gap: 10px;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.filter-group label {
  margin-bottom: 5px;
  font-size: 14px;
  color: #555;
}

.filter-group select,
.filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-input {
  position: relative;
}

.search-input input {
  padding-right: 30px;
  width: 200px;
}

.search-input i {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #777;
}

.log-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.tab {
  padding: 10px 20px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab:hover {
  background-color: #f0f0f0;
}

.tab.active {
  border-bottom-color: #007bff;
  color: #007bff;
}

.logs-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.loading,
.no-logs {
  padding: 40px;
  text-align: center;
  color: #777;
  font-size: 16px;
}

.loading i,
.no-logs i {
  margin-right: 10px;
  font-size: 20px;
}

.logs-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: #f8f9fa;
  padding: 12px 15px;
  text-align: right;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

th:hover {
  background-color: #e9ecef;
}

th i {
  margin-right: 5px;
}

td {
  padding: 12px 15px;
  border-top: 1px solid #eee;
  vertical-align: middle;
}

.log-type {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.log-type.system {
  background-color: #e3f2fd;
  color: #0d47a1;
}

.log-type.user {
  background-color: #e8f5e9;
  color: #1b5e20;
}

.log-type.ai {
  background-color: #f3e5f5;
  color: #4a148c;
}

.log-type i {
  margin-left: 5px;
}

.log-row.log-error {
  background-color: #fff8f8;
}

.log-row.log-warning {
  background-color: #fffbf0;
}

.log-row.log-success {
  background-color: #f0fff4;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
  gap: 15px;
}

.pagination span {
  font-size: 14px;
  color: #555;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 80%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #777;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  text-align: right;
}

.detail-row {
  display: flex;
  margin-bottom: 15px;
}

.detail-label {
  width: 150px;
  font-weight: 600;
  color: #555;
}

.detail-value {
  flex: 1;
}

.detail-value pre {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 13px;
}

.status {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status.success {
  background-color: #e8f5e9;
  color: #1b5e20;
}

.status.error {
  background-color: #ffebee;
  color: #b71c1c;
}

.status.warning {
  background-color: #fff8e1;
  color: #ff6f00;
}

.status.info {
  background-color: #e3f2fd;
  color: #0d47a1;
}

/* تحسينات للغة العربية */
[dir="rtl"] .search-input i {
  right: auto;
  left: 10px;
}

[dir="rtl"] th {
  text-align: right;
}

[dir="rtl"] .log-type i {
  margin-left: 0;
  margin-right: 5px;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .date-range {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .logs-table {
    font-size: 14px;
  }
  
  th, td {
    padding: 8px;
  }
  
  .modal-content {
    width: 95%;
  }
}
</style>
