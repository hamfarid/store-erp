<template>
  <div class="user-permissions">
    <h1>صلاحيات المستخدمين</h1>
    
    <!-- بطاقات الإحصائيات -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-users"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ usersCount }}</div>
          <div class="stat-label">المستخدمين</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-user-shield"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ usersWithRolesCount }}</div>
          <div class="stat-label">المستخدمين بأدوار</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-users-cog"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ rolesCount }}</div>
          <div class="stat-label">الأدوار</div>
        </div>
      </div>
    </div>
    
    <!-- فلتر البحث -->
    <div class="search-filter">
      <input 
        type="text" 
        v-model="userSearchQuery" 
        placeholder="البحث عن مستخدم..." 
        class="search-input"
      />
      <select v-model="organizationFilter" class="filter-select">
        <option value="">جميع المؤسسات</option>
        <option v-for="org in organizations" :key="org.id" :value="org.id">
          {{ org.name }}
        </option>
      </select>
      <select v-model="roleFilter" class="filter-select">
        <option value="">جميع الأدوار</option>
        <option v-for="role in roles" :key="role.id" :value="role.id">
          {{ role.name }}
        </option>
      </select>
    </div>
    
    <!-- جدول المستخدمين -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>اسم المستخدم</th>
            <th>البريد الإلكتروني</th>
            <th>المؤسسة</th>
            <th>الأدوار</th>
            <th>الإجراءات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ getOrganizationName(user.organization_id) }}</td>
            <td>
              <div class="role-tags">
                <span 
                  v-for="role in user.roles" 
                  :key="role.id" 
                  class="role-tag"
                  :class="{ 'system-role': role.is_system_role }"
                >
                  {{ role.name }}
                </span>
                <span v-if="!user.roles || user.roles.length === 0" class="no-roles">
                  لا توجد أدوار
                </span>
              </div>
            </td>
            <td class="actions">
              <button class="btn-icon" @click="manageUserRoles(user)">
                <i class="fas fa-users-cog"></i>
              </button>
              <button class="btn-icon" @click="viewUserPermissions(user)">
                <i class="fas fa-key"></i>
              </button>
              <button class="btn-icon" @click="copyUserRoles(user)">
                <i class="fas fa-copy"></i>
              </button>
            </td>
          </tr>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="5" class="no-data">لا يوجد مستخدمين مطابقين للبحث</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- التنقل بين الصفحات -->
    <div class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="currentPage--"
        class="pagination-btn"
      >
        السابق
      </button>
      <span class="pagination-info">
        الصفحة {{ currentPage }} من {{ totalPages }}
      </span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="currentPage++"
        class="pagination-btn"
      >
        التالي
      </button>
    </div>
    
    <!-- نوافذ الحوار -->
    
    <!-- نافذة إدارة أدوار المستخدم -->
    <modal v-if="showUserRolesModal" @close="showUserRolesModal = false" size="large">
      <template #header>
        <h3>إدارة أدوار المستخدم: {{ selectedUser ? selectedUser.full_name : '' }}</h3>
      </template>
      <template #body>
        <div class="user-roles-manager">
          <div class="search-filter">
            <input 
              type="text" 
              v-model="userRoleSearchQuery" 
              placeholder="البحث عن دور..." 
              class="search-input"
            />
            <select v-model="userRoleOrgFilter" class="filter-select">
              <option value="">جميع المؤسسات</option>
              <option v-for="org in organizations" :key="org.id" :value="org.id">
                {{ org.name }}
              </option>
            </select>
          </div>
          
          <div class="roles-grid">
            <div 
              v-for="role in filteredUserRoles" 
              :key="role.id" 
              class="role-item"
              :class="{ 
                'assigned': isRoleAssigned(role.id),
                'system-role': role.is_system_role
              }"
              @click="toggleRole(role.id)"
            >
              <div class="role-checkbox">
                <input 
                  type="checkbox" 
                  :checked="isRoleAssigned(role.id)" 
                  @click.stop
                />
              </div>
              <div class="role-info">
                <div class="role-name">{{ role.name }}</div>
                <div class="role-details">
                  <span class="organization">
                    {{ role.organization_id ? getOrganizationName(role.organization_id) : 'عام' }}
                  </span>
                  <span class="role-type">
                    {{ role.is_system_role ? 'نظام' : 'مخصص' }}
                  </span>
                </div>
              </div>
            </div>
            <div v-if="filteredUserRoles.length === 0" class="no-data">
              لا توجد أدوار مطابقة للبحث
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <button class="btn-secondary" @click="showUserRolesModal = false">إغلاق</button>
        <button class="btn-primary" @click="saveUserRoles">حفظ التغييرات</button>
      </template>
    </modal>
    
    <!-- نافذة عرض صلاحيات المستخدم -->
    <modal v-if="showUserPermissionsModal" @close="showUserPermissionsModal = false" size="large">
      <template #header>
        <h3>صلاحيات المستخدم: {{ selectedUser ? selectedUser.full_name : '' }}</h3>
      </template>
      <template #body>
        <div class="user-permissions-viewer">
          <div class="search-filter">
            <input 
              type="text" 
              v-model="userPermissionSearchQuery" 
              placeholder="البحث عن صلاحية..." 
              class="search-input"
            />
            <select v-model="userPermissionResourceFilter" class="filter-select">
              <option value="">جميع أنواع الموارد</option>
              <option v-for="type in resourceTypes" :key="type" :value="type">
                {{ type }}
              </option>
            </select>
            <select v-model="userPermissionActionFilter" class="filter-select">
              <option value="">جميع الإجراءات</option>
              <option v-for="action in actionTypes" :key="action" :value="action">
                {{ getActionLabel(action) }}
              </option>
            </select>
          </div>
          
          <div class="permissions-list">
            <table class="data-table">
              <thead>
                <tr>
                  <th>الصلاحية</th>
                  <th>نوع المورد</th>
                  <th>الإجراء</th>
                  <th>الدور</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(perm, index) in filteredUserPermissions" :key="index">
                  <td>{{ perm.name }}</td>
                  <td>{{ perm.resource_type }}</td>
                  <td>
                    <span :class="['action-type', perm.action]">
                      {{ getActionLabel(perm.action) }}
                    </span>
                  </td>
                  <td>{{ perm.role_name }}</td>
                </tr>
                <tr v-if="filteredUserPermissions.length === 0">
                  <td colspan="4" class="no-data">لا توجد صلاحيات مطابقة للبحث</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
      <template #footer>
        <button class="btn-primary" @click="showUserPermissionsModal = false">إغلاق</button>
      </template>
    </modal>
    
    <!-- نافذة نسخ صلاحيات مستخدم -->
    <modal v-if="showCopyUserRolesModal" @close="showCopyUserRolesModal = false">
      <template #header>
        <h3>نسخ صلاحيات مستخدم</h3>
      </template>
      <template #body>
        <form @submit.prevent="copyUserRolesToUser" class="form">
          <div class="form-group">
            <label for="sourceUserSelect">المستخدم المصدر*</label>
            <select 
              id="sourceUserSelect" 
              v-model="copyRolesForm.source_user_id" 
              required 
              class="form-control"
              :disabled="true"
            >
              <option value="">اختر مستخدم مصدر</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.full_name }} ({{ user.email }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="targetUserSelect">المستخدم الهدف*</label>
            <select 
              id="targetUserSelect" 
              v-model="copyRolesForm.target_user_id" 
              required 
              class="form-control"
              :disabled="!copyRolesForm.source_user_id"
            >
              <option value="">اختر مستخدم هدف</option>
              <option 
                v-for="user in users.filter(u => u.id !== copyRolesForm.source_user_id)" 
                :key="user.id" 
                :value="user.id"
              >
                {{ user.full_name }} ({{ user.email }})
              </option>
            </select>
          </div>
          <div class="form-group checkbox-group">
            <input 
              type="checkbox" 
              id="replaceExisting" 
              v-model="copyRolesForm.replace_existing"
            />
            <label for="replaceExisting">استبدال الصلاحيات الحالية</label>
          </div>
          <div v-if="copyRolesForm.source_user_id" class="source-roles-preview">
            <h4>أدوار المستخدم المصدر:</h4>
            <div class="role-tags">
              <span 
                v-for="role in getSourceUserRoles()" 
                :key="role.id" 
                class="role-tag"
                :class="{ 'system-role': role.is_system_role }"
              >
                {{ role.name }}
              </span>
              <span v-if="!getSourceUserRoles().length" class="no-roles">
                لا توجد أدوار
              </span>
            </div>
          </div>
        </form>
      </template>
      <template #footer>
        <button class="btn-secondary" @click="showCopyUserRolesModal = false">إلغاء</button>
        <button 
          class="btn-primary" 
          @click="copyUserRolesToUser"
          :disabled="!copyRolesForm.source_user_id || !copyRolesForm.target_user_id"
        >
          نسخ الصلاحيات
        </button>
      </template>
    </modal>
  </div>
</template>

<script>
/**
 * @component UserPermissions
 * @description مكون إدارة صلاحيات المستخدمين
 * 
 * يوفر هذا المكون واجهة لعرض وإدارة صلاحيات المستخدمين، مع إمكانية تعيين الأدوار
 * ونسخ الصلاحيات بين المستخدمين.
 * 
 * @author فريق Scan AI
 * @date 30 مايو 2025
 */
import { ref, computed, onMounted, watch } from 'vue';
import Modal from '@/components/common/Modal.vue';
import { useToast } from '@/composables/useToast';
import { usePermissionService } from '@/composables/usePermissionService';
import { useUserService } from '@/composables/useUserService';
import { useOrganizationService } from '@/composables/useOrganizationService';

export default {
  name: 'UserPermissions',
  
  components: {
    Modal
  },
  
  setup() {
    // الخدمات
    const { toast } = useToast();
    const permissionService = usePermissionService();
    const userService = useUserService();
    const organizationService = useOrganizationService();
    
    // حالة المكون
    const isLoading = ref(false);
    
    // بيانات المستخدمين والأدوار والمؤسسات
    const users = ref([]);
    const roles = ref([]);
    const organizations = ref([]);
    
    // إحصائيات
    const usersCount = ref(0);
    const usersWithRolesCount = ref(0);
    const rolesCount = ref(0);
    
    // فلاتر البحث
    const userSearchQuery = ref('');
    const organizationFilter = ref('');
    const roleFilter = ref('');
    
    // التنقل بين الصفحات
    const currentPage = ref(1);
    const itemsPerPage = 10;
    
    // نوافذ الحوار
    const showUserRolesModal = ref(false);
    const showUserPermissionsModal = ref(false);
    const showCopyUserRolesModal = ref(false);
    
    // نماذج البيانات
    const copyRolesForm = ref({
      source_user_id: '',
      target_user_id: '',
      replace_existing: true
    });
    
    // البيانات المحددة
    const selectedUser = ref(null);
    
    // بيانات إدارة أدوار المستخدم
    const userRoleSearchQuery = ref('');
    const userRoleOrgFilter = ref('');
    const selectedUserRoles = ref([]);
    
    // بيانات عرض صلاحيات المستخدم
    const userPermissionSearchQuery = ref('');
    const userPermissionResourceFilter = ref('');
    const userPermissionActionFilter = ref('');
    const userPermissions = ref([]);
    
    // القيم الثابتة
    const resourceTypes = [
      'user', 'role', 'permission', 'organization', 'branch', 'product', 
      'invoice', 'report', 'dashboard', 'setting', 'ai_agent', 'module'
    ];
    
    const actionTypes = [
      'create', 'read', 'update', 'delete', 'view', 'admin', 'approve'
    ];
    
    // الدوال المحسوبة
    
    /**
     * المستخدمين المصفاة حسب البحث والفلاتر
     */
    const filteredUsers = computed(() => {
      let result = [...users.value];
      
      // تطبيق فلتر البحث
      if (userSearchQuery.value) {
        const query = userSearchQuery.value.toLowerCase();
        result = result.filter(user => 
          user.full_name.toLowerCase().includes(query) || 
          user.email.toLowerCase().includes(query)
        );
      }
      
      // تطبيق فلتر المؤسسة
      if (organizationFilter.value) {
        result = result.filter(user => user.organization_id === organizationFilter.value);
      }
      
      // تطبيق فلتر الدور
      if (roleFilter.value) {
        result = result.filter(user => 
          user.roles && user.roles.some(role => role.id === roleFilter.value)
        );
      }
      
      // تطبيق التنقل بين الصفحات
      const startIndex = (currentPage.value - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      
      return result.slice(startIndex, endIndex);
    });
    
    /**
     * إجمالي صفحات المستخدمين
     */
    const totalPages = computed(() => {
      let result = [...users.value];
      
      // تطبيق فلتر البحث
      if (userSearchQuery.value) {
        const query = userSearchQuery.value.toLowerCase();
        result = result.filter(user => 
          user.full_name.toLowerCase().includes(query) || 
          user.email.toLowerCase().includes(query)
        );
      }
      
      // تطبيق فلتر المؤسسة
      if (organizationFilter.value) {
        result = result.filter(user => user.organization_id === organizationFilter.value);
      }
      
      // تطبيق فلتر الدور
      if (roleFilter.value) {
        result = result.filter(user => 
          user.roles && user.roles.some(role => role.id === roleFilter.value)
        );
      }
      
      return Math.ceil(result.length / itemsPerPage);
    });
    
    /**
     * أدوار المستخدم المصفاة
     */
    const filteredUserRoles = computed(() => {
      let result = [...roles.value];
      
      // تطبيق فلتر البحث
      if (userRoleSearchQuery.value) {
        const query = userRoleSearchQuery.value.toLowerCase();
        result = result.filter(role => 
          role.name.toLowerCase().includes(query) || 
          (role.description && role.description.toLowerCase().includes(query))
        );
      }
      
      // تطبيق فلتر المؤسسة
      if (userRoleOrgFilter.value) {
        result = result.filter(role => role.organization_id === userRoleOrgFilter.value);
      }
      
      return result;
    });
    
    /**
     * صلاحيات المستخدم المصفاة
     */
    const filteredUserPermissions = computed(() => {
      let result = [...userPermissions.value];
      
      // تطبيق فلتر البحث
      if (userPermissionSearchQuery.value) {
        const query = userPermissionSearchQuery.value.toLowerCase();
        result = result.filter(permission => 
          permission.name.toLowerCase().includes(query) || 
          (permission.description && permission.description.toLowerCase().includes(query))
        );
      }
      
      // تطبيق فلتر نوع المورد
      if (userPermissionResourceFilter.value) {
        result = result.filter(permission => permission.resource_type === userPermissionResourceFilter.value);
      }
      
      // تطبيق فلتر الإجراء
      if (userPermissionActionFilter.value) {
        result = result.filter(permission => permission.action === userPermissionActionFilter.value);
      }
      
      return result;
    });
    
    // دوال المساعدة
    
    /**
     * الحصول على اسم المؤسسة
     * @param {string} organizationId - معرف المؤسسة
     * @returns {string} - اسم المؤسسة
     */
    const getOrganizationName = (organizationId) => {
      if (!organizationId) return 'عام';
      
      const organization = organizations.value.find(org => org.id === organizationId);
      return organization ? organization.name : 'غير معروف';
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
     * التحقق مما إذا كان الدور معين للمستخدم
     * @param {string} roleId - معرف الدور
     * @returns {boolean} - ما إذا كان الدور معين للمستخدم
     */
    const isRoleAssigned = (roleId) => {
      return selectedUserRoles.value.includes(roleId);
    };
    
    /**
     * تبديل حالة الدور للمستخدم
     * @param {string} roleId - معرف الدور
     */
    const toggleRole = (roleId) => {
      const index = selectedUserRoles.value.indexOf(roleId);
      if (index === -1) {
        selectedUserRoles.value.push(roleId);
      } else {
        selectedUserRoles.value.splice(index, 1);
      }
    };
    
    /**
     * الحصول على أدوار المستخدم المصدر
     * @returns {Array} - أدوار المستخدم المصدر
     */
    const getSourceUserRoles = () => {
      if (!copyRolesForm.value.source_user_id) {
        return [];
      }
      
      const user = users.value.find(u => u.id === copyRolesForm.value.source_user_id);
      return user && user.roles ? user.roles : [];
    };
    
    // دوال التحميل
    
    /**
     * تحميل المستخدمين
     */
    const loadUsers = async () => {
      try {
        isLoading.value = true;
        const response = await userService.getUsers();
        users.value = response.data;
        usersCount.value = users.value.length;
        usersWithRolesCount.value = users.value.filter(user => user.roles && user.roles.length > 0).length;
      } catch (error) {
        toast.error('حدث خطأ أثناء تحميل المستخدمين');
        console.error('Error loading users:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * تحميل الأدوار
     */
    const loadRoles = async () => {
      try {
        isLoading.value = true;
        const response = await permissionService.getRoles();
        roles.value = response.data;
        rolesCount.value = roles.value.length;
      } catch (error) {
        toast.error('حدث خطأ أثناء تحميل الأدوار');
        console.error('Error loading roles:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * تحميل المؤسسات
     */
    const loadOrganizations = async () => {
      try {
        isLoading.value = true;
        const response = await organizationService.getOrganizations();
        organizations.value = response.data;
      } catch (error) {
        toast.error('حدث خطأ أثناء تحميل المؤسسات');
        console.error('Error loading organizations:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * تحميل صلاحيات المستخدم
     * @param {string} userId - معرف المستخدم
     */
    const loadUserPermissions = async (userId) => {
      try {
        isLoading.value = true;
        const response = await permissionService.getUserPermissions(userId);
        userPermissions.value = response.data;
      } catch (error) {
        toast.error('حدث خطأ أثناء تحميل صلاحيات المستخدم');
        console.error('Error loading user permissions:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    // دوال الإجراءات
    
    /**
     * إدارة أدوار المستخدم
     * @param {Object} user - المستخدم المراد إدارة أدواره
     */
    const manageUserRoles = (user) => {
      selectedUser.value = user;
      selectedUserRoles.value = user.roles ? user.roles.map(r => r.id) : [];
      showUserRolesModal.value = true;
    };
    
    /**
     * حفظ أدوار المستخدم
     */
    const saveUserRoles = async () => {
      try {
        isLoading.value = true;
        
        // الحصول على الأدوار الحالية للمستخدم
        const currentRoles = selectedUser.value.roles 
          ? selectedUser.value.roles.map(r => r.id) 
          : [];
        
        // تحديد الأدوار المضافة والمحذوفة
        const addedRoles = selectedUserRoles.value.filter(
          id => !currentRoles.includes(id)
        );
        
        const removedRoles = currentRoles.filter(
          id => !selectedUserRoles.value.includes(id)
        );
        
        // تطبيق التغييرات
        for (const roleId of addedRoles) {
          await permissionService.assignRoleToUser(selectedUser.value.id, roleId);
        }
        
        for (const roleId of removedRoles) {
          await permissionService.removeRoleFromUser(selectedUser.value.id, roleId);
        }
        
        toast.success('تم حفظ أدوار المستخدم بنجاح');
        
        // إعادة تحميل المستخدمين
        await loadUsers();
        
        // إغلاق النافذة
        showUserRolesModal.value = false;
      } catch (error) {
        toast.error('حدث خطأ أثناء حفظ أدوار المستخدم');
        console.error('Error saving user roles:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * عرض صلاحيات المستخدم
     * @param {Object} user - المستخدم المراد عرض صلاحياته
     */
    const viewUserPermissions = async (user) => {
      selectedUser.value = user;
      await loadUserPermissions(user.id);
      showUserPermissionsModal.value = true;
    };
    
    /**
     * نسخ صلاحيات مستخدم
     * @param {Object} user - المستخدم المراد نسخ صلاحياته
     */
    const copyUserRoles = (user) => {
      copyRolesForm.value.source_user_id = user.id;
      showCopyUserRolesModal.value = true;
    };
    
    /**
     * نسخ صلاحيات مستخدم إلى مستخدم آخر
     */
    const copyUserRolesToUser = async () => {
      try {
        isLoading.value = true;
        
        // التحقق من صحة البيانات
        if (!copyRolesForm.value.source_user_id) {
          toast.error('يرجى اختيار المستخدم المصدر');
          return;
        }
        
        if (!copyRolesForm.value.target_user_id) {
          toast.error('يرجى اختيار المستخدم الهدف');
          return;
        }
        
        // نسخ الصلاحيات
        await permissionService.copyUserRoles(
          copyRolesForm.value.source_user_id,
          copyRolesForm.value.target_user_id,
          copyRolesForm.value.replace_existing
        );
        
        toast.success('تم نسخ صلاحيات المستخدم بنجاح');
        
        // إعادة تحميل المستخدمين
        await loadUsers();
        
        // إغلاق النافذة
        showCopyUserRolesModal.value = false;
        copyRolesForm.value = {
          source_user_id: '',
          target_user_id: '',
          replace_existing: true
        };
      } catch (error) {
        toast.error('حدث خطأ أثناء نسخ صلاحيات المستخدم');
        console.error('Error copying user roles:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    // دورة حياة المكون
    
    onMounted(async () => {
      // تحميل البيانات
      await Promise.all([
        loadUsers(),
        loadRoles(),
        loadOrganizations()
      ]);
    });
    
    // مراقبة التغييرات
    
    watch(userSearchQuery, () => {
      currentPage.value = 1;
    });
    
    watch(organizationFilter, () => {
      currentPage.value = 1;
    });
    
    watch(roleFilter, () => {
      currentPage.value = 1;
    });
    
    return {
      // الحالة
      isLoading,
      
      // البيانات
      users,
      roles,
      organizations,
      
      // الإحصائيات
      usersCount,
      usersWithRolesCount,
      rolesCount,
      
      // الفلاتر
      userSearchQuery,
      organizationFilter,
      roleFilter,
      
      // التنقل بين الصفحات
      currentPage,
      
      // النوافذ
      showUserRolesModal,
      showUserPermissionsModal,
      showCopyUserRolesModal,
      
      // النماذج
      copyRolesForm,
      
      // البيانات المحددة
      selectedUser,
      
      // بيانات إدارة أدوار المستخدم
      userRoleSearchQuery,
      userRoleOrgFilter,
      selectedUserRoles,
      
      // بيانات عرض صلاحيات المستخدم
      userPermissionSearchQuery,
      userPermissionResourceFilter,
      userPermissionActionFilter,
      userPermissions,
      
      // القيم الثابتة
      resourceTypes,
      actionTypes,
      
      // الدوال المحسوبة
      filteredUsers,
      totalPages,
      filteredUserRoles,
      filteredUserPermissions,
      
      // دوال المساعدة
      getOrganizationName,
      getActionLabel,
      isRoleAssigned,
      toggleRole,
      getSourceUserRoles,
      
      // دوال الإجراءات
      manageUserRoles,
      saveUserRoles,
      viewUserPermissions,
      copyUserRoles,
      copyUserRolesToUser
    };
  }
};
</script>

<style scoped>
.user-permissions {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

/* بطاقات الإحصائيات */
.stats-cards {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.stat-card {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin: 0 10px;
  display: flex;
  align-items: center;
}

.stat-card:first-child {
  margin-right: 0;
}

.stat-card:last-child {
  margin-left: 0;
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

/* فلتر البحث */
.search-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.filter-select {
  min-width: 150px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* جدول البيانات */
.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
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

.data-table .actions {
  white-space: nowrap;
  text-align: center;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #666;
}

/* التنقل بين الصفحات */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-btn {
  padding: 8px 15px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  margin: 0 15px;
  color: #666;
}

/* الأزرار */
.btn-primary {
  background-color: #4a6cf7;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #3a5bd9;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-secondary:hover {
  background-color: #e5e5e5;
}

.btn-icon {
  background-color: transparent;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 5px;
  font-size: 1rem;
  transition: color 0.3s;
}

.btn-icon:hover {
  color: #4a6cf7;
}

/* العلامات والأيقونات */
.role-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.role-tag {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  background-color: #e3f2fd;
  color: #1976d2;
}

.role-tag.system-role {
  background-color: #fce4ec;
  color: #c2185b;
}

.no-roles {
  color: #999;
  font-style: italic;
}

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

/* شبكة الأدوار */
.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
  margin-top: 15px;
}

.role-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.role-item:hover {
  background-color: #f5f5f5;
}

.role-item.assigned {
  background-color: #e3f2fd;
  border-color: #1976d2;
}

.role-checkbox {
  margin-left: 10px;
}

.role-info {
  flex: 1;
}

.role-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.role-details {
  display: flex;
  gap: 10px;
  font-size: 0.8rem;
}

.organization,
.role-type {
  color: #666;
}

.role-item.system-role {
  border-color: #c2185b;
}

/* النماذج */
.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
}

.checkbox-group input {
  margin-left: 5px;
}

/* معاينة أدوار المستخدم المصدر */
.source-roles-preview {
  margin-top: 15px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.source-roles-preview h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #666;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .stats-cards {
    flex-direction: column;
  }
  
  .stat-card {
    margin: 0 0 10px 0;
  }
  
  .search-filter {
    flex-direction: column;
  }
  
  .search-input,
  .filter-select {
    width: 100%;
  }
}
</style>
