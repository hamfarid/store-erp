<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/PermissionsManager.vue -->
<template>
  <div class="permissions-manager">
    <div class="page-header">
      <h1>{{ $t('settings.permissions.title') }}</h1>
    </div>

    <div class="tabs">
      <div 
        class="tab" 
        :class="{ active: activeTab === 'roles' }" 
        @click="activeTab = 'roles'"
      >
        {{ $t('settings.permissions.roles') }}
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'permissions' }" 
        @click="activeTab = 'permissions'"
      >
        {{ $t('settings.permissions.permissions') }}
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'assignments' }" 
        @click="activeTab = 'assignments'"
      >
        {{ $t('settings.permissions.assignments') }}
      </div>
    </div>

    <!-- Roles Tab -->
    <div class="tab-content" v-if="activeTab === 'roles'">
      <div class="actions-bar">
        <button class="btn btn-primary" @click="openRoleModal()">
          <i class="fas fa-plus"></i> {{ $t('settings.permissions.addRole') }}
        </button>
        <div class="search">
          <input 
            type="text" 
            v-model="roleSearchQuery" 
            :placeholder="$t('common.search')" 
            @input="filterRoles"
          />
        </div>
      </div>

      <div class="data-table">
        <table>
          <thead>
            <tr>
              <th>{{ $t('settings.permissions.roleName') }}</th>
              <th>{{ $t('settings.permissions.roleDescription') }}</th>
              <th>{{ $t('settings.permissions.permissionsCount') }}</th>
              <th>{{ $t('settings.permissions.usersCount') }}</th>
              <th>{{ $t('settings.permissions.agentsCount') }}</th>
              <th>{{ $t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="role in filteredRoles" :key="role.id">
              <td>{{ role.name }}</td>
              <td>{{ role.description }}</td>
              <td>{{ role.permissions_count }}</td>
              <td>{{ role.users_count }}</td>
              <td>{{ role.agents_count }}</td>
              <td class="actions">
                <button class="btn btn-sm btn-edit" @click="openRoleModal(role)">
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  class="btn btn-sm btn-permissions" 
                  @click="openRolePermissionsModal(role)"
                >
                  <i class="fas fa-key"></i>
                </button>
                <button 
                  class="btn btn-sm btn-delete" 
                  @click="confirmDeleteRole(role)"
                  :disabled="role.is_system || role.users_count > 0 || role.agents_count > 0"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Permissions Tab -->
    <div class="tab-content" v-if="activeTab === 'permissions'">
      <div class="actions-bar">
        <button class="btn btn-primary" @click="openPermissionModal()">
          <i class="fas fa-plus"></i> {{ $t('settings.permissions.addPermission') }}
        </button>
        <div class="search">
          <input 
            type="text" 
            v-model="permissionSearchQuery" 
            :placeholder="$t('common.search')" 
            @input="filterPermissions"
          />
        </div>
        <div class="filter">
          <select v-model="moduleFilter" @change="filterPermissions">
            <option value="">{{ $t('settings.permissions.allModules') }}</option>
            <option v-for="module in modules" :key="module.id" :value="module.id">
              {{ module.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="data-table">
        <table>
          <thead>
            <tr>
              <th>{{ $t('settings.permissions.permissionName') }}</th>
              <th>{{ $t('settings.permissions.permissionDescription') }}</th>
              <th>{{ $t('settings.permissions.module') }}</th>
              <th>{{ $t('settings.permissions.type') }}</th>
              <th>{{ $t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="permission in filteredPermissions" :key="permission.id">
              <td>{{ permission.name }}</td>
              <td>{{ permission.description }}</td>
              <td>{{ getModuleName(permission.module_id) }}</td>
              <td>{{ getPermissionTypeLabel(permission.type) }}</td>
              <td class="actions">
                <button class="btn btn-sm btn-edit" @click="openPermissionModal(permission)">
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  class="btn btn-sm btn-delete" 
                  @click="confirmDeletePermission(permission)"
                  :disabled="permission.is_system"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Assignments Tab -->
    <div class="tab-content" v-if="activeTab === 'assignments'">
      <div class="assignment-container">
        <div class="assignment-section">
          <h2>{{ $t('settings.permissions.userAssignments') }}</h2>
          
          <div class="actions-bar">
            <button class="btn btn-primary" @click="openUserRoleModal()">
              <i class="fas fa-plus"></i> {{ $t('settings.permissions.assignRole') }}
            </button>
            <div class="search">
              <input 
                type="text" 
                v-model="userSearchQuery" 
                :placeholder="$t('common.search')" 
                @input="filterUsers"
              />
            </div>
          </div>

          <div class="data-table">
            <table>
              <thead>
                <tr>
                  <th>{{ $t('settings.permissions.userName') }}</th>
                  <th>{{ $t('settings.permissions.userEmail') }}</th>
                  <th>{{ $t('settings.permissions.assignedRoles') }}</th>
                  <th>{{ $t('common.actions') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td>{{ user.name }}</td>
                  <td>{{ user.email }}</td>
                  <td>
                    <div class="roles-list">
                      <span 
                        v-for="role in user.roles" 
                        :key="role.id" 
                        class="role-badge"
                      >
                        {{ role.name }}
                      </span>
                    </div>
                  </td>
                  <td class="actions">
                    <button class="btn btn-sm btn-edit" @click="openUserRoleModal(user)">
                      <i class="fas fa-edit"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="assignment-section">
          <h2>{{ $t('settings.permissions.agentAssignments') }}</h2>
          
          <div class="actions-bar">
            <button class="btn btn-primary" @click="openAgentRoleModal()">
              <i class="fas fa-plus"></i> {{ $t('settings.permissions.assignRole') }}
            </button>
            <div class="search">
              <input 
                type="text" 
                v-model="agentSearchQuery" 
                :placeholder="$t('common.search')" 
                @input="filterAgents"
              />
            </div>
          </div>

          <div class="data-table">
            <table>
              <thead>
                <tr>
                  <th>{{ $t('settings.permissions.agentName') }}</th>
                  <th>{{ $t('settings.permissions.agentType') }}</th>
                  <th>{{ $t('settings.permissions.assignedRoles') }}</th>
                  <th>{{ $t('common.actions') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="agent in filteredAgents" :key="agent.id">
                  <td>{{ agent.name }}</td>
                  <td>{{ agent.type }}</td>
                  <td>
                    <div class="roles-list">
                      <span 
                        v-for="role in agent.roles" 
                        :key="role.id" 
                        class="role-badge"
                      >
                        {{ role.name }}
                      </span>
                    </div>
                  </td>
                  <td class="actions">
                    <button class="btn btn-sm btn-edit" @click="openAgentRoleModal(agent)">
                      <i class="fas fa-edit"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Role Modal -->
    <div class="modal" v-if="showRoleModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditMode ? $t('settings.permissions.editRole') : $t('settings.permissions.addRole') }}</h2>
          <button class="close-btn" @click="closeRoleModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveRole">
            <div class="form-group">
              <label for="role-name">{{ $t('settings.permissions.roleName') }}</label>
              <input 
                type="text" 
                id="role-name" 
                v-model="roleForm.name" 
                :placeholder="$t('settings.permissions.roleNamePlaceholder')"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="role-description">{{ $t('settings.permissions.roleDescription') }}</label>
              <textarea 
                id="role-description" 
                v-model="roleForm.description" 
                :placeholder="$t('settings.permissions.roleDescriptionPlaceholder')"
                rows="3"
              ></textarea>
            </div>
            
            <div class="form-group">
              <div class="checkbox-option">
                <input type="checkbox" id="role-is-system" v-model="roleForm.is_system" />
                <label for="role-is-system">{{ $t('settings.permissions.isSystemRole') }}</label>
              </div>
              <div class="form-hint">{{ $t('settings.permissions.systemRoleHint') }}</div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeRoleModal">
                {{ $t('common.cancel') }}
              </button>
              <button type="submit" class="btn btn-primary">
                {{ isEditMode ? $t('common.save') : $t('common.create') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Permission Modal -->
    <div class="modal" v-if="showPermissionModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditMode ? $t('settings.permissions.editPermission') : $t('settings.permissions.addPermission') }}</h2>
          <button class="close-btn" @click="closePermissionModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="savePermission">
            <div class="form-group">
              <label for="permission-name">{{ $t('settings.permissions.permissionName') }}</label>
              <input 
                type="text" 
                id="permission-name" 
                v-model="permissionForm.name" 
                :placeholder="$t('settings.permissions.permissionNamePlaceholder')"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="permission-description">{{ $t('settings.permissions.permissionDescription') }}</label>
              <textarea 
                id="permission-description" 
                v-model="permissionForm.description" 
                :placeholder="$t('settings.permissions.permissionDescriptionPlaceholder')"
                rows="3"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="permission-module">{{ $t('settings.permissions.module') }}</label>
              <select id="permission-module" v-model="permissionForm.module_id" required>
                <option value="">{{ $t('settings.permissions.selectModule') }}</option>
                <option v-for="module in modules" :key="module.id" :value="module.id">
                  {{ module.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="permission-type">{{ $t('settings.permissions.type') }}</label>
              <select id="permission-type" v-model="permissionForm.type" required>
                <option value="">{{ $t('settings.permissions.selectType') }}</option>
                <option value="read">{{ $t('settings.permissions.typeRead') }}</option>
                <option value="write">{{ $t('settings.permissions.typeWrite') }}</option>
                <option value="admin">{{ $t('settings.permissions.typeAdmin') }}</option>
                <option value="view">{{ $t('settings.permissions.typeView') }}</option>
                <option value="approve">{{ $t('settings.permissions.typeApprove') }}</option>
              </select>
            </div>
            
            <div class="form-group">
              <div class="checkbox-option">
                <input type="checkbox" id="permission-is-system" v-model="permissionForm.is_system" />
                <label for="permission-is-system">{{ $t('settings.permissions.isSystemPermission') }}</label>
              </div>
              <div class="form-hint">{{ $t('settings.permissions.systemPermissionHint') }}</div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closePermissionModal">
                {{ $t('common.cancel') }}
              </button>
              <button type="submit" class="btn btn-primary">
                {{ isEditMode ? $t('common.save') : $t('common.create') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Role Permissions Modal -->
    <div class="modal" v-if="showRolePermissionsModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ $t('settings.permissions.manageRolePermissions', { role: selectedRole ? selectedRole.name : '' }) }}</h2>
          <button class="close-btn" @click="closeRolePermissionsModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="search-filter">
            <div class="search">
              <input 
                type="text" 
                v-model="rolePermissionSearchQuery" 
                :placeholder="$t('common.search')" 
                @input="filterRolePermissions"
              />
            </div>
            <div class="filter">
              <select v-model="rolePermissionModuleFilter" @change="filterRolePermissions">
                <option value="">{{ $t('settings.permissions.allModules') }}</option>
                <option v-for="module in modules" :key="module.id" :value="module.id">
                  {{ module.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="permissions-list">
            <div class="module-permissions" v-for="module in groupedPermissions" :key="module.id">
              <div class="module-header">
                <h3>{{ module.name }}</h3>
                <div class="module-actions">
                  <button 
                    class="btn btn-sm btn-select-all" 
                    @click="selectAllModulePermissions(module.id)"
                  >
                    {{ $t('settings.permissions.selectAll') }}
                  </button>
                  <button 
                    class="btn btn-sm btn-deselect-all" 
                    @click="deselectAllModulePermissions(module.id)"
                  >
                    {{ $t('settings.permissions.deselectAll') }}
                  </button>
                </div>
              </div>
              
              <div class="permissions-grid">
                <div 
                  v-for="permission in module.permissions" 
                  :key="permission.id" 
                  class="permission-item"
                >
                  <div class="checkbox-option">
                    <input 
                      type="checkbox" 
                      :id="'permission-' + permission.id" 
                      :value="permission.id" 
                      v-model="selectedPermissions"
                    />
                    <label :for="'permission-' + permission.id">
                      {{ permission.name }}
                      <span class="permission-type">{{ getPermissionTypeLabel(permission.type) }}</span>
                    </label>
                  </div>
                  <div class="permission-description">{{ permission.description }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeRolePermissionsModal">
              {{ $t('common.cancel') }}
            </button>
            <button type="button" class="btn btn-primary" @click="saveRolePermissions">
              {{ $t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- User Role Modal -->
    <div class="modal" v-if="showUserRoleModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditMode ? $t('settings.permissions.editUserRoles') : $t('settings.permissions.assignUserRole') }}</h2>
          <button class="close-btn" @click="closeUserRoleModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveUserRoles">
            <div class="form-group" v-if="!isEditMode">
              <label for="user-select">{{ $t('settings.permissions.selectUser') }}</label>
              <select id="user-select" v-model="userRoleForm.user_id" required>
                <option value="">{{ $t('settings.permissions.selectUserPlaceholder') }}</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.name }} ({{ user.email }})
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label>{{ $t('settings.permissions.assignRoles') }}</label>
              <div class="roles-selection">
                <div 
                  v-for="role in roles" 
                  :key="role.id" 
                  class="role-option"
                >
                  <div class="checkbox-option">
                    <input 
                      type="checkbox" 
                      :id="'user-role-' + role.id" 
                      :value="role.id" 
                      v-model="userRoleForm.role_ids"
                    />
                    <label :for="'user-role-' + role.id">{{ role.name }}</label>
                  </div>
                  <div class="role-description">{{ role.description }}</div>
                </div>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeUserRoleModal">
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

    <!-- Agent Role Modal -->
    <div class="modal" v-if="showAgentRoleModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditMode ? $t('settings.permissions.editAgentRoles') : $t('settings.permissions.assignAgentRole') }}</h2>
          <button class="close-btn" @click="closeAgentRoleModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveAgentRoles">
            <div class="form-group" v-if="!isEditMode">
              <label for="agent-select">{{ $t('settings.permissions.selectAgent') }}</label>
              <select id="agent-select" v-model="agentRoleForm.agent_id" required>
                <option value="">{{ $t('settings.permissions.selectAgentPlaceholder') }}</option>
                <option v-for="agent in agents" :key="agent.id" :value="agent.id">
                  {{ agent.name }} ({{ agent.type }})
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label>{{ $t('settings.permissions.assignRoles') }}</label>
              <div class="roles-selection">
                <div 
                  v-for="role in roles" 
                  :key="role.id" 
                  class="role-option"
                >
                  <div class="checkbox-option">
                    <input 
                      type="checkbox" 
                      :id="'agent-role-' + role.id" 
                      :value="role.id" 
                      v-model="agentRoleForm.role_ids"
                    />
                    <label :for="'agent-role-' + role.id">{{ role.name }}</label>
                  </div>
                  <div class="role-description">{{ role.description }}</div>
                </div>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeAgentRoleModal">
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
import aiAgentService from '@/services/aiAgentService';
import moduleService from '@/services/moduleService';
import permissionsService from '@/services/permissionsService';
import userService from '@/services/userService';
import { computed, onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'PermissionsManager',
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    
    // Data
    const activeTab = ref('roles');
    const roles = ref([]);
    const permissions = ref([]);
    const modules = ref([]);
    const users = ref([]);
    const agents = ref([]);
    
    // Search and filter
    const roleSearchQuery = ref('');
    const permissionSearchQuery = ref('');
    const userSearchQuery = ref('');
    const agentSearchQuery = ref('');
    const moduleFilter = ref('');
    const rolePermissionSearchQuery = ref('');
    const rolePermissionModuleFilter = ref('');
    
    // Filtered data
    const filteredRoles = ref([]);
    const filteredPermissions = ref([]);
    const filteredUsers = ref([]);
    const filteredAgents = ref([]);
    
    // Modal states
    const showRoleModal = ref(false);
    const showPermissionModal = ref(false);
    const showRolePermissionsModal = ref(false);
    const showUserRoleModal = ref(false);
    const showAgentRoleModal = ref(false);
    const showConfirmationModal = ref(false);
    const isProcessing = ref(false);
    const isEditMode = ref(false);
    
    // Selected items
    const selectedRole = ref(null);
    const selectedPermissions = ref([]);
    
    // Form data
    const roleForm = reactive({
      name: '',
      description: '',
      is_system: false
    });
    
    const permissionForm = reactive({
      name: '',
      description: '',
      module_id: '',
      type: '',
      is_system: false
    });
    
    const userRoleForm = reactive({
      user_id: '',
      role_ids: []
    });
    
    const agentRoleForm = reactive({
      agent_id: '',
      role_ids: []
    });
    
    // Confirmation modal
    const confirmationTitle = ref('');
    const confirmationMessage = ref('');
    const confirmationCallback = ref(null);
    
    // Processing modal
    const processingTitle = ref('');
    const processingMessage = ref('');
    
    // Fetch data
    const fetchRoles = async () => {
      try {
        const response = await permissionsService.getRoles();
        roles.value = response.data;
        filteredRoles.value = [...roles.value];
      } catch (error) {
        showToast(t('settings.permissions.errorFetchingRoles'), 'error');
        console.error('Error fetching roles:', error);
      }
    };
    
    const fetchPermissions = async () => {
      try {
        const response = await permissionsService.getPermissions();
        permissions.value = response.data;
        filteredPermissions.value = [...permissions.value];
      } catch (error) {
        showToast(t('settings.permissions.errorFetchingPermissions'), 'error');
        console.error('Error fetching permissions:', error);
      }
    };
    
    const fetchModules = async () => {
      try {
        const response = await moduleService.getModules();
        modules.value = response.data;
      } catch (error) {
        showToast(t('settings.permissions.errorFetchingModules'), 'error');
        console.error('Error fetching modules:', error);
      }
    };
    
    const fetchUsers = async () => {
      try {
        const response = await userService.getUsers();
        users.value = response.data;
        filteredUsers.value = [...users.value];
      } catch (error) {
        showToast(t('settings.permissions.errorFetchingUsers'), 'error');
        console.error('Error fetching users:', error);
      }
    };
    
    const fetchAgents = async () => {
      try {
        const response = await aiAgentService.getAgents();
        agents.value = response.data;
        filteredAgents.value = [...agents.value];
      } catch (error) {
        showToast(t('settings.permissions.errorFetchingAgents'), 'error');
        console.error('Error fetching agents:', error);
      }
    };
    
    // Filter functions
    const filterRoles = () => {
      if (!roleSearchQuery.value) {
        filteredRoles.value = [...roles.value];
        return;
      }
      
      const query = roleSearchQuery.value.toLowerCase();
      filteredRoles.value = roles.value.filter(role => 
        role.name.toLowerCase().includes(query) || 
        role.description.toLowerCase().includes(query)
      );
    };
    
    const filterPermissions = () => {
      let filtered = [...permissions.value];
      
      if (permissionSearchQuery.value) {
        const query = permissionSearchQuery.value.toLowerCase();
        filtered = filtered.filter(permission => 
          permission.name.toLowerCase().includes(query) || 
          permission.description.toLowerCase().includes(query)
        );
      }
      
      if (moduleFilter.value) {
        filtered = filtered.filter(permission => 
          permission.module_id === moduleFilter.value
        );
      }
      
      filteredPermissions.value = filtered;
    };
    
    const filterUsers = () => {
      if (!userSearchQuery.value) {
        filteredUsers.value = [...users.value];
        return;
      }
      
      const query = userSearchQuery.value.toLowerCase();
      filteredUsers.value = users.value.filter(user => 
        user.name.toLowerCase().includes(query) || 
        user.email.toLowerCase().includes(query)
      );
    };
    
    const filterAgents = () => {
      if (!agentSearchQuery.value) {
        filteredAgents.value = [...agents.value];
        return;
      }
      
      const query = agentSearchQuery.value.toLowerCase();
      filteredAgents.value = agents.value.filter(agent => 
        agent.name.toLowerCase().includes(query) || 
        agent.type.toLowerCase().includes(query)
      );
    };
    
    const filterRolePermissions = () => {
      // This function is used to filter permissions in the role permissions modal
      // The filtering is applied to the groupedPermissions computed property
    };
    
    // Role actions
    const openRoleModal = (role = null) => {
      if (role) {
        // Edit mode
        isEditMode.value = true;
        roleForm.name = role.name;
        roleForm.description = role.description;
        roleForm.is_system = role.is_system;
        selectedRole.value = role;
      } else {
        // Create mode
        isEditMode.value = false;
        roleForm.name = '';
        roleForm.description = '';
        roleForm.is_system = false;
        selectedRole.value = null;
      }
      
      showRoleModal.value = true;
    };
    
    const closeRoleModal = () => {
      showRoleModal.value = false;
      isEditMode.value = false;
      selectedRole.value = null;
    };
    
    const saveRole = async () => {
      isProcessing.value = true;
      processingTitle.value = isEditMode.value 
        ? t('settings.permissions.updatingRole') 
        : t('settings.permissions.creatingRole');
      processingMessage.value = isEditMode.value 
        ? t('settings.permissions.updatingRoleMessage') 
        : t('settings.permissions.creatingRoleMessage');
      
      try {
        if (isEditMode.value) {
          await permissionsService.updateRole(selectedRole.value.id, roleForm);
          
          // Update role in the list
          const index = roles.value.findIndex(r => r.id === selectedRole.value.id);
          if (index !== -1) {
            roles.value[index] = { 
              ...roles.value[index], 
              ...roleForm 
            };
          }
          
          showToast(t('settings.permissions.roleUpdated'), 'success');
        } else {
          const response = await permissionsService.createRole(roleForm);
          
          // Add new role to the list
          roles.value.push(response.data);
          
          showToast(t('settings.permissions.roleCreated'), 'success');
        }
        
        // Refresh filtered roles
        filterRoles();
        
        closeRoleModal();
      } catch (error) {
        showToast(
          isEditMode.value 
            ? t('settings.permissions.errorUpdatingRole') 
            : t('settings.permissions.errorCreatingRole'), 
          'error'
        );
        console.error('Error saving role:', error);
      } finally {
        isProcessing.value = false;
      }
    };
    
    const confirmDeleteRole = (role) => {
      if (role.is_system) {
        showToast(t('settings.permissions.cannotDeleteSystemRole'), 'error');
        return;
      }
      
      if (role.users_count > 0 || role.agents_count > 0) {
        showToast(t('settings.permissions.cannotDeleteAssignedRole'), 'error');
        return;
      }
      
      confirmationTitle.value = t('settings.permissions.deleteRole');
      confirmationMessage.value = t('settings.permissions.deleteRoleConfirmation', { name: role.name });
      
      confirmationCallback.value = async () => {
        isProcessing.value = true;
        processingTitle.value = t('settings.permissions.deletingRole');
        processingMessage.value = t('settings.permissions.deletingRoleMessage', { name: role.name });
        
        try {
          await permissionsService.deleteRole(role.id);
          
          // Remove role from the list
          roles.value = roles.value.filter(r => r.id !== role.id);
          filteredRoles.value = filteredRoles.value.filter(r => r.id !== role.id);
          
          showToast(t('settings.permissions.roleDeleted'), 'success');
        } catch (error) {
          showToast(t('settings.permissions.errorDeletingRole'), 'error');
          console.error('Error deleting role:', error);
        } finally {
          isProcessing.value = false;
          closeConfirmationModal();
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    // Permission actions
    const openPermissionModal = (permission = null) => {
      if (permission) {
        // Edit mode
        isEditMode.value = true;
        permissionForm.name = permission.name;
        permissionForm.description = permission.description;
        permissionForm.module_id = permission.module_id;
        permissionForm.type = permission.type;
        permissionForm.is_system = permission.is_system;
        selectedRole.value = permission;
      } else {
        // Create mode
        isEditMode.value = false;
        permissionForm.name = '';
        permissionForm.description = '';
        permissionForm.module_id = '';
        permissionForm.type = '';
        permissionForm.is_system = false;
        selectedRole.value = null;
      }
      
      showPermissionModal.value = true;
    };
    
    const closePermissionModal = () => {
      showPermissionModal.value = false;
      isEditMode.value = false;
      selectedRole.value = null;
    };
    
    const savePermission = async () => {
      isProcessing.value = true;
      processingTitle.value = isEditMode.value 
        ? t('settings.permissions.updatingPermission') 
        : t('settings.permissions.creatingPermission');
      processingMessage.value = isEditMode.value 
        ? t('settings.permissions.updatingPermissionMessage') 
        : t('settings.permissions.creatingPermissionMessage');
      
      try {
        if (isEditMode.value) {
          await permissionsService.updatePermission(selectedRole.value.id, permissionForm);
          
          // Update permission in the list
          const index = permissions.value.findIndex(p => p.id === selectedRole.value.id);
          if (index !== -1) {
            permissions.value[index] = { 
              ...permissions.value[index], 
              ...permissionForm 
            };
          }
          
          showToast(t('settings.permissions.permissionUpdated'), 'success');
        } else {
          const response = await permissionsService.createPermission(permissionForm);
          
          // Add new permission to the list
          permissions.value.push(response.data);
          
          showToast(t('settings.permissions.permissionCreated'), 'success');
        }
        
        // Refresh filtered permissions
        filterPermissions();
        
        closePermissionModal();
      } catch (error) {
        showToast(
          isEditMode.value 
            ? t('settings.permissions.errorUpdatingPermission') 
            : t('settings.permissions.errorCreatingPermission'), 
          'error'
        );
        console.error('Error saving permission:', error);
      } finally {
        isProcessing.value = false;
      }
    };
    
    const confirmDeletePermission = (permission) => {
      if (permission.is_system) {
        showToast(t('settings.permissions.cannotDeleteSystemPermission'), 'error');
        return;
      }
      
      confirmationTitle.value = t('settings.permissions.deletePermission');
      confirmationMessage.value = t('settings.permissions.deletePermissionConfirmation', { name: permission.name });
      
      confirmationCallback.value = async () => {
        isProcessing.value = true;
        processingTitle.value = t('settings.permissions.deletingPermission');
        processingMessage.value = t('settings.permissions.deletingPermissionMessage', { name: permission.name });
        
        try {
          await permissionsService.deletePermission(permission.id);
          
          // Remove permission from the list
          permissions.value = permissions.value.filter(p => p.id !== permission.id);
          filteredPermissions.value = filteredPermissions.value.filter(p => p.id !== permission.id);
          
          showToast(t('settings.permissions.permissionDeleted'), 'success');
        } catch (error) {
          showToast(t('settings.permissions.errorDeletingPermission'), 'error');
          console.error('Error deleting permission:', error);
        } finally {
          isProcessing.value = false;
          closeConfirmationModal();
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    // Role permissions actions
    const openRolePermissionsModal = async (role) => {
      selectedRole.value = role;
      isProcessing.value = true;
      processingTitle.value = t('settings.permissions.loadingPermissions');
      processingMessage.value = t('settings.permissions.loadingPermissionsMessage');
      
      try {
        const response = await permissionsService.getRolePermissions(role.id);
        selectedPermissions.value = response.data.map(p => p.id);
        showRolePermissionsModal.value = true;
      } catch (error) {
        showToast(t('settings.permissions.errorLoadingPermissions'), 'error');
        console.error('Error loading role permissions:', error);
      } finally {
        isProcessing.value = false;
      }
    };
    
    const closeRolePermissionsModal = () => {
      showRolePermissionsModal.value = false;
      selectedRole.value = null;
      selectedPermissions.value = [];
      rolePermissionSearchQuery.value = '';
      rolePermissionModuleFilter.value = '';
    };
    
    const saveRolePermissions = async () => {
      if (!selectedRole.value) return;
      
      isProcessing.value = true;
      processingTitle.value = t('settings.permissions.savingPermissions');
      processingMessage.value = t('settings.permissions.savingPermissionsMessage');
      
      try {
        await permissionsService.updateRolePermissions(selectedRole.value.id, {
          permission_ids: selectedPermissions.value
        });
        
        showToast(t('settings.permissions.permissionsSaved'), 'success');
        closeRolePermissionsModal();
      } catch (error) {
        showToast(t('settings.permissions.errorSavingPermissions'), 'error');
        console.error('Error saving role permissions:', error);
      } finally {
        isProcessing.value = false;
      }
    };
    
    const selectAllModulePermissions = (moduleId) => {
      const modulePermissions = permissions.value
        .filter(p => p.module_id === moduleId)
        .map(p => p.id);
      
      // Add all module permissions to selected permissions (avoid duplicates)
      selectedPermissions.value = [...new Set([...selectedPermissions.value, ...modulePermissions])];
    };
    
    const deselectAllModulePermissions = (moduleId) => {
      const modulePermissions = permissions.value
        .filter(p => p.module_id === moduleId)
        .map(p => p.id);
      
      // Remove all module permissions from selected permissions
      selectedPermissions.value = selectedPermissions.value.filter(id => !modulePermissions.includes(id));
    };
    
    // User role actions
    const openUserRoleModal = async (user = null) => {
      if (user) {
        // Edit mode
        isEditMode.value = true;
        userRoleForm.user_id = user.id;
        userRoleForm.role_ids = user.roles.map(r => r.id);
        selectedRole.value = user;
      } else {
        // Create mode
        isEditMode.value = false;
        userRoleForm.user_id = '';
        userRoleForm.role_ids = [];
        selectedRole.value = null;
      }
      
      showUserRoleModal.value = true;
    };
    
    const closeUserRoleModal = () => {
      showUserRoleModal.value = false;
      isEditMode.value = false;
      selectedRole.value = null;
    };
    
    const saveUserRoles = async () => {
      isProcessing.value = true;
      processingTitle.value = t('settings.permissions.savingUserRoles');
      processingMessage.value = t('settings.permissions.savingUserRolesMessage');
      
      try {
        await permissionsService.updateUserRoles(userRoleForm.user_id, {
          role_ids: userRoleForm.role_ids
        });
        
        // Update user roles in the list
        await fetchUsers();
        
        showToast(t('settings.permissions.userRolesSaved'), 'success');
        closeUserRoleModal();
      } catch (error) {
        showToast(t('settings.permissions.errorSavingUserRoles'), 'error');
        console.error('Error saving user roles:', error);
      } finally {
        isProcessing.value = false;
      }
    };
    
    // Agent role actions
    const openAgentRoleModal = async (agent = null) => {
      if (agent) {
        // Edit mode
        isEditMode.value = true;
        agentRoleForm.agent_id = agent.id;
        agentRoleForm.role_ids = agent.roles.map(r => r.id);
        selectedRole.value = agent;
      } else {
        // Create mode
        isEditMode.value = false;
        agentRoleForm.agent_id = '';
        agentRoleForm.role_ids = [];
        selectedRole.value = null;
      }
      
      showAgentRoleModal.value = true;
    };
    
    const closeAgentRoleModal = () => {
      showAgentRoleModal.value = false;
      isEditMode.value = false;
      selectedRole.value = null;
    };
    
    const saveAgentRoles = async () => {
      isProcessing.value = true;
      processingTitle.value = t('settings.permissions.savingAgentRoles');
      processingMessage.value = t('settings.permissions.savingAgentRolesMessage');
      
      try {
        await permissionsService.updateAgentRoles(agentRoleForm.agent_id, {
          role_ids: agentRoleForm.role_ids
        });
        
        // Update agent roles in the list
        await fetchAgents();
        
        showToast(t('settings.permissions.agentRolesSaved'), 'success');
        closeAgentRoleModal();
      } catch (error) {
        showToast(t('settings.permissions.errorSavingAgentRoles'), 'error');
        console.error('Error saving agent roles:', error);
      } finally {
        isProcessing.value = false;
      }
    };
    
    // Confirmation modal
    const closeConfirmationModal = () => {
      showConfirmationModal.value = false;
      confirmationTitle.value = '';
      confirmationMessage.value = '';
      confirmationCallback.value = null;
    };
    
    const confirmAction = () => {
      if (confirmationCallback.value) {
        confirmationCallback.value();
      }
    };
    
    // Computed properties
    const groupedPermissions = computed(() => {
      // Group permissions by module
      const moduleMap = new Map();
      
      // Filter permissions based on search and module filter
      let filteredPerms = [...permissions.value];
      
      if (rolePermissionSearchQuery.value) {
        const query = rolePermissionSearchQuery.value.toLowerCase();
        filteredPerms = filteredPerms.filter(p => 
          p.name.toLowerCase().includes(query) || 
          p.description.toLowerCase().includes(query)
        );
      }
      
      if (rolePermissionModuleFilter.value) {
        filteredPerms = filteredPerms.filter(p => 
          p.module_id === rolePermissionModuleFilter.value
        );
      }
      
      // Group filtered permissions by module
      filteredPerms.forEach(permission => {
        const moduleId = permission.module_id;
        if (!moduleMap.has(moduleId)) {
          const module = modules.value.find(m => m.id === moduleId);
          moduleMap.set(moduleId, {
            id: moduleId,
            name: module ? module.name : 'Unknown',
            permissions: []
          });
        }
        moduleMap.get(moduleId).permissions.push(permission);
      });
      
      // Convert map to array and sort by module name
      return Array.from(moduleMap.values()).sort((a, b) => a.name.localeCompare(b.name));
    });
    
    // Utility functions
    const getModuleName = (moduleId) => {
      const module = modules.value.find(m => m.id === moduleId);
      return module ? module.name : 'Unknown';
    };
    
    const getPermissionTypeLabel = (type) => {
      switch (type) {
        case 'read':
          return t('settings.permissions.typeRead');
        case 'write':
          return t('settings.permissions.typeWrite');
        case 'admin':
          return t('settings.permissions.typeAdmin');
        case 'view':
          return t('settings.permissions.typeView');
        case 'approve':
          return t('settings.permissions.typeApprove');
        default:
          return type;
      }
    };
    
    // Lifecycle hooks
    onMounted(async () => {
      await Promise.all([
        fetchRoles(),
        fetchPermissions(),
        fetchModules(),
        fetchUsers(),
        fetchAgents()
      ]);
    });
    
    return {
      activeTab,
      roles,
      permissions,
      modules,
      users,
      agents,
      filteredRoles,
      filteredPermissions,
      filteredUsers,
      filteredAgents,
      roleSearchQuery,
      permissionSearchQuery,
      userSearchQuery,
      agentSearchQuery,
      moduleFilter,
      rolePermissionSearchQuery,
      rolePermissionModuleFilter,
      showRoleModal,
      showPermissionModal,
      showRolePermissionsModal,
      showUserRoleModal,
      showAgentRoleModal,
      showConfirmationModal,
      isProcessing,
      isEditMode,
      selectedRole,
      selectedPermissions,
      roleForm,
      permissionForm,
      userRoleForm,
      agentRoleForm,
      confirmationTitle,
      confirmationMessage,
      processingTitle,
      processingMessage,
      groupedPermissions,
      filterRoles,
      filterPermissions,
      filterUsers,
      filterAgents,
      filterRolePermissions,
      openRoleModal,
      closeRoleModal,
      saveRole,
      confirmDeleteRole,
      openPermissionModal,
      closePermissionModal,
      savePermission,
      confirmDeletePermission,
      openRolePermissionsModal,
      closeRolePermissionsModal,
      saveRolePermissions,
      selectAllModulePermissions,
      deselectAllModulePermissions,
      openUserRoleModal,
      closeUserRoleModal,
      saveUserRoles,
      openAgentRoleModal,
      closeAgentRoleModal,
      saveAgentRoles,
      closeConfirmationModal,
      confirmAction,
      getModuleName,
      getPermissionTypeLabel
    };
  }
};
</script>

<style scoped>
.permissions-manager {
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

.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search input,
.filter select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.data-table {
  width: 100%;
  overflow-x: auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

.actions {
  display: flex;
  gap: 5px;
}

.roles-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.role-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75em;
  background-color: #e9ecef;
  color: #495057;
}

.assignment-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.assignment-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.assignment-section h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

.search-filter {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.permissions-list {
  margin-bottom: 20px;
}

.module-permissions {
  margin-bottom: 20px;
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.module-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.module-actions {
  display: flex;
  gap: 10px;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 10px;
}

.permission-item {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.permission-type {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 0.7em;
  background-color: #e9ecef;
  color: #495057;
  margin-right: 5px;
}

.permission-description {
  font-size: 0.85em;
  color: #6c757d;
  margin-top: 5px;
}

.roles-selection {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
}

.role-option {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.role-option:last-child {
  border-bottom: none;
}

.role-description {
  font-size: 0.85em;
  color: #6c757d;
  margin-top: 5px;
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

.btn-permissions {
  background-color: #ffc107;
  color: #212529;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}

.btn-select-all,
.btn-deselect-all {
  background-color: #6c757d;
  color: white;
  padding: 2px 8px;
  font-size: 0.8em;
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

/* Responsive styles */
@media (min-width: 768px) {
  .assignment-container {
    grid-template-columns: 1fr 1fr;
  }
}

/* RTL support */
html[dir="rtl"] th,
html[dir="rtl"] td {
  text-align: left;
}

html[dir="rtl"] .checkbox-option input {
  margin-left: 0;
  margin-right: 8px;
}

html[dir="rtl"] .permission-type {
  margin-right: 0;
  margin-left: 5px;
}
</style>
