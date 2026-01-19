<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/import_export/ImportExportDashboard.vue -->
<template>
  <div class="import-export-dashboard">
    <div class="page-header">
      <h1>{{ $t('import_export.title') }}</h1>
      <div class="header-actions">
        <el-button type="primary" @click="showImportModal">
          <i class="fas fa-file-import"></i> {{ $t('import_export.import') }}
        </el-button>
        <el-button type="success" @click="showExportModal">
          <i class="fas fa-file-export"></i> {{ $t('import_export.export') }}
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab" class="main-tabs">
      <el-tab-pane :label="$t('import_export.history')" name="history">
        <activity-history-table 
          :activities="activities" 
          :loading="loading"
          :total="totalActivities"
          @page-change="handlePageChange"
          @filter-change="handleFilterChange"
        />
      </el-tab-pane>
      <el-tab-pane :label="$t('import_export.templates')" name="templates" v-if="hasTemplatePermission">
        <templates-manager 
          :templates="templates" 
          :loading="loadingTemplates"
          @template-created="loadTemplates"
          @template-updated="loadTemplates"
          @template-deleted="loadTemplates"
        />
      </el-tab-pane>
      <el-tab-pane :label="$t('import_export.settings')" name="settings" v-if="hasAdminPermission">
        <import-export-settings 
          :settings="settings"
          :loading="loadingSettings"
          @settings-updated="loadSettings"
        />
      </el-tab-pane>
    </el-tabs>

    <!-- Import Modal -->
    <el-dialog
      :title="$t('import_export.import_data')"
      v-model="importModalVisible"
      width="60%"
      :before-close="closeImportModal"
      class="rtl-support"
    >
      <import-wizard
        :modules="availableModules"
        :templates="templates"
        @import-complete="handleImportComplete"
        @import-error="handleImportError"
      />
    </el-dialog>

    <!-- Export Modal -->
    <el-dialog
      :title="$t('import_export.export_data')"
      v-model="exportModalVisible"
      width="60%"
      :before-close="closeExportModal"
      class="rtl-support"
    >
      <export-wizard
        :modules="availableModules"
        :templates="templates"
        @export-complete="handleExportComplete"
        @export-error="handleExportError"
      />
    </el-dialog>
  </div>
</template>

<script>
import activityLogService from '@/services/activityLogService';
import importExportService from '@/services/importExportService';
import permissionsService from '@/services/permissionsService';
import { ElMessage } from 'element-plus';
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useStore } from 'vuex';

import ActivityHistoryTable from './ActivityHistoryTable.vue';
import ExportWizard from './ExportWizard.vue';
import ImportExportSettings from './ImportExportSettings.vue';
import ImportWizard from './ImportWizard.vue';
import TemplatesManager from './TemplatesManager.vue';

export default {
  name: 'ImportExportDashboard',
  components: {
    ActivityHistoryTable,
    TemplatesManager,
    ImportExportSettings,
    ImportWizard,
    ExportWizard
  },
  setup() {
    const { t } = useI18n();
    const store = useStore();
    
    // State
    const activeTab = ref('history');
    const importModalVisible = ref(false);
    const exportModalVisible = ref(false);
    const activities = ref([]);
    const templates = ref([]);
    const settings = ref({});
    const availableModules = ref([]);
    const loading = ref(false);
    const loadingTemplates = ref(false);
    const loadingSettings = ref(false);
    const totalActivities = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const filters = ref({
      type: null,
      module: null,
      status: null,
      dateRange: null
    });

    // Computed properties
    const hasTemplatePermission = computed(() => {
      return permissionsService.hasPermission('import_export', 'manage_templates');
    });

    const hasAdminPermission = computed(() => {
      return permissionsService.hasPermission('import_export', 'admin');
    });

    // Methods
    const loadActivities = async () => {
      try {
        loading.value = true;
        const response = await activityLogService.getActivityLogs({
          log_type: 'user',
          module_id: 'import_export',
          page: currentPage.value,
          page_size: pageSize.value,
          ...buildFilters()
        });
        activities.value = response.items;
        totalActivities.value = response.total;
      } catch (error) {
        console.error('Error loading activities:', error);
        ElMessage.error(t('import_export.error_loading_activities'));
      } finally {
        loading.value = false;
      }
    };

    const loadTemplates = async () => {
      if (!hasTemplatePermission.value) return;
      
      try {
        loadingTemplates.value = true;
        const response = await importExportService.getTemplates();
        templates.value = response;
      } catch (error) {
        console.error('Error loading templates:', error);
        ElMessage.error(t('import_export.error_loading_templates'));
      } finally {
        loadingTemplates.value = false;
      }
    };

    const loadSettings = async () => {
      if (!hasAdminPermission.value) return;
      
      try {
        loadingSettings.value = true;
        const response = await importExportService.getSettings();
        settings.value = response;
      } catch (error) {
        console.error('Error loading settings:', error);
        ElMessage.error(t('import_export.error_loading_settings'));
      } finally {
        loadingSettings.value = false;
      }
    };

    const loadAvailableModules = async () => {
      try {
        const response = await importExportService.getAvailableModules();
        availableModules.value = response;
      } catch (error) {
        console.error('Error loading available modules:', error);
        ElMessage.error(t('import_export.error_loading_modules'));
      }
    };

    const buildFilters = () => {
      const result = {};
      
      if (filters.value.type) {
        result.action_id = filters.value.type;
      }
      
      if (filters.value.module) {
        result.details = { module: filters.value.module };
      }
      
      if (filters.value.status) {
        result.status = filters.value.status;
      }
      
      if (filters.value.dateRange && filters.value.dateRange.length === 2) {
        result.start_date = filters.value.dateRange[0];
        result.end_date = filters.value.dateRange[1];
      }
      
      return result;
    };

    const handlePageChange = (page) => {
      currentPage.value = page;
      loadActivities();
    };

    const handleFilterChange = (newFilters) => {
      filters.value = { ...newFilters };
      currentPage.value = 1;
      loadActivities();
    };

    const showImportModal = () => {
      importModalVisible.value = true;
    };

    const closeImportModal = () => {
      importModalVisible.value = false;
    };

    const showExportModal = () => {
      exportModalVisible.value = true;
    };

    const closeExportModal = () => {
      exportModalVisible.value = false;
    };

    const handleImportComplete = (result) => {
      ElMessage.success({
        message: t('import_export.import_success', { count: result.imported_count }),
        duration: 5000
      });
      closeImportModal();
      loadActivities();
    };

    const handleImportError = (error) => {
      ElMessage.error({
        message: t('import_export.import_error', { error: error.message }),
        duration: 5000
      });
    };

    const handleExportComplete = (result) => {
      ElMessage.success({
        message: t('import_export.export_success', { count: result.exported_count }),
        duration: 5000
      });
      
      // Download the exported file
      if (result.download_url) {
        const link = document.createElement('a');
        link.href = result.download_url;
        link.download = result.filename || 'export.zip';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
      
      closeExportModal();
      loadActivities();
    };

    const handleExportError = (error) => {
      ElMessage.error({
        message: t('import_export.export_error', { error: error.message }),
        duration: 5000
      });
    };

    // Lifecycle hooks
    onMounted(() => {
      loadActivities();
      loadTemplates();
      loadSettings();
      loadAvailableModules();
    });

    return {
      activeTab,
      importModalVisible,
      exportModalVisible,
      activities,
      templates,
      settings,
      availableModules,
      loading,
      loadingTemplates,
      loadingSettings,
      totalActivities,
      hasTemplatePermission,
      hasAdminPermission,
      loadActivities,
      loadTemplates,
      loadSettings,
      handlePageChange,
      handleFilterChange,
      showImportModal,
      closeImportModal,
      showExportModal,
      closeExportModal,
      handleImportComplete,
      handleImportError,
      handleExportComplete,
      handleExportError
    };
  }
};
</script>

<style scoped>
.import-export-dashboard {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e4e7ed;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.main-tabs {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.rtl-support {
  direction: inherit;
}

/* Responsive design */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
