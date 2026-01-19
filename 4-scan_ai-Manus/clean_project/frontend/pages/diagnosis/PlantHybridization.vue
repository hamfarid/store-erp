<!-- صفحة تهجين النباتات -->
<template>
  <div class="plant-hybridization-page">
    <!-- Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fas fa-seedling me-3"></i>
            تهجين النباتات
          </h1>
          <p class="page-subtitle">محاكاة وتخطيط عمليات تهجين النباتات باستخدام الذكاء الاصطناعي</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-outline-info" @click="showHybridizationGuide">
            <i class="fas fa-book me-2"></i>
            دليل التهجين
          </button>
          <button class="btn btn-primary" @click="startNewHybridization">
            <i class="fas fa-plus me-2"></i>
            تهجين جديد
          </button>
        </div>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card primary">
          <div class="stat-icon">
            <i class="fas fa-dna"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ hybridizationStats.total_simulations || 0 }}</div>
            <div class="stat-label">محاكاة التهجين</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card success">
          <div class="stat-icon">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ hybridizationStats.successful_crosses || 0 }}</div>
            <div class="stat-label">تهجينات ناجحة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card info">
          <div class="stat-icon">
            <i class="fas fa-leaf"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ hybridizationStats.plant_varieties || 0 }}</div>
            <div class="stat-label">أصناف النباتات</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card warning">
          <div class="stat-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ hybridizationStats.success_rate || 0 }}%</div>
            <div class="stat-label">معدل النجاح</div>
          </div>
        </div>
      </div>
    </div>

    <!-- أداة التهجين الرئيسية -->
    <div class="row mb-4">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-flask me-2"></i>
              محاكي التهجين
            </h5>
          </div>
          <div class="card-body">
            <div class="hybridization-workspace">
              <!-- اختيار النباتات الأبوية -->
              <div class="parent-selection">
                <div class="row">
                  <div class="col-md-6">
                    <div class="parent-plant" :class="{ selected: selectedParent1 }">
                      <h6>النبات الأبوي الأول (♂)</h6>
                      <div class="plant-selector" @click="selectParent(1)">
                        <div v-if="selectedParent1" class="selected-plant">
                          <img :src="selectedParent1.image" :alt="selectedParent1.name" class="plant-image">
                          <div class="plant-info">
                            <div class="plant-name">{{ selectedParent1.name }}</div>
                            <div class="plant-variety">{{ selectedParent1.variety }}</div>
                          </div>
                        </div>
                        <div v-else class="plant-placeholder">
                          <i class="fas fa-plus-circle"></i>
                          <span>اختر النبات الأبوي الأول</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="col-md-6">
                    <div class="parent-plant" :class="{ selected: selectedParent2 }">
                      <h6>النبات الأبوي الثاني (♀)</h6>
                      <div class="plant-selector" @click="selectParent(2)">
                        <div v-if="selectedParent2" class="selected-plant">
                          <img :src="selectedParent2.image" :alt="selectedParent2.name" class="plant-image">
                          <div class="plant-info">
                            <div class="plant-name">{{ selectedParent2.name }}</div>
                            <div class="plant-variety">{{ selectedParent2.variety }}</div>
                          </div>
                        </div>
                        <div v-else class="plant-placeholder">
                          <i class="fas fa-plus-circle"></i>
                          <span>اختر النبات الأبوي الثاني</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- رمز التهجين -->
              <div class="hybridization-symbol" v-if="selectedParent1 && selectedParent2">
                <i class="fas fa-times"></i>
                <span>تهجين</span>
              </div>
              
              <!-- نتائج التهجين المتوقعة -->
              <div class="hybridization-results" v-if="hybridizationResult">
                <h6>النتائج المتوقعة</h6>
                <div class="offspring-grid">
                  <div class="offspring-item" v-for="offspring in hybridizationResult.offspring" :key="offspring.id">
                    <div class="offspring-image">
                      <img :src="offspring.predicted_image" :alt="offspring.name">
                    </div>
                    <div class="offspring-info">
                      <div class="offspring-name">{{ offspring.name }}</div>
                      <div class="offspring-probability">احتمالية: {{ offspring.probability }}%</div>
                      <div class="offspring-traits">
                        <span v-for="trait in offspring.traits" :key="trait" class="trait-badge">
                          {{ trait }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- أزرار التحكم -->
              <div class="hybridization-controls">
                <button class="btn btn-success btn-lg" 
                        @click="simulateHybridization"
                        :disabled="!canSimulate || isSimulating">
                  <i v-if="isSimulating" class="fas fa-spinner fa-spin me-2"></i>
                  <i v-else class="fas fa-play me-2"></i>
                  {{ isSimulating ? 'جاري المحاكاة...' : 'بدء المحاكاة' }}
                </button>
                
                <button class="btn btn-outline-secondary" @click="clearSelection">
                  <i class="fas fa-undo me-2"></i>
                  إعادة تعيين
                </button>
                
                <button class="btn btn-outline-info" @click="saveHybridization" v-if="hybridizationResult">
                  <i class="fas fa-save me-2"></i>
                  حفظ النتائج
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-cogs me-2"></i>
              إعدادات التهجين
            </h5>
          </div>
          <div class="card-body">
            <div class="setting-item">
              <label class="form-label">نوع التهجين</label>
              <select class="form-select" v-model="hybridizationSettings.type">
                <option value="simple">تهجين بسيط</option>
                <option value="backcross">تهجين عكسي</option>
                <option value="multiple">تهجين متعدد</option>
                <option value="advanced">تهجين متقدم</option>
              </select>
            </div>
            
            <div class="setting-item">
              <label class="form-label">عدد الأجيال</label>
              <input type="number" 
                     class="form-control" 
                     v-model="hybridizationSettings.generations"
                     min="1" 
                     max="10">
            </div>
            
            <div class="setting-item">
              <label class="form-label">حجم العينة</label>
              <select class="form-select" v-model="hybridizationSettings.sample_size">
                <option value="small">صغير (100 نبات)</option>
                <option value="medium">متوسط (500 نبات)</option>
                <option value="large">كبير (1000 نبات)</option>
                <option value="custom">مخصص</option>
              </select>
            </div>
            
            <div class="setting-item" v-if="hybridizationSettings.sample_size === 'custom'">
              <label class="form-label">عدد النباتات</label>
              <input type="number" 
                     class="form-control" 
                     v-model="hybridizationSettings.custom_size"
                     min="10" 
                     max="10000">
            </div>
            
            <div class="setting-item">
              <label class="form-label">الصفات المستهدفة</label>
              <div class="traits-selection">
                <div class="form-check" v-for="trait in availableTraits" :key="trait.id">
                  <input class="form-check-input" 
                         type="checkbox" 
                         :value="trait.id"
                         v-model="hybridizationSettings.target_traits">
                  <label class="form-check-label">{{ trait.name }}</label>
                </div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="hybridizationSettings.include_genetics">
                <label class="form-check-label">تضمين التحليل الوراثي</label>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="hybridizationSettings.environmental_factors">
                <label class="form-check-label">مراعاة العوامل البيئية</label>
              </div>
            </div>
          </div>
        </div>
        
        <!-- مكتبة النباتات -->
        <div class="card mt-3">
          <div class="card-header">
            <h6 class="card-title mb-0">
              <i class="fas fa-leaf me-2"></i>
              مكتبة النباتات
            </h6>
          </div>
          <div class="card-body">
            <div class="search-plants">
              <input type="text" 
                     class="form-control" 
                     placeholder="البحث في النباتات..."
                     v-model="plantSearchQuery">
            </div>
            
            <div class="plants-list">
              <div class="plant-item" 
                   v-for="plant in filteredPlants" 
                   :key="plant.id"
                   @click="selectPlantFromLibrary(plant)">
                <img :src="plant.thumbnail" :alt="plant.name" class="plant-thumbnail">
                <div class="plant-details">
                  <div class="plant-name">{{ plant.name }}</div>
                  <div class="plant-variety">{{ plant.variety }}</div>
                  <div class="plant-traits">
                    <span v-for="trait in plant.main_traits" :key="trait" class="trait-tag">
                      {{ trait }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- سجل التهجينات -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-history me-2"></i>
                سجل التهجينات
              </h5>
              <div class="card-actions">
                <button class="btn btn-sm btn-outline-primary" @click="refreshHistory">
                  <i class="fas fa-sync-alt"></i>
                </button>
                <button class="btn btn-sm btn-outline-success" @click="exportHistory">
                  <i class="fas fa-download"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>التاريخ</th>
                    <th>النبات الأبوي الأول</th>
                    <th>النبات الأبوي الثاني</th>
                    <th>نوع التهجين</th>
                    <th>عدد النتائج</th>
                    <th>معدل النجاح</th>
                    <th>الحالة</th>
                    <th>الإجراءات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="record in hybridizationHistory" :key="record.id">
                    <td>{{ formatDate(record.created_at) }}</td>
                    <td>
                      <div class="d-flex align-items-center">
                        <img :src="record.parent1.thumbnail" :alt="record.parent1.name" class="table-plant-image me-2">
                        {{ record.parent1.name }}
                      </div>
                    </td>
                    <td>
                      <div class="d-flex align-items-center">
                        <img :src="record.parent2.thumbnail" :alt="record.parent2.name" class="table-plant-image me-2">
                        {{ record.parent2.name }}
                      </div>
                    </td>
                    <td>{{ getHybridizationTypeText(record.type) }}</td>
                    <td>{{ record.offspring_count }}</td>
                    <td>
                      <span class="badge" :class="getSuccessRateClass(record.success_rate)">
                        {{ record.success_rate }}%
                      </span>
                    </td>
                    <td>
                      <span class="badge" :class="getStatusClass(record.status)">
                        {{ getStatusText(record.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-info" @click="viewHybridization(record)">
                          <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-outline-primary" @click="downloadReport(record)">
                          <i class="fas fa-download"></i>
                        </button>
                        <button class="btn btn-outline-success" @click="repeatHybridization(record)">
                          <i class="fas fa-redo"></i>
                        </button>
                        <button class="btn btn-outline-danger" @click="deleteHybridization(record)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة اختيار النبات -->
    <div class="modal fade" id="plantSelectionModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">اختيار النبات الأبوي</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-4" v-for="plant in availablePlants" :key="plant.id">
                <div class="plant-card" @click="confirmPlantSelection(plant)">
                  <img :src="plant.image" :alt="plant.name" class="plant-card-image">
                  <div class="plant-card-body">
                    <h6>{{ plant.name }}</h6>
                    <p>{{ plant.variety }}</p>
                    <div class="plant-traits">
                      <span v-for="trait in plant.traits" :key="trait" class="trait-badge">
                        {{ trait }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePlantHybridizationStore, useSystemStore } from '../../store/index.js'
import { plantHybridizationAPI } from '../../services/api.js'

export default {
  name: 'PlantHybridization',
  
  setup() {
    const router = useRouter()
    const plantHybridizationStore = usePlantHybridizationStore()
    const systemStore = useSystemStore()
    
    const selectedParent1 = ref(null)
    const selectedParent2 = ref(null)
    const currentParentSelection = ref(null)
    const isSimulating = ref(false)
    const plantSearchQuery = ref('')
    
    const hybridizationSettings = ref({
      type: 'simple',
      generations: 1,
      sample_size: 'medium',
      custom_size: 500,
      target_traits: [],
      include_genetics: true,
      environmental_factors: false
    })
    
    const availableTraits = ref([
      { id: 1, name: 'مقاومة الأمراض' },
      { id: 2, name: 'زيادة الإنتاج' },
      { id: 3, name: 'تحسين الجودة' },
      { id: 4, name: 'مقاومة الجفاف' },
      { id: 5, name: 'النضج المبكر' },
      { id: 6, name: 'تحسين الطعم' },
      { id: 7, name: 'زيادة الحجم' },
      { id: 8, name: 'مقاومة الحشرات' }
    ])
    
    // البيانات المحسوبة
    const hybridizationStats = computed(() => plantHybridizationStore.stats)
    const hybridizationResult = computed(() => plantHybridizationStore.currentResult)
    const hybridizationHistory = computed(() => plantHybridizationStore.history)
    const availablePlants = computed(() => plantHybridizationStore.plants)
    
    const filteredPlants = computed(() => {
      if (!plantSearchQuery.value) return availablePlants.value
      
      return availablePlants.value.filter(plant => 
        plant.name.toLowerCase().includes(plantSearchQuery.value.toLowerCase()) ||
        plant.variety.toLowerCase().includes(plantSearchQuery.value.toLowerCase())
      )
    })
    
    const canSimulate = computed(() => {
      return selectedParent1.value && selectedParent2.value && !isSimulating.value
    })
    
    // الوظائف
    const startNewHybridization = () => {
      clearSelection()
      plantHybridizationStore.clearCurrentResult()
    }
    
    const selectParent = (parentNumber) => {
      currentParentSelection.value = parentNumber
      const modal = new bootstrap.Modal(document.getElementById('plantSelectionModal'))
      modal.show()
    }
    
    const confirmPlantSelection = (plant) => {
      if (currentParentSelection.value === 1) {
        selectedParent1.value = plant
      } else {
        selectedParent2.value = plant
      }
      
      const modal = bootstrap.Modal.getInstance(document.getElementById('plantSelectionModal'))
      modal.hide()
      
      currentParentSelection.value = null
    }
    
    const selectPlantFromLibrary = (plant) => {
      if (!selectedParent1.value) {
        selectedParent1.value = plant
      } else if (!selectedParent2.value) {
        selectedParent2.value = plant
      } else {
        systemStore.addNotification({
          type: 'info',
          title: 'تم اختيار النباتات',
          message: 'تم اختيار النباتات الأبوية بالفعل'
        })
      }
    }
    
    const clearSelection = () => {
      selectedParent1.value = null
      selectedParent2.value = null
      plantHybridizationStore.clearCurrentResult()
    }
    
    const simulateHybridization = async () => {
      if (!canSimulate.value) return
      
      isSimulating.value = true
      
      try {
        const simulationData = {
          parent1_id: selectedParent1.value.id,
          parent2_id: selectedParent2.value.id,
          settings: hybridizationSettings.value
        }
        
        const result = await plantHybridizationAPI.simulateHybridization(simulationData)
        plantHybridizationStore.setCurrentResult(result.data)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تمت المحاكاة',
          message: 'تم إجراء محاكاة التهجين بنجاح'
        })
        
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في المحاكاة',
          message: 'فشل في إجراء محاكاة التهجين'
        })
      } finally {
        isSimulating.value = false
      }
    }
    
    const saveHybridization = async () => {
      try {
        await plantHybridizationAPI.saveHybridization({
          parent1: selectedParent1.value,
          parent2: selectedParent2.value,
          result: hybridizationResult.value,
          settings: hybridizationSettings.value
        })
        
        await plantHybridizationStore.fetchHistory()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم الحفظ',
          message: 'تم حفظ نتائج التهجين بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الحفظ',
          message: 'فشل في حفظ النتائج'
        })
      }
    }
    
    const showHybridizationGuide = () => {
      systemStore.addNotification({
        type: 'info',
        title: 'دليل التهجين',
        message: 'سيتم فتح دليل التهجين قريباً'
      })
    }
    
    const getHybridizationTypeText = (type) => {
      const types = {
        'simple': 'تهجين بسيط',
        'backcross': 'تهجين عكسي',
        'multiple': 'تهجين متعدد',
        'advanced': 'تهجين متقدم'
      }
      return types[type] || 'غير معروف'
    }
    
    const getSuccessRateClass = (rate) => {
      if (rate >= 80) return 'bg-success'
      if (rate >= 60) return 'bg-warning'
      return 'bg-danger'
    }
    
    const getStatusClass = (status) => {
      const classes = {
        'completed': 'bg-success',
        'in_progress': 'bg-info',
        'failed': 'bg-danger',
        'pending': 'bg-warning'
      }
      return classes[status] || 'bg-secondary'
    }
    
    const getStatusText = (status) => {
      const texts = {
        'completed': 'مكتمل',
        'in_progress': 'قيد التنفيذ',
        'failed': 'فشل',
        'pending': 'قيد الانتظار'
      }
      return texts[status] || 'غير معروف'
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const refreshHistory = async () => {
      await plantHybridizationStore.fetchHistory()
    }
    
    const exportHistory = async () => {
      try {
        const response = await plantHybridizationAPI.exportHistory()
        
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `hybridization-history-${new Date().toISOString().split('T')[0]}.xlsx`
        link.click()
        window.URL.revokeObjectURL(url)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التصدير',
          message: 'تم تصدير سجل التهجينات بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التصدير',
          message: 'فشل في تصدير السجل'
        })
      }
    }
    
    const viewHybridization = (record) => {
      // عرض تفاصيل التهجين
      router.push(`/diagnosis/plant-hybridization/${record.id}`)
    }
    
    const downloadReport = async (record) => {
      try {
        const response = await plantHybridizationAPI.downloadReport(record.id)
        
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `hybridization-report-${record.id}.pdf`
        link.click()
        window.URL.revokeObjectURL(url)
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التحميل',
          message: 'فشل في تحميل التقرير'
        })
      }
    }
    
    const repeatHybridization = (record) => {
      selectedParent1.value = record.parent1
      selectedParent2.value = record.parent2
      hybridizationSettings.value = { ...hybridizationSettings.value, ...record.settings }
      
      systemStore.addNotification({
        type: 'info',
        title: 'تم التحميل',
        message: 'تم تحميل إعدادات التهجين السابق'
      })
    }
    
    const deleteHybridization = async (record) => {
      if (confirm(`هل أنت متأكد من حذف سجل التهجين؟`)) {
        try {
          await plantHybridizationAPI.deleteHybridization(record.id)
          await plantHybridizationStore.fetchHistory()
          
          systemStore.addNotification({
            type: 'success',
            title: 'تم الحذف',
            message: 'تم حذف سجل التهجين بنجاح'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ في الحذف',
            message: 'فشل في حذف السجل'
          })
        }
      }
    }
    
    // تحميل البيانات عند التحميل
    onMounted(async () => {
      await plantHybridizationStore.fetchStats()
      await plantHybridizationStore.fetchHistory()
      await plantHybridizationStore.fetchPlants()
    })
    
    return {
      selectedParent1,
      selectedParent2,
      isSimulating,
      plantSearchQuery,
      hybridizationSettings,
      availableTraits,
      hybridizationStats,
      hybridizationResult,
      hybridizationHistory,
      availablePlants,
      filteredPlants,
      canSimulate,
      startNewHybridization,
      selectParent,
      confirmPlantSelection,
      selectPlantFromLibrary,
      clearSelection,
      simulateHybridization,
      saveHybridization,
      showHybridizationGuide,
      getHybridizationTypeText,
      getSuccessRateClass,
      getStatusClass,
      getStatusText,
      formatDate,
      refreshHistory,
      exportHistory,
      viewHybridization,
      downloadReport,
      repeatHybridization,
      deleteHybridization
    }
  }
}
</script>

<style scoped>
.plant-hybridization-page {
  padding: 20px;
  font-family: 'Cairo', sans-serif;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6c757d;
  margin-bottom: 0;
}

.stat-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card.primary {
  border-left-color: #4e73df;
}

.stat-card.success {
  border-left-color: #1cc88a;
}

.stat-card.info {
  border-left-color: #36b9cc;
}

.stat-card.warning {
  border-left-color: #f6c23e;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 1rem;
  font-size: 1.5rem;
  color: white;
}

.stat-card.primary .stat-icon {
  background: linear-gradient(45deg, #4e73df, #224abe);
}

.stat-card.success .stat-icon {
  background: linear-gradient(45deg, #1cc88a, #13855c);
}

.stat-card.info .stat-icon {
  background: linear-gradient(45deg, #36b9cc, #258391);
}

.stat-card.warning .stat-icon {
  background: linear-gradient(45deg, #f6c23e, #d4a017);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.hybridization-workspace {
  padding: 2rem;
}

.parent-selection {
  margin-bottom: 2rem;
}

.parent-plant {
  text-align: center;
}

.parent-plant h6 {
  margin-bottom: 1rem;
  font-weight: 600;
  color: #2c3e50;
}

.plant-selector {
  border: 2px dashed #e3e6f0;
  border-radius: 15px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.plant-selector:hover {
  border-color: #4e73df;
  background: rgba(78, 115, 223, 0.05);
}

.parent-plant.selected .plant-selector {
  border-color: #1cc88a;
  background: rgba(28, 200, 138, 0.05);
}

.plant-placeholder {
  text-align: center;
  color: #6c757d;
}

.plant-placeholder i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #4e73df;
}

.selected-plant {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.plant-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.plant-info {
  text-align: center;
}

.plant-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.plant-variety {
  color: #6c757d;
  font-size: 0.9rem;
}

.hybridization-symbol {
  text-align: center;
  margin: 2rem 0;
  font-size: 2rem;
  color: #4e73df;
  font-weight: 600;
}

.hybridization-symbol i {
  margin-left: 1rem;
}

.hybridization-results {
  margin-bottom: 2rem;
}

.hybridization-results h6 {
  margin-bottom: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e3e6f0;
  padding-bottom: 0.5rem;
}

.offspring-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.offspring-item {
  background: #f8f9fc;
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.3s ease;
}

.offspring-item:hover {
  transform: translateY(-5px);
}

.offspring-image img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.offspring-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.offspring-probability {
  color: #1cc88a;
  font-weight: 600;
  margin-bottom: 1rem;
}

.offspring-traits {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.trait-badge {
  background: #4e73df;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.hybridization-controls {
  text-align: center;
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.setting-item {
  margin-bottom: 1.5rem;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.traits-selection {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e3e6f0;
  border-radius: 8px;
  padding: 1rem;
}

.search-plants {
  margin-bottom: 1rem;
}

.plants-list {
  max-height: 400px;
  overflow-y: auto;
}

.plant-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.plant-item:hover {
  background: #f8f9fc;
  border-color: #e3e6f0;
}

.plant-thumbnail {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  margin-left: 1rem;
}

.plant-details {
  flex: 1;
}

.plant-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.plant-variety {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.trait-tag {
  background: #e3e6f0;
  color: #6c757d;
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  font-size: 0.7rem;
  margin-left: 0.25rem;
}

.table-plant-image {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
}

.plant-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
  margin-bottom: 1rem;
}

.plant-card:hover {
  transform: translateY(-5px);
}

.plant-card-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.plant-card-body {
  padding: 1rem;
}

.plant-card-body h6 {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.plant-card-body p {
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.plant-traits {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.card {
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: none;
}

.card-header {
  background: white;
  border-bottom: 1px solid #e3e6f0;
  border-radius: 15px 15px 0 0 !important;
}

.card-title {
  font-weight: 600;
  color: #2c3e50;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .page-header .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .hybridization-workspace {
    padding: 1rem;
  }
  
  .hybridization-controls {
    flex-direction: column;
  }
  
  .offspring-grid {
    grid-template-columns: 1fr;
  }
  
  .plant-item {
    flex-direction: column;
    text-align: center;
  }
  
  .plant-thumbnail {
    margin: 0 0 1rem 0;
  }
}
</style>

