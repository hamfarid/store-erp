<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/ml/DatasetManager.vue
الوصف: مكون إدارة مجموعات البيانات وتدريب النماذج
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="dataset-manager">
    <div class="header">
      <h2 class="title">إدارة مجموعات البيانات والنماذج</h2>
      <p class="description">
        يمكنك من هنا إدارة مجموعات البيانات وتدريب النماذج المخصصة
      </p>
    </div>

    <div class="tabs">
      <div 
        :class="['tab', { active: activeTab === 'datasets' }]"
        @click="activeTab = 'datasets'"
      >
        مجموعات البيانات
      </div>
      <div 
        :class="['tab', { active: activeTab === 'models' }]"
        @click="activeTab = 'models'"
      >
        النماذج
      </div>
      <div 
        :class="['tab', { active: activeTab === 'training' }]"
        @click="activeTab = 'training'"
      >
        التدريب
      </div>
      <div 
        :class="['tab', { active: activeTab === 'evaluation' }]"
        @click="activeTab = 'evaluation'"
      >
        التقييم
      </div>
    </div>

    <!-- قسم مجموعات البيانات -->
    <div v-if="activeTab === 'datasets'" class="tab-content">
      <div class="actions">
        <button class="btn primary" @click="showImportDialog = true">استيراد مجموعة بيانات</button>
        <button class="btn secondary" @click="refreshDatasets">تحديث</button>
      </div>

      <div class="datasets-list">
        <div v-if="loading" class="loading">جاري التحميل...</div>
        <div v-else-if="datasets.length === 0" class="empty-state">
          لا توجد مجموعات بيانات. قم باستيراد مجموعة بيانات للبدء.
        </div>
        <div v-else class="grid">
          <div v-for="dataset in datasets" :key="dataset.id" class="dataset-card">
            <div class="dataset-header">
              <h3>{{ dataset.name }}</h3>
              <span class="badge">{{ dataset.source }}</span>
            </div>
            <div class="dataset-stats">
              <div class="stat">
                <span class="label">الصور:</span>
                <span class="value">{{ dataset.imageCount }}</span>
              </div>
              <div class="stat">
                <span class="label">الفئات:</span>
                <span class="value">{{ dataset.classCount }}</span>
              </div>
              <div class="stat">
                <span class="label">الحجم:</span>
                <span class="value">{{ formatSize(dataset.size) }}</span>
              </div>
            </div>
            <div class="dataset-actions">
              <button class="btn small" @click="viewDatasetDetails(dataset)">التفاصيل</button>
              <button class="btn small" @click="showAugmentDialog(dataset)">توسيع</button>
              <button class="btn small danger" @click="deleteDataset(dataset)">حذف</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- قسم النماذج -->
    <div v-if="activeTab === 'models'" class="tab-content">
      <div class="actions">
        <button class="btn secondary" @click="refreshModels">تحديث</button>
      </div>

      <div class="models-list">
        <div v-if="loading" class="loading">جاري التحميل...</div>
        <div v-else-if="models.length === 0" class="empty-state">
          لا توجد نماذج. قم بتدريب نموذج للبدء.
        </div>
        <div v-else class="grid">
          <div v-for="model in models" :key="model.id" class="model-card">
            <div class="model-header">
              <h3>{{ model.name }}</h3>
              <span class="badge">{{ model.type }}</span>
            </div>
            <div class="model-stats">
              <div class="stat">
                <span class="label">الدقة:</span>
                <span class="value">{{ (model.accuracy * 100).toFixed(2) }}%</span>
              </div>
              <div class="stat">
                <span class="label">الحجم:</span>
                <span class="value">{{ formatSize(model.size) }}</span>
              </div>
              <div class="stat">
                <span class="label">تاريخ التدريب:</span>
                <span class="value">{{ formatDate(model.trainedAt) }}</span>
              </div>
            </div>
            <div class="model-actions">
              <button class="btn small" @click="viewModelDetails(model)">التفاصيل</button>
              <button class="btn small" @click="showOptimizeDialog(model)">تحسين</button>
              <button class="btn small" @click="showExportDialog(model)">تصدير</button>
              <button class="btn small danger" @click="deleteModel(model)">حذف</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- قسم التدريب -->
    <div v-if="activeTab === 'training'" class="tab-content">
      <div class="training-form">
        <h3>تدريب نموذج جديد</h3>
        
        <div class="form-group">
          <label for="dataset">مجموعة البيانات</label>
          <select id="dataset" v-model="trainingConfig.datasetId">
            <option value="">اختر مجموعة بيانات</option>
            <option v-for="dataset in datasets" :key="dataset.id" :value="dataset.id">
              {{ dataset.name }} ({{ dataset.classCount }} فئة، {{ dataset.imageCount }} صورة)
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="modelType">نوع النموذج</label>
          <select id="modelType" v-model="trainingConfig.modelType">
            <option value="vit">Vision Transformer (ViT)</option>
            <option value="efficientnet">EfficientNet</option>
            <option value="regnet">RegNet</option>
            <option value="hybrid">هجين (CNN+ViT)</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="modelVariant">متغير النموذج</label>
          <select id="modelVariant" v-model="trainingConfig.modelVariant">
            <option v-if="trainingConfig.modelType === 'vit'" value="base">ViT-Base</option>
            <option v-if="trainingConfig.modelType === 'vit'" value="large">ViT-Large</option>
            <option v-if="trainingConfig.modelType === 'efficientnet'" value="b0">EfficientNet-B0</option>
            <option v-if="trainingConfig.modelType === 'efficientnet'" value="b4">EfficientNet-B4</option>
            <option v-if="trainingConfig.modelType === 'efficientnet'" value="b7">EfficientNet-B7</option>
            <option v-if="trainingConfig.modelType === 'regnet'" value="y16">RegNetY-16GF</option>
            <option v-if="trainingConfig.modelType === 'regnet'" value="y32">RegNetY-32GF</option>
            <option v-if="trainingConfig.modelType === 'hybrid'" value="efficient_vit">EfficientNet+ViT</option>
            <option v-if="trainingConfig.modelType === 'hybrid'" value="regnet_vit">RegNet+ViT</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="trainingSettings">إعدادات التدريب</label>
          <div id="trainingSettings" class="training-settings">
            <div class="setting">
              <label for="training-epochs">عدد الحقب (Epochs)</label>
              <input 
                id="training-epochs"
                type="number" 
                v-model.number="trainingConfig.epochs" 
                min="1"
                max="1000"
              />
            </div>
            <div class="setting">
              <label for="training-batch-size">حجم الدفعة (Batch Size)</label>
              <input 
                id="training-batch-size"
                type="number" 
                v-model.number="trainingConfig.batchSize" 
                min="1"
                max="128"
              />
            </div>
            <div class="setting">
              <label for="training-learning-rate">معدل التعلم (Learning Rate)</label>
              <input 
                id="training-learning-rate"
                type="number" 
                v-model.number="trainingConfig.learningRate" 
                min="0.0001"
                max="0.1"
                step="0.0001"
              />
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="augmentation">توسيع البيانات</label>
          <div id="augmentation" class="checkbox-group">
            <label for="useAugmentation">
              <input id="useAugmentation" type="checkbox" v-model="trainingConfig.useAugmentation" />
              استخدام توسيع البيانات
            </label>
          </div>
          <div v-if="trainingConfig.useAugmentation" class="augmentation-settings">
            <div class="setting">
              <label for="augmentationMethod">طريقة التوسيع</label>
              <select id="augmentationMethod" v-model="trainingConfig.augmentationMethod">
                <option value="traditional">تقليدية (تدوير، قلب، تغيير الحجم)</option>
                <option value="smart">ذكية (Smart Augmentation)</option>
                <option value="gan">GAN (توليد صور جديدة)</option>
              </select>
            </div>
            <div class="setting">
              <label for="augmentationFactor">عامل التوسيع</label>
              <input id="augmentationFactor" type="number" v-model.number="trainingConfig.augmentationFactor" min="1" max="10" />
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="gpu">استخدام GPU</label>
          <div id="gpu" class="checkbox-group">
            <label for="useGPU">
              <input id="useGPU" type="checkbox" v-model="trainingConfig.useGPU" />
              استخدام GPU للتدريب (يتطلب تثبيت حاويات GPU)
            </label>
          </div>
        </div>
        
        <div class="form-actions">
          <button class="btn secondary" @click="resetTrainingForm">إعادة تعيين</button>
          <button 
            class="btn primary" 
            @click="startTraining" 
            :disabled="!trainingConfig.datasetId || !trainingConfig.modelType || !trainingConfig.modelVariant"
          >
            بدء التدريب
          </button>
        </div>
      </div>
      
      <div v-if="activeTrainings.length > 0" class="active-trainings">
        <h3>التدريبات النشطة</h3>
        <div class="trainings-list">
          <div v-for="training in activeTrainings" :key="training.id" class="training-item">
            <div class="training-info">
              <div class="training-name">{{ training.modelName }}</div>
              <div class="training-dataset">{{ training.datasetName }}</div>
            </div>
            <div class="training-progress">
              <div class="progress-bar">
                <div class="progress" :style="{ width: `${training.progress}%` }"></div>
              </div>
              <div class="progress-text">{{ training.progress }}%</div>
            </div>
            <div class="training-status">{{ getTrainingStatusText(training.status) }}</div>
            <div class="training-actions">
              <button v-if="training.status === 'running'" class="btn small danger" @click="cancelTraining(training)">إلغاء</button>
              <button v-if="training.status === 'completed'" class="btn small" @click="viewTrainingResults(training)">النتائج</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- قسم التقييم -->
    <div v-if="activeTab === 'evaluation'" class="tab-content">
      <div class="evaluation-form">
        <h3>تقييم نموذج</h3>
        
        <div class="form-group">
          <label for="evalModel">النموذج</label>
          <select id="evalModel" v-model="evaluationConfig.modelId">
            <option value="">اختر نموذج</option>
            <option v-for="model in models" :key="model.id" :value="model.id">
              {{ model.name }} ({{ model.type }})
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="evalDataset">مجموعة البيانات</label>
          <select id="evalDataset" v-model="evaluationConfig.datasetId">
            <option value="">اختر مجموعة بيانات</option>
            <option v-for="dataset in datasets" :key="dataset.id" :value="dataset.id">
              {{ dataset.name }} ({{ dataset.classCount }} فئة، {{ dataset.imageCount }} صورة)
            </option>
          </select>
        </div>
        
        <div class="form-actions">
          <button 
            class="btn primary" 
            @click="startEvaluation" 
            :disabled="!evaluationConfig.modelId || !evaluationConfig.datasetId"
          >
            بدء التقييم
          </button>
        </div>
      </div>
      
      <div v-if="evaluationResults" class="evaluation-results">
        <h3>نتائج التقييم</h3>
        
        <div class="metrics">
          <div class="metric-card">
            <div class="metric-title">الدقة (Accuracy)</div>
            <div class="metric-value">{{ (evaluationResults.accuracy * 100).toFixed(2) }}%</div>
          </div>
          <div class="metric-card">
            <div class="metric-title">الدقة (Precision)</div>
            <div class="metric-value">{{ (evaluationResults.precision * 100).toFixed(2) }}%</div>
          </div>
          <div class="metric-card">
            <div class="metric-title">الاستدعاء (Recall)</div>
            <div class="metric-value">{{ (evaluationResults.recall * 100).toFixed(2) }}%</div>
          </div>
          <div class="metric-card">
            <div class="metric-title">F1 Score</div>
            <div class="metric-value">{{ (evaluationResults.f1Score * 100).toFixed(2) }}%</div>
          </div>
        </div>
        
        <div class="confusion-matrix">
          <h4>مصفوفة الارتباك (Confusion Matrix)</h4>
          <div class="matrix-container">
            <!-- هنا يتم عرض مصفوفة الارتباك -->
          </div>
        </div>
        
        <div class="class-metrics">
          <h4>مقاييس الفئات</h4>
          <table class="metrics-table">
            <thead>
              <tr>
                <th>الفئة</th>
                <th>الدقة (Precision)</th>
                <th>الاستدعاء (Recall)</th>
                <th>F1 Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(metric, className) in evaluationResults.classMetrics" :key="className">
                <td>{{ className }}</td>
                <td>{{ (metric.precision * 100).toFixed(2) }}%</td>
                <td>{{ (metric.recall * 100).toFixed(2) }}%</td>
                <td>{{ (metric.f1Score * 100).toFixed(2) }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- نافذة استيراد مجموعة بيانات -->
    <div v-if="showImportDialog" class="dialog-overlay">
      <div class="dialog">
        <div class="dialog-header">
          <h3>استيراد مجموعة بيانات</h3>
          <button class="close-btn" @click="showImportDialog = false">&times;</button>
        </div>
        <div class="dialog-content">
          <div class="space-y-6">
            <div>
              <label for="dataset-name" class="block text-sm font-medium text-gray-700">
                {{ $t('dataset.name') }}
              </label>
              <input
                id="dataset-name"
                v-model="importConfig.datasetName"
                type="text"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              />
            </div>

            <div>
              <label for="dataset-description" class="block text-sm font-medium text-gray-700">
                {{ $t('dataset.description') }}
              </label>
              <textarea
                id="dataset-description"
                v-model="importConfig.description"
                rows="3"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              ></textarea>
            </div>

            <div>
              <label for="dataset-type" class="block text-sm font-medium text-gray-700">
                {{ $t('dataset.type') }}
              </label>
              <select
                id="dataset-type"
                v-model="importConfig.type"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              >
                <option value="classification">تصنيف</option>
                <option value="detection">كشف</option>
                <option value="segmentation">تجزئة</option>
              </select>
            </div>

            <div>
              <label for="dataset-category" class="block text-sm font-medium text-gray-700">
                {{ $t('dataset.category') }}
              </label>
              <select
                id="dataset-category"
                v-model="importConfig.category"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              >
                <option value="training">{{ $t('dataset.categories.training') }}</option>
                <option value="validation">{{ $t('dataset.categories.validation') }}</option>
                <option value="testing">{{ $t('dataset.categories.testing') }}</option>
              </select>
            </div>

            <div>
              <label for="dataset-access" class="block text-sm font-medium text-gray-700">
                {{ $t('dataset.access') }}
              </label>
              <select
                id="dataset-access"
                v-model="importConfig.access"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              >
                <option value="public">{{ $t('dataset.access_levels.public') }}</option>
                <option value="private">{{ $t('dataset.access_levels.private') }}</option>
                <option value="restricted">{{ $t('dataset.access_levels.restricted') }}</option>
              </select>
            </div>

            <div>
              <label for="dataset-split">نسبة تقسيم البيانات</label>
              <div class="split-inputs">
                <input 
                  id="dataset-split-train"
                  type="number" 
                  v-model="importConfig.split.train" 
                  min="0"
                  max="100"
                  placeholder="تدريب"
                />
                <input 
                  id="dataset-split-validation"
                  type="number" 
                  v-model="importConfig.split.validation" 
                  min="0"
                  max="100"
                  placeholder="تحقق"
                />
                <input 
                  id="dataset-split-test"
                  type="number" 
                  v-model="importConfig.split.test" 
                  min="0"
                  max="100"
                  placeholder="اختبار"
                />
              </div>
            </div>
            
            <div v-if="importConfig.source === 'custom'" class="form-group">
              <label for="dataset-source">المصدر</label>
              <select v-model="importConfig.source">
                <option value="plantvillage">PlantVillage</option>
                <option value="plantdoc">PlantDoc</option>
                <option value="custom">مخصص</option>
              </select>
            </div>
            
            <div v-if="importConfig.source === 'custom'" class="form-group">
              <label for="dataset-import-method">طريقة الاستيراد</label>
              <div class="radio-group">
                <label>
                  <input type="radio" v-model="importConfig.importMethod" value="url" />
                  رابط
                </label>
                <label>
                  <input type="radio" v-model="importConfig.importMethod" value="file" />
                  ملف
                </label>
              </div>
              
              <div v-if="importConfig.importMethod === 'url'" class="form-group">
                <label for="dataset-url">رابط مجموعة البيانات</label>
                <input type="text" v-model="importConfig.datasetUrl" placeholder="أدخل رابط مجموعة البيانات (ZIP أو TAR.GZ)" />
              </div>
              
              <div v-if="importConfig.importMethod === 'file'" class="form-group">
                <label for="dataset-file">ملف مجموعة البيانات</label>
                <input type="file" @change="handleFileUpload" accept=".zip,.tar.gz" />
                <p class="help-text">يجب أن يكون الملف بصيغة ZIP أو TAR.GZ ويحتوي على مجلدات للفئات المختلفة</p>
              </div>
            </div>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn cancel" @click="showImportDialog = false">إلغاء</button>
          <button 
            class="btn primary" 
            @click="importDataset" 
            :disabled="!importConfig.datasetName || (importConfig.source === 'custom' && importConfig.importMethod === 'url' && !importConfig.datasetUrl) || (importConfig.source === 'custom' && importConfig.importMethod === 'file' && !importConfig.datasetFile)"
          >
            استيراد
          </button>
        </div>
      </div>
    </div>

    <!-- نافذة توسيع مجموعة البيانات -->
    <div v-if="showAugmentDialog" class="dialog-overlay">
      <div class="dialog">
        <div class="dialog-header">
          <h3>توسيع مجموعة البيانات</h3>
          <button class="close-btn" @click="showAugmentDialog = false">&times;</button>
        </div>
        <div class="dialog-content">
          <p>توسيع مجموعة البيانات "{{ selectedDataset.name }}"</p>
          
          <div class="form-group">
            <label>طريقة التوسيع</label>
            <select v-model="augmentConfig.method">
              <option value="traditional">تقليدية (تدوير، قلب، تغيير الحجم)</option>
              <option value="smart_augmentation">ذكية (Smart Augmentation)</option>
              <option value="gan">GAN (توليد صور جديدة)</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>عامل التوسيع</label>
            <input type="number" v-model.number="augmentConfig.factor" min="1" max="10" />
            <p class="help-text">عدد الصور الجديدة التي سيتم إنشاؤها لكل صورة أصلية</p>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn cancel" @click="showAugmentDialog = false">إلغاء</button>
          <button class="btn primary" @click="augmentDataset">توسيع</button>
        </div>
      </div>
    </div>

    <!-- نافذة تحسين النموذج -->
    <div v-if="showOptimizeDialog" class="dialog-overlay">
      <div class="dialog">
        <div class="dialog-header">
          <h3>تحسين النموذج</h3>
          <button class="close-btn" @click="showOptimizeDialog = false">&times;</button>
        </div>
        <div class="dialog-content">
          <p>تحسين النموذج "{{ selectedModel.name }}"</p>
          
          <div class="form-group">
            <label>طريقة التحسين</label>
            <select v-model="optimizeConfig.method">
              <option value="pruning">تقليم (Pruning)</option>
              <option value="quantization">تكميم (Quantization)</option>
              <option value="distillation">تقطير المعرفة (Knowledge Distillation)</option>
            </select>
          </div>
          
          <div v-if="optimizeConfig.method === 'pruning'" class="form-group">
            <label>نسبة التقليم</label>
            <input type="number" v-model.number="optimizeConfig.pruningRatio" min="0.1" max="0.9" step="0.1" />
            <p class="help-text">نسبة الأوزان التي سيتم إزالتها (0.1 - 0.9)</p>
          </div>
          
          <div v-if="optimizeConfig.method === 'quantization'" class="form-group">
            <label>نوع التكميم</label>
            <select v-model="optimizeConfig.quantizationType">
              <option value="int8">INT8</option>
              <option value="fp16">FP16</option>
            </select>
          </div>
          
          <div v-if="optimizeConfig.method === 'distillation'" class="form-group">
            <label>النموذج المعلم</label>
            <select v-model="optimizeConfig.teacherModelId">
              <option v-for="model in models.filter(m => m.id !== selectedModel.id)" :key="model.id" :value="model.id">
                {{ model.name }}
              </option>
            </select>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn cancel" @click="showOptimizeDialog = false">إلغاء</button>
          <button class="btn primary" @click="optimizeModel">تحسين</button>
        </div>
      </div>
    </div>

    <!-- نافذة تصدير النموذج -->
    <div v-if="showExportDialog" class="dialog-overlay">
      <div class="dialog">
        <div class="dialog-header">
          <h3>تصدير النموذج</h3>
          <button class="close-btn" @click="showExportDialog = false">&times;</button>
        </div>
        <div class="dialog-content">
          <p>تصدير النموذج "{{ selectedModel.name }}"</p>
          
          <div class="form-group">
            <label>صيغة التصدير</label>
            <select v-model="exportConfig.format">
              <option value="onnx">ONNX</option>
              <option value="tflite">TensorFlow Lite</option>
              <option value="pytorch">PyTorch</option>
              <option value="coreml">Core ML</option>
            </select>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn cancel" @click="showExportDialog = false">إلغاء</button>
          <button class="btn primary" @click="exportModel">تصدير</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast';
import modelTrainingService from '@/services/modelTrainingService';
import { onMounted, reactive, ref } from 'vue';

export default {
  name: 'DatasetManager',
  
  setup() {
    const { showToast } = useToast();
    
    const activeTab = ref('datasets');
    const loading = ref(false);
    const datasets = ref([]);
    const models = ref([]);
    const activeTrainings = ref([]);
    const evaluationResults = ref(null);
    
    const showImportDialog = ref(false);
    const showAugmentDialog = ref(false);
    const showOptimizeDialog = ref(false);
    const showExportDialog = ref(false);
    
    const selectedDataset = ref({});
    const selectedModel = ref({});
    
    const importConfig = reactive({
      source: 'plantvillage',
      datasetName: '',
      importMethod: 'url',
      datasetUrl: '',
      datasetFile: null
    });
    
    const augmentConfig = reactive({
      method: 'traditional',
      factor: 2
    });
    
    const trainingConfig = reactive({
      datasetId: '',
      modelType: 'vit',
      modelVariant: 'base',
      epochs: 10,
      batchSize: 32,
      learningRate: 0.001,
      useAugmentation: true,
      augmentationMethod: 'traditional',
      augmentationFactor: 2,
      useGPU: true
    });
    
    const evaluationConfig = reactive({
      modelId: '',
      datasetId: ''
    });
    
    const optimizeConfig = reactive({
      method: 'pruning',
      pruningRatio: 0.5,
      quantizationType: 'int8',
      teacherModelId: ''
    });
    
    const exportConfig = reactive({
      format: 'onnx'
    });
    
    // تحميل البيانات عند تحميل المكون
    onMounted(async () => {
      await refreshDatasets();
      await refreshModels();
      startTrainingStatusPolling();
    });
    
    // تحديث مجموعات البيانات
    const refreshDatasets = async () => {
      loading.value = true;
      try {
        const response = await modelTrainingService.getDatasets();
        datasets.value = response.data;
      } catch (error) {
        console.error('Error fetching datasets:', error);
        showToast('حدث خطأ أثناء تحميل مجموعات البيانات', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    // تحديث النماذج
    const refreshModels = async () => {
      loading.value = true;
      try {
        const response = await modelTrainingService.getModels();
        models.value = response.data;
      } catch (error) {
        console.error('Error fetching models:', error);
        showToast('حدث خطأ أثناء تحميل النماذج', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    // معالجة تحميل الملف
    const handleFileUpload = (event) => {
      importConfig.datasetFile = event.target.files[0];
    };
    
    // استيراد مجموعة بيانات
    const importDataset = async () => {
      try {
        showToast('جاري استيراد مجموعة البيانات...', 'info');
        
        const options = {
          source: importConfig.source,
          datasetName: importConfig.datasetName
        };
        
        if (importConfig.source === 'custom') {
          if (importConfig.importMethod === 'url') {
            options.datasetUrl = importConfig.datasetUrl;
          } else {
            options.datasetFile = importConfig.datasetFile;
          }
        }
        
        await modelTrainingService.importDataset(options);
        
        showToast('تم استيراد مجموعة البيانات بنجاح', 'success');
        showImportDialog.value = false;
        
        // إعادة تعيين النموذج
        importConfig.datasetName = '';
        importConfig.datasetUrl = '';
        importConfig.datasetFile = null;
        
        // تحديث قائمة مجموعات البيانات
        await refreshDatasets();
      } catch (error) {
        console.error('Error importing dataset:', error);
        showToast('حدث خطأ أثناء استيراد مجموعة البيانات', 'error');
      }
    };
    
    // عرض تفاصيل مجموعة البيانات
    const viewDatasetDetails = async (dataset) => {
      try {
        loading.value = true;
        const response = await modelTrainingService.getDatasetDetails(dataset.id);
        // هنا يمكن عرض تفاصيل مجموعة البيانات في نافذة منبثقة
        console.log('Dataset details:', response.data);
      } catch (error) {
        console.error('Error fetching dataset details:', error);
        showToast('حدث خطأ أثناء تحميل تفاصيل مجموعة البيانات', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    // عرض نافذة توسيع مجموعة البيانات
    const showAugmentDialog = (dataset) => {
      selectedDataset.value = dataset;
      showAugmentDialog.value = true;
    };
    
    // توسيع مجموعة البيانات
    const augmentDataset = async () => {
      try {
        showToast('جاري توسيع مجموعة البيانات...', 'info');
        
        await modelTrainingService.augmentDataset({
          datasetId: selectedDataset.value.id,
          method: augmentConfig.method,
          factor: augmentConfig.factor,
          config: {}
        });
        
        showToast('تم توسيع مجموعة البيانات بنجاح', 'success');
        showAugmentDialog.value = false;
        
        // تحديث قائمة مجموعات البيانات
        await refreshDatasets();
      } catch (error) {
        console.error('Error augmenting dataset:', error);
        showToast('حدث خطأ أثناء توسيع مجموعة البيانات', 'error');
      }
    };
    
    // حذف مجموعة بيانات
    const deleteDataset = async (dataset) => {
      if (!confirm(`هل أنت متأكد من رغبتك في حذف مجموعة البيانات "${dataset.name}"؟`)) {
        return;
      }
      
      try {
        showToast('جاري حذف مجموعة البيانات...', 'info');
        
        // استدعاء خدمة حذف مجموعة البيانات
        await modelTrainingService.deleteDataset(dataset.id);
        
        showToast('تم حذف مجموعة البيانات بنجاح', 'success');
        
        // تحديث قائمة مجموعات البيانات
        await refreshDatasets();
      } catch (error) {
        console.error('Error deleting dataset:', error);
        showToast('حدث خطأ أثناء حذف مجموعة البيانات', 'error');
      }
    };
    
    // عرض تفاصيل النموذج
    const viewModelDetails = async (model) => {
      try {
        loading.value = true;
        const response = await modelTrainingService.getModelDetails(model.id);
        // هنا يمكن عرض تفاصيل النموذج في نافذة منبثقة
        console.log('Model details:', response.data);
      } catch (error) {
        console.error('Error fetching model details:', error);
        showToast('حدث خطأ أثناء تحميل تفاصيل النموذج', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    // عرض نافذة تحسين النموذج
    const showOptimizeDialog = (model) => {
      selectedModel.value = model;
      showOptimizeDialog.value = true;
    };
    
    // تحسين النموذج
    const optimizeModel = async () => {
      try {
        showToast('جاري تحسين النموذج...', 'info');
        
        const config = {};
        
        if (optimizeConfig.method === 'pruning') {
          config.pruningRatio = optimizeConfig.pruningRatio;
        } else if (optimizeConfig.method === 'quantization') {
          config.quantizationType = optimizeConfig.quantizationType;
        } else if (optimizeConfig.method === 'distillation') {
          config.teacherModelId = optimizeConfig.teacherModelId;
        }
        
        await modelTrainingService.optimizeModel(selectedModel.value.id, optimizeConfig.method, config);
        
        showToast('تم تحسين النموذج بنجاح', 'success');
        showOptimizeDialog.value = false;
        
        // تحديث قائمة النماذج
        await refreshModels();
      } catch (error) {
        console.error('Error optimizing model:', error);
        showToast('حدث خطأ أثناء تحسين النموذج', 'error');
      }
    };
    
    // عرض نافذة تصدير النموذج
    const showExportDialog = (model) => {
      selectedModel.value = model;
      showExportDialog.value = true;
    };
    
    // تصدير النموذج
    const exportModel = async () => {
      try {
        showToast('جاري تصدير النموذج...', 'info');
        
        const response = await modelTrainingService.exportModel(selectedModel.value.id, exportConfig.format);
        
        // إنشاء رابط تحميل
        const downloadLink = document.createElement('a');
        downloadLink.href = response.data.downloadUrl;
        downloadLink.download = `${selectedModel.value.name}.${exportConfig.format}`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        
        showToast('تم تصدير النموذج بنجاح', 'success');
        showExportDialog.value = false;
      } catch (error) {
        console.error('Error exporting model:', error);
        showToast('حدث خطأ أثناء تصدير النموذج', 'error');
      }
    };
    
    // حذف نموذج
    const deleteModel = async (model) => {
      if (!confirm(`هل أنت متأكد من رغبتك في حذف النموذج "${model.name}"؟`)) {
        return;
      }
      
      try {
        showToast('جاري حذف النموذج...', 'info');
        
        // استدعاء خدمة حذف النموذج
        await modelTrainingService.deleteModel(model.id);
        
        showToast('تم حذف النموذج بنجاح', 'success');
        
        // تحديث قائمة النماذج
        await refreshModels();
      } catch (error) {
        console.error('Error deleting model:', error);
        showToast('حدث خطأ أثناء حذف النموذج', 'error');
      }
    };
    
    // إعادة تعيين نموذج التدريب
    const resetTrainingForm = () => {
      trainingConfig.datasetId = '';
      trainingConfig.modelType = 'vit';
      trainingConfig.modelVariant = 'base';
      trainingConfig.epochs = 10;
      trainingConfig.batchSize = 32;
      trainingConfig.learningRate = 0.001;
      trainingConfig.useAugmentation = true;
      trainingConfig.augmentationMethod = 'traditional';
      trainingConfig.augmentationFactor = 2;
      trainingConfig.useGPU = true;
    };
    
    // بدء التدريب
    const startTraining = async () => {
      try {
        showToast('جاري بدء التدريب...', 'info');
        
        const options = {
          datasetId: trainingConfig.datasetId,
          modelType: trainingConfig.modelType,
          modelVariant: trainingConfig.modelVariant,
          useGPU: trainingConfig.useGPU,
          trainingConfig: {
            epochs: trainingConfig.epochs,
            batchSize: trainingConfig.batchSize,
            learningRate: trainingConfig.learningRate,
            useAugmentation: trainingConfig.useAugmentation
          }
        };
        
        if (trainingConfig.useAugmentation) {
          options.trainingConfig.augmentationMethod = trainingConfig.augmentationMethod;
          options.trainingConfig.augmentationFactor = trainingConfig.augmentationFactor;
        }
        
        const response = await modelTrainingService.trainModel(options);
        
        showToast('تم بدء التدريب بنجاح', 'success');
        
        // إضافة التدريب إلى قائمة التدريبات النشطة
        const dataset = datasets.value.find(d => d.id === trainingConfig.datasetId);
        activeTrainings.value.push({
          id: response.data.trainingId,
          modelName: `${trainingConfig.modelType}-${trainingConfig.modelVariant}`,
          datasetName: dataset ? dataset.name : 'مجموعة بيانات غير معروفة',
          progress: 0,
          status: 'running'
        });
      } catch (error) {
        console.error('Error starting training:', error);
        showToast('حدث خطأ أثناء بدء التدريب', 'error');
      }
    };
    
    // إلغاء التدريب
    const cancelTraining = async (training) => {
      if (!confirm(`هل أنت متأكد من رغبتك في إلغاء تدريب "${training.modelName}"؟`)) {
        return;
      }
      
      try {
        showToast('جاري إلغاء التدريب...', 'info');
        
        // استدعاء خدمة إلغاء التدريب
        await modelTrainingService.cancelTraining(training.id);
        
        showToast('تم إلغاء التدريب بنجاح', 'success');
        
        // تحديث حالة التدريب
        const index = activeTrainings.value.findIndex(t => t.id === training.id);
        if (index !== -1) {
          activeTrainings.value[index].status = 'cancelled';
        }
      } catch (error) {
        console.error('Error cancelling training:', error);
        showToast('حدث خطأ أثناء إلغاء التدريب', 'error');
      }
    };
    
    // عرض نتائج التدريب
    const viewTrainingResults = (training) => {
      // هنا يمكن عرض نتائج التدريب في نافذة منبثقة
      console.log('Training results:', training);
    };
    
    // بدء التقييم
    const startEvaluation = async () => {
      try {
        showToast('جاري بدء التقييم...', 'info');
        
        const response = await modelTrainingService.evaluateModel(
          evaluationConfig.modelId,
          evaluationConfig.datasetId
        );
        
        evaluationResults.value = response.data;
        
        showToast('تم إكمال التقييم بنجاح', 'success');
      } catch (error) {
        console.error('Error starting evaluation:', error);
        showToast('حدث خطأ أثناء بدء التقييم', 'error');
      }
    };
    
    // بدء استطلاع حالة التدريب
    const startTrainingStatusPolling = () => {
      setInterval(async () => {
        for (const training of activeTrainings.value.filter(t => t.status === 'running')) {
          try {
            const response = await modelTrainingService.getTrainingStatus(training.id);
            const status = response.data;
            
            // تحديث حالة التدريب
            const index = activeTrainings.value.findIndex(t => t.id === training.id);
            if (index !== -1) {
              activeTrainings.value[index].progress = status.progress;
              activeTrainings.value[index].status = status.status;
            }
            
            // إذا اكتمل التدريب، تحديث قائمة النماذج
            if (status.status === 'completed' && activeTrainings.value[index].status !== 'completed') {
              await refreshModels();
              showToast(`تم اكتمال تدريب "${training.modelName}" بنجاح`, 'success');
            }
          } catch (error) {
            console.error('Error polling training status:', error);
          }
        }
      }, 5000); // استطلاع كل 5 ثوانٍ
    };
    
    // الحصول على نص حالة التدريب
    const getTrainingStatusText = (status) => {
      switch (status) {
        case 'running':
          return 'قيد التنفيذ';
        case 'completed':
          return 'مكتمل';
        case 'failed':
          return 'فشل';
        case 'cancelled':
          return 'ملغى';
        default:
          return status;
      }
    };
    
    // تنسيق الحجم
    const formatSize = (sizeInBytes) => {
      if (sizeInBytes < 1024) {
        return `${sizeInBytes} B`;
      } else if (sizeInBytes < 1024 * 1024) {
        return `${(sizeInBytes / 1024).toFixed(2)} KB`;
      } else if (sizeInBytes < 1024 * 1024 * 1024) {
        return `${(sizeInBytes / (1024 * 1024)).toFixed(2)} MB`;
      } else {
        return `${(sizeInBytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
      }
    };
    
    // تنسيق التاريخ
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString('ar-EG');
    };
    
    // مراقبة تغيير نوع النموذج لتحديث متغير النموذج
    watch(() => trainingConfig.modelType, (newType) => {
      switch (newType) {
        case 'vit':
          trainingConfig.modelVariant = 'base';
          break;
        case 'efficientnet':
          trainingConfig.modelVariant = 'b4';
          break;
        case 'regnet':
          trainingConfig.modelVariant = 'y16';
          break;
        case 'hybrid':
          trainingConfig.modelVariant = 'efficient_vit';
          break;
      }
    });
    
    return {
      activeTab,
      loading,
      datasets,
      models,
      activeTrainings,
      evaluationResults,
      showImportDialog,
      showAugmentDialog,
      showOptimizeDialog,
      showExportDialog,
      selectedDataset,
      selectedModel,
      importConfig,
      augmentConfig,
      trainingConfig,
      evaluationConfig,
      optimizeConfig,
      exportConfig,
      refreshDatasets,
      refreshModels,
      handleFileUpload,
      importDataset,
      viewDatasetDetails,
      showAugmentDialog,
      augmentDataset,
      deleteDataset,
      viewModelDetails,
      showOptimizeDialog,
      optimizeModel,
      showExportDialog,
      exportModel,
      deleteModel,
      resetTrainingForm,
      startTraining,
      cancelTraining,
      viewTrainingResults,
      startEvaluation,
      getTrainingStatusText,
      formatSize,
      formatDate
    };
  }
};
</script>

<style scoped>
.dataset-manager {
  padding: 20px;
  background-color: var(--bg-color);
  color: var(--text-color);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header {
  margin-bottom: 20px;
}

.title {
  font-size: 24px;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.description {
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
}

.tab.active {
  border-bottom: 2px solid var(--primary-color);
  color: var(--primary-color);
  font-weight: bold;
}

.tab-content {
  margin-bottom: 30px;
}

.actions {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: bold;
}

.btn:hover {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.primary {
  background-color: var(--primary-color);
  color: white;
}

.btn.secondary {
  background-color: var(--secondary-color);
  color: white;
}

.btn.danger {
  background-color: #dc3545;
  color: white;
}

.btn.small {
  padding: 4px 8px;
  font-size: 12px;
}

.loading {
  text-align: center;
  padding: 20px;
  color: var(--text-secondary);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  border-radius: 8px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.dataset-card, .model-card {
  background-color: var(--bg-secondary);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.dataset-card:hover, .model-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.dataset-header, .model-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.dataset-header h3, .model-header h3 {
  margin: 0;
  font-size: 16px;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  background-color: var(--primary-color);
  color: white;
}

.dataset-stats, .model-stats {
  margin-bottom: 15px;
}

.stat {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.label {
  color: var(--text-secondary);
}

.dataset-actions, .model-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.training-form, .evaluation-form {
  background-color: var(--bg-secondary);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.training-form h3, .evaluation-form h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: var(--primary-color);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.training-settings, .augmentation-settings {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 10px;
}

.setting label {
  font-weight: normal;
}

input[type="text"],
input[type="number"],
select,
textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-color);
  color: var(--text-color);
}

.checkbox-group, .radio-group {
  margin-top: 5px;
}

.checkbox-group label, .radio-group label {
  display: flex;
  align-items: center;
  font-weight: normal;
  margin-bottom: 5px;
}

.checkbox-group input, .radio-group input {
  margin-right: 8px;
}

.help-text {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 5px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.active-trainings {
  margin-top: 30px;
}

.active-trainings h3 {
  margin-bottom: 15px;
  color: var(--primary-color);
}

.trainings-list {
  background-color: var(--bg-secondary);
  border-radius: 8px;
  padding: 15px;
}

.training-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid var(--border-color);
}

.training-item:last-child {
  border-bottom: none;
}

.training-info {
  flex: 1;
}

.training-name {
  font-weight: bold;
}

.training-dataset {
  font-size: 12px;
  color: var(--text-secondary);
}

.training-progress {
  flex: 2;
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: var(--bg-color);
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: var(--primary-color);
}

.progress-text {
  width: 40px;
  text-align: right;
  font-size: 12px;
}

.training-status {
  width: 80px;
  text-align: center;
  font-size: 12px;
}

.training-actions {
  width: 80px;
  text-align: right;
}

.evaluation-results {
  margin-top: 30px;
}

.evaluation-results h3 {
  margin-bottom: 15px;
  color: var(--primary-color);
}

.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.metric-card {
  background-color: var(--bg-secondary);
  border-radius: 8px;
  padding: 15px;
  text-align: center;
}

.metric-title {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary-color);
}

.confusion-matrix {
  margin-bottom: 20px;
}

.confusion-matrix h4 {
  margin-bottom: 10px;
  color: var(--primary-color);
}

.matrix-container {
  background-color: var(--bg-secondary);
  border-radius: 8px;
  padding: 15px;
  height: 300px;
  /* هنا يمكن إضافة كود لعرض مصفوفة الارتباك */
}

.class-metrics h4 {
  margin-bottom: 10px;
  color: var(--primary-color);
}

.metrics-table {
  width: 100%;
  border-collapse: collapse;
}

.metrics-table th, .metrics-table td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.metrics-table th {
  background-color: var(--bg-secondary);
  font-weight: bold;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background-color: var(--bg-color);
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid var(--border-color);
}

.dialog-header h3 {
  margin: 0;
  color: var(--primary-color);
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--text-secondary);
}

.dialog-content {
  padding: 20px;
}

.dialog-footer {
  padding: 15px 20px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn.cancel {
  background-color: var(--bg-secondary);
  color: var(--text-color);
}

/* تخصيص للوضع الداكن */
:root[data-theme="dark"] .dataset-card,
:root[data-theme="dark"] .model-card,
:root[data-theme="dark"] .training-form,
:root[data-theme="dark"] .evaluation-form,
:root[data-theme="dark"] .trainings-list,
:root[data-theme="dark"] .metric-card,
:root[data-theme="dark"] .matrix-container {
  background-color: var(--bg-secondary-dark);
}

/* تخصيص للهوية البصرية */
:root[data-brand="gaaragroup"] .title,
:root[data-brand="gaaragroup"] .tab.active,
:root[data-brand="gaaragroup"] .training-form h3,
:root[data-brand="gaaragroup"] .evaluation-form h3,
:root[data-brand="gaaragroup"] .active-trainings h3,
:root[data-brand="gaaragroup"] .evaluation-results h3,
:root[data-brand="gaaragroup"] .confusion-matrix h4,
:root[data-brand="gaaragroup"] .class-metrics h4,
:root[data-brand="gaaragroup"] .dialog-header h3,
:root[data-brand="gaaragroup"] .metric-value {
  color: var(--gaara-primary);
}

:root[data-brand="gaaragroup"] .tab.active {
  border-bottom-color: var(--gaara-primary);
}

:root[data-brand="gaaragroup"] .btn.primary,
:root[data-brand="gaaragroup"] .badge,
:root[data-brand="gaaragroup"] .progress {
  background-color: var(--gaara-primary);
}

:root[data-brand="magseeds"] .title,
:root[data-brand="magseeds"] .tab.active,
:root[data-brand="magseeds"] .training-form h3,
:root[data-brand="magseeds"] .evaluation-form h3,
:root[data-brand="magseeds"] .active-trainings h3,
:root[data-brand="magseeds"] .evaluation-results h3,
:root[data-brand="magseeds"] .confusion-matrix h4,
:root[data-brand="magseeds"] .class-metrics h4,
:root[data-brand="magseeds"] .dialog-header h3,
:root[data-brand="magseeds"] .metric-value {
  color: var(--mag-primary);
}

:root[data-brand="magseeds"] .tab.active {
  border-bottom-color: var(--mag-primary);
}

:root[data-brand="magseeds"] .btn.primary,
:root[data-brand="magseeds"] .badge,
:root[data-brand="magseeds"] .progress {
  background-color: var(--mag-primary);
}
</style>
