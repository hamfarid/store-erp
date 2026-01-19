<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/common/EntitySelector.vue
الوصف: مكون اختيار الكيانات (قاعدة البيانات، الشركة، الدولة)
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="entity-selector-container" :class="{ 'rtl-support': isRtl }">
    <div class="entity-selector-header">
      <div class="logo-container">
        <img :src="brandLogo" alt="شعار الشركة" class="brand-logo" />
      </div>
      <h1>{{ $t('entitySelector.title') }}</h1>
      <p>{{ $t('entitySelector.subtitle') }}</p>
    </div>

    <div class="entity-selector-content">
      <div class="selection-steps">
        <div 
          v-for="(step, index) in steps" 
          :key="step.id" 
          :class="['step-item', { active: currentStepIndex === index, completed: index < currentStepIndex }]"
        >
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-name">{{ $t(step.name) }}</div>
        </div>
      </div>

      <div class="selection-panel">
        <!-- قاعدة البيانات -->
        <div v-if="currentStep.id === 'database'" class="selection-section">
          <h2>{{ $t('entitySelector.selectDatabase') }}</h2>
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery" 
              :placeholder="$t('entitySelector.searchDatabases')" 
            />
            <i class="fas fa-search"></i>
          </div>
          <div class="entity-list">
            <div 
              v-for="db in filteredDatabases" 
              :key="db.id" 
              :class="['entity-item', { selected: selectedDatabase === db.id }]"
              @click="selectDatabase(db.id)"
            >
              <div class="entity-icon">
                <i class="fas fa-database"></i>
              </div>
              <div class="entity-details">
                <div class="entity-name">{{ db.name }}</div>
                <div class="entity-description">{{ db.description }}</div>
              </div>
              <div class="entity-status" v-if="db.status">
                <span :class="['status-badge', `status-${db.status}`]">
                  {{ getStatusText(db.status) }}
                </span>
              </div>
            </div>
            <div v-if="filteredDatabases.length === 0" class="no-results">
              {{ $t('entitySelector.noDatabasesFound') }}
            </div>
          </div>
        </div>

        <!-- الشركة -->
        <div v-if="currentStep.id === 'company'" class="selection-section">
          <h2>{{ $t('entitySelector.selectCompany') }}</h2>
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery" 
              :placeholder="$t('entitySelector.searchCompanies')" 
            />
            <i class="fas fa-search"></i>
          </div>
          <div class="entity-list">
            <div 
              v-for="company in filteredCompanies" 
              :key="company.id" 
              :class="['entity-item', { selected: selectedCompany === company.id }]"
              @click="selectCompany(company.id)"
            >
              <div class="entity-icon">
                <img v-if="company.logo" :src="company.logo" :alt="company.name" class="company-logo" />
                <i v-else class="fas fa-building"></i>
              </div>
              <div class="entity-details">
                <div class="entity-name">{{ company.name }}</div>
                <div class="entity-description">{{ company.description }}</div>
              </div>
            </div>
            <div v-if="filteredCompanies.length === 0" class="no-results">
              {{ $t('entitySelector.noCompaniesFound') }}
            </div>
          </div>
        </div>

        <!-- الدولة -->
        <div v-if="currentStep.id === 'country'" class="selection-section">
          <h2>{{ $t('entitySelector.selectCountry') }}</h2>
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery" 
              :placeholder="$t('entitySelector.searchCountries')" 
            />
            <i class="fas fa-search"></i>
          </div>
          <div class="entity-list">
            <div 
              v-for="country in filteredCountries" 
              :key="country.code" 
              :class="['entity-item', { selected: selectedCountry === country.code }]"
              @click="selectCountry(country.code)"
            >
              <div class="entity-icon">
                <img v-if="country.flag" :src="country.flag" :alt="country.name" class="country-flag" />
                <i v-else class="fas fa-flag"></i>
              </div>
              <div class="entity-details">
                <div class="entity-name">{{ country.name }}</div>
                <div class="entity-description">{{ country.localName }}</div>
              </div>
            </div>
            <div v-if="filteredCountries.length === 0" class="no-results">
              {{ $t('entitySelector.noCountriesFound') }}
            </div>
          </div>
        </div>

        <!-- الملخص -->
        <div v-if="currentStep.id === 'summary'" class="selection-section">
          <h2>{{ $t('entitySelector.summary') }}</h2>
          <div class="summary-content">
            <div class="summary-item">
              <div class="summary-label">{{ $t('entitySelector.selectedDatabase') }}</div>
              <div class="summary-value">{{ getSelectedDatabaseName() }}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">{{ $t('entitySelector.selectedCompany') }}</div>
              <div class="summary-value">{{ getSelectedCompanyName() }}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">{{ $t('entitySelector.selectedCountry') }}</div>
              <div class="summary-value">{{ getSelectedCountryName() }}</div>
            </div>
            <div class="summary-options">
              <div class="checkbox-option">
                <input type="checkbox" id="remember-selection" v-model="rememberSelection" />
                <label for="remember-selection">{{ $t('entitySelector.rememberSelection') }}</label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="selection-actions">
        <button 
          class="btn btn-secondary" 
          @click="previousStep" 
          :disabled="currentStepIndex === 0 || isProcessing"
        >
          {{ $t("common.previous") }}
        </button>
        <button 
          class="btn btn-primary" 
          @click="nextStep" 
          :disabled="!isCurrentStepValid || isProcessing"
        >
          {{ isLastStep ? $t("entitySelector.confirm") : $t("common.next") }}
        </button>
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
import { useToast } from "@/composables/useToast";
import entityService from "@/services/entityService";
import { computed, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";

// تعريف الخطوات
const selectionSteps = [
  { id: "database", name: "entitySelector.steps.database" },
  { id: "company", name: "entitySelector.steps.company" },
  { id: "country", name: "entitySelector.steps.country" },
  { id: "summary", name: "entitySelector.steps.summary" },
];

export default {
  name: "EntitySelector",
  props: {
    redirectTo: {
      type: String,
      default: "/dashboard"
    }
  },
  setup(props) {
    const { t, locale } = useI18n();
    const router = useRouter();
    const { showToast } = useToast();

    // الحالة
    const steps = ref(selectionSteps);
    const currentStepIndex = ref(0);
    const searchQuery = ref("");
    const isProcessing = ref(false);
    const processingTitle = ref("");
    const processingMessage = ref("");
    const rememberSelection = ref(true);

    // البيانات المحددة
    const selectedDatabase = ref(null);
    const selectedCompany = ref(null);
    const selectedCountry = ref(null);

    // قوائم البيانات
    const databases = ref([]);
    const companies = ref([]);
    const countries = ref([]);

    // الخصائص المحسوبة
    const currentStep = computed(() => steps.value[currentStepIndex.value]);
    const isLastStep = computed(() => currentStepIndex.value === steps.value.length - 1);
    const isRtl = computed(() => locale.value === 'ar');

    const isCurrentStepValid = computed(() => {
      switch (currentStep.value.id) {
        case "database":
          return !!selectedDatabase.value;
        case "company":
          return !!selectedCompany.value;
        case "country":
          return !!selectedCountry.value;
        case "summary":
          return true;
        default:
          return false;
      }
    });

    // القوائم المفلترة
    const filteredDatabases = computed(() => {
      if (!searchQuery.value) return databases.value;
      const query = searchQuery.value.toLowerCase();
      return databases.value.filter(db => 
        db.name.toLowerCase().includes(query) || 
        (db.description && db.description.toLowerCase().includes(query))
      );
    });

    const filteredCompanies = computed(() => {
      if (!searchQuery.value) return companies.value;
      const query = searchQuery.value.toLowerCase();
      return companies.value.filter(company => 
        company.name.toLowerCase().includes(query) || 
        (company.description && company.description.toLowerCase().includes(query))
      );
    });

    const filteredCountries = computed(() => {
      if (!searchQuery.value) return countries.value;
      const query = searchQuery.value.toLowerCase();
      return countries.value.filter(country => 
        country.name.toLowerCase().includes(query) || 
        (country.localName && country.localName.toLowerCase().includes(query))
      );
    });

    // جلب البيانات
    const fetchData = async () => {
      isProcessing.value = true;
      processingTitle.value = t("entitySelector.loadingData");
      processingMessage.value = t("entitySelector.loadingDataMessage");
      
      try {
        // جلب قواعد البيانات
        const dbResponse = await entityService.getDatabases();
        databases.value = dbResponse.data;
        
        // استعادة الاختيارات المحفوظة
        const savedSelections = localStorage.getItem('entitySelections');
        if (savedSelections) {
          const selections = JSON.parse(savedSelections);
          selectedDatabase.value = selections.database;
          selectedCompany.value = selections.company;
          selectedCountry.value = selections.country;
          
          // التحقق من صلاحية الاختيارات المحفوظة
          const dbExists = databases.value.some(db => db.id === selectedDatabase.value);
          if (!dbExists) {
            selectedDatabase.value = null;
          }
        }
      } catch (error) {
        console.error("Error fetching databases:", error);
        showToast(t("entitySelector.errorLoadingDatabases"), "error");
      } finally {
        isProcessing.value = false;
      }
    };

    // جلب الشركات بناءً على قاعدة البيانات المحددة
    const fetchCompanies = async () => {
      if (!selectedDatabase.value) return;
      
      isProcessing.value = true;
      processingTitle.value = t("entitySelector.loadingCompanies");
      processingMessage.value = t("entitySelector.loadingCompaniesMessage");
      
      try {
        const companyResponse = await entityService.getCompanies(selectedDatabase.value);
        companies.value = companyResponse.data;
        
        // التحقق من صلاحية الشركة المحددة
        if (selectedCompany.value) {
          const companyExists = companies.value.some(company => company.id === selectedCompany.value);
          if (!companyExists) {
            selectedCompany.value = null;
          }
        }
      } catch (error) {
        console.error("Error fetching companies:", error);
        showToast(t("entitySelector.errorLoadingCompanies"), "error");
      } finally {
        isProcessing.value = false;
      }
    };

    // جلب الدول بناءً على الشركة المحددة
    const fetchCountries = async () => {
      if (!selectedCompany.value) return;
      
      isProcessing.value = true;
      processingTitle.value = t("entitySelector.loadingCountries");
      processingMessage.value = t("entitySelector.loadingCountriesMessage");
      
      try {
        const countryResponse = await entityService.getCountries(selectedDatabase.value, selectedCompany.value);
        countries.value = countryResponse.data;
        
        // التحقق من صلاحية الدولة المحددة
        if (selectedCountry.value) {
          const countryExists = countries.value.some(country => country.code === selectedCountry.value);
          if (!countryExists) {
            selectedCountry.value = null;
          }
        }
      } catch (error) {
        console.error("Error fetching countries:", error);
        showToast(t("entitySelector.errorLoadingCountries"), "error");
      } finally {
        isProcessing.value = false;
      }
    };

    // الانتقال للخطوة التالية
    const nextStep = async () => {
      if (!isCurrentStepValid.value) {
        showToast(t("entitySelector.pleaseSelectOption"), "warning");
        return;
      }

      if (isLastStep.value) {
        // تأكيد الاختيارات وحفظها
        await confirmSelections();
      } else {
        // الانتقال للخطوة التالية
        searchQuery.value = ""; // إعادة تعيين البحث
        currentStepIndex.value++;
        
        // جلب البيانات للخطوة التالية
        if (currentStep.value.id === "company") {
          await fetchCompanies();
        } else if (currentStep.value.id === "country") {
          await fetchCountries();
        }
      }
    };

    // الانتقال للخطوة السابقة
    const previousStep = () => {
      if (currentStepIndex.value > 0) {
        searchQuery.value = ""; // إعادة تعيين البحث
        currentStepIndex.value--;
      }
    };

    // تأكيد الاختيارات وحفظها
    const confirmSelections = async () => {
      isProcessing.value = true;
      processingTitle.value = t("entitySelector.savingSelections");
      processingMessage.value = t("entitySelector.savingSelectionsMessage");
      
      try {
        // حفظ الاختيارات في الخدمة الخلفية
        await entityService.saveSelections({
          database: selectedDatabase.value,
          company: selectedCompany.value,
          country: selectedCountry.value
        });
        
        // حفظ الاختيارات محلياً إذا تم تحديد خيار التذكر
        if (rememberSelection.value) {
          localStorage.setItem('entitySelections', JSON.stringify({
            database: selectedDatabase.value,
            company: selectedCompany.value,
            country: selectedCountry.value
          }));
        }
        
        showToast(t("entitySelector.selectionsConfirmed"), "success");
        
        // الانتقال إلى الصفحة المحددة
        router.push(props.redirectTo);
      } catch (error) {
        console.error("Error saving selections:", error);
        showToast(t("entitySelector.errorSavingSelections"), "error");
      } finally {
        isProcessing.value = false;
      }
    };

    // اختيار قاعدة البيانات
    const selectDatabase = (dbId) => {
      selectedDatabase.value = dbId;
      selectedCompany.value = null; // إعادة تعيين الشركة المحددة
      selectedCountry.value = null; // إعادة تعيين الدولة المحددة
    };

    // اختيار الشركة
    const selectCompany = (companyId) => {
      selectedCompany.value = companyId;
      selectedCountry.value = null; // إعادة تعيين الدولة المحددة
    };

    // اختيار الدولة
    const selectCountry = (countryCode) => {
      selectedCountry.value = countryCode;
    };

    // الحصول على اسم قاعدة البيانات المحددة
    const getSelectedDatabaseName = () => {
      if (!selectedDatabase.value) return t("entitySelector.notSelected");
      const db = databases.value.find(db => db.id === selectedDatabase.value);
      return db ? db.name : t("entitySelector.notSelected");
    };

    // الحصول على اسم الشركة المحددة
    const getSelectedCompanyName = () => {
      if (!selectedCompany.value) return t("entitySelector.notSelected");
      const company = companies.value.find(company => company.id === selectedCompany.value);
      return company ? company.name : t("entitySelector.notSelected");
    };

    // الحصول على اسم الدولة المحددة
    const getSelectedCountryName = () => {
      if (!selectedCountry.value) return t("entitySelector.notSelected");
      const country = countries.value.find(country => country.code === selectedCountry.value);
      return country ? country.name : t("entitySelector.notSelected");
    };

    // الحصول على نص الحالة
    const getStatusText = (status) => {
      switch (status) {
        case "active":
          return t("common.active");
        case "maintenance":
          return t("common.maintenance");
        case "offline":
          return t("common.offline");
        default:
          return status;
      }
    };

    // مراقبة تغيير الخطوة لإعادة تعيين البحث
    watch(currentStepIndex, () => {
      searchQuery.value = "";
    });

    // دورة الحياة
    onMounted(async () => {
      await fetchData();
    });

    return {
      steps,
      currentStepIndex,
      currentStep,
      isLastStep,
      isCurrentStepValid,
      searchQuery,
      selectedDatabase,
      selectedCompany,
      selectedCountry,
      filteredDatabases,
      filteredCompanies,
      filteredCountries,
      isProcessing,
      processingTitle,
      processingMessage,
      rememberSelection,
      isRtl,
      brandLogo,
      nextStep,
      previousStep,
      selectDatabase,
      selectCompany,
      selectCountry,
      getSelectedDatabaseName,
      getSelectedCompanyName,
      getSelectedCountryName,
      getStatusText
    };
  }
};
</script>

<style scoped>
.entity-selector-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  direction: ltr;
}

.entity-selector-container.rtl-support {
  direction: rtl;
}

.entity-selector-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo-container {
  margin-bottom: 20px;
}

.brand-logo {
  max-height: 80px;
  max-width: 200px;
}

.entity-selector-header h1 {
  margin-bottom: 10px;
  color: var(--primary-color, #007bff);
}

.selection-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
  overflow-x: auto;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: #aaa;
  flex: 1;
  min-width: 100px;
  padding: 0 10px;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #eee;
  color: #aaa;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  margin-bottom: 8px;
  transition: background-color 0.3s, color 0.3s;
}

.step-name {
  font-size: 0.9em;
  font-weight: 500;
  transition: color 0.3s;
}

.step-item.active .step-number {
  background-color: var(--primary-color, #007bff);
  color: white;
}

.step-item.active .step-name {
  color: var(--primary-color, #007bff);
}

.step-item.completed .step-number {
  background-color: var(--success-color, #28a745);
  color: white;
}

.step-item.completed .step-name {
  color: #555;
}

.selection-panel {
  min-height: 300px;
  margin-bottom: 30px;
}

.selection-section h2 {
  margin-bottom: 20px;
  color: var(--primary-color, #007bff);
}

.search-box {
  position: relative;
  margin-bottom: 20px;
}

.search-box input {
  width: 100%;
  padding: 10px 40px 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
}

.rtl-support .search-box input {
  padding: 10px 15px 10px 40px;
}

.search-box i {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #aaa;
}

.rtl-support .search-box i {
  right: auto;
  left: 15px;
}

.entity-list {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 4px;
}

.entity-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.entity-item:last-child {
  border-bottom: none;
}

.entity-item:hover {
  background-color: #f9f9f9;
}

.entity-item.selected {
  background-color: rgba(0, 123, 255, 0.1);
  border-left: 4px solid var(--primary-color, #007bff);
}

.rtl-support .entity-item.selected {
  border-left: none;
  border-right: 4px solid var(--primary-color, #007bff);
}

.entity-icon {
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
  border-radius: 4px;
  background-color: #f5f5f5;
  overflow: hidden;
}

.rtl-support .entity-icon {
  margin-right: 0;
  margin-left: 15px;
}

.entity-icon i {
  font-size: 24px;
  color: var(--primary-color, #007bff);
}

.company-logo, .country-flag {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.entity-details {
  flex: 1;
}

.entity-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.entity-description {
  font-size: 0.9em;
  color: #666;
}

.entity-status {
  margin-left: 15px;
}

.rtl-support .entity-status {
  margin-left: 0;
  margin-right: 15px;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  font-weight: 500;
}

.status-active {
  background-color: rgba(40, 167, 69, 0.2);
  color: #28a745;
}

.status-maintenance {
  background-color: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.status-offline {
  background-color: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

.no-results {
  padding: 20px;
  text-align: center;
  color: #666;
}

.summary-content {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.summary-item {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #555;
}

.summary-value {
  font-size: 1.1em;
}

.summary-options {
  margin-top: 20px;
}

.checkbox-option {
  display: flex;
  align-items: center;
}

.checkbox-option input {
  margin-right: 10px;
}

.rtl-support .checkbox-option input {
  margin-right: 0;
  margin-left: 10px;
}

.selection-actions {
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.rtl-support .selection-actions {
  flex-direction: row-reverse;
}

.btn {
  cursor: pointer;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: var(--primary-color, #007bff);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-dark-color, #0069d9);
}

.btn-secondary {
  background-color: var(--secondary-color, #6c757d);
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--secondary-dark-color, #5a6268);
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
  border-top: 5px solid var(--primary-color, #007bff);
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .entity-selector-container {
    margin: 20px auto;
    padding: 20px;
  }
  
  .selection-steps {
    overflow-x: auto;
    padding-bottom: 15px;
    margin-bottom: 20px;
  }
  
  .step-item {
    min-width: 80px;
  }
  
  .entity-item {
    padding: 10px;
  }
  
  .entity-icon {
    width: 40px;
    height: 40px;
    margin-right: 10px;
  }
  
  .rtl-support .entity-icon {
    margin-right: 0;
    margin-left: 10px;
  }
  
  .entity-name {
    font-size: 0.9em;
  }
  
  .entity-description {
    font-size: 0.8em;
  }
}
</style>
