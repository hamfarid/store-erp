<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/ContainerManager.vue
الوصف: مكون إدارة الحاويات في شاشة الإعدادات
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="container-manager">
    <div class="header">
      <h2 class="title">إدارة الحاويات</h2>
      <p class="description">
        يمكنك من هنا إدارة حاويات النظام وتثبيت حاويات إضافية حسب احتياجاتك
      </p>
    </div>

    <div class="container-groups">
      <div class="group-tabs">
        <div 
          v-for="(group, index) in containerGroups" 
          :key="index"
          :class="['group-tab', { active: activeGroup === index }]"
          @click="activeGroup = index"
        >
          {{ group.name }}
        </div>
      </div>

      <div class="group-content">
        <div class="group-info">
          <h3>{{ containerGroups[activeGroup].name }}</h3>
          <p>{{ containerGroups[activeGroup].description }}</p>
        </div>

        <div class="containers-list">
          <div 
            v-for="(container, index) in containerGroups[activeGroup].containers" 
            :key="index"
            class="container-item"
          >
            <div class="container-header">
              <div class="container-name">{{ container.name }}</div>
              <div :class="['container-status', container.status]">{{ getStatusText(container.status) }}</div>
            </div>
            <div class="container-description">{{ container.description }}</div>
            <div class="container-actions">
              <button 
                v-if="container.status === 'not_installed'"
                class="btn install"
                @click="installContainer(container)"
              >
                تثبيت
              </button>
              <button 
                v-if="container.status === 'running'"
                class="btn stop"
                @click="stopContainer(container)"
              >
                إيقاف
              </button>
              <button 
                v-if="container.status === 'stopped'"
                class="btn start"
                @click="startContainer(container)"
              >
                تشغيل
              </button>
              <button 
                v-if="container.status !== 'not_installed'"
                class="btn restart"
                @click="restartContainer(container)"
              >
                إعادة تشغيل
              </button>
              <button 
                v-if="container.status !== 'not_installed'"
                class="btn remove"
                @click="removeContainer(container)"
              >
                إزالة
              </button>
              <button 
                class="btn configure"
                @click="configureContainer(container)"
              >
                إعدادات
              </button>
              <button 
                v-if="container.status !== 'not_installed'"
                class="btn logs"
                @click="viewLogs(container)"
              >
                السجلات
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة تثبيت الحاوية -->
    <div v-if="showInstallDialog" class="dialog-overlay">
      <div class="dialog">
        <div class="dialog-header">
          <h3>تثبيت {{ selectedContainer.name }}</h3>
          <button class="close-btn" @click="showInstallDialog = false">&times;</button>
        </div>
        <div class="dialog-content">
          <p>{{ selectedContainer.description }}</p>
          
          <div class="form-group">
            <label for="container-cpu">CPU</label>
            <input 
              id="container-cpu"
              type="number" 
              v-model="containerConfig.cpu" 
              min="1"
              max="16"
            />
          </div>
          
          <div class="form-group">
            <label for="container-memory">الذاكرة (GB)</label>
            <input 
              id="container-memory"
              type="number" 
              v-model="containerConfig.memory" 
              min="1"
              max="64"
            />
          </div>
          
          <div class="form-group">
            <label for="container-gpu">GPU</label>
            <input 
              id="container-gpu"
              type="checkbox" 
              v-model="containerConfig.useGPU"
            />
          </div>
          
          <div class="form-group">
            <label for="container-port">المنفذ</label>
            <input 
              id="container-port"
              type="number" 
              v-model="containerConfig.ports[0].container" 
              min="1"
              max="65535"
            />
          </div>
          
          <div class="form-group">
            <label for="container-host-port">منفذ المضيف</label>
            <input 
              id="container-host-port"
              type="number" 
              v-model="containerConfig.ports[0].host" 
              min="1"
              max="65535"
            />
          </div>
          
          <div class="form-group">
            <label for="container-env-key">المفتاح</label>
            <input 
              id="container-env-key"
              type="text" 
              v-model="containerConfig.env[0].key" 
              placeholder="مثال: API_KEY"
            />
          </div>
          
          <div class="form-group">
            <label for="container-env-value">القيمة</label>
            <input 
              id="container-env-value"
              type="text" 
              v-model="containerConfig.env[0].value" 
              placeholder="مثال: your-api-key"
            />
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn cancel" @click="showInstallDialog = false">إلغاء</button>
          <button class="btn install" @click="confirmInstall">تثبيت</button>
        </div>
      </div>
    </div>

    <!-- نافذة عرض السجلات -->
    <div v-if="showLogsDialog" class="dialog-overlay">
      <div class="dialog logs-dialog">
        <div class="dialog-header">
          <h3>سجلات {{ selectedContainer.name }}</h3>
          <button class="close-btn" @click="showLogsDialog = false">&times;</button>
        </div>
        <div class="dialog-content">
          <div class="logs-container">
            <pre>{{ containerLogs }}</pre>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn refresh" @click="refreshLogs">تحديث</button>
          <button class="btn close" @click="showLogsDialog = false">إغلاق</button>
        </div>
      </div>
    </div>

    <!-- نافذة إعدادات الحاوية -->
    <div v-if="showConfigDialog" class="dialog-overlay">
      <div class="dialog">
        <div class="dialog-header">
          <h3>إعدادات {{ selectedContainer.name }}</h3>
          <button class="close-btn" @click="showConfigDialog = false">&times;</button>
        </div>
        <div class="dialog-content">
          <!-- محتوى الإعدادات يعتمد على نوع الحاوية -->
          <div v-if="selectedContainer.type === 'ai_model'" class="ai-model-settings">
            <div class="form-group">
              <label for="container-model-type">نوع النموذج</label>
              <select 
                id="container-model-type"
                v-model="containerConfig.modelType"
              >
                <option value="classification">تصنيف</option>
                <option value="detection">كشف</option>
                <option value="segmentation">تجزئة</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="container-model-precision">دقة النموذج</label>
              <select 
                id="container-model-precision"
                v-model="containerConfig.modelPrecision"
              >
                <option value="fp32">FP32</option>
                <option value="fp16">FP16</option>
                <option value="int8">INT8</option>
              </select>
            </div>
          </div>
          <div v-else-if="selectedContainer.type === 'database'" class="database-settings">
            <div class="form-group">
              <label for="container-db-name">اسم قاعدة البيانات</label>
              <input 
                id="container-db-name"
                type="text" 
                v-model="containerConfig.dbName" 
                placeholder="مثال: my_database"
              />
            </div>
            
            <div class="form-group">
              <label for="container-db-user">اسم المستخدم</label>
              <input 
                id="container-db-user"
                type="text" 
                v-model="containerConfig.dbUser" 
                placeholder="مثال: admin"
              />
            </div>
            
            <div class="form-group">
              <label for="container-db-password">كلمة المرور</label>
              <input 
                id="container-db-password"
                type="password" 
                v-model="containerConfig.dbPassword" 
                placeholder="كلمة المرور"
              />
            </div>
          </div>
          <div v-else>
            <div class="form-group">
              <label>إعدادات عامة</label>
              <textarea v-model="containerConfig.generalConfig" rows="10"></textarea>
            </div>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn cancel" @click="showConfigDialog = false">إلغاء</button>
          <button class="btn save" @click="saveConfig">حفظ</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useTheme } from '@/composables/useTheme';
import { useToast } from '@/composables/useToast';
import containerService from '@/services/containerService';
import { onMounted, reactive, ref } from 'vue';

export default {
  name: 'ContainerManager',
  
  setup() {
    const { showToast } = useToast();
    const { theme } = useTheme();
    
    const activeGroup = ref(0);
    const containerGroups = ref([
      {
        name: 'الحاويات الأساسية',
        description: 'الحاويات الأساسية للنظام',
        containers: [
          {
            id: 'app',
            name: 'التطبيق الرئيسي',
            description: 'خدمة التطبيق الرئيسي',
            status: 'running',
            type: 'app'
          },
          {
            id: 'db',
            name: 'قاعدة البيانات',
            description: 'قاعدة بيانات PostgreSQL',
            status: 'running',
            type: 'database'
          },
          {
            id: 'redis',
            name: 'التخزين المؤقت',
            description: 'خدمة Redis للتخزين المؤقت',
            status: 'running',
            type: 'cache'
          },
          {
            id: 'minio',
            name: 'تخزين الملفات',
            description: 'خدمة MinIO لتخزين الملفات',
            status: 'running',
            type: 'storage'
          },
          {
            id: 'nginx',
            name: 'خادم الويب',
            description: 'خدمة Nginx لتوزيع الطلبات',
            status: 'running',
            type: 'web'
          }
        ]
      },
      {
        name: 'حاويات GPU المتقدمة',
        description: 'حاويات مدعومة بـ GPU لتسريع عمليات الذكاء الاصطناعي',
        containers: [
          {
            id: 'ai_central_gpu',
            name: 'الذكاء الاصطناعي المركزية مع GPU',
            description: 'خدمة الذكاء الاصطناعي المركزية مع دعم GPU',
            status: 'not_installed',
            type: 'ai_model',
            supportsGPU: true
          },
          {
            id: 'image_processing_gpu',
            name: 'معالجة الصور المتقدمة مع GPU',
            description: 'خدمة معالجة الصور المتقدمة مع دعم GPU',
            status: 'not_installed',
            type: 'ai_model',
            supportsGPU: true
          },
          {
            id: 'disease_detection_gpu',
            name: 'تشخيص الأمراض المتقدمة مع GPU',
            description: 'خدمة تشخيص الأمراض المتقدمة مع دعم GPU',
            status: 'not_installed',
            type: 'ai_model',
            supportsGPU: true
          }
        ]
      },
      {
        name: 'حاويات البحث الخارجية المتقدمة',
        description: 'حاويات البحث الخارجية المتقدمة',
        containers: [
          {
            id: 'elasticsearch_advanced',
            name: 'Elasticsearch المتقدم',
            description: 'خدمة Elasticsearch المتقدمة للبحث',
            status: 'not_installed',
            type: 'search'
          },
          {
            id: 'kibana',
            name: 'Kibana',
            description: 'خدمة Kibana للتحليل البصري',
            status: 'not_installed',
            type: 'visualization'
          },
          {
            id: 'logstash',
            name: 'Logstash',
            description: 'خدمة Logstash لمعالجة البيانات',
            status: 'not_installed',
            type: 'data_processing'
          }
        ]
      },
      {
        name: 'حاويات بحث إصابات الأصناف المتقدمة',
        description: 'حاويات بحث إصابات الأصناف المتقدمة',
        containers: [
          {
            id: 'disease_knowledge_base',
            name: 'قاعدة المعرفة للأمراض والإصابات',
            description: 'خدمة قاعدة المعرفة للأمراض والإصابات',
            status: 'not_installed',
            type: 'knowledge_base'
          },
          {
            id: 'inference_engine',
            name: 'محرك الاستدلال للتشخيص المتقدم',
            description: 'خدمة محرك الاستدلال للتشخيص المتقدم',
            status: 'not_installed',
            type: 'ai_model'
          },
          {
            id: 'multispectral_analysis',
            name: 'تحليل الصور متعددة الطيف',
            description: 'خدمة تحليل الصور متعددة الطيف للكشف عن الإصابات',
            status: 'not_installed',
            type: 'ai_model',
            supportsGPU: true
          }
        ]
      },
      {
        name: 'حاويات التعلم الآلي والبحث عن الصور',
        description: 'حاويات التعلم الآلي والبحث عن الصور المتقدمة',
        containers: [
          {
            id: 'local_ml_service',
            name: 'خدمة التعلم الآلي المحلية',
            description: 'نموذج مجاني يعمل ضمن البنية التحتية للمستخدم',
            status: 'not_installed',
            type: 'ai_model'
          },
          {
            id: 'premium_ml_service',
            name: 'خدمة التعلم الآلي المتقدمة',
            description: 'نموذج مدفوع متقدم يعتمد على بنية سحابية',
            status: 'not_installed',
            type: 'ai_model',
            supportsGPU: true
          },
          {
            id: 'advanced_image_search',
            name: 'البحث عن الصور المتقدمة',
            description: 'خدمة للبحث عن الصور بالمحتوى البصري',
            status: 'not_installed',
            type: 'ai_model',
            supportsGPU: true
          }
        ]
      },
      {
        name: 'أنظمة تشخيص الأمراض الجاهزة',
        description: 'أنظمة تشخيص الأمراض الجاهزة (مفتوحة المصدر)',
        containers: [
          {
            id: 'fastai_resnet34',
            name: 'Plant Disease Detection - FastAI + ResNet34',
            description: 'نظام تشخيص الأمراض باستخدام FastAI + ResNet34',
            status: 'not_installed',
            type: 'ai_model'
          },
          {
            id: 'pytorch_implementation',
            name: 'Plant Disease Detection - PyTorch',
            description: 'نظام تشخيص الأمراض باستخدام PyTorch',
            status: 'not_installed',
            type: 'ai_model'
          },
          {
            id: 'keras_fastapi',
            name: 'Plant Disease Detection - Keras + FastAPI',
            description: 'نظام تشخيص الأمراض باستخدام Keras + FastAPI',
            status: 'not_installed',
            type: 'ai_model'
          }
        ]
      }
    ]);
    
    const showInstallDialog = ref(false);
    const showLogsDialog = ref(false);
    const showConfigDialog = ref(false);
    const selectedContainer = ref({});
    const containerLogs = ref('');
    
    const containerConfig = reactive({
      cpu: 1,
      memory: 2,
      useGPU: false,
      ports: [{ host: '', container: '' }],
      env: [{ key: '', value: '' }],
      modelType: 'local',
      modelPrecision: 'fp32',
      dbName: '',
      dbUser: '',
      dbPassword: '',
      generalConfig: ''
    });
    
    const getStatusText = (status) => {
      switch (status) {
        case 'running':
          return 'يعمل';
        case 'stopped':
          return 'متوقف';
        case 'error':
          return 'خطأ';
        case 'not_installed':
          return 'غير مثبت';
        default:
          return status;
      }
    };
    
    const installContainer = (container) => {
      selectedContainer.value = container;
      
      // إعادة تعيين الإعدادات
      containerConfig.cpu = 1;
      containerConfig.memory = 2;
      containerConfig.useGPU = container.supportsGPU || false;
      containerConfig.ports = [{ host: '', container: '' }];
      containerConfig.env = [{ key: '', value: '' }];
      
      showInstallDialog.value = true;
    };
    
    const confirmInstall = async () => {
      try {
        showToast('جاري تثبيت الحاوية...', 'info');
        
        // تحويل الإعدادات إلى الصيغة المطلوبة
        const config = {
          id: selectedContainer.value.id,
          resources: {
            cpu: containerConfig.cpu,
            memory: containerConfig.memory,
            gpu: containerConfig.useGPU
          },
          ports: containerConfig.ports.filter(p => p.host && p.container),
          env: containerConfig.env.reduce((obj, item) => {
            if (item.key) obj[item.key] = item.value;
            return obj;
          }, {})
        };
        
        // إضافة إعدادات خاصة حسب نوع الحاوية
        if (selectedContainer.value.type === 'ai_model') {
          config.modelType = containerConfig.modelType;
          config.modelPrecision = containerConfig.modelPrecision;
        } else if (selectedContainer.value.type === 'database') {
          config.dbName = containerConfig.dbName;
          config.dbUser = containerConfig.dbUser;
          config.dbPassword = containerConfig.dbPassword;
        }
        
        // استدعاء خدمة تثبيت الحاوية
        await containerService.installContainer(config);
        
        // تحديث حالة الحاوية
        const groupIndex = containerGroups.value.findIndex(group => 
          group.containers.some(c => c.id === selectedContainer.value.id)
        );
        
        if (groupIndex !== -1) {
          const containerIndex = containerGroups.value[groupIndex].containers.findIndex(
            c => c.id === selectedContainer.value.id
          );
          
          if (containerIndex !== -1) {
            containerGroups.value[groupIndex].containers[containerIndex].status = 'running';
          }
        }
        
        showToast('تم تثبيت الحاوية بنجاح', 'success');
        showInstallDialog.value = false;
      } catch (error) {
        console.error('Error installing container:', error);
        showToast('حدث خطأ أثناء تثبيت الحاوية', 'error');
      }
    };
    
    const stopContainer = async (container) => {
      try {
        showToast('جاري إيقاف الحاوية...', 'info');
        
        // استدعاء خدمة إيقاف الحاوية
        await containerService.stopContainer(container.id);
        
        // تحديث حالة الحاوية
        const groupIndex = containerGroups.value.findIndex(group => 
          group.containers.some(c => c.id === container.id)
        );
        
        if (groupIndex !== -1) {
          const containerIndex = containerGroups.value[groupIndex].containers.findIndex(
            c => c.id === container.id
          );
          
          if (containerIndex !== -1) {
            containerGroups.value[groupIndex].containers[containerIndex].status = 'stopped';
          }
        }
        
        showToast('تم إيقاف الحاوية بنجاح', 'success');
      } catch (error) {
        console.error('Error stopping container:', error);
        showToast('حدث خطأ أثناء إيقاف الحاوية', 'error');
      }
    };
    
    const startContainer = async (container) => {
      try {
        showToast('جاري تشغيل الحاوية...', 'info');
        
        // استدعاء خدمة تشغيل الحاوية
        await containerService.startContainer(container.id);
        
        // تحديث حالة الحاوية
        const groupIndex = containerGroups.value.findIndex(group => 
          group.containers.some(c => c.id === container.id)
        );
        
        if (groupIndex !== -1) {
          const containerIndex = containerGroups.value[groupIndex].containers.findIndex(
            c => c.id === container.id
          );
          
          if (containerIndex !== -1) {
            containerGroups.value[groupIndex].containers[containerIndex].status = 'running';
          }
        }
        
        showToast('تم تشغيل الحاوية بنجاح', 'success');
      } catch (error) {
        console.error('Error starting container:', error);
        showToast('حدث خطأ أثناء تشغيل الحاوية', 'error');
      }
    };
    
    const restartContainer = async (container) => {
      try {
        showToast('جاري إعادة تشغيل الحاوية...', 'info');
        
        // استدعاء خدمة إعادة تشغيل الحاوية
        await containerService.restartContainer(container.id);
        
        // تحديث حالة الحاوية
        const groupIndex = containerGroups.value.findIndex(group => 
          group.containers.some(c => c.id === container.id)
        );
        
        if (groupIndex !== -1) {
          const containerIndex = containerGroups.value[groupIndex].containers.findIndex(
            c => c.id === container.id
          );
          
          if (containerIndex !== -1) {
            containerGroups.value[groupIndex].containers[containerIndex].status = 'running';
          }
        }
        
        showToast('تم إعادة تشغيل الحاوية بنجاح', 'success');
      } catch (error) {
        console.error('Error restarting container:', error);
        showToast('حدث خطأ أثناء إعادة تشغيل الحاوية', 'error');
      }
    };
    
    const removeContainer = async (container) => {
      if (!confirm(`هل أنت متأكد من رغبتك في إزالة الحاوية "${container.name}"؟`)) {
        return;
      }
      
      try {
        showToast('جاري إزالة الحاوية...', 'info');
        
        // استدعاء خدمة إزالة الحاوية
        await containerService.removeContainer(container.id);
        
        // تحديث حالة الحاوية
        const groupIndex = containerGroups.value.findIndex(group => 
          group.containers.some(c => c.id === container.id)
        );
        
        if (groupIndex !== -1) {
          const containerIndex = containerGroups.value[groupIndex].containers.findIndex(
            c => c.id === container.id
          );
          
          if (containerIndex !== -1) {
            containerGroups.value[groupIndex].containers[containerIndex].status = 'not_installed';
          }
        }
        
        showToast('تم إزالة الحاوية بنجاح', 'success');
      } catch (error) {
        console.error('Error removing container:', error);
        showToast('حدث خطأ أثناء إزالة الحاوية', 'error');
      }
    };
    
    const viewLogs = async (container) => {
      selectedContainer.value = container;
      containerLogs.value = 'جاري تحميل السجلات...';
      showLogsDialog.value = true;
      
      try {
        // استدعاء خدمة عرض سجلات الحاوية
        const logs = await containerService.getContainerLogs(container.id);
        containerLogs.value = logs;
      } catch (error) {
        console.error('Error fetching container logs:', error);
        containerLogs.value = 'حدث خطأ أثناء تحميل السجلات';
      }
    };
    
    const refreshLogs = async () => {
      containerLogs.value = 'جاري تحديث السجلات...';
      
      try {
        // استدعاء خدمة عرض سجلات الحاوية
        const logs = await containerService.getContainerLogs(selectedContainer.value.id);
        containerLogs.value = logs;
      } catch (error) {
        console.error('Error refreshing container logs:', error);
        containerLogs.value = 'حدث خطأ أثناء تحديث السجلات';
      }
    };
    
    const configureContainer = (container) => {
      selectedContainer.value = container;
      
      // إعادة تعيين الإعدادات حسب نوع الحاوية
      if (container.type === 'ai_model') {
        containerConfig.modelType = 'local';
        containerConfig.modelPrecision = 'fp32';
      } else if (container.type === 'database') {
        containerConfig.dbName = '';
        containerConfig.dbUser = '';
        containerConfig.dbPassword = '';
      } else {
        containerConfig.generalConfig = '';
      }
      
      showConfigDialog.value = true;
    };
    
    const saveConfig = async () => {
      try {
        showToast('جاري حفظ الإعدادات...', 'info');
        
        // تحويل الإعدادات إلى الصيغة المطلوبة
        const config = {
          id: selectedContainer.value.id
        };
        
        // إضافة إعدادات خاصة حسب نوع الحاوية
        if (selectedContainer.value.type === 'ai_model') {
          config.modelType = containerConfig.modelType;
          config.modelPrecision = containerConfig.modelPrecision;
        } else if (selectedContainer.value.type === 'database') {
          config.dbName = containerConfig.dbName;
          config.dbUser = containerConfig.dbUser;
          config.dbPassword = containerConfig.dbPassword;
        } else {
          config.generalConfig = containerConfig.generalConfig;
        }
        
        // استدعاء خدمة حفظ إعدادات الحاوية
        await containerService.saveContainerConfig(config);
        
        showToast('تم حفظ الإعدادات بنجاح', 'success');
        showConfigDialog.value = false;
      } catch (error) {
        console.error('Error saving container config:', error);
        showToast('حدث خطأ أثناء حفظ الإعدادات', 'error');
      }
    };
    
    const addPort = () => {
      containerConfig.ports.push({ host: '', container: '' });
    };
    
    const removePort = (index) => {
      containerConfig.ports.splice(index, 1);
    };
    
    const addEnv = () => {
      containerConfig.env.push({ key: '', value: '' });
    };
    
    const removeEnv = (index) => {
      containerConfig.env.splice(index, 1);
    };
    
    onMounted(async () => {
      try {
        // استدعاء خدمة الحصول على حالة الحاويات
        const containersStatus = await containerService.getContainersStatus();
        
        // تحديث حالة الحاويات
        containerGroups.value.forEach(group => {
          group.containers.forEach(container => {
            if (containersStatus[container.id]) {
              container.status = containersStatus[container.id];
            }
          });
        });
      } catch (error) {
        console.error('Error fetching containers status:', error);
        showToast('حدث خطأ أثناء تحميل حالة الحاويات', 'error');
      }
    });
    
    return {
      activeGroup,
      containerGroups,
      showInstallDialog,
      showLogsDialog,
      showConfigDialog,
      selectedContainer,
      containerLogs,
      containerConfig,
      getStatusText,
      installContainer,
      confirmInstall,
      stopContainer,
      startContainer,
      restartContainer,
      removeContainer,
      viewLogs,
      refreshLogs,
      configureContainer,
      saveConfig,
      addPort,
      removePort,
      addEnv,
      removeEnv
    };
  }
};
</script>

<style scoped>
.container-manager {
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

.container-groups {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.group-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.group-tab {
  padding: 10px 15px;
  background-color: var(--bg-secondary);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.group-tab.active {
  background-color: var(--primary-color);
  color: white;
}

.group-content {
  background-color: var(--bg-secondary);
  border-radius: 8px;
  padding: 20px;
}

.group-info {
  margin-bottom: 20px;
}

.group-info h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.containers-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.container-item {
  background-color: var(--bg-color);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.container-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.container-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.container-name {
  font-weight: bold;
  font-size: 16px;
}

.container-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.container-status.running {
  background-color: #e6f7e6;
  color: #28a745;
}

.container-status.stopped {
  background-color: #fff3cd;
  color: #ffc107;
}

.container-status.error {
  background-color: #f8d7da;
  color: #dc3545;
}

.container-status.not_installed {
  background-color: #e2e3e5;
  color: #6c757d;
}

.container-description {
  margin-bottom: 15px;
  color: var(--text-secondary);
  font-size: 14px;
}

.container-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.btn {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn:hover {
  opacity: 0.9;
}

.btn.install {
  background-color: #28a745;
  color: white;
}

.btn.stop {
  background-color: #ffc107;
  color: #212529;
}

.btn.start {
  background-color: #28a745;
  color: white;
}

.btn.restart {
  background-color: #17a2b8;
  color: white;
}

.btn.remove {
  background-color: #dc3545;
  color: white;
}

.btn.configure {
  background-color: #6c757d;
  color: white;
}

.btn.logs {
  background-color: #6610f2;
  color: white;
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

.logs-dialog {
  max-width: 800px;
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

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.resources {
  display: flex;
  gap: 15px;
}

.resource {
  flex: 1;
}

.resource label {
  display: block;
  margin-bottom: 5px;
  font-weight: normal;
}

input[type="text"],
input[type="number"],
input[type="password"],
select,
textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-color);
  color: var(--text-color);
}

.port-mapping,
.env-var {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.remove-btn {
  background: none;
  border: none;
  color: #dc3545;
  font-size: 18px;
  cursor: pointer;
}

.add-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.logs-container {
  background-color: #1e1e1e;
  color: #f8f8f8;
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  height: 400px;
  overflow-y: auto;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.btn.refresh {
  background-color: #17a2b8;
  color: white;
}

.btn.close,
.btn.cancel {
  background-color: #6c757d;
  color: white;
}

.btn.save {
  background-color: #28a745;
  color: white;
}

/* تخصيص للوضع الداكن */
:root[data-theme="dark"] .container-status.running {
  background-color: rgba(40, 167, 69, 0.2);
}

:root[data-theme="dark"] .container-status.stopped {
  background-color: rgba(255, 193, 7, 0.2);
}

:root[data-theme="dark"] .container-status.error {
  background-color: rgba(220, 53, 69, 0.2);
}

:root[data-theme="dark"] .container-status.not_installed {
  background-color: rgba(108, 117, 125, 0.2);
}

/* تخصيص للهوية البصرية */
:root[data-brand="gaaragroup"] .title,
:root[data-brand="gaaragroup"] .group-info h3 {
  color: var(--gaara-primary);
}

:root[data-brand="gaaragroup"] .group-tab.active {
  background-color: var(--gaara-primary);
}

:root[data-brand="gaaragroup"] .add-btn {
  background-color: var(--gaara-primary);
}

:root[data-brand="magseeds"] .title,
:root[data-brand="magseeds"] .group-info h3 {
  color: var(--mag-primary);
}

:root[data-brand="magseeds"] .group-tab.active {
  background-color: var(--mag-primary);
}

:root[data-brand="magseeds"] .add-btn {
  background-color: var(--mag-primary);
}
</style>
