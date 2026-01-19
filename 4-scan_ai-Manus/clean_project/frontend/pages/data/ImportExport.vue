<!-- File: /home/ubuntu/clean_project/frontend/pages/data/ImportExport.vue -->
<template>
  <div class="import-export-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="fas fa-exchange-alt"></i>
          استيراد وتصدير البيانات
        </h1>
        <p class="page-description">
          إدارة استيراد وتصدير البيانات بصيغ مختلفة
        </p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="showTemplatesModal = true">
          <i class="fas fa-file-download"></i>
          تحميل القوالب
        </button>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <div class="action-card export">
        <div class="action-icon">
          <i class="fas fa-upload"></i>
        </div>
        <div class="action-content">
          <h3>تصدير سريع</h3>
          <p>تصدير جميع البيانات بنقرة واحدة</p>
          <button class="btn btn-success" @click="quickExport">
            <i class="fas fa-download"></i>
            تصدير الآن
          </button>
        </div>
      </div>

      <div class="action-card import">
        <div class="action-icon">
          <i class="fas fa-download"></i>
        </div>
        <div class="action-content">
          <h3>استيراد سريع</h3>
          <p>استيراد البيانات من ملف</p>
          <button class="btn btn-primary" @click="triggerFileInput">
            <i class="fas fa-upload"></i>
            اختيار ملف
          </button>
          <input 
            ref="quickImportFile" 
            type="file" 
            @change="quickImport" 
            accept=".csv,.xlsx,.json"
            style="display: none"
          >
        </div>
      </div>

      <div class="action-card backup">
        <div class="action-icon">
          <i class="fas fa-database"></i>
        </div>
        <div class="action-content">
          <h3>نسخة احتياطية</h3>
          <p>إنشاء نسخة احتياطية كاملة</p>
          <button class="btn btn-warning" @click="createBackup">
            <i class="fas fa-archive"></i>
            إنشاء نسخة
          </button>
        </div>
      </div>
    </div>

    <!-- Export Section -->
    <div class="export-section">
      <div class="section-header">
        <h2>تصدير البيانات</h2>
        <p>اختر نوع البيانات والصيغة المطلوبة للتصدير</p>
      </div>

      <div class="export-form">
        <div class="form-grid">
          <div class="form-group">
            <label>نوع البيانات</label>
            <div class="data-types">
              <div 
                v-for="type in dataTypes" 
                :key="type.id"
                class="data-type-card"
                :class="{ selected: exportForm.selectedTypes.includes(type.id) }"
                @click="toggleDataType(type.id)"
              >
                <div class="type-icon">
                  <i :class="type.icon"></i>
                </div>
                <div class="type-info">
                  <h4>{{ type.name }}</h4>
                  <p>{{ type.description }}</p>
                  <small>{{ type.count }} عنصر</small>
                </div>
                <div class="type-checkbox">
                  <i class="fas fa-check" v-if="exportForm.selectedTypes.includes(type.id)"></i>
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>صيغة التصدير</label>
            <div class="format-options">
              <div 
                v-for="format in exportFormats" 
                :key="format.id"
                class="format-option"
                :class="{ selected: exportForm.format === format.id }"
                @click="exportForm.format = format.id"
              >
                <div class="format-icon">
                  <i :class="format.icon"></i>
                </div>
                <div class="format-info">
                  <h4>{{ format.name }}</h4>
                  <p>{{ format.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>خيارات التصدير</label>
            <div class="export-options">
              <div class="option-item">
                <input 
                  type="checkbox" 
                  id="includeHeaders" 
                  v-model="exportForm.includeHeaders"
                >
                <label for="includeHeaders">تضمين رؤوس الأعمدة</label>
              </div>
              <div class="option-item">
                <input 
                  type="checkbox" 
                  id="compressFile" 
                  v-model="exportForm.compressFile"
                >
                <label for="compressFile">ضغط الملف</label>
              </div>
              <div class="option-item">
                <input 
                  type="checkbox" 
                  id="encryptFile" 
                  v-model="exportForm.encryptFile"
                >
                <label for="encryptFile">تشفير الملف</label>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>فترة البيانات</label>
            <div class="date-range">
              <div class="date-input-group">
                <label>من تاريخ</label>
                <input 
                  type="date" 
                  v-model="exportForm.dateFrom"
                  class="form-control"
                >
              </div>
              <div class="date-input-group">
                <label>إلى تاريخ</label>
                <input 
                  type="date" 
                  v-model="exportForm.dateTo"
                  class="form-control"
                >
              </div>
            </div>
          </div>
        </div>

        <div class="export-actions">
          <button 
            class="btn btn-primary btn-lg" 
            @click="exportData"
            :disabled="!canExport || exporting"
          >
            <i class="fas fa-download" :class="{ 'fa-spin': exporting }"></i>
            {{ exporting ? 'جاري التصدير...' : 'تصدير البيانات' }}
          </button>
          <button class="btn btn-outline-secondary" @click="resetExportForm">
            <i class="fas fa-undo"></i>
            إعادة تعيين
          </button>
        </div>
      </div>
    </div>

    <!-- Import Section -->
    <div class="import-section">
      <div class="section-header">
        <h2>استيراد البيانات</h2>
        <p>رفع وتحليل ملفات البيانات للاستيراد</p>
      </div>

      <div class="import-form">
        <!-- File Upload Area -->
        <div 
          class="upload-area"
          :class="{ 'drag-over': dragOver, 'has-file': importForm.file }"
          @drop="handleDrop"
          @dragover.prevent="dragOver = true"
          @dragleave="dragOver = false"
          @click="triggerImportFileInput"
        >
          <div v-if="!importForm.file" class="upload-placeholder">
            <div class="upload-icon">
              <i class="fas fa-cloud-upload-alt"></i>
            </div>
            <h3>اسحب الملف هنا أو انقر للاختيار</h3>
            <p>الصيغ المدعومة: CSV, Excel, JSON</p>
            <small>الحد الأقصى: 50 ميجابايت</small>
          </div>

          <div v-else class="file-info">
            <div class="file-icon">
              <i :class="getFileIcon(importForm.file.name)"></i>
            </div>
            <div class="file-details">
              <h4>{{ importForm.file.name }}</h4>
              <p>{{ formatFileSize(importForm.file.size) }}</p>
              <small>{{ formatDate(new Date()) }}</small>
            </div>
            <button class="remove-file" @click.stop="removeFile">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <input 
            ref="importFileInput" 
            type="file" 
            @change="handleFileSelect" 
            accept=".csv,.xlsx,.xls,.json"
            style="display: none"
          >
        </div>

        <!-- File Analysis -->
        <div v-if="fileAnalysis" class="file-analysis">
          <h3>تحليل الملف</h3>
          <div class="analysis-grid">
            <div class="analysis-item">
              <label>نوع الملف:</label>
              <span>{{ fileAnalysis.type }}</span>
            </div>
            <div class="analysis-item">
              <label>عدد الصفوف:</label>
              <span>{{ fileAnalysis.rows }}</span>
            </div>
            <div class="analysis-item">
              <label>عدد الأعمدة:</label>
              <span>{{ fileAnalysis.columns }}</span>
            </div>
            <div class="analysis-item">
              <label>الترميز:</label>
              <span>{{ fileAnalysis.encoding }}</span>
            </div>
          </div>

          <!-- Column Mapping -->
          <div class="column-mapping">
            <h4>ربط الأعمدة</h4>
            <div class="mapping-grid">
              <div 
                v-for="(column, index) in fileAnalysis.sampleColumns" 
                :key="index"
                class="mapping-item"
              >
                <div class="source-column">
                  <label>العمود {{ index + 1 }}:</label>
                  <span>{{ column }}</span>
                </div>
                <div class="mapping-arrow">
                  <i class="fas fa-arrow-left"></i>
                </div>
                <div class="target-column">
                  <select v-model="columnMapping[index]" class="form-control">
                    <option value="">تجاهل</option>
                    <option v-for="field in targetFields" :key="field.id" :value="field.id">
                      {{ field.name }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <!-- Data Preview -->
          <div class="data-preview">
            <h4>معاينة البيانات</h4>
            <div class="preview-table">
              <table>
                <thead>
                  <tr>
                    <th v-for="(column, index) in fileAnalysis.sampleColumns" :key="index">
                      {{ column }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, rowIndex) in fileAnalysis.sampleData" :key="rowIndex">
                    <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                      {{ cell }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Import Options -->
        <div v-if="importForm.file" class="import-options">
          <h3>خيارات الاستيراد</h3>
          <div class="options-grid">
            <div class="option-item">
              <input 
                type="checkbox" 
                id="skipFirstRow" 
                v-model="importForm.skipFirstRow"
              >
              <label for="skipFirstRow">تجاهل الصف الأول (رؤوس الأعمدة)</label>
            </div>
            <div class="option-item">
              <input 
                type="checkbox" 
                id="validateData" 
                v-model="importForm.validateData"
              >
              <label for="validateData">التحقق من صحة البيانات</label>
            </div>
            <div class="option-item">
              <input 
                type="checkbox" 
                id="updateExisting" 
                v-model="importForm.updateExisting"
              >
              <label for="updateExisting">تحديث البيانات الموجودة</label>
            </div>
            <div class="option-item">
              <input 
                type="checkbox" 
                id="createBackupBeforeImport" 
                v-model="importForm.createBackupBeforeImport"
              >
              <label for="createBackupBeforeImport">إنشاء نسخة احتياطية قبل الاستيراد</label>
            </div>
          </div>
        </div>

        <!-- Import Actions -->
        <div v-if="importForm.file" class="import-actions">
          <button 
            class="btn btn-primary btn-lg" 
            @click="importData"
            :disabled="importing"
          >
            <i class="fas fa-upload" :class="{ 'fa-spin': importing }"></i>
            {{ importing ? 'جاري الاستيراد...' : 'استيراد البيانات' }}
          </button>
          <button class="btn btn-outline-secondary" @click="resetImportForm">
            <i class="fas fa-undo"></i>
            إعادة تعيين
          </button>
        </div>
      </div>
    </div>

    <!-- Import/Export History -->
    <div class="history-section">
      <div class="section-header">
        <h2>سجل العمليات</h2>
        <div class="history-controls">
          <button class="btn btn-sm btn-outline-danger" @click="clearHistory">
            <i class="fas fa-trash"></i>
            مسح السجل
          </button>
        </div>
      </div>

      <div class="history-list">
        <div 
          v-for="operation in operationHistory" 
          :key="operation.id"
          class="history-item"
          :class="operation.status"
        >
          <div class="operation-icon">
            <i :class="operation.type === 'export' ? 'fas fa-upload' : 'fas fa-download'"></i>
          </div>
          <div class="operation-info">
            <h4>{{ operation.type === 'export' ? 'تصدير' : 'استيراد' }} {{ operation.dataType }}</h4>
            <p>{{ operation.description }}</p>
            <small>{{ formatTime(operation.timestamp) }}</small>
          </div>
          <div class="operation-status">
            <span :class="['status-badge', operation.status]">
              {{ getStatusText(operation.status) }}
            </span>
          </div>
          <div class="operation-actions">
            <button 
              v-if="operation.downloadUrl" 
              class="btn-icon btn-primary"
              @click="downloadFile(operation.downloadUrl)"
              title="تحميل"
            >
              <i class="fas fa-download"></i>
            </button>
            <button 
              class="btn-icon btn-danger"
              @click="deleteOperation(operation.id)"
              title="حذف"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Templates Modal -->
    <div v-if="showTemplatesModal" class="modal-overlay" @click="showTemplatesModal = false">
      <div class="modal-content large-modal" @click.stop>
        <div class="modal-header">
          <h3>قوالب الاستيراد</h3>
          <button class="modal-close" @click="showTemplatesModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>تحميل القوالب الجاهزة لاستيراد البيانات بالصيغة الصحيحة</p>
          <div class="templates-grid">
            <div 
              v-for="template in templates" 
              :key="template.id"
              class="template-card"
            >
              <div class="template-icon">
                <i :class="template.icon"></i>
              </div>
              <div class="template-info">
                <h4>{{ template.name }}</h4>
                <p>{{ template.description }}</p>
              </div>
              <button 
                class="btn btn-primary"
                @click="downloadTemplate(template.id)"
              >
                <i class="fas fa-download"></i>
                تحميل
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress Modal -->
    <div v-if="showProgressModal" class="modal-overlay">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ progressTitle }}</h3>
        </div>
        <div class="modal-body">
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <div class="progress-text">{{ progress }}%</div>
          </div>
          <p>{{ progressMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImportExport',
  data() {
    return {
      dragOver: false,
      exporting: false,
      importing: false,
      showTemplatesModal: false,
      showProgressModal: false,
      progress: 0,
      progressTitle: '',
      progressMessage: '',
      
      exportForm: {
        selectedTypes: [],
        format: 'csv',
        includeHeaders: true,
        compressFile: false,
        encryptFile: false,
        dateFrom: '',
        dateTo: ''
      },
      
      importForm: {
        file: null,
        skipFirstRow: true,
        validateData: true,
        updateExisting: false,
        createBackupBeforeImport: true
      },
      
      fileAnalysis: null,
      columnMapping: {},
      
      dataTypes: [
        {
          id: 'users',
          name: 'المستخدمين',
          description: 'بيانات المستخدمين والحسابات',
          icon: 'fas fa-users',
          count: 156
        },
        {
          id: 'diagnoses',
          name: 'التشخيصات',
          description: 'نتائج التشخيص والتحليلات',
          icon: 'fas fa-stethoscope',
          count: 2847
        },
        {
          id: 'ai_models',
          name: 'نماذج الذكاء الاصطناعي',
          description: 'معلومات النماذج والتدريب',
          icon: 'fas fa-brain',
          count: 12
        },
        {
          id: 'activity_logs',
          name: 'سجل الأنشطة',
          description: 'سجلات النظام والمستخدمين',
          icon: 'fas fa-history',
          count: 15623
        },
        {
          id: 'settings',
          name: 'الإعدادات',
          description: 'إعدادات النظام والتكوين',
          icon: 'fas fa-cog',
          count: 45
        }
      ],
      
      exportFormats: [
        {
          id: 'csv',
          name: 'CSV',
          description: 'ملف قيم مفصولة بفواصل',
          icon: 'fas fa-file-csv'
        },
        {
          id: 'excel',
          name: 'Excel',
          description: 'ملف Microsoft Excel',
          icon: 'fas fa-file-excel'
        },
        {
          id: 'json',
          name: 'JSON',
          description: 'ملف JavaScript Object Notation',
          icon: 'fas fa-file-code'
        },
        {
          id: 'xml',
          name: 'XML',
          description: 'ملف Extensible Markup Language',
          icon: 'fas fa-file-code'
        }
      ],
      
      targetFields: [
        { id: 'name', name: 'الاسم' },
        { id: 'email', name: 'البريد الإلكتروني' },
        { id: 'phone', name: 'رقم الهاتف' },
        { id: 'role', name: 'الدور' },
        { id: 'status', name: 'الحالة' },
        { id: 'created_at', name: 'تاريخ الإنشاء' },
        { id: 'disease_name', name: 'اسم المرض' },
        { id: 'confidence', name: 'مستوى الثقة' },
        { id: 'description', name: 'الوصف' }
      ],
      
      templates: [
        {
          id: 'users_template',
          name: 'قالب المستخدمين',
          description: 'قالب لاستيراد بيانات المستخدمين',
          icon: 'fas fa-users'
        },
        {
          id: 'diagnoses_template',
          name: 'قالب التشخيصات',
          description: 'قالب لاستيراد نتائج التشخيص',
          icon: 'fas fa-stethoscope'
        },
        {
          id: 'diseases_template',
          name: 'قالب الأمراض',
          description: 'قالب لاستيراد معلومات الأمراض',
          icon: 'fas fa-virus'
        }
      ],
      
      operationHistory: [
        {
          id: 1,
          type: 'export',
          dataType: 'المستخدمين',
          description: 'تصدير 156 مستخدم بصيغة Excel',
          status: 'success',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
          downloadUrl: '/downloads/users_export.xlsx'
        },
        {
          id: 2,
          type: 'import',
          dataType: 'التشخيصات',
          description: 'استيراد 45 تشخيص من ملف CSV',
          status: 'success',
          timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000),
          downloadUrl: null
        },
        {
          id: 3,
          type: 'export',
          dataType: 'سجل الأنشطة',
          description: 'تصدير سجل الأنشطة لآخر 30 يوم',
          status: 'failed',
          timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000),
          downloadUrl: null
        }
      ]
    }
  },
  
  computed: {
    canExport() {
      return this.exportForm.selectedTypes.length > 0 && this.exportForm.format
    }
  },
  
  mounted() {
    this.setDefaultDateRange()
  },
  
  methods: {
    setDefaultDateRange() {
      const today = new Date()
      const monthAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)
      
      this.exportForm.dateTo = today.toISOString().split('T')[0]
      this.exportForm.dateFrom = monthAgo.toISOString().split('T')[0]
    },
    
    toggleDataType(typeId) {
      const index = this.exportForm.selectedTypes.indexOf(typeId)
      if (index > -1) {
        this.exportForm.selectedTypes.splice(index, 1)
      } else {
        this.exportForm.selectedTypes.push(typeId)
      }
    },
    
    resetExportForm() {
      this.exportForm = {
        selectedTypes: [],
        format: 'csv',
        includeHeaders: true,
        compressFile: false,
        encryptFile: false,
        dateFrom: '',
        dateTo: ''
      }
      this.setDefaultDateRange()
    },
    
    async exportData() {
      this.exporting = true
      this.showProgressModal = true
      this.progressTitle = 'تصدير البيانات'
      this.progress = 0
      
      try {
        // محاكاة عملية التصدير
        for (let i = 0; i <= 100; i += 10) {
          this.progress = i
          this.progressMessage = `جاري تصدير البيانات... ${i}%`
          await new Promise(resolve => setTimeout(resolve, 200))
        }
        
        // إنشاء ملف وهمي للتحميل
        const filename = `export_${Date.now()}.${this.exportForm.format}`
        const blob = new Blob(['بيانات تجريبية'], { type: 'text/plain' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        window.URL.revokeObjectURL(url)
        
        // إضافة إلى السجل
        this.operationHistory.unshift({
          id: Date.now(),
          type: 'export',
          dataType: this.exportForm.selectedTypes.join(', '),
          description: `تصدير ${this.exportForm.selectedTypes.length} نوع بيانات بصيغة ${this.exportForm.format.toUpperCase()}`,
          status: 'success',
          timestamp: new Date(),
          downloadUrl: url
        })
        
        this.$toast.success('تم تصدير البيانات بنجاح')
      } catch (error) {
        console.error('خطأ في تصدير البيانات:', error)
        this.$toast.error('فشل في تصدير البيانات')
      } finally {
        this.exporting = false
        this.showProgressModal = false
      }
    },
    
    triggerFileInput() {
      this.$refs.quickImportFile.click()
    },
    
    triggerImportFileInput() {
      this.$refs.importFileInput.click()
    },
    
    async quickImport(event) {
      const file = event.target.files[0]
      if (file) {
        this.importForm.file = file
        await this.analyzeFile(file)
      }
    },
    
    async quickExport() {
      // تحديد جميع أنواع البيانات للتصدير السريع
      this.exportForm.selectedTypes = this.dataTypes.map(type => type.id)
      await this.exportData()
    },
    
    async createBackup() {
      try {
        this.showProgressModal = true
        this.progressTitle = 'إنشاء نسخة احتياطية'
        this.progress = 0
        
        for (let i = 0; i <= 100; i += 5) {
          this.progress = i
          this.progressMessage = `جاري إنشاء النسخة الاحتياطية... ${i}%`
          await new Promise(resolve => setTimeout(resolve, 100))
        }
        
        const filename = `backup_${new Date().toISOString().split('T')[0]}.zip`
        const blob = new Blob(['نسخة احتياطية تجريبية'], { type: 'application/zip' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        window.URL.revokeObjectURL(url)
        
        this.$toast.success('تم إنشاء النسخة الاحتياطية بنجاح')
      } catch (error) {
        console.error('خطأ في إنشاء النسخة الاحتياطية:', error)
        this.$toast.error('فشل في إنشاء النسخة الاحتياطية')
      } finally {
        this.showProgressModal = false
      }
    },
    
    handleDrop(event) {
      event.preventDefault()
      this.dragOver = false
      
      const files = event.dataTransfer.files
      if (files.length > 0) {
        this.handleFileSelect({ target: { files } })
      }
    },
    
    async handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        // التحقق من حجم الملف
        if (file.size > 50 * 1024 * 1024) { // 50MB
          this.$toast.error('حجم الملف كبير جداً. الحد الأقصى 50 ميجابايت')
          return
        }
        
        // التحقق من نوع الملف
        const allowedTypes = ['.csv', '.xlsx', '.xls', '.json']
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
        if (!allowedTypes.includes(fileExtension)) {
          this.$toast.error('نوع الملف غير مدعوم. الصيغ المدعومة: CSV, Excel, JSON')
          return
        }
        
        this.importForm.file = file
        await this.analyzeFile(file)
      }
    },
    
    async analyzeFile(file) {
      try {
        // محاكاة تحليل الملف
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        this.fileAnalysis = {
          type: file.name.split('.').pop().toUpperCase(),
          rows: Math.floor(Math.random() * 1000) + 100,
          columns: Math.floor(Math.random() * 10) + 5,
          encoding: 'UTF-8',
          sampleColumns: ['الاسم', 'البريد الإلكتروني', 'رقم الهاتف', 'الدور', 'الحالة'],
          sampleData: [
            ['أحمد محمد', 'ahmed@example.com', '+966501234567', 'مستخدم', 'نشط'],
            ['فاطمة علي', 'fatima@example.com', '+966507654321', 'خبير', 'نشط'],
            ['محمد السعيد', 'mohamed@example.com', '+966509876543', 'مستخدم', 'غير نشط']
          ]
        }
        
        // تهيئة ربط الأعمدة
        this.columnMapping = {}
        this.fileAnalysis.sampleColumns.forEach((column, index) => {
          // محاولة ربط تلقائي بناءً على اسم العمود
          if (column.includes('اسم') || column.includes('الاسم')) {
            this.columnMapping[index] = 'name'
          } else if (column.includes('بريد') || column.includes('email')) {
            this.columnMapping[index] = 'email'
          } else if (column.includes('هاتف') || column.includes('phone')) {
            this.columnMapping[index] = 'phone'
          } else if (column.includes('دور') || column.includes('role')) {
            this.columnMapping[index] = 'role'
          } else if (column.includes('حالة') || column.includes('status')) {
            this.columnMapping[index] = 'status'
          }
        })
        
        this.$toast.success('تم تحليل الملف بنجاح')
      } catch (error) {
        console.error('خطأ في تحليل الملف:', error)
        this.$toast.error('فشل في تحليل الملف')
      }
    },
    
    removeFile() {
      this.importForm.file = null
      this.fileAnalysis = null
      this.columnMapping = {}
    },
    
    resetImportForm() {
      this.importForm = {
        file: null,
        skipFirstRow: true,
        validateData: true,
        updateExisting: false,
        createBackupBeforeImport: true
      }
      this.fileAnalysis = null
      this.columnMapping = {}
    },
    
    async importData() {
      this.importing = true
      this.showProgressModal = true
      this.progressTitle = 'استيراد البيانات'
      this.progress = 0
      
      try {
        // محاكاة عملية الاستيراد
        for (let i = 0; i <= 100; i += 5) {
          this.progress = i
          if (i < 20) {
            this.progressMessage = 'جاري قراءة الملف...'
          } else if (i < 50) {
            this.progressMessage = 'جاري التحقق من البيانات...'
          } else if (i < 80) {
            this.progressMessage = 'جاري حفظ البيانات...'
          } else {
            this.progressMessage = 'جاري إنهاء العملية...'
          }
          await new Promise(resolve => setTimeout(resolve, 100))
        }
        
        // إضافة إلى السجل
        this.operationHistory.unshift({
          id: Date.now(),
          type: 'import',
          dataType: 'بيانات مخصصة',
          description: `استيراد ${this.fileAnalysis.rows} صف من ${this.importForm.file.name}`,
          status: 'success',
          timestamp: new Date(),
          downloadUrl: null
        })
        
        this.$toast.success('تم استيراد البيانات بنجاح')
        this.resetImportForm()
      } catch (error) {
        console.error('خطأ في استيراد البيانات:', error)
        this.$toast.error('فشل في استيراد البيانات')
      } finally {
        this.importing = false
        this.showProgressModal = false
      }
    },
    
    async downloadTemplate(templateId) {
      try {
        // محاكاة تحميل القالب
        const template = this.templates.find(t => t.id === templateId)
        const filename = `${template.name.replace(/\s+/g, '_')}.csv`
        
        let csvContent = ''
        if (templateId === 'users_template') {
          csvContent = 'الاسم,البريد الإلكتروني,رقم الهاتف,الدور,الحالة\nأحمد محمد,ahmed@example.com,+966501234567,مستخدم,نشط'
        } else if (templateId === 'diagnoses_template') {
          csvContent = 'اسم المرض,مستوى الثقة,الوصف,تاريخ التشخيص\nصدأ الأوراق,0.85,مرض فطري يصيب الأوراق,2025-06-17'
        } else {
          csvContent = 'العمود 1,العمود 2,العمود 3\nقيمة 1,قيمة 2,قيمة 3'
        }
        
        const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        window.URL.revokeObjectURL(url)
        
        this.$toast.success('تم تحميل القالب بنجاح')
      } catch (error) {
        console.error('خطأ في تحميل القالب:', error)
        this.$toast.error('فشل في تحميل القالب')
      }
    },
    
    downloadFile(url) {
      const a = document.createElement('a')
      a.href = url
      a.download = ''
      a.click()
    },
    
    deleteOperation(operationId) {
      if (confirm('هل أنت متأكد من حذف هذه العملية من السجل؟')) {
        this.operationHistory = this.operationHistory.filter(op => op.id !== operationId)
        this.$toast.success('تم حذف العملية من السجل')
      }
    },
    
    clearHistory() {
      if (confirm('هل أنت متأكد من مسح جميع سجلات العمليات؟')) {
        this.operationHistory = []
        this.$toast.success('تم مسح سجل العمليات')
      }
    },
    
    getFileIcon(filename) {
      const extension = filename.split('.').pop().toLowerCase()
      const icons = {
        csv: 'fas fa-file-csv',
        xlsx: 'fas fa-file-excel',
        xls: 'fas fa-file-excel',
        json: 'fas fa-file-code',
        xml: 'fas fa-file-code'
      }
      return icons[extension] || 'fas fa-file'
    },
    
    getStatusText(status) {
      const texts = {
        success: 'نجح',
        failed: 'فشل',
        pending: 'قيد التنفيذ'
      }
      return texts[status] || status
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 بايت'
      const k = 1024
      const sizes = ['بايت', 'كيلوبايت', 'ميجابايت', 'جيجابايت']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString('ar-SA')
    },
    
    formatTime(date) {
      return new Date(date).toLocaleString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
/* استخدام نفس الأنماط الأساسية من الصفحات السابقة مع تخصيصات إضافية */
.import-export-page {
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2E7D32;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-description {
  color: #666;
  margin: 0.5rem 0 0 0;
  font-size: 1.1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

.action-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}

.action-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
}

.action-card.export .action-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.action-card.import .action-icon {
  background: linear-gradient(135deg, #007bff, #6f42c1);
}

.action-card.backup .action-icon {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
}

.action-content h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.3rem;
}

.action-content p {
  margin: 0 0 1rem 0;
  color: #666;
}

.export-section,
.import-section,
.history-section {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  overflow: hidden;
}

.section-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.section-header h2 {
  margin: 0 0 0.5rem 0;
  color: #2E7D32;
  font-size: 1.5rem;
}

.section-header p {
  margin: 0;
  color: #666;
}

.export-form,
.import-form {
  padding: 2rem;
}

.form-grid {
  display: grid;
  gap: 2rem;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group label {
  font-weight: 600;
  color: #333;
  font-size: 1.1rem;
}

.data-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.data-type-card {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.data-type-card:hover {
  border-color: #2E7D32;
  background: rgba(46, 125, 50, 0.05);
}

.data-type-card.selected {
  border-color: #2E7D32;
  background: rgba(46, 125, 50, 0.1);
}

.type-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.type-info {
  flex: 1;
}

.type-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.type-info p {
  margin: 0 0 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.type-info small {
  color: #999;
  font-size: 0.8rem;
}

.type-checkbox {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #2E7D32;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.data-type-card.selected .type-checkbox {
  opacity: 1;
}

.format-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.format-option {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.format-option:hover {
  border-color: #2E7D32;
}

.format-option.selected {
  border-color: #2E7D32;
  background: rgba(46, 125, 50, 0.1);
}

.format-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.format-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.format-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.export-options,
.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.option-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.option-item label {
  margin: 0;
  color: #333;
  font-weight: 500;
  cursor: pointer;
}

.date-range {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.date-input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.date-input-group label {
  font-weight: 500;
  color: #666;
  font-size: 0.9rem;
}

.form-control {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #2E7D32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
}

.export-actions,
.import-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.upload-area {
  border: 3px dashed #e9ecef;
  border-radius: 15px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 2rem;
}

.upload-area:hover {
  border-color: #2E7D32;
  background: rgba(46, 125, 50, 0.05);
}

.upload-area.drag-over {
  border-color: #2E7D32;
  background: rgba(46, 125, 50, 0.1);
}

.upload-area.has-file {
  border-color: #28a745;
  background: rgba(40, 167, 69, 0.05);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  font-size: 4rem;
  color: #2E7D32;
}

.upload-placeholder h3 {
  margin: 0;
  color: #333;
  font-size: 1.3rem;
}

.upload-placeholder p {
  margin: 0;
  color: #666;
}

.upload-placeholder small {
  color: #999;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  position: relative;
}

.file-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.file-details h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.file-details p {
  margin: 0 0 0.25rem 0;
  color: #666;
}

.file-details small {
  color: #999;
}

.remove-file {
  position: absolute;
  top: -10px;
  left: -10px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #dc3545;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-analysis {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.file-analysis h3 {
  margin: 0 0 1.5rem 0;
  color: #2E7D32;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.analysis-item {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.analysis-item label {
  display: block;
  font-weight: 600;
  color: #666;
  margin-bottom: 0.5rem;
}

.analysis-item span {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2E7D32;
}

.column-mapping {
  margin-bottom: 2rem;
}

.column-mapping h4 {
  margin: 0 0 1rem 0;
  color: #333;
}

.mapping-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mapping-item {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1rem;
  align-items: center;
  background: white;
  padding: 1rem;
  border-radius: 8px;
}

.source-column,
.target-column {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.source-column label,
.target-column label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.source-column span {
  color: #333;
  font-weight: 500;
}

.mapping-arrow {
  color: #2E7D32;
  font-size: 1.2rem;
}

.data-preview {
  margin-bottom: 2rem;
}

.data-preview h4 {
  margin: 0 0 1rem 0;
  color: #333;
}

.preview-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e9ecef;
}

.preview-table table {
  width: 100%;
  border-collapse: collapse;
}

.preview-table th,
.preview-table td {
  padding: 0.75rem;
  text-align: right;
  border-bottom: 1px solid #f0f0f0;
}

.preview-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.import-options {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.import-options h3 {
  margin: 0 0 1.5rem 0;
  color: #2E7D32;
}

.history-controls {
  display: flex;
  gap: 1rem;
}

.history-list {
  padding: 1rem;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 10px;
  margin-bottom: 1rem;
  border-left: 4px solid #2E7D32;
}

.history-item.failed {
  border-left-color: #dc3545;
}

.operation-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.operation-info {
  flex: 1;
}

.operation-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.operation-info p {
  margin: 0 0 0.25rem 0;
  color: #666;
}

.operation-info small {
  color: #999;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge.success {
  background: #d4edda;
  color: #155724;
}

.status-badge.failed {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.operation-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.btn-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.btn-primary { background: #007bff; }
.btn-danger { background: #dc3545; }

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-warning {
  background: #ffc107;
  color: #000;
}

.btn-outline-secondary {
  background: transparent;
  color: #6c757d;
  border: 2px solid #6c757d;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 15px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.large-modal {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  color: #2E7D32;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.template-card {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.template-card:hover {
  border-color: #2E7D32;
  background: rgba(46, 125, 50, 0.05);
}

.template-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin: 0 auto 1rem auto;
}

.template-info h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.template-info p {
  margin: 0 0 1rem 0;
  color: #666;
  font-size: 0.9rem;
}

.progress-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2E7D32, #4CAF50);
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-weight: 600;
  color: #2E7D32;
  font-size: 1.1rem;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1200px) {
  .quick-actions {
    grid-template-columns: 1fr;
  }
  
  .data-types {
    grid-template-columns: 1fr;
  }
  
  .analysis-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .import-export-page {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .action-card {
    flex-direction: column;
    text-align: center;
  }
  
  .format-options {
    grid-template-columns: 1fr;
  }
  
  .export-options,
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .date-range {
    grid-template-columns: 1fr;
  }
  
  .analysis-grid {
    grid-template-columns: 1fr;
  }
  
  .mapping-item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .mapping-arrow {
    transform: rotate(90deg);
  }
  
  .history-item {
    flex-direction: column;
    text-align: center;
  }
  
  .templates-grid {
    grid-template-columns: 1fr;
  }
}
</style>

