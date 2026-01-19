<!-- File: /home/ubuntu/clean_project/frontend/pages/admin/UserManagement.vue -->
<template>
  <div class="user-management-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="fas fa-users"></i>
          إدارة المستخدمين
        </h1>
        <p class="page-description">
          إدارة حسابات المستخدمين والصلاحيات والأدوار
        </p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="showAddUserModal = true">
          <i class="fas fa-plus"></i>
          إضافة مستخدم جديد
        </button>
        <button class="btn btn-outline-primary" @click="exportUsers">
          <i class="fas fa-download"></i>
          تصدير البيانات
        </button>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section">
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input 
          type="text" 
          placeholder="البحث في المستخدمين..." 
          v-model="searchQuery"
          @input="filterUsers"
        >
      </div>
      
      <div class="filter-controls">
        <select v-model="selectedRole" @change="filterUsers" class="filter-select">
          <option value="">جميع الأدوار</option>
          <option value="admin">مدير</option>
          <option value="user">مستخدم</option>
          <option value="expert">خبير</option>
          <option value="viewer">مشاهد</option>
        </select>
        
        <select v-model="selectedStatus" @change="filterUsers" class="filter-select">
          <option value="">جميع الحالات</option>
          <option value="active">نشط</option>
          <option value="inactive">غير نشط</option>
          <option value="suspended">معلق</option>
        </select>
        
        <button class="btn btn-outline-secondary" @click="resetFilters">
          <i class="fas fa-undo"></i>
          إعادة تعيين
        </button>
      </div>
    </div>

    <!-- Users Table -->
    <div class="users-table-container">
      <div class="table-header">
        <h3>قائمة المستخدمين ({{ filteredUsers.length }})</h3>
        <div class="table-actions">
          <button class="btn btn-sm btn-outline-danger" @click="deleteSelectedUsers" :disabled="selectedUsers.length === 0">
            <i class="fas fa-trash"></i>
            حذف المحدد ({{ selectedUsers.length }})
          </button>
        </div>
      </div>

      <div class="table-responsive">
        <table class="users-table">
          <thead>
            <tr>
              <th>
                <input 
                  type="checkbox" 
                  @change="toggleSelectAll"
                  :checked="selectedUsers.length === filteredUsers.length && filteredUsers.length > 0"
                >
              </th>
              <th>الصورة</th>
              <th @click="sortBy('name')" class="sortable">
                الاسم
                <i :class="getSortIcon('name')"></i>
              </th>
              <th @click="sortBy('email')" class="sortable">
                البريد الإلكتروني
                <i :class="getSortIcon('email')"></i>
              </th>
              <th>الدور</th>
              <th>الحالة</th>
              <th @click="sortBy('lastLogin')" class="sortable">
                آخر دخول
                <i :class="getSortIcon('lastLogin')"></i>
              </th>
              <th @click="sortBy('createdAt')" class="sortable">
                تاريخ الإنشاء
                <i :class="getSortIcon('createdAt')"></i>
              </th>
              <th>الإجراءات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id" :class="{ selected: selectedUsers.includes(user.id) }">
              <td>
                <input 
                  type="checkbox" 
                  :value="user.id"
                  v-model="selectedUsers"
                >
              </td>
              <td>
                <div class="user-avatar">
                  <img v-if="user.avatar" :src="user.avatar" :alt="user.name">
                  <div v-else class="avatar-placeholder">
                    {{ user.name.charAt(0).toUpperCase() }}
                  </div>
                </div>
              </td>
              <td>
                <div class="user-info">
                  <div class="user-name">{{ user.name }}</div>
                  <div class="user-username">@{{ user.username }}</div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>
                <span :class="['role-badge', `role-${user.role}`]">
                  {{ getRoleName(user.role) }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', `status-${user.status}`]">
                  {{ getStatusName(user.status) }}
                </span>
              </td>
              <td>
                <span v-if="user.lastLogin" class="date-text">
                  {{ formatDate(user.lastLogin) }}
                </span>
                <span v-else class="text-muted">لم يدخل بعد</span>
              </td>
              <td>
                <span class="date-text">{{ formatDate(user.createdAt) }}</span>
              </td>
              <td>
                <div class="action-buttons">
                  <button class="btn-icon btn-primary" @click="editUser(user)" title="تعديل">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn-icon btn-info" @click="viewUserDetails(user)" title="عرض التفاصيل">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button class="btn-icon btn-warning" @click="resetUserPassword(user)" title="إعادة تعيين كلمة المرور">
                    <i class="fas fa-key"></i>
                  </button>
                  <button 
                    class="btn-icon"
                    :class="user.status === 'active' ? 'btn-secondary' : 'btn-success'"
                    @click="toggleUserStatus(user)"
                    :title="user.status === 'active' ? 'تعطيل' : 'تفعيل'"
                  >
                    <i :class="user.status === 'active' ? 'fas fa-ban' : 'fas fa-check'"></i>
                  </button>
                  <button class="btn-icon btn-danger" @click="deleteUser(user)" title="حذف">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination-container">
        <div class="pagination-info">
          عرض {{ (currentPage - 1) * itemsPerPage + 1 }} إلى {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }} من {{ filteredUsers.length }} مستخدم
        </div>
        <div class="pagination">
          <button 
            class="btn btn-sm btn-outline-primary" 
            @click="currentPage--" 
            :disabled="currentPage === 1"
          >
            السابق
          </button>
          <span class="page-numbers">
            <button 
              v-for="page in visiblePages" 
              :key="page"
              class="btn btn-sm"
              :class="page === currentPage ? 'btn-primary' : 'btn-outline-primary'"
              @click="currentPage = page"
            >
              {{ page }}
            </button>
          </span>
          <button 
            class="btn btn-sm btn-outline-primary" 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
          >
            التالي
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit User Modal -->
    <div v-if="showAddUserModal || showEditUserModal" class="modal-overlay" @click="closeModals">
      <div class="modal-content large-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ showAddUserModal ? 'إضافة مستخدم جديد' : 'تعديل المستخدم' }}</h3>
          <button class="modal-close" @click="closeModals">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveUser" class="user-form">
            <div class="form-grid">
              <div class="form-group">
                <label>الاسم الكامل *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="userForm.name" 
                  required
                  placeholder="أدخل الاسم الكامل"
                >
              </div>
              
              <div class="form-group">
                <label>اسم المستخدم *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="userForm.username" 
                  required
                  placeholder="أدخل اسم المستخدم"
                >
              </div>
              
              <div class="form-group">
                <label>البريد الإلكتروني *</label>
                <input 
                  type="email" 
                  class="form-control" 
                  v-model="userForm.email" 
                  required
                  placeholder="أدخل البريد الإلكتروني"
                >
              </div>
              
              <div class="form-group">
                <label>رقم الهاتف</label>
                <input 
                  type="tel" 
                  class="form-control" 
                  v-model="userForm.phone"
                  placeholder="أدخل رقم الهاتف"
                >
              </div>
              
              <div class="form-group">
                <label>الدور *</label>
                <select class="form-control" v-model="userForm.role" required>
                  <option value="">اختر الدور</option>
                  <option value="admin">مدير</option>
                  <option value="user">مستخدم</option>
                  <option value="expert">خبير</option>
                  <option value="viewer">مشاهد</option>
                </select>
              </div>
              
              <div class="form-group">
                <label>الحالة</label>
                <select class="form-control" v-model="userForm.status">
                  <option value="active">نشط</option>
                  <option value="inactive">غير نشط</option>
                  <option value="suspended">معلق</option>
                </select>
              </div>
              
              <div v-if="showAddUserModal" class="form-group">
                <label>كلمة المرور *</label>
                <input 
                  type="password" 
                  class="form-control" 
                  v-model="userForm.password" 
                  required
                  placeholder="أدخل كلمة المرور"
                >
              </div>
              
              <div v-if="showAddUserModal" class="form-group">
                <label>تأكيد كلمة المرور *</label>
                <input 
                  type="password" 
                  class="form-control" 
                  v-model="userForm.confirmPassword" 
                  required
                  placeholder="أعد إدخال كلمة المرور"
                >
              </div>
            </div>
            
            <div class="form-group">
              <label>الملاحظات</label>
              <textarea 
                class="form-control" 
                v-model="userForm.notes" 
                rows="3"
                placeholder="ملاحظات إضافية عن المستخدم"
              ></textarea>
            </div>
            
            <div class="permissions-section">
              <h4>الصلاحيات</h4>
              <div class="permissions-grid">
                <div v-for="permission in availablePermissions" :key="permission.id" class="permission-item">
                  <input 
                    type="checkbox" 
                    :id="permission.id"
                    :value="permission.id"
                    v-model="userForm.permissions"
                  >
                  <label :for="permission.id">{{ permission.name }}</label>
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModals">إلغاء</button>
          <button type="submit" class="btn btn-primary" @click="saveUser" :disabled="saving">
            {{ saving ? 'جاري الحفظ...' : (showAddUserModal ? 'إضافة المستخدم' : 'حفظ التغييرات') }}
          </button>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div v-if="showUserDetailsModal" class="modal-overlay" @click="showUserDetailsModal = false">
      <div class="modal-content large-modal" @click.stop>
        <div class="modal-header">
          <h3>تفاصيل المستخدم</h3>
          <button class="modal-close" @click="showUserDetailsModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="selectedUserDetails" class="user-details">
            <div class="user-profile">
              <div class="profile-avatar">
                <img v-if="selectedUserDetails.avatar" :src="selectedUserDetails.avatar" :alt="selectedUserDetails.name">
                <div v-else class="avatar-placeholder large">
                  {{ selectedUserDetails.name.charAt(0).toUpperCase() }}
                </div>
              </div>
              <div class="profile-info">
                <h4>{{ selectedUserDetails.name }}</h4>
                <p>@{{ selectedUserDetails.username }}</p>
                <span :class="['status-badge', `status-${selectedUserDetails.status}`]">
                  {{ getStatusName(selectedUserDetails.status) }}
                </span>
              </div>
            </div>
            
            <div class="details-grid">
              <div class="detail-item">
                <label>البريد الإلكتروني:</label>
                <span>{{ selectedUserDetails.email }}</span>
              </div>
              <div class="detail-item">
                <label>رقم الهاتف:</label>
                <span>{{ selectedUserDetails.phone || 'غير محدد' }}</span>
              </div>
              <div class="detail-item">
                <label>الدور:</label>
                <span class="role-badge">{{ getRoleName(selectedUserDetails.role) }}</span>
              </div>
              <div class="detail-item">
                <label>تاريخ الإنشاء:</label>
                <span>{{ formatDate(selectedUserDetails.createdAt) }}</span>
              </div>
              <div class="detail-item">
                <label>آخر دخول:</label>
                <span>{{ selectedUserDetails.lastLogin ? formatDate(selectedUserDetails.lastLogin) : 'لم يدخل بعد' }}</span>
              </div>
              <div class="detail-item">
                <label>عدد مرات الدخول:</label>
                <span>{{ selectedUserDetails.loginCount || 0 }}</span>
              </div>
            </div>
            
            <div v-if="selectedUserDetails.notes" class="notes-section">
              <h5>الملاحظات:</h5>
              <p>{{ selectedUserDetails.notes }}</p>
            </div>
            
            <div class="permissions-display">
              <h5>الصلاحيات:</h5>
              <div class="permissions-list">
                <span 
                  v-for="permission in selectedUserDetails.permissions" 
                  :key="permission"
                  class="permission-tag"
                >
                  {{ getPermissionName(permission) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserManagement',
  data() {
    return {
      users: [],
      filteredUsers: [],
      selectedUsers: [],
      searchQuery: '',
      selectedRole: '',
      selectedStatus: '',
      sortField: 'name',
      sortDirection: 'asc',
      currentPage: 1,
      itemsPerPage: 10,
      
      // Modals
      showAddUserModal: false,
      showEditUserModal: false,
      showUserDetailsModal: false,
      selectedUserDetails: null,
      saving: false,
      
      // User Form
      userForm: {
        id: null,
        name: '',
        username: '',
        email: '',
        phone: '',
        role: '',
        status: 'active',
        password: '',
        confirmPassword: '',
        notes: '',
        permissions: []
      },
      
      // Available permissions
      availablePermissions: [
        { id: 'users_read', name: 'عرض المستخدمين' },
        { id: 'users_write', name: 'إدارة المستخدمين' },
        { id: 'diagnosis_read', name: 'عرض التشخيصات' },
        { id: 'diagnosis_write', name: 'إجراء التشخيصات' },
        { id: 'ai_read', name: 'عرض الذكاء الاصطناعي' },
        { id: 'ai_write', name: 'إدارة الذكاء الاصطناعي' },
        { id: 'reports_read', name: 'عرض التقارير' },
        { id: 'reports_write', name: 'إنشاء التقارير' },
        { id: 'settings_read', name: 'عرض الإعدادات' },
        { id: 'settings_write', name: 'تعديل الإعدادات' }
      ]
    }
  },
  computed: {
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredUsers.slice(start, end)
    },
    
    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.itemsPerPage)
    },
    
    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end = Math.min(this.totalPages, this.currentPage + 2)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    async loadUsers() {
      try {
        // محاكاة تحميل البيانات من الخادم
        const response = await fetch('/api/users')
        if (response.ok) {
          this.users = await response.json()
        } else {
          // بيانات تجريبية
          this.users = [
            {
              id: 1,
              name: 'أحمد محمد',
              username: 'ahmed_mohamed',
              email: 'ahmed@example.com',
              phone: '+966501234567',
              role: 'admin',
              status: 'active',
              avatar: null,
              lastLogin: new Date('2025-06-17T10:30:00'),
              createdAt: new Date('2025-01-15T09:00:00'),
              loginCount: 45,
              notes: 'مدير النظام الرئيسي',
              permissions: ['users_read', 'users_write', 'diagnosis_read', 'diagnosis_write', 'ai_read', 'ai_write', 'reports_read', 'reports_write', 'settings_read', 'settings_write']
            },
            {
              id: 2,
              name: 'فاطمة علي',
              username: 'fatima_ali',
              email: 'fatima@example.com',
              phone: '+966507654321',
              role: 'expert',
              status: 'active',
              avatar: null,
              lastLogin: new Date('2025-06-16T14:20:00'),
              createdAt: new Date('2025-02-01T11:30:00'),
              loginCount: 32,
              notes: 'خبيرة في أمراض النباتات',
              permissions: ['diagnosis_read', 'diagnosis_write', 'ai_read', 'reports_read']
            },
            {
              id: 3,
              name: 'محمد السعيد',
              username: 'mohamed_alsaeed',
              email: 'mohamed@example.com',
              phone: '+966509876543',
              role: 'user',
              status: 'active',
              avatar: null,
              lastLogin: new Date('2025-06-15T16:45:00'),
              createdAt: new Date('2025-03-10T08:15:00'),
              loginCount: 18,
              notes: '',
              permissions: ['diagnosis_read', 'diagnosis_write']
            },
            {
              id: 4,
              name: 'سارة أحمد',
              username: 'sara_ahmed',
              email: 'sara@example.com',
              phone: '+966502468135',
              role: 'viewer',
              status: 'inactive',
              avatar: null,
              lastLogin: null,
              createdAt: new Date('2025-04-05T13:20:00'),
              loginCount: 0,
              notes: 'حساب تجريبي',
              permissions: ['diagnosis_read']
            }
          ]
        }
        this.filteredUsers = [...this.users]
      } catch (error) {
        console.error('خطأ في تحميل المستخدمين:', error)
        this.$toast.error('فشل في تحميل بيانات المستخدمين')
      }
    },
    
    filterUsers() {
      this.filteredUsers = this.users.filter(user => {
        const matchesSearch = !this.searchQuery || 
          user.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.email.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.username.toLowerCase().includes(this.searchQuery.toLowerCase())
        
        const matchesRole = !this.selectedRole || user.role === this.selectedRole
        const matchesStatus = !this.selectedStatus || user.status === this.selectedStatus
        
        return matchesSearch && matchesRole && matchesStatus
      })
      
      this.sortUsers()
      this.currentPage = 1
    },
    
    sortBy(field) {
      if (this.sortField === field) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortDirection = 'asc'
      }
      this.sortUsers()
    },
    
    sortUsers() {
      this.filteredUsers.sort((a, b) => {
        let aVal = a[this.sortField]
        let bVal = b[this.sortField]
        
        if (this.sortField === 'lastLogin') {
          aVal = aVal ? new Date(aVal) : new Date(0)
          bVal = bVal ? new Date(bVal) : new Date(0)
        } else if (this.sortField === 'createdAt') {
          aVal = new Date(aVal)
          bVal = new Date(bVal)
        } else if (typeof aVal === 'string') {
          aVal = aVal.toLowerCase()
          bVal = bVal.toLowerCase()
        }
        
        if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1
        if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1
        return 0
      })
    },
    
    getSortIcon(field) {
      if (this.sortField !== field) return 'fas fa-sort'
      return this.sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down'
    },
    
    resetFilters() {
      this.searchQuery = ''
      this.selectedRole = ''
      this.selectedStatus = ''
      this.filteredUsers = [...this.users]
      this.currentPage = 1
    },
    
    toggleSelectAll() {
      if (this.selectedUsers.length === this.filteredUsers.length) {
        this.selectedUsers = []
      } else {
        this.selectedUsers = this.filteredUsers.map(user => user.id)
      }
    },
    
    editUser(user) {
      this.userForm = {
        id: user.id,
        name: user.name,
        username: user.username,
        email: user.email,
        phone: user.phone || '',
        role: user.role,
        status: user.status,
        password: '',
        confirmPassword: '',
        notes: user.notes || '',
        permissions: [...(user.permissions || [])]
      }
      this.showEditUserModal = true
    },
    
    viewUserDetails(user) {
      this.selectedUserDetails = user
      this.showUserDetailsModal = true
    },
    
    async saveUser() {
      if (this.showAddUserModal && this.userForm.password !== this.userForm.confirmPassword) {
        this.$toast.error('كلمات المرور غير متطابقة')
        return
      }
      
      this.saving = true
      
      try {
        const url = this.showAddUserModal ? '/api/users' : `/api/users/${this.userForm.id}`
        const method = this.showAddUserModal ? 'POST' : 'PUT'
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.userForm)
        })
        
        if (response.ok) {
          this.$toast.success(this.showAddUserModal ? 'تم إضافة المستخدم بنجاح' : 'تم تحديث المستخدم بنجاح')
          this.closeModals()
          this.loadUsers()
        } else {
          throw new Error('فشل في حفظ المستخدم')
        }
      } catch (error) {
        console.error('خطأ في حفظ المستخدم:', error)
        this.$toast.error('فشل في حفظ المستخدم')
      } finally {
        this.saving = false
      }
    },
    
    async deleteUser(user) {
      if (confirm(`هل أنت متأكد من حذف المستخدم "${user.name}"؟`)) {
        try {
          const response = await fetch(`/api/users/${user.id}`, {
            method: 'DELETE'
          })
          
          if (response.ok) {
            this.$toast.success('تم حذف المستخدم بنجاح')
            this.loadUsers()
          } else {
            throw new Error('فشل في حذف المستخدم')
          }
        } catch (error) {
          console.error('خطأ في حذف المستخدم:', error)
          this.$toast.error('فشل في حذف المستخدم')
        }
      }
    },
    
    async deleteSelectedUsers() {
      if (confirm(`هل أنت متأكد من حذف ${this.selectedUsers.length} مستخدم؟`)) {
        try {
          const response = await fetch('/api/users/bulk-delete', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ userIds: this.selectedUsers })
          })
          
          if (response.ok) {
            this.$toast.success('تم حذف المستخدمين بنجاح')
            this.selectedUsers = []
            this.loadUsers()
          } else {
            throw new Error('فشل في حذف المستخدمين')
          }
        } catch (error) {
          console.error('خطأ في حذف المستخدمين:', error)
          this.$toast.error('فشل في حذف المستخدمين')
        }
      }
    },
    
    async toggleUserStatus(user) {
      const newStatus = user.status === 'active' ? 'inactive' : 'active'
      
      try {
        const response = await fetch(`/api/users/${user.id}/status`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ status: newStatus })
        })
        
        if (response.ok) {
          user.status = newStatus
          this.$toast.success(`تم ${newStatus === 'active' ? 'تفعيل' : 'تعطيل'} المستخدم بنجاح`)
        } else {
          throw new Error('فشل في تغيير حالة المستخدم')
        }
      } catch (error) {
        console.error('خطأ في تغيير حالة المستخدم:', error)
        this.$toast.error('فشل في تغيير حالة المستخدم')
      }
    },
    
    async resetUserPassword(user) {
      if (confirm(`هل أنت متأكد من إعادة تعيين كلمة مرور "${user.name}"؟`)) {
        try {
          const response = await fetch(`/api/users/${user.id}/reset-password`, {
            method: 'POST'
          })
          
          if (response.ok) {
            const data = await response.json()
            this.$toast.success('تم إعادة تعيين كلمة المرور بنجاح')
            // يمكن عرض كلمة المرور الجديدة أو إرسالها بالبريد الإلكتروني
          } else {
            throw new Error('فشل في إعادة تعيين كلمة المرور')
          }
        } catch (error) {
          console.error('خطأ في إعادة تعيين كلمة المرور:', error)
          this.$toast.error('فشل في إعادة تعيين كلمة المرور')
        }
      }
    },
    
    async exportUsers() {
      try {
        const response = await fetch('/api/users/export')
        if (response.ok) {
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `users_${new Date().toISOString().split('T')[0]}.xlsx`
          a.click()
          window.URL.revokeObjectURL(url)
          this.$toast.success('تم تصدير البيانات بنجاح')
        } else {
          throw new Error('فشل في تصدير البيانات')
        }
      } catch (error) {
        console.error('خطأ في تصدير البيانات:', error)
        this.$toast.error('فشل في تصدير البيانات')
      }
    },
    
    closeModals() {
      this.showAddUserModal = false
      this.showEditUserModal = false
      this.userForm = {
        id: null,
        name: '',
        username: '',
        email: '',
        phone: '',
        role: '',
        status: 'active',
        password: '',
        confirmPassword: '',
        notes: '',
        permissions: []
      }
    },
    
    getRoleName(role) {
      const roles = {
        admin: 'مدير',
        user: 'مستخدم',
        expert: 'خبير',
        viewer: 'مشاهد'
      }
      return roles[role] || role
    },
    
    getStatusName(status) {
      const statuses = {
        active: 'نشط',
        inactive: 'غير نشط',
        suspended: 'معلق'
      }
      return statuses[status] || status
    },
    
    getPermissionName(permission) {
      const perm = this.availablePermissions.find(p => p.id === permission)
      return perm ? perm.name : permission
    },
    
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
/* استخدام نفس الأنماط من Settings.vue مع تخصيصات إضافية */
.user-management-page {
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2E7D32;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-description {
  color: #666;
  margin: 0.5rem 0 0 0;
  font-size: 1.1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  display: flex;
  gap: 2rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-box input:focus {
  outline: none;
  border-color: #2E7D32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
}

.filter-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.filter-select {
  padding: 0.5rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  min-width: 150px;
}

.users-table-container {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.table-header h3 {
  margin: 0;
  color: #2E7D32;
  font-size: 1.3rem;
}

.table-responsive {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th,
.users-table td {
  padding: 1rem;
  text-align: right;
  border-bottom: 1px solid #f0f0f0;
}

.users-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #333;
  position: sticky;
  top: 0;
  z-index: 10;
}

.users-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.3s ease;
}

.users-table th.sortable:hover {
  background: #e9ecef;
}

.users-table tr:hover {
  background: #f8f9fa;
}

.users-table tr.selected {
  background: rgba(46, 125, 50, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.2rem;
}

.avatar-placeholder.large {
  width: 80px;
  height: 80px;
  font-size: 2rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-name {
  font-weight: 600;
  color: #333;
}

.user-username {
  font-size: 0.85rem;
  color: #666;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.role-admin {
  background: #dc3545;
  color: white;
}

.role-expert {
  background: #fd7e14;
  color: white;
}

.role-user {
  background: #0d6efd;
  color: white;
}

.role-viewer {
  background: #6c757d;
  color: white;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-inactive {
  background: #f8d7da;
  color: #721c24;
}

.status-suspended {
  background: #fff3cd;
  color: #856404;
}

.date-text {
  font-size: 0.9rem;
  color: #666;
}

.text-muted {
  color: #999;
  font-style: italic;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn-icon {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.btn-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.btn-primary { background: #0d6efd; }
.btn-info { background: #0dcaf0; }
.btn-warning { background: #ffc107; color: #000; }
.btn-success { background: #198754; }
.btn-secondary { background: #6c757d; }
.btn-danger { background: #dc3545; }

.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.pagination {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.btn-primary {
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
}

.btn-outline-primary {
  background: transparent;
  color: #2E7D32;
  border: 2px solid #2E7D32;
}

.btn-outline-secondary {
  background: transparent;
  color: #6c757d;
  border: 2px solid #6c757d;
}

.btn-outline-danger {
  background: transparent;
  color: #dc3545;
  border: 2px solid #dc3545;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 15px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.large-modal {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  color: #2E7D32;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.user-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #333;
}

.form-control {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #2E7D32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
}

.permissions-section {
  margin-top: 1rem;
}

.permissions-section h4 {
  margin: 0 0 1rem 0;
  color: #2E7D32;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.permission-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.permission-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.user-profile {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 10px;
}

.profile-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2E7D32;
}

.profile-info p {
  margin: 0 0 0.5rem 0;
  color: #666;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.detail-item span {
  color: #333;
}

.notes-section {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.notes-section h5 {
  margin: 0 0 0.5rem 0;
  color: #2E7D32;
}

.permissions-display h5 {
  margin: 0 0 1rem 0;
  color: #2E7D32;
}

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.permission-tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .user-management-page {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .filters-section {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .filter-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .table-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .permissions-grid {
    grid-template-columns: 1fr;
  }
  
  .user-profile {
    flex-direction: column;
    text-align: center;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>

