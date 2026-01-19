<template>
  <div class="ai-avatar-wrapper">
    <AIAvatar 
      :avatarImage="avatarImage" 
      :agentName="agentName" 
      :isThinking="isThinking" 
    />
  </div>
</template>

<script>
/**
 * مكون غلاف أفتار الذكاء الاصطناعي
 * 
 * يقوم هذا المكون بتغليف مكون الأفتار الأساسي مع إضافة وظيفة جلب صورة الأفتار من الخدمة
 */
import AIAvatar from './AIAvatar.vue';
import { getAgentAvatar } from '../../services/aiService';

export default {
  name: 'AIAvatarWrapper',
  
  components: {
    AIAvatar
  },
  
  props: {
    /**
     * معرف الوكيل الذكي
     */
    agentId: {
      type: String,
      default: 'default'
    },
    
    /**
     * اسم الوكيل الذكي
     */
    agentName: {
      type: String,
      default: 'الوكيل الذكي'
    },
    
    /**
     * حالة التفكير للوكيل
     */
    isThinking: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      avatarImage: null,
      isLoading: true,
      hasError: false
    };
  },
  
  created() {
    this.loadAvatar();
  },
  
  watch: {
    // إعادة تحميل الأفتار عند تغيير معرف الوكيل
    agentId() {
      this.loadAvatar();
    }
  },
  
  methods: {
    /**
     * تحميل صورة الأفتار من الخدمة
     */
    async loadAvatar() {
      try {
        this.isLoading = true;
        this.hasError = false;
        
        // استخدام خدمة الذكاء الاصطناعي لجلب صورة الأفتار
        this.avatarImage = await getAgentAvatar(this.agentId);
      } catch (error) {
        console.error('خطأ في تحميل صورة الأفتار:', error);
        this.hasError = true;
        
        // استخدام صورة افتراضية في حالة الخطأ
        this.avatarImage = '/assets/images/default_ai_avatar.png';
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.ai-avatar-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
