<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/docker/DockerManager.vue
الوصف: مكون إدارة حاويات Docker من واجهة المستخدم
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="docker-manager-container rtl-support">
    <div class="header-section">
      <h1 class="title">{{ $t('docker.manager.title') }}</h1>
      <p class="description">{{ $t('docker.manager.description') }}</p>
    </div>

    <div class="tabs-container">
      <div 
        v-for="(tab, index) in tabs" 
        :key="index" 
        :class="['tab', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        <i :class="tab.icon"></i>
        <span>{{ tab.name }}</span>
      </div>
    </div>

    <div class="content-section">
      <!-- قسم الحاويات الأساسية -->
      <div v-if="activeTab === 'core'" class="tab-content">
        <h2>{{ $t('docker.manager.core.title') }}</h2>
        <p>{{ $t('docker.manager.core.description') }}</p>
        
        <div class="containers-grid">
          <div 
            v-for="(container, index) in coreContainers" 
            :key="index"
            class="container-card"
            :class="{ 'running': container.status === 'running' }"
          >
            <div class="container-header">
              <h3>{{ container.name }}</h3>
              <div class="status-badge" :class="container.status">
                {{ $t(`docker.status.${container.status}`) }}
              </div>
            </div>
            <p class="container-description">{{ container.description }}</p>
            <div class="container-details">
              <div class="detail-item">
                <span class="label">{{ $t('docker.manager.image') }}:</span>
                <span class="value">{{ container.image }}</span>
              </div>
              <div class="detail-item">
                <span class="label">{{ $t('docker.manager.ports') }}:</span>
                <span class="value">{{ container.ports.join(', ') }}</span>
              </div>
            </div>
            <div class="container-actions">
              <button 
                v-if="container.status !== 'running'" 
                class="action-button start"
                @click="startContainer(container.id)"
              >
                <i class="fas fa-play"></i> {{ $t('docker.actions.start') }}
              </button>
              <button 
                v-if="container.status === 'running'" 
                class="action-button stop"
                @click="stopContainer(container.id)"
              >
                <i class="fas fa-stop"></i> {{ $t('docker.actions.stop') }}
              </button>
              <button 
                v-if="container.status === 'running'" 
                class="action-button restart"
                @click="restartContainer(container.id)"
              >
                <i class="fas fa-sync"></i> {{ $t('docker.actions.restart') }}
              </button>
              <button 
                class="action-button logs"
                @click="viewLogs(container.id)"
              >
                <i class="fas fa-file-alt"></i> {{ $t('docker.actions.logs') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- قسم حاويات الذكاء الاصطناعي -->
      <div v-if="activeTab === 'ai'" class="tab-content">
        <h2>{{ $t('docker.manager.ai.title') }}</h2>
        <p>{{ $t('docker.manager.ai.description') }}</p>
        
        <div class="containers-grid">
          <div 
            v-for="(container, index) in aiContainers" 
            :key="index"
            class="container-card"
            :class="{ 'running': container.status === 'running' }"
          >
            <div class="container-header">
              <h3>{{ container.name }}</h3>
              <div class="status-badge" :class="container.status">
                {{ $t(`docker.status.${container.status}`) }}
              </div>
            </div>
            <p class="container-description">{{ container.description }}</p>
            <div class="container-details">
              <div class="detail-item">
                <span class="label">{{ $t('docker.manager.image') }}:</span>
                <span class="value">{{ container.image }}</span>
              </div>
              <div class="detail-item">
                <span class="label">{{ $t('docker.manager.gpu') }}:</span>
                <span class="value">{{ container.gpu ? $t('common.yes') : $t('common.no') }}</span>
              </div>
            </div>
            <div class="container-actions">
              <button 
                v-if="container.status !== 'running'" 
                class="action-button start"
                @click="startContainer(container.id)"
              >
                <i class="fas fa-play"></i> {{ $t('docker.actions.start') }}
              </button>
              <button 
                v-if="container.status === 'running'" 
                class="action-button stop"
                @click="stopContainer(container.id)"
              >
                <i class="fas fa-stop"></i> {{ $t('docker.actions.stop') }}
              </button>
              <button 
                v-if="container.status === 'running'" 
                class="action-button restart"
                @click="restartContainer(container.id)"
              >
                <i class="fas fa-sync"></i> {{ $t('docker.actions.restart') }}
              </button>
              <button 
                class="action-button logs"
                @click="viewLogs(container.id)"
              >
                <i class="fas fa-file-alt"></i> {{ $t('docker.actions.logs') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- قسم حاويات البحث -->
      <div v-if="activeTab === 'search'" class="tab-content">
        <h2>{{ $t('docker.manager.search.title') }}</h2>
        <p>{{ $t('docker.manager.search.description') }}</p>
        
        <div class="containers-grid">
          <div 
            v-for="(container, index) in searchContainers" 
            :key="index"
            class="container-card"
            :class="{ 'running': container.status === 'running' }"
          >
            <div class="container-header">
              <h3>{{ container.name }}</h3>
              <div class="status-badge" :class="container.status">
                {{ $t(`docker.status.${container.status}`) }}
              </div>
            </div>
            <p class="container-description">{{ container.description }}</p>
            <div class="container-details">
              <div class="detail-item">
                <span class="label">{{ $t('docker.manager.image') }}:</span>
                <span class="value">{{ container.image }}</span>
              </div>
              <div class="detail-item">
                <span class="label">{{ $t('docker.manager.type') }}:</span>
                <span class="value">{{ container.type }}</span>
              </div>
            </div>
            <div class="container-actions">
              <button 
                v-if="container.status !== 'running'" 
                class="action-button start"
                @click="startContainer(container.id)"
              >
                <i class="fas fa-play"></i> {{ $t('docker.actions.start') }}
              </button>
              <button 
                v-if="container.status === 'running'" 
                class="action-button stop"
                @click="stopContainer(container.id)"
              >
                <i class="fas fa-stop"></i> {{ $t('docker.actions.stop') }}
              </button>
              <button 
                v-if="container.status === 'running'" 
                class="action-button restart"
                @click="restartContainer(container.id)"
              >
                <i class="fas fa-sync"></i> {{ $t('docker.actions.restart') }}
              </button>
              <button 
                class="action-button logs"
                @click="viewLogs(container.id)"
              >
                <i class="fas fa-file-alt"></i> {{ $t('docker.actions.logs') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- قسم حاويات تشخيص الأمراض -->
      <div v-if="activeTab === 'disease'" class="tab-content">
        <h2>{{ $t('docker.manager.disease.title') }}</h2>
        <p>{{ $t('docker.manager.disease.description') }}</p>
        
        <div class="containers-grid">
          <div 
            v-for="(container, index) in diseaseContainers" 
            :key="index"
            class="container-card"
            :class="{ 'running': container.status === 'running' }"
          >
            <div class="container-header">
              <h3>{{ container.name }}</h3>
              <div class="status-badge" :class="container.status">
                {{ $t(`docker.status.${container.status}`) }}
              </div>
            </div>
            <p class="container-description">{{ container.description }}</p>
            <div class="container-details">
              <div class="detail-item">
                <span class="label">{{ $t('docker.manager.image') }}:</span>
                <span class="value">{{ container.image }}</span>
              </div>
              <div class="detail-item">
                <span class="label">{{ $t('docker.manager.models') }}:</span>
                <span class="value">{{ container.models.join(', ') }}</span>
              </div>
            </div>
            <div class="container-actions">
              <button 
                v-if="container.status !== 'running'" 
                class="action-button start"
                @click="startContainer(container.id)"
              >
                <i class="fas fa-play"></i> {{ $t('docker.actions.start') }}
              </button>
              <button 
                v-if="container.status === 'running'" 
                class="action-button stop"
                @click="stopContainer(container.id)"
              >
                <i class="fas fa-stop"></i> {{ $t('docker.actions.stop') }}
              </button>
              <button 
                v-if="container.status === 'running'" 
                class="action-button restart"
                @click="restartContainer(container.id)"
              >
                <i class="fas fa-sync"></i> {{ $t('docker.actions.restart') }}
              </button>
              <button 
                class="action-button logs"
                @click="viewLogs(container.id)"
              >
                <i class="fas fa-file-alt"></i> {{ $t('docker.actions.logs') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- قسم إضافة حاويات جديدة -->
      <div v-if="activeTab === 'add'" class="tab-content">
        <h2>{{ $t('docker.manager.add.title') }}</h2>
        <p>{{ $t('docker.manager.add.description') }}</p>
        
        <div class="add-container-form">
          <div class="form-section">
            <h3>{{ $t('docker.manager.add.select_type') }}</h3>
            <div class="container-types">
              <div 
                v-for="(type, index) in containerTypes" 
                :key="index"
                :class="['container-type-card', { 'selected': selectedContainerType === type.id }]"
                @click="selectedContainerType = type.id"
              >
                <i :class="type.icon"></i>
                <h4>{{ type.name }}</h4>
                <p>{{ type.description }}</p>
              </div>
            </div>
          </div>

          <div v-if="selectedContainerType" class="form-section">
            <h3>{{ $t('docker.manager.add.available_containers') }}</h3>
            <div class="available-containers">
              <div 
                v-for="(container, index) in availableContainers" 
                :key="index"
                :class="['available-container-card', { 'selected': selectedContainer === container.id }]"
                @click="selectedContainer = container.id"
              >
                <h4>{{ container.name }}</h4>
                <p>{{ container.description }}</p>
                <div class="container-meta">
                  <span class="meta-item">
                    <i class="fas fa-tag"></i> {{ container.version }}
                  </span>
                  <span class="meta-item">
                    <i class="fas fa-download"></i> {{ container.downloads }}
                  </span>
                  <span class="meta-item">
                    <i class="fas fa-star"></i> {{ container.rating }}/5
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="selectedContainer" class="form-section">
            <h3>{{ $t('docker.manager.add.configuration') }}</h3>
            <div class="configuration-form">
              <div class="form-group">
                <label for="container-name">{{ $t('docker.manager.add.name') }}</label>
                <input 
                  id="container-name" 
                  v-model="containerConfig.name" 
                  type="text" 
                  :placeholder="$t('docker.manager.add.name_placeholder')"
                />
              </div>
              
              <div class="form-group">
                <label for="container-port">{{ $t('docker.manager.add.port') }}</label>
                <input 
                  id="container-port" 
                  v-model="containerConfig.port" 
                  type="number" 
                  :placeholder="$t('docker.manager.add.port_placeholder')"
                />
              </div>
              
              <div class="form-group">
                <label for="container-env">{{ $t('docker.manager.add.environment') }}</label>
                <textarea 
                  id="container-env" 
                  v-model="containerConfig.env" 
                  :placeholder="$t('docker.manager.add.environment_placeholder')"
                ></textarea>
              </div>
              
              <div class="form-group checkbox">
                <input 
                  id="container-gpu" 
                  v-model="containerConfig.gpu" 
                  type="checkbox"
                />
                <label for="container-gpu">{{ $t('docker.manager.add.use_gpu') }}</label>
              </div>
              
              <div class="form-group checkbox">
                <input 
                  id="container-autostart" 
                  v-model="containerConfig.autostart" 
                  type="checkbox"
                />
                <label for="container-autostart">{{ $t('docker.manager.add.autostart') }}</label>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button 
              class="action-button cancel"
              @click="resetForm"
            >
              {{ $t('common.cancel') }}
            </button>
            <button 
              class="action-button install"
              :disabled="!canInstall"
              @click="installContainer"
            >
              <i class="fas fa-download"></i> {{ $t('docker.manager.add.install') }}
            </button>
          </div>
        </div>
      </div>

      <!-- قسم سجلات الحاويات -->
      <div v-if="activeTab === 'logs'" class="tab-content">
        <h2>{{ $t('docker.manager.logs.title') }}</h2>
        
        <div class="logs-container">
          <div class="logs-header">
            <div class="logs-selector">
              <label for="container-select">{{ $t('docker.manager.logs.select_container') }}</label>
              <select id="container-select" v-model="selectedLogContainer">
                <option value="">{{ $t('docker.manager.logs.select_placeholder') }}</option>
                <option 
                  v-for="container in allContainers" 
                  :key="container.id" 
                  :value="container.id"
                >
                  {{ container.name }}
                </option>
              </select>
            </div>
            
            <div class="logs-actions">
              <button 
                class="action-button refresh"
                @click="refreshLogs"
                :disabled="!selectedLogContainer"
              >
                <i class="fas fa-sync"></i> {{ $t('docker.manager.logs.refresh') }}
              </button>
              <button 
                class="action-button download"
                @click="downloadLogs"
                :disabled="!selectedLogContainer || !containerLogs"
              >
                <i class="fas fa-download"></i> {{ $t('docker.manager.logs.download') }}
              </button>
            </div>
          </div>
          
          <div class="logs-content">
            <pre v-if="containerLogs">{{ containerLogs }}</pre>
            <div v-else class="logs-placeholder">
              {{ selectedLogContainer ? $t('docker.manager.logs.loading') : $t('docker.manager.logs.select_container_first') }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة عرض السجلات -->
    <div v-if="showLogsModal" class="logs-modal">
      <div class="logs-modal-content">
        <div class="logs-modal-header">
          <h3>{{ $t('docker.manager.logs.title') }}: {{ currentLogContainer?.name }}</h3>
          <button class="close-button" @click="showLogsModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="logs-modal-body">
          <pre>{{ currentContainerLogs }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '@/frontend/composables/useToast';
import dockerService from '@/frontend/services/dockerService';
import { computed, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'DockerManager',
  
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    
    // حالة التبويبات
    const activeTab = ref('core');
    const tabs = [
      { id: 'core', name: t('docker.manager.tabs.core'), icon: 'fas fa-server' },
      { id: 'ai', name: t('docker.manager.tabs.ai'), icon: 'fas fa-brain' },
      { id: 'search', name: t('docker.manager.tabs.search'), icon: 'fas fa-search' },
      { id: 'disease', name: t('docker.manager.tabs.disease'), icon: 'fas fa-leaf' },
      { id: 'add', name: t('docker.manager.tabs.add'), icon: 'fas fa-plus-circle' },
      { id: 'logs', name: t('docker.manager.tabs.logs'), icon: 'fas fa-file-alt' }
    ];
    
    // حالة الحاويات
    const coreContainers = ref([]);
    const aiContainers = ref([]);
    const searchContainers = ref([]);
    const diseaseContainers = ref([]);
    
    // حالة إضافة حاوية جديدة
    const selectedContainerType = ref('');
    const selectedContainer = ref('');
    const containerConfig = ref({
      name: '',
      port: '',
      env: '',
      gpu: false,
      autostart: true
    });
    
    // أنواع الحاويات المتاحة
    const containerTypes = [
      { 
        id: 'ai', 
        name: t('docker.manager.types.ai'), 
        icon: 'fas fa-brain',
        description: t('docker.manager.types.ai_description')
      },
      { 
        id: 'search', 
        name: t('docker.manager.types.search'), 
        icon: 'fas fa-search',
        description: t('docker.manager.types.search_description')
      },
      { 
        id: 'disease', 
        name: t('docker.manager.types.disease'), 
        icon: 'fas fa-leaf',
        description: t('docker.manager.types.disease_description')
      },
      { 
        id: 'custom', 
        name: t('docker.manager.types.custom'), 
        icon: 'fas fa-code',
        description: t('docker.manager.types.custom_description')
      }
    ];
    
    // الحاويات المتاحة للتثبيت
    const availableContainers = ref([]);
    
    // حالة سجلات الحاويات
    const selectedLogContainer = ref('');
    const containerLogs = ref('');
    const showLogsModal = ref(false);
    const currentLogContainer = ref(null);
    const currentContainerLogs = ref('');
    
    // الحصول على جميع الحاويات
    const allContainers = computed(() => {
      return [
        ...coreContainers.value,
        ...aiContainers.value,
        ...searchContainers.value,
        ...diseaseContainers.value
      ];
    });
    
    // التحقق من إمكانية التثبيت
    const canInstall = computed(() => {
      return selectedContainerType.value && 
             selectedContainer.value && 
             containerConfig.value.name.trim() !== '';
    });
    
    // تحميل الحاويات عند تحميل المكون
    onMounted(async () => {
      await loadContainers();
    });
    
    // مراقبة تغيير نوع الحاوية
    watch(selectedContainerType, async (newType) => {
      if (newType) {
        await loadAvailableContainers(newType);
        selectedContainer.value = '';
      }
    });
    
    // مراقبة تغيير الحاوية المحددة للسجلات
    watch(selectedLogContainer, async (newContainer) => {
      if (newContainer) {
        await loadContainerLogs(newContainer);
      } else {
        containerLogs.value = '';
      }
    });
    
    // تحميل الحاويات
    const loadContainers = async () => {
      try {
        const response = await dockerService.getContainers();
        
        coreContainers.value = response.core || [];
        aiContainers.value = response.ai || [];
        searchContainers.value = response.search || [];
        diseaseContainers.value = response.disease || [];
        
      } catch (error) {
        console.error('Error loading containers:', error);
        showToast(t('docker.manager.errors.load_containers'), 'error');
      }
    };
    
    // تحميل الحاويات المتاحة
    const loadAvailableContainers = async (type) => {
      try {
        availableContainers.value = await dockerService.getAvailableContainers(type);
      } catch (error) {
        console.error('Error loading available containers:', error);
        showToast(t('docker.manager.errors.load_available'), 'error');
        availableContainers.value = [];
      }
    };
    
    // تشغيل حاوية
    const startContainer = async (containerId) => {
      try {
        await dockerService.startContainer(containerId);
        showToast(t('docker.manager.success.start'), 'success');
        await loadContainers();
      } catch (error) {
        console.error('Error starting container:', error);
        showToast(t('docker.manager.errors.start'), 'error');
      }
    };
    
    // إيقاف حاوية
    const stopContainer = async (containerId) => {
      try {
        await dockerService.stopContainer(containerId);
        showToast(t('docker.manager.success.stop'), 'success');
        await loadContainers();
      } catch (error) {
        console.error('Error stopping container:', error);
        showToast(t('docker.manager.errors.stop'), 'error');
      }
    };
    
    // إعادة تشغيل حاوية
    const restartContainer = async (containerId) => {
      try {
        await dockerService.restartContainer(containerId);
        showToast(t('docker.manager.success.restart'), 'success');
        await loadContainers();
      } catch (error) {
        console.error('Error restarting container:', error);
        showToast(t('docker.manager.errors.restart'), 'error');
      }
    };
    
    // عرض سجلات حاوية
    const viewLogs = async (containerId) => {
      try {
        const container = allContainers.value.find(c => c.id === containerId);
        if (!container) return;
        
        currentLogContainer.value = container;
        currentContainerLogs.value = await dockerService.getContainerLogs(containerId);
        showLogsModal.value = true;
      } catch (error) {
        console.error('Error viewing logs:', error);
        showToast(t('docker.manager.errors.logs'), 'error');
      }
    };
    
    // تحميل سجلات حاوية
    const loadContainerLogs = async (containerId) => {
      try {
        containerLogs.value = await dockerService.getContainerLogs(containerId);
      } catch (error) {
        console.error('Error loading logs:', error);
        showToast(t('docker.manager.errors.logs'), 'error');
        containerLogs.value = '';
      }
    };
    
    // تحديث سجلات حاوية
    const refreshLogs = async () => {
      if (selectedLogContainer.value) {
        await loadContainerLogs(selectedLogContainer.value);
      }
    };
    
    // تنزيل سجلات حاوية
    const downloadLogs = () => {
      if (!selectedLogContainer.value || !containerLogs.value) return;
      
      const container = allContainers.value.find(c => c.id === selectedLogContainer.value);
      if (!container) return;
      
      const filename = `${container.name}_logs_${new Date().toISOString().replace(/[:.]/g, '-')}.txt`;
      const blob = new Blob([containerLogs.value], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    };
    
    // تثبيت حاوية جديدة
    const installContainer = async () => {
      try {
        const containerData = {
          type: selectedContainerType.value,
          containerId: selectedContainer.value,
          config: containerConfig.value
        };
        
        await dockerService.installContainer(containerData);
        showToast(t('docker.manager.success.install'), 'success');
        
        // إعادة تعيين النموذج
        resetForm();
        
        // إعادة تحميل الحاويات
        await loadContainers();
        
        // الانتقال إلى التبويب المناسب
        switch (selectedContainerType.value) {
          case 'ai':
            activeTab.value = 'ai';
            break;
          case 'search':
            activeTab.value = 'search';
            break;
          case 'disease':
            activeTab.value = 'disease';
            break;
          default:
            activeTab.value = 'core';
        }
      } catch (error) {
        console.error('Error installing container:', error);
        showToast(t('docker.manager.errors.install'), 'error');
      }
    };
    
    // إعادة تعيين نموذج إضافة حاوية
    const resetForm = () => {
      selectedContainerType.value = '';
      selectedContainer.value = '';
      containerConfig.value = {
        name: '',
        port: '',
        env: '',
        gpu: false,
        autostart: true
      };
      availableContainers.value = [];
    };
    
    return {
      // التبويبات
      activeTab,
      tabs,
      
      // الحاويات
      coreContainers,
      aiContainers,
      searchContainers,
      diseaseContainers,
      allContainers,
      
      // إضافة حاوية جديدة
      containerTypes,
      selectedContainerType,
      availableContainers,
      selectedContainer,
      containerConfig,
      canInstall,
      
      // سجلات الحاويات
      selectedLogContainer,
      containerLogs,
      showLogsModal,
      currentLogContainer,
      currentContainerLogs,
      
      // الوظائف
      startContainer,
      stopContainer,
      restartContainer,
      viewLogs,
      refreshLogs,
      downloadLogs,
      installContainer,
      resetForm
    };
  }
};
</script>

<style scoped>
.docker-manager-container {
  padding: 20px;
  background-color: var(--bg-color);
  color: var(--text-color);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-section {
  margin-bottom: 20px;
}

.title {
  font-size: 24px;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.description {
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.tabs-container {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.tab {
  padding: 12px 20px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab i {
  font-size: 16px;
}

.tab.active {
  border-bottom-color: var(--primary-color);
  color: var(--primary-color);
  font-weight: 600;
}

.tab:hover:not(.active) {
  background-color: var(--hover-color);
}

.content-section {
  min-height: 400px;
}

.tab-content h2 {
  margin-bottom: 15px;
  color: var(--primary-color);
}

.tab-content p {
  margin-bottom: 20px;
  color: var(--text-secondary);
}

.containers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.container-card {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-right: 4px solid var(--border-color);
}

.container-card.running {
  border-right-color: var(--success-color);
}

.container-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.container-header h3 {
  font-size: 18px;
  margin: 0;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.running {
  background-color: rgba(var(--success-rgb), 0.2);
  color: var(--success-color);
}

.status-badge.stopped {
  background-color: rgba(var(--danger-rgb), 0.2);
  color: var(--danger-color);
}

.status-badge.exited {
  background-color: rgba(var(--warning-rgb), 0.2);
  color: var(--warning-color);
}

.container-description {
  margin-bottom: 15px;
  font-size: 14px;
  color: var(--text-secondary);
}

.container-details {
  margin-bottom: 15px;
}

.detail-item {
  display: flex;
  margin-bottom: 5px;
  font-size: 14px;
}

.detail-item .label {
  font-weight: 600;
  min-width: 80px;
}

.container-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.action-button {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s ease;
}

.action-button.start {
  background-color: var(--success-color);
  color: white;
}

.action-button.stop {
  background-color: var(--danger-color);
  color: white;
}

.action-button.restart {
  background-color: var(--warning-color);
  color: white;
}

.action-button.logs {
  background-color: var(--info-color);
  color: white;
}

.action-button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* إضافة حاوية جديدة */
.add-container-form {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 25px;
}

.form-section h3 {
  margin-bottom: 15px;
  color: var(--primary-color);
  font-size: 18px;
}

.container-types {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.container-type-card {
  background-color: var(--bg-color);
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  text-align: center;
}

.container-type-card i {
  font-size: 24px;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.container-type-card h4 {
  margin-bottom: 8px;
}

.container-type-card p {
  font-size: 14px;
  color: var(--text-secondary);
}

.container-type-card.selected {
  border-color: var(--primary-color);
  background-color: rgba(var(--primary-rgb), 0.1);
}

.container-type-card:hover:not(.selected) {
  background-color: var(--hover-color);
}

.available-containers {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.available-container-card {
  background-color: var(--bg-color);
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.available-container-card h4 {
  margin-bottom: 8px;
}

.available-container-card p {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.container-meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: var(--text-secondary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.available-container-card.selected {
  border-color: var(--primary-color);
  background-color: rgba(var(--primary-rgb), 0.1);
}

.available-container-card:hover:not(.selected) {
  background-color: var(--hover-color);
}

.configuration-form {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  background-color: var(--input-bg);
  color: var(--text-color);
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.form-group.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group.checkbox label {
  margin-bottom: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.action-button.cancel {
  background-color: var(--border-color);
  color: var(--text-color);
}

.action-button.install {
  background-color: var(--primary-color);
  color: white;
}

/* سجلات الحاويات */
.logs-container {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.logs-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logs-selector label {
  font-weight: 600;
}

.logs-selector select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  background-color: var(--input-bg);
  color: var(--text-color);
}

.logs-actions {
  display: flex;
  gap: 10px;
}

.action-button.refresh {
  background-color: var(--info-color);
  color: white;
}

.action-button.download {
  background-color: var(--primary-color);
  color: white;
}

.logs-content {
  background-color: var(--code-bg);
  border-radius: 4px;
  padding: 15px;
  min-height: 300px;
  max-height: 500px;
  overflow-y: auto;
}

.logs-content pre {
  margin: 0;
  font-family: monospace;
  font-size: 14px;
  color: var(--code-color);
  white-space: pre-wrap;
}

.logs-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  color: var(--text-secondary);
}

/* نافذة عرض السجلات */
.logs-modal {
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

.logs-modal-content {
  background-color: var(--bg-color);
  border-radius: 8px;
  width: 80%;
  max-width: 1000px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.logs-modal-header {
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
}

.logs-modal-header h3 {
  margin: 0;
  color: var(--primary-color);
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: var(--text-secondary);
}

.logs-modal-body {
  padding: 15px;
  overflow-y: auto;
  flex-grow: 1;
  background-color: var(--code-bg);
}

.logs-modal-body pre {
  margin: 0;
  font-family: monospace;
  font-size: 14px;
  color: var(--code-color);
  white-space: pre-wrap;
}

/* دعم RTL */
.rtl-support {
  direction: rtl;
  text-align: right;
}

.rtl-support .container-card {
  border-right: none;
  border-left: 4px solid var(--border-color);
}

.rtl-support .container-card.running {
  border-left-color: var(--success-color);
}

.rtl-support .form-actions {
  justify-content: flex-start;
}

.rtl-support .logs-header {
  flex-direction: row-reverse;
}

.rtl-support .logs-selector {
  flex-direction: row-reverse;
}

.rtl-support .logs-actions {
  flex-direction: row-reverse;
}

.rtl-support .logs-modal-header {
  flex-direction: row-reverse;
}

/* تخصيص الألوان حسب السمة */
:root {
  --primary-color: #1976d2;
  --primary-rgb: 25, 118, 210;
  --success-color: #4caf50;
  --success-rgb: 76, 175, 80;
  --danger-color: #f44336;
  --danger-rgb: 244, 67, 54;
  --warning-color: #ff9800;
  --warning-rgb: 255, 152, 0;
  --info-color: #2196f3;
  --info-rgb: 33, 150, 243;
  --bg-color: #ffffff;
  --card-bg: #f5f5f5;
  --text-color: #333333;
  --text-secondary: #666666;
  --border-color: #dddddd;
  --hover-color: #eeeeee;
  --input-bg: #ffffff;
  --code-bg: #2d2d2d;
  --code-color: #f8f8f2;
}

/* سمة داكنة */
.dark-theme {
  --bg-color: #1e1e1e;
  --card-bg: #2d2d2d;
  --text-color: #e0e0e0;
  --text-secondary: #a0a0a0;
  --border-color: #444444;
  --hover-color: #3d3d3d;
  --input-bg: #3d3d3d;
  --code-bg: #1a1a1a;
  --code-color: #f8f8f2;
}

/* سمة gaaragroup */
.gaaragroup-theme {
  --primary-color: #0056b3;
  --primary-rgb: 0, 86, 179;
}

/* سمة magseeds */
.magseeds-theme {
  --primary-color: #2e7d32;
  --primary-rgb: 46, 125, 50;
}
</style>
