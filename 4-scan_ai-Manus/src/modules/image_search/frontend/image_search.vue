# /home/ubuntu/image_search_integration/frontend/image_search.vue
<template>
  <div class="image-search-container">
    <h1 class="page-title">{{ $t('image_search.title') }}</h1>
    
    <!-- بطاقة البحث عن الصور -->
    <div class="search-card">
      <div class="card-header">
        <h2>{{ $t('image_search.search_title') }}</h2>
      </div>
      <div class="card-body">
        <div class="search-form">
          <div class="form-group">
            <label for="search-query">{{ $t('image_search.query_label') }}</label>
            <input 
              type="text" 
              id="search-query" 
              v-model="searchQuery" 
              :placeholder="$t('image_search.query_placeholder')" 
              class="form-control"
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
            />
          </div>
          
          <div class="form-group">
            <label>{{ $t('image_search.advanced_options') }}</label>
            <div class="advanced-options">
              <div class="option-group">
                <label for="safe-search">{{ $t('image_search.safe_search') }}</label>
                <select id="safe-search" v-model="searchParams.safeSearch" class="form-control">
                  <option value="off">{{ $t('image_search.safe_search_off') }}</option>
                  <option value="medium">{{ $t('image_search.safe_search_medium') }}</option>
                  <option value="high">{{ $t('image_search.safe_search_high') }}</option>
                </select>
              </div>
              
              <div class="option-group">
                <label for="image-size">{{ $t('image_search.image_size') }}</label>
                <select id="image-size" v-model="searchParams.imageSize" class="form-control">
                  <option value="small">{{ $t('image_search.image_size_small') }}</option>
                  <option value="medium">{{ $t('image_search.image_size_medium') }}</option>
                  <option value="large">{{ $t('image_search.image_size_large') }}</option>
                  <option value="xlarge">{{ $t('image_search.image_size_xlarge') }}</option>
                </select>
              </div>
              
              <div class="option-group">
                <label for="image-type">{{ $t('image_search.image_type') }}</label>
                <select id="image-type" v-model="searchParams.imageType" class="form-control">
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
        <div class="search-tabs">
          <div 
            class="tab" 
            :class="{ active: activeTab === 'disease' }" 
            @click="activeTab = 'disease'"
          >
            {{ $t('image_search.disease_tab') }}
          </div>
          <div 
            class="tab" 
            :class="{ active: activeTab === 'pest' }" 
            @click="activeTab = 'pest'"
          >
            {{ $t('image_search.pest_tab') }}
          </div>
          <div 
            class="tab" 
            :class="{ active: activeTab === 'crop' }" 
            @click="activeTab = 'crop'"
          >
            {{ $t('image_search.crop_tab') }}
          </div>
        </div>
        
        <div class="tab-content">
          <!-- بحث المرض -->
          <div v-if="activeTab === 'disease'" class="tab-pane">
            <div class="form-group">
              <label for="disease-select">{{ $t('image_search.select_disease') }}</label>
              <select 
                id="disease-select" 
                v-model="selectedDiseaseId" 
                class="form-control"
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
              />
            </div>
            
            <div class="form-actions">
              <button 
                @click="searchDiseaseImages" 
                class="btn btn-primary" 
                :disabled="isLoading || !selectedDiseaseId"
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
          <div v-if="activeTab === 'pest'" class="tab-pane">
            <div class="form-group">
              <label for="pest-select">{{ $t('image_search.select_pest') }}</label>
              <select 
                id="pest-select" 
                v-model="selectedPestId" 
                class="form-control"
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
              />
            </div>
            
            <div class="form-actions">
              <button 
                @click="searchPestImages" 
                class="btn btn-primary" 
                :disabled="isLoading || !selectedPestId"
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
          <div v-if="activeTab === 'crop'" class="tab-pane">
            <div class="form-group">
              <label for="crop-select">{{ $t('image_search.select_crop') }}</label>
              <select 
                id="crop-select" 
                v-model="selectedCropId" 
                class="form-control"
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
    
    <!-- نتائج البحث -->
    <div v-if="searchResults.length > 0" class="search-results">
      <h2>{{ $t('image_search.results_title') }} ({{ searchResults.length }})</h2>
      
      <div class="results-actions">
        <button 
          @click="collectSelectedImages" 
          class="btn btn-success" 
          :disabled="selectedImages.length === 0"
        >
          <i class="fas fa-download"></i> 
          {{ $t('image_search.collect_selected', { count: selectedImages.length }) }}
        </button>
        
        <button 
          @click="selectAllImages" 
          class="btn btn-outline-primary"
        >
          <i class="fas fa-check-square"></i> 
          {{ $t('image_search.select_all') }}
        </button>
        
        <button 
          @click="deselectAllImages" 
          class="btn btn-outline-secondary"
          :disabled="selectedImages.length === 0"
        >
          <i class="fas fa-square"></i> 
          {{ $t('image_search.deselect_all') }}
        </button>
      </div>
      
      <div class="image-grid">
        <div 
          v-for="(image, index) in searchResults" 
          :key="index" 
          class="image-item"
          :class="{ selected: isImageSelected(image) }"
          @click="toggleImageSelection(image)"
        >
          <div class="image-wrapper">
            <img :src="image" :alt="'Search result ' + (index + 1)" />
            <div class="image-overlay">
              <div class="checkbox">
                <i 
                  :class="[
                    'fas', 
                    isImageSelected(image) ? 'fa-check-square' : 'fa-square'
                  ]"
                ></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- رسالة عدم وجود نتائج -->
    <div v-else-if="hasSearched" class="no-results">
      <div class="alert alert-info">
        <i class="fas fa-info-circle"></i>
        {{ $t('image_search.no_results') }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';

export default {
  name: 'ImageSearch',
  
  setup() {
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
    
    // نتائج البحث
    const searchResults = ref([]);
    const selectedImages = ref([]);
    const isLoading = ref(false);
    const hasSearched = ref(false);
    
    // جلب البيانات المرجعية
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
    
    // البحث العام عن الصور
    const searchImages = async () => {
      if (!searchQuery.value.trim()) {
        toast.warning(t('image_search.empty_query'));
        return;
      }
      
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            query: searchQuery.value,
            count: searchCount.value,
            search_params: searchParams
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          searchResults.value = data.image_urls;
          hasSearched.value = true;
          
          if (data.image_urls.length === 0) {
            toast.info(t('image_search.no_results_found'));
          } else {
            toast.success(t('image_search.search_success', { count: data.image_urls.length }));
          }
        } else {
          const error = await response.json();
          toast.error(t('image_search.search_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error searching images:', error);
        toast.error(t('image_search.search_error', { message: error.message }));
      } finally {
        isLoading.value = false;
      }
    };
    
    // البحث عن صور المرض
    const searchDiseaseImages = async () => {
      if (!selectedDiseaseId.value) {
        toast.warning(t('image_search.select_disease_warning'));
        return;
      }
      
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/search/disease', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            disease_id: selectedDiseaseId.value,
            count: diseaseSearchCount.value
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          searchResults.value = data.image_urls;
          hasSearched.value = true;
          
          if (data.image_urls.length === 0) {
            toast.info(t('image_search.no_results_found'));
          } else {
            toast.success(t('image_search.search_success', { count: data.image_urls.length }));
          }
        } else {
          const error = await response.json();
          toast.error(t('image_search.search_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error searching disease images:', error);
        toast.error(t('image_search.search_error', { message: error.message }));
      } finally {
        isLoading.value = false;
      }
    };
    
    // البحث عن صور الآفة
    const searchPestImages = async () => {
      if (!selectedPestId.value) {
        toast.warning(t('image_search.select_pest_warning'));
        return;
      }
      
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/search/pest', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            pest_id: selectedPestId.value,
            count: pestSearchCount.value
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          searchResults.value = data.image_urls;
          hasSearched.value = true;
          
          if (data.image_urls.length === 0) {
            toast.info(t('image_search.no_results_found'));
          } else {
            toast.success(t('image_search.search_success', { count: data.image_urls.length }));
          }
        } else {
          const error = await response.json();
          toast.error(t('image_search.search_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error searching pest images:', error);
        toast.error(t('image_search.search_error', { message: error.message }));
      } finally {
        isLoading.value = false;
      }
    };
    
    // البحث عن صور المحصول
    const searchCropImages = async () => {
      if (!selectedCropId.value) {
        toast.warning(t('image_search.select_crop_warning'));
        return;
      }
      
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/search/crop', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            crop_id: selectedCropId.value,
            condition: cropCondition.value || null,
            count: cropSearchCount.value
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          searchResults.value = data.image_urls;
          hasSearched.value = true;
          
          if (data.image_urls.length === 0) {
            toast.info(t('image_search.no_results_found'));
          } else {
            toast.success(t('image_search.search_success', { count: data.image_urls.length }));
          }
        } else {
          const error = await response.json();
          toast.error(t('image_search.search_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error searching crop images:', error);
        toast.error(t('image_search.search_error', { message: error.message }));
      } finally {
        isLoading.value = false;
      }
    };
    
    // إدارة تحديد الصور
    const isImageSelected = (image) => {
      return selectedImages.value.includes(image);
    };
    
    const toggleImageSelection = (image) => {
      if (isImageSelected(image)) {
        selectedImages.value = selectedImages.value.filter(img => img !== image);
      } else {
        selectedImages.value.push(image);
      }
    };
    
    const selectAllImages = () => {
      selectedImages.value = [...searchResults.value];
    };
    
    const deselectAllImages = () => {
      selectedImages.value = [];
    };
    
    // جمع الصور المحددة
    const collectSelectedImages = async () => {
      if (selectedImages.value.length === 0) {
        toast.warning(t('image_search.no_images_selected'));
        return;
      }
      
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/collect', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            keywords: [searchQuery.value || activeTab.value],
            image_urls: selectedImages.value
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          toast.success(t('image_search.collect_success', { count: data.total_collected }));
          
          // إعادة تعيين التحديد بعد الجمع
          selectedImages.value = [];
        } else {
          const error = await response.json();
          toast.error(t('image_search.collect_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error collecting images:', error);
        toast.error(t('image_search.collect_error', { message: error.message }));
      } finally {
        isLoading.value = false;
      }
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
      
      // نتائج البحث
      searchResults,
      selectedImages,
      isLoading,
      hasSearched,
      
      // وظائف البحث
      searchImages,
      searchDiseaseImages,
      searchPestImages,
      searchCropImages,
      
      // إدارة تحديد الصور
      isImageSelected,
      toggleImageSelection,
      selectAllImages,
      deselectAllImages,
      collectSelectedImages
    };
  }
};
</script>

<style scoped>
.image-search-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 20px;
  color: #2c3e50;
  font-size: 24px;
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

.search-results {
  margin-top: 30px;
}

.search-results h2 {
  margin-bottom: 15px;
  font-size: 20px;
  color: #2c3e50;
}

.results-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.btn-success {
  background-color: #2196f3;
  color: white;
  border: none;
}

.btn-success:hover {
  background-color: #1e88e5;
}

.btn-outline-primary {
  background-color: transparent;
  color: #4caf50;
  border: 1px solid #4caf50;
}

.btn-outline-primary:hover {
  background-color: #f1f8e9;
}

.btn-outline-secondary {
  background-color: transparent;
  color: #757575;
  border: 1px solid #757575;
}

.btn-outline-secondary:hover {
  background-color: #f5f5f5;
}

.btn-outline-secondary:disabled {
  color: #bdbdbd;
  border-color: #bdbdbd;
  cursor: not-allowed;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.image-item {
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.image-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.image-item.selected {
  box-shadow: 0 0 0 3px #4caf50;
}

.image-wrapper {
  position: relative;
  padding-top: 75%; /* 4:3 Aspect Ratio */
}

.image-wrapper img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  opacity: 0;
  transition: opacity 0.2s;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 10px;
}

.image-item:hover .image-overlay,
.image-item.selected .image-overlay {
  opacity: 1;
}

.checkbox {
  background-color: white;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4caf50;
}

.image-item:not(.selected) .checkbox {
  color: #757575;
}

.no-results {
  margin-top: 30px;
}

.alert {
  padding: 15px;
  border-radius: 4px;
}

.alert-info {
  background-color: #e3f2fd;
  color: #0d47a1;
  border: 1px solid #bbdefb;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .advanced-options {
    grid-template-columns: 1fr;
  }
  
  .image-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  
  .results-actions {
    flex-direction: column;
  }
}
</style>
