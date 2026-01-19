<template>
  <div class="role-management">
    <h1>إدارة الأدوار والصلاحيات</h1>
    
    <!-- بطاقات الإحصائيات -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-users-cog"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ rolesCount }}</div>
          <div class="stat-label">الأدوار</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-key"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ permissionsCount }}</div>
          <div class="stat-label">الصلاحيات</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-user-shield"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ usersWithRolesCount }}</div>
          <div class="stat-label">المستخدمين بأدوار</div>
        </div>
      </div>
    </div>
    
    <!-- علامات التبويب -->
    <div class="tabs">
      <div 
        :class="['tab', { active: activeTab === 'roles' }]" 
        @click="activeTab = 'roles'"
      >
        الأدوار
      </div>
      <div 
        :class="['tab', { active: activeTab === 'permissions' }]" 
        @click="activeTab = 'permissions'"
      >
        الصلاحيات
      </div>
      <div 
        :class="['tab', { active: activeTab === 'userRoles' }]" 
        @click="activeTab = 'userRoles'"
      >
        أدوار المستخدمين
      </div>
    </div>
    
    <!-- محتوى علامات التبويب -->
    <div class="tab-content">
      <!-- قسم الأدوار -->
      <div v-if="activeTab === 'roles'" class="roles-section">
        <div class="section-header">
          <h2>إدارة الأدوار</h2>
          <button class="btn-primary" @click="showAddRoleModal = true">
            <i class="fas fa-plus"></i> إضافة دور جديد
          </button>
        </div>
        
        <!-- فلتر البحث -->
        <div class="search-filter">
          <input 
            type="text" 
            v-model="roleSearchQuery" 
            placeholder="البحث عن دور..." 
            class="search-input"
          />
          <select v-model="organizationFilter" class="filter-select">
            <option value="">جميع المؤسسات</option>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
          <div class="filter-checkbox">
            <input type="checkbox" id="systemRolesFilter" v-model="showSystemRoles" />
            <label for="systemRolesFilter">عرض أدوار النظام</label>
          </div>
        </div>
        
        <!-- جدول الأدوار -->
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>الاسم</th>
                <th>الوصف</th>
                <th>المؤسسة</th>
                <th>نوع الدور</th>
                <th>عدد الصلاحيات</th>
                <th>عدد المستخدمين</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="role in filteredRoles" :key="role.id">
                <td>{{ role.name }}</td>
                <td>{{ role.description }}</td>
                <td>{{ getOrganizationName(role.organization_id) }}</td>
                <td>
                  <span :class="['role-type', role.is_system_role ? 'system' : 'custom']">
                    {{ role.is_system_role ? 'نظام' : 'مخصص' }}
                  </span>
                </td>
                <td>{{ role.permissions ? role.permissions.length : 0 }}</td>
                <td>{{ role.users ? role.users.length : 0 }}</td>
                <td class="actions">
                  <button class="btn-icon" @click="editRole(role)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn-icon" @click="viewRolePermissions(role)">
                    <i class="fas fa-key"></i>
                  </button>
                  <button 
                    class="btn-icon" 
                    @click="deleteRole(role)"
                    :disabled="role.is_system_role || role.users.length > 0"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredRoles.length === 0">
                <td colspan="7" class="no-data">لا توجد أدوار مطابقة للبحث</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- التنقل بين الصفحات -->
        <div class="pagination">
          <button 
            :disabled="currentRolePage === 1" 
            @click="currentRolePage--"
            class="pagination-btn"
          >
            السابق
          </button>
          <span class="pagination-info">
            الصفحة {{ currentRolePage }} من {{ totalRolePages }}
          </span>
          <button 
            :disabled="currentRolePage === totalRolePages" 
            @click="currentRolePage++"
            class="pagination-btn"
          >
            التالي
          </button>
        </div>
      </div>
      
      <!-- قسم الصلاحيات -->
      <div v-if="activeTab === 'permissions'" class="permissions-section">
        <div class="section-header">
          <h2>إدارة الصلاحيات</h2>
          <button class="btn-primary" @click="showAddPermissionModal = true">
            <i class="fas fa-plus"></i> إضافة صلاحية جديدة
          </button>
        </div>
        
        <!-- فلتر البحث -->
        <div class="search-filter">
          <input 
            type="text" 
            v-model="permissionSearchQuery" 
            placeholder="البحث عن صلاحية..." 
            class="search-input"
          />
          <select v-model="resourceTypeFilter" class="filter-select">
            <option value="">جميع أنواع الموارد</option>
            <option v-for="type in resourceTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
          <select v-model="actionFilter" class="filter-select">
            <option value="">جميع الإجراءات</option>
            <option v-for="action in actionTypes" :key="action" :value="action">
              {{ getActionLabel(action) }}
            </option>
          </select>
        </div>
        
        <!-- جدول الصلاحيات -->
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>الاسم</th>
                <th>الوصف</th>
                <th>نوع المورد</th>
                <th>الإجراء</th>
                <th>عدد الأدوار</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="permission in filteredPermissions" :key="permission.id">
                <td>{{ permission.name }}</td>
                <td>{{ permission.description }}</td>
                <td>{{ permission.resource_type }}</td>
                <td>
                  <span :class="['action-type', permission.action]">
                    {{ getActionLabel(permission.action) }}
                  </span>
                </td>
                <td>{{ permission.roles ? permission.roles.length : 0 }}</td>
                <td class="actions">
                  <button class="btn-icon" @click="editPermission(permission)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn-icon" @click="viewPermissionRoles(permission)">
                    <i class="fas fa-users-cog"></i>
                  </button>
                  <button 
                    class="btn-icon" 
                    @click="deletePermission(permission)"
                    :disabled="permission.roles && permission.roles.length > 0"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredPermissions.length === 0">
                <td colspan="6" class="no-data">لا توجد صلاحيات مطابقة للبحث</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- التنقل بين الصفحات -->
        <div class="pagination">
          <button 
            :disabled="currentPermissionPage === 1" 
            @click="currentPermissionPage--"
            class="pagination-btn"
          >
            السابق
          </button>
          <span class="pagination-info">
            الصفحة {{ currentPermissionPage }} من {{ totalPermissionPages }}
          </span>
          <button 
            :disabled="currentPermissionPage === totalPermissionPages" 
            @click="currentPermissionPage++"
            class="pagination-btn"
          >
            التالي
          </button>
        </div>
      </div>
      
      <!-- قسم أدوار المستخدمين -->
      <div v-if="activeTab === 'userRoles'" class="user-roles-section">
        <div class="section-header">
          <h2>إدارة أدوار المستخدمين</h2>
          <div class="header-actions">
            <button class="btn-secondary" @click="showCopyUserRolesModal = true">
              <i class="fas fa-copy"></i> نسخ صلاحيات مستخدم
            </button>
            <button class="btn-primary" @click="showAssignRoleModal = true">
              <i class="fas fa-user-plus"></i> تعيين دور لمستخدم
            </button>
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
          <select v-model="userRoleFilter" class="filter-select">
            <option value="">جميع الأدوار</option>
            <option v-for="role in roles" :key="role.id" :value="role.id">
              {{ role.name }}
            </option>
          </select>
          <select v-model="organizationUserFilter" class="filter-select">
            <option value="">جميع المؤسسات</option>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>
        
        <!-- جدول المستخدمين وأدوارهم -->
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
            :disabled="currentUserPage === 1" 
            @click="currentUserPage--"
            class="pagination-btn"
          >
            السابق
          </button>
          <span class="pagination-info">
            الصفحة {{ currentUserPage }} من {{ totalUserPages }}
          </span>
          <button 
            :disabled="currentUserPage === totalUserPages" 
            @click="currentUserPage++"
            class="pagination-btn"
          >
            التالي
          </button>
        </div>
      </div>
    </div>
    
    <!-- نوافذ الحوار -->
    
    <!-- نافذة إضافة/تعديل دور -->
    <modal v-if="showAddRoleModal || showEditRoleModal" @close="closeRoleModal">
      <template #header>
        <h3>{{ showEditRoleModal ? 'تعديل دور' : 'إضافة دور جديد' }}</h3>
      </template>
      <template #body>
        <form @submit.prevent="saveRole" class="form">
          <div class="form-group">
            <label for="roleName">اسم الدور*</label>
            <input 
              type="text" 
              id="roleName" 
              v-model="roleForm.name" 
              required 
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="roleDescription">وصف الدور</label>
            <textarea 
              id="roleDescription" 
              v-model="roleForm.description" 
              class="form-control"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="roleOrganization">المؤسسة</label>
            <select 
              id="roleOrganization" 
              v-model="roleForm.organization_id" 
              class="form-control"
            >
              <option value="">بدون مؤسسة (دور عام)</option>
              <option v-for="org in organizations" :key="org.id" :value="org.id">
                {{ org.name }}
              </option>
            </select>
          </div>
          <div class="form-group checkbox-group" v-if="isAdmin">
            <input 
              type="checkbox" 
              id="isSystemRole" 
              v-model="roleForm.is_system_role"
            />
            <label for="isSystemRole">دور نظام</label>
          </div>
        </form>
      </template>
      <template #footer>
        <button class="btn-secondary" @click="closeRoleModal">إلغاء</button>
        <button class="btn-primary" @click="saveRole">حفظ</button>
      </template>
    </modal>
    
    <!-- نافذة إضافة/تعديل صلاحية -->
    <modal v-if="showAddPermissionModal || showEditPermissionModal" @close="closePermissionModal">
      <template #header>
        <h3>{{ showEditPermissionModal ? 'تعديل صلاحية' : 'إضافة صلاحية جديدة' }}</h3>
      </template>
      <template #body>
        <form @submit.prevent="savePermission" class="form">
          <div class="form-group">
            <label for="permissionName">اسم الصلاحية*</label>
            <input 
              type="text" 
              id="permissionName" 
              v-model="permissionForm.name" 
              required 
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="permissionDescription">وصف الصلاحية</label>
            <textarea 
              id="permissionDescription" 
              v-model="permissionForm.description" 
              class="form-control"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="resourceType">نوع المورد*</label>
            <select 
              id="resourceType" 
              v-model="permissionForm.resource_type" 
              required 
              class="form-control"
            >
              <option value="">اختر نوع المورد</option>
              <option v-for="type in resourceTypes" :key="type" :value="type">
                {{ type }}
              </option>
              <option value="custom">مخصص</option>
            </select>
          </div>
          <div class="form-group" v-if="permissionForm.resource_type === 'custom'">
            <label for="customResourceType">نوع المورد المخصص*</label>
            <input 
              type="text" 
              id="customResourceType" 
              v-model="permissionForm.custom_resource_type" 
              required 
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="actionType">نوع الإجراء*</label>
            <select 
              id="actionType" 
              v-model="permissionForm.action" 
              required 
              class="form-control"
            >
              <option value="">اختر نوع الإجراء</option>
              <option v-for="action in actionTypes" :key="action" :value="action">
                {{ getActionLabel(action) }}
              </option>
            </select>
          </div>
        </form>
      </template>
      <template #footer>
        <button class="btn-secondary" @click="closePermissionModal">إلغاء</button>
        <button class="btn-primary" @click="savePermission">حفظ</button>
      </template>
    </modal>
    
    <!-- نافذة تعيين دور لمستخدم -->
    <modal v-if="showAssignRoleModal" @close="showAssignRoleModal = false">
      <template #header>
        <h3>تعيين دور لمستخدم</h3>
      </template>
      <template #body>
        <form @submit.prevent="assignRoleToUser" class="form">
          <div class="form-group">
            <label for="userSelect">المستخدم*</label>
            <select 
              id="userSelect" 
              v-model="assignRoleForm.user_id" 
              required 
              class="form-control"
            >
              <option value="">اختر مستخدم</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.full_name }} ({{ user.email }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="roleSelect">الدور*</label>
            <select 
              id="roleSelect" 
              v-model="assignRoleForm.role_id" 
              required 
              class="form-control"
            >
              <option value="">اختر دور</option>
              <option v-for="role in filteredRolesForAssign" :key="role.id" :value="role.id">
                {{ role.name }}
              </option>
            </select>
          </div>
        </form>
      </template>
      <template #footer>
        <button class="btn-secondary" @click="showAssignRoleModal = false">إلغاء</button>
        <button class="btn-primary" @click="assignRoleToUser">تعيين</button>
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
    
    <!-- نافذة إدارة صلاحيات الدور -->
    <modal v-if="showRolePermissionsModal" @close="showRolePermissionsModal = false" size="large">
      <template #header>
        <h3>إدارة صلاحيات الدور: {{ selectedRole ? selectedRole.name : '' }}</h3>
      </template>
      <template #body>
        <div class="role-permissions-manager">
          <div class="search-filter">
            <input 
              type="text" 
              v-model="rolePermissionSearchQuery" 
              placeholder="البحث عن صلاحية..." 
              class="search-input"
            />
            <select v-model="rolePermissionResourceFilter" class="filter-select">
              <option value="">جميع أنواع الموارد</option>
              <option v-for="type in resourceTypes" :key="type" :value="type">
                {{ type }}
              </option>
            </select>
          </div>
          
          <div class="permissions-grid">
            <div 
              v-for="permission in filteredRolePermissions" 
              :key="permission.id" 
              class="permission-item"
              :class="{ 'assigned': isPermissionAssigned(permission.id) }"
              @click="togglePermission(permission.id)"
            >
              <div class="permission-checkbox">
                <input 
                  type="checkbox" 
                  :checked="isPermissionAssigned(permission.id)" 
                  @click.stop
                />
              </div>
              <div class="permission-info">
                <div class="permission-name">{{ permission.name }}</div>
                <div class="permission-details">
                  <span class="resource-type">{{ permission.resource_type }}</span>
                  <span :class="['action-type', permission.action]">
                    {{ getActionLabel(permission.action) }}
                  </span>
                </div>
              </div>
            </div>
            <div v-if="filteredRolePermissions.length === 0" class="no-data">
              لا توجد صلاحيات مطابقة للبحث
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <button class="btn-secondary" @click="showRolePermissionsModal = false">إغلاق</button>
        <button class="btn-primary" @click="saveRolePermissions">حفظ التغييرات</button>
      </template>
    </modal>
    
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
    
    <!-- نافذة التأكيد -->
    <modal v-if="showConfirmModal" @close="showConfirmModal = false" size="small">
      <template #header>
        <h3>{{ confirmTitle }}</h3>
      </template>
      <template #body>
        <p>{{ confirmMessage }}</p>
      </template>
      <template #footer>
        <button class="btn-secondary" @click="showConfirmModal = false">إلغاء</button>
        <button class="btn-danger" @click="confirmAction">تأكيد</button>
      </template>
    </modal>
  </div>
</template>

<script>
/**
 * @component RoleManagement
 * @description مكون إدارة الأدوار والصلاحيات في النظام
 * 
 * يوفر هذا المكون واجهة متكاملة لإدارة الأدوار والصلاحيات وتعيينها للمستخدمين،
 * مع دعم نسخ صلاحيات مستخدم لآخر وتخصيص الصلاحيات حسب المؤسسات والفروع.
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
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'RoleManagement',
  
  components: {
    Modal
  },
  
  setup() {
    // الخدمات
    const { toast } = useToast();
    const permissionService = usePermissionService();
    const userService = useUserService();
    const organizationService = useOrganizationService();
    const authStore = useAuthStore();
    
    // حالة المكون
    const activeTab = ref('roles');
    const isLoading = ref(false);
    
    // بيانات الأدوار والصلاحيات والمستخدمين
    const roles = ref([]);
    const permissions = ref([]);
    const users = ref([]);
    const organizations = ref([]);
    
    // إحصائيات
    const rolesCount = ref(0);
    const permissionsCount = ref(0);
    const usersWithRolesCount = ref(0);
    
    // فلاتر البحث
    const roleSearchQuery = ref('');
    const permissionSearchQuery = ref('');
    const userSearchQuery = ref('');
    const organizationFilter = ref('');
    const resourceTypeFilter = ref('');
    const actionFilter = ref('');
    const userRoleFilter = ref('');
    const organizationUserFilter = ref('');
    const showSystemRoles = ref(true);
    
    // التنقل بين الصفحات
    const currentRolePage = ref(1);
    const currentPermissionPage = ref(1);
    const currentUserPage = ref(1);
    const itemsPerPage = 10;
    
    // نوافذ الحوار
    const showAddRoleModal = ref(false);
    const showEditRoleModal = ref(false);
    const showAddPermissionModal = ref(false);
    const showEditPermissionModal = ref(false);
    const showAssignRoleModal = ref(false);
    const showCopyUserRolesModal = ref(false);
    const showRolePermissionsModal = ref(false);
    const showUserRolesModal = ref(false);
    const showUserPermissionsModal = ref(false);
    const showConfirmModal = ref(false);
    
    // نماذج البيانات
    const roleForm = ref({
      id: null,
      name: '',
      description: '',
      is_system_role: false,
      organization_id: ''
    });
    
    const permissionForm = ref({
      id: null,
      name: '',
      description: '',
      resource_type: '',
      custom_resource_type: '',
      action: ''
    });
    
    const assignRoleForm = ref({
      user_id: '',
      role_id: ''
    });
    
    const copyRolesForm = ref({
      source_user_id: '',
      target_user_id: '',
      replace_existing: true
    });
    
    // البيانات المحددة
    const selectedRole = ref(null);
    const selectedUser = ref(null);
    const selectedPermission = ref(null);
    
    // بيانات التأكيد
    const confirmTitle = ref('');
    const confirmMessage = ref('');
    const confirmAction = ref(() => {});
    
    // بيانات إدارة صلاحيات الدور
    const rolePermissionSearchQuery = ref('');
    const rolePermissionResourceFilter = ref('');
    const selectedRolePermissions = ref([]);
    
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
     * الأدوار المصفاة حسب البحث والفلاتر
     */
    const filteredRoles = computed(() => {
      let result = [...roles.value];
      
      // تطبيق فلتر البحث
      if (roleSearchQuery.value) {
        const query = roleSearchQuery.value.toLowerCase();
        result = result.filter(role => 
          role.name.toLowerCase().includes(query) || 
          (role.description && role.description.toLowerCase().includes(query))
        );
      }
      
      // تطبيق فلتر المؤسسة
      if (organizationFilter.value) {
        result = result.filter(role => role.organization_id === organizationFilter.value);
      }
      
      // تطبيق فلتر أدوار النظام
      if (!showSystemRoles.value) {
        result = result.filter(role => !role.is_system_role);
      }
      
      // تطبيق التنقل بين الصفحات
      const startIndex = (currentRolePage.value - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      
      return result.slice(startIndex, endIndex);
    });
    
    /**
     * إجمالي صفحات الأدوار
     */
    const totalRolePages = computed(() => {
      let result = [...roles.value];
      
      // تطبيق فلتر البحث
      if (roleSearchQuery.value) {
        const query = roleSearchQuery.value.toLowerCase();
        result = result.filter(role => 
          role.name.toLowerCase().includes(query) || 
          (role.description && role.description.toLowerCase().includes(query))
        );
      }
      
      // تطبيق فلتر المؤسسة
      if (organizationFilter.value) {
        result = result.filter(role => role.organization_id === organizationFilter.value);
      }
      
      // تطبيق فلتر أدوار النظام
      if (!showSystemRoles.value) {
        result = result.filter(role => !role.is_system_role);
      }
      
      return Math.ceil(result.length / itemsPerPage);
    });
    
    /**
     * الصلاحيات المصفاة حسب البحث والفلاتر
     */
    const filteredPermissions = computed(() => {
      let result = [...permissions.value];
      
      // تطبيق فلتر البحث
      if (permissionSearchQuery.value) {
        const query = permissionSearchQuery.value.toLowerCase();
        result = result.filter(permission => 
          permission.name.toLowerCase().includes(query) || 
          (permission.description && permission.description.toLowerCase().includes(query))
        );
      }
      
      // تطبيق فلتر نوع المورد
      if (resourceTypeFilter.value) {
        result = result.filter(permission => permission.resource_type === resourceTypeFilter.value);
      }
      
      // تطبيق فلتر الإجراء
      if (actionFilter.value) {
        result = result.filter(permission => permission.action === actionFilter.value);
      }
      
      // تطبيق التنقل بين الصفحات
      const startIndex = (currentPermissionPage.value - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      
      return result.slice(startIndex, endIndex);
    });
    
    /**
     * إجمالي صفحات الصلاحيات
     */
    const totalPermissionPages = computed(() => {
      let result = [...permissions.value];
      
      // تطبيق فلتر البحث
      if (permissionSearchQuery.value) {
        const query = permissionSearchQuery.value.toLowerCase();
        result = result.filter(permission => 
          permission.name.toLowerCase().includes(query) || 
          (permission.description && permission.description.toLowerCase().includes(query))
        );
      }
      
      // تطبيق فلتر نوع المورد
      if (resourceTypeFilter.value) {
        result = result.filter(permission => permission.resource_type === resourceTypeFilter.value);
      }
      
      // تطبيق فلتر الإجراء
      if (actionFilter.value) {
        result = result.filter(permission => permission.action === actionFilter.value);
      }
      
      return Math.ceil(result.length / itemsPerPage);
    });
    
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
      
      // تطبيق فلتر الدور
      if (userRoleFilter.value) {
        result = result.filter(user => 
          user.roles && user.roles.some(role => role.id === userRoleFilter.value)
        );
      }
      
      // تطبيق فلتر المؤسسة
      if (organizationUserFilter.value) {
        result = result.filter(user => user.organization_id === organizationUserFilter.value);
      }
      
      // تطبيق التنقل بين الصفحات
      const startIndex = (currentUserPage.value - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      
      return result.slice(startIndex, endIndex);
    });
    
    /**
     * إجمالي صفحات المستخدمين
     */
    const totalUserPages = computed(() => {
      let result = [...users.value];
      
      // تطبيق فلتر البحث
      if (userSearchQuery.value) {
        const query = userSearchQuery.value.toLowerCase();
        result = result.filter(user => 
          user.full_name.toLowerCase().includes(query) || 
          user.email.toLowerCase().includes(query)
        );
      }
      
      // تطبيق فلتر الدور
      if (userRoleFilter.value) {
        result = result.filter(user => 
          user.roles && user.roles.some(role => role.id === userRoleFilter.value)
        );
      }
      
      // تطبيق فلتر المؤسسة
      if (organizationUserFilter.value) {
        result = result.filter(user => user.organization_id === organizationUserFilter.value);
      }
      
      return Math.ceil(result.length / itemsPerPage);
    });
    
    /**
     * الأدوار المصفاة للتعيين
     */
    const filteredRolesForAssign = computed(() => {
      if (!assignRoleForm.value.user_id) {
        return roles.value;
      }
      
      const user = users.value.find(u => u.id === assignRoleForm.value.user_id);
      if (!user) {
        return roles.value;
      }
      
      // الحصول على الأدوار التي لم يتم تعيينها للمستخدم بعد
      return roles.value.filter(role => 
        !user.roles || !user.roles.some(r => r.id === role.id)
      );
    });
    
    /**
     * صلاحيات الدور المصفاة
     */
    const filteredRolePermissions = computed(() => {
      let result = [...permissions.value];
      
      // تطبيق فلتر البحث
      if (rolePermissionSearchQuery.value) {
        const query = rolePermissionSearchQuery.value.toLowerCase();
        result = result.filter(permission => 
          permission.name.toLowerCase().includes(query) || 
          (permission.description && permission.description.toLowerCase().includes(query))
        );
      }
      
      // تطبيق فلتر نوع المورد
      if (rolePermissionResourceFilter.value) {
        result = result.filter(permission => permission.resource_type === rolePermissionResourceFilter.value);
      }
      
      return result;
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
    
    /**
     * التحقق من صلاحيات المستخدم الحالي
     */
    const isAdmin = computed(() => {
      return authStore.hasPermission('admin');
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
     * التحقق مما إذا كانت الصلاحية معينة للدور
     * @param {string} permissionId - معرف الصلاحية
     * @returns {boolean} - ما إذا كانت الصلاحية معينة للدور
     */
    const isPermissionAssigned = (permissionId) => {
      return selectedRolePermissions.value.includes(permissionId);
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
     * تبديل حالة الصلاحية للدور
     * @param {string} permissionId - معرف الصلاحية
     */
    const togglePermission = (permissionId) => {
      const index = selectedRolePermissions.value.indexOf(permissionId);
      if (index === -1) {
        selectedRolePermissions.value.push(permissionId);
      } else {
        selectedRolePermissions.value.splice(index, 1);
      }
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
     * تحميل الصلاحيات
     */
    const loadPermissions = async () => {
      try {
        isLoading.value = true;
        const response = await permissionService.getPermissions();
        permissions.value = response.data;
        permissionsCount.value = permissions.value.length;
      } catch (error) {
        toast.error('حدث خطأ أثناء تحميل الصلاحيات');
        console.error('Error loading permissions:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * تحميل المستخدمين
     */
    const loadUsers = async () => {
      try {
        isLoading.value = true;
        const response = await userService.getUsers();
        users.value = response.data;
        usersWithRolesCount.value = users.value.filter(user => user.roles && user.roles.length > 0).length;
      } catch (error) {
        toast.error('حدث خطأ أثناء تحميل المستخدمين');
        console.error('Error loading users:', error);
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
     * إغلاق نافذة الدور
     */
    const closeRoleModal = () => {
      showAddRoleModal.value = false;
      showEditRoleModal.value = false;
      roleForm.value = {
        id: null,
        name: '',
        description: '',
        is_system_role: false,
        organization_id: ''
      };
    };
    
    /**
     * إغلاق نافذة الصلاحية
     */
    const closePermissionModal = () => {
      showAddPermissionModal.value = false;
      showEditPermissionModal.value = false;
      permissionForm.value = {
        id: null,
        name: '',
        description: '',
        resource_type: '',
        custom_resource_type: '',
        action: ''
      };
    };
    
    /**
     * تحرير دور
     * @param {Object} role - الدور المراد تحريره
     */
    const editRole = (role) => {
      roleForm.value = {
        id: role.id,
        name: role.name,
        description: role.description || '',
        is_system_role: role.is_system_role,
        organization_id: role.organization_id || ''
      };
      showEditRoleModal.value = true;
    };
    
    /**
     * تحرير صلاحية
     * @param {Object} permission - الصلاحية المراد تحريرها
     */
    const editPermission = (permission) => {
      permissionForm.value = {
        id: permission.id,
        name: permission.name,
        description: permission.description || '',
        resource_type: permission.resource_type,
        custom_resource_type: '',
        action: permission.action
      };
      showEditPermissionModal.value = true;
    };
    
    /**
     * حفظ الدور
     */
    const saveRole = async () => {
      try {
        isLoading.value = true;
        
        // التحقق من صحة البيانات
        if (!roleForm.value.name) {
          toast.error('يرجى إدخال اسم الدور');
          return;
        }
        
        // تحديد نوع المورد المخصص إذا كان مطلوباً
        const formData = {
          name: roleForm.value.name,
          description: roleForm.value.description,
          is_system_role: roleForm.value.is_system_role,
          organization_id: roleForm.value.organization_id || null
        };
        
        if (showEditRoleModal.value) {
          // تحديث دور موجود
          await permissionService.updateRole(roleForm.value.id, formData);
          toast.success('تم تحديث الدور بنجاح');
        } else {
          // إنشاء دور جديد
          await permissionService.createRole(formData);
          toast.success('تم إنشاء الدور بنجاح');
        }
        
        // إعادة تحميل الأدوار
        await loadRoles();
        
        // إغلاق النافذة
        closeRoleModal();
      } catch (error) {
        toast.error('حدث خطأ أثناء حفظ الدور');
        console.error('Error saving role:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * حفظ الصلاحية
     */
    const savePermission = async () => {
      try {
        isLoading.value = true;
        
        // التحقق من صحة البيانات
        if (!permissionForm.value.name) {
          toast.error('يرجى إدخال اسم الصلاحية');
          return;
        }
        
        if (!permissionForm.value.resource_type) {
          toast.error('يرجى اختيار نوع المورد');
          return;
        }
        
        if (!permissionForm.value.action) {
          toast.error('يرجى اختيار نوع الإجراء');
          return;
        }
        
        // تحديد نوع المورد المخصص إذا كان مطلوباً
        const resourceType = permissionForm.value.resource_type === 'custom' 
          ? permissionForm.value.custom_resource_type 
          : permissionForm.value.resource_type;
        
        const formData = {
          name: permissionForm.value.name,
          description: permissionForm.value.description,
          resource_type: resourceType,
          action: permissionForm.value.action
        };
        
        if (showEditPermissionModal.value) {
          // تحديث صلاحية موجودة
          await permissionService.updatePermission(permissionForm.value.id, formData);
          toast.success('تم تحديث الصلاحية بنجاح');
        } else {
          // إنشاء صلاحية جديدة
          await permissionService.createPermission(formData);
          toast.success('تم إنشاء الصلاحية بنجاح');
        }
        
        // إعادة تحميل الصلاحيات
        await loadPermissions();
        
        // إغلاق النافذة
        closePermissionModal();
      } catch (error) {
        toast.error('حدث خطأ أثناء حفظ الصلاحية');
        console.error('Error saving permission:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * حذف دور
     * @param {Object} role - الدور المراد حذفه
     */
    const deleteRole = (role) => {
      // التحقق من إمكانية حذف الدور
      if (role.is_system_role) {
        toast.error('لا يمكن حذف دور النظام');
        return;
      }
      
      if (role.users && role.users.length > 0) {
        toast.error('لا يمكن حذف الدور لأنه مرتبط بمستخدمين');
        return;
      }
      
      // تأكيد الحذف
      confirmTitle.value = 'تأكيد حذف الدور';
      confirmMessage.value = `هل أنت متأكد من حذف الدور "${role.name}"؟`;
      confirmAction.value = async () => {
        try {
          isLoading.value = true;
          await permissionService.deleteRole(role.id);
          toast.success('تم حذف الدور بنجاح');
          await loadRoles();
        } catch (error) {
          toast.error('حدث خطأ أثناء حذف الدور');
          console.error('Error deleting role:', error);
        } finally {
          isLoading.value = false;
          showConfirmModal.value = false;
        }
      };
      
      showConfirmModal.value = true;
    };
    
    /**
     * حذف صلاحية
     * @param {Object} permission - الصلاحية المراد حذفها
     */
    const deletePermission = (permission) => {
      // التحقق من إمكانية حذف الصلاحية
      if (permission.roles && permission.roles.length > 0) {
        toast.error('لا يمكن حذف الصلاحية لأنها مرتبطة بأدوار');
        return;
      }
      
      // تأكيد الحذف
      confirmTitle.value = 'تأكيد حذف الصلاحية';
      confirmMessage.value = `هل أنت متأكد من حذف الصلاحية "${permission.name}"؟`;
      confirmAction.value = async () => {
        try {
          isLoading.value = true;
          await permissionService.deletePermission(permission.id);
          toast.success('تم حذف الصلاحية بنجاح');
          await loadPermissions();
        } catch (error) {
          toast.error('حدث خطأ أثناء حذف الصلاحية');
          console.error('Error deleting permission:', error);
        } finally {
          isLoading.value = false;
          showConfirmModal.value = false;
        }
      };
      
      showConfirmModal.value = true;
    };
    
    /**
     * عرض صلاحيات الدور
     * @param {Object} role - الدور المراد عرض صلاحياته
     */
    const viewRolePermissions = (role) => {
      selectedRole.value = role;
      selectedRolePermissions.value = role.permissions ? role.permissions.map(p => p.id) : [];
      showRolePermissionsModal.value = true;
    };
    
    /**
     * حفظ صلاحيات الدور
     */
    const saveRolePermissions = async () => {
      try {
        isLoading.value = true;
        
        // الحصول على الصلاحيات الحالية للدور
        const currentPermissions = selectedRole.value.permissions 
          ? selectedRole.value.permissions.map(p => p.id) 
          : [];
        
        // تحديد الصلاحيات المضافة والمحذوفة
        const addedPermissions = selectedRolePermissions.value.filter(
          id => !currentPermissions.includes(id)
        );
        
        const removedPermissions = currentPermissions.filter(
          id => !selectedRolePermissions.value.includes(id)
        );
        
        // تطبيق التغييرات
        for (const permissionId of addedPermissions) {
          await permissionService.assignPermissionToRole(selectedRole.value.id, permissionId);
        }
        
        for (const permissionId of removedPermissions) {
          await permissionService.removePermissionFromRole(selectedRole.value.id, permissionId);
        }
        
        toast.success('تم حفظ صلاحيات الدور بنجاح');
        
        // إعادة تحميل الأدوار
        await loadRoles();
        
        // إغلاق النافذة
        showRolePermissionsModal.value = false;
      } catch (error) {
        toast.error('حدث خطأ أثناء حفظ صلاحيات الدور');
        console.error('Error saving role permissions:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
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
     * تعيين دور لمستخدم
     */
    const assignRoleToUser = async () => {
      try {
        isLoading.value = true;
        
        // التحقق من صحة البيانات
        if (!assignRoleForm.value.user_id) {
          toast.error('يرجى اختيار المستخدم');
          return;
        }
        
        if (!assignRoleForm.value.role_id) {
          toast.error('يرجى اختيار الدور');
          return;
        }
        
        // تعيين الدور للمستخدم
        await permissionService.assignRoleToUser(
          assignRoleForm.value.user_id, 
          assignRoleForm.value.role_id
        );
        
        toast.success('تم تعيين الدور للمستخدم بنجاح');
        
        // إعادة تحميل المستخدمين
        await loadUsers();
        
        // إغلاق النافذة
        showAssignRoleModal.value = false;
        assignRoleForm.value = {
          user_id: '',
          role_id: ''
        };
      } catch (error) {
        toast.error('حدث خطأ أثناء تعيين الدور للمستخدم');
        console.error('Error assigning role to user:', error);
      } finally {
        isLoading.value = false;
      }
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
    
    /**
     * عرض صلاحيات المستخدم
     * @param {Object} user - المستخدم المراد عرض صلاحياته
     */
    const viewUserPermissions = async (user) => {
      selectedUser.value = user;
      await loadUserPermissions(user.id);
      showUserPermissionsModal.value = true;
    };
    
    // دورة حياة المكون
    
    onMounted(async () => {
      // تحميل البيانات
      await Promise.all([
        loadRoles(),
        loadPermissions(),
        loadUsers(),
        loadOrganizations()
      ]);
    });
    
    // مراقبة التغييرات
    
    watch(roleSearchQuery, () => {
      currentRolePage.value = 1;
    });
    
    watch(permissionSearchQuery, () => {
      currentPermissionPage.value = 1;
    });
    
    watch(userSearchQuery, () => {
      currentUserPage.value = 1;
    });
    
    watch(organizationFilter, () => {
      currentRolePage.value = 1;
    });
    
    watch(resourceTypeFilter, () => {
      currentPermissionPage.value = 1;
    });
    
    watch(actionFilter, () => {
      currentPermissionPage.value = 1;
    });
    
    watch(userRoleFilter, () => {
      currentUserPage.value = 1;
    });
    
    watch(organizationUserFilter, () => {
      currentUserPage.value = 1;
    });
    
    watch(showSystemRoles, () => {
      currentRolePage.value = 1;
    });
    
    return {
      // الحالة
      activeTab,
      isLoading,
      
      // البيانات
      roles,
      permissions,
      users,
      organizations,
      
      // الإحصائيات
      rolesCount,
      permissionsCount,
      usersWithRolesCount,
      
      // الفلاتر
      roleSearchQuery,
      permissionSearchQuery,
      userSearchQuery,
      organizationFilter,
      resourceTypeFilter,
      actionFilter,
      userRoleFilter,
      organizationUserFilter,
      showSystemRoles,
      
      // التنقل بين الصفحات
      currentRolePage,
      currentPermissionPage,
      currentUserPage,
      
      // النوافذ
      showAddRoleModal,
      showEditRoleModal,
      showAddPermissionModal,
      showEditPermissionModal,
      showAssignRoleModal,
      showCopyUserRolesModal,
      showRolePermissionsModal,
      showUserRolesModal,
      showUserPermissionsModal,
      showConfirmModal,
      
      // النماذج
      roleForm,
      permissionForm,
      assignRoleForm,
      copyRolesForm,
      
      // البيانات المحددة
      selectedRole,
      selectedUser,
      selectedPermission,
      
      // بيانات التأكيد
      confirmTitle,
      confirmMessage,
      confirmAction,
      
      // بيانات إدارة صلاحيات الدور
      rolePermissionSearchQuery,
      rolePermissionResourceFilter,
      selectedRolePermissions,
      
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
      filteredRoles,
      totalRolePages,
      filteredPermissions,
      totalPermissionPages,
      filteredUsers,
      totalUserPages,
      filteredRolesForAssign,
      filteredRolePermissions,
      filteredUserRoles,
      filteredUserPermissions,
      isAdmin,
      
      // دوال المساعدة
      getOrganizationName,
      getActionLabel,
      isPermissionAssigned,
      isRoleAssigned,
      togglePermission,
      toggleRole,
      getSourceUserRoles,
      
      // دوال الإجراءات
      closeRoleModal,
      closePermissionModal,
      editRole,
      editPermission,
      saveRole,
      savePermission,
      deleteRole,
      deletePermission,
      viewRolePermissions,
      saveRolePermissions,
      manageUserRoles,
      saveUserRoles,
      assignRoleToUser,
      copyUserRoles,
      copyUserRolesToUser,
      viewUserPermissions
    };
  }
};
</script>

<style scoped>
.role-management {
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

/* علامات التبويب */
.tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab.active {
  border-bottom: 2px solid #4a6cf7;
  color: #4a6cf7;
  font-weight: bold;
}

.tab:hover {
  background-color: #f5f5f5;
}

/* محتوى علامات التبويب */
.tab-content {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

/* رأس القسم */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 10px;
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

.filter-checkbox {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.filter-checkbox input {
  margin-left: 5px;
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

.btn-danger {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-danger:hover {
  background-color: #d32f2f;
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

.btn-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

/* العلامات والأيقونات */
.role-type,
.action-type {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.role-type.system {
  background-color: #e3f2fd;
  color: #1976d2;
}

.role-type.custom {
  background-color: #e8f5e9;
  color: #388e3c;
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

/* شبكة الصلاحيات والأدوار */
.permissions-grid,
.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
  margin-top: 15px;
}

.permission-item,
.role-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.permission-item:hover,
.role-item:hover {
  background-color: #f5f5f5;
}

.permission-item.assigned,
.role-item.assigned {
  background-color: #e3f2fd;
  border-color: #1976d2;
}

.permission-checkbox,
.role-checkbox {
  margin-left: 10px;
}

.permission-info,
.role-info {
  flex: 1;
}

.permission-name,
.role-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.permission-details,
.role-details {
  display: flex;
  gap: 10px;
  font-size: 0.8rem;
}

.resource-type,
.organization,
.role-type {
  color: #666;
}

.role-item.system-role {
  border-color: #c2185b;
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

/* قائمة صلاحيات المستخدم */
.permissions-list {
  margin-top: 15px;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .stats-cards {
    flex-direction: column;
  }
  
  .stat-card {
    margin: 0 0 10px 0;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-actions {
    margin-top: 10px;
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
