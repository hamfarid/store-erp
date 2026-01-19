<!--
مكون تحليل أنماط الانتباه
يوفر هذا المكون واجهة تفاعلية لتحليل أنماط الانتباه في نماذج تشخيص أمراض النباتات
ويتيح للمستخدمين تحميل الصور واختيار النماذج وعرض نتائج التحليل بشكل مرئي

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="attention-analysis-tool">
    <v-card class="mb-4">
      <v-card-title class="primary--text">
        <v-icon large color="primary" class="ml-2">mdi-eye-outline</v-icon>
        تحليل أنماط الانتباه
      </v-card-title>
      <v-card-subtitle>
        تحليل كيفية تركيز النماذج على مناطق محددة في الصور عند تشخيص أمراض النباتات
      </v-card-subtitle>
      <v-card-text>
        <v-alert
          v-if="error"
          type="error"
          dense
          dismissible
          class="mb-4"
        >
          {{ error }}
        </v-alert>

        <!-- قسم اختيار النماذج والصور -->
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedModels"
              :items="availableModels"
              item-text="name"
              item-value="name"
              label="اختر النماذج للتحليل"
              multiple
              chips
              :disabled="loading"
              :rules="[v => v.length > 0 || 'يرجى اختيار نموذج واحد على الأقل']"
            >
              <template v-slot:selection="{ item, index }">
                <v-chip v-if="index < 3" small>
                  {{ item.name }}
                </v-chip>
                <span v-if="index === 3" class="grey--text caption">
                  (+{{ selectedModels.length - 3 }} أخرى)
                </span>
              </template>
            </v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-file-input
              v-model="selectedFiles"
              label="اختر صور للتحليل"
              multiple
              chips
              accept="image/*"
              :disabled="loading"
              :rules="[v => v.length > 0 || 'يرجى اختيار صورة واحدة على الأقل']"
              show-size
              counter
            ></v-file-input>
          </v-col>
        </v-row>

        <!-- أزرار التحكم -->
        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="!canAnalyze"
              @click="analyzeAttention"
              block
            >
              <v-icon left>mdi-magnify</v-icon>
              تحليل أنماط الانتباه
            </v-btn>
          </v-col>
          <v-col cols="12" md="6">
            <v-btn
              color="secondary"
              :loading="loading"
              :disabled="!canCompare"
              @click="compareAttentionPatterns"
              block
            >
              <v-icon left>mdi-compare</v-icon>
              مقارنة أنماط الانتباه
            </v-btn>
          </v-col>
        </v-row>

        <!-- شريط التقدم -->
        <v-progress-linear
          v-if="loading"
          indeterminate
          color="primary"
          class="mt-4"
        ></v-progress-linear>
      </v-card-text>
    </v-card>

    <!-- عرض نتائج التحليل -->
    <v-card v-if="analysisResults.length > 0" class="mb-4">
      <v-card-title class="primary--text">
        <v-icon large color="primary" class="ml-2">mdi-chart-areaspline</v-icon>
        نتائج تحليل الانتباه
      </v-card-title>
      <v-card-text>
        <v-tabs v-model="activeTab" background-color="transparent" grow>
          <v-tab v-for="(result, index) in analysisResults" :key="index">
            {{ result.model_name }}
          </v-tab>
          <v-tab v-if="comparisonResult">
            مقارنة النماذج
          </v-tab>

          <!-- محتوى التبويبات -->
          <v-tab-item v-for="(result, index) in analysisResults" :key="index">
            <v-card flat>
              <v-card-text>
                <h3 class="text-h5 mb-4">تحليل أنماط الانتباه للنموذج: {{ result.model_name }}</h3>
                
                <!-- إحصائيات الانتباه -->
                <v-row>
                  <v-col cols="12" md="6">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">إحصائيات الانتباه</v-card-title>
                      <v-card-text>
                        <v-simple-table>
                          <template v-slot:default>
                            <tbody>
                              <tr v-for="(value, key) in getAttentionStatistics(result)" :key="key">
                                <td>{{ formatStatName(key) }}</td>
                                <td>{{ formatStatValue(value) }}</td>
                              </tr>
                            </tbody>
                          </template>
                        </v-simple-table>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">توزيع التركيز</v-card-title>
                      <v-card-text>
                        <div class="focus-distribution-grid">
                          <div 
                            v-for="i in 3" 
                            :key="`row_${i}`"
                            class="focus-row"
                          >
                            <div 
                              v-for="j in 3" 
                              :key="`${i}_${j}`"
                              class="focus-cell"
                              :style="getFocusCellStyle(result, i-1, j-1)"
                            >
                              {{ getFocusCellValue(result, i-1, j-1) }}
                            </div>
                          </div>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- التفسيرات البصرية -->
                <h4 class="text-h6 mt-6 mb-3">التفسيرات البصرية</h4>
                <v-row>
                  <v-col 
                    v-for="(path, imgId) in result.visual_explanations" 
                    :key="imgId"
                    cols="12" sm="6" md="4"
                  >
                    <v-card outlined>
                      <v-img
                        :src="getImageUrl(path)"
                        aspect-ratio="1"
                        class="grey lighten-2"
                        contain
                      >
                        <template v-slot:placeholder>
                          <v-row
                            class="fill-height ma-0"
                            align="center"
                            justify="center"
                          >
                            <v-progress-circular indeterminate color="primary"></v-progress-circular>
                          </v-row>
                        </template>
                      </v-img>
                      <v-card-text class="text-center">
                        {{ imgId }}
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>

          <!-- تبويب المقارنة -->
          <v-tab-item v-if="comparisonResult">
            <v-card flat>
              <v-card-text>
                <h3 class="text-h5 mb-4">مقارنة أنماط الانتباه بين النماذج</h3>
                
                <!-- مخطط المقارنة -->
                <v-row>
                  <v-col cols="12">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">مخطط مقارنة أنماط الانتباه</v-card-title>
                      <v-card-text>
                        <v-img
                          v-if="comparisonResult.comparison_chart_path"
                          :src="getImageUrl(comparisonResult.comparison_chart_path)"
                          max-height="500"
                          contain
                        ></v-img>
                        <div v-else class="text-center pa-4">
                          لا يوجد مخطط مقارنة متاح
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- جدول المقارنة -->
                <v-row class="mt-4">
                  <v-col cols="12">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">جدول مقارنة أنماط الانتباه</v-card-title>
                      <v-card-text>
                        <v-data-table
                          :headers="comparisonHeaders"
                          :items="comparisonItems"
                          :items-per-page="10"
                          class="elevation-1"
                        ></v-data-table>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </v-card-text>
    </v-card>

    <!-- عرض التقارير السابقة -->
    <v-card v-if="previousReports.length > 0">
      <v-card-title class="primary--text">
        <v-icon large color="primary" class="ml-2">mdi-history</v-icon>
        تقارير تحليل الانتباه السابقة
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="reportHeaders"
          :items="previousReports"
          :items-per-page="5"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn
              small
              color="primary"
              text
              @click="viewReport(item)"
            >
              <v-icon small>mdi-eye</v-icon>
              عرض
            </v-btn>
            <v-btn
              small
              color="secondary"
              text
              @click="downloadReport(item)"
            >
              <v-icon small>mdi-download</v-icon>
              تحميل
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'AttentionAnalysisTool',
  
  data() {
    return {
      selectedModels: [],
      selectedFiles: [],
      loading: false,
      error: null,
      analysisResults: [],
      comparisonResult: null,
      activeTab: 0,
      previousReports: [],
      reportHeaders: [
        { text: 'النموذج', value: 'model_name' },
        { text: 'التاريخ', value: 'timestamp' },
        { text: 'النوع', value: 'type' },
        { text: 'الإجراءات', value: 'actions', sortable: false }
      ],
      comparisonHeaders: [
        { text: 'النموذج', value: 'model' },
        { text: 'نسبة التركيز', value: 'focus_ratio' },
        { text: 'انتشار الانتباه', value: 'attention_spread' },
        { text: 'إنتروبيا الانتباه', value: 'attention_entropy' }
      ]
    };
  },
  
  computed: {
    ...mapGetters({
      availableModels: 'plantDisease/getAvailableModels'
    }),
    
    canAnalyze() {
      return this.selectedModels.length > 0 && this.selectedFiles && this.selectedFiles.length > 0;
    },
    
    canCompare() {
      return this.selectedModels.length > 1 && this.selectedFiles && this.selectedFiles.length > 0;
    },
    
    comparisonItems() {
      if (!this.comparisonResult || !this.comparisonResult.comparison_data) {
        return [];
      }
      
      const items = [];
      for (const [model, data] of Object.entries(this.comparisonResult.comparison_data)) {
        const focusRatio = data.focus_ratio ? 
          `${(data.focus_ratio.mean * 100).toFixed(2)}% ± ${(data.focus_ratio.std * 100).toFixed(2)}%` : 'غير متاح';
        
        const attentionSpread = data.attention_spread ? 
          `${data.attention_spread.mean.toFixed(3)} ± ${data.attention_spread.std.toFixed(3)}` : 'غير متاح';
        
        const attentionEntropy = data.attention_entropy ? 
          `${data.attention_entropy.mean.toFixed(3)} ± ${data.attention_entropy.std.toFixed(3)}` : 'غير متاح';
        
        items.push({
          model,
          focus_ratio: focusRatio,
          attention_spread: attentionSpread,
          attention_entropy: attentionEntropy
        });
      }
      
      return items;
    }
  },
  
  mounted() {
    this.fetchAvailableModels();
    this.fetchPreviousReports();
  },
  
  methods: {
    async fetchAvailableModels() {
      try {
        await this.$store.dispatch('plantDisease/fetchAvailableModels');
      } catch (error) {
        this.error = `خطأ في جلب النماذج المتاحة: ${error.message}`;
      }
    },
    
    async fetchPreviousReports() {
      try {
        const response = await this.$store.dispatch('plantDisease/fetchAttentionReports');
        this.previousReports = response.reports.map(report => ({
          ...report,
          type: report.model_name === 'مقارنة' ? 'مقارنة' : 'تحليل'
        }));
      } catch (error) {
        this.error = `خطأ في جلب التقارير السابقة: ${error.message}`;
      }
    },
    
    async analyzeAttention() {
      if (!this.canAnalyze) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        // تحميل الصور أولاً
        const uploadResult = await this.uploadImages();
        
        if (!uploadResult || !uploadResult.image_paths || uploadResult.image_paths.length === 0) {
          throw new Error('فشل في تحميل الصور');
        }
        
        // تحليل أنماط الانتباه لكل نموذج
        this.analysisResults = [];
        
        for (const model of this.selectedModels) {
          const result = await this.$store.dispatch('plantDisease/analyzeAttention', {
            model_name: model,
            image_paths: uploadResult.image_paths
          });
          
          if (result.error) {
            throw new Error(`فشل في تحليل أنماط الانتباه للنموذج ${model}: ${result.error}`);
          }
          
          this.analysisResults.push(result);
        }
        
        // تحديث التقارير السابقة
        await this.fetchPreviousReports();
        
        // تعيين التبويب النشط
        this.activeTab = 0;
        
      } catch (error) {
        this.error = `خطأ في تحليل أنماط الانتباه: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async compareAttentionPatterns() {
      if (!this.canCompare) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        // تحميل الصور أولاً
        const uploadResult = await this.uploadImages();
        
        if (!uploadResult || !uploadResult.image_paths || uploadResult.image_paths.length === 0) {
          throw new Error('فشل في تحميل الصور');
        }
        
        // مقارنة أنماط الانتباه بين النماذج
        const result = await this.$store.dispatch('plantDisease/compareAttentionPatterns', {
          models: this.selectedModels,
          image_paths: uploadResult.image_paths
        });
        
        if (result.error) {
          throw new Error(`فشل في مقارنة أنماط الانتباه: ${result.error}`);
        }
        
        this.comparisonResult = result;
        
        // تحليل أنماط الانتباه لكل نموذج
        await this.analyzeAttention();
        
        // تعيين التبويب النشط للمقارنة
        this.activeTab = this.analysisResults.length;
        
      } catch (error) {
        this.error = `خطأ في مقارنة أنماط الانتباه: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async uploadImages() {
      if (!this.selectedFiles || this.selectedFiles.length === 0) {
        return null;
      }
      
      const formData = new FormData();
      this.selectedFiles.forEach((file, index) => {
        formData.append(`image_${index}`, file);
      });
      
      return await this.$store.dispatch('plantDisease/uploadTestImages', formData);
    },
    
    getAttentionStatistics(result) {
      if (!result || !result.attention_statistics) {
        return {};
      }
      
      const stats = {};
      
      // استخراج الإحصائيات المهمة
      if (result.attention_statistics.focus_ratio) {
        stats.focus_ratio = result.attention_statistics.focus_ratio.mean;
        stats.focus_ratio_std = result.attention_statistics.focus_ratio.std;
      }
      
      if (result.attention_statistics.attention_spread) {
        stats.attention_spread = result.attention_statistics.attention_spread.mean;
        stats.attention_spread_std = result.attention_statistics.attention_spread.std;
      }
      
      if (result.attention_statistics.attention_entropy) {
        stats.attention_entropy = result.attention_statistics.attention_entropy.mean;
        stats.attention_entropy_std = result.attention_statistics.attention_entropy.std;
      }
      
      return stats;
    },
    
    formatStatName(key) {
      const nameMap = {
        focus_ratio: 'نسبة التركيز',
        focus_ratio_std: 'انحراف نسبة التركيز',
        attention_spread: 'انتشار الانتباه',
        attention_spread_std: 'انحراف انتشار الانتباه',
        attention_entropy: 'إنتروبيا الانتباه',
        attention_entropy_std: 'انحراف إنتروبيا الانتباه'
      };
      
      return nameMap[key] || key;
    },
    
    formatStatValue(value) {
      if (value === undefined || value === null) {
        return 'غير متاح';
      }
      
      if (typeof value === 'number') {
        // تنسيق النسب المئوية
        if (value >= 0 && value <= 1) {
          return `${(value * 100).toFixed(2)}%`;
        }
        
        // تنسيق القيم العشرية
        return value.toFixed(3);
      }
      
      return value.toString();
    },
    
    getFocusCellStyle(result, i, j) {
      if (!result || !result.focus_regions) {
        return {};
      }
      
      // البحث عن بيانات توزيع التركيز للصورة الأولى
      const firstImageKey = Object.keys(result.focus_regions)[0];
      if (!firstImageKey || !result.focus_regions[firstImageKey]) {
        return {};
      }
      
      const focusDistribution = result.focus_regions[firstImageKey].focus_distribution;
      if (!focusDistribution) {
        return {};
      }
      
      const regionKey = `region_${i}_${j}`;
      const value = focusDistribution[regionKey] || 0;
      
      // تحويل القيمة إلى لون (من الأزرق الفاتح إلى الأحمر الداكن)
      const intensity = Math.min(value * 2, 1); // تضخيم القيمة للحصول على ألوان أوضح
      const r = Math.floor(255 * intensity);
      const g = Math.floor(100 * (1 - intensity));
      const b = Math.floor(100 * (1 - intensity));
      
      return {
        backgroundColor: `rgba(${r}, ${g}, ${b}, 0.7)`,
        color: intensity > 0.5 ? 'white' : 'black'
      };
    },
    
    getFocusCellValue(result, i, j) {
      if (!result || !result.focus_regions) {
        return '?';
      }
      
      // البحث عن بيانات توزيع التركيز للصورة الأولى
      const firstImageKey = Object.keys(result.focus_regions)[0];
      if (!firstImageKey || !result.focus_regions[firstImageKey]) {
        return '?';
      }
      
      const focusDistribution = result.focus_regions[firstImageKey].focus_distribution;
      if (!focusDistribution) {
        return '?';
      }
      
      const regionKey = `region_${i}_${j}`;
      const value = focusDistribution[regionKey] || 0;
      
      return (value * 100).toFixed(0) + '%';
    },
    
    getImageUrl(path) {
      // تحويل المسار المحلي إلى URL للعرض
      if (!path) return '';
      
      if (path.startsWith('http')) {
        return path;
      }
      
      // استخراج اسم الملف من المسار
      const fileName = path.split('/').pop();
      
      // إنشاء URL للملف
      return `/api/files/reports/${fileName}`;
    },
    
    async viewReport(report) {
      try {
        // جلب تفاصيل التقرير
        const reportDetails = await this.$store.dispatch('plantDisease/getAttentionReportDetails', report.path);
        
        if (report.model_name === 'مقارنة') {
          // عرض تقرير المقارنة
          this.comparisonResult = reportDetails;
          this.activeTab = this.analysisResults.length;
        } else {
          // عرض تقرير التحليل
          this.analysisResults = [reportDetails];
          this.activeTab = 0;
        }
      } catch (error) {
        this.error = `خطأ في عرض التقرير: ${error.message}`;
      }
    },
    
    async downloadReport(report) {
      try {
        // تحميل ملف التقرير
        const response = await this.$axios.get(`/api/plant-disease/reports/attention/${report.timestamp}`, {
          responseType: 'blob'
        });
        
        // إنشاء رابط تحميل
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `attention_report_${report.model_name}_${report.timestamp}.json`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        this.error = `خطأ في تحميل التقرير: ${error.message}`;
      }
    }
  }
};
</script>

<style scoped>
.focus-distribution-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 2px;
  width: 100%;
  aspect-ratio: 1;
  max-width: 300px;
  margin: 0 auto;
}

.focus-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-radius: 4px;
  padding: 8px;
}
</style>
