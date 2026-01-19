<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/setup/SetupWizard.vue -->
<template>
  <div class="setup-wizard">
    <div class="wizard-header">
      <h1>{{ $t('setup.title') }}</h1>
      <p>{{ $t('setup.description') }}</p>
    </div>

    <div class="wizard-steps">
      <div
        v-for="(step, index) in setupSteps"
        :key="index"
        :class="['step', { active: currentStep === index, completed: currentStep > index }]"
        @click="goToStep(index)"
      >
        <div class="step-number">{{ index + 1 }}</div>
        <div class="step-title">{{ step.title }}</div>
      </div>
    </div>

    <div class="wizard-content">
      <component
        :is="currentComponent"
        @next="nextStep"
        @back="previousStep"
        @complete="completeSetup"
      />
    </div>

    <div class="wizard-navigation">
      <button
        v-if="currentStep > 0"
        class="btn btn-secondary"
        @click="previousStep"
      >
        {{ $t('common.back') }}
      </button>
      <button
        v-if="currentStep < setupSteps.length - 1"
        class="btn btn-primary"
        @click="nextStep"
      >
        {{ $t('common.next') }}
      </button>
      <button
        v-if="currentStep === setupSteps.length - 1"
        class="btn btn-success"
        @click="completeSetup"
      >
        {{ $t('common.complete') }}
      </button>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'SetupWizard',
  
  setup() {
    const router = useRouter()
    const store = useStore()
    const currentStep = ref(0)
    
    const setupSteps = [
      {
        title: 'Welcome',
        component: 'WelcomeStep'
      },
      {
        title: 'Company Information',
        component: 'CompanyStep'
      },
      {
        title: 'User Setup',
        component: 'UserStep'
      },
      {
        title: 'System Configuration',
        component: 'SystemStep'
      },
      {
        title: 'Review',
        component: 'ReviewStep'
      }
    ]

    const currentComponent = computed(() => {
      return setupSteps[currentStep.value].component
    })

    const nextStep = () => {
      if (currentStep.value < setupSteps.length - 1) {
        currentStep.value++
      }
    }

    const previousStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
      }
    }

    const goToStep = (index) => {
      if (index <= currentStep.value) {
        currentStep.value = index
      }
    }

    const completeSetup = async () => {
      try {
        await store.dispatch('setup/completeSetup')
        ElMessage.success('Setup completed successfully')
        router.push('/dashboard')
      } catch (error) {
        console.error('Setup completion failed:', error)
        ElMessage.error(error.message || 'Failed to complete setup. Please try again.')
      }
    }

    return {
      currentStep,
      setupSteps,
      currentComponent,
      nextStep,
      previousStep,
      goToStep,
      completeSetup
    }
  }
}
</script>

<style scoped>
.setup-wizard {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.wizard-header {
  text-align: center;
  margin-bottom: 30px;
}

.wizard-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.3s;
}

.step.active {
  opacity: 1;
}

.step.completed {
  opacity: 0.8;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 5px;
}

.step.active .step-number {
  background-color: #007bff;
  color: white;
}

.step.completed .step-number {
  background-color: #28a745;
  color: white;
}

.wizard-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.wizard-navigation {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-success {
  background-color: #28a745;
  color: white;
}
</style>
