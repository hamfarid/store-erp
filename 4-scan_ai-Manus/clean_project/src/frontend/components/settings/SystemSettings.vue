<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/SystemSettings.vue -->
<template>
  <div class="system-settings">
    <div class="page-header">
      <h1>{{ $t("settings.system.title") }}</h1>
    </div>

    <div class="settings-sections">
      <!-- General Settings -->
      <div class="card">
        <h2>{{ $t("settings.system.general") }}</h2>
        <form @submit.prevent="saveGeneralSettings">
          <div class="form-group">
            <label for="default-language">{{ $t("settings.system.defaultLanguage") }}</label>
            <select id="default-language" v-model="generalSettings.default_language">
              <option value="">{{ $t("settings.system.selectLanguage") }}</option>
              <option v-for="lang in availableLanguages" :key="lang.code" :value="lang.code">
                {{ lang.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="default-currency">{{ $t("settings.system.defaultCurrency") }}</label>
            <select id="default-currency" v-model="generalSettings.default_currency">
              <option value="">{{ $t("settings.system.selectCurrency") }}</option>
              <option v-for="currency in availableCurrencies" :key="currency.code" :value="currency.code">
                {{ currency.name }} ({{ currency.code }})
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="timezone">{{ $t("settings.system.timezone") }}</label>
            <select id="timezone" v-model="generalSettings.timezone">
              <option value="">{{ $t("settings.system.selectTimezone") }}</option>
              <option v-for="tz in availableTimezones" :key="tz" :value="tz">
                {{ tz }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="date-format">{{ $t("settings.system.dateFormat") }}</label>
            <select id="date-format" v-model="generalSettings.date_format">
              <option value="YYYY-MM-DD">YYYY-MM-DD</option>
              <option value="DD/MM/YYYY">DD/MM/YYYY</option>
              <option value="MM/DD/YYYY">MM/DD/YYYY</option>
              <option value="DD.MM.YYYY">DD.MM.YYYY</option>
            </select>
          </div>

          <div class="form-group">
            <label for="time-format">{{ $t("settings.system.timeFormat") }}</label>
            <select id="time-format" v-model="generalSettings.time_format">
              <option value="HH:mm:ss">24-hour (HH:mm:ss)</option>
              <option value="hh:mm:ss A">12-hour (hh:mm:ss A)</option>
            </select>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="isProcessing">
              {{ $t("common.save") }}
            </button>
          </div>
        </form>
      </div>

      <!-- Email Settings -->
      <div class="card">
        <h2>{{ $t("settings.system.email") }}</h2>
        <form @submit.prevent="saveEmailSettings">
          <div class="form-group">
            <label for="email-driver">{{ $t("settings.system.emailDriver") }}</label>
            <select id="email-driver" v-model="emailSettings.driver">
              <option value="smtp">SMTP</option>
              <option value="sendmail">Sendmail</option>
              <option value="log">Log (Testing)</option>
            </select>
          </div>

          <div v-if="emailSettings.driver === "smtp"">
            <div class="form-group">
              <label for="smtp-host">{{ $t("settings.system.smtpHost") }}</label>
              <input type="text" id="smtp-host" v-model="emailSettings.smtp_host" />
            </div>
            <div class="form-group">
              <label for="smtp-port">{{ $t("settings.system.smtpPort") }}</label>
              <input type="number" id="smtp-port" v-model.number="emailSettings.smtp_port" />
            </div>
            <div class="form-group">
              <label for="smtp-encryption">{{ $t("settings.system.smtpEncryption") }}</label>
              <select id="smtp-encryption" v-model="emailSettings.smtp_encryption">
                <option value="">None</option>
                <option value="tls">TLS</option>
                <option value="ssl">SSL</option>
              </select>
            </div>
            <div class="form-group">
              <label for="smtp-username">{{ $t("settings.system.smtpUsername") }}</label>
              <input type="text" id="smtp-username" v-model="emailSettings.smtp_username" />
            </div>
            <div class="form-group">
              <label for="smtp-password">{{ $t("settings.system.smtpPassword") }}</label>
              <input type="password" id="smtp-password" v-model="emailSettings.smtp_password" />
            </div>
          </div>

          <div class="form-group">
            <label for="from-address">{{ $t("settings.system.fromAddress") }}</label>
            <input type="email" id="from-address" v-model="emailSettings.from_address" />
          </div>
          <div class="form-group">
            <label for="from-name">{{ $t("settings.system.fromName") }}</label>
            <input type="text" id="from-name" v-model="emailSettings.from_name" />
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="testEmailSettings" :disabled="isProcessing">
              {{ $t("settings.system.testEmail") }}
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isProcessing">
              {{ $t("common.save") }}
            </button>
          </div>
        </form>
      </div>

      <!-- Security Settings -->
      <div class="card">
        <h2>{{ $t("settings.system.security") }}</h2>
        <form @submit.prevent="saveSecuritySettings">
          <div class="form-group">
            <label for="password-policy">{{ $t("settings.system.passwordPolicy") }}</label>
            <select id="password-policy" v-model="securitySettings.password_policy">
              <option value="simple">{{ $t("settings.system.policySimple") }}</option>
              <option value="medium">{{ $t("settings.system.policyMedium") }}</option>
              <option value="strong">{{ $t("settings.system.policyStrong") }}</option>
            </select>
            <div class="form-hint">{{ getPasswordPolicyHint(securitySettings.password_policy) }}</div>
          </div>

          <div class="form-group">
            <label for="session-timeout">{{ $t("settings.system.sessionTimeout") }}</label>
            <input 
              type="number" 
              id="session-timeout" 
              v-model.number="securitySettings.session_timeout" 
              min="5"
            />
            <div class="form-hint">{{ $t("settings.system.sessionTimeoutHint") }}</div>
          </div>

          <div class="form-group">
            <div class="checkbox-option">
              <input type="checkbox" id="two-factor-auth" v-model="securitySettings.two_factor_auth_enabled" />
              <label for="two-factor-auth">{{ $t("settings.system.enable2FA") }}</label>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="isProcessing">
              {{ $t("common.save") }}
            </button>
          </div>
        </form>
      </div>

      <!-- AI Settings -->
      <div class="card">
        <h2>{{ $t("settings.system.ai") }}</h2>
        <form @submit.prevent="saveAiSettings">
          <div class="form-group">
            <label for="default-ai-model">{{ $t("settings.system.defaultAiModel") }}</label>
            <select id="default-ai-model" v-model="aiSettings.default_model">
              <option value="">{{ $t("settings.system.selectModel") }}</option>
              <option v-for="model in availableAiModels" :key="model.id" :value="model.id">
                {{ model.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="ai-api-key">{{ $t("settings.system.aiApiKey") }}</label>
            <input type="password" id="ai-api-key" v-model="aiSettings.api_key" />
            <div class="form-hint">{{ $t("settings.system.apiKeyHint") }}</div>
          </div>

          <div class="form-group">
            <div class="checkbox-option">
              <input type="checkbox" id="enable-ai-logging" v-model="aiSettings.enable_logging" />
              <label for="enable-ai-logging">{{ $t("settings.system.enableAiLogging") }}</label>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="isProcessing">
              {{ $t("common.save") }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Processing Modal -->
    <div class="modal" v-if="isProcessing">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ processingTitle }}</h2>
        </div>
        <div class="modal-body">
          <div class="loading-spinner"></div>
          <p>{{ processingMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useToast } from "@/composables/useToast";
import settingsService from "@/services/settingsService";

export default {
  name: "SystemSettings",
  setup() {
    const { t } = useI18n();
    const { showToast } = useToast();

    // Data
    const generalSettings = reactive({
      default_language: "",
      default_currency: "",
      timezone: "",
      date_format: "",
      time_format: "",
    });
    const emailSettings = reactive({
      driver: "smtp",
      smtp_host: "",
      smtp_port: 587,
      smtp_encryption: "tls",
      smtp_username: "",
      smtp_password: "",
      from_address: "",
      from_name: "",
    });
    const securitySettings = reactive({
      password_policy: "medium",
      session_timeout: 30,
      two_factor_auth_enabled: false,
    });
    const aiSettings = reactive({
      default_model: "",
      api_key: "",
      enable_logging: true,
    });

    const availableLanguages = ref([]);
    const availableCurrencies = ref([]);
    const availableTimezones = ref([]);
    const availableAiModels = ref([]);

    // Modal states
    const isProcessing = ref(false);
    const processingTitle = ref("");
    const processingMessage = ref("");

    // Fetch data
    const fetchSettings = async () => {
      isProcessing.value = true;
      processingTitle.value = t("settings.system.loadingSettings");
      processingMessage.value = t("settings.system.loadingSettingsMessage");
      try {
        const [generalRes, emailRes, securityRes, aiRes, langRes, currRes, tzRes, modelRes] = await Promise.all([
          settingsService.getGeneralSettings(),
          settingsService.getEmailSettings(),
          settingsService.getSecuritySettings(),
          settingsService.getAiSettings(),
          settingsService.getLanguages(),
          settingsService.getCurrencies(),
          settingsService.getTimezones(),
          settingsService.getAiModels(),
        ]);

        Object.assign(generalSettings, generalRes.data);
        Object.assign(emailSettings, emailRes.data);
        Object.assign(securitySettings, securityRes.data);
        Object.assign(aiSettings, aiRes.data);
        availableLanguages.value = langRes.data;
        availableCurrencies.value = currRes.data;
        availableTimezones.value = tzRes.data;
        availableAiModels.value = modelRes.data;

      } catch (error) {
        showToast(t("settings.system.errorFetchingSettings"), "error");
        console.error("Error fetching settings:", error);
      } finally {
        isProcessing.value = false;
      }
    };

    // Save actions
    const saveGeneralSettings = async () => {
      isProcessing.value = true;
      processingTitle.value = t("settings.system.savingSettings");
      processingMessage.value = t("settings.system.savingSettingsMessage");
      try {
        await settingsService.updateGeneralSettings(generalSettings);
        showToast(t("settings.system.generalSettingsSaved"), "success");
      } catch (error) {
        showToast(t("settings.system.errorSavingSettings"), "error");
        console.error("Error saving general settings:", error);
      } finally {
        isProcessing.value = false;
      }
    };

    const saveEmailSettings = async () => {
      isProcessing.value = true;
      processingTitle.value = t("settings.system.savingSettings");
      processingMessage.value = t("settings.system.savingSettingsMessage");
      try {
        await settingsService.updateEmailSettings(emailSettings);
        showToast(t("settings.system.emailSettingsSaved"), "success");
      } catch (error) {
        showToast(t("settings.system.errorSavingSettings"), "error");
        console.error("Error saving email settings:", error);
      } finally {
        isProcessing.value = false;
      }
    };

    const saveSecuritySettings = async () => {
      isProcessing.value = true;
      processingTitle.value = t("settings.system.savingSettings");
      processingMessage.value = t("settings.system.savingSettingsMessage");
      try {
        await settingsService.updateSecuritySettings(securitySettings);
        showToast(t("settings.system.securitySettingsSaved"), "success");
      } catch (error) {
        showToast(t("settings.system.errorSavingSettings"), "error");
        console.error("Error saving security settings:", error);
      } finally {
        isProcessing.value = false;
      }
    };

    const saveAiSettings = async () => {
      isProcessing.value = true;
      processingTitle.value = t("settings.system.savingSettings");
      processingMessage.value = t("settings.system.savingSettingsMessage");
      try {
        await settingsService.updateAiSettings(aiSettings);
        showToast(t("settings.system.aiSettingsSaved"), "success");
      } catch (error) {
        showToast(t("settings.system.errorSavingSettings"), "error");
        console.error("Error saving AI settings:", error);
      } finally {
        isProcessing.value = false;
      }
    };

    // Test email
    const testEmailSettings = async () => {
      isProcessing.value = true;
      processingTitle.value = t("settings.system.testingEmail");
      processingMessage.value = t("settings.system.testingEmailMessage");
      try {
        await settingsService.testEmailSettings(emailSettings);
        showToast(t("settings.system.testEmailSuccess"), "success");
      } catch (error) {
        showToast(t("settings.system.testEmailError"), "error");
        console.error("Error testing email settings:", error);
      } finally {
        isProcessing.value = false;
      }
    };

    // Utility functions
    const getPasswordPolicyHint = (policy) => {
      switch (policy) {
        case "simple":
          return t("settings.system.policySimpleHint");
        case "medium":
          return t("settings.system.policyMediumHint");
        case "strong":
          return t("settings.system.policyStrongHint");
        default:
          return "";
      }
    };

    // Lifecycle hooks
    onMounted(async () => {
      await fetchSettings();
    });

    return {
      generalSettings,
      emailSettings,
      securitySettings,
      aiSettings,
      availableLanguages,
      availableCurrencies,
      availableTimezones,
      availableAiModels,
      isProcessing,
      processingTitle,
      processingMessage,
      saveGeneralSettings,
      saveEmailSettings,
      saveSecuritySettings,
      saveAiSettings,
      testEmailSettings,
      getPasswordPolicyHint,
    };
  },
};
</script>

<style scoped>
.system-settings {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.settings-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.card {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-hint {
  font-size: 0.85em;
  color: #6c757d;
  margin-top: 5px;
}

.checkbox-option {
  display: flex;
  align-items: center;
}

.checkbox-option input {
  width: auto;
  margin-left: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn {
  cursor: pointer;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ddd;
}

.modal-body {
  padding: 20px;
  text-align: center;
}

/* Loading spinner */
.loading-spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-radius: 50%;
  border-top: 5px solid #007bff;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* RTL support */
html[dir="rtl"] .checkbox-option input {
  margin-left: 0;
  margin-right: 8px;
}
</style>
