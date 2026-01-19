<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/AIAgentManagement.vue -->
<template>
  <div class="ai-agent-management">
    <div class="page-header">
      <h1>{{ $t('settings.aiAgentManagement.title') }}</h1>
      <div class="actions">
        <button class="btn btn-primary" @click="showAddAgentModal">
          <i class="fas fa-plus"></i> {{ $t('settings.aiAgentManagement.addAgent') }}
        </button>
      </div>
    </div>

    <div class="filters">
      <div class="search">
        <input 
          type="text" 
          v-model="searchQuery" 
          :placeholder="$t('common.search')" 
          @input="filterAgents"
        />
      </div>
      <div class="filter-model">
        <select v-model="modelFilter" @change="filterAgents">
          <option value="">{{ $t('settings.aiAgentManagement.allModels') }}</option>
          <option v-for="model in aiModels" :key="model.id" :value="model.id">
            {{ model.name }}
          </option>
        </select>
      </div>
      <div class="filter-status">
        <select v-model="statusFilter" @change="filterAgents">
          <option value="">{{ $t('settings.aiAgentManagement.allStatuses') }}</option>
          <option value="active">{{ $t('settings.aiAgentManagement.active') }}</option>
          <option value="inactive">{{ $t('settings.aiAgentManagement.inactive') }}</option>
        </select>
      </div>
    </div>

    <div class="agents-grid">
      <div v-for="agent in filteredAgents" :key="agent.id" class="agent-card">
        <div class="agent-avatar">
          <img :src="agent.avatar_url || '/assets/images/default-avatar.png'" :alt="agent.name">
          <span :class="['status-indicator', agent.is_active ? 'active' : 'inactive']"></span>
        </div>
        <div class="agent-info">
          <h3>{{ agent.name }}</h3>
          <p class="agent-description">{{ agent.description }}</p>
          <div class="agent-model">
            <span class="label">{{ $t('settings.aiAgentManagement.model') }}:</span>
            <span class="value">{{ getModelName(agent.model_id) }}</span>
          </div>
          <div class="agent-actions">
            <button class="btn btn-sm btn-edit" @click="editAgent(agent)">
              <i class="fas fa-edit"></i> {{ $t('common.edit') }}
            </button>
            <button 
              class="btn btn-sm" 
              :class="agent.is_active ? 'btn-deactivate' : 'btn-activate'"
              @click="toggleAgentStatus(agent)"
            >
              <i :class="agent.is_active ? 'fas fa-pause' : 'fas fa-play'"></i>
              {{ agent.is_active ? $t('common.deactivate') : $t('common.activate') }}
            </button>
            <button class="btn btn-sm btn-delete" @click="deleteAgent(agent)">
              <i class="fas fa-trash"></i> {{ $t('common.delete') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Agent Modal -->
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? $t('settings.aiAgentManagement.editAgent') : $t('settings.aiAgentManagement.addAgent') }}</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveAgent">
            <div class="form-group">
              <label for="name">{{ $t('settings.aiAgentManagement.name') }}</label>
              <input 
                type="text" 
                id="name" 
                v-model="currentAgent.name" 
                required
              />
            </div>
            <div class="form-group">
              <label for="description">{{ $t('settings.aiAgentManagement.description') }}</label>
              <textarea 
                id="description" 
                v-model="currentAgent.description" 
                rows="3"
              ></textarea>
            </div>
            <div class="form-group">
              <label for="model">{{ $t('settings.aiAgentManagement.model') }}</label>
              <select id="model" v-model="currentAgent.model_id" required>
                <option v-for="model in aiModels" :key="model.id" :value="model.id">
                  {{ model.name }} ({{ model.type }})
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="avatar">{{ $t('settings.aiAgentManagement.avatar') }}</label>
              <div class="avatar-selector">
                <div class="current-avatar">
                  <img :src="currentAgent.avatar_url || '/assets/images/default-avatar.png'" alt="Avatar">
                </div>
                <div class="avatar-upload">
                  <input 
                    type="file" 
                    id="avatar" 
                    @change="handleAvatarUpload" 
                    accept="image/*"
                  />
                  <label for="avatar" class="btn btn-secondary">
                    {{ $t('settings.aiAgentManagement.uploadAvatar') }}
                  </label>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label for="config">{{ $t('settings.aiAgentManagement.configuration') }}</label>
              <textarea 
                id="config" 
                v-model="configJson" 
                rows="5"
                class="code-editor"
              ></textarea>
              <div class="form-hint">{{ $t('settings.aiAgentManagement.configHint') }}</div>
            </div>
            <div class="form-group">
              <label for="status">{{ $t('settings.aiAgentManagement.status') }}</label>
              <select id="status" v-model="currentAgent.is_active">
                <option :value="true">{{ $t('settings.aiAgentManagement.active') }}</option>
                <option :value="false">{{ $t('settings.aiAgentManagement.inactive') }}</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">
                {{ $t('common.cancel') }}
              </button>
              <button type="submit" class="btn btn-primary">
                {{ $t('common.save') }}
              </button>
            </div>
          </form>
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
import aiAgentService from '@/services/aiAgentService';
import aiModelService from '@/services/aiModelService';
import { onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'AIAgentManagement',
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    
    // Data
    const agents = ref([]);
    const aiModels = ref([]);
    const filteredAgents = ref([]);
    const searchQuery = ref('');
    const modelFilter = ref('');
    const statusFilter = ref('');
    
    // Modal states
    const showModal = ref(false);
    const showConfirmationModal = ref(false);
    const isEditing = ref(false);
    const currentAgent = reactive({
      id: null,
      name: '',
      description: '',
      model_id: null,
      avatar_url: '',
      config: {},
      is_active: true
    });
    const configJson = ref('{}');
    
    // Confirmation modal
    const confirmationTitle = ref('');
    const confirmationMessage = ref('');
    const confirmationCallback = ref(null);
    
    // Fetch data
    const fetchAgents = async () => {
      try {
        const response = await aiAgentService.getAgents();
        agents.value = response.data;
        filteredAgents.value = [...agents.value];
      } catch (error) {
        showToast(t('settings.aiAgentManagement.errorFetchingAgents'), 'error');
        console.error('Error fetching AI agents:', error);
      }
    };
    
    const fetchModels = async () => {
      try {
        const response = await aiModelService.getModels();
        aiModels.value = response.data;
      } catch (error) {
        showToast(t('settings.aiAgentManagement.errorFetchingModels'), 'error');
        console.error('Error fetching AI models:', error);
      }
    };
    
    // Filter agents
    const filterAgents = () => {
      filteredAgents.value = agents.value.filter(agent => {
        const matchesSearch = searchQuery.value === '' || 
          agent.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          agent.description.toLowerCase().includes(searchQuery.value.toLowerCase());
        
        const matchesModel = modelFilter.value === '' || 
          agent.model_id === modelFilter.value;
        
        const matchesStatus = statusFilter.value === '' || 
          (statusFilter.value === 'active' && agent.is_active) ||
          (statusFilter.value === 'inactive' && !agent.is_active);
        
        return matchesSearch && matchesModel && matchesStatus;
      });
    };
    
    // Agent actions
    const showAddAgentModal = () => {
      isEditing.value = false;
      resetCurrentAgent();
      showModal.value = true;
    };
    
    const editAgent = (agent) => {
      isEditing.value = true;
      currentAgent.id = agent.id;
      currentAgent.name = agent.name;
      currentAgent.description = agent.description;
      currentAgent.model_id = agent.model_id;
      currentAgent.avatar_url = agent.avatar_url;
      currentAgent.config = agent.config || {};
      currentAgent.is_active = agent.is_active;
      configJson.value = JSON.stringify(agent.config || {}, null, 2);
      showModal.value = true;
    };
    
    const toggleAgentStatus = (agent) => {
      confirmationTitle.value = agent.is_active 
        ? t('settings.aiAgentManagement.deactivateAgent') 
        : t('settings.aiAgentManagement.activateAgent');
      
      confirmationMessage.value = agent.is_active 
        ? t('settings.aiAgentManagement.deactivateAgentConfirmation', { name: agent.name }) 
        : t('settings.aiAgentManagement.activateAgentConfirmation', { name: agent.name });
      
      confirmationCallback.value = async () => {
        try {
          await aiAgentService.updateAgentStatus(agent.id, !agent.is_active);
          agent.is_active = !agent.is_active;
          showToast(
            agent.is_active 
              ? t('settings.aiAgentManagement.agentActivated') 
              : t('settings.aiAgentManagement.agentDeactivated'), 
            'success'
          );
          closeConfirmationModal();
        } catch (error) {
          showToast(t('settings.aiAgentManagement.errorUpdatingStatus'), 'error');
          console.error('Error updating agent status:', error);
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    const deleteAgent = (agent) => {
      confirmationTitle.value = t('settings.aiAgentManagement.deleteAgent');
      confirmationMessage.value = t('settings.aiAgentManagement.deleteAgentConfirmation', { name: agent.name });
      
      confirmationCallback.value = async () => {
        try {
          await aiAgentService.deleteAgent(agent.id);
          agents.value = agents.value.filter(a => a.id !== agent.id);
          filteredAgents.value = filteredAgents.value.filter(a => a.id !== agent.id);
          showToast(t('settings.aiAgentManagement.agentDeleted'), 'success');
          closeConfirmationModal();
        } catch (error) {
          showToast(t('settings.aiAgentManagement.errorDeletingAgent'), 'error');
          console.error('Error deleting agent:', error);
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    // Form actions
    const handleAvatarUpload = (event) => {
      const file = event.target.files[0];
      if (!file) return;
      
      if (!file.type.match('image.*')) {
        showToast(t('settings.aiAgentManagement.invalidImageFormat'), 'error');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        currentAgent.avatar_url = e.target.result;
      };
      reader.readAsDataURL(file);
    };
    
    const saveAgent = async () => {
      try {
        // Parse config JSON
        try {
          currentAgent.config = JSON.parse(configJson.value);
        } catch (e) {
          showToast(t('settings.aiAgentManagement.invalidJson'), 'error');
          return;
        }
        
        if (isEditing.value) {
          await aiAgentService.updateAgent(currentAgent.id, {
            name: currentAgent.name,
            description: currentAgent.description,
            model_id: currentAgent.model_id,
            avatar_url: currentAgent.avatar_url,
            config: currentAgent.config,
            is_active: currentAgent.is_active
          });
          
          // Update agent in the list
          const index = agents.value.findIndex(a => a.id === currentAgent.id);
          if (index !== -1) {
            agents.value[index] = { ...agents.value[index], ...currentAgent };
          }
          
          showToast(t('settings.aiAgentManagement.agentUpdated'), 'success');
        } else {
          const response = await aiAgentService.createAgent({
            name: currentAgent.name,
            description: currentAgent.description,
            model_id: currentAgent.model_id,
            avatar_url: currentAgent.avatar_url,
            config: currentAgent.config,
            is_active: currentAgent.is_active
          });
          
          // Add new agent to the list
          agents.value.push(response.data);
          
          showToast(t('settings.aiAgentManagement.agentCreated'), 'success');
        }
        
        closeModal();
        filterAgents();
      } catch (error) {
        showToast(
          isEditing.value 
            ? t('settings.aiAgentManagement.errorUpdatingAgent') 
            : t('settings.aiAgentManagement.errorCreatingAgent'), 
          'error'
        );
        console.error('Error saving agent:', error);
      }
    };
    
    const confirmAction = () => {
      if (confirmationCallback.value) {
        confirmationCallback.value();
      }
    };
    
    // Modal helpers
    const closeModal = () => {
      showModal.value = false;
      resetCurrentAgent();
    };
    
    const closeConfirmationModal = () => {
      showConfirmationModal.value = false;
      confirmationTitle.value = '';
      confirmationMessage.value = '';
      confirmationCallback.value = null;
    };
    
    const resetCurrentAgent = () => {
      currentAgent.id = null;
      currentAgent.name = '';
      currentAgent.description = '';
      currentAgent.model_id = aiModels.value.length > 0 ? aiModels.value[0].id : null;
      currentAgent.avatar_url = '';
      currentAgent.config = {};
      currentAgent.is_active = true;
      configJson.value = '{}';
    };
    
    // Utility functions
    const getModelName = (modelId) => {
      const model = aiModels.value.find(m => m.id === modelId);
      return model ? model.name : t('settings.aiAgentManagement.unknownModel');
    };
    
    // Lifecycle hooks
    onMounted(async () => {
      await Promise.all([fetchAgents(), fetchModels()]);
    });
    
    return {
      agents,
      aiModels,
      filteredAgents,
      searchQuery,
      modelFilter,
      statusFilter,
      showModal,
      showConfirmationModal,
      isEditing,
      currentAgent,
      configJson,
      confirmationTitle,
      confirmationMessage,
      filterAgents,
      showAddAgentModal,
      editAgent,
      toggleAgentStatus,
      deleteAgent,
      handleAvatarUpload,
      saveAgent,
      confirmAction,
      closeModal,
      closeConfirmationModal,
      getModelName
    };
  }
};
</script>

<style scoped>
.ai-agent-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search input,
.filter-model select,
.filter-status select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.agent-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.agent-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.agent-avatar {
  position: relative;
  height: 150px;
  overflow: hidden;
  background-color: #f8f9fa;
}

.agent-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-indicator {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-indicator.active {
  background-color: #28a745;
  box-shadow: 0 0 0 2px white;
}

.status-indicator.inactive {
  background-color: #dc3545;
  box-shadow: 0 0 0 2px white;
}

.agent-info {
  padding: 15px;
}

.agent-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1.2rem;
}

.agent-description {
  color: #6c757d;
  margin-bottom: 10px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.agent-model {
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.agent-model .label {
  font-weight: bold;
  margin-left: 5px;
}

.agent-actions {
  display: flex;
  gap: 5px;
}

.btn {
  cursor: pointer;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
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

.btn-edit {
  background-color: #17a2b8;
  color: white;
}

.btn-activate {
  background-color: #28a745;
  color: white;
}

.btn-deactivate {
  background-color: #dc3545;
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

.avatar-selector {
  display: flex;
  align-items: center;
  gap: 15px;
}

.current-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #f8f9fa;
}

.current-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-upload {
  flex: 1;
}

.avatar-upload input[type="file"] {
  display: none;
}

.code-editor {
  font-family: monospace;
  white-space: pre;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

/* RTL support */
html[dir="rtl"] .agent-model .label {
  margin-left: 0;
  margin-right: 5px;
}

html[dir="rtl"] .status-indicator {
  right: auto;
  left: 10px;
}
</style>
