<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/BackupRestore.vue -->
<template>
  <div class="backup-restore">
    <div class="page-header">
      <h1>{{ $t('settings.backupRestore.title') }}</h1>
    </div>

    <div class="tabs">
      <div 
        class="tab" 
        :class="{ active: activeTab === 'backup' }" 
        @click="activeTab = 'backup'"
      >
        {{ $t('settings.backupRestore.backup') }}
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'restore' }" 
        @click="activeTab = 'restore'"
      >
        {{ $t('settings.backupRestore.restore') }}
      </div>
    </div>

    <!-- Backup Tab -->
    <div class="tab-content" v-if="activeTab === 'backup'">
      <div class="card">
        <h2>{{ $t('settings.backupRestore.createBackup') }}</h2>
        
        <div class="form-group">
          <label>{{ $t('settings.backupRestore.backupType') }}</label>
          <div class="radio-group">
            <div class="radio-option">
              <input type="radio" id="full-backup" value="full" v-model="backupType" />
              <label for="full-backup">{{ $t('settings.backupRestore.fullBackup') }}</label>
            </div>
            <div class="radio-option">
              <input type="radio" id="database-backup" value="database" v-model="backupType" />
              <label for="database-backup">{{ $t('settings.backupRestore.databaseBackup') }}</label>
            </div>
            <div class="radio-option">
              <input type="radio" id="settings-backup" value="settings" v-model="backupType" />
              <label for="settings-backup">{{ $t('settings.backupRestore.settingsBackup') }}</label>
            </div>
            <div class="radio-option">
              <input type="radio" id="learning-data-backup" value="learning" v-model="backupType" />
              <label for="learning-data-backup">{{ $t('settings.backupRestore.learningDataBackup') }}</label>
            </div>
          </div>
        </div>

        <div class="form-group" v-if="backupType === 'database'">
          <label>{{ $t('settings.backupRestore.selectModules') }}</label>
          <div class="checkbox-group">
            <div class="checkbox-option">
              <input type="checkbox" id="all-modules" v-model="allModulesSelected" @change="toggleAllModules" />
              <label for="all-modules">{{ $t('settings.backupRestore.allModules') }}</label>
            </div>
            <div class="checkbox-option" v-for="module in availableModules" :key="module.id">
              <input 
                type="checkbox" 
                :id="'module-' + module.id" 
                :value="module.id" 
                v-model="selectedModules"
                @change="updateAllModulesState"
              />
              <label :for="'module-' + module.id">{{ module.name }}</label>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="backup-name">{{ $t('settings.backupRestore.backupName') }}</label>
          <input 
            type="text" 
            id="backup-name" 
            v-model="backupName" 
            :placeholder="$t('settings.backupRestore.backupNamePlaceholder')"
          />
          <div class="form-hint">{{ $t('settings.backupRestore.backupNameHint') }}</div>
        </div>

        <div class="form-group">
          <label for="backup-description">{{ $t('settings.backupRestore.description') }}</label>
          <textarea 
            id="backup-description" 
            v-model="backupDescription" 
            rows="3"
            :placeholder="$t('settings.backupRestore.descriptionPlaceholder')"
          ></textarea>
        </div>

        <div class="form-actions">
          <button 
            class="btn btn-primary" 
            @click="createBackup" 
            :disabled="isProcessing"
          >
            <i class="fas fa-download"></i> {{ $t('settings.backupRestore.createBackup') }}
          </button>
        </div>
      </div>

      <div class="card">
        <h2>{{ $t('settings.backupRestore.backupHistory') }}</h2>
        
        <div class="filters">
          <div class="search">
            <input 
              type="text" 
              v-model="searchQuery" 
              :placeholder="$t('common.search')" 
              @input="filterBackups"
            />
          </div>
          <div class="filter-type">
            <select v-model="typeFilter" @change="filterBackups">
              <option value="">{{ $t('settings.backupRestore.allTypes') }}</option>
              <option value="full">{{ $t('settings.backupRestore.fullBackup') }}</option>
              <option value="database">{{ $t('settings.backupRestore.databaseBackup') }}</option>
              <option value="settings">{{ $t('settings.backupRestore.settingsBackup') }}</option>
              <option value="learning">{{ $t('settings.backupRestore.learningDataBackup') }}</option>
            </select>
          </div>
        </div>

        <div class="backup-list">
          <table>
            <thead>
              <tr>
                <th>{{ $t('settings.backupRestore.name') }}</th>
                <th>{{ $t('settings.backupRestore.type') }}</th>
                <th>{{ $t('settings.backupRestore.date') }}</th>
                <th>{{ $t('settings.backupRestore.size') }}</th>
                <th>{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="backup in filteredBackups" :key="backup.id">
                <td>
                  <div class="backup-name">{{ backup.name }}</div>
                  <div class="backup-description">{{ backup.description }}</div>
                </td>
                <td>{{ getBackupTypeLabel(backup.type) }}</td>
                <td>{{ formatDate(backup.created_at) }}</td>
                <td>{{ formatSize(backup.size) }}</td>
                <td class="actions">
                  <button class="btn btn-sm btn-download" @click="downloadBackup(backup)">
                    <i class="fas fa-download"></i>
                  </button>
                  <button class="btn btn-sm btn-restore" @click="prepareRestore(backup)">
                    <i class="fas fa-undo"></i>
                  </button>
                  <button class="btn btn-sm btn-delete" @click="deleteBackup(backup)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Restore Tab -->
    <div class="tab-content" v-if="activeTab === 'restore'">
      <div class="card">
        <h2>{{ $t('settings.backupRestore.restoreFromFile') }}</h2>
        
        <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleFileDrop">
          <input 
            type="file" 
            ref="fileInput" 
            style="display: none" 
            @change="handleFileSelect" 
            accept=".zip,.tar.gz,.gz"
          />
          <i class="fas fa-cloud-upload-alt"></i>
          <p>{{ $t('settings.backupRestore.dragDropHint') }}</p>
          <button class="btn btn-secondary">{{ $t('settings.backupRestore.browseFiles') }}</button>
        </div>

        <div class="selected-file" v-if="selectedFile">
          <div class="file-info">
            <i class="fas fa-file-archive"></i>
            <div class="file-details">
              <div class="file-name">{{ selectedFile.name }}</div>
              <div class="file-size">{{ formatSize(selectedFile.size) }}</div>
            </div>
          </div>
          <button class="btn btn-sm btn-delete" @click="clearSelectedFile">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="form-actions" v-if="selectedFile">
          <button 
            class="btn btn-primary" 
            @click="restoreFromFile" 
            :disabled="isProcessing"
          >
            <i class="fas fa-undo"></i> {{ $t('settings.backupRestore.restoreFromFile') }}
          </button>
        </div>
      </div>

      <div class="card">
        <h2>{{ $t('settings.backupRestore.availableBackups') }}</h2>
        
        <div class="filters">
          <div class="search">
            <input 
              type="text" 
              v-model="searchQuery" 
              :placeholder="$t('common.search')" 
              @input="filterBackups"
            />
          </div>
          <div class="filter-type">
            <select v-model="typeFilter" @change="filterBackups">
              <option value="">{{ $t('settings.backupRestore.allTypes') }}</option>
              <option value="full">{{ $t('settings.backupRestore.fullBackup') }}</option>
              <option value="database">{{ $t('settings.backupRestore.databaseBackup') }}</option>
              <option value="settings">{{ $t('settings.backupRestore.settingsBackup') }}</option>
              <option value="learning">{{ $t('settings.backupRestore.learningDataBackup') }}</option>
            </select>
          </div>
        </div>

        <div class="backup-list">
          <table>
            <thead>
              <tr>
                <th>{{ $t('settings.backupRestore.name') }}</th>
                <th>{{ $t('settings.backupRestore.type') }}</th>
                <th>{{ $t('settings.backupRestore.date') }}</th>
                <th>{{ $t('settings.backupRestore.size') }}</th>
                <th>{{ $t('common.actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="backup in filteredBackups" :key="backup.id">
                <td>
                  <div class="backup-name">{{ backup.name }}</div>
                  <div class="backup-description">{{ backup.description }}</div>
                </td>
                <td>{{ getBackupTypeLabel(backup.type) }}</td>
                <td>{{ formatDate(backup.created_at) }}</td>
                <td>{{ formatSize(backup.size) }}</td>
                <td class="actions">
                  <button class="btn btn-sm btn-restore" @click="prepareRestore(backup)">
                    <i class="fas fa-undo"></i> {{ $t('settings.backupRestore.restore') }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
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
          <div class="progress-bar" v-if="showProgress">
            <div class="progress" :style="{ width: `${progress}%` }"></div>
          </div>
          <div class="progress-text" v-if="showProgress">
            {{ progress }}%
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
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast';
import backupService from '@/services/backupService';
import moduleService from '@/services/moduleService';
import { defineComponent, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default defineComponent({
  name: 'BackupRestore',
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    
    // Data
    const activeTab = ref('backup');
    const backups = ref([]);
    const filteredBackups = ref([]);
    const availableModules = ref([]);
    const searchQuery = ref('');
    const typeFilter = ref('');
    
    // Backup form
    const backupType = ref('full');
    const selectedModules = ref([]);
    const allModulesSelected = ref(false);
    const backupName = ref('');
    const backupDescription = ref('');
    
    // Restore form
    const fileInput = ref(null);
    const selectedFile = ref(null);
    
    // Modal states
    const isProcessing = ref(false);
    const processingTitle = ref('');
    const processingMessage = ref('');
    const showProgress = ref(false);
    const progress = ref(0);
    
    const showConfirmationModal = ref(false);
    const confirmationTitle = ref('');
    const confirmationMessage = ref('');
    const confirmationCallback = ref(null);
    
    // Fetch data
    const fetchBackups = async () => {
      try {
        const response = await backupService.getBackups();
        backups.value = response.data;
        filteredBackups.value = [...backups.value];
      } catch (error) {
        showToast(t('settings.backupRestore.errorFetchingBackups'), 'error');
        console.error('Error fetching backups:', error);
      }
    };
    
    const fetchModules = async () => {
      try {
        const response = await moduleService.getModules();
        availableModules.value = response.data;
      } catch (error) {
        showToast(t('settings.backupRestore.errorFetchingModules'), 'error');
        console.error('Error fetching modules:', error);
      }
    };
    
    // Filter backups
    const filterBackups = () => {
      filteredBackups.value = backups.value.filter(backup => {
        const matchesSearch = searchQuery.value === '' || 
          backup.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          backup.description.toLowerCase().includes(searchQuery.value.toLowerCase());
        
        const matchesType = typeFilter.value === '' || backup.type === typeFilter.value;
        
        return matchesSearch && matchesType;
      });
    };
    
    // Module selection
    const toggleAllModules = () => {
      if (allModulesSelected.value) {
        selectedModules.value = availableModules.value.map(module => module.id);
      } else {
        selectedModules.value = [];
      }
    };
    
    const updateAllModulesState = () => {
      allModulesSelected.value = selectedModules.value.length === availableModules.value.length;
    };
    
    // Backup actions
    const createBackup = async () => {
      // Validate form
      if (backupType.value === 'database' && selectedModules.value.length === 0) {
        showToast(t('settings.backupRestore.selectAtLeastOneModule'), 'error');
        return;
      }
      
      // Set default backup name if not provided
      if (!backupName.value) {
        const date = new Date();
        const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        backupName.value = `${backupType.value}_backup_${formattedDate}`;
      }
      
      // Show processing modal
      isProcessing.value = true;
      processingTitle.value = t('settings.backupRestore.creatingBackup');
      processingMessage.value = t('settings.backupRestore.creatingBackupMessage');
      showProgress.value = true;
      progress.value = 0;
      
      try {
        // Start backup process
        const backupData = {
          type: backupType.value,
          name: backupName.value,
          description: backupDescription.value,
          modules: backupType.value === 'database' ? selectedModules.value : []
        };
        
        const response = await backupService.createBackup(backupData);
        
        // Poll for backup progress
        const backupId = response.data.id;
        const progressInterval = setInterval(async () => {
          try {
            const progressResponse = await backupService.getBackupProgress(backupId);
            progress.value = progressResponse.data.progress;
            
            if (progressResponse.data.status === 'completed') {
              clearInterval(progressInterval);
              
              // Refresh backup list
              await fetchBackups();
              
              // Reset form
              backupName.value = '';
              backupDescription.value = '';
              
              // Hide processing modal
              isProcessing.value = false;
              
              showToast(t('settings.backupRestore.backupCreated'), 'success');
            } else if (progressResponse.data.status === 'failed') {
              clearInterval(progressInterval);
              isProcessing.value = false;
              showToast(t('settings.backupRestore.backupFailed') + ': ' + progressResponse.data.error, 'error');
            }
          } catch (error) {
            clearInterval(progressInterval);
            isProcessing.value = false;
            showToast(t('settings.backupRestore.errorCheckingProgress'), 'error');
            console.error('Error checking backup progress:', error);
          }
        }, 2000);
      } catch (error) {
        isProcessing.value = false;
        showToast(t('settings.backupRestore.errorCreatingBackup'), 'error');
        console.error('Error creating backup:', error);
      }
    };
    
    const downloadBackup = async (backup) => {
      try {
        const response = await backupService.downloadBackup(backup.id);
        
        // Create a download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${backup.name}.${getBackupExtension(backup.type)}`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        showToast(t('settings.backupRestore.errorDownloadingBackup'), 'error');
        console.error('Error downloading backup:', error);
      }
    };
    
    const deleteBackup = (backup) => {
      confirmationTitle.value = t('settings.backupRestore.deleteBackup');
      confirmationMessage.value = t('settings.backupRestore.deleteBackupConfirmation', { name: backup.name });
      
      confirmationCallback.value = async () => {
        try {
          await backupService.deleteBackup(backup.id);
          backups.value = backups.value.filter(b => b.id !== backup.id);
          filteredBackups.value = filteredBackups.value.filter(b => b.id !== backup.id);
          showToast(t('settings.backupRestore.backupDeleted'), 'success');
          closeConfirmationModal();
        } catch (error) {
          showToast(t('settings.backupRestore.errorDeletingBackup'), 'error');
          console.error('Error deleting backup:', error);
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    // Restore actions
    const triggerFileInput = () => {
      fileInput.value.click();
    };
    
    const handleFileSelect = (event) => {
      const file = event.target.files[0];
      if (file) {
        selectedFile.value = file;
      }
    };
    
    const handleFileDrop = (event) => {
      const file = event.dataTransfer.files[0];
      if (file) {
        selectedFile.value = file;
      }
    };
    
    const clearSelectedFile = () => {
      selectedFile.value = null;
      fileInput.value.value = '';
    };
    
    const restoreFromFile = async () => {
      confirmationTitle.value = t('settings.backupRestore.restoreBackup');
      confirmationMessage.value = t('settings.backupRestore.restoreBackupConfirmation');
      
      confirmationCallback.value = async () => {
        // Show processing modal
        isProcessing.value = true;
        processingTitle.value = t('settings.backupRestore.restoringBackup');
        processingMessage.value = t('settings.backupRestore.restoringBackupMessage');
        showProgress.value = true;
        progress.value = 0;
        
        try {
          const formData = new FormData();
          formData.append('file', selectedFile.value);
          
          const response = await backupService.restoreFromFile(formData);
          
          // Poll for restore progress
          const restoreId = response.data.id;
          const progressInterval = setInterval(async () => {
            try {
              const progressResponse = await backupService.getRestoreProgress(restoreId);
              progress.value = progressResponse.data.progress;
              
              if (progressResponse.data.status === 'completed') {
                clearInterval(progressInterval);
                
                // Reset form
                clearSelectedFile();
                
                // Hide processing modal
                isProcessing.value = false;
                
                showToast(t('settings.backupRestore.restoreCompleted'), 'success');
              } else if (progressResponse.data.status === 'failed') {
                clearInterval(progressInterval);
                isProcessing.value = false;
                showToast(t('settings.backupRestore.restoreFailed') + ': ' + progressResponse.data.error, 'error');
              }
            } catch (error) {
              clearInterval(progressInterval);
              isProcessing.value = false;
              showToast(t('settings.backupRestore.errorCheckingProgress'), 'error');
              console.error('Error checking restore progress:', error);
            }
          }, 2000);
        } catch (error) {
          isProcessing.value = false;
          showToast(t('settings.backupRestore.errorRestoringBackup'), 'error');
          console.error('Error restoring backup:', error);
        }
        
        closeConfirmationModal();
      };
      
      showConfirmationModal.value = true;
    };
    
    const prepareRestore = (backup) => {
      confirmationTitle.value = t('settings.backupRestore.restoreBackup');
      confirmationMessage.value = t('settings.backupRestore.restoreBackupConfirmation');
      
      confirmationCallback.value = async () => {
        // Show processing modal
        isProcessing.value = true;
        processingTitle.value = t('settings.backupRestore.restoringBackup');
        processingMessage.value = t('settings.backupRestore.restoringBackupMessage');
        showProgress.value = true;
        progress.value = 0;
        
        try {
          const response = await backupService.restoreBackup(backup.id);
          
          // Poll for restore progress
          const restoreId = response.data.id;
          const progressInterval = setInterval(async () => {
            try {
              const progressResponse = await backupService.getRestoreProgress(restoreId);
              progress.value = progressResponse.data.progress;
              
              if (progressResponse.data.status === 'completed') {
                clearInterval(progressInterval);
                
                // Hide processing modal
                isProcessing.value = false;
                
                showToast(t('settings.backupRestore.restoreCompleted'), 'success');
              } else if (progressResponse.data.status === 'failed') {
                clearInterval(progressInterval);
                isProcessing.value = false;
                showToast(t('settings.backupRestore.restoreFailed') + ': ' + progressResponse.data.error, 'error');
              }
            } catch (error) {
              clearInterval(progressInterval);
              isProcessing.value = false;
              showToast(t('settings.backupRestore.errorCheckingProgress'), 'error');
              console.error('Error checking restore progress:', error);
            }
          }, 2000);
        } catch (error) {
          isProcessing.value = false;
          showToast(t('settings.backupRestore.errorRestoringBackup'), 'error');
          console.error('Error restoring backup:', error);
        }
        
        closeConfirmationModal();
      };
      
      showConfirmationModal.value = true;
    };
    
    const confirmAction = () => {
      if (confirmationCallback.value) {
        confirmationCallback.value();
      }
    };
    
    // Modal helpers
    const closeConfirmationModal = () => {
      showConfirmationModal.value = false;
      confirmationTitle.value = '';
      confirmationMessage.value = '';
      confirmationCallback.value = null;
    };
    
    // Utility functions
    const getBackupTypeLabel = (type) => {
      switch (type) {
        case 'full':
          return t('settings.backupRestore.fullBackup');
        case 'database':
          return t('settings.backupRestore.databaseBackup');
        case 'settings':
          return t('settings.backupRestore.settingsBackup');
        case 'learning':
          return t('settings.backupRestore.learningDataBackup');
        default:
          return type;
      }
    };
    
    const getBackupExtension = (type) => {
      switch (type) {
        case 'full':
          return 'tar.gz';
        case 'database':
          return 'sql.gz';
        case 'settings':
          return 'tar.gz';
        case 'learning':
          return 'zip';
        default:
          return 'zip';
      }
    };
    
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('ar-SA', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };
    
    const formatSize = (bytes) => {
      if (bytes === 0) return '0 Bytes';
      
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    // Lifecycle hooks
    onMounted(async () => {
      await Promise.all([fetchBackups(), fetchModules()]);
    });
    
    return {
      activeTab,
      backups,
      filteredBackups,
      availableModules,
      searchQuery,
      typeFilter,
      backupType,
      selectedModules,
      allModulesSelected,
      backupName,
      backupDescription,
      fileInput,
      selectedFile,
      isProcessing,
      processingTitle,
      processingMessage,
      showProgress,
      progress,
      showConfirmationModal,
      confirmationTitle,
      confirmationMessage,
      filterBackups,
      toggleAllModules,
      updateAllModulesState,
      createBackup,
      downloadBackup,
      deleteBackup,
      triggerFileInput,
      handleFileSelect,
      handleFileDrop,
      clearSelectedFile,
      restoreFromFile,
      prepareRestore,
      confirmAction,
      closeConfirmationModal,
      getBackupTypeLabel,
      formatDate,
      formatSize
    };
  }
});
</script>

<style scoped>
.backup-restore {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.tab {
  padding: 10px 20px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  font-weight: 500;
}

.tab.active {
  border-bottom-color: #007bff;
  color: #007bff;
}

.tab-content {
  margin-bottom: 30px;
}

.card {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.card h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

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

.radio-group,
.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.radio-option,
.checkbox-option {
  display: flex;
  align-items: center;
}

.radio-option input,
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

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search input,
.filter-type select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.backup-list {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 15px;
  text-align: right;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.backup-name {
  font-weight: 500;
}

.backup-description {
  font-size: 0.85em;
  color: #6c757d;
  margin-top: 5px;
}

.actions {
  display: flex;
  gap: 5px;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
}

.upload-area:hover {
  border-color: #007bff;
}

.upload-area i {
  font-size: 3rem;
  color: #6c757d;
  margin-bottom: 15px;
}

.selected-file {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
  margin-top: 15px;
}

.file-info {
  display: flex;
  align-items: center;
}

.file-info i {
  font-size: 1.5rem;
  color: #6c757d;
  margin-left: 10px;
}

.file-name {
  font-weight: 500;
}

.file-size {
  font-size: 0.85em;
  color: #6c757d;
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

.btn-download {
  background-color: #17a2b8;
  color: white;
}

.btn-restore {
  background-color: #28a745;
  color: white;
}

.btn-delete {
  background-color: #dc3545;
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

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
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

/* Progress bar */
.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #f3f3f3;
  border-radius: 5px;
  margin: 15px 0;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s;
}

.progress-text {
  font-weight: bold;
}

/* RTL support */
html[dir="rtl"] th,
html[dir="rtl"] td {
  text-align: left;
}

html[dir="rtl"] .radio-option input,
html[dir="rtl"] .checkbox-option input {
  margin-left: 0;
  margin-right: 8px;
}

html[dir="rtl"] .file-info i {
  margin-left: 0;
  margin-right: 10px;
}
</style>
