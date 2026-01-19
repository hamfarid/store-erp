<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/diagnosis/DiagnosisForm.vue -->
<template>
  <div class="diagnosis-form-container">
    <v-card class="diagnosis-card">
      <v-card-title class="text-center primary--text">
        {{ title }}
      </v-card-title>
      
      <v-card-text>
        <v-form ref="form" v-model="isFormValid" lazy-validation>
          <!-- اختيار المحصول -->
          <v-autocomplete
            v-model="selectedCrop"
            :items="crops"
            item-text="name"
            item-value="id"
            label="اختر المحصول"
            outlined
            dense
            :loading="isLoadingCrops"
            :disabled="isProcessing"
            :rules="[v => !!v || 'يرجى اختيار المحصول']"
            @change="onCropChange"
          >
            <template v-slot:item="{ item }">
              <v-list-item-content>
                <v-list-item-title>{{ item.name }}</v-list-item-title>
                <v-list-item-subtitle v-if="item.scientificName">{{ item.scientificName }}</v-list-item-subtitle>
              </v-list-item-content>
            </template>
          </v-autocomplete>
          
          <!-- إدخال الأعراض -->
          <v-textarea
            v-model="symptoms"
            outlined
            label="أعراض المرض"
            hint="أدخل الأعراض مفصولة بفواصل"
            :disabled="isProcessing"
            :rules="[v => !!v || !!(selectedImage || selectedImages.length > 0) || 'يجب إدخال الأعراض أو تحميل صورة']"
            rows="3"
          ></v-textarea>
          
          <!-- تحميل الصور -->
          <div class="image-upload-section mt-4">
            <v-file-input
              v-model="selectedImages"
              outlined
              dense
              label="تحميل صور للتشخيص"
              prepend-icon="mdi-camera"
              accept="image/*"
              :disabled="isProcessing"
              multiple
              show-size
              counter
              truncate-length="15"
              @change="onImagesSelected"
            ></v-file-input>
            
            <!-- عرض الصور المختارة -->
            <div v-if="selectedImages.length > 0" class="selected-images-preview mt-2">
              <v-row>
                <v-col
                  v-for="(image, index) in imagePreviews"
                  :key="index"
                  cols="6"
                  sm="4"
                  md="3"
                >
                  <v-card class="image-preview-card">
                    <v-img
                      :src="image"
                      aspect-ratio="1"
                      class="grey lighten-2"
                      contain
                    ></v-img>
                    <v-card-actions class="pa-0">
                      <v-btn
                        icon
                        small
                        color="error"
                        @click="removeImage(index)"
                        :disabled="isProcessing"
                      >
                        <v-icon small>mdi-close</v-icon>
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </div>
          
          <!-- خيارات متقدمة -->
          <v-expansion-panels v-if="showAdvancedOptions" class="mt-4">
            <v-expansion-panel>
              <v-expansion-panel-header>خيارات متقدمة</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-checkbox
                  v-model="useAI"
                  label="استخدام الذكاء الاصطناعي للتشخيص"
                  :disabled="isProcessing"
                ></v-checkbox>
                
                <v-select
                  v-if="useAI"
                  v-model="selectedModel"
                  :items="aiModels"
                  item-text="name"
                  item-value="id"
                  label="نموذج الذكاء الاصطناعي"
                  outlined
                  dense
                  :disabled="isProcessing"
                ></v-select>
                
                <v-checkbox
                  v-model="searchExternalSources"
                  label="البحث في مصادر خارجية"
                  :disabled="isProcessing"
                ></v-checkbox>
                
                <v-slider
                  v-model="confidenceThreshold"
                  label="حد الثقة الأدنى"
                  thumb-label="always"
                  :min="0"
                  :max="100"
                  :disabled="isProcessing"
                ></v-slider>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-form>
      </v-card-text>
      
      <v-card-actions class="justify-center pa-4">
        <v-btn
          color="error"
          outlined
          :disabled="!isProcessing"
          @click="cancelDiagnosis"
          class="mx-2"
        >
          <v-icon left>mdi-cancel</v-icon>
          إلغاء
        </v-btn>
        
        <v-btn
          color="primary"
          :loading="isProcessing"
          :disabled="!isFormValid || isProcessing"
          @click="submitDiagnosis"
          class="mx-2"
        >
          <v-icon left>mdi-magnify</v-icon>
          تشخيص
        </v-btn>
      </v-card-actions>
    </v-card>
    
    <!-- عرض نتائج التشخيص -->
    <v-dialog v-model="showResults" max-width="800">
      <v-card>
        <v-card-title class="headline primary--text">
          نتائج التشخيص
          <v-spacer></v-spacer>
          <v-btn icon @click="showResults = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text v-if="diagnosisResults.length > 0">
          <v-tabs v-model="activeResultTab">
            <v-tab v-for="(result, index) in diagnosisResults" :key="index">
              {{ result.disease.name }} ({{ Math.round(result.confidence * 100) }}%)
            </v-tab>
            
            <v-tab-item v-for="(result, index) in diagnosisResults" :key="index">
              <v-card flat>
                <v-card-text>
                  <h3 class="primary--text mb-2">{{ result.disease.name }}</h3>
                  <p v-if="result.disease.scientificName" class="subtitle-1 font-italic mb-4">{{ result.disease.scientificName }}</p>
                  
                  <v-divider class="mb-4"></v-divider>
                  
                  <div class="mb-4">
                    <h4 class="subtitle-1 font-weight-bold">الوصف:</h4>
                    <p>{{ result.disease.description || 'لا يوجد وصف متاح' }}</p>
                  </div>
                  
                  <div class="mb-4">
                    <h4 class="subtitle-1 font-weight-bold">الأعراض:</h4>
                    <ul v-if="result.disease.symptoms && result.disease.symptoms.length">
                      <li v-for="(symptom, i) in result.disease.symptoms" :key="i">{{ symptom }}</li>
                    </ul>
                    <p v-else>لا توجد أعراض مسجلة</p>
                  </div>
                  
                  <div class="mb-4">
                    <h4 class="subtitle-1 font-weight-bold">العلاج الموصى به:</h4>
                    <ul v-if="result.disease.treatments && result.disease.treatments.length">
                      <li v-for="(treatment, i) in result.disease.treatments" :key="i">{{ treatment }}</li>
                    </ul>
                    <p v-else>لا توجد علاجات مسجلة</p>
                  </div>
                  
                  <div class="mb-4">
                    <h4 class="subtitle-1 font-weight-bold">الإجراءات الوقائية:</h4>
                    <ul v-if="result.disease.preventiveMeasures && result.disease.preventiveMeasures.length">
                      <li v-for="(measure, i) in result.disease.preventiveMeasures" :key="i">{{ measure }}</li>
                    </ul>
                    <p v-else>لا توجد إجراءات وقائية مسجلة</p>
                  </div>
                  
                  <div v-if="result.disease.references && result.disease.references.length" class="mb-4">
                    <h4 class="subtitle-1 font-weight-bold">المراجع:</h4>
                    <ul>
                      <li v-for="(reference, i) in result.disease.references" :key="i">
                        <a :href="reference.url" target="_blank" rel="noopener noreferrer">{{ reference.title || reference.url }}</a>
                      </li>
                    </ul>
                  </div>
                  
                  <div v-if="result.similarImages && result.similarImages.length" class="mb-4">
                    <h4 class="subtitle-1 font-weight-bold">صور مشابهة:</h4>
                    <v-row>
                      <v-col
                        v-for="(image, i) in result.similarImages"
                        :key="i"
                        cols="6"
                        sm="4"
                        md="3"
                      >
                        <v-img
                          :src="image.url"
                          aspect-ratio="1"
                          class="grey lighten-2"
                          contain
                          @click="openImagePreview(image.url)"
                        ></v-img>
                      </v-col>
                    </v-row>
                  </div>
                </v-card-text>
                
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    text
                    @click="saveDiagnosis(result)"
                  >
                    <v-icon left>mdi-content-save</v-icon>
                    حفظ التشخيص
                  </v-btn>
                  <v-btn
                    color="primary"
                    text
                    @click="searchMoreInfo(result.disease)"
                  >
                    <v-icon left>mdi-magnify</v-icon>
                    بحث عن معلومات إضافية
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-tab-item>
          </v-tabs>
        </v-card-text>
        
        <v-card-text v-else class="text-center pa-5">
          <v-icon size="64" color="warning">mdi-alert-circle-outline</v-icon>
          <h3 class="mt-3">لم يتم العثور على نتائج</h3>
          <p class="grey--text">لم نتمكن من تشخيص المرض بناءً على المعلومات المقدمة. يرجى تقديم المزيد من التفاصيل أو صور أوضح.</p>
        </v-card-text>
      </v-card>
    </v-dialog>
    
    <!-- عرض الصورة بحجم كبير -->
    <v-dialog v-model="showImagePreview" max-width="90vw">
      <v-card>
        <v-img
          :src="previewImageUrl"
          contain
          max-height="80vh"
        ></v-img>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            icon
            @click="showImagePreview = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
/**
 * مكون نموذج التشخيص
 * 
 * يوفر هذا المكون واجهة لتشخيص أمراض النباتات من خلال إدخال الأعراض وتحميل الصور
 * ويعرض نتائج التشخيص بتنسيق مفصل
 */
export default {
  name: 'DiagnosisForm',
  
  props: {
    /**
     * عنوان النموذج
     */
    title: {
      type: String,
      default: 'تشخيص أمراض النباتات'
    },
    
    /**
     * إظهار الخيارات المتقدمة
     */
    showAdvancedOptions: {
      type: Boolean,
      default: true
    },
    
    /**
     * عنوان API للتشخيص
     */
    apiEndpoint: {
      type: String,
      default: '/api/disease-diagnosis/diagnose'
    }
  },
  
  data() {
    return {
      // بيانات النموذج
      isFormValid: false,
      selectedCrop: null,
      symptoms: '',
      selectedImages: [],
      imagePreviews: [],
      
      // خيارات متقدمة
      useAI: true,
      selectedModel: 'default',
      searchExternalSources: false,
      confidenceThreshold: 50,
      
      // حالة النموذج
      isProcessing: false,
      isLoadingCrops: false,
      
      // بيانات المحاصيل والنماذج
      crops: [],
      aiModels: [
        { id: 'default', name: 'النموذج الافتراضي' },
        { id: 'resnet50', name: 'ResNet50' },
        { id: 'efficientnet', name: 'EfficientNet' },
        { id: 'vit', name: 'Vision Transformer' }
      ],
      
      // نتائج التشخيص
      showResults: false,
      diagnosisResults: [],
      activeResultTab: 0,
      
      // عرض الصورة
      showImagePreview: false,
      previewImageUrl: ''
    };
  },
  
  created() {
    // تحميل بيانات المحاصيل عند إنشاء المكون
    this.loadCrops();
  },
  
  methods: {
    /**
     * تحميل بيانات المحاصيل من الخادم
     */
    async loadCrops() {
      this.isLoadingCrops = true;
      try {
        // هنا يتم الاتصال بالخادم لتحميل بيانات المحاصيل
        // في هذا المثال، نستخدم بيانات وهمية
        setTimeout(() => {
          this.crops = [
            { id: 1, name: 'طماطم', scientificName: 'Solanum lycopersicum' },
            { id: 2, name: 'خيار', scientificName: 'Cucumis sativus' },
            { id: 3, name: 'بطاطس', scientificName: 'Solanum tuberosum' },
            { id: 4, name: 'باذنجان', scientificName: 'Solanum melongena' },
            { id: 5, name: 'فلفل', scientificName: 'Capsicum annuum' },
            { id: 6, name: 'قمح', scientificName: 'Triticum aestivum' },
            { id: 7, name: 'ذرة', scientificName: 'Zea mays' },
            { id: 8, name: 'أرز', scientificName: 'Oryza sativa' }
          ];
          this.isLoadingCrops = false;
        }, 1000);
      } catch (error) {
        console.error('خطأ في تحميل بيانات المحاصيل:', error);
        this.isLoadingCrops = false;
      }
    },
    
    /**
     * معالجة تغيير المحصول المحدد
     */
    onCropChange() {
      // يمكن إضافة منطق إضافي هنا، مثل تحميل الأمراض الشائعة للمحصول المحدد
    },
    
    /**
     * معالجة اختيار الصور
     */
    onImagesSelected() {
      // إنشاء معاينات للصور المحددة
      this.imagePreviews = [];
      
      if (this.selectedImages && this.selectedImages.length > 0) {
        for (const file of this.selectedImages) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.imagePreviews.push(e.target.result);
          };
          reader.readAsDataURL(file);
        }
      }
    },
    
    /**
     * إزالة صورة من القائمة
     * @param {Number} index - فهرس الصورة المراد إزالتها
     */
    removeImage(index) {
      // إنشاء نسخة جديدة من المصفوفات لتجنب مشاكل التفاعلية
      const newSelectedImages = [...this.selectedImages];
      const newImagePreviews = [...this.imagePreviews];
      
      // إزالة الصورة من المصفوفات
      newSelectedImages.splice(index, 1);
      newImagePreviews.splice(index, 1);
      
      // تحديث البيانات
      this.selectedImages = newSelectedImages;
      this.imagePreviews = newImagePreviews;
    },
    
    /**
     * إرسال طلب التشخيص
     */
    async submitDiagnosis() {
      // التحقق من صحة النموذج
      if (!this.$refs.form.validate()) {
        return;
      }
      
      // التحقق من وجود أعراض أو صور
      if (!this.symptoms && this.selectedImages.length === 0) {
        this.$emit('error', 'يجب إدخال الأعراض أو تحميل صورة على الأقل');
        return;
      }
      
      this.isProcessing = true;
      
      try {
        // إنشاء كائن FormData لإرسال البيانات والملفات
        const formData = new FormData();
        formData.append('crop_id', this.selectedCrop);
        formData.append('symptoms', this.symptoms);
        formData.append('use_ai', this.useAI);
        formData.append('model_id', this.selectedModel);
        formData.append('search_external', this.searchExternalSources);
        formData.append('confidence_threshold', this.confidenceThreshold / 100);
        
        // إضافة الصور
        for (const image of this.selectedImages) {
          formData.append('images', image);
        }
        
        // هنا يتم إرسال البيانات إلى الخادم
        // في هذا المثال، نستخدم بيانات وهمية
        setTimeout(() => {
          // محاكاة استجابة الخادم
          this.diagnosisResults = [
            {
              disease: {
                id: 1,
                name: 'اللفحة المتأخرة',
                scientificName: 'Phytophthora infestans',
                description: 'اللفحة المتأخرة هي مرض فطري يصيب النباتات من عائلة الباذنجانيات، وخاصة الطماطم والبطاطس. يمكن أن يتسبب في خسائر كبيرة في المحصول إذا لم يتم التحكم فيه.',
                symptoms: [
                  'بقع بنية أو سوداء على الأوراق',
                  'بقع مائية على الثمار',
                  'تعفن الأوراق والسيقان',
                  'ظهور نمو أبيض على السطح السفلي للأوراق في الظروف الرطبة'
                ],
                treatments: [
                  'استخدام المبيدات الفطرية الوقائية',
                  'إزالة النباتات المصابة وحرقها',
                  'تجنب الري العلوي وتقليل الرطوبة',
                  'زراعة أصناف مقاومة للمرض'
                ],
                preventiveMeasures: [
                  'استخدام بذور معتمدة وخالية من المرض',
                  'تناوب المحاصيل',
                  'تحسين تهوية النباتات',
                  'تجنب الزراعة في المناطق المنخفضة والرطبة'
                ],
                references: [
                  { title: 'دليل أمراض الطماطم', url: 'https://example.com/tomato-diseases' },
                  { title: 'مكافحة اللفحة المتأخرة', url: 'https://example.com/late-blight-control' }
                ]
              },
              confidence: 0.92,
              similarImages: [
                { url: 'https://example.com/images/late-blight-1.jpg' },
                { url: 'https://example.com/images/late-blight-2.jpg' }
              ]
            },
            {
              disease: {
                id: 2,
                name: 'البياض الدقيقي',
                scientificName: 'Erysiphe cichoracearum',
                description: 'البياض الدقيقي هو مرض فطري شائع يصيب مجموعة واسعة من النباتات. يظهر على شكل بقع بيضاء مسحوقية على الأوراق والسيقان والثمار.',
                symptoms: [
                  'بقع بيضاء مسحوقية على الأوراق',
                  'تشوه الأوراق والبراعم',
                  'اصفرار الأوراق وسقوطها',
                  'ضعف عام في النبات'
                ],
                treatments: [
                  'استخدام المبيدات الفطرية',
                  'رش محلول بيكربونات الصوديوم',
                  'استخدام الزيوت النباتية مثل زيت النيم',
                  'إزالة الأجزاء المصابة من النبات'
                ],
                preventiveMeasures: [
                  'زراعة أصناف مقاومة',
                  'تحسين تهوية النباتات',
                  'تجنب الري العلوي',
                  'تجنب الإفراط في استخدام الأسمدة النيتروجينية'
                ],
                references: [
                  { title: 'مكافحة البياض الدقيقي', url: 'https://example.com/powdery-mildew-control' }
                ]
              },
              confidence: 0.78,
              similarImages: [
                { url: 'https://example.com/images/powdery-mildew-1.jpg' }
              ]
            }
          ];
          
          this.showResults = true;
          this.isProcessing = false;
        }, 2000);
        
      } catch (error) {
        console.error('خطأ في إرسال طلب التشخيص:', error);
        this.$emit('error', 'حدث خطأ أثناء معالجة طلب التشخيص');
        this.isProcessing = false;
      }
    },
    
    /**
     * إلغاء عملية التشخيص الجارية
     */
    cancelDiagnosis() {
      // هنا يمكن إضافة منطق لإلغاء الطلب الجاري
      this.isProcessing = false;
      this.$emit('cancel');
    },
    
    /**
     * حفظ نتيجة التشخيص
     * @param {Object} result - نتيجة التشخيص المراد حفظها
     */
    saveDiagnosis(result) {
      // هنا يمكن إضافة منطق لحفظ نتيجة التشخيص
      this.$emit('save', result);
      
      // إظهار رسالة نجاح
      this.$emit('success', 'تم حفظ نتيجة التشخيص بنجاح');
    },
    
    /**
     * البحث عن معلومات إضافية حول المرض
     * @param {Object} disease - المرض المراد البحث عنه
     */
    searchMoreInfo(disease) {
      // هنا يمكن إضافة منطق للبحث عن معلومات إضافية
      const searchQuery = `${disease.name} ${disease.scientificName || ''} أعراض علاج`;
      
      // فتح نافذة بحث جديدة
      window.open(`https://www.google.com/search?q=${encodeURIComponent(searchQuery)}`, '_blank');
    },
    
    /**
     * فتح معاينة الصورة
     * @param {String} url - رابط الصورة
     */
    openImagePreview(url) {
      this.previewImageUrl = url;
      this.showImagePreview = true;
    }
  }
};
</script>

<style scoped>
.diagnosis-form-container {
  max-width: 800px;
  margin: 0 auto;
}

.diagnosis-card {
  border-radius: 8px;
  overflow: hidden;
}

.image-preview-card {
  position: relative;
  overflow: hidden;
  border-radius: 4px;
}

.selected-images-preview {
  max-height: 300px;
  overflow-y: auto;
}
</style>
