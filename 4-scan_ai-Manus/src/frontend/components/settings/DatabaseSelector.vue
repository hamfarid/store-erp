<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/DatabaseSelector.vue -->
<template>
  <div class="database-selector">
    <div class="page-header">
      <h1>{{ $t('settings.databaseSelector.title') }}</h1>
    </div>

    <div class="database-selection-form">
      <form @submit.prevent="saveSettings">
        <div class="form-group">
          <label for="database-type">{{ $t('settings.databaseSelector.databaseType') }}</label>
          <select id="database-type" v-model="settings.database_type" @change="onDatabaseTypeChange">
            <option value="postgresql">PostgreSQL</option>
            <option value="mysql">MySQL</option>
            <option value="sqlite">SQLite</option>
          </select>
        </div>

        <div class="form-group" v-if="settings.database_type !== 'sqlite'">
          <label for="host">{{ $t('settings.databaseSelector.host') }}</label>
          <input type="text" id="host" v-model="settings.host" required />
        </div>

        <div class="form-group" v-if="settings.database_type !== 'sqlite'">
          <label for="port">{{ $t('settings.databaseSelector.port') }}</label>
          <input type="number" id="port" v-model="settings.port" required />
        </div>

        <div class="form-group">
          <label for="database-name">{{ $t('settings.databaseSelector.databaseName') }}</label>
          <input type="text" id="database-name" v-model="settings.database_name" required />
        </div>

        <div class="form-group" v-if="settings.database_type !== 'sqlite'">
          <label for="username">{{ $t('settings.databaseSelector.username') }}</label>
          <input type="text" id="username" v-model="settings.username" required />
        </div>

        <div class="form-group" v-if="settings.database_type !== 'sqlite'">
          <label for="password">{{ $t('settings.databaseSelector.password') }}</label>
          <input type="password" id="password" v-model="settings.password" required />
        </div>

        <div class="form-group">
          <label for="connection-pool">{{ $t('settings.databaseSelector.connectionPool') }}</label>
          <input type="number" id="connection-pool" v-model="settings.connection_pool" min="1" max="100" required />
        </div>

        <div class="form-group">
          <label for="timeout">{{ $t('settings.databaseSelector.timeout') }} ({{ $t('settings.databaseSelector.seconds') }})</label>
          <input type="number" id="timeout" v-model="settings.timeout" min="1" max="300" required />
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="testConnection">
            {{ $t('settings.databaseSelector.testConnection') }}
          </button>
          <button type="submit" class="btn btn-primary" :disabled="isTesting">
            {{ $t('common.save') }}
          </button>
        </div>
      </form>
    </div>

    <div class="database-list">
      <h2>{{ $t('settings.databaseSelector.savedConnections') }}</h2>
      <table>
        <thead>
          <tr>
            <th>{{ $t('settings.databaseSelector.name') }}</th>
            <th>{{ $t('settings.databaseSelector.type') }}</th>
            <th>{{ $t('settings.databaseSelector.host') }}</th>
            <th>{{ $t('settings.databaseSelector.status') }}</th>
            <th>{{ $t('common.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="connection in savedConnections" :key="connection.id">
            <td>{{ connection.name }}</td>
            <td>{{ connection.database_type }}</td>
            <td>{{ connection.host || $t('settings.databaseSelector.local') }}</td>
            <td>
              <span :class="['status-badge', connection.is_active ? 'active' : 'inactive']">
                {{ connection.is_active ? $t('settings.databaseSelector.active') : $t('settings.databaseSelector.inactive') }}
              </span>
            </td>
            <td class="actions">
              <button class="btn btn-sm btn-edit" @click="editConnection(connection)">
                <i class="fas fa-edit"></i>
              </button>
              <button 
                class="btn btn-sm" 
                :class="connection.is_active ? 'btn-deactivate' : 'btn-activate'"
                @click="activateConnection(connection)"
                :disabled="connection.is_active"
              >
                <i class="fas fa-check-circle"></i>
              </button>
              <button class="btn btn-sm btn-delete" @click="deleteConnection(connection)">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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

    <!-- Testing Connection Modal -->
    <div class="modal" v-if="isTesting">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ $t('settings.databaseSelector.testingConnection') }}</h2>
        </div>
        <div class="modal-body">
          <div class="loading-spinner"></div>
          <p>{{ $t('settings.databaseSelector.testingConnectionMessage') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast';
import databaseService from '@/services/databaseService';
import { onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'DatabaseSelector',
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    
    // Data
    const savedConnections = ref([]);
    const settings = reactive({
      database_type: 'postgresql',
      host: 'localhost',
      port: 5432,
      database_name: '',
      username: '',
      password: '',
      connection_pool: 10,
      timeout: 30,
      is_active: false
    });
    const isTesting = ref(false);
    
    // Modal states
    const showConfirmationModal = ref(false);
    const confirmationTitle = ref('');
    const confirmationMessage = ref('');
    const confirmationCallback = ref(null);
    const isEditing = ref(false);
    const editingConnectionId = ref(null);
    
    // Fetch data
    const fetchConnections = async () => {
      try {
        const response = await databaseService.getConnections();
        savedConnections.value = response.data;
      } catch (error) {
        showToast(t('settings.databaseSelector.errorFetchingConnections'), 'error');
        console.error('Error fetching database connections:', error);
      }
    };
    
    // Form actions
    const onDatabaseTypeChange = () => {
      // Update port based on database type
      switch (settings.database_type) {
        case 'postgresql':
          settings.port = 5432;
          break;
        case 'mysql':
          settings.port = 3306;
          break;
        case 'sqlite':
          settings.port = null;
          settings.host = null;
          settings.username = null;
          settings.password = null;
          break;
      }
    };
    
    const testConnection = async () => {
      isTesting.value = true;
      
      try {
        const response = await databaseService.testConnection({
          database_type: settings.database_type,
          host: settings.host,
          port: settings.port,
          database_name: settings.database_name,
          username: settings.username,
          password: settings.password,
          connection_pool: settings.connection_pool,
          timeout: settings.timeout
        });
        
        if (response.data.success) {
          showToast(t('settings.databaseSelector.connectionSuccessful'), 'success');
        } else {
          showToast(t('settings.databaseSelector.connectionFailed') + ': ' + response.data.message, 'error');
        }
      } catch (error) {
        showToast(t('settings.databaseSelector.connectionFailed'), 'error');
        console.error('Error testing database connection:', error);
      } finally {
        isTesting.value = false;
      }
    };
    
    const saveSettings = async () => {
      try {
        const connectionData = {
          database_type: settings.database_type,
          host: settings.database_type === 'sqlite' ? null : settings.host,
          port: settings.database_type === 'sqlite' ? null : settings.port,
          database_name: settings.database_name,
          username: settings.database_type === 'sqlite' ? null : settings.username,
          password: settings.database_type === 'sqlite' ? null : settings.password,
          connection_pool: settings.connection_pool,
          timeout: settings.timeout,
          name: settings.database_name // Use database name as connection name
        };
        
        if (isEditing.value) {
          await databaseService.updateConnection(editingConnectionId.value, connectionData);
          showToast(t('settings.databaseSelector.connectionUpdated'), 'success');
        } else {
          await databaseService.createConnection(connectionData);
          showToast(t('settings.databaseSelector.connectionSaved'), 'success');
        }
        
        // Reset form and refresh connections
        resetForm();
        await fetchConnections();
      } catch (error) {
        showToast(t('settings.databaseSelector.errorSavingConnection'), 'error');
        console.error('Error saving database connection:', error);
      }
    };
    
    const editConnection = (connection) => {
      isEditing.value = true;
      editingConnectionId.value = connection.id;
      
      settings.database_type = connection.database_type;
      settings.host = connection.host;
      settings.port = connection.port;
      settings.database_name = connection.database_name;
      settings.username = connection.username;
      settings.password = ''; // Don't populate password for security reasons
      settings.connection_pool = connection.connection_pool;
      settings.timeout = connection.timeout;
    };
    
    const activateConnection = (connection) => {
      confirmationTitle.value = t('settings.databaseSelector.activateConnection');
      confirmationMessage.value = t('settings.databaseSelector.activateConnectionConfirmation', { name: connection.name });
      
      confirmationCallback.value = async () => {
        try {
          await databaseService.activateConnection(connection.id);
          
          // Update all connections' active status
          savedConnections.value.forEach(conn => {
            conn.is_active = conn.id === connection.id;
          });
          
          showToast(t('settings.databaseSelector.connectionActivated'), 'success');
          closeConfirmationModal();
        } catch (error) {
          showToast(t('settings.databaseSelector.errorActivatingConnection'), 'error');
          console.error('Error activating database connection:', error);
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    const deleteConnection = (connection) => {
      confirmationTitle.value = t('settings.databaseSelector.deleteConnection');
      confirmationMessage.value = t('settings.databaseSelector.deleteConnectionConfirmation', { name: connection.name });
      
      confirmationCallback.value = async () => {
        try {
          await databaseService.deleteConnection(connection.id);
          savedConnections.value = savedConnections.value.filter(conn => conn.id !== connection.id);
          showToast(t('settings.databaseSelector.connectionDeleted'), 'success');
          closeConfirmationModal();
        } catch (error) {
          showToast(t('settings.databaseSelector.errorDeletingConnection'), 'error');
          console.error('Error deleting database connection:', error);
        }
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
    
    const resetForm = () => {
      isEditing.value = false;
      editingConnectionId.value = null;
      
      settings.database_type = 'postgresql';
      settings.host = 'localhost';
      settings.port = 5432;
      settings.database_name = '';
      settings.username = '';
      settings.password = '';
      settings.connection_pool = 10;
      settings.timeout = 30;
    };
    
    // Lifecycle hooks
    onMounted(async () => {
      await fetchConnections();
    });
    
    return {
      savedConnections,
      settings,
      isTesting,
      showConfirmationModal,
      confirmationTitle,
      confirmationMessage,
      onDatabaseTypeChange,
      testConnection,
      saveSettings,
      editConnection,
      activateConnection,
      deleteConnection,
      confirmAction,
      closeConfirmationModal
    };
  }
};
</script>

<style scoped>
.database-selector {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.database-selection-form {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
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
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.database-list {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.database-list h2 {
  margin-top: 0;
  margin-bottom: 15px;
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

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.85em;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.actions {
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

/* RTL support */
html[dir="rtl"] th,
html[dir="rtl"] td {
  text-align: left;
}
</style>
