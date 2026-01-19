<!-- File: /home/ubuntu/clean_project/frontend/pages/admin/Settings.vue -->
<template>
  <div class="settings-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="fas fa-cog"></i>
          إعدادات النظام
        </h1>
        <p class="page-description">
          إدارة وتخصيص إعدادات النظام العامة والمتقدمة
        </p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="saveAllSettings" :disabled="saving">
          <i class="fas fa-save"></i>
          {{ saving ? 'جاري الحفظ...' : 'حفظ جميع الإعدادات' }}
        </button>
      </div>
    </div>

    <!-- Settings Tabs -->
    <div class="settings-container">
      <div class="settings-sidebar">
        <nav class="settings-nav">
          <a 
            v-for="tab in settingsTabs" 
            :key="tab.id"
            :class="['nav-item', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            <i :class="tab.icon"></i>
            <span>{{ tab.name }}</span>
          </a>
        </nav>
      </div>

      <div class="settings-content">
        <!-- General Settings -->
        <div v-if="activeTab === 'general'" class="settings-section">
          <div class="section-header">
            <h2>الإعدادات العامة</h2>
            <p>إعدادات النظام الأساسية والعامة</p>
          </div>

          <div class="settings-grid">
            <div class="setting-group">
              <label class="setting-label">اسم النظام</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="settings.general.systemName"
                placeholder="WhatIsScanAI"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">وصف النظام</label>
              <textarea 
                class="form-control" 
                v-model="settings.general.systemDescription"
                rows="3"
                placeholder="نظام ذكي لتشخيص أمراض النباتات"
              ></textarea>
            </div>

            <div class="setting-group">
              <label class="setting-label">اللغة الافتراضية</label>
              <select class="form-control" v-model="settings.general.defaultLanguage">
                <option value="ar">العربية</option>
                <option value="en">English</option>
                <option value="fr">Français</option>
              </select>
            </div>

            <div class="setting-group">
              <label class="setting-label">المنطقة الزمنية</label>
              <select class="form-control" v-model="settings.general.timezone">
                <option value="Asia/Riyadh">الرياض (GMT+3)</option>
                <option value="Asia/Dubai">دبي (GMT+4)</option>
                <option value="Africa/Cairo">القاهرة (GMT+2)</option>
                <option value="UTC">UTC (GMT+0)</option>
              </select>
            </div>

            <div class="setting-group">
              <label class="setting-label">تنسيق التاريخ</label>
              <select class="form-control" v-model="settings.general.dateFormat">
                <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                <option value="YYYY-MM-DD">YYYY-MM-DD</option>
              </select>
            </div>

            <div class="setting-group">
              <label class="setting-label">عدد العناصر في الصفحة</label>
              <select class="form-control" v-model="settings.general.itemsPerPage">
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
          </div>
        </div>

        <!-- AI Settings -->
        <div v-if="activeTab === 'ai'" class="settings-section">
          <div class="section-header">
            <h2>إعدادات الذكاء الاصطناعي</h2>
            <p>تكوين نماذج وخدمات الذكاء الاصطناعي</p>
          </div>

          <div class="settings-grid">
            <div class="setting-group">
              <label class="setting-label">النموذج الافتراضي للتشخيص</label>
              <select class="form-control" v-model="settings.ai.defaultDiagnosisModel">
                <option value="yolo-v8">YOLO v8</option>
                <option value="resnet-50">ResNet-50</option>
                <option value="efficientnet">EfficientNet</option>
              </select>
            </div>

            <div class="setting-group">
              <label class="setting-label">حد الثقة الأدنى</label>
              <input 
                type="range" 
                class="form-range" 
                min="0.1" 
                max="1.0" 
                step="0.1"
                v-model="settings.ai.confidenceThreshold"
              >
              <span class="range-value">{{ settings.ai.confidenceThreshold }}</span>
            </div>

            <div class="setting-group">
              <label class="setting-label">عدد النتائج الأقصى</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="settings.ai.maxResults"
                min="1" 
                max="20"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">تفعيل التعلم التلقائي</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="autoLearning" 
                  v-model="settings.ai.autoLearning"
                >
                <label for="autoLearning" class="toggle-label"></label>
              </div>
            </div>

            <div class="setting-group">
              <label class="setting-label">تفعيل ذاكرة السياق</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="contextMemory" 
                  v-model="settings.ai.contextMemory"
                >
                <label for="contextMemory" class="toggle-label"></label>
              </div>
            </div>

            <div class="setting-group">
              <label class="setting-label">مدة الاحتفاظ بالذاكرة (أيام)</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="settings.ai.memoryRetentionDays"
                min="1" 
                max="365"
              >
            </div>
          </div>
        </div>

        <!-- Security Settings -->
        <div v-if="activeTab === 'security'" class="settings-section">
          <div class="section-header">
            <h2>إعدادات الأمان</h2>
            <p>تكوين أمان النظام والمصادقة</p>
          </div>

          <div class="settings-grid">
            <div class="setting-group">
              <label class="setting-label">مدة انتهاء الجلسة (دقائق)</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="settings.security.sessionTimeout"
                min="5" 
                max="1440"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">عدد محاولات تسجيل الدخول</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="settings.security.maxLoginAttempts"
                min="3" 
                max="10"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">تفعيل المصادقة الثنائية</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="twoFactorAuth" 
                  v-model="settings.security.twoFactorAuth"
                >
                <label for="twoFactorAuth" class="toggle-label"></label>
              </div>
            </div>

            <div class="setting-group">
              <label class="setting-label">تفعيل تسجيل الأنشطة</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="activityLogging" 
                  v-model="settings.security.activityLogging"
                >
                <label for="activityLogging" class="toggle-label"></label>
              </div>
            </div>

            <div class="setting-group">
              <label class="setting-label">مستوى التشفير</label>
              <select class="form-control" v-model="settings.security.encryptionLevel">
                <option value="basic">أساسي (AES-128)</option>
                <option value="standard">قياسي (AES-256)</option>
                <option value="advanced">متقدم (AES-256 + RSA)</option>
              </select>
            </div>

            <div class="setting-group">
              <label class="setting-label">تفعيل HTTPS فقط</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="httpsOnly" 
                  v-model="settings.security.httpsOnly"
                >
                <label for="httpsOnly" class="toggle-label"></label>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Settings -->
        <div v-if="activeTab === 'performance'" class="settings-section">
          <div class="section-header">
            <h2>إعدادات الأداء</h2>
            <p>تحسين أداء النظام والموارد</p>
          </div>

          <div class="settings-grid">
            <div class="setting-group">
              <label class="setting-label">حجم ذاكرة التخزين المؤقت (MB)</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="settings.performance.cacheSize"
                min="100" 
                max="2048"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">مدة انتهاء التخزين المؤقت (ثواني)</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="settings.performance.cacheExpiry"
                min="60" 
                max="3600"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">عدد العمليات المتزامنة</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="settings.performance.maxConcurrentOperations"
                min="1" 
                max="20"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">تفعيل ضغط البيانات</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="dataCompression" 
                  v-model="settings.performance.dataCompression"
                >
                <label for="dataCompression" class="toggle-label"></label>
              </div>
            </div>

            <div class="setting-group">
              <label class="setting-label">تفعيل التحميل التدريجي</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="lazyLoading" 
                  v-model="settings.performance.lazyLoading"
                >
                <label for="lazyLoading" class="toggle-label"></label>
              </div>
            </div>

            <div class="setting-group">
              <label class="setting-label">مستوى جودة الصور</label>
              <select class="form-control" v-model="settings.performance.imageQuality">
                <option value="low">منخفض (سريع)</option>
                <option value="medium">متوسط (متوازن)</option>
                <option value="high">عالي (جودة)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Backup Settings -->
        <div v-if="activeTab === 'backup'" class="settings-section">
          <div class="section-header">
            <h2>إعدادات النسخ الاحتياطي</h2>
            <p>تكوين النسخ الاحتياطي والاستعادة</p>
          </div>

          <div class="settings-grid">
            <div class="setting-group">
              <label class="setting-label">تفعيل النسخ الاحتياطي التلقائي</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="autoBackup" 
                  v-model="settings.backup.autoBackup"
                >
                <label for="autoBackup" class="toggle-label"></label>
              </div>
            </div>

            <div class="setting-group">
              <label class="setting-label">تكرار النسخ الاحتياطي</label>
              <select class="form-control" v-model="settings.backup.frequency">
                <option value="daily">يومي</option>
                <option value="weekly">أسبوعي</option>
                <option value="monthly">شهري</option>
              </select>
            </div>

            <div class="setting-group">
              <label class="setting-label">وقت النسخ الاحتياطي</label>
              <input 
                type="time" 
                class="form-control" 
                v-model="settings.backup.backupTime"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">عدد النسخ المحفوظة</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="settings.backup.retentionCount"
                min="1" 
                max="30"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">مسار النسخ الاحتياطي</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="settings.backup.backupPath"
                placeholder="/backup/whatisScanAI"
              >
            </div>

            <div class="setting-group">
              <label class="setting-label">تشفير النسخ الاحتياطي</label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="encryptBackup" 
                  v-model="settings.backup.encryptBackup"
                >
                <label for="encryptBackup" class="toggle-label"></label>
              </div>
            </div>
          </div>

          <div class="backup-actions">
            <button class="btn btn-outline-primary" @click="createBackup">
              <i class="fas fa-download"></i>
              إنشاء نسخة احتياطية الآن
            </button>
            <button class="btn btn-outline-success" @click="restoreBackup">
              <i class="fas fa-upload"></i>
              استعادة من نسخة احتياطية
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Save Confirmation Modal -->
    <div v-if="showSaveModal" class="modal-overlay" @click="showSaveModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>تأكيد الحفظ</h3>
          <button class="modal-close" @click="showSaveModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>هل أنت متأكد من حفظ جميع الإعدادات؟ قد تحتاج بعض التغييرات إلى إعادة تشغيل النظام.</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showSaveModal = false">إلغاء</button>
          <button class="btn btn-primary" @click="confirmSave">تأكيد الحفظ</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      activeTab: 'general',
      saving: false,
      showSaveModal: false,
      settingsTabs: [
        { id: 'general', name: 'عام', icon: 'fas fa-cog' },
        { id: 'ai', name: 'الذكاء الاصطناعي', icon: 'fas fa-brain' },
        { id: 'security', name: 'الأمان', icon: 'fas fa-shield-alt' },
        { id: 'performance', name: 'الأداء', icon: 'fas fa-tachometer-alt' },
        { id: 'backup', name: 'النسخ الاحتياطي', icon: 'fas fa-database' }
      ],
      settings: {
        general: {
          systemName: 'WhatIsScanAI',
          systemDescription: 'نظام ذكي لتشخيص أمراض النباتات باستخدام الذكاء الاصطناعي',
          defaultLanguage: 'ar',
          timezone: 'Asia/Riyadh',
          dateFormat: 'DD/MM/YYYY',
          itemsPerPage: 25
        },
        ai: {
          defaultDiagnosisModel: 'yolo-v8',
          confidenceThreshold: 0.7,
          maxResults: 10,
          autoLearning: true,
          contextMemory: true,
          memoryRetentionDays: 30
        },
        security: {
          sessionTimeout: 60,
          maxLoginAttempts: 5,
          twoFactorAuth: false,
          activityLogging: true,
          encryptionLevel: 'standard',
          httpsOnly: true
        },
        performance: {
          cacheSize: 512,
          cacheExpiry: 300,
          maxConcurrentOperations: 5,
          dataCompression: true,
          lazyLoading: true,
          imageQuality: 'medium'
        },
        backup: {
          autoBackup: true,
          frequency: 'daily',
          backupTime: '02:00',
          retentionCount: 7,
          backupPath: '/backup/whatisScanAI',
          encryptBackup: true
        }
      }
    }
  },
  mounted() {
    this.loadSettings()
  },
  methods: {
    async loadSettings() {
      try {
        // تحميل الإعدادات من الخادم
        const response = await fetch('/api/settings')
        if (response.ok) {
          const data = await response.json()
          this.settings = { ...this.settings, ...data }
        }
      } catch (error) {
        console.error('خطأ في تحميل الإعدادات:', error)
        this.$toast.error('فشل في تحميل الإعدادات')
      }
    },
    
    saveAllSettings() {
      this.showSaveModal = true
    },
    
    async confirmSave() {
      this.saving = true
      this.showSaveModal = false
      
      try {
        const response = await fetch('/api/settings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.settings)
        })
        
        if (response.ok) {
          this.$toast.success('تم حفظ الإعدادات بنجاح')
        } else {
          throw new Error('فشل في حفظ الإعدادات')
        }
      } catch (error) {
        console.error('خطأ في حفظ الإعدادات:', error)
        this.$toast.error('فشل في حفظ الإعدادات')
      } finally {
        this.saving = false
      }
    },
    
    async createBackup() {
      try {
        this.$toast.info('جاري إنشاء النسخة الاحتياطية...')
        
        const response = await fetch('/api/backup/create', {
          method: 'POST'
        })
        
        if (response.ok) {
          this.$toast.success('تم إنشاء النسخة الاحتياطية بنجاح')
        } else {
          throw new Error('فشل في إنشاء النسخة الاحتياطية')
        }
      } catch (error) {
        console.error('خطأ في إنشاء النسخة الاحتياطية:', error)
        this.$toast.error('فشل في إنشاء النسخة الاحتياطية')
      }
    },
    
    async restoreBackup() {
      // فتح نافذة اختيار الملف
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = '.zip,.tar.gz'
      input.onchange = async (event) => {
        const file = event.target.files[0]
        if (file) {
          try {
            this.$toast.info('جاري استعادة النسخة الاحتياطية...')
            
            const formData = new FormData()
            formData.append('backup', file)
            
            const response = await fetch('/api/backup/restore', {
              method: 'POST',
              body: formData
            })
            
            if (response.ok) {
              this.$toast.success('تم استعادة النسخة الاحتياطية بنجاح')
              setTimeout(() => {
                window.location.reload()
              }, 2000)
            } else {
              throw new Error('فشل في استعادة النسخة الاحتياطية')
            }
          } catch (error) {
            console.error('خطأ في استعادة النسخة الاحتياطية:', error)
            this.$toast.error('فشل في استعادة النسخة الاحتياطية')
          }
        }
      }
      input.click()
    }
  }
}
</script>

<style scoped>
.settings-page {
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

.settings-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
  height: calc(100vh - 200px);
}

.settings-sidebar {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  height: fit-content;
}

.settings-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  color: #666;
  font-weight: 500;
}

.nav-item:hover {
  background: #f8f9fa;
  color: #2E7D32;
  transform: translateX(5px);
}

.nav-item.active {
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
}

.settings-content {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  overflow-y: auto;
}

.section-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.section-header h2 {
  color: #2E7D32;
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.section-header p {
  color: #666;
  margin: 0;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.setting-label {
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
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

.form-range {
  width: 100%;
  margin: 0.5rem 0;
}

.range-value {
  display: inline-block;
  background: #2E7D32;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 600;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 30px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-label {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 30px;
}

.toggle-label:before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .toggle-label {
  background-color: #2E7D32;
}

input:checked + .toggle-label:before {
  transform: translateX(30px);
}

.backup-actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 2px solid #f0f0f0;
}

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

.btn-primary {
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(46, 125, 50, 0.3);
}

.btn-outline-primary {
  background: transparent;
  color: #2E7D32;
  border: 2px solid #2E7D32;
}

.btn-outline-primary:hover {
  background: #2E7D32;
  color: white;
}

.btn-outline-success {
  background: transparent;
  color: #4CAF50;
  border: 2px solid #4CAF50;
}

.btn-outline-success:hover {
  background: #4CAF50;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
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

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

@media (max-width: 768px) {
  .settings-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .settings-sidebar {
    order: 2;
  }
  
  .settings-content {
    order: 1;
  }
  
  .settings-nav {
    flex-direction: row;
    overflow-x: auto;
  }
  
  .nav-item {
    white-space: nowrap;
    min-width: 150px;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>

