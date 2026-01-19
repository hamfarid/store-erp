<!-- File: /home/ubuntu/clean_project/frontend/pages/data/ActivityLog.vue -->
<template>
  <div class="activity-log-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="fas fa-history"></i>
          سجل الأنشطة
        </h1>
        <p class="page-description">
          عرض وتتبع جميع أنشطة المستخدمين والنظام
        </p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="refreshLogs">
          <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
          تحديث
        </button>
        <button class="btn btn-outline-primary" @click="exportLogs">
          <i class="fas fa-download"></i>
          تصدير السجل
        </button>
        <button class="btn btn-outline-danger" @click="clearLogs">
          <i class="fas fa-trash"></i>
          مسح السجل
        </button>
      </div>
    </div>

    <!-- Filters and Statistics -->
    <div class="filters-section">
      <div class="stats-cards">
        <div class="stat-card">
          <div class="stat-icon success">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-info">
            <h3>{{ statistics.successful }}</h3>
            <p>عمليات ناجحة</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon warning">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <div class="stat-info">
            <h3>{{ statistics.warnings }}</h3>
            <p>تحذيرات</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon error">
            <i class="fas fa-times-circle"></i>
          </div>
          <div class="stat-info">
            <h3>{{ statistics.errors }}</h3>
            <p>أخطاء</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon info">
            <i class="fas fa-info-circle"></i>
          </div>
          <div class="stat-info">
            <h3>{{ statistics.total }}</h3>
            <p>إجمالي الأنشطة</p>
          </div>
        </div>
      </div>

      <div class="filter-controls">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input 
            type="text" 
            placeholder="البحث في الأنشطة..." 
            v-model="searchQuery"
            @input="filterLogs"
          >
        </div>
        
        <select v-model="selectedLevel" @change="filterLogs" class="filter-select">
          <option value="">جميع المستويات</option>
          <option value="info">معلومات</option>
          <option value="success">نجح</option>
          <option value="warning">تحذير</option>
          <option value="error">خطأ</option>
        </select>
        
        <select v-model="selectedAction" @change="filterLogs" class="filter-select">
          <option value="">جميع الإجراءات</option>
          <option value="login">تسجيل دخول</option>
          <option value="logout">تسجيل خروج</option>
          <option value="diagnosis">تشخيص</option>
          <option value="user_management">إدارة المستخدمين</option>
          <option value="settings">الإعدادات</option>
          <option value="ai_training">تدريب الذكاء الاصطناعي</option>
        </select>
        
        <select v-model="selectedUser" @change="filterLogs" class="filter-select">
          <option value="">جميع المستخدمين</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.name }}
          </option>
        </select>
        
        <div class="date-range">
          <input 
            type="date" 
            v-model="dateFrom" 
            @change="filterLogs"
            class="date-input"
          >
          <span>إلى</span>
          <input 
            type="date" 
            v-model="dateTo" 
            @change="filterLogs"
            class="date-input"
          >
        </div>
        
        <button class="btn btn-outline-secondary" @click="resetFilters">
          <i class="fas fa-undo"></i>
          إعادة تعيين
        </button>
      </div>
    </div>

    <!-- Activity Timeline -->
    <div class="timeline-section">
      <div class="section-header">
        <h2>الأنشطة الحديثة</h2>
        <div class="timeline-controls">
          <button 
            class="btn btn-sm"
            :class="viewMode === 'timeline' ? 'btn-primary' : 'btn-outline-primary'"
            @click="viewMode = 'timeline'"
          >
            <i class="fas fa-stream"></i>
            عرض زمني
          </button>
          <button 
            class="btn btn-sm"
            :class="viewMode === 'table' ? 'btn-primary' : 'btn-outline-primary'"
            @click="viewMode = 'table'"
          >
            <i class="fas fa-table"></i>
            عرض جدولي
          </button>
        </div>
      </div>

      <!-- Timeline View -->
      <div v-if="viewMode === 'timeline'" class="timeline-container">
        <div class="timeline">
          <div 
            v-for="log in paginatedLogs" 
            :key="log.id"
            class="timeline-item"
            :class="log.level"
          >
            <div class="timeline-marker">
              <i :class="getActionIcon(log.action)"></i>
            </div>
            <div class="timeline-content">
              <div class="timeline-header">
                <h4>{{ getActionName(log.action) }}</h4>
                <span class="timeline-time">{{ formatTime(log.timestamp) }}</span>
              </div>
              <div class="timeline-body">
                <p>{{ log.description }}</p>
                <div class="timeline-meta">
                  <span class="user-info">
                    <i class="fas fa-user"></i>
                    {{ getUserName(log.userId) }}
                  </span>
                  <span class="ip-info">
                    <i class="fas fa-globe"></i>
                    {{ log.ipAddress }}
                  </span>
                  <span v-if="log.userAgent" class="device-info">
                    <i class="fas fa-desktop"></i>
                    {{ getDeviceType(log.userAgent) }}
                  </span>
                </div>
                <div v-if="log.details" class="timeline-details">
                  <button 
                    class="btn btn-sm btn-outline-info"
                    @click="toggleDetails(log.id)"
                  >
                    <i class="fas fa-info-circle"></i>
                    {{ expandedLogs.includes(log.id) ? 'إخفاء التفاصيل' : 'عرض التفاصيل' }}
                  </button>
                  <div v-if="expandedLogs.includes(log.id)" class="details-content">
                    <pre>{{ JSON.stringify(log.details, null, 2) }}</pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Table View -->
      <div v-if="viewMode === 'table'" class="table-container">
        <div class="table-responsive">
          <table class="logs-table">
            <thead>
              <tr>
                <th @click="sortBy('timestamp')" class="sortable">
                  الوقت
                  <i :class="getSortIcon('timestamp')"></i>
                </th>
                <th @click="sortBy('level')" class="sortable">
                  المستوى
                  <i :class="getSortIcon('level')"></i>
                </th>
                <th @click="sortBy('action')" class="sortable">
                  الإجراء
                  <i :class="getSortIcon('action')"></i>
                </th>
                <th @click="sortBy('userId')" class="sortable">
                  المستخدم
                  <i :class="getSortIcon('userId')"></i>
                </th>
                <th>الوصف</th>
                <th>عنوان IP</th>
                <th>الجهاز</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in paginatedLogs" :key="log.id" :class="log.level">
                <td>
                  <span class="timestamp">{{ formatTime(log.timestamp) }}</span>
                </td>
                <td>
                  <span :class="['level-badge', log.level]">
                    {{ getLevelName(log.level) }}
                  </span>
                </td>
                <td>
                  <div class="action-cell">
                    <i :class="getActionIcon(log.action)"></i>
                    {{ getActionName(log.action) }}
                  </div>
                </td>
                <td>
                  <div class="user-cell">
                    <div class="user-avatar">
                      {{ getUserName(log.userId).charAt(0) }}
                    </div>
                    {{ getUserName(log.userId) }}
                  </div>
                </td>
                <td>
                  <span class="description">{{ log.description }}</span>
                </td>
                <td>
                  <span class="ip-address">{{ log.ipAddress }}</span>
                </td>
                <td>
                  <span class="device-type">{{ getDeviceType(log.userAgent) }}</span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button 
                      class="btn-icon btn-info" 
                      @click="viewLogDetails(log)"
                      title="عرض التفاصيل"
                    >
                      <i class="fas fa-eye"></i>
                    </button>
                    <button 
                      class="btn-icon btn-danger" 
                      @click="deleteLog(log)"
                      title="حذف"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div class="pagination-container">
        <div class="pagination-info">
          عرض {{ (currentPage - 1) * itemsPerPage + 1 }} إلى {{ Math.min(currentPage * itemsPerPage, filteredLogs.length) }} من {{ filteredLogs.length }} نشاط
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

    <!-- Log Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click="showDetailsModal = false">
      <div class="modal-content large-modal" @click.stop>
        <div class="modal-header">
          <h3>تفاصيل النشاط</h3>
          <button class="modal-close" @click="showDetailsModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="selectedLog" class="log-details">
            <div class="detail-grid">
              <div class="detail-item">
                <label>الوقت:</label>
                <span>{{ formatTime(selectedLog.timestamp) }}</span>
              </div>
              <div class="detail-item">
                <label>المستوى:</label>
                <span :class="['level-badge', selectedLog.level]">
                  {{ getLevelName(selectedLog.level) }}
                </span>
              </div>
              <div class="detail-item">
                <label>الإجراء:</label>
                <span>{{ getActionName(selectedLog.action) }}</span>
              </div>
              <div class="detail-item">
                <label>المستخدم:</label>
                <span>{{ getUserName(selectedLog.userId) }}</span>
              </div>
              <div class="detail-item">
                <label>عنوان IP:</label>
                <span>{{ selectedLog.ipAddress }}</span>
              </div>
              <div class="detail-item">
                <label>نوع الجهاز:</label>
                <span>{{ getDeviceType(selectedLog.userAgent) }}</span>
              </div>
            </div>
            
            <div class="description-section">
              <h4>الوصف:</h4>
              <p>{{ selectedLog.description }}</p>
            </div>
            
            <div v-if="selectedLog.userAgent" class="user-agent-section">
              <h4>معلومات المتصفح:</h4>
              <p class="user-agent">{{ selectedLog.userAgent }}</p>
            </div>
            
            <div v-if="selectedLog.details" class="details-section">
              <h4>التفاصيل الإضافية:</h4>
              <pre class="details-json">{{ JSON.stringify(selectedLog.details, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActivityLog',
  data() {
    return {
      loading: false,
      viewMode: 'timeline', // timeline or table
      searchQuery: '',
      selectedLevel: '',
      selectedAction: '',
      selectedUser: '',
      dateFrom: '',
      dateTo: '',
      sortField: 'timestamp',
      sortDirection: 'desc',
      currentPage: 1,
      itemsPerPage: 20,
      expandedLogs: [],
      showDetailsModal: false,
      selectedLog: null,
      
      logs: [],
      filteredLogs: [],
      users: [],
      
      statistics: {
        total: 0,
        successful: 0,
        warnings: 0,
        errors: 0
      }
    }
  },
  
  computed: {
    paginatedLogs() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredLogs.slice(start, end)
    },
    
    totalPages() {
      return Math.ceil(this.filteredLogs.length / this.itemsPerPage)
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
    this.loadLogs()
    this.loadUsers()
    this.setDefaultDateRange()
  },
  
  methods: {
    async loadLogs() {
      this.loading = true
      
      try {
        // محاكاة تحميل البيانات من الخادم
        const response = await fetch('/api/activity-logs')
        if (response.ok) {
          this.logs = await response.json()
        } else {
          // بيانات تجريبية
          this.logs = this.generateMockLogs()
        }
        
        this.filteredLogs = [...this.logs]
        this.calculateStatistics()
        this.sortLogs()
      } catch (error) {
        console.error('خطأ في تحميل السجلات:', error)
        this.logs = this.generateMockLogs()
        this.filteredLogs = [...this.logs]
        this.calculateStatistics()
      } finally {
        this.loading = false
      }
    },
    
    async loadUsers() {
      try {
        const response = await fetch('/api/users')
        if (response.ok) {
          this.users = await response.json()
        } else {
          // بيانات تجريبية
          this.users = [
            { id: 1, name: 'أحمد محمد' },
            { id: 2, name: 'فاطمة علي' },
            { id: 3, name: 'محمد السعيد' },
            { id: 4, name: 'سارة أحمد' }
          ]
        }
      } catch (error) {
        console.error('خطأ في تحميل المستخدمين:', error)
      }
    },
    
    generateMockLogs() {
      const actions = ['login', 'logout', 'diagnosis', 'user_management', 'settings', 'ai_training']
      const levels = ['info', 'success', 'warning', 'error']
      const descriptions = {
        login: 'تم تسجيل الدخول بنجاح',
        logout: 'تم تسجيل الخروج',
        diagnosis: 'تم إجراء تشخيص جديد',
        user_management: 'تم تعديل بيانات المستخدم',
        settings: 'تم تحديث الإعدادات',
        ai_training: 'تم بدء تدريب نموذج جديد'
      }
      
      const logs = []
      for (let i = 1; i <= 100; i++) {
        const action = actions[Math.floor(Math.random() * actions.length)]
        const level = levels[Math.floor(Math.random() * levels.length)]
        const userId = Math.floor(Math.random() * 4) + 1
        
        logs.push({
          id: i,
          timestamp: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000),
          level: level,
          action: action,
          userId: userId,
          description: descriptions[action],
          ipAddress: `192.168.1.${Math.floor(Math.random() * 255)}`,
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          details: {
            sessionId: `session_${i}`,
            duration: Math.floor(Math.random() * 3600),
            success: Math.random() > 0.2
          }
        })
      }
      
      return logs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    },
    
    setDefaultDateRange() {
      const today = new Date()
      const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)
      
      this.dateTo = today.toISOString().split('T')[0]
      this.dateFrom = weekAgo.toISOString().split('T')[0]
    },
    
    filterLogs() {
      this.filteredLogs = this.logs.filter(log => {
        const matchesSearch = !this.searchQuery || 
          log.description.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          this.getUserName(log.userId).toLowerCase().includes(this.searchQuery.toLowerCase())
        
        const matchesLevel = !this.selectedLevel || log.level === this.selectedLevel
        const matchesAction = !this.selectedAction || log.action === this.selectedAction
        const matchesUser = !this.selectedUser || log.userId.toString() === this.selectedUser
        
        const logDate = new Date(log.timestamp).toISOString().split('T')[0]
        const matchesDateFrom = !this.dateFrom || logDate >= this.dateFrom
        const matchesDateTo = !this.dateTo || logDate <= this.dateTo
        
        return matchesSearch && matchesLevel && matchesAction && matchesUser && matchesDateFrom && matchesDateTo
      })
      
      this.calculateStatistics()
      this.sortLogs()
      this.currentPage = 1
    },
    
    resetFilters() {
      this.searchQuery = ''
      this.selectedLevel = ''
      this.selectedAction = ''
      this.selectedUser = ''
      this.setDefaultDateRange()
      this.filteredLogs = [...this.logs]
      this.calculateStatistics()
      this.currentPage = 1
    },
    
    sortBy(field) {
      if (this.sortField === field) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortDirection = 'desc'
      }
      this.sortLogs()
    },
    
    sortLogs() {
      this.filteredLogs.sort((a, b) => {
        let aVal = a[this.sortField]
        let bVal = b[this.sortField]
        
        if (this.sortField === 'timestamp') {
          aVal = new Date(aVal)
          bVal = new Date(bVal)
        } else if (this.sortField === 'userId') {
          aVal = this.getUserName(aVal)
          bVal = this.getUserName(bVal)
        } else if (typeof aVal === 'string') {
          aVal = aVal.toLowerCase()
          bVal = bVal.toLowerCase()
        }
        
        if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1
        if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1
        return 0
      })
    },
    
    calculateStatistics() {
      this.statistics.total = this.filteredLogs.length
      this.statistics.successful = this.filteredLogs.filter(log => 
        log.level === 'success' || log.level === 'info').length
      this.statistics.warnings = this.filteredLogs.filter(log => 
        log.level === 'warning').length
      this.statistics.errors = this.filteredLogs.filter(log => 
        log.level === 'error').length
    },
    
    toggleDetails(logId) {
      const index = this.expandedLogs.indexOf(logId)
      if (index > -1) {
        this.expandedLogs.splice(index, 1)
      } else {
        this.expandedLogs.push(logId)
      }
    },
    
    viewLogDetails(log) {
      this.selectedLog = log
      this.showDetailsModal = true
    },
    
    async deleteLog(log) {
      if (confirm(`هل أنت متأكد من حذف هذا النشاط؟`)) {
        try {
          const response = await fetch(`/api/activity-logs/${log.id}`, {
            method: 'DELETE'
          })
          
          if (response.ok) {
            this.logs = this.logs.filter(l => l.id !== log.id)
            this.filterLogs()
            this.$toast.success('تم حذف النشاط بنجاح')
          } else {
            throw new Error('فشل في حذف النشاط')
          }
        } catch (error) {
          console.error('خطأ في حذف النشاط:', error)
          this.$toast.error('فشل في حذف النشاط')
        }
      }
    },
    
    async refreshLogs() {
      await this.loadLogs()
      this.$toast.success('تم تحديث السجلات بنجاح')
    },
    
    async exportLogs() {
      try {
        const exportData = this.filteredLogs.map(log => ({
          الوقت: this.formatTime(log.timestamp),
          المستوى: this.getLevelName(log.level),
          الإجراء: this.getActionName(log.action),
          المستخدم: this.getUserName(log.userId),
          الوصف: log.description,
          'عنوان IP': log.ipAddress,
          الجهاز: this.getDeviceType(log.userAgent)
        }))
        
        const csv = this.convertToCSV(exportData)
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `activity_log_${new Date().toISOString().split('T')[0]}.csv`
        a.click()
        window.URL.revokeObjectURL(url)
        
        this.$toast.success('تم تصدير السجل بنجاح')
      } catch (error) {
        console.error('خطأ في تصدير السجل:', error)
        this.$toast.error('فشل في تصدير السجل')
      }
    },
    
    async clearLogs() {
      if (confirm('هل أنت متأكد من مسح جميع السجلات؟ هذا الإجراء لا يمكن التراجع عنه.')) {
        try {
          const response = await fetch('/api/activity-logs', {
            method: 'DELETE'
          })
          
          if (response.ok) {
            this.logs = []
            this.filteredLogs = []
            this.calculateStatistics()
            this.$toast.success('تم مسح جميع السجلات بنجاح')
          } else {
            throw new Error('فشل في مسح السجلات')
          }
        } catch (error) {
          console.error('خطأ في مسح السجلات:', error)
          this.$toast.error('فشل في مسح السجلات')
        }
      }
    },
    
    convertToCSV(data) {
      if (!data.length) return ''
      
      const headers = Object.keys(data[0])
      const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => `"${row[header]}"`).join(','))
      ].join('\n')
      
      return '\uFEFF' + csvContent // Add BOM for UTF-8
    },
    
    getSortIcon(field) {
      if (this.sortField !== field) return 'fas fa-sort'
      return this.sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down'
    },
    
    getActionIcon(action) {
      const icons = {
        login: 'fas fa-sign-in-alt',
        logout: 'fas fa-sign-out-alt',
        diagnosis: 'fas fa-stethoscope',
        user_management: 'fas fa-users-cog',
        settings: 'fas fa-cog',
        ai_training: 'fas fa-brain'
      }
      return icons[action] || 'fas fa-circle'
    },
    
    getActionName(action) {
      const names = {
        login: 'تسجيل دخول',
        logout: 'تسجيل خروج',
        diagnosis: 'تشخيص',
        user_management: 'إدارة المستخدمين',
        settings: 'الإعدادات',
        ai_training: 'تدريب الذكاء الاصطناعي'
      }
      return names[action] || action
    },
    
    getLevelName(level) {
      const names = {
        info: 'معلومات',
        success: 'نجح',
        warning: 'تحذير',
        error: 'خطأ'
      }
      return names[level] || level
    },
    
    getUserName(userId) {
      const user = this.users.find(u => u.id === userId)
      return user ? user.name : `مستخدم ${userId}`
    },
    
    getDeviceType(userAgent) {
      if (!userAgent) return 'غير محدد'
      
      if (userAgent.includes('Mobile')) return 'هاتف محمول'
      if (userAgent.includes('Tablet')) return 'جهاز لوحي'
      return 'حاسوب مكتبي'
    },
    
    formatTime(date) {
      return new Date(date).toLocaleString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.activity-log-page {
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
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  overflow: hidden;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
}

.stat-card {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-right: 1px solid #e9ecef;
}

.stat-card:last-child {
  border-right: none;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-icon.success {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.stat-icon.warning {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
}

.stat-icon.error {
  background: linear-gradient(135deg, #dc3545, #e83e8c);
}

.stat-icon.info {
  background: linear-gradient(135deg, #007bff, #6f42c1);
}

.stat-info h3 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #333;
}

.stat-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.filter-controls {
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 250px;
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

.filter-select,
.date-input {
  padding: 0.5rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  min-width: 120px;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.timeline-section {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.section-header h2 {
  margin: 0;
  color: #2E7D32;
  font-size: 1.5rem;
}

.timeline-controls {
  display: flex;
  gap: 0.5rem;
}

.timeline-container {
  padding: 2rem;
}

.timeline {
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  right: 2rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, #2E7D32, #4CAF50);
}

.timeline-item {
  position: relative;
  margin-bottom: 2rem;
  padding-right: 5rem;
}

.timeline-marker {
  position: absolute;
  right: 1.25rem;
  top: 0.5rem;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: white;
  border: 3px solid #2E7D32;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  color: #2E7D32;
  z-index: 2;
}

.timeline-item.warning .timeline-marker {
  border-color: #ffc107;
  color: #ffc107;
}

.timeline-item.error .timeline-marker {
  border-color: #dc3545;
  color: #dc3545;
}

.timeline-content {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 1.5rem;
  border-left: 4px solid #2E7D32;
}

.timeline-item.warning .timeline-content {
  border-left-color: #ffc107;
}

.timeline-item.error .timeline-content {
  border-left-color: #dc3545;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.timeline-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
}

.timeline-time {
  color: #666;
  font-size: 0.9rem;
}

.timeline-body p {
  margin: 0 0 1rem 0;
  color: #555;
}

.timeline-meta {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.timeline-meta span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.timeline-meta i {
  color: #2E7D32;
}

.timeline-details {
  margin-top: 1rem;
}

.details-content {
  margin-top: 1rem;
  background: white;
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #e9ecef;
}

.details-content pre {
  margin: 0;
  font-size: 0.85rem;
  color: #333;
  white-space: pre-wrap;
  word-break: break-word;
}

.table-container {
  padding: 1rem;
}

.table-responsive {
  overflow-x: auto;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
}

.logs-table th,
.logs-table td {
  padding: 1rem;
  text-align: right;
  border-bottom: 1px solid #f0f0f0;
}

.logs-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #333;
  position: sticky;
  top: 0;
  z-index: 10;
}

.logs-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.3s ease;
}

.logs-table th.sortable:hover {
  background: #e9ecef;
}

.logs-table tr:hover {
  background: #f8f9fa;
}

.logs-table tr.warning {
  background: rgba(255, 193, 7, 0.05);
}

.logs-table tr.error {
  background: rgba(220, 53, 69, 0.05);
}

.timestamp {
  font-size: 0.9rem;
  color: #666;
}

.level-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.level-badge.info,
.level-badge.success {
  background: #d4edda;
  color: #155724;
}

.level-badge.warning {
  background: #fff3cd;
  color: #856404;
}

.level-badge.error {
  background: #f8d7da;
  color: #721c24;
}

.action-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.8rem;
}

.description {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ip-address {
  font-family: monospace;
  font-size: 0.9rem;
  color: #666;
}

.device-type {
  font-size: 0.9rem;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn-icon {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 6px;
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

.btn-info { background: #17a2b8; }
.btn-danger { background: #dc3545; }

.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
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

.btn-outline-info {
  background: transparent;
  color: #17a2b8;
  border: 2px solid #17a2b8;
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
  border-bottom: 1px solid #e9ecef;
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

.log-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
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

.description-section,
.user-agent-section,
.details-section {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.description-section h4,
.user-agent-section h4,
.details-section h4 {
  margin: 0 0 0.5rem 0;
  color: #2E7D32;
  font-size: 1rem;
}

.user-agent {
  font-family: monospace;
  font-size: 0.85rem;
  color: #666;
  word-break: break-all;
}

.details-json {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 1rem;
  font-size: 0.85rem;
  color: #333;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1200px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .activity-log-page {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .timeline::before {
    right: 1rem;
  }
  
  .timeline-item {
    padding-right: 3rem;
  }
  
  .timeline-marker {
    right: 0.75rem;
  }
  
  .timeline-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .logs-table {
    font-size: 0.85rem;
  }
  
  .logs-table th,
  .logs-table td {
    padding: 0.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .pagination-container {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>

