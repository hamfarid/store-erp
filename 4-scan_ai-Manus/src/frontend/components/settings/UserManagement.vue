<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/UserManagement.vue -->
<template>
  <div class="user-management">
    <div class="page-header">
      <h1>{{ $t('settings.userManagement.title') }}</h1>
      <div class="actions">
        <button class="btn btn-primary" @click="showAddUserModal">
          <i class="fas fa-plus"></i> {{ $t('settings.userManagement.addUser') }}
        </button>
      </div>
    </div>

    <div class="filters">
      <div class="search">
        <input 
          type="text" 
          v-model="searchQuery" 
          :placeholder="$t('common.search')" 
          @input="filterUsers"
        />
      </div>
      <div class="filter-role">
        <select v-model="roleFilter" @change="filterUsers">
          <option value="">{{ $t('settings.userManagement.allRoles') }}</option>
          <option v-for="role in roles" :key="role.id" :value="role.id">
            {{ role.name }}
          </option>
        </select>
      </div>
      <div class="filter-status">
        <select v-model="statusFilter" @change="filterUsers">
          <option value="">{{ $t('settings.userManagement.allStatuses') }}</option>
          <option value="active">{{ $t('settings.userManagement.active') }}</option>
          <option value="inactive">{{ $t('settings.userManagement.inactive') }}</option>
          <option value="blocked">{{ $t('settings.userManagement.blocked') }}</option>
        </select>
      </div>
    </div>

    <div class="users-table">
      <table>
        <thead>
          <tr>
            <th>{{ $t('settings.userManagement.username') }}</th>
            <th>{{ $t('settings.userManagement.email') }}</th>
            <th>{{ $t('settings.userManagement.roles') }}</th>
            <th>{{ $t('settings.userManagement.status') }}</th>
            <th>{{ $t('settings.userManagement.lastLogin') }}</th>
            <th>{{ $t('common.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span class="role-badge" v-for="role in user.roles" :key="role.id">
                {{ role.name }}
              </span>
            </td>
            <td>
              <span :class="['status-badge', getUserStatusClass(user)]">
                {{ getUserStatusText(user) }}
              </span>
            </td>
            <td>{{ formatDate(user.last_login) }}</td>
            <td class="actions">
              <button class="btn btn-sm btn-edit" @click="editUser(user)">
                <i class="fas fa-edit"></i>
              </button>
              <button class="btn btn-sm btn-reset-password" @click="resetPassword(user)">
                <i class="fas fa-key"></i>
              </button>
              <button 
                v-if="isUserBlocked(user)"
                class="btn btn-sm btn-unblock" 
                @click="unblockUser(user)"
                title="إلغاء حظر المستخدم"
              >
                <i class="fas fa-unlock"></i>
              </button>
              <button 
                v-else
                class="btn btn-sm" 
                :class="user.is_active ? 'btn-deactivate' : 'btn-activate'"
                @click="toggleUserStatus(user)"
              >
                <i :class="user.is_active ? 'fas fa-user-slash' : 'fas fa-user-check'"></i>
              </button>
              <button class="btn btn-sm btn-delete" @click="deleteUser(user)">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit User Modal -->
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? $t('settings.userManagement.editUser') : $t('settings.userManagement.addUser') }}</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveUser">
            <div class="form-group">
              <label for="username">{{ $t('settings.userManagement.username') }}</label>
              <input 
                type="text" 
                id="username" 
                v-model="currentUser.username" 
                required
                :disabled="isEditing"
              />
            </div>
            <div class="form-group">
              <label for="email">{{ $t('settings.userManagement.email') }}</label>
              <input 
                type="email" 
                id="email" 
                v-model="currentUser.email" 
                required
              />
            </div>
            <div class="form-group" v-if="!isEditing">
              <label for="password">{{ $t('settings.userManagement.password') }}</label>
              <input 
                type="password" 
                id="password" 
                v-model="currentUser.password" 
                required
              />
            </div>
            <div class="form-group">
              <label>{{ $t('settings.userManagement.roles') }}</label>
              <div class="roles-checkboxes">
                <div v-for="role in roles" :key="role.id" class="role-checkbox">
                  <input 
                    type="checkbox" 
                    :id="'role-' + role.id" 
                    :value="role.id" 
                    v-model="currentUser.roleIds"
                  />
                  <label :for="'role-' + role.id">{{ role.name }}</label>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label for="status">{{ $t('settings.userManagement.status') }}</label>
              <select id="status" v-model="currentUser.is_active">
                <option :value="true">{{ $t('settings.userManagement.active') }}</option>
                <option :value="false">{{ $t('settings.userManagement.inactive') }}</option>
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

    <!-- Reset Password Modal -->
    <div class="modal" v-if="showResetPasswordModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ $t('settings.userManagement.resetPassword') }}</h2>
          <button class="close-btn" @click="closeResetPasswordModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="confirmResetPassword">
            <div class="form-group">
              <label for="new-password">{{ $t('settings.userManagement.newPassword') }}</label>
              <input 
                type="password" 
                id="new-password" 
                v-model="newPassword" 
                required
              />
            </div>
            <div class="form-group">
              <label for="confirm-password">{{ $t('settings.userManagement.confirmPassword') }}</label>
              <input 
                type="password" 
                id="confirm-password" 
                v-model="confirmPassword" 
                required
              />
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeResetPasswordModal">
                {{ $t('common.cancel') }}
              </button>
              <button type="submit" class="btn btn-primary">
                {{ $t('common.confirm') }}
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
import roleService from '@/services/roleService';
import securityService from '@/services/securityService';
import userService from '@/services/userService';
import { defineComponent, onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default defineComponent({
  name: 'UserManagement',
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();
    
    // Data
    const users = ref([]);
    const roles = ref([]);
    const filteredUsers = ref([]);
    const searchQuery = ref('');
    const roleFilter = ref('');
    const statusFilter = ref('');
    
    // Modal states
    const showModal = ref(false);
    const showResetPasswordModal = ref(false);
    const showConfirmationModal = ref(false);
    const isEditing = ref(false);
    const currentUser = reactive({
      id: null,
      username: '',
      email: '',
      password: '',
      roleIds: [],
      is_active: true
    });
    const userToReset = ref(null);
    const newPassword = ref('');
    const confirmPassword = ref('');
    
    // Confirmation modal
    const confirmationTitle = ref('');
    const confirmationMessage = ref('');
    const confirmationCallback = ref(null);
    
    // Fetch data
    const fetchUsers = async () => {
      try {
        const response = await userService.getUsers();
        users.value = response.data;
        filteredUsers.value = [...users.value];
      } catch (error) {
        showToast(t('settings.userManagement.errorFetchingUsers'), 'error');
        console.error('Error fetching users:', error);
      }
    };
    
    const fetchRoles = async () => {
      try {
        const response = await roleService.getRoles();
        roles.value = response.data;
      } catch (error) {
        showToast(t('settings.userManagement.errorFetchingRoles'), 'error');
        console.error('Error fetching roles:', error);
      }
    };
    
    // Helper functions
    const isUserBlocked = (user) => {
      return user.locked_until && new Date(user.locked_until) > new Date();
    };
    
    const getUserStatusClass = (user) => {
      if (isUserBlocked(user)) return 'blocked';
      return user.is_active ? 'active' : 'inactive';
    };
    
    const getUserStatusText = (user) => {
      if (isUserBlocked(user)) return t('settings.userManagement.blocked');
      return user.is_active ? t('settings.userManagement.active') : t('settings.userManagement.inactive');
    };
    
    // Filter users
    const filterUsers = () => {
      filteredUsers.value = users.value.filter(user => {
        const matchesSearch = searchQuery.value === '' || 
          user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          user.email.toLowerCase().includes(searchQuery.value.toLowerCase());
        
        const matchesRole = roleFilter.value === '' || 
          user.roles.some(role => role.id === roleFilter.value);
        
        let matchesStatus = true;
        if (statusFilter.value === 'active') {
          matchesStatus = user.is_active && !isUserBlocked(user);
        } else if (statusFilter.value === 'inactive') {
          matchesStatus = !user.is_active && !isUserBlocked(user);
        } else if (statusFilter.value === 'blocked') {
          matchesStatus = isUserBlocked(user);
        }
        
        return matchesSearch && matchesRole && matchesStatus;
      });
    };
    
    // User actions
    const showAddUserModal = () => {
      isEditing.value = false;
      resetCurrentUser();
      showModal.value = true;
    };
    
    const editUser = (user) => {
      isEditing.value = true;
      currentUser.id = user.id;
      currentUser.username = user.username;
      currentUser.email = user.email;
      currentUser.is_active = user.is_active;
      currentUser.roleIds = user.roles.map(role => role.id);
      showModal.value = true;
    };
    
    const resetPassword = (user) => {
      userToReset.value = user;
      newPassword.value = '';
      confirmPassword.value = '';
      showResetPasswordModal.value = true;
    };
    
    const unblockUser = (user) => {
      confirmationTitle.value = t('settings.userManagement.unblockUser');
      confirmationMessage.value = t('settings.userManagement.unblockUserConfirmation', { username: user.username });
      
      confirmationCallback.value = async () => {
        try {
          await securityService.unblockUser(user.id);
          // Update user in the list
          user.locked_until = null;
          user.failed_login_attempts = 0;
          showToast(t('settings.userManagement.userUnblocked'), 'success');
          closeConfirmationModal();
          filterUsers();
        } catch (error) {
          showToast(t('settings.userManagement.errorUnblockingUser'), 'error');
          console.error('Error unblocking user:', error);
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    const toggleUserStatus = (user) => {
      confirmationTitle.value = user.is_active 
        ? t('settings.userManagement.deactivateUser') 
        : t('settings.userManagement.activateUser');
      
      confirmationMessage.value = user.is_active 
        ? t('settings.userManagement.deactivateUserConfirmation', { username: user.username }) 
        : t('settings.userManagement.activateUserConfirmation', { username: user.username });
      
      confirmationCallback.value = async () => {
        try {
          await userService.updateUserStatus(user.id, !user.is_active);
          user.is_active = !user.is_active;
          showToast(
            user.is_active 
              ? t('settings.userManagement.userActivated') 
              : t('settings.userManagement.userDeactivated'), 
            'success'
          );
          closeConfirmationModal();
          filterUsers();
        } catch (error) {
          showToast(t('settings.userManagement.errorUpdatingStatus'), 'error');
          console.error('Error updating user status:', error);
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    const deleteUser = (user) => {
      confirmationTitle.value = t('settings.userManagement.deleteUser');
      confirmationMessage.value = t('settings.userManagement.deleteUserConfirmation', { username: user.username });
      
      confirmationCallback.value = async () => {
        try {
          await userService.deleteUser(user.id);
          users.value = users.value.filter(u => u.id !== user.id);
          filteredUsers.value = filteredUsers.value.filter(u => u.id !== user.id);
          showToast(t('settings.userManagement.userDeleted'), 'success');
          closeConfirmationModal();
        } catch (error) {
          showToast(t('settings.userManagement.errorDeletingUser'), 'error');
          console.error('Error deleting user:', error);
        }
      };
      
      showConfirmationModal.value = true;
    };
    
    // Form actions
    const saveUser = async () => {
      try {
        if (isEditing.value) {
          await userService.updateUser(currentUser.id, {
            email: currentUser.email,
            is_active: currentUser.is_active,
            role_ids: currentUser.roleIds
          });
          
          // Update user in the list
          const index = users.value.findIndex(u => u.id === currentUser.id);
          if (index !== -1) {
            users.value[index].email = currentUser.email;
            users.value[index].is_active = currentUser.is_active;
            users.value[index].roles = roles.value.filter(role => currentUser.roleIds.includes(role.id));
          }
          
          showToast(t('settings.userManagement.userUpdated'), 'success');
        } else {
          const response = await userService.createUser({
            username: currentUser.username,
            email: currentUser.email,
            password: currentUser.password,
            is_active: currentUser.is_active,
            role_ids: currentUser.roleIds
          });
          
          // Add new user to the list
          const newUser = response.data;
          newUser.roles = roles.value.filter(role => currentUser.roleIds.includes(role.id));
          users.value.push(newUser);
          
          showToast(t('settings.userManagement.userCreated'), 'success');
        }
        
        closeModal();
        filterUsers();
      } catch (error) {
        showToast(
          isEditing.value 
            ? t('settings.userManagement.errorUpdatingUser') 
            : t('settings.userManagement.errorCreatingUser'), 
          'error'
        );
        console.error('Error saving user:', error);
      }
    };
    
    const confirmResetPassword = async () => {
      if (newPassword.value !== confirmPassword.value) {
        showToast(t('settings.userManagement.passwordsDoNotMatch'), 'error');
        return;
      }
      
      try {
        await userService.resetPassword(userToReset.value.id, newPassword.value);
        showToast(t('settings.userManagement.passwordReset'), 'success');
        closeResetPasswordModal();
      } catch (error) {
        showToast(t('settings.userManagement.errorResettingPassword'), 'error');
        console.error('Error resetting password:', error);
      }
    };
    
    const confirmAction = () => {
      if (confirmationCallback.value) {
        confirmationCallback.value();
      }
    };
    
    // Modal helpers
    const resetCurrentUser = () => {
      currentUser.id = null;
      currentUser.username = '';
      currentUser.email = '';
      currentUser.password = '';
      currentUser.roleIds = [];
      currentUser.is_active = true;
    };
    
    const closeModal = () => {
      showModal.value = false;
      resetCurrentUser();
    };
    
    const closeResetPasswordModal = () => {
      showResetPasswordModal.value = false;
      userToReset.value = null;
      newPassword.value = '';
      confirmPassword.value = '';
    };
    
    const closeConfirmationModal = () => {
      showConfirmationModal.value = false;
      confirmationTitle.value = '';
      confirmationMessage.value = '';
      confirmationCallback.value = null;
    };
    
    // Utility functions
    const formatDate = (dateString) => {
      if (!dateString) return t('common.never');
      
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };
    
    // Lifecycle hooks
    onMounted(() => {
      fetchUsers();
      fetchRoles();
    });
    
    return {
      users,
      roles,
      filteredUsers,
      searchQuery,
      roleFilter,
      statusFilter,
      showModal,
      showResetPasswordModal,
      showConfirmationModal,
      isEditing,
      currentUser,
      userToReset,
      newPassword,
      confirmPassword,
      confirmationTitle,
      confirmationMessage,
      isUserBlocked,
      getUserStatusClass,
      getUserStatusText,
      filterUsers,
      showAddUserModal,
      editUser,
      resetPassword,
      unblockUser,
      toggleUserStatus,
      deleteUser,
      saveUser,
      confirmResetPassword,
      confirmAction,
      closeModal,
      closeResetPasswordModal,
      closeConfirmationModal,
      formatDate
    };
  }
});
</script>

<style scoped>
.user-management {
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

.search input, .filter-role select, .filter-status select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}

.users-table {
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

.role-badge {
  display: inline-block;
  background-color: #e9ecef;
  color: #495057;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  margin-right: 5px;
}

.status-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.8em;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.status-badge.blocked {
  background-color: #f8d7da;
  color: #721c24;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 5px;
}

.btn {
  cursor: pointer;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
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
  font-size: 0.8em;
}

.btn-edit {
  background-color: #17a2b8;
  color: white;
}

.btn-reset-password {
  background-color: #6610f2;
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

.btn-unblock {
  background-color: #28a745;
  color: white;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}

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
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
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
  font-size: 1.5em;
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

.form-group input, .form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.roles-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
}

.role-checkbox {
  display: flex;
  align-items: center;
}

.role-checkbox input {
  margin-right: 5px;
  width: auto;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .actions {
    flex-wrap: wrap;
  }
  
  .roles-checkboxes {
    grid-template-columns: 1fr;
  }
}
</style>
