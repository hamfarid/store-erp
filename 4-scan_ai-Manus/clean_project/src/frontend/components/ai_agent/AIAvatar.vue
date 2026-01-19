// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/ai_agent/AIAvatar.vue
<template>
  <div class="ai-avatar-container" :class="{ 'thinking': isThinking }">
    <div class="avatar-image-container">
      <img 
        v-if="avatarImage" 
        :src="avatarImage" 
        alt="صورة الوكيل الذكي" 
        class="avatar-image"
      />
      <div v-else class="avatar-placeholder">
        <v-icon size="64" color="primary">mdi-robot</v-icon>
      </div>
    </div>
    <div class="avatar-animation" v-if="isThinking">
      <div class="thinking-dot"></div>
      <div class="thinking-dot"></div>
      <div class="thinking-dot"></div>
    </div>
    <div class="avatar-name">{{ agentName }}</div>
  </div>
</template>

<script>
/**
 * مكون أفتار الذكاء الاصطناعي
 * 
 * يعرض هذا المكون صورة متحركة للوكيل الذكي مع حالة التفكير
 * ويمكن تخصيصه باستخدام صورة مخصصة أو استخدام الأيقونة الافتراضية
 */
export default {
  name: 'AIAvatar',
  
  props: {
    /**
     * مسار صورة الأفتار (اختياري)
     */
    avatarImage: {
      type: String,
      default: null
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
      // يمكن إضافة بيانات إضافية هنا إذا لزم الأمر
    };
  },
  
  methods: {
    /**
     * تعيين حالة التفكير للوكيل
     * @param {Boolean} status - حالة التفكير الجديدة
     */
    setThinkingStatus(status) {
      this.$emit('update:isThinking', status);
    }
  }
};
</script>

<style scoped>
.ai-avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  transition: all 0.3s ease;
}

.avatar-image-container {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--v-surface-base);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 3px solid var(--v-primary-base);
  transition: all 0.3s ease;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: var(--v-secondary-lighten1);
}

.avatar-name {
  margin-top: 0.75rem;
  font-weight: bold;
  color: var(--v-primary-darken1);
  text-align: center;
}

.avatar-animation {
  display: flex;
  justify-content: center;
  margin-top: 0.5rem;
}

.thinking-dot {
  width: 8px;
  height: 8px;
  margin: 0 4px;
  background-color: var(--v-primary-base);
  border-radius: 50%;
  animation: thinking 1.4s infinite ease-in-out both;
}

.thinking-dot:nth-child(1) {
  animation-delay: -0.32s;
}

.thinking-dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes thinking {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.ai-avatar-container.thinking .avatar-image-container {
  border-color: var(--v-accent-base);
  box-shadow: 0 0 15px var(--v-accent-lighten3);
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 600px) {
  .avatar-image-container {
    width: 80px;
    height: 80px;
  }
}
</style>
