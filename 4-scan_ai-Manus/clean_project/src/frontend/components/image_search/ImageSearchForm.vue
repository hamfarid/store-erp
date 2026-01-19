<template>
  <div class="search-form-container">
    <!-- بطاقة البحث عن الصور -->
    <div class="search-card">
      <div class="card-header">
        <h2>{{ $t('image_search.search_title') }}</h2>
      </div>
      <div class="card-body">
        <div class="search-form">
          <div class="form-group">
            <label for="search-query">{{ $t('image_search.search_query') }}</label>
            <input 
              type="text" 
              id="search-query" 
              v-model="searchQuery" 
              :placeholder="$t('image_search.query_placeholder')" 
              class="form-control"
              aria-label="Search query"
            />
          </div>
          
          <div class="form-group">
            <label for="search-count">{{ $t('image_search.count_label') }}</label>
            <input 
              type="number" 
              id="search-count" 
              v-model="searchCount" 
              min="1" 
              max="100" 
              class="form-control"
              aria-label="Number of results"
            />
          </div>
          
          <div class="form-group">
            <label for="advanced-options">{{ $t('image_search.advanced_options') }}</label>
            <div id="advanced-options" class="advanced-options" role="group">
              <div class="option-group">
                <label for="safe-search">{{ $t('image_search.safe_search') }}</label>
                <select id="safe-search" v-model="searchParams.safeSearch" class="form-control" aria-label="Safe search level">
                  <option value="off">{{ $t('image_search.safe_search_off') }}</option>
                  <option value="medium">{{ $t('image_search.safe_search_medium') }}</option>
                  <option value="high">{{ $t('image_search.safe_search_high') }}</option>
                </select>
              </div>
              
              <div class="option-group">
                <label for="image-size">{{ $t('image_search.image_size') }}</label>
                <select id="image-size" v-model="searchParams.imageSize" class="form-control" aria-label="Image size">
                  <option value="small">{{ $t('image_search.image_size_small') }}</option>
                  <option value="medium">{{ $t('image_search.image_size_medium') }}</option>
                  <option value="large">{{ $t('image_search.image_size_large') }}</option>
                  <option value="xlarge">{{ $t('image_search.image_size_xlarge') }}</option>
                </select>
              </div>
              
              <div class="option-group">
                <label for="image-type">{{ $t('image_search.image_type') }}</label>
                <select id="image-type" v-model="searchParams.imageType" class="form-control" aria-label="Image type">
                  <option value="photo">{{ $t('image_search.image_type_photo') }}</option>
                  <option value="clipart">{{ $t('image_search.image_type_clipart') }}</option>
                  <option value="lineart">{{ $t('image_search.image_type_lineart') }}</option>
                  <option value="face">{{ $t('image_search.image_type_face') }}</option>
                </select>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button 
              @click="searchImages" 
              class="btn btn-primary" 
              :disabled="isLoading"
            >
              <span v-if="isLoading">
                <i class="fas fa-spinner fa-spin"></i> {{ $t('image_search.searching') }}
              </span>
              <span v-else>
                <i class="fas fa-search"></i> {{ $t('image_search.search_button') }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- بطاقة البحث المتقدم -->
    <div class="advanced-search-card">
      <div class="card-header">
        <h2>{{ $t('image_search.advanced_search_title') }}</h2>
      </div>
      <div class="card-body">
        <div class="search-tabs" role="tablist">
          <div 
            class="tab" 
            :class="{ active: activeTab === 'disease' }" 
            @click="activeTab = 'disease'"
            role="tab"
            :aria-selected="activeTab === 'disease'"
            aria-controls="disease-tab-panel"
            tabindex="0"
          >
            {{ $t('image_search.disease_tab') }}
          </div>
          <div 
            class="tab" 
            :class="{ active: activeTab === 'pest' }" 
            @click="activeTab = 'pest'"
            role="tab"
            :aria-selected="activeTab === 'pest'"
            aria-controls="pest-tab-panel"
            tabindex="0"
          >
            {{ $t('image_search.pest_tab') }}
          </div>
          <div 
            class="tab" 
            :class="{ active: activeTab === 'crop' }" 
            @click="activeTab = 'crop'"
            role="tab"
            :aria-selected="activeTab === 'crop'"
            aria-controls="crop-tab-panel"
            tabindex="0"
          >
            {{ $t('image_search.crop_tab') }}
          </div>
        </div>
        
        <div class="tab-content">
          <!-- بحث المرض -->
          <div v-if="activeTab === 'disease'" class="tab-pane" role="tabpanel" id="disease-tab-panel">
            <div class="form-group">
              <label for="disease-select">{{ $t('image_search.select_disease') }}</label>
              <select 
                id="disease-select" 
                v-model="selectedDiseaseId" 
                class="form-control"
                aria-label="Select disease"
              >
                <option value="">{{ $t('image_search.select_disease_placeholder') }}</option>
                <option 
                  v-for="disease in diseases" 
                  :key="disease.id" 
                  :value="disease.id"
                >
                  {{ disease.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="disease-count">{{ $t('image_search.count_label') }}</label>
              <input 
                type="number" 
                id="disease-count" 
                v-model="diseaseSearchCount" 
                min="1" 
                max="100" 
                class="form-control"
                aria-label="Number of disease results"
              />
            </div>
            
            <div class="form-actions">
              <button 
                @click="searchDiseaseImages" 
                class="btn btn-primary" 
                :disabled="isLoading || !selectedDiseaseId"
                aria-label="Search disease images"
              >
                <span v-if="isLoading">
                  <i class="fas fa-spinner fa-spin"></i> {{ $t('image_search.searching') }}
                </span>
                <span v-else>
                  <i class="fas fa-search"></i> {{ $t('image_search.search_button') }}
                </span>
              </button>
            </div>
          </div>
          
          <!-- بحث الآفة -->
          <div v-if="activeTab === 'pest'" class="tab-pane" role="tabpanel" id="pest-tab-panel">
            <div class="form-group">
              <label for="pest-select">{{ $t('image_search.select_pest') }}</label>
              <select 
                id="pest-select" 
                v-model="selectedPestId" 
                class="form-control"
                aria-label="Select pest"
              >
                <option value="">{{ $t('image_search.select_pest_placeholder') }}</option>
                <option 
                  v-for="pest in pests" 
                  :key="pest.id" 
                  :value="pest.id"
                >
                  {{ pest.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="pest-count">{{ $t('image_search.count_label') }}</label>
              <input 
                type="number" 
                id="pest-count" 
                v-model="pestSearchCount" 
                min="1" 
                max="100" 
                class="form-control"
                aria-label="Number of pest results"
              />
            </div>
            
            <div class="form-actions">
              <button 
                @click="searchPestImages" 
                class="btn btn-primary" 
                :disabled="isLoading || !selectedPestId"
                aria-label="Search pest images"
              >
                <span v-if="isLoading">
                  <i class="fas fa-spinner fa-spin"></i> {{ $t('image_search.searching') }}
                </span>
                <span v-else>
                  <i class="fas fa-search"></i> {{ $t('image_search.search_button') }}
                </span>
              </button>
            </div>
          </div>
          
          <!-- بحث المحصول -->
          <div v-if="activeTab === 'crop'" class="tab-pane" role="tabpanel" id="crop-tab-panel">
            <div class="form-group">
              <label for="crop-select">{{ $t('image_search.select_crop') }}</label>
              <select 
                id="crop-select" 
                v-model="selectedCropId" 
                class="form-control"
                aria-label="Select crop"
              >
                <option value="">{{ $t('image_search.select_crop_placeholder') }}</option>
                <option 
                  v-for="crop in crops" 
                  :key="crop.id" 
                  :value="crop.id"
                >
                  {{ crop.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="crop-condition">{{ $t('image_search.crop_condition') }}</label>
              <select 
                id="crop-condition" 
                v-model="cropCondition" 
                class="form-control"
              >
                <option value="">{{ $t('image_search.any_condition') }}</option>
                <option value="healthy">{{ $t('image_search.healthy_condition') }}</option>
                <option value="diseased">{{ $t('image_search.diseased_condition') }}</option>
                <option value="damaged">{{ $t('image_search.damaged_condition') }}</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="crop-count">{{ $t('image_search.count_label') }}</label>
              <input 
                type="number" 
                id="crop-count" 
                v-model="cropSearchCount" 
                min="1" 
                max="100" 
                class="form-control"
              />
            </div>
            
            <div class="form-actions">
              <button 
                @click="searchCropImages" 
                class="btn btn-primary" 
                :disabled="isLoading || !selectedCropId"
              >
                <span v-if="isLoading">
                  <i class="fas fa-spinner fa-spin"></i> {{ $t('image_search.searching') }}
                </span>
                <span v-else>
                  <i class="fas fa-search"></i> {{ $t('image_search.search_button') }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';

/**
 * @component ImageSearchForm
 * @description مكون نموذج البحث عن الصور الذي يتيح للمستخدمين البحث عن الصور باستخدام استعلامات نصية أو معايير متقدمة
 */
export default {
  name: 'ImageSearchForm',
  
  /**
   * @emits search-images - ينبعث عند إجراء بحث عام عن الصور
   * @emits search-disease-images - ينبعث عند إجراء بحث عن صور الأمراض
   * @emits search-pest-images - ينبعث عند إجراء بحث عن صور الآفات
   * @emits search-crop-images - ينبعث عند إجراء بحث عن صور المحاصيل
   */
  emits: ['search-images', 'search-disease-images', 'search-pest-images', 'search-crop-images'],
  
  setup(props, { emit }) {
    const { t } = useI18n();
    const toast = useToast();
    
    // حالة البحث
    const searchQuery = ref('');
    const searchCount = ref(10);
    const searchParams = reactive({
      safeSearch: 'medium',
      imageSize: 'medium',
      imageType: 'photo'
    });
    
    // حالة البحث المتقدم
    const activeTab = ref('disease');
    const selectedDiseaseId = ref('');
    const selectedPestId = ref('');
    const selectedCropId = ref('');
    const cropCondition = ref('');
    const diseaseSearchCount = ref(10);
    const pestSearchCount = ref(10);
    const cropSearchCount = ref(10);
    
    // البيانات المرجعية
    const diseases = ref([]);
    const pests = ref([]);
    const crops = ref([]);
    
    // حالة التحميل
    const isLoading = ref(false);
    
    /**
     * جلب البيانات المرجعية عند تحميل المكون
     */
    onMounted(async () => {
      try {
        // جلب الأمراض
        const diseasesResponse = await fetch('/api/diseases');
        if (diseasesResponse.ok) {
          diseases.value = await diseasesResponse.json();
        }
        
        // جلب الآفات
        const pestsResponse = await fetch('/api/pests');
        if (pestsResponse.ok) {
          pests.value = await pestsResponse.json();
        }
        
        // جلب المحاصيل
        const cropsResponse = await fetch('/api/crops');
        if (cropsResponse.ok) {
          crops.value = await cropsResponse.json();
        }
      } catch (error) {
        console.error('Error fetching reference data:', error);
        toast.error(t('image_search.error_loading_data'));
      }
    });
    
    /**
     * البحث العام عن الصور
     * @emits search-images - ينبعث مع معلمات البحث
     */
    const searchImages = () => {
      if (!searchQuery.value.trim()) {
        toast.warning(t('image_search.empty_query'));
        return;
      }
      
      isLoading.value = true;
      
      // إرسال حدث البحث إلى المكون الأب
      emit('search-images', {
        query: searchQuery.value,
        count: searchCount.value,
        search_params: searchParams
      });
    };
    
    /**
     * البحث عن صور المرض
     * @emits search-disease-images - ينبعث مع معرف المرض وعدد النتائج المطلوبة
     */
    const searchDiseaseImages = () => {
      if (!selectedDiseaseId.value) {
        toast.warning(t('image_search.select_disease_warning'));
        return;
      }
      
      isLoading.value = true;
      
      // إرسال حدث البحث إلى المكون الأب
      emit('search-disease-images', {
        disease_id: selectedDiseaseId.value,
        count: diseaseSearchCount.value
      });
    };
    
    /**
     * البحث عن صور الآفة
     * @emits search-pest-images - ينبعث مع معرف الآفة وعدد النتائج المطلوبة
     */
    const searchPestImages = () => {
      if (!selectedPestId.value) {
        toast.warning(t('image_search.select_pest_warning'));
        return;
      }
      
      isLoading.value = true;
      
      // إرسال حدث البحث إلى المكون الأب
      emit('search-pest-images', {
        pest_id: selectedPestId.value,
        count: pestSearchCount.value
      });
    };
    
    /**
     * البحث عن صور المحصول
     * @emits search-crop-images - ينبعث مع معرف المحصول وحالة المحصول وعدد النتائج المطلوبة
     */
    const searchCropImages = () => {
      if (!selectedCropId.value) {
        toast.warning(t('image_search.select_crop_warning'));
        return;
      }
      
      isLoading.value = true;
      
      // إرسال حدث البحث إلى المكون الأب
      emit('search-crop-images', {
        crop_id: selectedCropId.value,
        condition: cropCondition.value || null,
        count: cropSearchCount.value
      });
    };
    
    /**
     * تعيين حالة التحميل
     * @param {boolean} loading - حالة التحميل الجديدة
     */
    const setLoading = (loading) => {
      isLoading.value = loading;
    };
    
    return {
      // حالة البحث
      searchQuery,
      searchCount,
      searchParams,
      
      // حالة البحث المتقدم
      activeTab,
      selectedDiseaseId,
      selectedPestId,
      selectedCropId,
      cropCondition,
      diseaseSearchCount,
      pestSearchCount,
      cropSearchCount,
      
      // البيانات المرجعية
      diseases,
      pests,
      crops,
      
      // حالة التحميل
      isLoading,
      setLoading,
      
      // وظائف البحث
      searchImages,
      searchDiseaseImages,
      searchPestImages,
      searchCropImages
    };
  }
};
</script>

<style scoped>
.search-form-container {
  margin-bottom: 20px;
}

.search-card,
.advanced-search-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  overflow: hidden;
}

.card-header {
  background-color: #f8f9fa;
  padding: 15px 20px;
  border-bottom: 1px solid #e9ecef;
}

.card-header h2 {
  margin: 0;
  font-size: 18px;
  color: #495057;
}

.card-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #495057;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.advanced-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 10px;
}

.form-actions {
  margin-top: 20px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #4caf50;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #43a047;
}

.btn-primary:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.search-tabs {
  display: flex;
  border-bottom: 1px solid #e9ecef;
  margin-bottom: 15px;
}

.tab {
  padding: 10px 20px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.tab:hover {
  background-color: #f8f9fa;
}

.tab.active {
  border-bottom-color: #4caf50;
  color: #4caf50;
  font-weight: 500;
}

.tab-pane {
  padding: 10px 0;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .advanced-options {
    grid-template-columns: 1fr;
  }
}
</style>
