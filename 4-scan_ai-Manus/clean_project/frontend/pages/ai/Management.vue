<!-- صفحة إدارة الذكاء الاصطناعي -->
<template>
  <div class="ai-management-page">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fas fa-brain me-3"></i>
            إدارة الذكاء الاصطناعي
          </h1>
          <p class="page-subtitle">إدارة نماذج الذكاء الاصطناعي والمساعدين الأذكياء</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-primary" @click="showCreateModel">
            <i class="fas fa-plus me-2"></i>
            إضافة نموذج جديد
          </button>
        </div>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stat-card">
          <div class="stat-icon bg-primary">
            <i class="fas fa-robot"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ aiStats.total_models || 0 }}</div>
            <div class="stat-label">إجمالي النماذج</div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stat-card">
          <div class="stat-icon bg-success">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ aiStats.active_models || 0 }}</div>
            <div class="stat-label">النماذج النشطة</div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stat-card">
          <div class="stat-icon bg-info">
            <i class="fas fa-comments"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ aiStats.total_conversations || 0 }}</div>
            <div class="stat-label">المحادثات اليوم</div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stat-card">
          <div class="stat-icon bg-warning">
            <i class="fas fa-users"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ aiStats.active_users || 0 }}</div>
            <div class="stat-label">المستخدمين النشطين</div>
          </div>
        </div>
      </div>
    </div>

    <!-- قائمة النماذج -->
    <div class="card shadow">
      <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">
            <i class="fas fa-list me-2"></i>
            نماذج الذكاء الاصطناعي
          </h5>
          <div class="card-actions">
            <div class="input-group" style="width: 300px;">
              <input 
                type="text" 
                class="form-control" 
                placeholder="البحث في النماذج..."
                v-model="searchQuery"
                @input="filterModels"
              >
              <span class="input-group-text">
                <i class="fas fa-search"></i>
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>النموذج</th>
                <th>النوع</th>
                <th>الحالة</th>
                <th>الاستخدام</th>
                <th>آخر تحديث</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="model in filteredModels" :key="model.id">
                <td>
                  <div class="d-flex align-items-center">
                    <div class="model-icon me-3">
                      <i :class="getModelIcon(model.type)"></i>
                    </div>
                    <div>
                      <div class="model-name">{{ model.name }}</div>
                      <div class="model-description">{{ model.description }}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="badge" :class="getTypeBadgeClass(model.type)">
                    {{ getTypeLabel(model.type) }}
                  </span>
                </td>
                <td>
                  <span class="badge" :class="getStatusBadgeClass(model.status)">
                    <i class="fas fa-circle me-1"></i>
                    {{ getStatusLabel(model.status) }}
                  </span>
                </td>
                <td>
                  <div class="usage-info">
                    <div class="usage-number">{{ model.usage_count || 0 }}</div>
                    <div class="usage-label">استخدام</div>
                  </div>
                </td>
                <td>{{ formatDate(model.updated_at) }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button 
                      class="btn btn-sm btn-outline-primary"
                      @click="editModel(model)"
                      title="تعديل"
                    >
                      <i class="fas fa-edit"></i>
                    </button>
                    <button 
                      class="btn btn-sm btn-outline-info"
                      @click="testModel(model)"
                      title="اختبار"
                    >
                      <i class="fas fa-play"></i>
                    </button>
                    <button 
                      class="btn btn-sm btn-outline-success"
                      @click="viewStats(model)"
                      title="الإحصائيات"
                    >
                      <i class="fas fa-chart-bar"></i>
                    </button>
                    <button 
                      class="btn btn-sm btn-outline-danger"
                      @click="deleteModel(model)"
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
        
        <!-- Pagination -->
        <nav v-if="totalPages > 1">
          <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">السابق</a>
            </li>
            <li 
              class="page-item" 
              v-for="page in visiblePages" 
              :key="page"
              :class="{ active: page === currentPage }"
            >
              <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">التالي</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- نافذة إنشاء/تعديل النموذج -->
    <div class="modal fade" id="modelModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editingModel ? 'تعديل النموذج' : 'إضافة نموذج جديد' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveModel">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">اسم النموذج</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="modelForm.name"
                    required
                  >
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">نوع النموذج</label>
                  <select class="form-select" v-model="modelForm.type" required>
                    <option value="">اختر النوع</option>
                    <option value="chat">محادثة</option>
                    <option value="diagnosis">تشخيص</option>
                    <option value="analysis">تحليل</option>
                    <option value="classification">تصنيف</option>
                  </select>
                </div>
              </div>
              
              <div class="mb-3">
                <label class="form-label">الوصف</label>
                <textarea 
                  class="form-control" 
                  rows="3"
                  v-model="modelForm.description"
                ></textarea>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">الإصدار</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="modelForm.version"
                    placeholder="1.0.0"
                  >
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">الحالة</label>
                  <select class="form-select" v-model="modelForm.status">
                    <option value="active">نشط</option>
                    <option value="inactive">غير نشط</option>
                    <option value="training">قيد التدريب</option>
                    <option value="testing">قيد الاختبار</option>
                  </select>
                </div>
              </div>
              
              <div class="mb-3">
                <label class="form-label">إعدادات النموذج (JSON)</label>
                <textarea 
                  class="form-control" 
                  rows="5"
                  v-model="modelForm.config"
                  placeholder='{"temperature": 0.7, "max_tokens": 1000}'
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              إلغاء
            </button>
            <button type="button" class="btn btn-primary" @click="saveModel" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              {{ saving ? 'جاري الحفظ...' : 'حفظ' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useSystemStore } from '../../store/index.js'
import { aiAPI } from '../../services/api.js'

export default {
  name: 'AIManagement',
  
  setup() {
    const systemStore = useSystemStore()
    
    // البيانات التفاعلية
    const models = ref([])
    const aiStats = ref({})
    const searchQuery = ref('')
    const currentPage = ref(1)
    const itemsPerPage = 10
    const editingModel = ref(null)
    const saving = ref(false)
    
    const modelForm = reactive({
      name: '',
      type: '',
      description: '',
      version: '',
      status: 'active',
      config: ''
    })
    
    // البيانات المحسوبة
    const filteredModels = computed(() => {
      let filtered = models.value
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(model => 
          model.name.toLowerCase().includes(query) ||
          model.description.toLowerCase().includes(query) ||
          model.type.toLowerCase().includes(query)
        )
      }
      
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return filtered.slice(start, end)
    })
    
    const totalPages = computed(() => {
      return Math.ceil(models.value.length / itemsPerPage)
    })
    
    const visiblePages = computed(() => {
      const pages = []
      const start = Math.max(1, currentPage.value - 2)
      const end = Math.min(totalPages.value, currentPage.value + 2)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    })
    
    // الوظائف
    const loadModels = async () => {
      try {
        const response = await aiAPI.getModels()
        models.value = response.data
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ',
          message: 'فشل في تحميل النماذج'
        })
      }
    }
    
    const loadStats = async () => {
      try {
        const response = await aiAPI.getStats()
        aiStats.value = response.data
      } catch (error) {
        console.error('خطأ في تحميل الإحصائيات:', error)
      }
    }
    
    const showCreateModel = () => {
      editingModel.value = null
      resetForm()
      const modal = new bootstrap.Modal(document.getElementById('modelModal'))
      modal.show()
    }
    
    const editModel = (model) => {
      editingModel.value = model
      modelForm.name = model.name
      modelForm.type = model.type
      modelForm.description = model.description
      modelForm.version = model.version
      modelForm.status = model.status
      modelForm.config = JSON.stringify(model.config, null, 2)
      
      const modal = new bootstrap.Modal(document.getElementById('modelModal'))
      modal.show()
    }
    
    const saveModel = async () => {
      saving.value = true
      
      try {
        const data = {
          ...modelForm,
          config: modelForm.config ? JSON.parse(modelForm.config) : {}
        }
        
        if (editingModel.value) {
          await aiAPI.updateModel(editingModel.value.id, data)
          systemStore.addNotification({
            type: 'success',
            title: 'تم التحديث',
            message: 'تم تحديث النموذج بنجاح'
          })
        } else {
          await aiAPI.createModel(data)
          systemStore.addNotification({
            type: 'success',
            title: 'تم الإنشاء',
            message: 'تم إنشاء النموذج بنجاح'
          })
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('modelModal'))
        modal.hide()
        
        await loadModels()
        await loadStats()
        
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ',
          message: 'فشل في حفظ النموذج'
        })
      } finally {
        saving.value = false
      }
    }
    
    const deleteModel = async (model) => {
      if (!confirm(`هل أنت متأكد من حذف النموذج "${model.name}"؟`)) {
        return
      }
      
      try {
        await aiAPI.deleteModel(model.id)
        systemStore.addNotification({
          type: 'success',
          title: 'تم الحذف',
          message: 'تم حذف النموذج بنجاح'
        })
        
        await loadModels()
        await loadStats()
        
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ',
          message: 'فشل في حذف النموذج'
        })
      }
    }
    
    const testModel = (model) => {
      // فتح نافذة اختبار النموذج
      systemStore.addNotification({
        type: 'info',
        title: 'اختبار النموذج',
        message: `جاري فتح واجهة اختبار النموذج ${model.name}`
      })
    }
    
    const viewStats = (model) => {
      // عرض إحصائيات النموذج
      systemStore.addNotification({
        type: 'info',
        title: 'إحصائيات النموذج',
        message: `عرض إحصائيات النموذج ${model.name}`
      })
    }
    
    const resetForm = () => {
      modelForm.name = ''
      modelForm.type = ''
      modelForm.description = ''
      modelForm.version = ''
      modelForm.status = 'active'
      modelForm.config = ''
    }
    
    const filterModels = () => {
      currentPage.value = 1
    }
    
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
      }
    }
    
    const getModelIcon = (type) => {
      const icons = {
        'chat': 'fas fa-comments',
        'diagnosis': 'fas fa-stethoscope',
        'analysis': 'fas fa-chart-line',
        'classification': 'fas fa-tags'
      }
      return icons[type] || 'fas fa-robot'
    }
    
    const getTypeBadgeClass = (type) => {
      const classes = {
        'chat': 'bg-primary',
        'diagnosis': 'bg-success',
        'analysis': 'bg-info',
        'classification': 'bg-warning'
      }
      return classes[type] || 'bg-secondary'
    }
    
    const getTypeLabel = (type) => {
      const labels = {
        'chat': 'محادثة',
        'diagnosis': 'تشخيص',
        'analysis': 'تحليل',
        'classification': 'تصنيف'
      }
      return labels[type] || type
    }
    
    const getStatusBadgeClass = (status) => {
      const classes = {
        'active': 'bg-success',
        'inactive': 'bg-secondary',
        'training': 'bg-warning',
        'testing': 'bg-info'
      }
      return classes[status] || 'bg-secondary'
    }
    
    const getStatusLabel = (status) => {
      const labels = {
        'active': 'نشط',
        'inactive': 'غير نشط',
        'training': 'قيد التدريب',
        'testing': 'قيد الاختبار'
      }
      return labels[status] || status
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ar-SA')
    }
    
    // تحميل البيانات عند التحميل
    onMounted(() => {
      loadModels()
      loadStats()
    })
    
    return {
      models,
      aiStats,
      searchQuery,
      currentPage,
      filteredModels,
      totalPages,
      visiblePages,
      editingModel,
      saving,
      modelForm,
      showCreateModel,
      editModel,
      saveModel,
      deleteModel,
      testModel,
      viewStats,
      filterModels,
      changePage,
      getModelIcon,
      getTypeBadgeClass,
      getTypeLabel,
      getStatusBadgeClass,
      getStatusLabel,
      formatDate
    }
  }
}
</script>

<style scoped>
.ai-management-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-title {
  color: var(--magseeds-dark);
  font-weight: var(--font-weight-bold);
  margin-bottom: 5px;
}

.page-subtitle {
  color: var(--magseeds-secondary);
  margin-bottom: 0;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  margin-left: 15px;
}

.stat-number {
  font-size: 2rem;
  font-weight: var(--font-weight-bold);
  color: var(--magseeds-dark);
  line-height: 1;
}

.stat-label {
  color: var(--magseeds-secondary);
  font-size: 0.9rem;
}

.model-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: var(--magseeds-light);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--magseeds-primary);
}

.model-name {
  font-weight: var(--font-weight-medium);
  color: var(--magseeds-dark);
}

.model-description {
  font-size: 0.85rem;
  color: var(--magseeds-secondary);
}

.usage-info {
  text-align: center;
}

.usage-number {
  font-weight: var(--font-weight-bold);
  color: var(--magseeds-dark);
}

.usage-label {
  font-size: 0.75rem;
  color: var(--magseeds-secondary);
}

.btn-group .btn {
  margin: 0 2px;
}

.table th {
  border-top: none;
  font-weight: var(--font-weight-medium);
  color: var(--magseeds-dark);
}

.badge {
  font-size: 0.75rem;
}

.pagination .page-link {
  color: var(--magseeds-primary);
  border-color: #dee2e6;
}

.pagination .page-item.active .page-link {
  background-color: var(--magseeds-primary);
  border-color: var(--magseeds-primary);
}
</style>

