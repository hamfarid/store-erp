<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/ModelConfigurationPanel.vue
الوصف: مكون لوحة إعدادات نماذج تشخيص أمراض النباتات
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="model-configuration-panel">
    <div class="panel-header">
      <h2>إعدادات نماذج تشخيص أمراض النباتات</h2>
      <p class="description">إدارة وتكوين نماذج تشخيص أمراض النباتات المتاحة في النظام</p>
    </div>

    <div class="panel-content">
      <div class="tabs">
        <div 
          class="tab" 
          :class="{ active: activeTab === 'available' }" 
          @click="activeTab = 'available'"
        >
          النماذج المتاحة
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'add' }" 
          @click="activeTab = 'add'"
        >
          إضافة نموذج جديد
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'ensemble' }" 
          @click="activeTab = 'ensemble'"
        >
          إعدادات التجميع
        </div>
        <div 
          class="tab" 
          :class="{ active: activeTab === 'system' }" 
          @click="activeTab = 'system'"
        >
          حالة النظام
        </div>
      </div>

      <div class="tab-content">
        <!-- النماذج المتاحة -->
        <div v-if="activeTab === 'available'" class="available-models-tab">
          <div class="search-bar">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="ابحث عن نموذج..."
              aria-label="البحث عن نموذج"
              role="searchbox"
            />
            <select 
              v-model="typeFilter" 
              aria-label="تصفية حسب نوع النموذج"
            >
              <option value="all">جميع الأنواع</option>
              <option value="huggingface">Hugging Face</option>
              <option value="github">GitHub</option>
              <option value="docker">Docker</option>
            </select>
          </div>

          <div v-if="loading" class="loading-indicator">
            <div class="spinner"></div>
            <p>جاري تحميل النماذج المتاحة...</p>
          </div>

          <div v-else-if="filteredModels.length === 0" class="no-models">
            <p v-if="searchQuery || typeFilter">لا توجد نماذج تطابق معايير البحث.</p>
            <p v-else>لا توجد نماذج متاحة. يرجى إضافة نماذج جديدة.</p>
          </div>

          <div v-else class="models-list" role="list" aria-label="قائمة النماذج المتاحة">
            <div 
              v-for="model in filteredModels" 
              :key="model.id"
              class="model-item"
              role="listitem"
              :aria-label="`نموذج ${model.name}`"
            >
              <div class="model-info">
                <h3>{{ model.name }}</h3>
                <p>{{ model.description }}</p>
                <div class="model-meta">
                  <span class="model-type" :aria-label="`نوع النموذج: ${model.type}`">
                    <i class="fas" :class="getModelTypeIcon(model.type)"></i>
                    {{ model.type }}
                  </span>
                  <span class="model-status" :aria-label="`حالة النموذج: ${model.status}`">
                    <i class="fas fa-circle" :class="getStatusClass(model.status)"></i>
                    {{ model.status }}
                  </span>
                </div>
              </div>
              <div class="model-actions">
                <button 
                  @click="editModel(model)"
                  class="edit-btn"
                  :aria-label="`تعديل نموذج ${model.name}`"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  @click="deleteModel(model)"
                  class="delete-btn"
                  :aria-label="`حذف نموذج ${model.name}`"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- إضافة نموذج جديد -->
        <div v-if="activeTab === 'add'" class="add-model-tab">
          <div class="model-source-selector">
            <h3>اختر مصدر النموذج</h3>
            <div class="source-options">
              <div 
                class="source-option" 
                :class="{ selected: selectedSource === 'huggingface' }"
                @click="selectedSource = 'huggingface'"
              >
                <div class="source-icon">
                  <i class="fas fa-brain"></i>
                </div>
                <div class="source-info">
                  <h4>Hugging Face</h4>
                  <p>استخدام نموذج من منصة Hugging Face</p>
                </div>
              </div>
              
              <div 
                class="source-option" 
                :class="{ selected: selectedSource === 'github' }"
                @click="selectedSource = 'github'"
              >
                <div class="source-icon">
                  <i class="fab fa-github"></i>
                </div>
                <div class="source-info">
                  <h4>GitHub</h4>
                  <p>استخدام نموذج من مستودع GitHub</p>
                </div>
              </div>
              
              <div 
                class="source-option" 
                :class="{ selected: selectedSource === 'docker' }"
                @click="selectedSource = 'docker'"
              >
                <div class="source-icon">
                  <i class="fab fa-docker"></i>
                </div>
                <div class="source-info">
                  <h4>Docker</h4>
                  <p>استخدام نموذج من حاوية Docker</p>
                </div>
              </div>
            </div>
          </div>

          <div v-if="selectedSource" class="model-form">
            <h3>إضافة نموذج من {{ getSourceLabel(selectedSource) }}</h3>
            
            <div v-if="selectedSource === 'huggingface'" class="huggingface-form">
              <div class="form-group">
                <label for="hf-model-name">اسم النموذج في Hugging Face</label>
                <input 
                  id="hf-model-name"
                  type="text" 
                  v-model="newModel.huggingface.modelName" 
                  placeholder="مثال: username/model-name"
                />
                <small>أدخل اسم النموذج بالصيغة username/model-name</small>
              </div>
              
              <div class="form-group">
                <label for="hf-display-name">الاسم المعروض</label>
                <input 
                  id="hf-display-name"
                  type="text" 
                  v-model="newModel.huggingface.displayName" 
                  placeholder="الاسم الذي سيظهر في النظام"
                />
              </div>
              
              <div class="form-group">
                <label for="hf-description">الوصف</label>
                <textarea 
                  id="hf-description"
                  v-model="newModel.huggingface.description" 
                  placeholder="وصف النموذج وقدراته"
                ></textarea>
              </div>
            </div>
            
            <div v-if="selectedSource === 'github'" class="github-form">
              <div class="form-group">
                <label for="gh-repo-url">عنوان المستودع</label>
                <input 
                  id="gh-repo-url"
                  type="text" 
                  v-model="newModel.github.repoUrl" 
                  placeholder="مثال: https://github.com/username/repo"
                />
              </div>
              
              <div class="form-group">
                <label for="gh-repo-name">اسم المستودع</label>
                <input 
                  id="gh-repo-name"
                  type="text" 
                  v-model="newModel.github.repoName" 
                  placeholder="اسم المستودع"
                />
              </div>
              
              <div class="form-group">
                <label for="gh-model-path">مسار النموذج داخل المستودع</label>
                <input 
                  id="gh-model-path"
                  type="text" 
                  v-model="newModel.github.modelPath" 
                  placeholder="مثال: models/plant_disease"
                />
                <small>المسار النسبي للنموذج داخل المستودع</small>
              </div>
              
              <div class="form-group">
                <label for="gh-description">الوصف</label>
                <textarea 
                  id="gh-description"
                  v-model="newModel.github.description" 
                  placeholder="وصف النموذج وقدراته"
                ></textarea>
              </div>
            </div>
            
            <div v-if="selectedSource === 'docker'" class="docker-form">
              <div class="form-group">
                <label for="docker-image-name">اسم الصورة</label>
                <input 
                  id="docker-image-name"
                  type="text" 
                  v-model="newModel.docker.imageName" 
                  placeholder="مثال: username/model-image:tag"
                />
              </div>
              
              <div class="form-group">
                <label for="docker-display-name">الاسم المعروض</label>
                <input 
                  id="docker-display-name"
                  type="text" 
                  v-model="newModel.docker.displayName" 
                  placeholder="الاسم الذي سيظهر في النظام"
                />
              </div>
              
              <div class="form-group">
                <label for="docker-port">منفذ الخدمة</label>
                <input 
                  id="docker-port"
                  type="number" 
                  v-model="newModel.docker.port" 
                  placeholder="مثال: 8080"
                />
              </div>
              
              <div class="form-group">
                <label for="docker-api-path">مسار واجهة برمجة التطبيقات</label>
                <input 
                  id="docker-api-path"
                  type="text" 
                  v-model="newModel.docker.apiPath" 
                  placeholder="مثال: /api/predict"
                />
              </div>
              
              <div class="form-group">
                <label for="docker-description">الوصف</label>
                <textarea 
                  id="docker-description"
                  v-model="newModel.docker.description" 
                  placeholder="وصف النموذج وقدراته"
                ></textarea>
              </div>
            </div>
            
            <div class="form-actions">
              <button 
                class="primary-btn" 
                @click="addNewModel" 
                :disabled="!canAddModel"
              >
                <i class="fas fa-plus"></i> إضافة النموذج
              </button>
              <button 
                class="secondary-btn" 
                @click="resetNewModelForm"
              >
                <i class="fas fa-redo"></i> إعادة ضبط
              </button>
            </div>
          </div>
        </div>

        <!-- إعدادات التجميع -->
        <div v-if="activeTab === 'ensemble'" class="ensemble-tab">
          <div v-if="loading" class="loading-indicator">
            <div class="spinner"></div>
            <p>جاري تحميل إعدادات التجميع...</p>
          </div>

          <div v-else class="ensemble-settings">
            <div class="ensemble-header">
              <h3>إعدادات معالج التجميع (Ensemble)</h3>
              <p>معالج التجميع يجمع نتائج من عدة نماذج لتحسين دقة التشخيص</p>
            </div>

            <div class="ensemble-status">
              <div class="status-toggle">
                <label class="toggle-label" for="ensemble-enabled">
                  <span>تفعيل معالج التجميع</span>
                  <div class="toggle-switch">
                    <input 
                      id="ensemble-enabled"
                      type="checkbox" 
                      v-model="ensembleSettings.enabled"
                      @change="updateEnsembleSettings"
                    />
                    <span class="toggle-slider"></span>
                  </div>
                </label>
              </div>
            </div>

            <div v-if="ensembleSettings.enabled" class="ensemble-config">
              <div class="voting-method">
                <h4>طريقة التصويت</h4>
                <div class="radio-options">
                  <label class="radio-option" for="voting-weighted">
                    <input 
                      id="voting-weighted"
                      type="radio" 
                      v-model="ensembleSettings.votingMethod" 
                      value="weighted"
                      @change="updateEnsembleSettings"
                    />
                    <span>موزون (Weighted)</span>
                    <small>يأخذ في الاعتبار أوزان النماذج المختلفة</small>
                  </label>
                  <label class="radio-option" for="voting-majority">
                    <input 
                      id="voting-majority"
                      type="radio" 
                      v-model="ensembleSettings.votingMethod" 
                      value="majority"
                      @change="updateEnsembleSettings"
                    />
                    <span>أغلبية (Majority)</span>
                    <small>كل نموذج له صوت متساوٍ</small>
                  </label>
                  <label class="radio-option" for="voting-confidence">
                    <input 
                      id="voting-confidence"
                      type="radio" 
                      v-model="ensembleSettings.votingMethod" 
                      value="confidence"
                      @change="updateEnsembleSettings"
                    />
                    <span>ثقة (Confidence)</span>
                    <small>يختار النموذج ذو أعلى ثقة</small>
                  </label>
                </div>
              </div>

              <div class="model-weights">
                <h4>أوزان النماذج</h4>
                <p>اضبط أوزان النماذج المختلفة في معالج التجميع</p>

                <div class="weights-list">
                  <div 
                    v-for="model in availableModels.filter(m => m.id !== 'ensemble')" 
                    :key="model.id"
                    class="weight-item"
                  >
                    <div class="weight-info">
                      <div class="weight-name">{{ model.name }}</div>
                      <div class="weight-type">{{ getModelTypeLabel(model.type) }}</div>
                    </div>
                    <div class="weight-control">
                      <input 
                        type="range" 
                        min="0" 
                        max="100" 
                        step="5"
                        v-model.number="modelWeights[model.id]"
                        @change="updateEnsembleSettings"
                      />
                      <div class="weight-value">{{ modelWeights[model.id] }}%</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="ensemble-actions">
                <button class="primary-btn" @click="updateEnsembleSettings">
                  <i class="fas fa-save"></i> حفظ الإعدادات
                </button>
                <button class="secondary-btn" @click="resetEnsembleSettings">
                  <i class="fas fa-redo"></i> إعادة ضبط
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- حالة النظام -->
        <div v-if="activeTab === 'system'" class="system-tab">
          <div v-if="loading" class="loading-indicator">
            <div class="spinner"></div>
            <p>جاري تحميل حالة النظام...</p>
          </div>

          <div v-else class="system-status">
            <div class="status-header">
              <h3>حالة نظام تشخيص أمراض النباتات</h3>
            </div>

            <div class="status-cards">
              <div class="status-card">
                <div class="card-icon">
                  <i class="fas fa-brain"></i>
                </div>
                <div class="card-content">
                  <h4>إجمالي النماذج</h4>
                  <div class="card-value">{{ systemStatus.total_processors }}</div>
                </div>
              </div>
              
              <div class="status-card">
                <div class="card-icon">
                  <i class="fas fa-layer-group"></i>
                </div>
                <div class="card-content">
                  <h4>معالج التجميع</h4>
                  <div class="card-value">{{ systemStatus.ensemble_available ? 'متاح' : 'غير متاح' }}</div>
                </div>
              </div>
              
              <div class="status-card">
                <div class="card-icon">
                  <i class="fas fa-seedling"></i>
                </div>
                <div class="card-content">
                  <h4>المحاصيل المدعومة</h4>
                  <div class="card-value">{{ systemStatus.supported_crops?.length || 0 }}</div>
                </div>
              </div>
              
              <div class="status-card">
                <div class="card-icon">
                  <i class="fas fa-bug"></i>
                </div>
                <div class="card-content">
                  <h4>الأمراض المدعومة</h4>
                  <div class="card-value">{{ systemStatus.supported_diseases?.length || 0 }}</div>
                </div>
              </div>
            </div>

            <div class="processor-types">
              <h4>أنواع النماذج</h4>
              <div class="types-chart">
                <canvas ref="typesChart"></canvas>
              </div>
            </div>

            <div class="system-actions">
              <button class="primary-btn" @click="refreshSystemStatus">
                <i class="fas fa-sync"></i> تحديث الحالة
              </button>
              <button class="secondary-btn" @click="exportSystemConfig">
                <i class="fas fa-file-export"></i> تصدير التكوين
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة تفاصيل النموذج -->
    <div v-if="showModelDetails" class="modal-overlay" @click="closeModelDetails">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedModelDetails.name }}</h3>
          <button class="close-btn" @click="closeModelDetails">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="model-info-section">
            <div class="info-item">
              <span class="info-label">النوع:</span>
              <span class="info-value">{{ getModelTypeLabel(selectedModelDetails.type) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">المعرف:</span>
              <span class="info-value">{{ selectedModelDetails.id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">الوصف:</span>
              <span class="info-value">{{ selectedModelDetails.description || 'لا يوجد وصف متاح' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">المسار:</span>
              <span class="info-value">{{ selectedModelDetails.model_path || 'غير متاح' }}</span>
            </div>
          </div>
          
          <div class="model-capabilities">
            <h4>القدرات</h4>
            
            <div class="capabilities-section">
              <h5>المحاصيل المدعومة ({{ selectedModelDetails.supported_crops?.length || 0 }})</h5>
              <div class="tags-container">
                <div 
                  v-for="(crop, index) in selectedModelDetails.supported_crops" 
                  :key="index"
                  class="tag"
                >
                  {{ crop }}
                </div>
              </div>
            </div>
            
            <div class="capabilities-section">
              <h5>الأمراض المدعومة ({{ selectedModelDetails.supported_diseases?.length || 0 }})</h5>
              <div class="tags-container">
                <div 
                  v-for="(disease, index) in selectedModelDetails.supported_diseases" 
                  :key="index"
                  class="tag"
                >
                  {{ disease }}
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="selectedModelDetails.metadata" class="model-metadata">
            <h4>البيانات الوصفية</h4>
            <div class="metadata-table">
              <div 
                v-for="(value, key) in selectedModelDetails.metadata" 
                :key="key"
                class="metadata-row"
              >
                <div class="metadata-key">{{ key }}</div>
                <div class="metadata-value">{{ value }}</div>
              </div>
            </div>
          </div>
          
          <div v-if="selectedModelDetails.type === 'ensemble'" class="ensemble-details">
            <h4>تفاصيل التجميع</h4>
            
            <div class="ensemble-info">
              <div class="info-item">
                <span class="info-label">طريقة التصويت:</span>
                <span class="info-value">{{ getVotingMethodLabel(selectedModelDetails.voting_method) }}</span>
              </div>
            </div>
            
            <div class="component-models">
              <h5>النماذج المكونة</h5>
              <ul class="models-list">
                <li 
                  v-for="modelId in selectedModelDetails.component_processors" 
                  :key="modelId"
                >
                  {{ getModelNameById(modelId) }}
                  <span v-if="selectedModelDetails.weights && selectedModelDetails.weights[modelId]">
                    ({{ (selectedModelDetails.weights[modelId] * 100).toFixed(0) }}%)
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="secondary-btn" @click="closeModelDetails">
            <i class="fas fa-times"></i> إغلاق
          </button>
        </div>
      </div>
    </div>

    <!-- نافذة تكوين النموذج -->
    <div v-if="showModelConfig" class="modal-overlay" @click="closeModelConfig">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>تكوين {{ selectedModelDetails.name }}</h3>
          <button class="close-btn" @click="closeModelConfig">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="config-form">
            <div class="form-group">
              <label for="model-display-name">الاسم المعروض</label>
              <input 
                id="model-display-name"
                type="text" 
                v-model="modelConfig.name" 
                placeholder="الاسم الذي سيظهر في النظام"
                aria-required="true"
                aria-describedby="model-name-help"
              />
              <small id="model-name-help" class="form-text">أدخل اسماً وصفياً للنموذج</small>
            </div>
            
            <div class="form-group">
              <label for="model-description">الوصف</label>
              <textarea 
                id="model-description"
                v-model="modelConfig.description" 
                placeholder="وصف النموذج وقدراته"
                aria-describedby="model-description-help"
                rows="3"
              ></textarea>
              <small id="model-description-help" class="form-text">أدخل وصفاً تفصيلياً للنموذج وقدراته</small>
            </div>
            
            <div class="form-group">
              <label for="model-metadata">البيانات الوصفية</label>
              <div id="model-metadata" class="metadata-editor" role="group" aria-labelledby="metadata-title">
                <h4 id="metadata-title" class="sr-only">تحرير البيانات الوصفية</h4>
                <div 
                  v-for="(value, key, index) in modelConfig.metadata" 
                  :key="index"
                  class="metadata-item"
                  role="group"
                  :aria-label="`بيان ${key}`"
                >
                  <input 
                    type="text" 
                    v-model="modelConfig.metadata[index].key" 
                    placeholder="المفتاح"
                    :aria-label="`مفتاح ${index + 1}`"
                  />
                  <input 
                    type="text" 
                    v-model="modelConfig.metadata[index].value" 
                    placeholder="القيمة"
                    :aria-label="`قيمة ${index + 1}`"
                  />
                  <button 
                    @click="removeMetadata(index)"
                    class="remove-btn"
                    :aria-label="`حذف ${key}`"
                  >
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <button 
                  @click="addMetadata"
                  class="add-btn"
                  aria-label="إضافة بيانات وصفية جديدة"
                >
                  <i class="fas fa-plus"></i> إضافة
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="primary-btn" @click="saveModelConfig">
            <i class="fas fa-save"></i> حفظ التكوين
          </button>
          <button class="secondary-btn" @click="closeModelConfig">
            <i class="fas fa-times"></i> إلغاء
          </button>
        </div>
      </div>
    </div>

    <!-- نافذة تأكيد الحذف -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDeleteModel">
      <div class="modal-content confirm-dialog" @click.stop>
        <div class="modal-header">
          <h3>تأكيد الحذف</h3>
          <button class="close-btn" @click="cancelDeleteModel">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <p>هل أنت متأكد من رغبتك في حذف النموذج "{{ getModelNameById(modelToDelete) }}"؟</p>
          <p class="warning-text">هذا الإجراء لا يمكن التراجع عنه.</p>
        </div>
        
        <div class="modal-footer">
          <button class="danger-btn" @click="deleteModel">
            <i class="fas fa-trash"></i> حذف
          </button>
          <button class="secondary-btn" @click="cancelDeleteModel">
            <i class="fas fa-times"></i> إلغاء
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast';
import plantDiseaseService from '@/services/plantDiseaseService';
import Chart from 'chart.js/auto';
import { computed, nextTick, onMounted, ref, watch } from 'vue';

export default {
  name: 'ModelConfigurationPanel',
  
  setup() {
    const { showToast } = useToast();
    
    // حالة النموذج
    const loading = ref(false);
    const activeTab = ref('available');
    const availableModels = ref([]);
    const systemStatus = ref({});
    const searchQuery = ref('');
    const typeFilter = ref('');
    
    // إضافة نموذج جديد
    const selectedSource = ref('');
    const newModel = ref({
      huggingface: {
        modelName: '',
        displayName: '',
        description: ''
      },
      github: {
        repoUrl: '',
        repoName: '',
        modelPath: '',
        description: ''
      },
      docker: {
        imageName: '',
        displayName: '',
        port: 8080,
        apiPath: '/api/predict',
        description: ''
      }
    });
    
    // إعدادات التجميع
    const ensembleSettings = ref({
      enabled: false,
      votingMethod: 'weighted'
    });
    const modelWeights = ref({});
    
    // تفاصيل النموذج
    const showModelDetails = ref(false);
    const selectedModelDetails = ref({});
    
    // تكوين النموذج
    const showModelConfig = ref(false);
    const modelConfig = ref({
      name: '',
      description: '',
      metadata: {}
    });
    const metadataKeys = ref([]);
    
    // حذف النموذج
    const showDeleteConfirm = ref(false);
    const modelToDelete = ref('');
    
    // مراجع الرسوم البيانية
    const typesChart = ref(null);
    let typesChartInstance = null;
    
    // القيم المحسوبة
    const filteredModels = computed(() => {
      if (!searchQuery.value && !typeFilter.value) {
        return availableModels.value;
      }
      
      return availableModels.value.filter(model => {
        const matchesSearch = !searchQuery.value || 
          model.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          (model.description && model.description.toLowerCase().includes(searchQuery.value.toLowerCase()));
        
        const matchesType = !typeFilter.value || model.type === typeFilter.value;
        
        return matchesSearch && matchesType;
      });
    });
    
    const canAddModel = computed(() => {
      if (selectedSource.value === 'huggingface') {
        return newModel.value.huggingface.modelName && newModel.value.huggingface.displayName;
      } else if (selectedSource.value === 'github') {
        return newModel.value.github.repoUrl && newModel.value.github.repoName;
      } else if (selectedSource.value === 'docker') {
        return newModel.value.docker.imageName && newModel.value.docker.displayName;
      }
      
      return false;
    });
    
    // طرق الحياة
    onMounted(async () => {
      await loadAvailableModels();
      await loadSystemStatus();
    });
    
    watch(activeTab, async (newTab) => {
      if (newTab === 'ensemble') {
        await loadEnsembleSettings();
      } else if (newTab === 'system') {
        await loadSystemStatus();
      }
    });
    
    // الطرق
    const loadAvailableModels = async () => {
      try {
        loading.value = true;
        const response = await plantDiseaseService.getAvailableProcessors();
        availableModels.value = response.data;
      } catch (error) {
        console.error('Error loading available models:', error);
        showToast('خطأ في تحميل النماذج المتاحة', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    const loadSystemStatus = async () => {
      try {
        loading.value = true;
        const response = await plantDiseaseService.getSystemStatus();
        systemStatus.value = response.data;
        
        await nextTick();
        renderTypesChart();
      } catch (error) {
        console.error('Error loading system status:', error);
        showToast('خطأ في تحميل حالة النظام', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    const loadEnsembleSettings = async () => {
      try {
        loading.value = true;
        
        // الحصول على تفاصيل معالج التجميع
        const response = await plantDiseaseService.getProcessorDetails('ensemble');
        const ensembleDetails = response.data;
        
        // تعيين إعدادات التجميع
        ensembleSettings.value = {
          enabled: true, // إذا كان موجوداً، فهو مفعل
          votingMethod: ensembleDetails.voting_method || 'weighted'
        };
        
        // تعيين أوزان النماذج
        const weights = ensembleDetails.weights || {};
        
        // تحويل الأوزان إلى نسب مئوية
        modelWeights.value = {};
        
        availableModels.value.forEach(model => {
          if (model.id !== 'ensemble') {
            modelWeights.value[model.id] = Math.round((weights[model.id] || 0) * 100);
          }
        });
      } catch (error) {
        console.error('Error loading ensemble settings:', error);
        
        // إذا كان الخطأ بسبب عدم وجود معالج التجميع
        if (error.response && error.response.status === 404) {
          ensembleSettings.value = {
            enabled: false,
            votingMethod: 'weighted'
          };
          
          // تعيين أوزان متساوية افتراضية
          modelWeights.value = {};
          
          availableModels.value.forEach(model => {
            if (model.id !== 'ensemble') {
              modelWeights.value[model.id] = 100 / (availableModels.value.length - 1);
            }
          });
        } else {
          showToast('خطأ في تحميل إعدادات التجميع', 'error');
        }
      } finally {
        loading.value = false;
      }
    };
    
    const getModelTypeLabel = (type) => {
      const typeLabels = {
        'local': 'محلي',
        'huggingface': 'Hugging Face',
        'github': 'GitHub',
        'ensemble': 'تجميعي',
        'docker': 'Docker'
      };
      
      return typeLabels[type] || type;
    };
    
    const getSourceLabel = (source) => {
      const sourceLabels = {
        'huggingface': 'Hugging Face',
        'github': 'GitHub',
        'docker': 'Docker'
      };
      
      return sourceLabels[source] || source;
    };
    
    const getVotingMethodLabel = (method) => {
      const methodLabels = {
        'weighted': 'موزون (Weighted)',
        'majority': 'أغلبية (Majority)',
        'confidence': 'ثقة (Confidence)'
      };
      
      return methodLabels[method] || method;
    };
    
    const getModelNameById = (modelId) => {
      const model = availableModels.value.find(m => m.id === modelId);
      return model ? model.name : modelId;
    };
    
    const viewModelDetails = async (modelId) => {
      try {
        loading.value = true;
        const response = await plantDiseaseService.getProcessorDetails(modelId);
        selectedModelDetails.value = response.data;
        showModelDetails.value = true;
      } catch (error) {
        console.error('Error loading model details:', error);
        showToast('خطأ في تحميل تفاصيل النموذج', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    const closeModelDetails = () => {
      showModelDetails.value = false;
      selectedModelDetails.value = {};
    };
    
    const configureModel = async (modelId) => {
      try {
        loading.value = true;
        const response = await plantDiseaseService.getProcessorDetails(modelId);
        selectedModelDetails.value = response.data;
        
        // تعيين قيم التكوين
        modelConfig.value = {
          name: selectedModelDetails.value.name || '',
          description: selectedModelDetails.value.description || '',
          metadata: { ...(selectedModelDetails.value.metadata || {}) }
        };
        
        // تعيين مفاتيح البيانات الوصفية
        metadataKeys.value = Object.keys(modelConfig.value.metadata);
        
        showModelConfig.value = true;
      } catch (error) {
        console.error('Error loading model details for configuration:', error);
        showToast('خطأ في تحميل تفاصيل النموذج للتكوين', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    const closeModelConfig = () => {
      showModelConfig.value = false;
      modelConfig.value = {
        name: '',
        description: '',
        metadata: {}
      };
      metadataKeys.value = [];
    };
    
    const addMetadataItem = () => {
      const newKey = `key_${Object.keys(modelConfig.value.metadata).length + 1}`;
      modelConfig.value.metadata[newKey] = '';
      metadataKeys.value.push(newKey);
    };
    
    const removeMetadataItem = (key) => {
      const index = metadataKeys.value.indexOf(key);
      if (index !== -1) {
        metadataKeys.value.splice(index, 1);
      }
      
      const newMetadata = {};
      Object.keys(modelConfig.value.metadata).forEach(k => {
        if (k !== key) {
          newMetadata[k] = modelConfig.value.metadata[k];
        }
      });
      
      modelConfig.value.metadata = newMetadata;
    };
    
    const updateMetadataKey = (index, oldKey) => {
      const newKey = metadataKeys.value[index];
      
      if (newKey !== oldKey) {
        const value = modelConfig.value.metadata[oldKey];
        delete modelConfig.value.metadata[oldKey];
        modelConfig.value.metadata[newKey] = value;
      }
    };
    
    const saveModelConfig = async () => {
      try {
        loading.value = true;
        
        const config = {
          name: modelConfig.value.name,
          description: modelConfig.value.description,
          metadata: modelConfig.value.metadata
        };
        
        await plantDiseaseService.updateProcessorConfig(selectedModelDetails.value.id, config);
        
        showToast('تم حفظ التكوين بنجاح', 'success');
        closeModelConfig();
        
        // إعادة تحميل النماذج المتاحة
        await loadAvailableModels();
      } catch (error) {
        console.error('Error saving model configuration:', error);
        showToast('خطأ في حفظ تكوين النموذج', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    const confirmDeleteModel = (modelId) => {
      modelToDelete.value = modelId;
      showDeleteConfirm.value = true;
    };
    
    const cancelDeleteModel = () => {
      showDeleteConfirm.value = false;
      modelToDelete.value = '';
    };
    
    const deleteModel = async () => {
      try {
        loading.value = true;
        
        await plantDiseaseService.removeExternalModel(modelToDelete.value);
        
        showToast('تم حذف النموذج بنجاح', 'success');
        cancelDeleteModel();
        
        // إعادة تحميل النماذج المتاحة
        await loadAvailableModels();
      } catch (error) {
        console.error('Error deleting model:', error);
        showToast('خطأ في حذف النموذج', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    const addNewModel = async () => {
      try {
        loading.value = true;
        
        let modelInfo = {};
        
        if (selectedSource.value === 'huggingface') {
          modelInfo = {
            type: 'huggingface',
            model_name: newModel.value.huggingface.modelName,
            display_name: newModel.value.huggingface.displayName,
            description: newModel.value.huggingface.description
          };
        } else if (selectedSource.value === 'github') {
          modelInfo = {
            type: 'github',
            repo_url: newModel.value.github.repoUrl,
            repo_name: newModel.value.github.repoName,
            repo_path: newModel.value.github.modelPath,
            description: newModel.value.github.description
          };
        } else if (selectedSource.value === 'docker') {
          modelInfo = {
            type: 'docker',
            image_name: newModel.value.docker.imageName,
            display_name: newModel.value.docker.displayName,
            port: newModel.value.docker.port,
            api_path: newModel.value.docker.apiPath,
            description: newModel.value.docker.description
          };
        }
        
        await plantDiseaseService.addExternalModel(modelInfo);
        
        showToast('تم إضافة النموذج بنجاح', 'success');
        resetNewModelForm();
        
        // إعادة تحميل النماذج المتاحة
        await loadAvailableModels();
        
        // الانتقال إلى علامة التبويب النماذج المتاحة
        activeTab.value = 'available';
      } catch (error) {
        console.error('Error adding new model:', error);
        showToast('خطأ في إضافة النموذج الجديد', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    const resetNewModelForm = () => {
      selectedSource.value = '';
      newModel.value = {
        huggingface: {
          modelName: '',
          displayName: '',
          description: ''
        },
        github: {
          repoUrl: '',
          repoName: '',
          modelPath: '',
          description: ''
        },
        docker: {
          imageName: '',
          displayName: '',
          port: 8080,
          apiPath: '/api/predict',
          description: ''
        }
      };
    };
    
    const updateEnsembleSettings = async () => {
      try {
        loading.value = true;
        
        // تحويل الأوزان من نسب مئوية إلى قيم عشرية
        const normalizedWeights = {};
        let totalWeight = 0;
        
        Object.keys(modelWeights.value).forEach(modelId => {
          totalWeight += modelWeights.value[modelId];
        });
        
        Object.keys(modelWeights.value).forEach(modelId => {
          normalizedWeights[modelId] = modelWeights.value[modelId] / totalWeight;
        });
        
        const config = {
          enabled: ensembleSettings.value.enabled,
          voting_method: ensembleSettings.value.votingMethod,
          weights: normalizedWeights,
          processors: Object.keys(modelWeights.value)
        };
        
        await plantDiseaseService.updateProcessorConfig('ensemble', config);
        
        showToast('تم تحديث إعدادات التجميع بنجاح', 'success');
        
        // إعادة تحميل النماذج المتاحة
        await loadAvailableModels();
      } catch (error) {
        console.error('Error updating ensemble settings:', error);
        showToast('خطأ في تحديث إعدادات التجميع', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    const resetEnsembleSettings = async () => {
      await loadEnsembleSettings();
    };
    
    const refreshSystemStatus = async () => {
      await loadSystemStatus();
    };
    
    const exportSystemConfig = () => {
      try {
        const config = {
          models: availableModels.value.map(model => ({
            id: model.id,
            name: model.name,
            type: model.type
          })),
          ensemble: {
            enabled: ensembleSettings.value.enabled,
            voting_method: ensembleSettings.value.votingMethod,
            weights: modelWeights.value
          },
          system_status: systemStatus.value
        };
        
        const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = 'plant_disease_system_config.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showToast('تم تصدير التكوين بنجاح', 'success');
      } catch (error) {
        console.error('Error exporting system configuration:', error);
        showToast('خطأ في تصدير تكوين النظام', 'error');
      }
    };
    
    const renderTypesChart = () => {
      if (!typesChart.value || !systemStatus.value.processor_types) return;
      
      const types = systemStatus.value.processor_types;
      const labels = Object.keys(types).map(type => getModelTypeLabel(type));
      const data = Object.values(types);
      
      if (typesChartInstance) {
        typesChartInstance.destroy();
      }
      
      typesChartInstance = new Chart(typesChart.value, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: [
              'rgba(54, 162, 235, 0.6)',
              'rgba(75, 192, 192, 0.6)',
              'rgba(153, 102, 255, 0.6)',
              'rgba(255, 159, 64, 0.6)'
            ],
            borderColor: [
              'rgba(54, 162, 235, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'right',
            },
            title: {
              display: true,
              text: 'توزيع أنواع النماذج'
            }
          }
        }
      });
    };
    
    return {
      // الحالة
      loading,
      activeTab,
      availableModels,
      systemStatus,
      searchQuery,
      typeFilter,
      selectedSource,
      newModel,
      ensembleSettings,
      modelWeights,
      showModelDetails,
      selectedModelDetails,
      showModelConfig,
      modelConfig,
      metadataKeys,
      showDeleteConfirm,
      modelToDelete,
      typesChart,
      
      // القيم المحسوبة
      filteredModels,
      canAddModel,
      
      // الطرق
      getModelTypeLabel,
      getSourceLabel,
      getVotingMethodLabel,
      getModelNameById,
      viewModelDetails,
      closeModelDetails,
      configureModel,
      closeModelConfig,
      addMetadataItem,
      removeMetadataItem,
      updateMetadataKey,
      saveModelConfig,
      confirmDeleteModel,
      cancelDeleteModel,
      deleteModel,
      addNewModel,
      resetNewModelForm,
      updateEnsembleSettings,
      resetEnsembleSettings,
      refreshSystemStatus,
      exportSystemConfig
    };
  }
};
</script>

<style scoped>
.model-configuration-panel {
  background-color: var(--bg-color);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
  direction: rtl;
}

.panel-header {
  margin-bottom: 20px;
  text-align: center;
}

.panel-header h2 {
  color: var(--primary-color);
  margin-bottom: 10px;
}

.panel-header .description {
  color: var(--text-secondary);
  font-size: 14px;
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.tab:hover {
  color: var(--primary-color);
}

.tab.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
  font-weight: 500;
}

.tab-content {
  min-height: 400px;
}

/* النماذج المتاحة */
.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
}

.type-filter {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 40px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.no-models {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}

.models-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.model-item {
  background-color: var(--bg-color-light);
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.2s ease;
}

.model-item:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.model-info {
  padding: 15px;
}

.model-info h3 {
  margin: 0 0 10px 0;
  color: var(--primary-color);
}

.model-info p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.model-meta {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.model-type {
  font-size: 12px;
  color: var(--text-secondary);
  background-color: var(--bg-color);
  padding: 4px 8px;
  border-radius: 4px;
}

.model-status {
  font-size: 12px;
  color: var(--text-secondary);
  background-color: var(--bg-color);
  padding: 4px 8px;
  border-radius: 4px;
}

.model-actions {
  padding: 15px;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s ease;
}

.edit-btn {
  background-color: var(--primary-color-light);
  color: var(--primary-color);
}

.edit-btn:hover {
  background-color: var(--primary-color-light);
  filter: brightness(0.95);
}

.delete-btn {
  background-color: var(--danger-color-light);
  color: var(--danger-color);
  margin-right: auto;
}

.delete-btn:hover {
  background-color: var(--danger-color-light);
  filter: brightness(0.95);
}

/* إضافة نموذج جديد */
.model-source-selector {
  margin-bottom: 30px;
}

.model-source-selector h3 {
  margin: 0 0 15px 0;
  color: var(--primary-color);
}

.source-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.source-option {
  background-color: var(--bg-color-light);
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.source-option:hover {
  background-color: var(--hover-color);
}

.source-option.selected {
  border-color: var(--primary-color);
  background-color: var(--primary-color-light);
}

.source-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: var(--primary-color);
}

.source-info {
  flex: 1;
}

.source-info h4 {
  margin: 0 0 5px 0;
  color: var(--text-primary);
}

.source-info p {
  margin: 0;
  font-size: 12px;
  color: var(--text-secondary);
}

.model-form {
  background-color: var(--bg-color-light);
  border-radius: 8px;
  padding: 20px;
}

.model-form h3 {
  margin: 0 0 20px 0;
  color: var(--primary-color);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: var(--text-primary);
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.form-group small {
  display: block;
  margin-top: 5px;
  font-size: 12px;
  color: var(--text-secondary);
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.primary-btn,
.secondary-btn,
.danger-btn {
  padding: 10px 20px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.primary-btn {
  background-color: var(--primary-color);
  color: white;
}

.primary-btn:hover {
  background-color: var(--primary-color-dark);
}

.primary-btn:disabled {
  background-color: var(--disabled-color);
  cursor: not-allowed;
}

.secondary-btn {
  background-color: var(--secondary-color);
  color: var(--text-primary);
}

.secondary-btn:hover {
  background-color: var(--secondary-color-dark);
}

.danger-btn {
  background-color: var(--danger-color);
  color: white;
}

.danger-btn:hover {
  background-color: var(--danger-color-dark);
}

/* إعدادات التجميع */
.ensemble-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ensemble-header {
  margin-bottom: 10px;
}

.ensemble-header h3 {
  margin: 0 0 5px 0;
  color: var(--primary-color);
}

.ensemble-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.ensemble-status {
  background-color: var(--bg-color-light);
  border-radius: 8px;
  padding: 15px;
}

.status-toggle {
  display: flex;
  align-items: center;
}

.toggle-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  cursor: pointer;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--disabled-color);
  transition: .4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

.ensemble-config {
  background-color: var(--bg-color-light);
  border-radius: 8px;
  padding: 15px;
}

.voting-method {
  margin-bottom: 20px;
}

.voting-method h4 {
  margin: 0 0 10px 0;
  color: var(--text-primary);
}

.radio-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.radio-option {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
}

.radio-option input {
  margin-top: 3px;
}

.radio-option span {
  font-weight: 500;
  color: var(--text-primary);
}

.radio-option small {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
}

.model-weights {
  margin-top: 20px;
}

.model-weights h4 {
  margin: 0 0 5px 0;
  color: var(--text-primary);
}

.model-weights p {
  margin: 0 0 15px 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.weights-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.weight-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.weight-info {
  width: 150px;
}

.weight-name {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 3px;
}

.weight-type {
  font-size: 12px;
  color: var(--text-secondary);
}

.weight-control {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.weight-control input {
  flex: 1;
}

.weight-value {
  width: 50px;
  text-align: left;
  font-weight: 500;
}

.ensemble-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

/* حالة النظام */
.system-status {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status-header {
  margin-bottom: 10px;
}

.status-header h3 {
  margin: 0;
  color: var(--primary-color);
}

.status-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.status-card {
  background-color: var(--bg-color-light);
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary-color-light);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 15px;
  font-size: 20px;
  color: var(--primary-color);
}

.card-content {
  flex: 1;
}

.card-content h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.card-value {
  font-weight: 500;
  font-size: 18px;
  color: var(--text-primary);
}

.processor-types {
  background-color: var(--bg-color-light);
  border-radius: 8px;
  padding: 15px;
  margin-top: 20px;
}

.processor-types h4 {
  margin: 0 0 15px 0;
  color: var(--text-primary);
  text-align: center;
}

.types-chart {
  height: 300px;
}

.system-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

/* النوافذ المنبثقة */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--bg-color);
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  direction: rtl;
}

.confirm-dialog {
  max-width: 400px;
}

.modal-header {
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: var(--primary-color);
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--text-secondary);
}

.close-btn:hover {
  color: var(--text-primary);
}

.modal-body {
  padding: 15px;
}

.modal-footer {
  padding: 15px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.warning-text {
  color: var(--danger-color);
  font-weight: 500;
}

/* تفاصيل النموذج */
.model-info-section {
  margin-bottom: 20px;
}

.info-item {
  margin-bottom: 10px;
  display: flex;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-label {
  font-weight: 500;
  color: var(--text-secondary);
  width: 100px;
  margin-left: 10px;
}

.info-value {
  flex: 1;
  color: var(--text-primary);
}

.model-capabilities {
  margin-bottom: 20px;
}

.model-capabilities h4 {
  margin: 0 0 15px 0;
  color: var(--primary-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 10px;
}

.capabilities-section {
  margin-bottom: 15px;
}

.capabilities-section h5 {
  margin: 0 0 10px 0;
  color: var(--text-primary);
  font-size: 14px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background-color: var(--bg-color-light);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  color: var(--text-primary);
}

.model-metadata {
  margin-bottom: 20px;
}

.model-metadata h4 {
  margin: 0 0 15px 0;
  color: var(--primary-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 10px;
}

.metadata-table {
  border: 1px solid var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.metadata-row {
  display: flex;
  border-bottom: 1px solid var(--border-color);
}

.metadata-row:last-child {
  border-bottom: none;
}

.metadata-key,
.metadata-value {
  padding: 8px 12px;
}

.metadata-key {
  width: 40%;
  background-color: var(--bg-color-light);
  font-weight: 500;
  border-left: 1px solid var(--border-color);
}

.metadata-value {
  width: 60%;
}

.ensemble-details {
  margin-bottom: 20px;
}

.ensemble-details h4 {
  margin: 0 0 15px 0;
  color: var(--primary-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 10px;
}

.ensemble-info {
  margin-bottom: 15px;
}

.component-models h5 {
  margin: 0 0 10px 0;
  color: var(--text-primary);
  font-size: 14px;
}

.models-list {
  margin: 0;
  padding-right: 20px;
}

.models-list li {
  margin-bottom: 5px;
}

/* تكوين النموذج */
.metadata-editor {
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 10px;
  background-color: var(--bg-color);
}

.metadata-item {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.metadata-item input {
  flex: 1;
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
}

.remove-btn {
  background-color: var(--danger-color-light);
  color: var(--danger-color);
  border: none;
  border-radius: 4px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.add-btn {
  background-color: var(--bg-color-light);
  color: var(--primary-color);
  border: 1px dashed var(--border-color);
  border-radius: 4px;
  padding: 8px 12px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn:hover {
  background-color: var(--hover-color);
}

/* متغيرات CSS */
:root {
  --primary-color: #2c7be5;
  --primary-color-dark: #1a68d1;
  --primary-color-light: #e5f0ff;
  --secondary-color: #edf2f9;
  --secondary-color-dark: #d8e2f0;
  --success-color: #00d97e;
  --danger-color: #e63757;
  --danger-color-light: #fae3e8;
  --danger-color-dark: #d21e3c;
  --warning-color: #f6c343;
  --info-color: #39afd1;
  --text-primary: #12263f;
  --text-secondary: #95aac9;
  --bg-color: #ffffff;
  --bg-color-light: #f9fbfd;
  --bg-color-accent: #edf2f9;
  --border-color: #e3ebf6;
  --hover-color: #f5f8fc;
  --disabled-color: #b1c2d8;
}

/* تصميم متجاوب */
@media (max-width: 768px) {
  .models-list {
    grid-template-columns: 1fr;
  }
  
  .status-cards {
    grid-template-columns: 1fr 1fr;
  }
  
  .source-options {
    grid-template-columns: 1fr;
  }
  
  .model-result-content {
    grid-template-columns: 1fr;
  }
}
</style>
