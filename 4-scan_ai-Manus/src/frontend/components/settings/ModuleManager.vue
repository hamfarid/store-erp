<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/ModuleManager.vue -->
<template>
  <div class="module-manager">
    <div class="page-header">
      <h1>{{ $t('settings.moduleManager.title') }}</h1>
    </div>

    <div class="search-box">
      <label for="module-search" class="block text-sm font-medium text-gray-700">
        {{ $t('module.search') }}
      </label>
      <input
        id="module-search"
        v-model="searchQuery"
        type="text"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
        :placeholder="$t('module.search_placeholder')"
      />
    </div>

    <div class="modules-grid">
      <div v-for="module in modules" :key="module.id" class="module-card">
        <div class="module-header">
          <div class="module-icon">
            <i :class="module.icon || 'fas fa-puzzle-piece'"></i>
          </div>
          <div class="module-title">
            <h3>{{ module.name }}</h3>
            <div class="module-status">
              <span :class="['status-badge', module.is_active ? 'active' : 'inactive']">
                {{ module.is_active ? $t('settings.moduleManager.active') : $t('settings.moduleManager.inactive') }}
              </span>
            </div>
          </div>
          <div class="module-toggle">
            <label class="switch">
              <input 
                type="checkbox" 
                :checked="module.is_active" 
                @change="toggleModule(module)"
                :disabled="module.is_core || isProcessing"
              />
              <span class="slider"></span>
            </label>
          </div>
        </div>
        <div class="module-body">
          <p class="module-description">{{ module.description }}</p>
          <div class="module-details">
            <div class="detail-item">
              <span class="label">{{ $t('settings.moduleManager.version') }}:</span>
              <span class="value">{{ module.version }}</span>
            </div>
            <div class="detail-item">
              <span class="label">{{ $t('settings.moduleManager.type') }}:</span>
              <span class="value">{{ getModuleTypeLabel(module.type) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">{{ $t('settings.moduleManager.dependencies') }}:</span>
              <span class="value">{{ module.dependencies.length || $t('settings.moduleManager.none') }}</span>
            </div>
          </div>
        </div>
        <div class="module-footer">
          <button 
            class="btn btn-sm btn-settings" 
            @click="openModuleSettings(module)"
            :disabled="!module.has_settings || !module.is_active"
          >
            <i class="fas fa-cog"></i> {{ $t('settings.moduleManager.settings') }}
          </button>
          <button 
            class="btn btn-sm btn-info" 
            @click="showModuleInfo(module)"
          >
            <i class="fas fa-info-circle"></i> {{ $t('settings.moduleManager.info') }}
          </button>
          <button 
            class="btn btn-sm btn-update" 
            @click="checkForUpdates(module)"
            :disabled="isProcessing"
          >
            <i class="fas fa-sync"></i> {{ $t('settings.moduleManager.checkUpdates') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Module Info Modal -->
    <div class="modal" v-if="showInfoModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ selectedModule ? selectedModule.name : '' }}</h2>
          <button class="close-btn" @click="closeInfoModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="module-info">
            <div class="info-section">
              <h3>{{ $t('settings.moduleManager.generalInfo') }}</h3>
              <div class="info-item">
                <span class="label">{{ $t('settings.moduleManager.description') }}:</span>
                <span class="value">{{ selectedModule ? selectedModule.description : '' }}</span>
              </div>
              <div class="info-item">
                <span class="label">{{ $t('settings.moduleManager.version') }}:</span>
                <span class="value">{{ selectedModule ? selectedModule.version : '' }}</span>
              </div>
              <div class="info-item">
                <span class="label">{{ $t('settings.moduleManager.author') }}:</span>
                <span class="value">{{ selectedModule ? selectedModule.author : '' }}</span>
              </div>
              <div class="info-item">
                <span class="label">{{ $t('settings.moduleManager.license') }}:</span>
                <span class="value">{{ selectedModule ? selectedModule.license : '' }}</span>
              </div>
            </div>

            <div class="info-section">
              <h3>{{ $t('settings.moduleManager.technicalInfo') }}</h3>
              <div class="info-item">
                <span class="label">{{ $t('settings.moduleManager.type') }}:</span>
                <span class="value">{{ selectedModule ? getModuleTypeLabel(selectedModule.type) : '' }}</span>
              </div>
              <div class="info-item">
                <span class="label">{{ $t('settings.moduleManager.path') }}:</span>
                <span class="value">{{ selectedModule ? selectedModule.path : '' }}</span>
              </div>
              <div class="info-item">
                <span class="label">{{ $t('settings.moduleManager.entryPoint') }}:</span>
                <span class="value">{{ selectedModule ? selectedModule.entry_point : '' }}</span>
              </div>
              <div class="info-item">
                <span class="label">{{ $t('settings.moduleManager.isCore') }}:</span>
                <span class="value">{{ selectedModule ? (selectedModule.is_core ? $t('common.yes') : $t('common.no')) : '' }}</span>
              </div>
            </div>

            <div class="info-section">
              <h3>{{ $t('settings.moduleManager.dependencies') }}</h3>
              <div v-if="selectedModule && selectedModule.dependencies.length > 0">
                <ul class="dependencies-list">
                  <li v-for="dep in selectedModule.dependencies" :key="dep.id">
                    <span class="dependency-name">{{ dep.name }}</span>
                    <span class="dependency-version">{{ dep.version }}</span>
                    <span 
                      :class="['dependency-status', getDependencyStatusClass(dep.status)]"
                    >
                      {{ getDependencyStatusLabel(dep.status) }}
                    </span>
                  </li>
                </ul>
              </div>
              <div v-else class="no-dependencies">
                {{ $t('settings.moduleManager.noDependencies') }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Module Settings Modal -->
    <div class="modal" v-if="showSettingsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ $t('settings.moduleManager.moduleSettings', { name: selectedModule ? selectedModule.name : '' }) }}</h2>
          <button class="close-btn" @click="closeSettingsModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="module-settings">
            <div v-if="moduleSettings.length > 0">
              <form @submit.prevent="saveModuleSettings">
                <div 
                  v-for="setting in moduleSettings" 
                  :key="setting.key" 
                  class="form-group"
                >
                  <label :for="'setting-' + setting.key">{{ setting.label }}</label>
                  
                  <!-- Text input -->
                  <input 
                    v-if="setting.type === 'text'" 
                    type="text" 
                    :id="'setting-' + setting.key" 
                    v-model="setting.value"
                    :placeholder="setting.placeholder"
                  />
                  
                  <!-- Number input -->
                  <input 
                    v-if="setting.type === 'number'" 
                    type="number" 
                    :id="'setting-' + setting.key" 
                    v-model.number="setting.value"
                    :min="setting.min"
                    :max="setting.max"
                    :step="setting.step"
                  />
                  
                  <!-- Boolean input -->
                  <div v-if="setting.type === 'boolean'" class="checkbox-option">
                    <input 
                      type="checkbox" 
                      :id="'setting-' + setting.key" 
                      v-model="setting.value"
                    />
                    <label :for="'setting-' + setting.key">{{ setting.checkboxLabel }}</label>
                  </div>
                  
                  <!-- Select input -->
                  <select 
                    v-if="setting.type === 'select'" 
                    :id="'setting-' + setting.key" 
                    v-model="setting.value"
                  >
                    <option 
                      v-for="option in setting.options" 
                      :key="option.value" 
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                  
                  <!-- Textarea input -->
                  <textarea 
                    v-if="setting.type === 'textarea'" 
                    :id="'setting-' + setting.key" 
                    v-model="setting.value"
                    :rows="setting.rows || 3"
                    :placeholder="setting.placeholder"
                  ></textarea>
                  
                  <div class="form-hint" v-if="setting.hint">{{ setting.hint }}</div>
                </div>
                
                <div class="form-actions">
                  <button type="button" class="btn btn-secondary" @click="resetModuleSettings">
                    {{ $t('common.reset') }}
                  </button>
                  <button type="submit" class="btn btn-primary">
                    {{ $t('common.save') }}
                  </button>
                </div>
              </form>
            </div>
            <div v-else class="no-settings">
              {{ $t('settings.moduleManager.noSettings') }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div class="modal" v-if="showConfirmationModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ confirmationTitle }}</h2>
          <button class="close-btn" @click="closeConfirmationModal">&times;</button>
        </div>
        <div class="modal-body">
          <p>{{ confirmationMessage }}</p>
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeConfirmationModal">
              {{ $t('common.cancel') }}
            </button>
            <button type="button" class="btn btn-danger" @click="confirmAction">
              {{ $t('common.confirm') }}
            </button>
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
import { useToast } from '@/composables/useToast';
import moduleService from '@/services/moduleService';
import { defineComponent, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default defineComponent({
  name: 'ModuleManager',
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    
    // Data
    const modules = ref([]);
    const selectedModule = ref(null);
    const moduleSettings = ref([]);
    const originalSettings = ref([]);
    
    // Modal states
    const showInfoModal = ref(false);
    const showSettingsModal = ref(false);
    const showConfirmationModal = ref(false);
    const isProcessing = ref(false);
    
    const confirmationTitle = ref('');
    const confirmationMessage = ref('');
    const confirmationCallback = ref(null);
    
    const processingTitle = ref('');
    const processingMessage = ref('');
    
    // Fetch data
    const fetchModules = async () => {
      try {
        const response = await moduleService.getModules();
        modules.value = response.data;
      } catch (error) {
        showToast(t('settings.moduleManager.errorFetchingModules'), 'error');
        console.error('Error fetching modules:', error);
      }
    };
    
    // Module actions
    const toggleModule = (module) => {
      if (module.is_core) {
        showToast(t('settings.moduleManager.cannotDisableCoreModule'), 'error');
        return;
      }
      
      const newStatus = !module.is_active;
      
      confirmationTitle.value = newStatus 
        ? t('settings.moduleManager.activateModule') 
        : t('settings.moduleManager.deactivateModule');
      
      confirmationMessage.value = newStatus 
        ? t('settings.moduleManager.activateModuleConfirmation', { name: module.name }) 
        : t('settings.moduleManager.deactivateModuleConfirmation', { name: module.name });
      
      confirmationCallback.value = async () => {
        isProcessing.value = true;
        processingTitle.value = newStatus 
          ? t('settings.moduleManager.activatingModule') 
          : t('settings.moduleManager.deactivatingModule');
        processingMessage.value = newStatus 
          ? t('settings.moduleManager.activatingModuleMessage', { name: module.name }) 
          : t('settings.moduleManager.deactivatingModuleMessage', { name: module.name });
        
        try {
          await moduleService.toggleModule(module.id, newStatus);
          module.is_active = newStatus;
          
          showToast(
            newStatus 
              ? t('settings.moduleManager.moduleActivated', { name: module.name }) 
              : t('settings.moduleManager.moduleDeactivated', { name: module.name }), 
            'success'
          );
        } catch (error) {
          showToast(t('settings.moduleManager.errorTogglingModule'), 'error');
          console.error('Error toggling module:', error);
        } finally {
          isProcessing.value = false;
          closeConfirmationModal();
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    const showModuleInfo = (module) => {
      selectedModule.value = module;
      showInfoModal.value = true;
    };
    
    const openModuleSettings = async (module) => {
      if (!module.has_settings || !module.is_active) {
        return;
      }
      
      selectedModule.value = module;
      isProcessing.value = true;
      processingTitle.value = t('settings.moduleManager.loadingSettings');
      processingMessage.value = t('settings.moduleManager.loadingSettingsMessage', { name: module.name });
      
      try {
        const response = await moduleService.getModuleSettings(module.id);
        moduleSettings.value = response.data;
        originalSettings.value = JSON.parse(JSON.stringify(response.data)); // Deep copy
        showSettingsModal.value = true;
      } catch (error) {
        showToast(t('settings.moduleManager.errorLoadingSettings'), 'error');
        console.error('Error loading module settings:', error);
      } finally {
        isProcessing.value = false;
      }
    };
    
    const saveModuleSettings = async () => {
      if (!selectedModule.value) return;
      
      isProcessing.value = true;
      processingTitle.value = t('settings.moduleManager.savingSettings');
      processingMessage.value = t('settings.moduleManager.savingSettingsMessage', { name: selectedModule.value.name });
      
      try {
        // Convert settings to key-value pairs
        const settingsData = moduleSettings.value.reduce((acc, setting) => {
          acc[setting.key] = setting.value;
          return acc;
        }, {});
        
        await moduleService.saveModuleSettings(selectedModule.value.id, settingsData);
        
        // Update original settings
        originalSettings.value = JSON.parse(JSON.stringify(moduleSettings.value));
        
        showToast(t('settings.moduleManager.settingsSaved'), 'success');
        closeSettingsModal();
      } catch (error) {
        showToast(t('settings.moduleManager.errorSavingSettings'), 'error');
        console.error('Error saving module settings:', error);
      } finally {
        isProcessing.value = false;
      }
    };
    
    const resetModuleSettings = () => {
      moduleSettings.value = JSON.parse(JSON.stringify(originalSettings.value));
    };
    
    const checkForUpdates = async (module) => {
      isProcessing.value = true;
      processingTitle.value = t('settings.moduleManager.checkingUpdates');
      processingMessage.value = t('settings.moduleManager.checkingUpdatesMessage', { name: module.name });
      
      try {
        const response = await moduleService.checkForUpdates(module.id);
        
        if (response.data.has_update) {
          confirmationTitle.value = t('settings.moduleManager.updateAvailable');
          confirmationMessage.value = t('settings.moduleManager.updateAvailableMessage', { 
            name: module.name,
            currentVersion: module.version,
            newVersion: response.data.new_version
          });
          
          confirmationCallback.value = async () => {
            isProcessing.value = true;
            processingTitle.value = t('settings.moduleManager.updatingModule');
            processingMessage.value = t('settings.moduleManager.updatingModuleMessage', { name: module.name });
            
            try {
              await moduleService.updateModule(module.id);
              
              // Update module version
              module.version = response.data.new_version;
              
              showToast(t('settings.moduleManager.moduleUpdated', { name: module.name }), 'success');
            } catch (error) {
              showToast(t('settings.moduleManager.errorUpdatingModule'), 'error');
              console.error('Error updating module:', error);
            } finally {
              isProcessing.value = false;
              closeConfirmationModal();
            }
          };
          
          isProcessing.value = false;
          showConfirmationModal.value = true;
        } else {
          isProcessing.value = false;
          showToast(t('settings.moduleManager.noUpdatesAvailable', { name: module.name }), 'info');
        }
      } catch (error) {
        isProcessing.value = false;
        showToast(t('settings.moduleManager.errorCheckingUpdates'), 'error');
        console.error('Error checking for updates:', error);
      }
    };
    
    const confirmAction = () => {
      if (confirmationCallback.value) {
        confirmationCallback.value();
      }
    };
    
    // Modal helpers
    const closeInfoModal = () => {
      showInfoModal.value = false;
      selectedModule.value = null;
    };
    
    const closeSettingsModal = () => {
      showSettingsModal.value = false;
      selectedModule.value = null;
      moduleSettings.value = [];
      originalSettings.value = [];
    };
    
    const closeConfirmationModal = () => {
      showConfirmationModal.value = false;
      confirmationTitle.value = '';
      confirmationMessage.value = '';
      confirmationCallback.value = null;
    };
    
    // Utility functions
    const getModuleTypeLabel = (type) => {
      switch (type) {
        case 'core':
          return t('settings.moduleManager.typeCore');
        case 'business':
          return t('settings.moduleManager.typeBusiness');
        case 'service':
          return t('settings.moduleManager.typeService');
        case 'integration':
          return t('settings.moduleManager.typeIntegration');
        case 'utility':
          return t('settings.moduleManager.typeUtility');
        case 'ai':
          return t('settings.moduleManager.typeAI');
        default:
          return type;
      }
    };
    
    const getDependencyStatusLabel = (status) => {
      switch (status) {
        case 'installed':
          return t('settings.moduleManager.dependencyInstalled');
        case 'missing':
          return t('settings.moduleManager.dependencyMissing');
        case 'version_mismatch':
          return t('settings.moduleManager.dependencyVersionMismatch');
        default:
          return status;
      }
    };
    
    const getDependencyStatusClass = (status) => {
      switch (status) {
        case 'installed':
          return 'installed';
        case 'missing':
          return 'missing';
        case 'version_mismatch':
          return 'version-mismatch';
        default:
          return '';
      }
    };
    
    // Lifecycle hooks
    onMounted(async () => {
      await fetchModules();
    });
    
    return {
      modules,
      selectedModule,
      moduleSettings,
      showInfoModal,
      showSettingsModal,
      showConfirmationModal,
      isProcessing,
      confirmationTitle,
      confirmationMessage,
      processingTitle,
      processingMessage,
      toggleModule,
      showModuleInfo,
      openModuleSettings,
      saveModuleSettings,
      resetModuleSettings,
      checkForUpdates,
      confirmAction,
      closeInfoModal,
      closeSettingsModal,
      closeConfirmationModal,
      getModuleTypeLabel,
      getDependencyStatusLabel,
      getDependencyStatusClass
    };
  }
});
</script>

<style scoped>
.module-manager {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.module-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.module-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.module-header {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
}

.module-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #e9ecef;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 10px;
}

.module-icon i {
  font-size: 1.2rem;
  color: #495057;
}

.module-title {
  flex: 1;
}

.module-title h3 {
  margin: 0;
  font-size: 1.1rem;
}

.module-status {
  margin-top: 5px;
}

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75em;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.module-toggle {
  margin-right: 10px;
}

/* Toggle switch */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #28a745;
}

input:focus + .slider {
  box-shadow: 0 0 1px #28a745;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

input:disabled + .slider {
  opacity: 0.5;
  cursor: not-allowed;
}

.module-body {
  padding: 15px;
}

.module-description {
  margin-top: 0;
  margin-bottom: 15px;
  color: #6c757d;
  height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.module-details {
  margin-bottom: 15px;
}

.detail-item {
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.detail-item .label {
  font-weight: bold;
  margin-left: 5px;
}

.module-footer {
  display: flex;
  justify-content: space-between;
  padding: 10px 15px;
  background-color: #f8f9fa;
  border-top: 1px solid #ddd;
}

.btn {
  cursor: pointer;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 0.85em;
}

.btn-settings {
  background-color: #17a2b8;
  color: white;
}

.btn-info {
  background-color: #6c757d;
  color: white;
}

.btn-update {
  background-color: #28a745;
  color: white;
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
  width: 600px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
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
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

/* Module info styles */
.module-info {
  margin-bottom: 20px;
}

.info-section {
  margin-bottom: 20px;
}

.info-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1.1rem;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

.info-item {
  margin-bottom: 5px;
}

.info-item .label {
  font-weight: bold;
  margin-left: 5px;
}

.dependencies-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.dependencies-list li {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.dependency-name {
  font-weight: bold;
  margin-left: 5px;
}

.dependency-version {
  margin: 0 10px;
  color: #6c757d;
}

.dependency-status {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75em;
}

.dependency-status.installed {
  background-color: #d4edda;
  color: #155724;
}

.dependency-status.missing {
  background-color: #f8d7da;
  color: #721c24;
}

.dependency-status.version-mismatch {
  background-color: #fff3cd;
  color: #856404;
}

.no-dependencies {
  color: #6c757d;
  font-style: italic;
}

/* Module settings styles */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-hint {
  font-size: 0.85em;
  color: #6c757d;
  margin-top: 5px;
}

.checkbox-option {
  display: flex;
  align-items: center;
}

.checkbox-option input {
  width: auto;
  margin-left: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.no-settings {
  color: #6c757d;
  font-style: italic;
  text-align: center;
  padding: 20px;
}

/* Loading spinner */
.loading-spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-radius: 50%;
  border-top: 5px solid #007bff;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* RTL support */
html[dir="rtl"] .module-icon {
  margin-left: 0;
  margin-right: 10px;
}

html[dir="rtl"] .module-toggle {
  margin-right: 0;
  margin-left: 10px;
}

html[dir="rtl"] .detail-item .label,
html[dir="rtl"] .info-item .label,
html[dir="rtl"] .dependency-name {
  margin-left: 0;
  margin-right: 5px;
}

html[dir="rtl"] .checkbox-option input {
  margin-left: 0;
  margin-right: 8px;
}
</style>
