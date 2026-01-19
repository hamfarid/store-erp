<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/diagnosis/DiagnosisResults.vue -->
<template>
  <div class="diagnosis-results-container">
    <v-card class="results-card">
      <v-card-title class="text-center primary--text">
        {{ title }}
        <v-spacer></v-spacer>
        <v-btn icon @click="$emit('close')" v-if="showCloseButton">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      
      <v-card-text v-if="isLoading" class="text-center pa-5">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
        <h3 class="mt-3">جاري تحليل البيانات...</h3>
        <p class="grey--text">يرجى الانتظار بينما نقوم بتحليل المعلومات المقدمة</p>
      </v-card-text>
      
      <template v-else>
        <v-card-text v-if="results.length > 0">
          <v-tabs v-model="activeResultTab">
            <v-tab v-for="(result, index) in results" :key="index">
              {{ result.disease.name }} ({{ Math.round(result.confidence * 100) }}%)
            </v-tab>
            
            <v-tab-item v-for="(result, index) in results" :key="index">
              <v-card flat>
                <v-card-text>
                  <h3 class="primary--text mb-2">{{ result.disease.name }}</h3>
                  <p v-if="result.disease.scientificName" class="subtitle-1 font-italic mb-4">{{ result.disease.scientificName }}</p>
                  
                  <v-chip
                    class="ma-1"
                    :color="getConfidenceColor(result.confidence)"
                    text-color="white"
                  >
                    مستوى الثقة: {{ Math.round(result.confidence * 100) }}%
                  </v-chip>
                  
                  <v-divider class="my-4"></v-divider>
                  
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
                  
                  <div v-if="result.aiAnalysis" class="mb-4">
                    <h4 class="subtitle-1 font-weight-bold">تحليل الذكاء الاصطناعي:</h4>
                    <v-alert
                      dense
                      text
                      color="info"
                      class="mt-2"
                    >
                      {{ result.aiAnalysis }}
                    </v-alert>
                  </div>
                </v-card-text>
                
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    text
                    @click="saveDiagnosis(result)"
                    :disabled="isSaving"
                    :loading="isSaving && savingResultId === result.disease.id"
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
                  <v-btn
                    color="primary"
                    text
                    @click="generateReport(result)"
                  >
                    <v-icon left>mdi-file-document</v-icon>
                    إنشاء تقرير
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
          
          <v-btn
            color="primary"
            class="mt-4"
            @click="$emit('retry')"
          >
            <v-icon left>mdi-refresh</v-icon>
            إعادة المحاولة
          </v-btn>
        </v-card-text>
      </template>
    </v-card>
    
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
    
    <!-- نافذة إنشاء التقرير -->
    <v-dialog v-model="showReportDialog" max-width="600px">
      <v-card>
        <v-card-title class="headline primary--text">
          إنشاء تقرير التشخيص
        </v-card-title>
        
        <v-card-text>
          <v-form ref="reportForm" v-model="isReportFormValid">
            <v-text-field
              v-model="reportTitle"
              label="عنوان التقرير"
              outlined
              dense
              :rules="[v => !!v || 'عنوان التقرير مطلوب']"
            ></v-text-field>
            
            <v-textarea
              v-model="reportNotes"
              label="ملاحظات إضافية"
              outlined
              rows="4"
            ></v-textarea>
            
            <v-checkbox
              v-model="includeImages"
              label="تضمين الصور في التقرير"
            ></v-checkbox>
            
            <v-checkbox
              v-model="includeReferences"
              label="تضمين المراجع في التقرير"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="showReportDialog = false"
          >
            إلغاء
          </v-btn>
          <v-btn
            color="primary"
            :disabled="!isReportFormValid || isGeneratingReport"
            :loading="isGeneratingReport"
            @click="downloadReport"
          >
            <v-icon left>mdi-download</v-icon>
            تنزيل التقرير
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
/**
 * مكون عرض نتائج التشخيص
 * 
 * يوفر هذا المكون واجهة لعرض نتائج تشخيص أمراض النباتات بتنسيق مفصل
 * مع إمكانية حفظ النتائج وإنشاء تقارير
 */
export default {
  name: 'DiagnosisResults',
  
  props: {
    /**
     * عنوان النتائج
     */
    title: {
      type: String,
      default: 'نتائج التشخيص'
    },
    
    /**
     * نتائج التشخيص
     */
    results: {
      type: Array,
      default: () => []
    },
    
    /**
     * حالة التحميل
     */
    isLoading: {
      type: Boolean,
      default: false
    },
    
    /**
     * إظهار زر الإغلاق
     */
    showCloseButton: {
      type: Boolean,
      default: true
    },
    
    /**
     * عنوان API لحفظ التشخيص
     */
    saveApiEndpoint: {
      type: String,
      default: '/api/disease-diagnosis/diagnoses'
    }
  },
  
  data() {
    return {
      activeResultTab: 0,
      showImagePreview: false,
      previewImageUrl: '',
      isSaving: false,
      savingResultId: null,
      
      // بيانات التقرير
      showReportDialog: false,
      reportTitle: '',
      reportNotes: '',
      includeImages: true,
      includeReferences: true,
      isReportFormValid: false,
      isGeneratingReport: false,
      
      // بيانات التشخيص الحالي للتقرير
      currentReportResult: null
    };
  },
  
  watch: {
    results: {
      immediate: true,
      handler(newResults) {
        if (newResults && newResults.length > 0) {
          // تعيين عنوان التقرير الافتراضي
          this.reportTitle = `تقرير تشخيص - ${newResults[0].disease.name}`;
        }
      }
    }
  },
  
  methods: {
    /**
     * الحصول على لون مستوى الثقة
     * @param {Number} confidence - مستوى الثقة (0-1)
     * @returns {String} - لون مستوى الثقة
     */
    getConfidenceColor(confidence) {
      if (confidence >= 0.9) {
        return 'success';
      } else if (confidence >= 0.7) {
        return 'primary';
      } else if (confidence >= 0.5) {
        return 'warning';
      } else {
        return 'error';
      }
    },
    
    /**
     * فتح معاينة الصورة
     * @param {String} url - رابط الصورة
     */
    openImagePreview(url) {
      this.previewImageUrl = url;
      this.showImagePreview = true;
    },
    
    /**
     * حفظ نتيجة التشخيص
     * @param {Object} result - نتيجة التشخيص المراد حفظها
     */
    async saveDiagnosis(result) {
      this.isSaving = true;
      this.savingResultId = result.disease.id;
      
      try {
        // هنا يتم إرسال البيانات إلى الخادم لحفظ التشخيص
        // في هذا المثال، نستخدم محاكاة للاستجابة
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // إرسال حدث النجاح
        this.$emit('save-success', {
          message: 'تم حفظ نتيجة التشخيص بنجاح',
          result
        });
      } catch (error) {
        console.error('خطأ في حفظ نتيجة التشخيص:', error);
        
        // إرسال حدث الخطأ
        this.$emit('save-error', {
          message: 'حدث خطأ أثناء حفظ نتيجة التشخيص',
          error
        });
      } finally {
        this.isSaving = false;
        this.savingResultId = null;
      }
    },
    
    /**
     * البحث عن معلومات إضافية حول المرض
     * @param {Object} disease - المرض المراد البحث عنه
     */
    searchMoreInfo(disease) {
      // إنشاء استعلام البحث
      const searchQuery = `${disease.name} ${disease.scientificName || ''} أعراض علاج`;
      
      // فتح نافذة بحث جديدة
      window.open(`https://www.google.com/search?q=${encodeURIComponent(searchQuery)}`, '_blank');
      
      // إرسال حدث البحث
      this.$emit('search', {
        disease,
        query: searchQuery
      });
    },
    
    /**
     * إنشاء تقرير للتشخيص
     * @param {Object} result - نتيجة التشخيص المراد إنشاء تقرير لها
     */
    generateReport(result) {
      this.currentReportResult = result;
      this.reportTitle = `تقرير تشخيص - ${result.disease.name}`;
      this.reportNotes = '';
      this.showReportDialog = true;
    },
    
    /**
     * تنزيل تقرير التشخيص
     */
    async downloadReport() {
      if (!this.$refs.reportForm.validate() || !this.currentReportResult) {
        return;
      }
      
      this.isGeneratingReport = true;
      
      try {
        // هنا يتم إنشاء التقرير وتنزيله
        // في هذا المثال، نستخدم محاكاة للعملية
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // إرسال حدث نجاح إنشاء التقرير
        this.$emit('report-success', {
          message: 'تم إنشاء التقرير بنجاح',
          reportData: {
            title: this.reportTitle,
            notes: this.reportNotes,
            includeImages: this.includeImages,
            includeReferences: this.includeReferences,
            result: this.currentReportResult
          }
        });
        
        // إغلاق نافذة إنشاء التقرير
        this.showReportDialog = false;
      } catch (error) {
        console.error('خطأ في إنشاء التقرير:', error);
        
        // إرسال حدث الخطأ
        this.$emit('report-error', {
          message: 'حدث خطأ أثناء إنشاء التقرير',
          error
        });
      } finally {
        this.isGeneratingReport = false;
      }
    }
  }
};
</script>

<style scoped>
.diagnosis-results-container {
  max-width: 800px;
  margin: 0 auto;
}

.results-card {
  border-radius: 8px;
  overflow: hidden;
}
</style>
