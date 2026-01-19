// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/AlertsManagement.vue
<template>
  <div class="alerts-management">
    <v-card class="management-card">
      <v-card-title class="text-center">إدارة التنبيهات</v-card-title>
      
      <v-card-text>
        <div class="filter-controls">
          <v-text-field
            v-model="searchQuery"
            outlined
            dense
            hide-details
            prepend-inner-icon="mdi-magnify"
            placeholder="بحث في التنبيهات..."
            class="search-field"
            clearable
          ></v-text-field>
          
          <v-select
            v-model="severityFilter"
            :items="severityOptions"
            outlined
            dense
            hide-details
            prepend-inner-icon="mdi-filter-variant"
            placeholder="تصفية حسب الشدة"
            class="filter-field"
            clearable
          ></v-select>
          
          <v-select
            v-model="componentFilter"
            :items="componentOptions"
            outlined
            dense
            hide-details
            prepend-inner-icon="mdi-filter-variant"
            placeholder="تصفية حسب المكون"
            class="filter-field"
            clearable
          ></v-select>
          
          <v-select
            v-model="statusFilter"
            :items="statusOptions"
            outlined
            dense
            hide-details
            prepend-inner-icon="mdi-filter-variant"
            placeholder="تصفية حسب الحالة"
            class="filter-field"
            clearable
          ></v-select>
        </div>
        
        <div class="date-range-filter">
          <v-menu
            v-model="startDateMenu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            max-width="290px"
            min-width="290px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="startDateFormatted"
                label="من تاريخ"
                readonly
                outlined
                dense
                hide-details
                v-bind="attrs"
                v-on="on"
                class="date-field"
                clearable
                @click:clear="startDate = null"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="startDate"
              no-title
              @input="startDateMenu = false"
              locale="ar"
            ></v-date-picker>
          </v-menu>
          
          <v-menu
            v-model="endDateMenu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            max-width="290px"
            min-width="290px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="endDateFormatted"
                label="إلى تاريخ"
                readonly
                outlined
                dense
                hide-details
                v-bind="attrs"
                v-on="on"
                class="date-field"
                clearable
                @click:clear="endDate = null"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="endDate"
              no-title
              @input="endDateMenu = false"
              locale="ar"
            ></v-date-picker>
          </v-menu>
          
          <v-btn
            color="primary"
            @click="applyFilters"
            class="filter-button"
          >
            <v-icon left>mdi-filter</v-icon>
            تطبيق
          </v-btn>
          
          <v-btn
            text
            @click="resetFilters"
            class="filter-button"
          >
            <v-icon left>mdi-filter-remove</v-icon>
            إعادة تعيين
          </v-btn>
        </div>
        
        <div class="alerts-actions">
          <v-btn
            color="error"
            @click="dismissAllAlerts"
            :disabled="selectedAlerts.length === 0"
            class="action-button"
          >
            <v-icon left>mdi-bell-off</v-icon>
            تجاهل المحدد
          </v-btn>
          
          <v-btn
            color="primary"
            @click="exportAlerts"
            :disabled="filteredAlerts.length === 0"
            class="action-button"
          >
            <v-icon left>mdi-file-export</v-icon>
            تصدير
          </v-btn>
          
          <v-btn
            color="primary"
            @click="refreshAlerts"
            :loading="isLoading"
            class="action-button"
          >
            <v-icon left>mdi-refresh</v-icon>
            تحديث
          </v-btn>
        </div>
        
        <div v-if="isLoading" class="loading-container">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
          ></v-progress-circular>
          <div class="loading-text">جاري تحميل التنبيهات...</div>
        </div>
        
        <div v-else-if="filteredAlerts.length === 0" class="empty-state">
          <v-icon size="64" color="grey lighten-1">mdi-bell-off</v-icon>
          <div class="empty-text">
            {{ hasFilters ? 'لا توجد تنبيهات تطابق معايير البحث' : 'لا توجد تنبيهات متاحة حالياً' }}
          </div>
        </div>
        
        <v-data-table
          v-else
          :headers="tableHeaders"
          :items="filteredAlerts"
          :items-per-page="10"
          :footer-props="{
            'items-per-page-options': [5, 10, 25, 50],
            'items-per-page-text': 'عناصر في الصفحة'
          }"
          class="alerts-table"
          :loading="isLoading"
          v-model="selectedAlerts"
          show-select
        >
          <!-- تخصيص عرض الشدة -->
          <template v-slot:item.severity="{ item }">
            <v-chip
              small
              :color="getSeverityColor(item.severity)"
              text-color="white"
            >
              {{ getSeverityText(item.severity) }}
            </v-chip>
          </template>
          
          <!-- تخصيص عرض الوقت -->
          <template v-slot:item.timestamp="{ item }">
            {{ formatAlertTime(item.timestamp) }}
          </template>
          
          <!-- تخصيص عرض الحالة -->
          <template v-slot:item.status="{ item }">
            <v-chip
              small
              :color="getStatusColor(item.status)"
              outlined
            >
              {{ getStatusText(item.status) }}
            </v-chip>
          </template>
          
          <!-- تخصيص عرض الإجراءات -->
          <template v-slot:item.actions="{ item }">
            <v-btn
              icon
              small
              @click="viewAlertDetails(item)"
              color="primary"
              class="mx-1"
            >
              <v-icon small>mdi-information</v-icon>
            </v-btn>
            
            <v-btn
              icon
              small
              @click="toggleAlertStatus(item)"
              :color="item.status === 'dismissed' ? 'success' : 'grey'"
              class="mx-1"
            >
              <v-icon small>{{ item.status === 'dismissed' ? 'mdi-bell' : 'mdi-bell-off' }}</v-icon>
            </v-btn>
            
            <v-btn
              icon
              small
              @click="deleteAlert(item)"
              color="error"
              class="mx-1"
            >
              <v-icon small>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
    
    <!-- نافذة تفاصيل التنبيه -->
    <v-dialog
      v-model="detailsDialog"
      max-width="600px"
    >
      <v-card v-if="selectedAlert">
        <v-card-title class="text-center">
          تفاصيل التنبيه
          <v-spacer></v-spacer>
          <v-btn
            icon
            @click="detailsDialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text>
          <div class="alert-details">
            <div class="detail-item">
              <div class="detail-label">العنوان:</div>
              <div class="detail-value">{{ selectedAlert.title }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">الشدة:</div>
              <div class="detail-value">
                <v-chip
                  small
                  :color="getSeverityColor(selectedAlert.severity)"
                  text-color="white"
                >
                  {{ getSeverityText(selectedAlert.severity) }}
                </v-chip>
              </div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">الوقت:</div>
              <div class="detail-value">{{ formatAlertTime(selectedAlert.timestamp, true) }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">المكون:</div>
              <div class="detail-value">{{ selectedAlert.component }}</div>
            </div>
            
            <div class="detail-item">
              <div class="detail-label">الحالة:</div>
              <div class="detail-value">
                <v-chip
                  small
                  :color="getStatusColor(selectedAlert.status)"
                  outlined
                >
                  {{ getStatusText(selectedAlert.status) }}
                </v-chip>
              </div>
            </div>
            
            <div class="detail-item full-width">
              <div class="detail-label">الرسالة:</div>
              <div class="detail-value message-value">{{ selectedAlert.message }}</div>
            </div>
            
            <div class="detail-item full-width" v-if="selectedAlert.details">
              <div class="detail-label">تفاصيل إضافية:</div>
              <div class="detail-value message-value">{{ selectedAlert.details }}</div>
            </div>
          </div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="toggleAlertStatus(selectedAlert)"
          >
            <v-icon left>{{ selectedAlert.status === 'dismissed' ? 'mdi-bell' : 'mdi-bell-off' }}</v-icon>
            {{ selectedAlert.status === 'dismissed' ? 'تفعيل' : 'تجاهل' }}
          </v-btn>
          <v-btn
            color="error"
            text
            @click="deleteAlert(selectedAlert); detailsDialog = false"
          >
            <v-icon left>mdi-delete</v-icon>
            حذف
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
/**
 * مكون إدارة التنبيهات
 * 
 * يوفر هذا المكون واجهة لإدارة تنبيهات النظام
 * مع إمكانية البحث والتصفية وعرض التفاصيل
 */
export default {
  name: 'AlertsManagement',
  
  data() {
    return {
      isLoading: false,
      searchQuery: '',
      severityFilter: null,
      componentFilter: null,
      statusFilter: null,
      startDate: null,
      endDate: null,
      startDateMenu: false,
      endDateMenu: false,
      selectedAlerts: [],
      detailsDialog: false,
      selectedAlert: null,
      
      // خيارات التصفية
      severityOptions: [
        { text: 'معلومات', value: 'info' },
        { text: 'تحذير', value: 'warning' },
        { text: 'خطأ', value: 'error' },
        { text: 'حرج', value: 'critical' }
      ],
      
      componentOptions: [
        { text: 'النظام', value: 'system' },
        { text: 'قاعدة البيانات', value: 'database' },
        { text: 'خدمات الذكاء الاصطناعي', value: 'ai_services' },
        { text: 'بوابة API', value: 'api_gateway' },
        { text: 'تخزين الملفات', value: 'file_storage' }
      ],
      
      statusOptions: [
        { text: 'جديد', value: 'new' },
        { text: 'قيد المعالجة', value: 'processing' },
        { text: 'تم تجاهله', value: 'dismissed' },
        { text: 'تم حله', value: 'resolved' }
      ],
      
      // رؤوس الجدول
      tableHeaders: [
        { text: 'العنوان', value: 'title', align: 'center' },
        { text: 'الشدة', value: 'severity', align: 'center' },
        { text: 'الوقت', value: 'timestamp', align: 'center' },
        { text: 'المكون', value: 'component', align: 'center' },
        { text: 'الحالة', value: 'status', align: 'center' },
        { text: 'الإجراءات', value: 'actions', align: 'center', sortable: false }
      ],
      
      // بيانات التنبيهات
      alerts: [
        {
          id: 'alert-001',
          title: 'فشل الاتصال بخدمة تخزين الملفات',
          severity: 'error',
          timestamp: new Date(Date.now() - 5 * 60 * 1000), // قبل 5 دقائق
          component: 'file_storage',
          status: 'new',
          message: 'تعذر الاتصال بخدمة تخزين الملفات. يرجى التحقق من إعدادات الاتصال.',
          details: 'خطأ اتصال: Connection refused (111)'
        },
        {
          id: 'alert-002',
          title: 'ارتفاع استخدام قاعدة البيانات',
          severity: 'warning',
          timestamp: new Date(Date.now() - 15 * 60 * 1000), // قبل 15 دقيقة
          component: 'database',
          status: 'processing',
          message: 'ارتفع استخدام موارد قاعدة البيانات عن الحد الطبيعي. يرجى مراقبة الأداء.',
          details: 'استخدام المعالج: 85%, استخدام الذاكرة: 92%'
        },
        {
          id: 'alert-003',
          title: 'تم تحديث النظام',
          severity: 'info',
          timestamp: new Date(Date.now() - 45 * 60 * 1000), // قبل 45 دقيقة
          component: 'system',
          status: 'dismissed',
          message: 'تم تحديث النظام إلى الإصدار 3.2.1 بنجاح.',
          details: 'تم تثبيت 15 تحديث و5 إصلاحات أمنية'
        },
        {
          id: 'alert-004',
          title: 'فشل مهمة النسخ الاحتياطي',
          severity: 'critical',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // قبل ساعتين
          component: 'system',
          status: 'new',
          message: 'فشلت مهمة النسخ الاحتياطي المجدولة. يرجى التحقق من إعدادات النسخ الاحتياطي.',
          details: 'خطأ: لا توجد مساحة كافية على القرص'
        },
        {
          id: 'alert-005',
          title: 'تم تجاوز حد استخدام API',
          severity: 'warning',
          timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000), // قبل 3 ساعات
          component: 'api_gateway',
          status: 'resolved',
          message: 'تم تجاوز حد استخدام API لمستخدم "admin". تم تطبيق الحد الافتراضي.',
          details: 'الحد: 1000 طلب/دقيقة, الاستخدام الفعلي: 1250 طلب/دقيقة'
        },
        {
          id: 'alert-006',
          title: 'تم إعادة تشغيل خدمة الذكاء الاصطناعي',
          severity: 'info',
          timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000), // قبل 5 ساعات
          component: 'ai_services',
          status: 'dismissed',
          message: 'تم إعادة تشغيل خدمة الذكاء الاصطناعي تلقائياً بعد تحديث النماذج.',
          details: 'تم تحميل 3 نماذج جديدة'
        }
      ]
    };
  },
  
  computed: {
    /**
     * التنبيهات المصفاة حسب معايير البحث والتصفية
     */
    filteredAlerts() {
      let result = [...this.alerts];
      
      // تصفية حسب البحث
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(alert => 
          alert.title.toLowerCase().includes(query) || 
          alert.message.toLowerCase().includes(query)
        );
      }
      
      // تصفية حسب الشدة
      if (this.severityFilter) {
        result = result.filter(alert => alert.severity === this.severityFilter);
      }
      
      // تصفية حسب المكون
      if (this.componentFilter) {
        result = result.filter(alert => alert.component === this.componentFilter);
      }
      
      // تصفية حسب الحالة
      if (this.statusFilter) {
        result = result.filter(alert => alert.status === this.statusFilter);
      }
      
      // تصفية حسب تاريخ البداية
      if (this.startDate) {
        const startDateTime = new Date(this.startDate).setHours(0, 0, 0, 0);
        result = result.filter(alert => new Date(alert.timestamp) >= startDateTime);
      }
      
      // تصفية حسب تاريخ النهاية
      if (this.endDate) {
        const endDateTime = new Date(this.endDate).setHours(23, 59, 59, 999);
        result = result.filter(alert => new Date(alert.timestamp) <= endDateTime);
      }
      
      return result;
    },
    
    /**
     * تاريخ البداية المنسق
     */
    startDateFormatted() {
      return this.formatDate(this.startDate);
    },
    
    /**
     * تاريخ النهاية المنسق
     */
    endDateFormatted() {
      return this.formatDate(this.endDate);
    },
    
    /**
     * التحقق من وجود تصفية نشطة
     */
    hasFilters() {
      return this.searchQuery || 
             this.severityFilter || 
             this.componentFilter || 
             this.statusFilter || 
             this.startDate || 
             this.endDate;
    }
  },
  
  methods: {
    /**
     * الحصول على لون الشدة
     * @param {String} severity - شدة التنبيه (info, warning, error, critical)
     * @returns {String} - لون الشدة
     */
    getSeverityColor(severity) {
      switch (severity) {
        case 'info':
          return 'info';
        case 'warning':
          return 'warning';
        case 'error':
          return 'error';
        case 'critical':
          return 'deep-orange';
        default:
          return 'grey';
      }
    },
    
    /**
     * الحصول على نص الشدة
     * @param {String} severity - شدة التنبيه (info, warning, error, critical)
     * @returns {String} - نص الشدة
     */
    getSeverityText(severity) {
      switch (severity) {
        case 'info':
          return 'معلومات';
        case 'warning':
          return 'تحذير';
        case 'error':
          return 'خطأ';
        case 'critical':
          return 'حرج';
        default:
          return 'غير معروف';
      }
    },
    
    /**
     * الحصول على لون الحالة
     * @param {String} status - حالة التنبيه (new, processing, dismissed, resolved)
     * @returns {String} - لون الحالة
     */
    getStatusColor(status) {
      switch (status) {
        case 'new':
          return 'error';
        case 'processing':
          return 'info';
        case 'dismissed':
          return 'grey';
        case 'resolved':
          return 'success';
        default:
          return 'grey';
      }
    },
    
    /**
     * الحصول على نص الحالة
     * @param {String} status - حالة التنبيه (new, processing, dismissed, resolved)
     * @returns {String} - نص الحالة
     */
    getStatusText(status) {
      switch (status) {
        case 'new':
          return 'جديد';
        case 'processing':
          return 'قيد المعالجة';
        case 'dismissed':
          return 'تم تجاهله';
        case 'resolved':
          return 'تم حله';
        default:
          return 'غير معروف';
      }
    },
    
    /**
     * تنسيق التاريخ
     * @param {String} date - التاريخ
     * @returns {String} - التاريخ المنسق
     */
    formatDate(date) {
      if (!date) return '';
      
      const d = new Date(date);
      const day = d.getDate().toString().padStart(2, '0');
      const month = (d.getMonth() + 1).toString().padStart(2, '0');
      const year = d.getFullYear();
      
      return `${day}/${month}/${year}`;
    },
    
    /**
     * تنسيق وقت التنبيه
     * @param {Date} timestamp - الطابع الزمني
     * @param {Boolean} detailed - عرض تفاصيل أكثر
     * @returns {String} - الوقت المنسق
     */
    formatAlertTime(timestamp, detailed = false) {
      if (!timestamp) return '';
      
      if (detailed) {
        const d = new Date(timestamp);
        const day = d.getDate().toString().padStart(2, '0');
        const month = (d.getMonth() + 1).toString().padStart(2, '0');
        const year = d.getFullYear();
        const hours = d.getHours().toString().padStart(2, '0');
        const minutes = d.getMinutes().toString().padStart(2, '0');
        
        return `${day}/${month}/${year} ${hours}:${minutes}`;
      }
      
      const now = new Date();
      const diff = Math.floor((now - new Date(timestamp)) / 1000 / 60); // الفرق بالدقائق
      
      if (diff < 1) {
        return 'الآن';
      } else if (diff < 60) {
        return `منذ ${diff} دقيقة`;
      } else if (diff < 24 * 60) {
        const hours = Math.floor(diff / 60);
        return `منذ ${hours} ساعة`;
      } else {
        const days = Math.floor(diff / (24 * 60));
        return `منذ ${days} يوم`;
      }
    },
    
    /**
     * تطبيق التصفية
     */
    applyFilters() {
      // يمكن هنا تنفيذ منطق إضافي لتطبيق التصفية
      console.log('تم تطبيق التصفية');
    },
    
    /**
     * إعادة تعيين التصفية
     */
    resetFilters() {
      this.searchQuery = '';
      this.severityFilter = null;
      this.componentFilter = null;
      this.statusFilter = null;
      this.startDate = null;
      this.endDate = null;
      this.selectedAlerts = [];
    },
    
    /**
     * تجاهل جميع التنبيهات المحددة
     */
    dismissAllAlerts() {
      if (this.selectedAlerts.length === 0) return;
      
      // تحديث حالة التنبيهات المحددة
      this.selectedAlerts.forEach(alert => {
        const alertIndex = this.alerts.findIndex(a => a.id === alert.id);
        if (alertIndex !== -1) {
          this.alerts[alertIndex].status = 'dismissed';
        }
      });
      
      // إعادة تعيين التحديد
      this.selectedAlerts = [];
    },
    
    /**
     * تصدير التنبيهات
     */
    exportAlerts() {
      console.log('تصدير التنبيهات');
      // يمكن هنا تنفيذ منطق تصدير التنبيهات
    },
    
    /**
     * تحديث التنبيهات
     */
    refreshAlerts() {
      this.isLoading = true;
      
      // محاكاة تحديث البيانات
      setTimeout(() => {
        // يمكن هنا تنفيذ منطق تحديث البيانات
        this.isLoading = false;
      }, 1500);
    },
    
    /**
     * عرض تفاصيل التنبيه
     * @param {Object} alert - التنبيه
     */
    viewAlertDetails(alert) {
      this.selectedAlert = alert;
      this.detailsDialog = true;
    },
    
    /**
     * تبديل حالة التنبيه
     * @param {Object} alert - التنبيه
     */
    toggleAlertStatus(alert) {
      const alertIndex = this.alerts.findIndex(a => a.id === alert.id);
      if (alertIndex !== -1) {
        // تبديل الحالة بين "تم تجاهله" و "جديد"
        this.alerts[alertIndex].status = this.alerts[alertIndex].status === 'dismissed' ? 'new' : 'dismissed';
      }
    },
    
    /**
     * حذف التنبيه
     * @param {Object} alert - التنبيه
     */
    deleteAlert(alert) {
      const alertIndex = this.alerts.findIndex(a => a.id === alert.id);
      if (alertIndex !== -1) {
        this.alerts.splice(alertIndex, 1);
      }
      
      // إغلاق نافذة التفاصيل إذا كانت مفتوحة
      if (this.detailsDialog && this.selectedAlert && this.selectedAlert.id === alert.id) {
        this.detailsDialog = false;
        this.selectedAlert = null;
      }
    }
  }
};
</script>

<style scoped>
.alerts-management {
  width: 100%;
}

.management-card {
  border-radius: 8px;
  overflow: hidden;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.search-field {
  flex-grow: 2;
  min-width: 250px;
}

.filter-field {
  flex-grow: 1;
  min-width: 200px;
}

.date-range-filter {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.date-field {
  flex-grow: 1;
  min-width: 150px;
}

.filter-button {
  margin-top: 0.5rem;
}

.alerts-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.action-button {
  flex-grow: 1;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.loading-text {
  margin-top: 1rem;
  color: var(--v-primary-base);
  font-weight: bold;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.empty-text {
  margin-top: 1rem;
  color: var(--v-secondary-base);
  font-size: 1.1rem;
}

.alerts-table {
  border-radius: 8px;
  overflow: hidden;
}

.alert-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.detail-item {
  flex: 1 1 45%;
  min-width: 200px;
  margin-bottom: 0.5rem;
}

.full-width {
  flex: 1 1 100%;
}

.detail-label {
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: var(--v-secondary-darken1);
}

.detail-value {
  word-break: break-word;
}

.message-value {
  background-color: rgba(0, 0, 0, 0.03);
  padding: 0.75rem;
  border-radius: 4px;
  white-space: pre-line;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 600px) {
  .filter-controls,
  .date-range-filter,
  .alerts-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .search-field,
  .filter-field,
  .date-field {
    width: 100%;
  }
  
  .detail-item {
    flex: 1 1 100%;
  }
}
</style>
