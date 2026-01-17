# DATABASE SCHEMA DOCUMENTATION - Gaara ERP v12
**Generated**: 2025-11-18
**Database**: SQLite (development)
**Django Version**: 5.x

---

## a2a_integration

### APICredential

**Table**: `a2a_integration_apicredential`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| external_system | ForeignKey | No | - | Yes |
| auth_type | CharField | No | - | No |
| key_id | CharField | Yes | - | No |
| key_secret | CharField | Yes | - | No |
| token | TextField | Yes | - | No |
| token_expiry | DateTimeField | Yes | - | No |
| additional_data | JSONField | Yes | <class 'dict'> | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `external_system` → a2a_integration.ExternalSystem

---

### ExternalSystem

**Table**: `a2a_integration_externalsystem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| system_type | CharField | No | - | No |
| base_url | CharField | Yes | - | No |
| description | TextField | Yes | - | No |
| contact_person | CharField | Yes | - | No |
| contact_email | CharField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `integration_configs` (from a2a_integration.IntegrationConfig)
- `api_credentials` (from a2a_integration.APICredential)

---

### IntegrationConfig

**Table**: `a2a_integration_integrationconfig`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| external_system | ForeignKey | No | - | Yes |
| integration_type | CharField | No | - | No |
| direction | CharField | No | - | No |
| endpoint_url | CharField | Yes | - | No |
| data_format | CharField | No | json | No |
| headers | JSONField | Yes | <class 'dict'> | No |
| parameters | JSONField | Yes | <class 'dict'> | No |
| schedule | CharField | Yes | - | No |
| retry_count | PositiveSmallIntegerField | No | 3 | No |
| retry_delay | PositiveSmallIntegerField | No | 60 | No |
| timeout | PositiveSmallIntegerField | No | 30 | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `external_system` → a2a_integration.ExternalSystem

**Reverse Relations**:

- `logs` (from a2a_integration.IntegrationLog)

---

### IntegrationLog

**Table**: `a2a_integration_integrationlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| integration_config | ForeignKey | No | - | Yes |
| request_data | JSONField | Yes | <class 'dict'> | No |
| response_data | JSONField | Yes | <class 'dict'> | No |
| status | CharField | No | - | No |
| status_code | PositiveSmallIntegerField | Yes | - | No |
| error_message | TextField | Yes | - | No |
| execution_time | FloatField | Yes | - | No |
| retry_count | PositiveSmallIntegerField | No | 0 | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `integration_config` → a2a_integration.IntegrationConfig
- `created_by` → users.User

---

## accounting

### Account

**Table**: `accounting_account`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| balance | DecimalField | No | 0.00 | No |
| account_type | ForeignKey | Yes | - | Yes |
| parent | ForeignKey | Yes | - | Yes |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| is_reconcilable | BooleanField | No | False | No |
| opening_debit | DecimalField | No | 0.00 | No |
| opening_credit | DecimalField | No | 0.00 | No |
| current_debit | DecimalField | No | 0.00 | No |
| current_credit | DecimalField | No | 0.00 | No |
| currency | ForeignKey | Yes | - | Yes |
| branch | ForeignKey | Yes | - | Yes |
| department | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company
- `account_type` → accounting.AccountType
- `parent` → accounting.Account
- `currency` → core.Currency
- `branch` → core.Branch
- `department` → core.Department

**Reverse Relations**:

- `children` (from accounting.Account)
- `journal_lines` (from accounting.JournalEntryLine)
- `rent_asset_properties` (from rent.Property)
- `rent_income_properties` (from rent.Property)
- `rent_expense_properties` (from rent.Property)

**Indexes**:

- accounting__company_ee9541_idx: (company, account_type)
- accounting__parent__da6035_idx: (parent)
- accounting__is_acti_28dd04_idx: (is_active)

**Unique Together**:

- (company, code)

---

### AccountType

**Table**: `accounting_accounttype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| type | CharField | No | - | No |
| parent | ForeignKey | Yes | - | Yes |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company
- `parent` → accounting.AccountType

**Reverse Relations**:

- `children` (from accounting.AccountType)
- `accounts` (from accounting.Account)

**Indexes**:

- accounting__company_dc940c_idx: (company, type)
- accounting__parent__fa7f66_idx: (parent)

---

### AnalyticAccount

**Table**: `accounting_analyticaccount`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| parent | ForeignKey | Yes | - | Yes |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company
- `parent` → accounting.AnalyticAccount

**Reverse Relations**:

- `journal_lines` (from accounting.JournalEntryLine)
- `children` (from accounting.AnalyticAccount)

**Indexes**:

- accounting__parent__cbc402_idx: (parent)
- accounting__is_acti_ababfa_idx: (is_active)

**Unique Together**:

- (company, code)

---

### Currency

**Table**: `accounting_currency`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| symbol | CharField | No | - | No |
| is_base | BooleanField | No | False | No |
| exchange_rate | DecimalField | No | 1.000000 | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company

**Indexes**:

- accounting__company_9f1727_idx: (company, is_base)

**Unique Together**:

- (company, code)

---

### FiscalPeriod

**Table**: `accounting_fiscalperiod`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| fiscal_year | ForeignKey | Yes | - | Yes |
| type | CharField | No | monthly | No |
| start_date | DateField | No | - | No |
| end_date | DateField | No | - | No |
| is_closed | BooleanField | No | False | No |
| created_at | DateTimeField | Yes | - | No |
| updated_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company
- `fiscal_year` → accounting.FiscalYear

**Reverse Relations**:

- `entries` (from accounting.JournalEntry)

**Indexes**:

- accounting__fiscal__c2b37e_idx: (fiscal_year, is_closed)
- accounting__start_d_9f449b_idx: (start_date, end_date)

**Unique Together**:

- (company, fiscal_year, name)

---

### FiscalYear

**Table**: `accounting_fiscalyear`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| start_date | DateField | No | - | No |
| end_date | DateField | No | - | No |
| is_closed | BooleanField | No | False | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | Yes | - | No |
| updated_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company

**Reverse Relations**:

- `periods` (from accounting.FiscalPeriod)

**Indexes**:

- accounting__company_a30f1d_idx: (company, is_active)
- accounting__start_d_f7d96b_idx: (start_date, end_date)

**Unique Together**:

- (company, name)

---

### Journal

**Table**: `accounting_journal`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| type | CharField | No | general | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| branch | ForeignKey | Yes | - | Yes |
| department | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company
- `branch` → core.Branch
- `department` → core.Department

**Reverse Relations**:

- `entries` (from accounting.JournalEntry)
- `rentalcontract` (from rent.RentalContract)
- `pos_configs` (from pos.POSConfig)

**Indexes**:

- accounting__company_d04129_idx: (company, type)
- accounting__is_acti_52d688_idx: (is_active)

**Unique Together**:

- (company, code)

---

### JournalEntry

**Table**: `accounting_journalentry`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| company | ForeignKey | Yes | - | Yes |
| reference | CharField | No | - | No |
| date | DateField | No | <function now at 0x00000247D3A64680> | No |
| journal | ForeignKey | Yes | - | Yes |
| description | TextField | Yes | - | No |
| status | CharField | No | draft | No |
| fiscal_period | ForeignKey | Yes | - | Yes |
| total_debit | DecimalField | No | 0.00 | No |
| total_credit | DecimalField | No | 0.00 | No |
| content_type | ForeignKey | Yes | - | Yes |
| object_id | PositiveIntegerField | Yes | - | No |
| branch | ForeignKey | Yes | - | Yes |
| department | ForeignKey | Yes | - | Yes |
| posted_by | ForeignKey | Yes | - | Yes |
| posted_at | DateTimeField | Yes | - | No |
| content_object | GenericForeignKey | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company
- `journal` → accounting.Journal
- `fiscal_period` → accounting.FiscalPeriod
- `content_type` → contenttypes.ContentType
- `branch` → core.Branch
- `department` → core.Department
- `posted_by` → users.User

**Reverse Relations**:

- `lines` (from accounting.JournalEntryLine)

**Indexes**:

- accounting__company_7eceea_idx: (company, status)
- accounting__fiscal__e2381c_idx: (fiscal_period, status)
- accounting__date_e3f521_idx: (date)

**Unique Together**:

- (company, reference)

---

### JournalEntryLine

**Table**: `accounting_journalentryline`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| entry | ForeignKey | Yes | - | Yes |
| account | ForeignKey | Yes | - | Yes |
| description | CharField | Yes | - | No |
| debit | DecimalField | No | 0.00 | No |
| credit | DecimalField | No | 0.00 | No |
| partner_content_type | ForeignKey | Yes | - | Yes |
| partner_object_id | PositiveIntegerField | Yes | - | No |
| analytic_account | ForeignKey | Yes | - | Yes |
| tax | ForeignKey | Yes | - | Yes |
| tax_amount | DecimalField | No | 0.00 | No |
| partner | GenericForeignKey | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `entry` → accounting.JournalEntry
- `account` → accounting.Account
- `partner_content_type` → contenttypes.ContentType
- `analytic_account` → accounting.AnalyticAccount
- `tax` → accounting.Tax

**Indexes**:

- accounting__entry_i_ce00ce_idx: (entry, account)

---

### Settlement

**Table**: `accounting_settlement`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| status | CharField | No | draft | No |
| settlement_date | DateField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| confirmed_by | ForeignKey | Yes | - | Yes |
| cancelled_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| confirmed_at | DateTimeField | Yes | - | No |
| cancelled_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `confirmed_by` → users.User
- `cancelled_by` → users.User

**Reverse Relations**:

- `items` (from accounting.SettlementItem)

---

### SettlementItem

**Table**: `accounting_settlementitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| settlement | ForeignKey | Yes | - | Yes |
| item_type | CharField | No | - | No |
| amount | DecimalField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `settlement` → accounting.Settlement

---

### Tax

**Table**: `accounting_tax`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| type | CharField | No | percentage | No |
| rate | DecimalField | No | 0.0000 | No |
| amount | DecimalField | No | 0.00 | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company

**Reverse Relations**:

- `journal_lines` (from accounting.JournalEntryLine)
- `purchase_order_lines` (from purchasing.PurchaseOrderLine)

**Indexes**:

- accounting__company_67399f_idx: (company, is_active)

**Unique Together**:

- (company, code)

---

## admin

### LogEntry

**Table**: `django_admin_log`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| action_time | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| user | ForeignKey | No | - | Yes |
| content_type | ForeignKey | Yes | - | Yes |
| object_id | TextField | Yes | - | No |
| object_repr | CharField | No | - | No |
| action_flag | PositiveSmallIntegerField | No | - | No |
| change_message | TextField | No | - | No |

**Foreign Keys**:

- `user` → users.User
- `content_type` → contenttypes.ContentType

---

## admin_data_import_export

### ExportJob

**Table**: `admin_data_import_export_exportjob`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| model_name | CharField | No | - | No |
| file_format | CharField | No | CSV | No |
| status | CharField | No | PENDING | Yes |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| started_at | DateTimeField | Yes | - | No |
| completed_at | DateTimeField | Yes | - | No |
| exported_file | FileField | Yes | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### ImportJob

**Table**: `admin_data_import_export_importjob`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| model_name | CharField | No | - | No |
| file | FileField | No | - | No |
| status | CharField | No | PENDING | Yes |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| started_at | DateTimeField | Yes | - | No |
| completed_at | DateTimeField | Yes | - | No |
| total_rows | PositiveIntegerField | Yes | - | No |
| processed_rows | PositiveIntegerField | No | 0 | No |
| error_count | PositiveIntegerField | No | 0 | No |
| log_file | FileField | Yes | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

## admin_reports

### AIAgentUsageLog

**Table**: `admin_reports_aiagentusagelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| user | ForeignKey | Yes | - | Yes |
| agent_name | CharField | No | - | Yes |
| session_id | UUIDField | Yes | - | Yes |
| query_text | TextField | No | - | No |
| response_text | TextField | No | - | No |
| timestamp | DateTimeField | No | - | Yes |
| analysis_status | CharField | No | pending | Yes |
| is_within_scope | BooleanField | Yes | - | No |
| analysis_details | JSONField | Yes | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

**Indexes**:

- admin_repor_user_id_40daac_idx: (user, timestamp)
- admin_repor_agent_n_c7dead_idx: (agent_name, timestamp)

---

## agricultural_experiments

### AIAnalysis

**Table**: `agricultural_experiments_aianalysis`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| analysis_date | DateTimeField | No | - | No |
| analysis_type | CharField | No | - | No |
| model_name | CharField | No | - | No |
| model_version | CharField | No | - | No |
| input_parameters | JSONField | No | <class 'dict'> | No |
| results | JSONField | No | <class 'dict'> | No |
| confidence_score | FloatField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `experiment` → agricultural_experiments.Experiment
- `created_by` → users.User

**Reverse Relations**:

- `variety_analyses` (from agricultural_experiments.VarietyAIAnalysis)

---

### Experiment

**Table**: `agricultural_experiments_experiment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| code | CharField | No | - | No |
| description | TextField | No | - | No |
| location | ForeignKey | No | - | Yes |
| season | ForeignKey | No | - | Yes |
| start_date | DateField | No | - | No |
| end_date | DateField | No | - | No |
| actual_end_date | DateField | Yes | - | No |
| status | CharField | No | planned | No |
| replications | PositiveIntegerField | No | 3 | No |
| plot_size | DecimalField | No | - | No |
| plants_per_plot | PositiveIntegerField | No | - | No |
| row_spacing | DecimalField | No | - | No |
| plant_spacing | DecimalField | No | - | No |
| objectives | TextField | No | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `location` → agricultural_experiments.Location
- `season` → agricultural_experiments.Season
- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `experiment_varieties` (from agricultural_experiments.ExperimentVariety)
- `ai_analyses` (from agricultural_experiments.AIAnalysis)
- `comparison_reports` (from agricultural_experiments.VarietyComparisonReport)

---

### ExperimentVariety

**Table**: `agricultural_experiments_experimentvariety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| variety | ForeignKey | No | - | Yes |
| entry_number | PositiveIntegerField | No | - | No |
| planting_date | DateField | No | - | No |
| number_of_plants | PositiveIntegerField | Yes | - | No |
| area_planted_sqm | DecimalField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `experiment` → agricultural_experiments.Experiment
- `variety` → agricultural_experiments.Variety

**Reverse Relations**:

- `ai_analyses` (from agricultural_experiments.VarietyAIAnalysis)
- `harvests` (from agricultural_experiments.Harvest)
- `fruit_specifications` (from agricultural_experiments.FruitSpecification)
- `plant_specifications` (from agricultural_experiments.PlantSpecification)
- `comparison_report_items` (from agricultural_experiments.VarietyComparisonReportItem)

**Unique Together**:

- (experiment, variety)
- (experiment, entry_number)

---

### ExternalVariety

**Table**: `agricultural_experiments_externalvariety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| variety | ForeignKey | No | - | Yes |
| source | CharField | No | - | No |
| reference_code | CharField | Yes | - | No |
| market_price | DecimalField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `variety` → agricultural_experiments.Variety
- `created_by` → users.User

**Reverse Relations**:

- `specifications` (from agricultural_experiments.ExternalVarietySpecification)
- `yield_data` (from agricultural_experiments.ExternalVarietyYieldData)
- `comparison_report_items` (from agricultural_experiments.VarietyComparisonReportItem)

---

### ExternalVarietySpecification

**Table**: `agricultural_experiments_externalvarietyspecification`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| external_variety | ForeignKey | No | - | Yes |
| specification_date | DateField | No | - | No |
| length_cm | DecimalField | Yes | - | No |
| shape_uniformity_rating | IntegerField | Yes | - | No |
| fruit_deformity_rate | PositiveSmallIntegerField | Yes | - | No |
| firmness_rating | PositiveSmallIntegerField | Yes | - | No |
| color_description | CharField | No | - | No |
| color_rating | IntegerField | Yes | - | No |
| storage_transport_tolerance_rating | IntegerField | Yes | - | No |
| brix_value | DecimalField | Yes | - | No |
| earliness_rating | IntegerField | Yes | - | No |
| plant_vigor_rating | IntegerField | Yes | - | No |
| leaf_shape_description | CharField | No | - | No |
| fruit_coverage_rating | IntegerField | Yes | - | No |
| fungal_resistance_rating | IntegerField | Yes | - | No |
| bacterial_resistance_rating | IntegerField | Yes | - | No |
| insect_resistance_rating | IntegerField | Yes | - | No |
| viral_resistance_rating | IntegerField | Yes | - | No |
| cold_tolerance_rating | IntegerField | Yes | - | No |
| heat_tolerance_rating | IntegerField | Yes | - | No |
| soil_salinity_tolerance_rating | IntegerField | Yes | - | No |
| water_salinity_tolerance_rating | IntegerField | Yes | - | No |
| drought_tolerance_rating | IntegerField | Yes | - | No |
| notes | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `external_variety` → agricultural_experiments.ExternalVariety
- `created_by` → users.User

---

### ExternalVarietyYieldData

**Table**: `agricultural_experiments_externalvarietyyielddata`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| external_variety | ForeignKey | No | - | Yes |
| data_source | CharField | No | - | No |
| data_year | PositiveIntegerField | No | - | No |
| average_yield | DecimalField | No | - | No |
| max_yield | DecimalField | Yes | - | No |
| min_yield | DecimalField | Yes | - | No |
| notes | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `external_variety` → agricultural_experiments.ExternalVariety
- `created_by` → users.User

**Unique Together**:

- (external_variety, data_source, data_year)

---

### FruitSpecification

**Table**: `agricultural_experiments_fruitspecification`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment_variety | ForeignKey | No | - | Yes |
| evaluation_date | DateField | No | - | No |
| length_cm | DecimalField | Yes | - | No |
| shape_uniformity_rating | IntegerField | Yes | - | No |
| fruit_deformity_rate | PositiveSmallIntegerField | Yes | - | No |
| firmness_rating | PositiveSmallIntegerField | Yes | - | No |
| color_description | CharField | No | - | No |
| color_rating | IntegerField | Yes | - | No |
| storage_transport_tolerance_rating | IntegerField | Yes | - | No |
| brix_value | DecimalField | Yes | - | No |
| notes | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `experiment_variety` → agricultural_experiments.ExperimentVariety

---

### Harvest

**Table**: `agricultural_experiments_harvest`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment_variety | ForeignKey | No | - | Yes |
| harvest_number | PositiveIntegerField | No | - | No |
| harvest_date | DateField | No | - | No |
| fruit_count | PositiveIntegerField | No | - | No |
| fruit_weight | DecimalField | No | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `experiment_variety` → agricultural_experiments.ExperimentVariety
- `created_by` → users.User

**Reverse Relations**:

- `quality_grades` (from agricultural_experiments.HarvestQualityGrade)

**Unique Together**:

- (experiment_variety, harvest_number)

---

### HarvestQualityGrade

**Table**: `agricultural_experiments_harvestqualitygrade`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| harvest | ForeignKey | No | - | Yes |
| grade | CharField | No | - | No |
| fruit_count | PositiveIntegerField | No | - | No |
| fruit_weight | DecimalField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `harvest` → agricultural_experiments.Harvest

**Unique Together**:

- (harvest, grade)

---

### InventoryVarietyComparisonItem

**Table**: `agricultural_experiments_inventoryvarietycomparisonitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| report | ForeignKey | No | - | Yes |
| variety | ForeignKey | No | - | Yes |
| purchase_price | DecimalField | Yes | - | No |
| selling_price | DecimalField | Yes | - | No |
| purchase_quantity | DecimalField | Yes | - | No |
| sales_quantity | DecimalField | Yes | - | No |
| purchase_volume | DecimalField | Yes | - | No |
| sales_volume | DecimalField | Yes | - | No |
| inventory_turnover_rate | FloatField | Yes | - | No |
| capital_recovery_rate | FloatField | Yes | - | No |
| sales_recovery_rate | FloatField | Yes | - | No |
| engineers_count | IntegerField | Yes | - | No |
| engineers_sales_percentage | FloatField | Yes | - | No |
| customers_count | IntegerField | Yes | - | No |
| customers_sales_percentage | FloatField | Yes | - | No |
| additional_data | JSONField | No | <class 'dict'> | No |

**Foreign Keys**:

- `report` → agricultural_experiments.InventoryVarietyComparisonReport
- `variety` → agricultural_experiments.Variety

**Unique Together**:

- (report, variety)

---

### InventoryVarietyComparisonReport

**Table**: `agricultural_experiments_inventoryvarietycomparisonreport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| report_date | DateTimeField | No | - | No |
| time_period_start | DateField | No | - | No |
| time_period_end | DateField | No | - | No |
| criteria | JSONField | No | <class 'dict'> | No |
| results | JSONField | No | <class 'dict'> | No |
| summary | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| varieties | ManyToManyField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `items` (from agricultural_experiments.InventoryVarietyComparisonItem)

---

### Location

**Table**: `agricultural_experiments_location`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| address | TextField | No | - | No |
| coordinates | CharField | Yes | - | No |
| area | DecimalField | No | - | No |
| soil_type | CharField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `experiments` (from agricultural_experiments.Experiment)

---

### PlantSpecification

**Table**: `agricultural_experiments_plantspecification`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment_variety | ForeignKey | No | - | Yes |
| evaluation_date | DateField | No | - | No |
| earliness_rating | IntegerField | Yes | - | No |
| plant_vigor_rating | IntegerField | Yes | - | No |
| leaf_shape_description | CharField | No | - | No |
| fruit_coverage_rating | IntegerField | Yes | - | No |
| fungal_resistance_rating | IntegerField | Yes | - | No |
| bacterial_resistance_rating | IntegerField | Yes | - | No |
| insect_resistance_rating | IntegerField | Yes | - | No |
| viral_resistance_rating | IntegerField | Yes | - | No |
| cold_tolerance_rating | IntegerField | Yes | - | No |
| heat_tolerance_rating | IntegerField | Yes | - | No |
| soil_salinity_tolerance_rating | IntegerField | Yes | - | No |
| water_salinity_tolerance_rating | IntegerField | Yes | - | No |
| drought_tolerance_rating | IntegerField | Yes | - | No |
| notes | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `experiment_variety` → agricultural_experiments.ExperimentVariety

---

### Season

**Table**: `agricultural_experiments_season`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| season_type | CharField | No | - | No |
| start_date | DateField | No | - | No |
| end_date | DateField | No | - | No |
| is_active | BooleanField | No | True | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `experiments` (from agricultural_experiments.Experiment)

---

### Variety

**Table**: `agricultural_experiments_variety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| lot_number | CharField | Yes | - | No |
| variety_type | ForeignKey | No | - | Yes |
| is_competitor | BooleanField | No | False | No |
| competitor_name | CharField | Yes | - | No |
| competitor_price | DecimalField | Yes | - | No |
| status | CharField | No | testing | No |
| description | TextField | Yes | - | No |
| seed_source | CharField | Yes | - | No |
| seed_inventory_item | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `variety_type` → agricultural_experiments.VarietyType
- `seed_inventory_item` → inventory.Product
- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `experiment_participations` (from agricultural_experiments.ExperimentVariety)
- `ai_analyses` (from agricultural_experiments.VarietyAIAnalysis)
- `external_varieties` (from agricultural_experiments.ExternalVariety)
- `comparison_report_items` (from agricultural_experiments.VarietyComparisonReportItem)
- `inventory_comparison_items` (from agricultural_experiments.InventoryVarietyComparisonItem)

---

### VarietyAIAnalysis

**Table**: `agricultural_experiments_varietyaianalysis`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| ai_analysis | ForeignKey | No | - | Yes |
| experiment_variety | ForeignKey | Yes | - | Yes |
| variety | ForeignKey | Yes | - | Yes |
| is_external | BooleanField | No | False | No |
| performance_score | FloatField | Yes | - | No |
| strengths | JSONField | No | <class 'list'> | No |
| weaknesses | JSONField | No | <class 'list'> | No |
| recommendations | TextField | No | - | No |
| predicted_yield | FloatField | Yes | - | No |
| predicted_market_potential | FloatField | Yes | - | No |
| suggested_price | DecimalField | Yes | - | No |

**Foreign Keys**:

- `ai_analysis` → agricultural_experiments.AIAnalysis
- `experiment_variety` → agricultural_experiments.ExperimentVariety
- `variety` → agricultural_experiments.Variety

---

### VarietyComparisonReport

**Table**: `agricultural_experiments_varietycomparisonreport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| report_date | DateTimeField | No | - | No |
| report_type | CharField | No | - | No |
| time_period_start | DateField | Yes | - | No |
| time_period_end | DateField | Yes | - | No |
| criteria | JSONField | No | <class 'dict'> | No |
| results | JSONField | No | <class 'dict'> | No |
| summary | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `experiment` → agricultural_experiments.Experiment
- `created_by` → users.User

**Reverse Relations**:

- `items` (from agricultural_experiments.VarietyComparisonReportItem)

---

### VarietyComparisonReportItem

**Table**: `agricultural_experiments_varietycomparisonreportitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| report | ForeignKey | No | - | Yes |
| experiment_variety | ForeignKey | Yes | - | Yes |
| external_variety | ForeignKey | Yes | - | Yes |
| variety | ForeignKey | No | - | Yes |
| is_external | BooleanField | No | False | No |
| performance_data | JSONField | No | <class 'dict'> | No |
| pricing_data | JSONField | No | <class 'dict'> | No |
| sales_data | JSONField | No | <class 'dict'> | No |
| inventory_data | JSONField | No | <class 'dict'> | No |
| customer_data | JSONField | No | <class 'dict'> | No |
| engineer_data | JSONField | No | <class 'dict'> | No |

**Foreign Keys**:

- `report` → agricultural_experiments.VarietyComparisonReport
- `experiment_variety` → agricultural_experiments.ExperimentVariety
- `external_variety` → agricultural_experiments.ExternalVariety
- `variety` → agricultural_experiments.Variety

**Unique Together**:

- (report, variety)

---

### VarietyType

**Table**: `agricultural_experiments_varietytype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| scientific_name | CharField | Yes | - | No |
| description | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `varieties` (from agricultural_experiments.Variety)

---

## agricultural_production

### OperationEquipmentCost

**Table**: `agricultural_production_operationequipmentcost`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| operation | ForeignKey | No | - | Yes |
| equipment_name | CharField | No | - | No |
| hours | DecimalField | No | - | No |
| hourly_rate | DecimalField | No | - | No |
| cost | DecimalField | No | - | No |

**Foreign Keys**:

- `operation` → agricultural_production.ProductionOperation

---

### OperationLaborCost

**Table**: `agricultural_production_operationlaborcost`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| operation | ForeignKey | No | - | Yes |
| employee_name | CharField | No | - | No |
| hours | DecimalField | No | - | No |
| hourly_rate | DecimalField | No | - | No |
| cost | DecimalField | No | - | No |

**Foreign Keys**:

- `operation` → agricultural_production.ProductionOperation

---

### OperationMaterialCost

**Table**: `agricultural_production_operationmaterialcost`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| operation | ForeignKey | No | - | Yes |
| material_name | CharField | No | - | No |
| quantity | DecimalField | No | - | No |
| unit_cost | DecimalField | No | - | No |
| cost | DecimalField | No | - | No |

**Foreign Keys**:

- `operation` → agricultural_production.ProductionOperation

---

### ProductionBatch

**Table**: `agricultural_production_productionbatch`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| production_order | ForeignKey | Yes | - | Yes |
| batch_number | CharField | No | - | No |
| lot_number | CharField | No | - | No |
| product | CharField | No | - | No |
| grade | CharField | No | - | No |
| quantity | DecimalField | Yes | - | No |
| unit | CharField | No | - | No |
| status | CharField | No | draft | No |
| completion_date | DateField | Yes | - | No |
| expiry_date | DateField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `production_order` → agricultural_production.ProductionOrder
- `created_by` → users.User
- `updated_by` → users.User

---

### ProductionOperation

**Table**: `agricultural_production_productionoperation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| production_order | ForeignKey | No | - | Yes |
| operation_type | CharField | No | - | No |
| sequence | PositiveIntegerField | No | - | No |
| planned_start_date | DateTimeField | No | - | No |
| actual_start_date | DateTimeField | Yes | - | No |
| planned_end_date | DateTimeField | No | - | No |
| actual_end_date | DateTimeField | Yes | - | No |
| input_quantity | DecimalField | No | - | No |
| output_quantity | DecimalField | Yes | - | No |
| waste_quantity | DecimalField | Yes | - | No |
| status | CharField | No | draft | No |
| notes | TextField | No | - | No |
| responsible | ForeignKey | No | - | Yes |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `production_order` → agricultural_production.ProductionOrder
- `responsible` → users.User
- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `labor_costs` (from agricultural_production.OperationLaborCost)
- `equipment_costs` (from agricultural_production.OperationEquipmentCost)
- `material_costs` (from agricultural_production.OperationMaterialCost)
- `wastes` (from agricultural_production.ProductionWaste)

**Unique Together**:

- (production_order, sequence)

---

### ProductionOrder

**Table**: `agricultural_production_productionorder`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order_number | CharField | No | - | No |
| product_type | CharField | No | - | No |
| product | CharField | No | - | No |
| source | CharField | No | internal | No |
| supplier_name | CharField | Yes | - | No |
| farm | ForeignKey | Yes | - | Yes |
| seed_production_batch_id | CharField | Yes | - | No |
| planned_start_date | DateField | No | - | No |
| actual_start_date | DateField | Yes | - | No |
| planned_end_date | DateField | No | - | No |
| actual_end_date | DateField | Yes | - | No |
| input_quantity | DecimalField | No | - | No |
| input_unit | CharField | No | - | No |
| expected_output_quantity | DecimalField | No | - | No |
| actual_output_quantity | DecimalField | Yes | - | No |
| output_unit | CharField | No | - | No |
| status | CharField | No | draft | No |
| notes | TextField | No | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm
- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `operations` (from agricultural_production.ProductionOperation)
- `batches` (from agricultural_production.ProductionBatch)

---

### ProductionWaste

**Table**: `agricultural_production_productionwaste`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| production_operation | ForeignKey | Yes | - | Yes |
| product | CharField | No | - | No |
| waste_type | CharField | No | - | No |
| quantity | DecimalField | Yes | - | No |
| unit | CharField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `production_operation` → agricultural_production.ProductionOperation
- `created_by` → users.User

---

### RawMaterial

**Table**: `agricultural_production_rawmaterial`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| code | CharField | No | - | No |
| name | CharField | No | - | No |
| unit | CharField | No | - | No |

---

## ai

### AIActivity

**Table**: `ai_aiactivity`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| activity_type | CharField | No | - | No |
| user | ForeignKey | Yes | - | Yes |
| agent_name | CharField | No | - | No |
| service_name | CharField | No | - | No |
| action | CharField | No | - | No |
| details | JSONField | Yes | - | No |
| status | CharField | No | success | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

---

### AIIntegration

**Table**: `ai_aiintegration`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| integration_type | CharField | No | - | No |
| module_path | CharField | No | - | No |
| configuration | JSONField | Yes | - | No |
| status | CharField | No | inactive | No |
| last_sync | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### AIKnowledgeEntry

**Table**: `ai_aiknowledgeentry`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| entry_hash | CharField | No | - | No |
| content | TextField | No | - | No |
| source | ForeignKey | Yes | - | Yes |
| confidence_score | DecimalField | Yes | - | No |
| related_product | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| keywords | ManyToManyField | No | - | No |

**Foreign Keys**:

- `source` → ai.LearningSource
- `related_product` → inventory.Product

---

### AIModel

**Table**: `ai_aimodel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| provider | CharField | No | - | No |
| model_identifier | CharField | No | - | No |
| is_active | BooleanField | No | True | Yes |
| description | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `crop_analyses` (from ai_agriculture.CropAnalysis)
- `crop_predictions` (from ai_agriculture.CropPrediction)
- `yield_predictions` (from ai_agriculture.YieldPrediction)
- `agri_predictions` (from ai_agriculture.AgriPrediction)

**Indexes**:

- ai_aimodel_name_e917eb_idx: (name)
- ai_aimodel_is_acti_b3a235_idx: (is_active)

---

### AIPerformanceLog

**Table**: `ai_aiperformancelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trace_id | CharField | No | - | Yes |
| parent_log | ForeignKey | Yes | - | Yes |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| event_type | CharField | No | - | No |
| acting_agent | ForeignKey | Yes | - | Yes |
| target_agent | ForeignKey | Yes | - | Yes |
| input_data | JSONField | Yes | - | No |
| output_data | JSONField | Yes | - | No |
| metadata | JSONField | Yes | - | No |
| latency_ms | PositiveIntegerField | Yes | - | No |
| status | CharField | No | success | No |
| error_message | TextField | Yes | - | No |

**Foreign Keys**:

- `parent_log` → ai.AIPerformanceLog
- `acting_agent` → ai.ModelDeployment
- `target_agent` → ai.ModelDeployment

**Reverse Relations**:

- `child_logs` (from ai.AIPerformanceLog)

---

### AISettings

**Table**: `ai_aisettings`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| key | CharField | No | - | No |
| value | JSONField | No | - | No |
| description | TextField | No | - | No |
| is_system | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### APIKey

**Table**: `ai_apikey`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| key_type | CharField | No | - | No |
| key_value | CharField | No | - | No |
| is_active | BooleanField | No | True | No |
| description | TextField | No | - | No |
| expires_at | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `created_by` → users.User

---

### Conversation

**Table**: `ai_conversation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| title | CharField | Yes | - | No |
| start_time | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| last_updated | DateTimeField | No | - | No |
| summary | TextField | Yes | - | No |

**Foreign Keys**:

- `user` → users.User

**Reverse Relations**:

- `messages` (from ai.Message)

**Indexes**:

- ai_conversa_last_up_6a052e_idx: (-last_updated, user)

---

### DataDriftReport

**Table**: `ai_datadriftreport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| report_time | DateTimeField | No | - | No |
| model_deployment | ForeignKey | Yes | - | Yes |
| reference_data_info | CharField | Yes | - | No |
| current_data_info | CharField | Yes | - | No |
| drift_detected | BooleanField | No | False | No |
| drift_details | JSONField | Yes | - | No |
| report_file_path | FileField | Yes | - | No |

**Foreign Keys**:

- `model_deployment` → ai.ModelDeployment

---

### Keyword

**Table**: `ai_keyword`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| keyword | CharField | No | - | No |
| category | CharField | No | - | No |
| source | ForeignKey | Yes | - | Yes |
| is_system_generated | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `source` → ai.LearningSource

**Indexes**:

- ai_keyword_created_c564b8_idx: (-created_at, category)

---

### KeywordFile

**Table**: `ai_keywordfile`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| file_path | FileField | No | - | No |
| source_type | CharField | No | - | No |
| variety_name | CharField | Yes | - | Yes |
| description | TextField | Yes | - | No |
| uploaded_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `uploaded_by` → users.User

**Indexes**:

- ai_keywordf_created_abf5c9_idx: (-created_at, source_type)

---

### LearningSource

**Table**: `ai_learningsource`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| source_type | CharField | No | - | No |
| url | CharField | Yes | - | No |
| file_path | CharField | Yes | - | No |
| reliability_score | DecimalField | Yes | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `keywords` (from ai.Keyword)
- `aiknowledgeentry` (from ai.AIKnowledgeEntry)

**Indexes**:

- ai_learning_created_056913_idx: (-created_at, source_type)

---

### Message

**Table**: `ai_message`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| conversation | ForeignKey | No | - | Yes |
| sender_type | CharField | No | user | No |
| text_content | TextField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| feedback_score | IntegerField | Yes | - | No |
| feedback_notes | TextField | Yes | - | No |

**Foreign Keys**:

- `conversation` → ai.Conversation

**Indexes**:

- ai_message_timesta_8cb0de_idx: (timestamp, sender_type)

---

### ModelDeployment

**Table**: `ai_modeldeployment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| training_run | ForeignKey | Yes | - | Yes |
| model_name | CharField | No | - | No |
| version | CharField | No | - | No |
| agent_type | CharField | No | general_assistant | No |
| model_category | CharField | No | other | No |
| cost_tier | CharField | No | medium | No |
| performance_rating | DecimalField | Yes | - | No |
| deployment_time | DateTimeField | No | - | No |
| endpoint_url | CharField | Yes | - | No |
| capabilities | JSONField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| description | TextField | Yes | - | No |

**Foreign Keys**:

- `training_run` → ai.TrainingRun

**Reverse Relations**:

- `performance_logs` (from ai.AIPerformanceLog)
- `targeted_performance_logs` (from ai.AIPerformanceLog)
- `datadriftreport` (from ai.DataDriftReport)

**Unique Together**:

- (model_name, version)

---

### ReferenceFile

**Table**: `ai_referencefile`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| file_path | FileField | No | - | No |
| file_type | CharField | No | - | No |
| description | TextField | Yes | - | No |
| uploaded_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `uploaded_by` → users.User

**Indexes**:

- ai_referenc_created_763f05_idx: (-created_at, file_type)

---

### TrainingRun

**Table**: `ai_trainingrun`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| model_name | CharField | No | - | No |
| start_time | DateTimeField | No | - | No |
| end_time | DateTimeField | Yes | - | No |
| status | CharField | No | running | No |
| dataset_description | TextField | Yes | - | No |
| hyperparameters | JSONField | Yes | - | No |
| metrics | JSONField | Yes | - | No |
| trained_model_path | CharField | Yes | - | No |
| notes | TextField | Yes | - | No |

**Reverse Relations**:

- `modeldeployment` (from ai.ModelDeployment)

---

## ai_agent

### Agent

**Table**: `ai_agent_agent`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| agent_type | ForeignKey | No | - | Yes |
| description | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| config | JSONField | No | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `agent_type` → ai_agent.AgentType

**Reverse Relations**:

- `initiated_interactions` (from ai_agent.AgentInteraction)
- `received_interactions` (from ai_agent.AgentInteraction)
- `activity_logs` (from ai_agent.AgentActivityLog)

---

### AgentActivityLog

**Table**: `ai_agent_agentactivitylog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | Yes |
| agent | ForeignKey | Yes | - | Yes |
| action | CharField | No | - | Yes |
| status | CharField | No | info | Yes |
| related_interaction | ForeignKey | Yes | - | Yes |
| details | JSONField | No | <class 'dict'> | No |

**Foreign Keys**:

- `agent` → ai_agent.Agent
- `related_interaction` → ai_agent.AgentInteraction

---

### AgentInteraction

**Table**: `ai_agent_agentinteraction`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| initiating_agent | ForeignKey | Yes | - | Yes |
| responding_agent | ForeignKey | Yes | - | Yes |
| interaction_type | CharField | No | - | No |
| interaction_pattern | CharField | No | direct_async | No |
| correlation_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| content | JSONField | No | - | No |
| response_content | JSONField | Yes | - | No |
| status | CharField | No | queued | No |
| error_details | TextField | Yes | - | No |
| retry_count | PositiveIntegerField | No | 0 | No |
| created_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| updated_at | DateTimeField | No | - | No |
| completed_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `initiating_agent` → ai_agent.Agent
- `responding_agent` → ai_agent.Agent

**Reverse Relations**:

- `activity_logs` (from ai_agent.AgentActivityLog)

---

### AgentType

**Table**: `ai_agent_agenttype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |

**Reverse Relations**:

- `agents` (from ai_agent.Agent)

---

## ai_agents

### Agent

**Table**: `ai_agents_agent`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | Yes |
| description | TextField | No | - | No |
| agent_type | CharField | No | - | Yes |
| owner | ForeignKey | Yes | - | Yes |
| avatar | FileField | Yes | - | No |
| configuration | JSONField | No | <class 'dict'> | No |
| status | CharField | No | inactive | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| last_active | DateTimeField | Yes | - | Yes |
| api_key | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| version | CharField | No | 1.0.0 | No |
| is_system_agent | BooleanField | No | False | No |

**Foreign Keys**:

- `owner` → users.User

**Reverse Relations**:

- `capabilities` (from ai_agents.AgentCapability)
- `roles` (from ai_agents.AgentRole)
- `sent_messages` (from ai_agents.Message)
- `received_messages` (from ai_agents.Message)
- `activities` (from ai_agents.AgentActivity)
- `errors` (from ai_agents.ErrorLog)

**Indexes**:

- ai_agents_a_status_c7e30d_idx: (status, agent_type)
- ai_agents_a_owner_i_9b0d5e_idx: (owner, status)

---

### AgentActivity

**Table**: `ai_agents_agentactivity`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| agent | ForeignKey | No | - | Yes |
| activity_type | CharField | No | - | Yes |
| description | TextField | No | - | No |
| metadata | JSONField | No | <class 'dict'> | No |
| created_at | DateTimeField | No | - | Yes |
| ip_address | GenericIPAddressField | Yes | - | No |
| user_agent | TextField | Yes | - | No |

**Foreign Keys**:

- `agent` → ai_agents.Agent

**Indexes**:

- ai_agents_a_agent_i_80fd41_idx: (agent, activity_type)
- ai_agents_a_agent_i_67b68b_idx: (agent, created_at)

---

### AgentCapability

**Table**: `ai_agents_agentcapability`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| agent | ForeignKey | No | - | Yes |
| name | CharField | No | - | Yes |
| description | TextField | No | - | No |
| parameters | JSONField | No | <class 'dict'> | No |
| is_enabled | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `agent` → ai_agents.Agent

**Indexes**:

- ai_agents_a_agent_i_95d498_idx: (agent, is_enabled)

**Unique Together**:

- (agent, name)

---

### AgentRole

**Table**: `ai_agents_agentrole`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| agent | ForeignKey | No | - | Yes |
| role | ForeignKey | No | - | Yes |
| assigned_at | DateTimeField | No | - | No |
| assigned_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `agent` → ai_agents.Agent
- `role` → ai_agents.Role
- `assigned_by` → users.User

**Indexes**:

- ai_agents_a_agent_i_0639b4_idx: (agent, is_active)

**Unique Together**:

- (agent, role)

---

### ErrorLog

**Table**: `ai_agents_errorlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| error_type | CharField | No | - | Yes |
| error_message | TextField | No | - | No |
| stack_trace | TextField | Yes | - | No |
| agent | ForeignKey | Yes | - | Yes |
| message | ForeignKey | Yes | - | Yes |
| severity | CharField | No | medium | Yes |
| metadata | JSONField | No | <class 'dict'> | No |
| created_at | DateTimeField | No | - | Yes |
| resolved | BooleanField | No | False | Yes |
| resolved_at | DateTimeField | Yes | - | No |
| resolved_by | ForeignKey | Yes | - | Yes |
| resolution_notes | TextField | Yes | - | No |
| error_code | CharField | Yes | - | No |

**Foreign Keys**:

- `agent` → ai_agents.Agent
- `message` → ai_agents.Message
- `resolved_by` → users.User

**Indexes**:

- ai_agents_e_error_t_0ca827_idx: (error_type, severity)
- ai_agents_e_agent_i_c121a8_idx: (agent, resolved)

---

### Message

**Table**: `ai_agents_message`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| sender | ForeignKey | No | - | Yes |
| receiver | ForeignKey | No | - | Yes |
| message_type | CharField | No | - | Yes |
| content | TextField | No | - | No |
| metadata | JSONField | No | <class 'dict'> | No |
| status | CharField | No | pending | Yes |
| priority | IntegerField | No | 0 | Yes |
| created_at | DateTimeField | No | - | No |
| delivered_at | DateTimeField | Yes | - | No |
| read_at | DateTimeField | Yes | - | No |
| processed_at | DateTimeField | Yes | - | No |
| error_message | TextField | Yes | - | No |
| retry_count | IntegerField | No | 0 | No |
| expires_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `sender` → ai_agents.Agent
- `receiver` → ai_agents.Agent

**Reverse Relations**:

- `errors` (from ai_agents.ErrorLog)

**Indexes**:

- ai_agents_m_sender__7ca669_idx: (sender, status)
- ai_agents_m_receive_aa384e_idx: (receiver, status)
- ai_agents_m_priorit_fad3d8_idx: (priority, created_at)

---

### Permission

**Table**: `ai_agents_permission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code_name | CharField | No | - | Yes |
| description | TextField | No | - | No |
| category | CharField | No | general | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `roles` (from ai_agents.RolePermission)

---

### Role

**Table**: `ai_agents_role`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | Yes |
| description | TextField | No | - | No |
| is_system_role | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `permissions` (from ai_agents.RolePermission)
- `users` (from ai_agents.UserRole)
- `agents` (from ai_agents.AgentRole)

---

### RolePermission

**Table**: `ai_agents_rolepermission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| role | ForeignKey | No | - | Yes |
| permission | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `role` → ai_agents.Role
- `permission` → ai_agents.Permission

**Indexes**:

- ai_agents_r_role_id_599ee7_idx: (role, permission)

**Unique Together**:

- (role, permission)

---

### UserRole

**Table**: `ai_agents_userrole`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| role | ForeignKey | No | - | Yes |
| assigned_at | DateTimeField | No | - | No |
| assigned_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `user` → users.User
- `role` → ai_agents.Role
- `assigned_by` → users.User

**Indexes**:

- ai_agents_u_user_id_b46885_idx: (user, is_active)

**Unique Together**:

- (user, role)

---

## ai_agriculture

### AgriCropData

**Table**: `ai_agriculture_agricropdata`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| crop_type | CharField | No | - | No |
| planting_date | DateField | No | - | No |
| harvest_date | DateField | Yes | - | No |
| area | DecimalField | No | - | No |
| yield_amount | DecimalField | Yes | - | No |
| yield_quality | CharField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm

**Reverse Relations**:

- `predictions` (from ai_agriculture.AgriPrediction)
- `recommendations` (from ai_agriculture.AgriRecommendation)

---

### AgriPrediction

**Table**: `ai_agriculture_agriprediction`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| crop_data | ForeignKey | No | - | Yes |
| prediction_type | CharField | No | - | No |
| value | JSONField | No | - | No |
| confidence | FloatField | No | - | No |
| model | ForeignKey | Yes | - | Yes |
| input_parameters | JSONField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| valid_until | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `crop_data` → ai_agriculture.AgriCropData
- `model` → ai.AIModel

**Reverse Relations**:

- `recommendations` (from ai_agriculture.AgriRecommendation)

---

### AgriRecommendation

**Table**: `ai_agriculture_agrirecommendation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| crop_data | ForeignKey | Yes | - | Yes |
| prediction | ForeignKey | Yes | - | Yes |
| recommendation_type | CharField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| priority | CharField | No | medium | No |
| status | CharField | No | pending | No |
| implementation_date | DateTimeField | Yes | - | No |
| deadline | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `farm` → farms.Farm
- `crop_data` → ai_agriculture.AgriCropData
- `prediction` → ai_agriculture.AgriPrediction
- `created_by` → users.User
- `updated_by` → users.User

---

### CropAnalysis

**Table**: `ai_agriculture_cropanalysis`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| crop_type | CharField | No | - | No |
| planting_date | DateField | No | - | No |
| harvest_date | DateField | Yes | - | No |
| environmental_data | JSONField | No | <class 'dict'> | No |
| soil_analysis | ForeignKey | Yes | - | Yes |
| analysis_date | DateTimeField | No | - | No |
| status | CharField | No | pending | No |
| analysis_result | JSONField | Yes | - | No |
| ai_model | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm
- `soil_analysis` → ai_agriculture.SoilAnalysis
- `ai_model` → ai.AIModel

**Reverse Relations**:

- `recommendations` (from ai_agriculture.CropRecommendation)

---

### CropPrediction

**Table**: `ai_agriculture_cropprediction`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| crop_type | CharField | No | - | No |
| planting_date | DateField | No | - | No |
| current_growth_stage | CharField | No | - | No |
| symptoms | JSONField | Yes | - | No |
| images | JSONField | Yes | - | No |
| prediction_date | DateTimeField | No | - | No |
| status | CharField | No | pending | No |
| prediction_result | JSONField | Yes | - | No |
| ai_model | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm
- `ai_model` → ai.AIModel

---

### CropRecommendation

**Table**: `ai_agriculture_croprecommendation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| crop_analysis | ForeignKey | No | - | Yes |
| recommendation_type | CharField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| priority | CharField | No | medium | No |
| implementation_deadline | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `crop_analysis` → ai_agriculture.CropAnalysis

---

### SoilAnalysis

**Table**: `ai_agriculture_soilanalysis`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| soil_type | CharField | No | - | No |
| ph_level | FloatField | Yes | - | No |
| nitrogen_level | FloatField | Yes | - | No |
| phosphorus_level | FloatField | Yes | - | No |
| potassium_level | FloatField | Yes | - | No |
| organic_matter | FloatField | Yes | - | No |
| moisture_content | FloatField | Yes | - | No |
| analysis_date | DateTimeField | No | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm

**Reverse Relations**:

- `crop_analyses` (from ai_agriculture.CropAnalysis)

---

### YieldPrediction

**Table**: `ai_agriculture_yieldprediction`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| crop_type | CharField | No | - | No |
| planting_date | DateField | No | - | No |
| area_size | DecimalField | No | - | No |
| soil_type | CharField | Yes | - | No |
| prediction_date | DateTimeField | No | - | No |
| status | CharField | No | pending | No |
| prediction_result | JSONField | Yes | - | No |
| ai_model | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm
- `ai_model` → ai.AIModel

---

## ai_analytics

### AnalyticsDataset

**Table**: `ai_analytics_analyticsdataset`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| schema | JSONField | Yes | - | No |
| tags | JSONField | Yes | - | No |
| is_public | BooleanField | No | False | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| data_sources | ManyToManyField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `dataset_sources` (from ai_analytics.AnalyticsDatasetSource)
- `models` (from ai_analytics.AnalyticsModel)
- `reports` (from ai_analytics.AnalyticsReport)

---

### AnalyticsDatasetSource

**Table**: `ai_analytics_analyticsdatasetsource`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| dataset | ForeignKey | No | - | Yes |
| data_source | ForeignKey | No | - | Yes |
| transformation | JSONField | Yes | - | No |
| filters | JSONField | Yes | - | No |
| last_refresh | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `dataset` → ai_analytics.AnalyticsDataset
- `data_source` → ai_analytics.AnalyticsDataSource

**Unique Together**:

- (dataset, data_source)

---

### AnalyticsDataSource

**Table**: `ai_analytics_analyticsdatasource`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| source_type | CharField | No | - | No |
| connection_details | JSONField | Yes | - | No |
| credentials | JSONField | Yes | - | No |
| schema | JSONField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| refresh_interval | IntegerField | Yes | - | No |
| last_refresh | DateTimeField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `source_datasets` (from ai_analytics.AnalyticsDatasetSource)

---

### AnalyticsInsight

**Table**: `ai_analytics_analyticsinsight`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| insight_type | CharField | No | - | No |
| severity | CharField | No | info | No |
| report | ForeignKey | Yes | - | Yes |
| model | ForeignKey | Yes | - | Yes |
| data | JSONField | Yes | - | No |
| is_read | BooleanField | No | False | No |
| is_archived | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `report` → ai_analytics.AnalyticsReport
- `model` → ai_analytics.AnalyticsModel

---

### AnalyticsJob

**Table**: `ai_analytics_analyticsjob`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| job_type | CharField | No | - | No |
| status | CharField | No | pending | No |
| parameters | JSONField | Yes | - | No |
| result | JSONField | Yes | - | No |
| error_message | TextField | Yes | - | No |
| progress | FloatField | No | 0.0 | No |
| scheduled_at | DateTimeField | Yes | - | No |
| started_at | DateTimeField | Yes | - | No |
| completed_at | DateTimeField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### AnalyticsModel

**Table**: `ai_analytics_analyticsmodel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| model_type | CharField | No | - | No |
| status | CharField | No | draft | No |
| version | CharField | No | 1.0.0 | No |
| dataset | ForeignKey | Yes | - | Yes |
| parameters | JSONField | Yes | - | No |
| metrics | JSONField | Yes | - | No |
| model_path | CharField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `dataset` → ai_analytics.AnalyticsDataset
- `created_by` → users.User

**Reverse Relations**:

- `reports` (from ai_analytics.AnalyticsReport)
- `insights` (from ai_analytics.AnalyticsInsight)

---

### AnalyticsReport

**Table**: `ai_analytics_analyticsreport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| report_type | CharField | No | - | No |
| dataset | ForeignKey | Yes | - | Yes |
| model | ForeignKey | Yes | - | Yes |
| config | JSONField | No | - | No |
| filters | JSONField | Yes | - | No |
| schedule | JSONField | Yes | - | No |
| is_public | BooleanField | No | False | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `dataset` → ai_analytics.AnalyticsDataset
- `model` → ai_analytics.AnalyticsModel
- `created_by` → users.User

**Reverse Relations**:

- `insights` (from ai_analytics.AnalyticsInsight)

---

## ai_dashboard

### AIInsight

**Table**: `ai_dashboard_aiinsight`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| widget | ForeignKey | No | - | Yes |
| insight_type | CharField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| ai_analysis | TextField | No | - | No |
| confidence_score | FloatField | No | - | No |
| priority | CharField | No | medium | No |
| data_snapshot | JSONField | No | <class 'dict'> | No |
| is_active | BooleanField | No | True | No |
| generated_at | DateTimeField | No | - | No |
| expires_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `widget` → ai_dashboard.DashboardWidget

---

### AIModelPerformance

**Table**: `ai_dashboard_aimodelperformance`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| model_name | CharField | No | - | No |
| widget | ForeignKey | No | - | Yes |
| response_time | FloatField | No | - | No |
| accuracy_score | FloatField | Yes | - | No |
| memory_usage | FloatField | Yes | - | No |
| cpu_usage | FloatField | Yes | - | No |
| error_count | IntegerField | No | 0 | No |
| error_details | TextField | No | - | No |
| timestamp | DateTimeField | No | - | No |

**Foreign Keys**:

- `widget` → ai_dashboard.DashboardWidget

---

### DashboardAnalytics

**Table**: `ai_dashboard_dashboardanalytics`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| widget | ForeignKey | No | - | Yes |
| view_count | IntegerField | No | 0 | No |
| interaction_count | IntegerField | No | 0 | No |
| time_spent | DurationField | Yes | - | No |
| last_viewed | DateTimeField | No | - | No |
| is_favorite | BooleanField | No | False | No |
| feedback_score | IntegerField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User
- `widget` → ai_dashboard.DashboardWidget

**Unique Together**:

- (user, widget)

---

### DashboardWidget

**Table**: `ai_dashboard_dashboardwidget`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| widget_type | CharField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| ai_enabled | BooleanField | No | False | No |
| ai_model | CharField | No | - | No |
| ai_prompt | TextField | No | - | No |
| data_source | CharField | No | - | No |
| query_config | JSONField | No | <class 'dict'> | No |
| refresh_interval | IntegerField | No | 30 | No |
| position_x | IntegerField | No | 0 | No |
| position_y | IntegerField | No | 0 | No |
| width | IntegerField | No | 4 | No |
| height | IntegerField | No | 3 | No |
| is_public | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | No | - | Yes |
| allowed_users | ManyToManyField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `aiinsight` (from ai_dashboard.AIInsight)
- `dashboardanalytics` (from ai_dashboard.DashboardAnalytics)
- `aimodelperformance` (from ai_dashboard.AIModelPerformance)

---

### SmartAlert

**Table**: `ai_dashboard_smartalert`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| message | TextField | No | - | No |
| alert_type | CharField | No | - | No |
| severity | CharField | No | - | No |
| ai_generated | BooleanField | No | False | No |
| ai_confidence | FloatField | Yes | - | No |
| is_global | BooleanField | No | False | No |
| is_active | BooleanField | No | True | No |
| is_read | BooleanField | No | False | No |
| source_data | JSONField | No | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |
| expires_at | DateTimeField | Yes | - | No |
| target_users | ManyToManyField | No | - | No |
| acknowledged_by | ManyToManyField | No | - | No |

---

## ai_memory

### KnowledgeBase

**Table**: `ai_memory_knowledgebase`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| knowledge_type | CharField | No | factual | No |
| domain | CharField | No | - | No |
| description | TextField | No | - | No |
| content | JSONField | No | <class 'dict'> | No |
| rules | JSONField | No | <class 'list'> | No |
| examples | JSONField | No | <class 'list'> | No |
| accuracy | FloatField | No | 0.8 | No |
| completeness | FloatField | No | 0.7 | No |
| reliability | FloatField | No | 0.8 | No |
| usage_count | PositiveIntegerField | No | 0 | No |
| last_used | DateTimeField | Yes | - | No |
| version | CharField | No | 1.0 | No |
| last_updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `last_updated_by` → users.User

**Indexes**:

- ai_memory_k_knowled_c92391_idx: (knowledge_type)
- ai_memory_k_domain_099b77_idx: (domain)
- ai_memory_k_is_acti_737322_idx: (is_active)
- ai_memory_k_accurac_73ba65_idx: (accuracy)
- ai_memory_k_usage_c_9f8c28_idx: (usage_count)

---

### LearningPattern

**Table**: `ai_memory_learningpattern`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| pattern_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| pattern_type | CharField | No | - | No |
| description | TextField | No | - | No |
| user | ForeignKey | Yes | - | Yes |
| agent_id | CharField | No | - | No |
| pattern_data | JSONField | No | <class 'dict'> | No |
| conditions | JSONField | No | <class 'list'> | No |
| actions | JSONField | No | <class 'list'> | No |
| confidence | FloatField | No | 0.5 | No |
| support | PositiveIntegerField | No | 1 | No |
| frequency | FloatField | No | 0.0 | No |
| applied_count | PositiveIntegerField | No | 0 | No |
| success_count | PositiveIntegerField | No | 0 | No |
| last_applied | DateTimeField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| discovered_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

**Indexes**:

- ai_memory_l_pattern_9b6f76_idx: (pattern_id)
- ai_memory_l_pattern_50626b_idx: (pattern_type)
- ai_memory_l_user_id_ff5066_idx: (user)
- ai_memory_l_agent_i_8da2ad_idx: (agent_id)
- ai_memory_l_confide_140f73_idx: (confidence)
- ai_memory_l_is_acti_336d82_idx: (is_active)

---

### Memory

**Table**: `ai_memory_memory`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| memory_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| memory_type | ForeignKey | No | - | Yes |
| context | ForeignKey | No | - | Yes |
| title | CharField | No | - | No |
| content | TextField | No | - | No |
| summary | TextField | No | - | No |
| structured_data | JSONField | No | <class 'dict'> | No |
| keywords | JSONField | No | <class 'list'> | No |
| entities | JSONField | No | <class 'list'> | No |
| importance | CharField | No | normal | No |
| confidence | CharField | No | medium | No |
| relevance_score | FloatField | No | 0.0 | No |
| access_count | PositiveIntegerField | No | 0 | No |
| last_accessed | DateTimeField | Yes | - | No |
| learned_from | CharField | No | - | No |
| validation_status | CharField | No | pending | No |
| expires_at | DateTimeField | Yes | - | No |
| is_permanent | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `memory_type` → ai_memory.MemoryType
- `context` → ai_memory.MemoryContext
- `created_by` → users.User

**Reverse Relations**:

- `outgoing_associations` (from ai_memory.MemoryAssociation)
- `incoming_associations` (from ai_memory.MemoryAssociation)

**Indexes**:

- ai_memory_m_memory__e87cff_idx: (memory_id)
- ai_memory_m_memory__6e2df3_idx: (memory_type)
- ai_memory_m_context_7ca1a8_idx: (context)
- ai_memory_m_importa_0f1379_idx: (importance)
- ai_memory_m_confide_a900c1_idx: (confidence)
- ai_memory_m_relevan_f1036c_idx: (relevance_score)
- ai_memory_m_validat_9a26a7_idx: (validation_status)
- ai_memory_m_expires_b24dea_idx: (expires_at)
- ai_memory_m_created_528be7_idx: (created_at)

---

### MemoryAssociation

**Table**: `ai_memory_memoryassociation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| source_memory | ForeignKey | No | - | Yes |
| target_memory | ForeignKey | No | - | Yes |
| association_type | CharField | No | - | No |
| strength | FloatField | No | 0.5 | No |
| description | TextField | No | - | No |
| learned_automatically | BooleanField | No | True | No |
| confidence | FloatField | No | 0.5 | No |
| usage_count | PositiveIntegerField | No | 0 | No |
| last_used | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `source_memory` → ai_memory.Memory
- `target_memory` → ai_memory.Memory

**Indexes**:

- ai_memory_m_source__eb1b8e_idx: (source_memory)
- ai_memory_m_target__7aa6b1_idx: (target_memory)
- ai_memory_m_associa_8c247f_idx: (association_type)
- ai_memory_m_strengt_ecfb82_idx: (strength)
- ai_memory_m_confide_b796f7_idx: (confidence)

**Unique Together**:

- (source_memory, target_memory, association_type)

---

### MemoryCleanupLog

**Table**: `ai_memory_memorycleanuplog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| cleanup_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| cleanup_type | CharField | No | - | No |
| description | TextField | No | - | No |
| memories_processed | PositiveIntegerField | No | 0 | No |
| memories_deleted | PositiveIntegerField | No | 0 | No |
| memories_archived | PositiveIntegerField | No | 0 | No |
| space_freed | BigIntegerField | No | 0 | No |
| started_at | DateTimeField | No | - | No |
| completed_at | DateTimeField | Yes | - | No |
| duration | DurationField | Yes | - | No |
| executed_by | ForeignKey | Yes | - | Yes |
| is_successful | BooleanField | No | True | No |
| error_message | TextField | No | - | No |

**Foreign Keys**:

- `executed_by` → users.User

**Indexes**:

- ai_memory_m_cleanup_fafe64_idx: (cleanup_id)
- ai_memory_m_cleanup_cce2a7_idx: (cleanup_type)
- ai_memory_m_started_eacd25_idx: (started_at)
- ai_memory_m_is_succ_224d91_idx: (is_successful)

---

### MemoryContext

**Table**: `ai_memory_memorycontext`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| context_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| context_type | CharField | No | conversation | No |
| description | TextField | No | - | No |
| user | ForeignKey | Yes | - | Yes |
| agent_id | CharField | No | - | No |
| metadata | JSONField | No | <class 'dict'> | No |
| tags | JSONField | No | <class 'list'> | No |
| started_at | DateTimeField | No | - | No |
| ended_at | DateTimeField | Yes | - | No |
| last_accessed | DateTimeField | No | - | No |
| is_active | BooleanField | No | True | No |
| is_archived | BooleanField | No | False | No |

**Foreign Keys**:

- `user` → users.User

**Reverse Relations**:

- `memories` (from ai_memory.Memory)

**Indexes**:

- ai_memory_m_context_c132a0_idx: (context_id)
- ai_memory_m_context_4f442f_idx: (context_type)
- ai_memory_m_user_id_33a92f_idx: (user)
- ai_memory_m_agent_i_99a5e2_idx: (agent_id)
- ai_memory_m_is_acti_7b6eaf_idx: (is_active)
- ai_memory_m_started_b4ab3b_idx: (started_at)

---

### MemoryType

**Table**: `ai_memory_memorytype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| type_code | CharField | No | - | No |
| description | TextField | No | - | No |
| retention_period | PositiveIntegerField | No | 60 | No |
| max_capacity | PositiveIntegerField | No | 1000 | No |
| priority | PositiveIntegerField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `memories` (from ai_memory.Memory)

---

## ai_models

### AIModel

**Table**: `ai_models_aimodel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| model_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| model_type | CharField | No | - | No |
| status | CharField | No | development | No |
| version | CharField | No | 1.0.0 | No |
| previous_version | CharField | No | - | No |
| training_data_size | BigIntegerField | No | 0 | No |
| training_duration | DurationField | Yes | - | No |
| training_cost | DecimalField | No | 0.00 | No |
| accuracy | FloatField | No | 0.0 | No |
| precision | FloatField | No | 0.0 | No |
| recall | FloatField | No | 0.0 | No |
| f1_score | FloatField | No | 0.0 | No |
| inference_time | FloatField | No | 0.0 | No |
| deployment_type | CharField | No | local | No |
| deployment_url | CharField | No | - | No |
| api_endpoint | CharField | No | - | No |
| memory_requirements | PositiveIntegerField | No | 512 | No |
| cpu_requirements | CharField | No | - | No |
| gpu_requirements | CharField | No | - | No |
| model_file_path | CharField | No | - | No |
| config_file_path | CharField | No | - | No |
| weights_file_path | CharField | No | - | No |
| total_requests | PositiveIntegerField | No | 0 | No |
| successful_requests | PositiveIntegerField | No | 0 | No |
| average_response_time | FloatField | No | 0.0 | No |
| last_used | DateTimeField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| is_default | BooleanField | No | False | No |
| deployed_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `conversation` (from intelligent_assistant.Conversation)
- `userpreference` (from intelligent_assistant.UserPreference)
- `aianalytics` (from intelligent_assistant.AIAnalytics)
- `versions` (from ai_models.ModelVersion)
- `usage_logs` (from ai_models.ModelUsageLog)

---

### ModelDeployment

**Table**: `ai_models_modeldeployment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| deployment_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| model_version | ForeignKey | No | - | Yes |
| environment | CharField | No | - | No |
| status | CharField | No | pending | No |
| deployment_config | JSONField | No | <class 'dict'> | No |
| scaling_config | JSONField | No | <class 'dict'> | No |
| service_name | CharField | No | - | No |
| service_port | PositiveIntegerField | Yes | - | No |
| health_check_url | CharField | No | - | No |
| allocated_memory | PositiveIntegerField | No | 512 | No |
| allocated_cpu | FloatField | No | 0.5 | No |
| allocated_gpu | PositiveIntegerField | No | 0 | No |
| current_load | FloatField | No | 0.0 | No |
| peak_load | FloatField | No | 0.0 | No |
| uptime_percentage | FloatField | No | 0.0 | No |
| deployed_at | DateTimeField | Yes | - | No |
| last_health_check | DateTimeField | Yes | - | No |
| deployed_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `model_version` → ai_models.ModelVersion
- `deployed_by` → users.User

---

### ModelUsageLog

**Table**: `ai_models_modelusagelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| log_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| model | ForeignKey | No | - | Yes |
| request_id | CharField | No | - | No |
| user | ForeignKey | Yes | - | Yes |
| input_data_size | PositiveIntegerField | No | 0 | No |
| output_data_size | PositiveIntegerField | No | 0 | No |
| processing_time | FloatField | No | 0.0 | No |
| success | BooleanField | No | True | No |
| error_message | TextField | No | - | No |
| confidence_score | FloatField | Yes | - | No |
| metadata | JSONField | No | <class 'dict'> | No |
| timestamp | DateTimeField | No | - | No |

**Foreign Keys**:

- `model` → ai_models.AIModel
- `user` → users.User

---

### ModelVersion

**Table**: `ai_models_modelversion`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| version_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| model | ForeignKey | No | - | Yes |
| version_number | CharField | No | - | No |
| release_notes | TextField | No | - | No |
| changes | JSONField | No | <class 'list'> | No |
| improvements | JSONField | No | <class 'list'> | No |
| bug_fixes | JSONField | No | <class 'list'> | No |
| performance_metrics | JSONField | No | <class 'dict'> | No |
| benchmark_results | JSONField | No | <class 'dict'> | No |
| model_file_size | BigIntegerField | No | 0 | No |
| checksum | CharField | No | - | No |
| is_stable | BooleanField | No | False | No |
| is_deprecated | BooleanField | No | False | No |
| released_at | DateTimeField | No | - | No |
| deprecated_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `model` → ai_models.AIModel

**Reverse Relations**:

- `deployments` (from ai_models.ModelDeployment)

**Unique Together**:

- (model, version_number)

---

## ai_monitoring

### PerformanceLog

**Table**: `ai_monitoring_performancelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| log_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| metric | ForeignKey | No | - | Yes |
| value | FloatField | No | - | No |
| previous_value | FloatField | Yes | - | No |
| change_percentage | FloatField | Yes | - | No |
| context_data | JSONField | No | <class 'dict'> | No |
| measured_at | DateTimeField | No | - | No |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `metric` → ai_monitoring.PerformanceMetric

---

### PerformanceMetric

**Table**: `ai_monitoring_performancemetric`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| metric_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| metric_type | CharField | No | - | No |
| description | TextField | No | - | No |
| current_value | FloatField | No | 0.0 | No |
| target_value | FloatField | No | 0.0 | No |
| threshold_min | FloatField | Yes | - | No |
| threshold_max | FloatField | Yes | - | No |
| agent_id | CharField | No | - | No |
| module_name | CharField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| last_measured | DateTimeField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Reverse Relations**:

- `logs` (from ai_monitoring.PerformanceLog)

---

### SystemAlert

**Table**: `ai_monitoring_systemalert`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| alert_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| title | CharField | No | - | No |
| message | TextField | No | - | No |
| severity | CharField | No | - | No |
| status | CharField | No | new | No |
| source_type | CharField | No | - | No |
| source_id | CharField | No | - | No |
| triggered_at | DateTimeField | No | - | No |
| acknowledged_at | DateTimeField | Yes | - | No |
| resolved_at | DateTimeField | Yes | - | No |
| acknowledged_by | ForeignKey | Yes | - | Yes |
| resolved_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `acknowledged_by` → users.User
- `resolved_by` → users.User

---

## ai_permissions

### AgentRole

**Table**: `ai_permissions_agentrole`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| agent | ForeignKey | No | - | Yes |
| role | ForeignKey | No | - | Yes |
| scope | CharField | No | - | No |
| valid_from | DateTimeField | No | - | No |
| valid_until | DateTimeField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| assigned_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `agent` → ai_permissions.AIAgent
- `role` → ai_permissions.AIRole
- `assigned_by` → users.User

**Unique Together**:

- (agent, role, scope)

---

### AIAgent

**Table**: `ai_permissions_aiagent`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `agentrole` (from ai_permissions.AgentRole)
- `aipermissionauditlog` (from ai_permissions.AIPermissionAuditLog)

---

### AIModel

**Table**: `ai_permissions_aimodel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| model_type | CharField | No | text | No |

---

### AIModelPermission

**Table**: `ai_permissions_aimodelpermission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| model_type | CharField | No | - | No |
| description | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Unique Together**:

- (name, model_type)

---

### AIPermissionAuditLog

**Table**: `ai_permissions_aipermissionauditlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| agent | ForeignKey | No | - | Yes |
| action | CharField | No | - | No |
| permission | CharField | No | - | No |
| result | BooleanField | No | - | No |
| details | JSONField | No | <class 'dict'> | No |
| user | ForeignKey | Yes | - | Yes |
| timestamp | DateTimeField | No | - | No |

**Foreign Keys**:

- `agent` → ai_permissions.AIAgent
- `user` → users.User

---

### AIRole

**Table**: `ai_permissions_airole`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| permissions | ManyToManyField | No | - | No |

**Reverse Relations**:

- `agentrole` (from ai_permissions.AgentRole)

---

## ai_reports

### AIReport

**Table**: `ai_reports_aireport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| report_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| report_type | CharField | No | - | No |
| status | CharField | No | generating | No |
| start_date | DateTimeField | No | - | No |
| end_date | DateTimeField | No | - | No |
| filters | JSONField | No | <class 'dict'> | No |
| criteria | JSONField | No | <class 'dict'> | No |
| data_sources | JSONField | No | <class 'list'> | No |
| summary_data | JSONField | No | <class 'dict'> | No |
| detailed_data | JSONField | No | <class 'dict'> | No |
| output_format | CharField | No | pdf | No |
| file_path | CharField | No | - | No |
| file_size | PositiveIntegerField | No | 0 | No |
| generation_time | DurationField | Yes | - | No |
| generated_by | ForeignKey | No | - | Yes |
| is_scheduled | BooleanField | No | False | No |
| schedule_frequency | CharField | No | - | No |
| next_generation | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| completed_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `generated_by` → users.User

**Reverse Relations**:

- `insights` (from ai_reports.ReportInsight)

---

### ReportInsight

**Table**: `ai_reports_reportinsight`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| insight_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| report | ForeignKey | No | - | Yes |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| insight_type | CharField | No | - | No |
| supporting_data | JSONField | No | <class 'dict'> | No |
| metrics | JSONField | No | <class 'dict'> | No |
| confidence | CharField | No | medium | No |
| importance_score | FloatField | No | 0.5 | No |
| recommendations | JSONField | No | <class 'list'> | No |
| action_items | JSONField | No | <class 'list'> | No |
| discovered_at | DateTimeField | No | - | No |
| is_acknowledged | BooleanField | No | False | No |
| acknowledged_by | ForeignKey | Yes | - | Yes |
| acknowledged_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `report` → ai_reports.AIReport
- `acknowledged_by` → users.User

---

### ReportSchedule

**Table**: `ai_reports_reportschedule`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| schedule_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| template | ForeignKey | No | - | Yes |
| frequency | CharField | No | - | No |
| custom_cron | CharField | No | - | No |
| start_time | TimeField | No | - | No |
| timezone | CharField | No | UTC | No |
| recipients | JSONField | No | <class 'list'> | No |
| email_subject | CharField | No | - | No |
| email_body | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| last_run | DateTimeField | Yes | - | No |
| next_run | DateTimeField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `template` → ai_reports.ReportTemplate
- `created_by` → users.User

---

### ReportTemplate

**Table**: `ai_reports_reporttemplate`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| template_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| report_type | CharField | No | - | No |
| template_config | JSONField | No | <class 'dict'> | No |
| default_filters | JSONField | No | <class 'dict'> | No |
| chart_configs | JSONField | No | <class 'list'> | No |
| layout_config | JSONField | No | <class 'dict'> | No |
| style_config | JSONField | No | <class 'dict'> | No |
| usage_count | PositiveIntegerField | No | 0 | No |
| last_used | DateTimeField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| is_public | BooleanField | No | False | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `schedules` (from ai_reports.ReportSchedule)

---

## ai_security

### SecurityAccessControl

**Table**: `ai_security_securityaccesscontrol`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| resource_type | CharField | No | - | No |
| resource_id | CharField | No | - | No |
| access_level | CharField | No | - | No |
| conditions | JSONField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| roles | ManyToManyField | No | - | No |
| users | ManyToManyField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### SecurityAudit

**Table**: `ai_security_securityaudit`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| audit_type | CharField | No | - | No |
| description | TextField | No | - | No |
| status | CharField | No | scheduled | No |
| scope | JSONField | No | - | No |
| findings | JSONField | Yes | - | No |
| recommendations | JSONField | Yes | - | No |
| scheduled_at | DateTimeField | No | - | No |
| started_at | DateTimeField | Yes | - | No |
| completed_at | DateTimeField | Yes | - | No |
| conducted_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `conducted_by` → users.User

---

### SecurityIncident

**Table**: `ai_security_securityincident`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| incident_type | CharField | No | - | No |
| description | TextField | No | - | No |
| severity | CharField | No | - | No |
| status | CharField | No | reported | No |
| affected_systems | JSONField | No | - | No |
| reported_by | ForeignKey | Yes | - | Yes |
| assigned_to | ForeignKey | Yes | - | Yes |
| reported_at | DateTimeField | No | - | No |
| resolved_at | DateTimeField | Yes | - | No |
| resolution | TextField | Yes | - | No |
| root_cause | TextField | Yes | - | No |
| lessons_learned | TextField | Yes | - | No |

**Foreign Keys**:

- `reported_by` → users.User
- `assigned_to` → users.User

---

### SecurityPolicy

**Table**: `ai_security_securitypolicy`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| policy_type | CharField | No | - | No |
| description | TextField | No | - | No |
| rules | JSONField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| applies_to_models | ManyToManyField | No | - | No |
| applies_to_agents | ManyToManyField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### SecurityScan

**Table**: `ai_security_securityscan`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| scan_type | CharField | No | - | No |
| description | TextField | No | - | No |
| status | CharField | No | scheduled | No |
| configuration | JSONField | No | - | No |
| results | JSONField | Yes | - | No |
| scheduled_at | DateTimeField | No | - | No |
| started_at | DateTimeField | Yes | - | No |
| completed_at | DateTimeField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| target_models | ManyToManyField | No | - | No |
| target_agents | ManyToManyField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### SecurityVulnerability

**Table**: `ai_security_securityvulnerability`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| vulnerability_type | CharField | No | - | No |
| description | TextField | No | - | No |
| severity | CharField | No | - | No |
| status | CharField | No | identified | No |
| discovered_by | ForeignKey | Yes | - | Yes |
| assigned_to | ForeignKey | Yes | - | Yes |
| discovered_at | DateTimeField | No | - | No |
| remediated_at | DateTimeField | Yes | - | No |
| remediation_steps | TextField | Yes | - | No |
| verification_steps | TextField | Yes | - | No |
| affected_models | ManyToManyField | No | - | No |
| affected_agents | ManyToManyField | No | - | No |

**Foreign Keys**:

- `discovered_by` → users.User
- `assigned_to` → users.User

---

## ai_services

### AIMemoryIntegration

**Table**: `ai_services_aimemoryintegration`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| service | OneToOneField | No | - | Yes |
| memory_enabled | BooleanField | No | False | No |
| short_term_memory_ttl | PositiveIntegerField | No | 3600 | No |
| long_term_memory_enabled | BooleanField | No | False | No |
| memory_config | JSONField | No | <class 'dict'> | No |

**Reverse Relations**:

- `service` (from ai_services.AIService)

---

### AIModel

**Table**: `ai_services_aimodel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | Yes |
| description | TextField | No | - | No |
| model_type | CharField | No | local | Yes |
| provider | CharField | No | - | No |
| model_identifier | CharField | No | - | No |
| is_active | BooleanField | No | True | Yes |
| config | JSONField | No | <class 'dict'> | No |
| cost_per_token | DecimalField | No | 0 | No |
| usage_limit | PositiveIntegerField | Yes | - | No |

**Reverse Relations**:

- `model_services` (from ai_services.AIServiceModel)
- `usage_logs` (from ai_services.AIUsageLog)
- `usage_summaries` (from ai_services.AIUsageSummary)

**Indexes**:

- ai_services_name_8b9541_idx: (name)
- ai_services_model_t_39bec4_idx: (model_type)
- ai_services_is_acti_63c481_idx: (is_active)

---

### AIService

**Table**: `ai_services_aiservice`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | Yes |
| description | TextField | No | - | No |
| service_type | CharField | No | - | Yes |
| is_active | BooleanField | No | True | Yes |
| config | JSONField | No | <class 'dict'> | No |
| ai_models | ManyToManyField | No | - | No |

**Reverse Relations**:

- `service_models` (from ai_services.AIServiceModel)
- `usage_logs` (from ai_services.AIUsageLog)
- `usage_summaries` (from ai_services.AIUsageSummary)
- `memory_integration` (from ai_services.AIMemoryIntegration)

**Indexes**:

- ai_services_name_6a4ace_idx: (name)
- ai_services_service_44f746_idx: (service_type)
- ai_services_is_acti_9a3513_idx: (is_active)

---

### AIServiceModel

**Table**: `ai_services_aiservicemodel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| service | ForeignKey | No | - | Yes |
| model | ForeignKey | No | - | Yes |
| is_default | BooleanField | No | False | No |
| config_override | JSONField | No | <class 'dict'> | No |

**Foreign Keys**:

- `service` → ai_services.AIService
- `model` → ai_services.AIModel

**Indexes**:

- ai_services_is_defa_a05e55_idx: (is_default)

**Unique Together**:

- (service, model)

---

### AIUsageLog

**Table**: `ai_services_aiusagelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| service | ForeignKey | Yes | - | Yes |
| model | ForeignKey | Yes | - | Yes |
| user | ForeignKey | Yes | - | Yes |
| agent_id | CharField | Yes | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | Yes |
| request_data | JSONField | No | <class 'dict'> | No |
| response_data | JSONField | No | <class 'dict'> | No |
| tokens_input | PositiveIntegerField | No | 0 | No |
| tokens_output | PositiveIntegerField | No | 0 | No |
| cost | DecimalField | No | 0 | No |
| status | CharField | No | success | Yes |
| error_message | TextField | Yes | - | No |

**Foreign Keys**:

- `service` → ai_services.AIService
- `model` → ai_services.AIModel
- `user` → users.User

**Indexes**:

- ai_services_timesta_381980_idx: (-timestamp)
- ai_services_service_33770e_idx: (service, -timestamp)
- ai_services_model_i_42653c_idx: (model, -timestamp)
- ai_services_user_id_6711ae_idx: (user, -timestamp)
- ai_services_status_7a5dd4_idx: (status)

---

### AIUsageSummary

**Table**: `ai_services_aiusagesummary`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| period_type | CharField | No | - | Yes |
| period_start | DateTimeField | No | - | Yes |
| period_end | DateTimeField | No | - | No |
| service | ForeignKey | Yes | - | Yes |
| model | ForeignKey | Yes | - | Yes |
| user | ForeignKey | Yes | - | Yes |
| request_count | PositiveIntegerField | No | 0 | No |
| success_count | PositiveIntegerField | No | 0 | No |
| error_count | PositiveIntegerField | No | 0 | No |
| tokens_input | PositiveIntegerField | No | 0 | No |
| tokens_output | PositiveIntegerField | No | 0 | No |
| total_cost | DecimalField | No | 0 | No |

**Foreign Keys**:

- `service` → ai_services.AIService
- `model` → ai_services.AIModel
- `user` → users.User

**Indexes**:

- ai_services_period__906e05_idx: (period_type, -period_start)
- ai_services_service_d19fe2_idx: (service, period_type, -period_start)
- ai_services_model_i_611d7c_idx: (model, period_type, -period_start)
- ai_services_user_id_679a6d_idx: (user, period_type, -period_start)

**Unique Together**:

- (period_type, period_start, service, model, user)

---

## ai_training

### ModelEvaluation

**Table**: `ai_training_modelevaluation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| evaluation_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| training_job | ForeignKey | No | - | Yes |
| evaluation_name | CharField | No | - | No |
| test_dataset | ForeignKey | Yes | - | Yes |
| overall_accuracy | FloatField | No | 0.0 | No |
| precision | FloatField | No | 0.0 | No |
| recall | FloatField | No | 0.0 | No |
| f1_score | FloatField | No | 0.0 | No |
| detailed_results | JSONField | No | <class 'dict'> | No |
| confusion_matrix | JSONField | No | <class 'dict'> | No |
| evaluated_at | DateTimeField | No | - | No |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `training_job` → ai_training.TrainingJob
- `test_dataset` → ai_training.TrainingDataset

---

### TrainingDataset

**Table**: `ai_training_trainingdataset`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| dataset_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| dataset_type | CharField | No | - | No |
| status | CharField | No | collecting | No |
| total_samples | PositiveIntegerField | No | 0 | No |
| training_samples | PositiveIntegerField | No | 0 | No |
| validation_samples | PositiveIntegerField | No | 0 | No |
| test_samples | PositiveIntegerField | No | 0 | No |
| quality_score | FloatField | No | 0.0 | No |
| completeness | FloatField | No | 0.0 | No |
| consistency | FloatField | No | 0.0 | No |
| data_path | CharField | No | - | No |
| metadata_path | CharField | No | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| last_processed | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `training_jobs` (from ai_training.TrainingJob)
- `evaluations` (from ai_training.ModelEvaluation)

---

### TrainingJob

**Table**: `ai_training_trainingjob`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| job_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| job_type | CharField | No | - | No |
| status | CharField | No | pending | No |
| dataset | ForeignKey | No | - | Yes |
| model_name | CharField | No | - | No |
| model_version | CharField | No | 1.0 | No |
| hyperparameters | JSONField | No | <class 'dict'> | No |
| training_config | JSONField | No | <class 'dict'> | No |
| progress_percentage | FloatField | No | 0.0 | No |
| current_epoch | PositiveIntegerField | No | 0 | No |
| total_epochs | PositiveIntegerField | No | 100 | No |
| training_loss | FloatField | Yes | - | No |
| validation_loss | FloatField | Yes | - | No |
| training_accuracy | FloatField | Yes | - | No |
| validation_accuracy | FloatField | Yes | - | No |
| started_at | DateTimeField | Yes | - | No |
| completed_at | DateTimeField | Yes | - | No |
| estimated_completion | DateTimeField | Yes | - | No |
| gpu_usage | FloatField | No | 0.0 | No |
| memory_usage | FloatField | No | 0.0 | No |
| cpu_usage | FloatField | No | 0.0 | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `dataset` → ai_training.TrainingDataset
- `created_by` → users.User

**Reverse Relations**:

- `evaluations` (from ai_training.ModelEvaluation)

---

## analytics

### AnalyticsService

**Table**: `analytics_analyticsservice`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| service_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| service_type | CharField | No | - | No |
| tracking_id | CharField | No | - | No |
| api_key | CharField | No | - | No |
| track_pageviews | BooleanField | No | True | No |
| track_events | BooleanField | No | True | No |
| track_conversions | BooleanField | No | True | No |
| total_events | PositiveIntegerField | No | 0 | No |
| total_pageviews | PositiveIntegerField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

## auth

### Group

**Table**: `auth_group`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| name | CharField | No | - | No |
| permissions | ManyToManyField | No | - | No |

---

### Permission

**Table**: `auth_permission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| name | CharField | No | - | No |
| content_type | ForeignKey | No | - | Yes |
| codename | CharField | No | - | No |

**Foreign Keys**:

- `content_type` → contenttypes.ContentType

**Unique Together**:

- (content_type, codename)

---

## banking_payments

### BankProvider

**Table**: `banking_payments_bankprovider`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| provider_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| provider_type | CharField | No | - | No |
| status | CharField | No | active | No |
| api_endpoint | CharField | No | - | No |
| api_version | CharField | No | - | No |
| documentation_url | CharField | No | - | No |
| api_key | CharField | No | - | No |
| secret_key | CharField | No | - | No |
| webhook_url | CharField | No | - | No |
| total_transactions | PositiveIntegerField | No | 0 | No |
| successful_transactions | PositiveIntegerField | No | 0 | No |
| failed_transactions | PositiveIntegerField | No | 0 | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `transactions` (from banking_payments.PaymentTransaction)

---

### PaymentTransaction

**Table**: `banking_payments_paymenttransaction`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| transaction_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| provider | ForeignKey | No | - | Yes |
| transaction_type | CharField | No | - | No |
| amount | DecimalField | No | - | No |
| currency | CharField | No | USD | No |
| status | CharField | No | pending | No |
| processed_at | DateTimeField | Yes | - | No |
| description | TextField | No | - | No |
| reference_number | CharField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `provider` → banking_payments.BankProvider

---

## cloud_services

### CloudFile

**Table**: `cloud_services_cloudfile`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| file_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| provider | ForeignKey | No | - | Yes |
| original_name | CharField | No | - | No |
| file_path | CharField | No | - | No |
| file_type | CharField | No | - | No |
| file_size | BigIntegerField | No | - | No |
| mime_type | CharField | No | - | No |
| uploaded_by | ForeignKey | No | - | Yes |
| upload_date | DateTimeField | No | - | No |
| download_count | PositiveIntegerField | No | 0 | No |
| last_accessed | DateTimeField | Yes | - | No |
| is_public | BooleanField | No | False | No |
| is_archived | BooleanField | No | False | No |

**Foreign Keys**:

- `provider` → cloud_services.CloudProvider
- `uploaded_by` → users.User

---

### CloudProvider

**Table**: `cloud_services_cloudprovider`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| provider_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| provider_type | CharField | No | - | No |
| api_endpoint | CharField | No | - | No |
| access_key | CharField | No | - | No |
| secret_key | CharField | No | - | No |
| region | CharField | No | - | No |
| bucket_name | CharField | No | - | No |
| storage_quota | BigIntegerField | No | 0 | No |
| used_storage | BigIntegerField | No | 0 | No |
| total_files | PositiveIntegerField | No | 0 | No |
| total_uploads | PositiveIntegerField | No | 0 | No |
| total_downloads | PositiveIntegerField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| is_default | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `files` (from cloud_services.CloudFile)

---

## communication

### CommunicationLog

**Table**: `communication_communicationlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| communication_type | CharField | No | - | Yes |
| recipient | CharField | No | - | Yes |
| subject | CharField | No | - | No |
| message_body | TextField | No | - | No |
| status | CharField | No | PENDING | Yes |
| sent_at | DateTimeField | Yes | - | Yes |
| related_object_type | ForeignKey | Yes | - | Yes |
| related_object_id | PositiveIntegerField | Yes | - | Yes |
| error_message | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |
| related_object | GenericForeignKey | No | - | No |

**Foreign Keys**:

- `related_object_type` → contenttypes.ContentType

**Indexes**:

- communicati_related_dac88f_idx: (related_object_type, related_object_id)
- communicati_status_13febb_idx: (status, created_at)

---

### EmailTemplate

**Table**: `communication_emailtemplate`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| subject | CharField | No | - | No |
| body_html | TextField | No | - | No |
| body_text | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

## contacts

### Address

**Table**: `contacts_address`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| street | CharField | No | - | No |
| city | CharField | No | - | No |
| country | CharField | No | - | No |
| postal_code | CharField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### City

**Table**: `contacts_city`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| country | CharField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### Communication

**Table**: `contacts_communication`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| contact_type | CharField | No | - | No |
| value | CharField | No | - | No |
| is_primary | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### Contact

**Table**: `contacts_contact`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| email | CharField | Yes | - | No |
| phone | CharField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### ContactCategory

**Table**: `contacts_contactcategory`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### ContactTag

**Table**: `contacts_contacttag`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| color | CharField | No | #007bff | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### Country

**Table**: `contacts_country`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

## contenttypes

### ContentType

**Table**: `django_content_type`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| app_label | CharField | No | - | No |
| model | CharField | No | - | No |

**Reverse Relations**:

- `logentry` (from admin.LogEntry)
- `permission` (from auth.Permission)
- `user_activities` (from users.UserActivity)
- `journalentry` (from accounting.JournalEntry)
- `journal_lines` (from accounting.JournalEntryLine)
- `notification` (from notifications.Notification)
- `communicationlog` (from communication.CommunicationLog)
- `aiinsight` (from intelligent_assistant.AIInsight)

**Unique Together**:

- (app_label, model)

---

## core

### APIKey

**Table**: `core_apikey`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| company | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| key | CharField | No | - | No |
| prefix | CharField | No | - | No |
| type | CharField | No | user | No |
| scope | CharField | No | read | No |
| user | ForeignKey | No | - | Yes |
| expires_at | DateTimeField | Yes | - | No |
| last_used_at | DateTimeField | Yes | - | No |
| revoked | BooleanField | No | False | No |
| revoked_at | DateTimeField | Yes | - | No |
| revoked_reason | TextField | Yes | - | No |
| allowed_ips | TextField | Yes | - | No |
| allowed_referers | TextField | Yes | - | No |
| rate_limit | PositiveIntegerField | No | 100 | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company
- `user` → users.User

**Reverse Relations**:

- `logs` (from core.APIKeyLog)

**Indexes**:

- core_apikey_company_28c0ae_idx: (company)

---

### APIKeyLog

**Table**: `core_apikeylog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| api_key | ForeignKey | No | - | Yes |
| endpoint | CharField | No | - | No |
| method | CharField | No | - | No |
| status_code | PositiveIntegerField | No | - | No |
| ip_address | GenericIPAddressField | No | - | No |
| user_agent | TextField | Yes | - | No |
| referer | TextField | Yes | - | No |
| request_data | JSONField | Yes | - | No |
| response_data | JSONField | Yes | - | No |
| execution_time | FloatField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `api_key` → core.APIKey

---

### Branch

**Table**: `core_branch`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| code | CharField | Yes | - | No |
| company | ForeignKey | No | - | Yes |
| address | TextField | Yes | - | No |
| phone | CharField | Yes | - | No |
| email | CharField | Yes | - | No |
| country | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company
- `country` → core.Country

**Reverse Relations**:

- `department` (from core.Department)
- `accounts` (from accounting.Account)
- `journals` (from accounting.Journal)
- `journal_entries` (from accounting.JournalEntry)
- `customers` (from sales.Customer)
- `goodsreceipt` (from purchasing.GoodsReceipt)
- `supplierinvoice` (from purchasing.SupplierInvoice)
- `property` (from rent.Property)
- `rentalcontract` (from rent.RentalContract)
- `seedproductionorder` (from seed_production.SeedProductionOrder)
- `seedproductionlot` (from seed_production.SeedProductionLot)

---

### Company

**Table**: `core_company`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| code | CharField | Yes | - | No |
| description | TextField | Yes | - | No |
| address | TextField | Yes | - | No |
| phone | CharField | Yes | - | No |
| email | CharField | Yes | - | No |
| website | CharField | Yes | - | No |
| country | ForeignKey | Yes | - | Yes |
| tax_number | CharField | Yes | - | No |
| logo | FileField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `country` → core.Country

**Reverse Relations**:

- `branches` (from core.Branch)
- `department` (from core.Department)
- `apikeys` (from core.APIKey)
- `accounttypes` (from accounting.AccountType)
- `currencys` (from accounting.Currency)
- `accounts` (from accounting.Account)
- `fiscalyears` (from accounting.FiscalYear)
- `fiscalperiods` (from accounting.FiscalPeriod)
- `journals` (from accounting.Journal)
- `journalentrys` (from accounting.JournalEntry)
- `analyticaccounts` (from accounting.AnalyticAccount)
- `taxs` (from accounting.Tax)
- `customers` (from sales.Customer)
- `price_lists` (from sales.PriceList)
- `sales_orders` (from sales.SalesOrder)
- `sales_returns` (from sales.SalesReturn)
- `sales_teams` (from sales.SalesTeam)
- `sales_targets` (from sales.SalesTarget)
- `purchase_orders` (from purchasing.PurchaseOrder)
- `goodsreceipt` (from purchasing.GoodsReceipt)
- `purchase_returns` (from purchasing.PurchaseReturn)
- `supplierinvoice` (from purchasing.SupplierInvoice)
- `propertytype` (from rent.PropertyType)
- `propertyfeature` (from rent.PropertyFeature)
- `property` (from rent.Property)
- `company_rental_contracts` (from rent.RentalContract)
- `tenant_rental_contracts` (from rent.RentalContract)
- `leaseagreement` (from rent.LeaseAgreement)
- `maintenancerequest` (from rent.MaintenanceRequest)
- `vehicleleaseagreement` (from rent.VehicleLeaseAgreement)
- `pos_configs` (from pos.POSConfig)
- `production_lines` (from production.ProductionLine)
- `production_operations` (from production.ProductionOperation)
- `bill_of_materials` (from production.BillOfMaterials)
- `production_orders` (from production.ProductionOrder)
- `inventoryverifications` (from seed_production.InventoryVerification)
- `lotchangelogs` (from seed_production.LotChangeLog)
- `seedpackagings` (from seed_production.SeedPackaging)
- `seedproductionplans` (from seed_production.SeedProductionPlan)
- `seedtreatmentlogs` (from seed_production.SeedTreatmentLog)

---

### Country

**Table**: `core_country`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| is_active | BooleanField | No | True | No |

**Reverse Relations**:

- `company` (from core.Company)
- `branch` (from core.Branch)

---

### Currency

**Table**: `core_currency`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| symbol | CharField | No | - | No |
| exchange_rate | DecimalField | No | 1.0 | No |
| is_base | BooleanField | No | False | No |
| is_active | BooleanField | No | True | No |

**Reverse Relations**:

- `accounts` (from accounting.Account)

---

### Department

**Table**: `core_department`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| branch | ForeignKey | Yes | - | Yes |
| company | ForeignKey | No | - | Yes |
| parent_department | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `branch` → core.Branch
- `company` → core.Company
- `parent_department` → core.Department

**Reverse Relations**:

- `child_departments` (from core.Department)
- `accounts` (from accounting.Account)
- `journals` (from accounting.Journal)
- `journal_entries` (from accounting.JournalEntry)

**Unique Together**:

- (name, branch)
- (name, company)

---

### DocumentSequence

**Table**: `core_documentsequence`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| document_type | CharField | No | - | No |
| prefix | CharField | Yes | - | No |
| current_number | PositiveIntegerField | No | 1 | No |
| increment_by | PositiveIntegerField | No | 1 | No |
| is_active | BooleanField | No | True | No |

---

### RoleDatabasePermission

**Table**: `core_roledatabasepermission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| database_alias | CharField | No | - | No |
| can_access | BooleanField | No | True | No |

---

### SlugTestModel

**Table**: `core_slugtestmodel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| title | CharField | No | - | No |
| slug | SlugField | No | - | Yes |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |

---

### SystemSetting

**Table**: `core_systemsetting`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| key | CharField | No | - | No |
| value | TextField | No | - | No |
| description | TextField | Yes | - | No |

---

## custom_admin

### AdminNotification

**Table**: `custom_admin_adminnotification`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| message | TextField | No | - | No |
| notification_type | CharField | No | info | No |
| level | CharField | No | medium | No |
| link | CharField | No | - | No |
| is_read | BooleanField | No | False | No |
| user | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

---

### AIUsageReport

**Table**: `custom_admin_aiusagereport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| feature | CharField | No | - | No |
| tokens_used | PositiveIntegerField | No | 0 | No |
| cost | DecimalField | No | 0.0000 | No |
| request_data | JSONField | No | <class 'dict'> | No |
| response_data | JSONField | No | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

---

### AuditLog

**Table**: `custom_admin_auditlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | Yes | - | Yes |
| action | CharField | No | - | No |
| model_name | CharField | No | - | No |
| object_id | CharField | No | - | No |
| object_repr | CharField | No | - | No |
| changes | JSONField | No | <class 'dict'> | No |
| ip_address | GenericIPAddressField | Yes | - | No |
| user_agent | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

---

### BackupRecord

**Table**: `custom_admin_backuprecord`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| backup_type | CharField | No | full | No |
| file_path | CharField | No | - | No |
| file_size | PositiveBigIntegerField | Yes | - | No |
| status | CharField | No | pending | No |
| error_message | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| completed_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `restore_records` (from custom_admin.RestoreRecord)

---

### CustomMenu

**Table**: `custom_admin_custommenu`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| title | CharField | No | - | No |
| icon | CharField | No | - | No |
| parent | ForeignKey | Yes | - | Yes |
| url | CharField | No | - | No |
| order | PositiveSmallIntegerField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `parent` → custom_admin.CustomMenu
- `created_by` → users.User

**Reverse Relations**:

- `children` (from custom_admin.CustomMenu)

---

### CustomReport

**Table**: `custom_admin_customreport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| report_type | CharField | No | - | No |
| model_name | CharField | No | - | No |
| fields | JSONField | No | <class 'list'> | No |
| filters | JSONField | No | <class 'list'> | No |
| grouping | JSONField | No | <class 'list'> | No |
| sorting | JSONField | No | <class 'list'> | No |
| chart_config | JSONField | No | <class 'dict'> | No |
| is_public | BooleanField | No | False | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### CustomUIElement

**Table**: `custom_admin_customuielement`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| element_type | CharField | No | - | No |
| target_model | CharField | No | - | No |
| target_view | CharField | No | - | No |
| position | CharField | No | - | No |
| config | JSONField | No | <class 'dict'> | No |
| is_active | BooleanField | No | True | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### DashboardLayout

**Table**: `custom_admin_dashboardlayout`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| is_default | BooleanField | No | False | No |
| user | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

**Unique Together**:

- (name, user)

---

### DashboardWidget

**Table**: `custom_admin_dashboardwidget`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| title | CharField | No | - | No |
| widget_type | CharField | No | - | No |
| data_source | CharField | No | - | No |
| refresh_interval | PositiveIntegerField | No | 60 | No |
| position_x | PositiveSmallIntegerField | No | 0 | No |
| position_y | PositiveSmallIntegerField | No | 0 | No |
| width | PositiveSmallIntegerField | No | 1 | No |
| height | PositiveSmallIntegerField | No | 1 | No |
| is_visible | BooleanField | No | True | No |
| config | JSONField | No | <class 'dict'> | No |
| user | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

**Unique Together**:

- (name, user)

---

### RestoreRecord

**Table**: `custom_admin_restorerecord`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| backup | ForeignKey | No | - | Yes |
| description | TextField | No | - | No |
| status | CharField | No | pending | No |
| error_message | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| completed_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `backup` → custom_admin.BackupRecord
- `created_by` → users.User

---

### SystemAlert

**Table**: `custom_admin_systemalert`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| alert_type | CharField | No | - | No |
| severity | CharField | No | medium | No |
| is_resolved | BooleanField | No | False | No |
| resolved_by | ForeignKey | Yes | - | Yes |
| resolved_at | DateTimeField | Yes | - | No |
| metadata | JSONField | No | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `resolved_by` → users.User

---

### SystemSetting

**Table**: `custom_admin_systemsetting`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| key | CharField | No | - | No |
| value | TextField | No | - | No |
| data_type | CharField | No | string | No |
| setting_type | CharField | No | general | No |
| description | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### UserPreference

**Table**: `custom_admin_userpreference`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| key | CharField | No | - | No |
| value | TextField | No | - | No |
| data_type | CharField | No | string | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

**Unique Together**:

- (user, key)

---

## dashboard

### UserDashboardSettings

**Table**: `dashboard_userdashboardsettings`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | OneToOneField | No | - | Yes |
| widget_config | JSONField | No | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `user` (from users.User)

---

## database_management

### BackupLog

**Table**: `database_management_backuplog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| backup_type | CharField | No | full | No |
| backup_method | CharField | No | manual | No |
| status | CharField | No | pending | Yes |
| database_name | CharField | No | - | No |
| compression | CharField | No | gzip | No |
| started_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| completed_at | DateTimeField | Yes | - | No |
| duration_seconds | PositiveIntegerField | Yes | - | No |
| file_path | CharField | Yes | - | No |
| file_size | BigIntegerField | Yes | - | No |
| message | TextField | No | - | No |
| is_encrypted | BooleanField | No | False | No |
| retention_days | PositiveIntegerField | No | 30 | No |
| expiry_date | DateField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `restore_logs` (from database_management.RestoreLog)

**Indexes**:

- database_ma_status_f1faac_idx: (status)
- database_ma_started_06d988_idx: (-started_at)
- database_ma_databas_616b59_idx: (database_name)
- database_ma_expiry__2f5f2c_idx: (expiry_date)

---

### BackupSchedule

**Table**: `database_management_backupschedule`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| database_connection | ForeignKey | No | - | Yes |
| backup_type | CharField | No | full | No |
| frequency | CharField | No | daily | No |
| hour | PositiveSmallIntegerField | No | 0 | No |
| minute | PositiveSmallIntegerField | No | 0 | No |
| day_of_week | PositiveSmallIntegerField | Yes | - | No |
| day_of_month | PositiveSmallIntegerField | Yes | - | No |
| cron_expression | CharField | No | - | No |
| retention_days | PositiveIntegerField | No | 30 | No |
| compression | CharField | No | gzip | No |
| is_active | BooleanField | No | True | No |
| last_run | DateTimeField | Yes | - | No |
| next_run | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `database_connection` → database_management.DatabaseConnectionSettings
- `created_by` → users.User

**Indexes**:

- database_ma_frequen_b0f7b8_idx: (frequency)
- database_ma_is_acti_93a7ed_idx: (is_active)
- database_ma_next_ru_f2c9f9_idx: (next_run)

---

### DatabaseConnectionSettings

**Table**: `database_management_databaseconnectionsettings`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| engine | CharField | No | - | No |
| engine_custom | CharField | No | - | No |
| db_name | CharField | No | - | No |
| user | CharField | No | - | No |
| password | CharField | No | - | No |
| host | CharField | No | - | No |
| port | CharField | No | - | No |
| options | JSONField | No | <class 'dict'> | No |
| is_active | BooleanField | No | True | No |
| is_default | BooleanField | No | False | No |
| allow_backup | BooleanField | No | True | No |
| allow_restore | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `backup_schedules` (from database_management.BackupSchedule)

---

### RestoreLog

**Table**: `database_management_restorelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| source_backup | ForeignKey | No | - | Yes |
| restore_method | CharField | No | manual | No |
| status | CharField | No | pending | Yes |
| target_database | CharField | No | - | No |
| started_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| completed_at | DateTimeField | Yes | - | No |
| duration_seconds | PositiveIntegerField | Yes | - | No |
| message | TextField | No | - | No |
| is_overwrite | BooleanField | No | False | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `source_backup` → database_management.BackupLog
- `created_by` → users.User

**Indexes**:

- database_ma_status_78832a_idx: (status)
- database_ma_started_71641c_idx: (-started_at)
- database_ma_target__6fc63d_idx: (target_database)

---

## database_optimization

### DatabaseHealth

**Table**: `database_optimization_databasehealth`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| database_name | CharField | No | default | No |
| total_size_bytes | BigIntegerField | No | - | No |
| table_count | PositiveIntegerField | No | - | No |
| index_count | PositiveIntegerField | No | - | No |
| avg_query_time | FloatField | No | - | No |
| slow_query_count | PositiveIntegerField | No | - | No |
| unused_index_count | PositiveIntegerField | No | - | No |
| cache_hit_ratio | FloatField | No | - | No |
| connection_count | PositiveIntegerField | No | - | No |
| health_score | FloatField | No | - | No |
| health_status | CharField | No | - | No |
| recommendations | JSONField | No | <class 'list'> | No |
| timestamp | DateTimeField | No | - | No |

---

### DatabaseIndex

**Table**: `database_optimization_databaseindex`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| table_name | CharField | No | - | No |
| index_name | CharField | No | - | No |
| index_type | CharField | No | btree | No |
| columns | JSONField | No | - | No |
| is_unique | BooleanField | No | False | No |
| condition | TextField | Yes | - | No |
| size_bytes | BigIntegerField | No | 0 | No |
| usage_count | PositiveIntegerField | No | 0 | No |
| last_used | DateTimeField | Yes | - | No |
| status | CharField | No | active | No |
| performance_impact | FloatField | No | 0.0 | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Indexes**:

- database_op_table_n_c26458_idx: (table_name)
- database_op_status_1facae_idx: (status)
- database_op_usage_c_1961e7_idx: (usage_count)

**Unique Together**:

- (table_name, index_name)

---

### DatabaseMetric

**Table**: `database_optimization_databasemetric`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| metric_type | CharField | No | - | No |
| table_name | CharField | Yes | - | No |
| query_hash | CharField | Yes | - | No |
| value | FloatField | No | - | No |
| unit | CharField | No | ms | No |
| metadata | JSONField | No | <class 'dict'> | No |
| timestamp | DateTimeField | No | - | No |

**Indexes**:

- database_op_metric__d874f2_idx: (metric_type, timestamp)
- database_op_table_n_c2949e_idx: (table_name, timestamp)
- database_op_query_h_0b3f35_idx: (query_hash)

---

### QueryOptimization

**Table**: `database_optimization_queryoptimization`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| slow_query | ForeignKey | No | - | Yes |
| optimization_type | CharField | No | - | No |
| description | TextField | No | - | No |
| sql_before | TextField | No | - | No |
| sql_after | TextField | Yes | - | No |
| expected_improvement | FloatField | No | - | No |
| actual_improvement | FloatField | Yes | - | No |
| status | CharField | No | pending | No |
| applied_by | ForeignKey | Yes | - | Yes |
| applied_at | DateTimeField | Yes | - | No |
| notes | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `slow_query` → database_optimization.SlowQuery
- `applied_by` → users.User

---

### SlowQuery

**Table**: `database_optimization_slowquery`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| query_hash | CharField | No | - | No |
| query_text | TextField | No | - | No |
| execution_time | FloatField | No | - | No |
| execution_count | PositiveIntegerField | No | 1 | No |
| avg_execution_time | FloatField | No | - | No |
| max_execution_time | FloatField | No | - | No |
| affected_tables | JSONField | No | <class 'list'> | No |
| optimization_suggestions | JSONField | No | <class 'list'> | No |
| is_optimized | BooleanField | No | False | No |
| first_seen | DateTimeField | No | - | No |
| last_seen | DateTimeField | No | - | No |

**Reverse Relations**:

- `queryoptimization` (from database_optimization.QueryOptimization)

**Indexes**:

- database_op_executi_ae986f_idx: (execution_time)
- database_op_avg_exe_95c734_idx: (avg_execution_time)
- database_op_is_opti_6118d8_idx: (is_optimized)

---

## django_celery_beat

### ClockedSchedule

**Table**: `django_celery_beat_clockedschedule`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| clocked_time | DateTimeField | No | - | No |

**Reverse Relations**:

- `periodictask` (from django_celery_beat.PeriodicTask)

---

### CrontabSchedule

**Table**: `django_celery_beat_crontabschedule`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| minute | CharField | No | * | No |
| hour | CharField | No | * | No |
| day_of_month | CharField | No | * | No |
| month_of_year | CharField | No | * | No |
| day_of_week | CharField | No | * | No |
| timezone | CharField | No | <function crontab_schedule_celery_timezone at 0x00000247D573BD80> | No |

**Reverse Relations**:

- `periodictask` (from django_celery_beat.PeriodicTask)

---

### IntervalSchedule

**Table**: `django_celery_beat_intervalschedule`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| every | IntegerField | No | - | No |
| period | CharField | No | - | No |

**Reverse Relations**:

- `periodictask` (from django_celery_beat.PeriodicTask)

---

### PeriodicTask

**Table**: `django_celery_beat_periodictask`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| name | CharField | No | - | No |
| task | CharField | No | - | No |
| interval | ForeignKey | Yes | - | Yes |
| crontab | ForeignKey | Yes | - | Yes |
| solar | ForeignKey | Yes | - | Yes |
| clocked | ForeignKey | Yes | - | Yes |
| args | TextField | No | [] | No |
| kwargs | TextField | No | {} | No |
| queue | CharField | Yes | None | No |
| exchange | CharField | Yes | None | No |
| routing_key | CharField | Yes | None | No |
| headers | TextField | No | {} | No |
| priority | PositiveIntegerField | Yes | None | No |
| expires | DateTimeField | Yes | - | No |
| expire_seconds | PositiveIntegerField | Yes | - | No |
| one_off | BooleanField | No | False | No |
| start_time | DateTimeField | Yes | - | No |
| enabled | BooleanField | No | True | No |
| last_run_at | DateTimeField | Yes | - | No |
| total_run_count | PositiveIntegerField | No | 0 | No |
| date_changed | DateTimeField | No | - | No |
| description | TextField | No | - | No |

**Foreign Keys**:

- `interval` → django_celery_beat.IntervalSchedule
- `crontab` → django_celery_beat.CrontabSchedule
- `solar` → django_celery_beat.SolarSchedule
- `clocked` → django_celery_beat.ClockedSchedule

---

### PeriodicTasks

**Table**: `django_celery_beat_periodictasks`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| ident | SmallIntegerField | No | 1 | No |
| last_update | DateTimeField | No | - | No |

---

### SolarSchedule

**Table**: `django_celery_beat_solarschedule`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | AutoField | No | - | No |
| event | CharField | No | - | No |
| latitude | DecimalField | No | - | No |
| longitude | DecimalField | No | - | No |

**Reverse Relations**:

- `periodictask` (from django_celery_beat.PeriodicTask)

**Unique Together**:

- (event, latitude, longitude)

---

## email_messaging

### EmailCampaign

**Table**: `email_messaging_emailcampaign`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| campaign_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| provider | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| subject | CharField | No | - | No |
| content | TextField | No | - | No |
| sender_name | CharField | No | - | No |
| sender_email | CharField | No | - | No |
| reply_to | CharField | No | - | No |
| recipient_list | JSONField | No | <class 'list'> | No |
| status | CharField | No | draft | No |
| scheduled_time | DateTimeField | Yes | - | No |
| sent_time | DateTimeField | Yes | - | No |
| total_recipients | PositiveIntegerField | No | 0 | No |
| emails_sent | PositiveIntegerField | No | 0 | No |
| emails_delivered | PositiveIntegerField | No | 0 | No |
| emails_opened | PositiveIntegerField | No | 0 | No |
| links_clicked | PositiveIntegerField | No | 0 | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `provider` → email_messaging.EmailProvider
- `created_by` → users.User

---

### EmailProvider

**Table**: `email_messaging_emailprovider`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| provider_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| provider_type | CharField | No | - | No |
| smtp_host | CharField | No | - | No |
| smtp_port | PositiveIntegerField | No | 587 | No |
| smtp_username | CharField | No | - | No |
| smtp_password | CharField | No | - | No |
| use_tls | BooleanField | No | True | No |
| api_key | CharField | No | - | No |
| api_secret | CharField | No | - | No |
| emails_sent | PositiveIntegerField | No | 0 | No |
| emails_delivered | PositiveIntegerField | No | 0 | No |
| emails_bounced | PositiveIntegerField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| is_default | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `campaigns` (from email_messaging.EmailCampaign)

---

### SMSProvider

**Table**: `email_messaging_smsprovider`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| provider_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| provider_type | CharField | No | - | No |
| api_key | CharField | No | - | No |
| api_secret | CharField | No | - | No |
| sender_id | CharField | No | - | No |
| sms_sent | PositiveIntegerField | No | 0 | No |
| sms_delivered | PositiveIntegerField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

## experiments

### Experiment

**Table**: `experiments_experiment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| code | CharField | No | - | No |
| location | ForeignKey | No | - | Yes |
| season | ForeignKey | No | - | Yes |
| start_date | DateField | No | - | No |
| end_date | DateField | No | - | No |

**Foreign Keys**:

- `location` → experiments.Location
- `season` → experiments.Season

**Reverse Relations**:

- `experimentvariety` (from experiments.ExperimentVariety)
- `fertilizationprogram` (from experiments.FertilizationProgram)
- `pesticideprogram` (from experiments.PesticideProgram)
- `experimentcost` (from experiments.ExperimentCost)
- `varietypricerecommendation` (from experiments.VarietyPriceRecommendation)

---

### ExperimentCost

**Table**: `experiments_experimentcost`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| cost_type | CharField | No | - | No |
| description | TextField | No | - | No |
| amount | DecimalField | No | - | No |
| date_incurred | DateField | No | - | No |

**Foreign Keys**:

- `experiment` → experiments.Experiment

---

### ExperimentVariety

**Table**: `experiments_experimentvariety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| variety | ForeignKey | No | - | Yes |
| entry_number | PositiveIntegerField | No | - | No |
| planting_date | DateField | No | - | No |

**Foreign Keys**:

- `experiment` → experiments.Experiment
- `variety` → experiments.Variety

**Reverse Relations**:

- `harvest` (from experiments.Harvest)
- `varietyevaluation` (from experiments.VarietyEvaluation)

**Unique Together**:

- (experiment, variety)
- (experiment, entry_number)

---

### FertilizationApplication

**Table**: `experiments_fertilizationapplication`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| program | ForeignKey | No | - | Yes |
| application_date | DateField | No | - | No |
| fertilizer_name | CharField | No | - | No |
| fertilizer_type | CharField | No | - | No |
| quantity | DecimalField | No | - | No |
| unit | CharField | No | - | No |
| application_method | CharField | No | - | No |
| cost | DecimalField | No | - | No |

**Foreign Keys**:

- `program` → experiments.FertilizationProgram

---

### FertilizationProgram

**Table**: `experiments_fertilizationprogram`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| description | TextField | No | - | No |

**Foreign Keys**:

- `experiment` → experiments.Experiment

**Reverse Relations**:

- `fertilizationapplication` (from experiments.FertilizationApplication)

---

### Harvest

**Table**: `experiments_harvest`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment_variety | ForeignKey | No | - | Yes |
| harvest_number | PositiveIntegerField | No | - | No |
| harvest_date | DateField | No | - | No |
| fruit_count | PositiveIntegerField | No | - | No |
| fruit_weight | DecimalField | No | - | No |

**Foreign Keys**:

- `experiment_variety` → experiments.ExperimentVariety

**Reverse Relations**:

- `harvestqualitygrade` (from experiments.HarvestQualityGrade)

**Unique Together**:

- (experiment_variety, harvest_number)

---

### HarvestQualityGrade

**Table**: `experiments_harvestqualitygrade`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| harvest | ForeignKey | No | - | Yes |
| grade | CharField | No | - | No |
| fruit_count | PositiveIntegerField | No | - | No |
| fruit_weight | DecimalField | No | - | No |

**Foreign Keys**:

- `harvest` → experiments.Harvest

**Unique Together**:

- (harvest, grade)

---

### Location

**Table**: `experiments_location`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |

**Reverse Relations**:

- `experiment` (from experiments.Experiment)

---

### PesticideApplication

**Table**: `experiments_pesticideapplication`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| program | ForeignKey | No | - | Yes |
| application_date | DateField | No | - | No |
| pesticide_name | CharField | No | - | No |
| pesticide_type | CharField | No | - | No |
| target_pest | CharField | No | - | No |
| quantity | DecimalField | No | - | No |
| unit | CharField | No | - | No |
| application_method | CharField | No | - | No |
| cost | DecimalField | No | - | No |

**Foreign Keys**:

- `program` → experiments.PesticideProgram

---

### PesticideProgram

**Table**: `experiments_pesticideprogram`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| description | TextField | No | - | No |

**Foreign Keys**:

- `experiment` → experiments.Experiment

**Reverse Relations**:

- `pesticideapplication` (from experiments.PesticideApplication)

---

### Season

**Table**: `experiments_season`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| start_date | DateField | No | - | No |
| end_date | DateField | No | - | No |

**Reverse Relations**:

- `experiment` (from experiments.Experiment)

---

### Variety

**Table**: `experiments_variety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| variety_type | ForeignKey | No | - | Yes |

**Foreign Keys**:

- `variety_type` → experiments.VarietyType

**Reverse Relations**:

- `experimentvariety` (from experiments.ExperimentVariety)
- `varietypricerecommendation` (from experiments.VarietyPriceRecommendation)

---

### VarietyEvaluation

**Table**: `experiments_varietyevaluation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment_variety | ForeignKey | No | - | Yes |
| evaluation_date | DateField | No | - | No |
| fruit_length | PositiveSmallIntegerField | No | 3 | No |
| fruit_shape_regularity | PositiveSmallIntegerField | No | 3 | No |
| fruit_deformity_rate | PositiveSmallIntegerField | No | 3 | No |
| fruit_firmness | PositiveSmallIntegerField | No | 3 | No |
| fruit_color | PositiveSmallIntegerField | No | 3 | No |
| storage_ability | PositiveSmallIntegerField | No | 3 | No |
| transport_ability | PositiveSmallIntegerField | No | 3 | No |
| earliness | PositiveSmallIntegerField | No | 3 | No |
| leaf_shape | PositiveSmallIntegerField | No | 3 | No |
| fruit_coverage | PositiveSmallIntegerField | No | 3 | No |
| fungal_resistance | PositiveSmallIntegerField | No | 3 | No |
| bacterial_resistance | PositiveSmallIntegerField | No | 3 | No |
| insect_resistance | PositiveSmallIntegerField | No | 3 | No |
| viral_resistance | PositiveSmallIntegerField | No | 3 | No |
| cold_tolerance | PositiveSmallIntegerField | No | 3 | No |
| heat_tolerance | PositiveSmallIntegerField | No | 3 | No |
| soil_salinity_tolerance | PositiveSmallIntegerField | No | 3 | No |
| water_salinity_tolerance | PositiveSmallIntegerField | No | 3 | No |
| drought_tolerance | PositiveSmallIntegerField | No | 3 | No |
| strengths | TextField | No |  | No |
| weaknesses | TextField | No |  | No |
| notes | TextField | No |  | No |

**Foreign Keys**:

- `experiment_variety` → experiments.ExperimentVariety

---

### VarietyPriceRecommendation

**Table**: `experiments_varietypricerecommendation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| variety | ForeignKey | No | - | Yes |
| experiment | ForeignKey | No | - | Yes |
| competitor_price | DecimalField | Yes | - | No |
| recommended_price | DecimalField | No | - | No |
| justification | TextField | No | - | No |

**Foreign Keys**:

- `variety` → experiments.Variety
- `experiment` → experiments.Experiment

---

### VarietyType

**Table**: `experiments_varietytype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |

**Reverse Relations**:

- `variety` (from experiments.Variety)

---

## farms

### AgriculturalActivity

**Table**: `farms_agriculturalactivity`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| planting_season | ForeignKey | No | - | Yes |
| activity_type | ForeignKey | No | - | Yes |
| activity_date | DateField | No | - | No |
| description | TextField | Yes | - | No |
| cost | DecimalField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `planting_season` → farms.PlantingSeason
- `activity_type` → farms.AgriculturalActivityType

**Reverse Relations**:

- `resources` (from farms.FarmResource)
- `worker_logs` (from farms.FarmWorkerLog)
- `equipment_logs` (from farms.FarmEquipmentLog)

---

### AgriculturalActivityType

**Table**: `farms_agriculturalactivitytype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |

**Reverse Relations**:

- `activities` (from farms.AgriculturalActivity)

---

### Crop

**Table**: `farms_crop`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| scientific_name | CharField | Yes | - | No |
| crop_type | CharField | No | - | No |
| growing_season | CharField | Yes | - | No |
| description | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `varieties` (from farms.CropVariety)
- `planting_seasons` (from farms.PlantingSeason)

---

### CropVariety

**Table**: `farms_cropvariety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| crop | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| description | TextField | Yes | - | No |
| maturity_days | PositiveIntegerField | Yes | - | No |
| yield_potential | CharField | Yes | - | No |
| disease_resistance | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `crop` → farms.Crop

**Reverse Relations**:

- `plantings` (from farms.Planting)

**Unique Together**:

- (crop, code)

---

### Equipment

**Table**: `farms_equipment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| equipment_type | CharField | No | - | No |
| model | CharField | Yes | - | No |
| serial_number | CharField | Yes | - | No |
| purchase_date | DateField | Yes | - | No |
| purchase_cost | DecimalField | Yes | - | No |
| status | CharField | No | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm

**Reverse Relations**:

- `maintenance_records` (from farms.EquipmentMaintenance)

---

### EquipmentMaintenance

**Table**: `farms_equipmentmaintenance`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| equipment | ForeignKey | No | - | Yes |
| maintenance_date | DateField | No | - | No |
| maintenance_type | CharField | No | - | No |
| description | TextField | No | - | No |
| cost | DecimalField | No | - | No |
| performed_by | CharField | No | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `equipment` → farms.Equipment

---

### Farm

**Table**: `farms_farm`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| location | TextField | No | - | No |
| gps_coordinates | CharField | Yes | - | No |
| total_area | DecimalField | No | - | No |
| cultivated_area | DecimalField | No | - | No |
| farm_type | CharField | No | - | No |
| description | TextField | Yes | - | No |
| manager | ForeignKey | Yes | - | Yes |
| establishment_date | DateField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `manager` → users.User

**Reverse Relations**:

- `productionorder` (from agricultural_production.ProductionOrder)
- `sections` (from farms.FarmSection)
- `farm_plots` (from farms.FarmPlot)
- `activities` (from farms.FarmActivity)
- `equipment` (from farms.Equipment)
- `fields` (from farms.Field)
- `crop_data` (from ai_agriculture.AgriCropData)
- `soil_analyses` (from ai_agriculture.SoilAnalysis)
- `crop_analyses` (from ai_agriculture.CropAnalysis)
- `crop_predictions` (from ai_agriculture.CropPrediction)
- `yield_predictions` (from ai_agriculture.YieldPrediction)
- `ai_recommendations` (from ai_agriculture.AgriRecommendation)

---

### FarmActivity

**Table**: `farms_farmactivity`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| planting | ForeignKey | Yes | - | Yes |
| activity_type | CharField | No | - | No |
| date | DateField | No | - | No |
| description | TextField | No | - | No |
| performed_by | ForeignKey | Yes | - | Yes |
| cost | DecimalField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm
- `planting` → farms.Planting
- `performed_by` → users.User

---

### FarmEquipmentLog

**Table**: `farms_farmequipmentlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| activity | ForeignKey | No | - | Yes |
| log_date | DateField | No | - | No |
| cost | DecimalField | Yes | - | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `activity` → farms.AgriculturalActivity

---

### FarmPlot

**Table**: `farms_farmplot`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | Yes | - | Yes |
| name | CharField | No | - | No |
| area | DecimalField | Yes | - | No |
| soil_type | CharField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm

---

### FarmResource

**Table**: `farms_farmresource`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| activity | ForeignKey | No | - | Yes |
| product_name_temp | CharField | No | - | No |
| quantity_used | DecimalField | No | - | No |
| unit_of_measure | CharField | No | - | No |
| cost_per_unit | DecimalField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `activity` → farms.AgriculturalActivity

---

### FarmSection

**Table**: `farms_farmsection`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| section_type | CharField | No | - | No |
| area | DecimalField | No | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm

**Reverse Relations**:

- `plots` (from farms.Plot)

**Unique Together**:

- (farm, code)

---

### FarmWorkerLog

**Table**: `farms_farmworkerlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| activity | ForeignKey | No | - | Yes |
| log_date | DateField | No | - | No |
| cost | DecimalField | Yes | - | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `activity` → farms.AgriculturalActivity

---

### Field

**Table**: `farms_field`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| area | DecimalField | No | - | No |
| description | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm` → farms.Farm

**Reverse Relations**:

- `planting_seasons` (from farms.PlantingSeason)

---

### Harvest

**Table**: `farms_harvest`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| planting | ForeignKey | No | - | Yes |
| harvest_date | DateField | No | - | No |
| quantity | DecimalField | No | - | No |
| unit | CharField | No | - | No |
| quality_grade | CharField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `planting` → farms.Planting

---

### Planting

**Table**: `farms_planting`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| plot | ForeignKey | No | - | Yes |
| crop_variety | ForeignKey | No | - | Yes |
| planting_date | DateField | No | - | No |
| expected_harvest_date | DateField | Yes | - | No |
| actual_harvest_date | DateField | Yes | - | No |
| planting_method | CharField | No | - | No |
| plant_spacing | DecimalField | Yes | - | No |
| row_spacing | DecimalField | Yes | - | No |
| seed_rate | DecimalField | Yes | - | No |
| status | CharField | No | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `plot` → farms.Plot
- `crop_variety` → farms.CropVariety

**Reverse Relations**:

- `activities` (from farms.FarmActivity)
- `harvests` (from farms.Harvest)

---

### PlantingSeason

**Table**: `farms_plantingseason`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| field | ForeignKey | No | - | Yes |
| crop | ForeignKey | No | - | Yes |
| start_date | DateField | No | - | No |
| expected_harvest_date | DateField | Yes | - | No |
| actual_harvest_date | DateField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `field` → farms.Field
- `crop` → farms.Crop

**Reverse Relations**:

- `activities` (from farms.AgriculturalActivity)

---

### Plot

**Table**: `farms_plot`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| farm_section | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| area | DecimalField | No | - | No |
| soil_type | CharField | Yes | - | No |
| irrigation_type | CharField | Yes | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `farm_section` → farms.FarmSection

**Reverse Relations**:

- `plantings` (from farms.Planting)

**Unique Together**:

- (farm_section, code)

---

## forecast

### ForecastDataSource

**Table**: `forecast_forecastdatasource`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| source_type | CharField | No | database | No |
| connection_params | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| refresh_frequency | CharField | No | daily | No |
| last_refresh | DateTimeField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### ForecastModel

**Table**: `forecast_forecastmodel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| model_type | CharField | No | linear | No |
| parameters | TextField | No | - | No |
| target_entity | CharField | No | sales | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| version | PositiveIntegerField | No | 1 | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `results` (from forecast.ForecastResult)

**Indexes**:

- forecast_fo_model_t_4d0ff0_idx: (model_type)
- forecast_fo_target__b6b145_idx: (target_entity)

---

### ForecastPeriod

**Table**: `forecast_forecastperiod`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| start_date | DateField | No | - | No |
| end_date | DateField | No | - | No |
| period_type | CharField | No | monthly | No |
| description | TextField | No | - | No |

**Reverse Relations**:

- `results` (from forecast.ForecastResult)

---

### ForecastResult

**Table**: `forecast_forecastresult`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| forecast_model | ForeignKey | No | - | Yes |
| period | ForeignKey | No | - | Yes |
| result_data | TextField | No | - | No |
| accuracy | FloatField | Yes | - | No |
| status | CharField | No | draft | No |
| notes | TextField | No | - | No |
| error_message | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `forecast_model` → forecast.ForecastModel
- `period` → forecast.ForecastPeriod
- `created_by` → users.User

**Indexes**:

- forecast_fo_status_66773d_idx: (status)
- forecast_fo_created_bbc384_idx: (created_at)

**Unique Together**:

- (forecast_model, period)

---

## health_monitoring

### ServerMetric

**Table**: `health_monitoring_servermetric`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | Yes |
| cpu_percent | FloatField | No | - | No |
| memory_percent | FloatField | No | - | No |
| disk_usage_percent | FloatField | No | - | No |

---

### SystemEventLog

**Table**: `health_monitoring_systemeventlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | Yes |
| level | CharField | No | - | No |
| source_module | CharField | No | - | No |
| message | TextField | No | - | No |
| details | JSONField | Yes | - | No |

---

### UserActivityLog

**Table**: `health_monitoring_useractivitylog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| activity_type | CharField | No | - | No |

**Foreign Keys**:

- `user` → users.User

---

## intelligent_assistant

### AIAnalytics

**Table**: `intelligent_assistant_aianalytics`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| date | DateField | No | - | No |
| metric_type | CharField | No | - | No |
| ai_model | ForeignKey | Yes | - | Yes |
| user | ForeignKey | Yes | - | Yes |
| value | FloatField | No | - | No |
| unit | CharField | No | count | No |
| metadata | JSONField | No | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `ai_model` → ai_models.AIModel
- `user` → users.User

**Indexes**:

- intelligent_date_a0c89e_idx: (date, metric_type)
- intelligent_ai_mode_245f93_idx: (ai_model, date)

**Unique Together**:

- (date, metric_type, ai_model, user)

---

### AIInsight

**Table**: `intelligent_assistant_aiinsight`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| insight_type | CharField | No | - | No |
| priority | CharField | No | medium | No |
| confidence_score | FloatField | No | - | No |
| data_source | CharField | No | - | No |
| analysis_data | JSONField | No | <class 'dict'> | No |
| recommendations | JSONField | No | <class 'list'> | No |
| impact_estimate | TextField | No | - | No |
| content_type | ForeignKey | Yes | - | Yes |
| object_id | PositiveIntegerField | Yes | - | No |
| status | CharField | No | new | No |
| assigned_to | ForeignKey | Yes | - | Yes |
| tags | JSONField | No | <class 'list'> | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| related_object | GenericForeignKey | No | - | No |

**Foreign Keys**:

- `content_type` → contenttypes.ContentType
- `assigned_to` → users.User

**Indexes**:

- intelligent_insight_da1874_idx: (insight_type, priority)
- intelligent_status_0626d3_idx: (status, created_at)
- intelligent_confide_f3bde5_idx: (confidence_score)

---

### AssistantConfiguration

**Table**: `intelligent_assistant_assistantconfiguration`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| is_default | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### Conversation

**Table**: `intelligent_assistant_conversation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| user | ForeignKey | No | - | Yes |
| title | CharField | No | - | No |
| conversation_type | CharField | No | chat | No |
| ai_model | ForeignKey | Yes | - | Yes |
| context_data | JSONField | No | <class 'dict'> | No |
| status | CharField | No | active | No |
| message_count | PositiveIntegerField | No | 0 | No |
| total_tokens | PositiveIntegerField | No | 0 | No |
| satisfaction_rating | PositiveSmallIntegerField | Yes | - | No |
| tags | JSONField | No | <class 'list'> | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User
- `ai_model` → ai_models.AIModel

**Reverse Relations**:

- `messages` (from intelligent_assistant.Message)

**Indexes**:

- intelligent_user_id_847f90_idx: (user, conversation_type)
- intelligent_status_7f819e_idx: (status, created_at)

---

### KnowledgeBase

**Table**: `intelligent_assistant_knowledgebase`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| content | TextField | No | - | No |
| content_type | CharField | No | - | No |
| keywords | JSONField | No | <class 'list'> | No |
| embedding_vector | JSONField | Yes | - | No |
| relevance_score | FloatField | No | 0.0 | No |
| usage_count | PositiveIntegerField | No | 0 | No |
| status | CharField | No | draft | No |
| author | ForeignKey | Yes | - | Yes |
| tags | JSONField | No | <class 'list'> | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `author` → users.User

**Indexes**:

- intelligent_content_3e316e_idx: (content_type, status)
- intelligent_relevan_92ee6f_idx: (relevance_score)

---

### Message

**Table**: `intelligent_assistant_message`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| conversation | ForeignKey | No | - | Yes |
| message_type | CharField | No | - | No |
| content | TextField | No | - | No |
| metadata | JSONField | No | <class 'dict'> | No |
| token_count | PositiveIntegerField | No | 0 | No |
| response_time | FloatField | Yes | - | No |
| confidence_score | FloatField | Yes | - | No |
| is_helpful | BooleanField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `conversation` → intelligent_assistant.Conversation

**Indexes**:

- intelligent_convers_9e4dde_idx: (conversation, created_at)
- intelligent_message_4dbcd4_idx: (message_type)

---

### UserPreference

**Table**: `intelligent_assistant_userpreference`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | OneToOneField | No | - | Yes |
| preferred_ai_model | ForeignKey | Yes | - | Yes |
| communication_style | CharField | No | casual | No |
| language_preference | CharField | No | ar | No |
| notification_preferences | JSONField | No | <class 'dict'> | No |
| privacy_settings | JSONField | No | <class 'dict'> | No |
| custom_instructions | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `preferred_ai_model` → ai_models.AIModel

**Reverse Relations**:

- `user` (from users.User)

---

## internal_diagnosis_module

### DiagnosisResult

**Table**: `internal_diagnosis_module_diagnosisresult`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| session | ForeignKey | No | - | Yes |
| component | CharField | No | - | No |
| check_name | CharField | No | - | No |
| severity | CharField | No | info | No |
| message | TextField | No | - | No |
| details | JSONField | Yes | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |

**Foreign Keys**:

- `session` → internal_diagnosis_module.DiagnosisSession

---

### DiagnosisSession

**Table**: `internal_diagnosis_module_diagnosissession`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| session_id | CharField | No | - | No |
| status | CharField | No | pending | No |
| started_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| completed_at | DateTimeField | Yes | - | No |
| initiated_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `initiated_by` → users.User

**Reverse Relations**:

- `results` (from internal_diagnosis_module.DiagnosisResult)

---

## inventory

### InventoryAdjustment

**Table**: `inventory_inventoryadjustment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| adjustment_type | CharField | No | - | No |
| quantity | DecimalField | No | - | No |
| reason | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### Lot

**Table**: `inventory_lot`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| product | ForeignKey | Yes | - | Yes |
| name | CharField | No | LOT-UNKNOWN | No |
| quantity | DecimalField | No | 0 | No |
| expiration_date | DateField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `product` → inventory.Product

**Reverse Relations**:

- `stock_moves` (from inventory.StockMove)
- `seed_movements` (from seed_production.SeedInventoryMovement)

---

### LotBatch

**Table**: `inventory_lotbatch`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| batch_number | CharField | No | - | No |
| quantity | DecimalField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### Product

**Table**: `inventory_product`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| sku | CharField | No | - | No |
| description | TextField | Yes | - | No |
| barcode | CharField | Yes | - | No |
| category | ForeignKey | Yes | - | Yes |
| product_type | CharField | No | storable | No |
| tracking_type | CharField | No | none | No |
| sale_price | DecimalField | No | 0.00 | No |
| list_price | DecimalField | No | 0.00 | No |
| cost_price | DecimalField | No | 0.00 | No |
| quantity_on_hand | DecimalField | No | 0.00 | No |
| is_active | BooleanField | No | True | No |
| can_be_sold | BooleanField | No | True | No |
| can_be_purchased | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `category` → inventory.ProductCategory

**Reverse Relations**:

- `lots` (from inventory.Lot)
- `stocks` (from inventory.Stock)
- `stock_moves` (from inventory.StockMove)
- `price_list_items` (from sales.PriceListItem)
- `sales_return_lines` (from sales.SalesReturnLine)
- `purchase_order_lines` (from purchasing.PurchaseOrderLine)
- `goodsreceiptitem` (from purchasing.GoodsReceiptItem)
- `purchase_return_lines` (from purchasing.PurchaseReturnLine)
- `pos_order_lines` (from pos.POSOrderLine)
- `bill_of_materials` (from production.BillOfMaterials)
- `bom_items` (from production.BOMItem)
- `production_orders` (from production.ProductionOrder)
- `production_order_items` (from production.ProductionOrderItem)
- `production_outputs` (from production.ProductionOutput)
- `production_wastes` (from production.ProductionWaste)
- `variety_seeds` (from agricultural_experiments.Variety)
- `seed_production_orders` (from seed_production.SeedProductionOrder)
- `seed_production_lots` (from seed_production.SeedProductionLot)
- `knowledge_entries` (from ai.AIKnowledgeEntry)

---

### ProductCategory

**Table**: `inventory_productcategory`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| parent | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `parent` → inventory.ProductCategory

**Reverse Relations**:

- `children` (from inventory.ProductCategory)
- `products` (from inventory.Product)

---

### Stock

**Table**: `inventory_stock`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| product | ForeignKey | No | - | Yes |
| store | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | 0 | No |
| reserved_quantity | DecimalField | No | 0 | No |
| location | CharField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `product` → inventory.Product
- `store` → inventory.Store

**Indexes**:

- idx_stock_product: (product)
- idx_stock_store: (store)
- idx_stock_created: (created_at)

**Unique Together**:

- (product, store)

---

### StockLocation

**Table**: `inventory_stocklocation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### StockMove

**Table**: `inventory_stockmove`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| product | ForeignKey | No | - | Yes |
| store | ForeignKey | No | - | Yes |
| lot | ForeignKey | Yes | - | Yes |
| uom | ForeignKey | Yes | - | Yes |
| quantity | DecimalField | No | - | No |
| unit_cost | DecimalField | Yes | - | No |
| move_type | CharField | No | - | No |
| reference | CharField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `product` → inventory.Product
- `store` → inventory.Store
- `lot` → inventory.Lot
- `uom` → inventory.UoM

**Indexes**:

- idx_move_prod_store_created: (product, store, created_at)
- idx_move_store_created: (store, created_at)
- idx_move_prod_created: (product, created_at)
- idx_move_type: (move_type)

---

### Store

**Table**: `inventory_store`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| location_description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `stocks` (from inventory.Stock)
- `stock_moves` (from inventory.StockMove)
- `purchase_orders` (from purchasing.PurchaseOrder)
- `goodsreceipt` (from purchasing.GoodsReceipt)
- `purchase_returns` (from purchasing.PurchaseReturn)
- `pos_configs` (from pos.POSConfig)
- `production_lines` (from production.ProductionLine)

---

### UoM

**Table**: `inventory_uom`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| symbol | CharField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `stock_moves` (from inventory.StockMove)
- `goodsreceiptitem` (from purchasing.GoodsReceiptItem)
- `bill_of_materials` (from production.BillOfMaterials)
- `bom_items` (from production.BOMItem)
- `production_orders` (from production.ProductionOrder)
- `production_order_items` (from production.ProductionOrderItem)
- `production_outputs` (from production.ProductionOutput)
- `production_wastes` (from production.ProductionWaste)

---

### UoMCategory

**Table**: `inventory_uomcategory`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### Warehouse

**Table**: `inventory_warehouse`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| address | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `locations` (from inventory.WarehouseLocation)

---

### WarehouseLocation

**Table**: `inventory_warehouselocation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| warehouse | ForeignKey | No | - | Yes |

**Foreign Keys**:

- `warehouse` → inventory.Warehouse

**Unique Together**:

- (warehouse, code)

---

## memory_ai

### MemoryItem

**Table**: `memory_ai_memoryitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| key | CharField | No | - | No |
| value | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

## notifications

### Notification

**Table**: `notifications_notification`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| notification_type | ForeignKey | No | - | Yes |
| recipient | ForeignKey | No | - | Yes |
| sender | ForeignKey | Yes | - | Yes |
| title | CharField | No | - | No |
| message | TextField | No | - | No |
| data | TextField | Yes | - | No |
| is_read | BooleanField | No | False | No |
| read_at | DateTimeField | Yes | - | No |
| content_type | ForeignKey | Yes | - | Yes |
| object_id | PositiveIntegerField | Yes | - | No |
| url | CharField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| content_object | GenericForeignKey | No | - | No |

**Foreign Keys**:

- `notification_type` → notifications.NotificationType
- `recipient` → users.User
- `sender` → users.User
- `content_type` → contenttypes.ContentType

**Reverse Relations**:

- `deliveries` (from notifications.NotificationDelivery)

---

### NotificationChannel

**Table**: `notifications_notificationchannel`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `user_preferences` (from notifications.UserNotificationPreference)
- `deliveries` (from notifications.NotificationDelivery)

---

### NotificationDelivery

**Table**: `notifications_notificationdelivery`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| notification | ForeignKey | No | - | Yes |
| channel | ForeignKey | No | - | Yes |
| status | CharField | No | pending | No |
| delivered_at | DateTimeField | Yes | - | No |
| error_message | TextField | Yes | - | No |
| retry_count | PositiveIntegerField | No | 0 | No |
| external_id | CharField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `notification` → notifications.Notification
- `channel` → notifications.NotificationChannel

---

### NotificationType

**Table**: `notifications_notificationtype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| description | TextField | Yes | - | No |
| template | TextField | No | - | No |
| icon | CharField | Yes | - | No |
| color | CharField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `user_preferences` (from notifications.UserNotificationPreference)
- `notifications` (from notifications.Notification)

---

### UserNotificationPreference

**Table**: `notifications_usernotificationpreference`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| notification_type | ForeignKey | No | - | Yes |
| channel | ForeignKey | No | - | Yes |
| is_enabled | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User
- `notification_type` → notifications.NotificationType
- `channel` → notifications.NotificationChannel

**Unique Together**:

- (user, notification_type, channel)

---

## nurseries

### ActivityResourceUsage

**Table**: `nurseries_activityresourceusage`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| nursery_activity | ForeignKey | No | - | Yes |
| resource | ForeignKey | No | - | Yes |
| quantity_used | DecimalField | No | - | No |
| cost | DecimalField | Yes | - | No |

**Foreign Keys**:

- `nursery_activity` → nurseries.NurseryActivity
- `resource` → nurseries.NurseryResource

---

### BatchStageLog

**Table**: `nurseries_batchstagelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| production_batch | ForeignKey | No | - | Yes |
| growth_stage | ForeignKey | No | - | Yes |
| entry_date | DateTimeField | No | - | No |
| exit_date | DateTimeField | Yes | - | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `production_batch` → nurseries.ProductionBatch
- `growth_stage` → nurseries.GrowthStage

---

### EnvironmentalLog

**Table**: `nurseries_environmentallog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| nursery_section | ForeignKey | No | - | Yes |
| log_datetime | DateTimeField | No | - | No |
| temperature | DecimalField | Yes | - | No |
| humidity | DecimalField | Yes | - | No |
| light_intensity | DecimalField | Yes | - | No |
| recorded_by | ForeignKey | Yes | - | Yes |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `nursery_section` → nurseries.NurserySection
- `recorded_by` → users.User

---

### GrowthStage

**Table**: `nurseries_growthstage`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| order | PositiveIntegerField | No | 0 | No |
| plant_variety | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `plant_variety` → nurseries.PlantVariety

**Reverse Relations**:

- `productionbatch` (from nurseries.ProductionBatch)
- `batchstagelog` (from nurseries.BatchStageLog)

---

### Nursery

**Table**: `nurseries_nursery`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| location | TextField | Yes | - | No |
| area | DecimalField | Yes | - | No |
| manager | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `manager` → users.User

**Reverse Relations**:

- `sections` (from nurseries.NurserySection)

---

### NurseryActivity

**Table**: `nurseries_nurseryactivity`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| activity_type | ForeignKey | No | - | Yes |
| production_batch | ForeignKey | Yes | - | Yes |
| nursery_section | ForeignKey | Yes | - | Yes |
| performed_by | ForeignKey | Yes | - | Yes |
| date_performed | DateTimeField | No | - | No |
| cost | DecimalField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `activity_type` → nurseries.NurseryActivityType
- `production_batch` → nurseries.ProductionBatch
- `nursery_section` → nurseries.NurserySection
- `performed_by` → users.User

**Reverse Relations**:

- `resource_usages` (from nurseries.ActivityResourceUsage)

---

### NurseryActivityType

**Table**: `nurseries_nurseryactivitytype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |

**Reverse Relations**:

- `nurseryactivity` (from nurseries.NurseryActivity)

---

### NurseryArea

**Table**: `nurseries_nurseryarea`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| nursery_site | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| area_size | DecimalField | No | - | No |
| capacity | PositiveIntegerField | No | - | No |

**Foreign Keys**:

- `nursery_site` → nurseries.NurserySite

---

### NurseryResource

**Table**: `nurseries_nurseryresource`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| resource_type | CharField | No | - | No |
| unit_of_measure | CharField | No | - | No |
| description | TextField | Yes | - | No |

**Reverse Relations**:

- `activityresourceusage` (from nurseries.ActivityResourceUsage)

---

### NurserySection

**Table**: `nurseries_nurserysection`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| nursery | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| section_type | CharField | Yes | - | No |
| area | DecimalField | Yes | - | No |
| capacity | PositiveIntegerField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `nursery` → nurseries.Nursery

**Reverse Relations**:

- `productionbatch` (from nurseries.ProductionBatch)
- `activities` (from nurseries.NurseryActivity)
- `environmental_logs` (from nurseries.EnvironmentalLog)

---

### NurserySite

**Table**: `nurseries_nurserysite`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| nursery_type | CharField | No | - | No |
| total_area | DecimalField | No | - | No |
| designed_capacity | PositiveIntegerField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `areas` (from nurseries.NurseryArea)

---

### PlantSpecies

**Table**: `nurseries_plantspecies`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| scientific_name | CharField | Yes | - | No |
| species_type | CharField | No | - | No |

---

### PlantVariety

**Table**: `nurseries_plantvariety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| scientific_name | CharField | Yes | - | No |
| description | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `growth_stages` (from nurseries.GrowthStage)
- `productionbatch` (from nurseries.ProductionBatch)

---

### ProductionBatch

**Table**: `nurseries_productionbatch`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| batch_identifier | CharField | No | - | No |
| plant_variety | ForeignKey | No | - | Yes |
| nursery_section | ForeignKey | Yes | - | Yes |
| start_date | DateField | No | - | No |
| initial_quantity | PositiveIntegerField | No | - | No |
| current_quantity | PositiveIntegerField | Yes | - | No |
| current_growth_stage | ForeignKey | Yes | - | Yes |
| status | CharField | No | ACTIVE | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `plant_variety` → nurseries.PlantVariety
- `nursery_section` → nurseries.NurserySection
- `current_growth_stage` → nurseries.GrowthStage

**Reverse Relations**:

- `stage_logs` (from nurseries.BatchStageLog)
- `activities` (from nurseries.NurseryActivity)
- `quality_checks` (from nurseries.QualityCheck)

---

### QualityCheck

**Table**: `nurseries_qualitycheck`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| production_batch | ForeignKey | No | - | Yes |
| check_date | DateTimeField | No | - | No |
| checked_by | ForeignKey | Yes | - | Yes |
| overall_quality | CharField | Yes | - | No |
| parameters_checked | JSONField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `production_batch` → nurseries.ProductionBatch
- `checked_by` → users.User

---

## organization

### Branch

**Table**: `organization_branch`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| company | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| address | TextField | Yes | - | No |
| phone | CharField | Yes | - | No |
| email | CharField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `company` → organization.Company

**Reverse Relations**:

- `departments` (from organization.Department)

**Unique Together**:

- (company, code)

---

### City

**Table**: `organization_city`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| country | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `country` → organization.Country

**Unique Together**:

- (country, code)

---

### Company

**Table**: `organization_company`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| legal_name | CharField | Yes | - | No |
| code | CharField | No | - | No |
| country | ForeignKey | No | - | Yes |
| base_currency | ForeignKey | No | - | Yes |
| registration_number | CharField | Yes | - | No |
| tax_id | CharField | Yes | - | No |
| address | TextField | Yes | - | No |
| phone | CharField | Yes | - | No |
| email | CharField | Yes | - | No |
| website | CharField | Yes | - | No |
| logo | FileField | Yes | - | No |
| parent_company | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `country` → organization.Country
- `base_currency` → organization.Currency
- `parent_company` → organization.Company

**Reverse Relations**:

- `subsidiaries` (from organization.Company)
- `branches` (from organization.Branch)
- `core_org_depts` (from organization.Department)

---

### Country

**Table**: `organization_country`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| default_currency | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | Yes | - | No |
| updated_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `default_currency` → organization.Currency

**Reverse Relations**:

- `cities` (from organization.City)
- `companies` (from organization.Company)

---

### Currency

**Table**: `organization_currency`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| code | CharField | No | - | No |
| name | CharField | No | - | No |
| symbol | CharField | No | - | No |
| decimal_places | PositiveSmallIntegerField | No | 2 | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | Yes | - | No |
| updated_at | DateTimeField | Yes | - | No |

**Reverse Relations**:

- `rates_from` (from organization.ExchangeRate)
- `rates_to` (from organization.ExchangeRate)
- `countries_default` (from organization.Country)
- `companies_base` (from organization.Company)

---

### Department

**Table**: `organization_department`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| branch | ForeignKey | Yes | - | Yes |
| company | ForeignKey | Yes | - | Yes |
| code | CharField | No | - | No |
| parent_department | ForeignKey | Yes | - | Yes |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `branch` → organization.Branch
- `company` → organization.Company
- `parent_department` → organization.Department

**Reverse Relations**:

- `sub_departments` (from organization.Department)

---

### ExchangeRate

**Table**: `organization_exchangerate`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| from_currency | ForeignKey | No | - | Yes |
| to_currency | ForeignKey | No | - | Yes |
| rate | DecimalField | No | - | No |
| date | DateField | No | - | Yes |
| source | CharField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `from_currency` → organization.Currency
- `to_currency` → organization.Currency

**Unique Together**:

- (from_currency, to_currency, date)

---

## performance

### APIPerformance

**Table**: `performance_apiperformance`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| endpoint | CharField | No | - | No |
| method | CharField | No | - | No |
| response_time | FloatField | No | - | No |
| status_code | IntegerField | No | - | No |
| request_size | IntegerField | No | 0 | No |
| response_size | IntegerField | No | 0 | No |
| user | ForeignKey | Yes | - | Yes |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| user_agent | TextField | No | - | No |
| ip_address | GenericIPAddressField | Yes | - | No |

**Foreign Keys**:

- `user` → users.User

**Indexes**:

- performance_endpoin_8adc56_idx: (endpoint, timestamp)
- performance_method_1f5807_idx: (method, timestamp)
- performance_status__439c9c_idx: (status_code, timestamp)
- performance_respons_a19659_idx: (response_time)

---

### CacheStatistics

**Table**: `performance_cachestatistics`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| cache_name | CharField | No | - | No |
| hits | BigIntegerField | No | 0 | No |
| misses | BigIntegerField | No | 0 | No |
| hit_rate | FloatField | No | 0.0 | No |
| total_keys | IntegerField | No | 0 | No |
| memory_usage | FloatField | No | 0.0 | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |

**Indexes**:

- performance_cache_n_4bb8a4_idx: (cache_name, timestamp)

---

### DatabasePerformance

**Table**: `performance_databaseperformance`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| query_type | CharField | No | - | No |
| query_hash | CharField | No | - | No |
| execution_time | FloatField | No | - | No |
| rows_affected | IntegerField | No | 0 | No |
| table_name | CharField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| user | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `user` → users.User

**Indexes**:

- performance_query_t_663df9_idx: (query_type, timestamp)
- performance_executi_2830b6_idx: (execution_time)
- performance_table_n_e059ee_idx: (table_name, timestamp)

---

### PerformanceAlert

**Table**: `performance_performancealert`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| alert_type | CharField | No | - | No |
| severity | CharField | No | - | No |
| message | TextField | No | - | No |
| threshold_value | FloatField | No | - | No |
| actual_value | FloatField | No | - | No |
| component | CharField | No | - | No |
| is_resolved | BooleanField | No | False | No |
| created_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| resolved_at | DateTimeField | Yes | - | No |
| metadata | JSONField | No | <class 'dict'> | No |

**Indexes**:

- performance_alert_t_a4a30d_idx: (alert_type, created_at)
- performance_severit_a7ba2e_idx: (severity, is_resolved)
- performance_compone_7ffde2_idx: (component, created_at)

---

### PerformanceMetric

**Table**: `performance_performancemetric`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| metric_type | CharField | No | - | No |
| value | FloatField | No | - | No |
| unit | CharField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| endpoint | CharField | Yes | - | No |
| user | ForeignKey | Yes | - | Yes |
| metadata | JSONField | No | <class 'dict'> | No |

**Foreign Keys**:

- `user` → users.User

**Indexes**:

- performance_metric__b34494_idx: (metric_type, timestamp)
- performance_endpoin_bd2cf3_idx: (endpoint, timestamp)
- performance_user_id_5a10a8_idx: (user, timestamp)

---

### PerformanceOptimization

**Table**: `performance_performanceoptimization`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| optimization_type | CharField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| before_value | FloatField | No | - | No |
| after_value | FloatField | No | - | No |
| improvement_percentage | FloatField | No | - | No |
| implementation_date | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| implemented_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `implemented_by` → users.User

---

### SystemHealth

**Table**: `performance_systemhealth`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| component | CharField | No | - | No |
| status | CharField | No | - | No |
| cpu_usage | FloatField | No | - | No |
| memory_usage | FloatField | No | - | No |
| disk_usage | FloatField | No | - | No |
| active_connections | IntegerField | No | 0 | No |
| response_time | FloatField | No | 0.0 | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| details | JSONField | No | <class 'dict'> | No |

**Indexes**:

- performance_compone_21e8d1_idx: (component, timestamp)
- performance_status_38a11d_idx: (status, timestamp)

---

## permissions

### AIAgent

**Table**: `permissions_aiagent`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | default_name | No |
| agent_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| agent_type | CharField | No | assistant | No |
| description | TextField | Yes | - | No |
| owner | ForeignKey | No | - | Yes |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `owner` → users.User

**Reverse Relations**:

- `ai_role_assignments` (from permissions.AIAgentRoleAssignment)

---

### AIAgentRoleAssignment

**Table**: `permissions_aiagentroleassignment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| agent | ForeignKey | No | - | Yes |
| role | ForeignKey | No | - | Yes |
| assigned_at | DateTimeField | No | - | No |
| assigned_by | ForeignKey | Yes | - | Yes |
| expires_at | DateTimeField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `agent` → permissions.AIAgent
- `role` → permissions.AIRole
- `assigned_by` → users.User

**Unique Together**:

- (agent, role)

---

### AIPermission

**Table**: `permissions_aipermission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | default_name | No |
| code | CharField | No | default_code | No |
| description | TextField | Yes | - | No |
| permission_type | CharField | No | model_access | No |
| ai_module | CharField | No | - | No |
| resource_type | CharField | No | - | No |
| security_level | CharField | No | medium | No |
| is_system_permission | BooleanField | No | False | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `airolepermission` (from permissions.AIRolePermission)

**Unique Together**:

- (code, ai_module)

---

### AIRole

**Table**: `permissions_airole`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | default_name | No |
| code | CharField | No | default_code | No |
| description | TextField | Yes | - | No |
| parent_role | ForeignKey | Yes | - | Yes |
| ai_model_type | CharField | No | - | No |
| is_system_role | BooleanField | No | False | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| permissions | ManyToManyField | No | - | No |

**Foreign Keys**:

- `parent_role` → permissions.AIRole

**Reverse Relations**:

- `child_ai_roles` (from permissions.AIRole)
- `airolepermission` (from permissions.AIRolePermission)
- `aiagentroleassignment` (from permissions.AIAgentRoleAssignment)

---

### AIRolePermission

**Table**: `permissions_airolepermission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| role | ForeignKey | No | - | Yes |
| permission | ForeignKey | No | - | Yes |
| granted_at | DateTimeField | No | - | No |
| granted_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `role` → permissions.AIRole
- `permission` → permissions.AIPermission
- `granted_by` → users.User

**Unique Together**:

- (role, permission)

---

### PermissionAuditLog

**Table**: `permissions_permissionauditlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| entity_type | CharField | No | - | No |
| entity_id | CharField | No | - | No |
| action | CharField | No | - | No |
| permission_code | CharField | No | - | No |
| resource | CharField | No | - | No |
| result | BooleanField | No | - | No |
| details | JSONField | No | <class 'dict'> | No |
| performed_by | ForeignKey | Yes | - | Yes |
| timestamp | DateTimeField | No | - | No |

**Foreign Keys**:

- `performed_by` → users.User

---

### UserPermission

**Table**: `permissions_userpermission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | default_name | No |
| code | CharField | No | default_code | No |
| description | TextField | Yes | - | No |
| permission_type | CharField | No | read | No |
| module | CharField | No | - | No |
| category | CharField | No | - | No |
| is_system_permission | BooleanField | No | False | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `userrolepermission` (from permissions.UserRolePermission)

**Unique Together**:

- (code, module)

---

### UserRole

**Table**: `permissions_userrole`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | default_name | No |
| code | CharField | No | default_code | No |
| description | TextField | Yes | - | No |
| parent_role | ForeignKey | Yes | - | Yes |
| is_system_role | BooleanField | No | False | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| permissions | ManyToManyField | No | - | No |

**Foreign Keys**:

- `parent_role` → permissions.UserRole

**Reverse Relations**:

- `child_user_roles` (from permissions.UserRole)
- `userrolepermission` (from permissions.UserRolePermission)
- `userroleassignment` (from permissions.UserRoleAssignment)

---

### UserRoleAssignment

**Table**: `permissions_userroleassignment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| role | ForeignKey | No | - | Yes |
| assigned_at | DateTimeField | No | - | No |
| assigned_by | ForeignKey | Yes | - | Yes |
| expires_at | DateTimeField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `user` → users.User
- `role` → permissions.UserRole
- `assigned_by` → users.User

**Unique Together**:

- (user, role)

---

### UserRolePermission

**Table**: `permissions_userrolepermission`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| role | ForeignKey | No | - | Yes |
| permission | ForeignKey | No | - | Yes |
| granted_at | DateTimeField | No | - | No |
| granted_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `role` → permissions.UserRole
- `permission` → permissions.UserPermission
- `granted_by` → users.User

**Unique Together**:

- (role, permission)

---

## plant_diagnosis

### DiagnosisResult

**Table**: `plant_diagnosis_diagnosisresult`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| diagnosis_request | OneToOneField | No | - | Yes |
| disease_name | CharField | Yes | - | No |
| scientific_name | CharField | Yes | - | No |
| confidence_score | FloatField | Yes | - | No |
| is_healthy | BooleanField | No | False | No |
| description | TextField | No | - | No |
| treatment | TextField | No | - | No |
| prevention | TextField | No | - | No |
| received_at | DateTimeField | No | - | No |
| additional_data | JSONField | No | <class 'dict'> | No |

**Reverse Relations**:

- `diagnosis_request` (from plant_diagnosis.PlantDiagnosisRequest)

---

### PlantDiagnosisRequest

**Table**: `plant_diagnosis_plantdiagnosisrequest`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| user | ForeignKey | No | - | Yes |
| image | FileField | No | - | No |
| plant_type | CharField | No | - | No |
| symptoms_description | TextField | No | - | No |
| location | CharField | No | - | No |
| status | CharField | No | pending | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| external_request_id | CharField | Yes | - | No |

**Foreign Keys**:

- `user` → users.User

**Reverse Relations**:

- `result` (from plant_diagnosis.DiagnosisResult)

---

## pos

### POSConfig

**Table**: `pos_posconfig`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| warehouse | ForeignKey | No | - | Yes |
| journal | ForeignKey | No | - | Yes |
| is_active | BooleanField | No | True | No |
| allow_discount | BooleanField | No | True | No |
| allow_price_change | BooleanField | No | False | No |
| allow_credit_sales | BooleanField | No | False | No |
| allow_returns | BooleanField | No | True | No |
| receipt_header | TextField | Yes | - | No |
| receipt_footer | TextField | Yes | - | No |

**Foreign Keys**:

- `company` → core.Company
- `warehouse` → inventory.Store
- `journal` → accounting.Journal

**Reverse Relations**:

- `sessions` (from pos.POSSession)

**Unique Together**:

- (name, company)

---

### POSOrder

**Table**: `pos_posorder`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| session | ForeignKey | No | - | Yes |
| date_order | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| state | CharField | No | draft | No |
| amount_total | DecimalField | No | 0.00 | No |
| amount_tax | DecimalField | No | 0.00 | No |
| amount_paid | DecimalField | No | 0.00 | No |
| amount_return | DecimalField | No | 0.00 | No |
| note | TextField | Yes | - | No |

**Foreign Keys**:

- `session` → pos.POSSession

**Reverse Relations**:

- `lines` (from pos.POSOrderLine)
- `payments` (from pos.POSPayment)

---

### POSOrderLine

**Table**: `pos_posorderline`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| qty | DecimalField | No | - | No |
| price_unit | DecimalField | No | - | No |
| price_subtotal | DecimalField | No | 0.00 | No |
| discount | DecimalField | No | 0.00 | No |

**Foreign Keys**:

- `order` → pos.POSOrder
- `product` → inventory.Product

---

### POSPayment

**Table**: `pos_pospayment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order | ForeignKey | No | - | Yes |
| payment_method | CharField | No | cash | No |
| amount | DecimalField | No | - | No |
| payment_date | DateTimeField | No | <function now at 0x00000247D3A64680> | No |

**Foreign Keys**:

- `order` → pos.POSOrder

---

### POSSession

**Table**: `pos_possession`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| config | ForeignKey | No | - | Yes |
| opening_date | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| closing_date | DateTimeField | Yes | - | No |
| state | CharField | No | opened | No |
| opening_balance | DecimalField | No | 0.00 | No |
| closing_balance | DecimalField | No | 0.00 | No |
| cash_register_balance | DecimalField | No | 0.00 | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `config` → pos.POSConfig

**Reverse Relations**:

- `orders` (from pos.POSOrder)

---

## production

### BillOfMaterials

**Table**: `production_billofmaterials`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | - | No |
| uom | ForeignKey | No | - | Yes |
| is_active | BooleanField | No | True | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `company` → core.Company
- `product` → inventory.Product
- `uom` → inventory.UoM

**Reverse Relations**:

- `items` (from production.BOMItem)
- `operations` (from production.BOMOperation)
- `production_orders` (from production.ProductionOrder)

**Indexes**:

- production__name_8bd041_idx: (name)
- production__code_0b26c4_idx: (code)
- production__company_d553e8_idx: (company)
- production__product_4e703f_idx: (product)
- production__is_acti_f1d462_idx: (is_active)

**Unique Together**:

- (code, company)

---

### BOMItem

**Table**: `production_bomitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| bom | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | - | No |
| uom | ForeignKey | No | - | Yes |
| unit_cost | DecimalField | No | - | No |
| subtotal | DecimalField | No | 0 | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `bom` → production.BillOfMaterials
- `product` → inventory.Product
- `uom` → inventory.UoM

**Indexes**:

- production__bom_id_2a7c10_idx: (bom)
- production__product_935327_idx: (product)

**Unique Together**:

- (bom, product)

---

### BOMOperation

**Table**: `production_bomoperation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| bom | ForeignKey | No | - | Yes |
| operation | ForeignKey | No | - | Yes |
| sequence | PositiveIntegerField | No | 10 | No |
| time_required | DecimalField | No | - | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `bom` → production.BillOfMaterials
- `operation` → production.ProductionOperation

**Indexes**:

- production__bom_id_465450_idx: (bom)
- production__operati_820376_idx: (operation)
- production__sequenc_4feb5f_idx: (sequence)

**Unique Together**:

- (bom, operation)

---

### ProductionLine

**Table**: `production_productionline`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| warehouse | ForeignKey | No | - | Yes |
| capacity_per_hour | DecimalField | No | - | No |
| is_active | BooleanField | No | True | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `company` → core.Company
- `warehouse` → inventory.Store

**Reverse Relations**:

- `production_orders` (from production.ProductionOrder)

**Indexes**:

- production__name_f946f8_idx: (name)
- production__code_9fbc39_idx: (code)
- production__company_e0b9b8_idx: (company)
- production__is_acti_f24418_idx: (is_active)

**Unique Together**:

- (name, company)

---

### ProductionOperation

**Table**: `production_productionoperation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| description | TextField | Yes | - | No |
| time_required | DecimalField | No | - | No |
| is_active | BooleanField | No | True | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `company` → core.Company

**Reverse Relations**:

- `bom_operations` (from production.BOMOperation)
- `production_order_operations` (from production.ProductionOrderOperation)

**Indexes**:

- production__name_1a7563_idx: (name)
- production__code_8e26af_idx: (code)
- production__company_c14137_idx: (company)
- production__is_acti_4fc0c1_idx: (is_active)

**Unique Together**:

- (name, company)

---

### ProductionOrder

**Table**: `production_productionorder`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| bom | ForeignKey | No | - | Yes |
| production_line | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | - | No |
| uom | ForeignKey | No | - | Yes |
| planned_start_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| planned_end_date | DateField | No | - | No |
| actual_start_date | DateField | Yes | - | No |
| actual_end_date | DateField | Yes | - | No |
| state | CharField | No | draft | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `company` → core.Company
- `bom` → production.BillOfMaterials
- `production_line` → production.ProductionLine
- `product` → inventory.Product
- `uom` → inventory.UoM

**Reverse Relations**:

- `items` (from production.ProductionOrderItem)
- `order_operations` (from production.ProductionOrderOperation)
- `outputs` (from production.ProductionOutput)
- `wastes` (from production.ProductionWaste)

**Indexes**:

- production__name_6ebe00_idx: (name)
- production__company_ceda61_idx: (company)
- production__bom_id_b31aa7_idx: (bom)
- production__product_704e4f_idx: (production_line)
- production__product_3bec5f_idx: (product)
- production__state_cd6148_idx: (state)
- production__planned_06b57c_idx: (planned_start_date)
- production__planned_384b1b_idx: (planned_end_date)

---

### ProductionOrderItem

**Table**: `production_productionorderitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | - | No |
| uom | ForeignKey | No | - | Yes |
| unit_cost | DecimalField | No | - | No |
| subtotal | DecimalField | No | 0 | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `order` → production.ProductionOrder
- `product` → inventory.Product
- `uom` → inventory.UoM

**Indexes**:

- production__order_i_67d9c0_idx: (order)
- production__product_da454c_idx: (product)

**Unique Together**:

- (order, product)

---

### ProductionOrderOperation

**Table**: `production_productionorderoperation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order | ForeignKey | No | - | Yes |
| operation | ForeignKey | No | - | Yes |
| sequence | PositiveIntegerField | No | 10 | No |
| time_required | DecimalField | No | - | No |
| state | CharField | No | pending | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `order` → production.ProductionOrder
- `operation` → production.ProductionOperation

**Indexes**:

- production__order_i_e28c90_idx: (order)
- production__operati_90b80f_idx: (operation)
- production__sequenc_65e00c_idx: (sequence)
- production__state_ece80a_idx: (state)

**Unique Together**:

- (order, operation)

---

### ProductionOutput

**Table**: `production_productionoutput`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | - | No |
| uom | ForeignKey | No | - | Yes |
| production_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `order` → production.ProductionOrder
- `product` → inventory.Product
- `uom` → inventory.UoM

**Indexes**:

- production__order_i_08783e_idx: (order)
- production__product_a775e1_idx: (product)
- production__product_4a1a1f_idx: (production_date)

---

### ProductionWaste

**Table**: `production_productionwaste`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | - | No |
| uom | ForeignKey | No | - | Yes |
| waste_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| reason | CharField | No | - | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `order` → production.ProductionOrder
- `product` → inventory.Product
- `uom` → inventory.UoM

**Indexes**:

- production__order_i_f1ece6_idx: (order)
- production__product_622ad4_idx: (product)
- production__waste_d_6e9859_idx: (waste_date)

---

## purchasing

### GoodsReceipt

**Table**: `purchasing_goodsreceipt`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| purchase_order | ForeignKey | No | - | Yes |
| supplier | ForeignKey | No | - | Yes |
| company | ForeignKey | No | - | Yes |
| branch | ForeignKey | No | - | Yes |
| warehouse | ForeignKey | No | - | Yes |
| receipt_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| state | CharField | No | draft | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `purchase_order` → purchasing.PurchaseOrder
- `supplier` → purchasing.Supplier
- `company` → core.Company
- `branch` → core.Branch
- `warehouse` → inventory.Store

**Reverse Relations**:

- `items` (from purchasing.GoodsReceiptItem)

---

### GoodsReceiptItem

**Table**: `purchasing_goodsreceiptitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| goods_receipt | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| ordered_quantity | DecimalField | No | - | No |
| received_quantity | DecimalField | No | - | No |
| unit_of_measure | ForeignKey | No | - | Yes |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `goods_receipt` → purchasing.GoodsReceipt
- `product` → inventory.Product
- `unit_of_measure` → inventory.UoM

**Unique Together**:

- (goods_receipt, product)

---

### PaymentMethod

**Table**: `purchasing_paymentmethod`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |

---

### PurchaseInvoice

**Table**: `purchasing_purchaseinvoice`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| invoice_number | CharField | No | - | No |
| supplier | ForeignKey | No | - | Yes |
| invoice_date | DateField | No | - | No |
| due_date | DateField | No | - | No |
| status | CharField | No | draft | No |
| total_amount | DecimalField | No | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| created_by | ForeignKey | No | - | Yes |
| parent_invoice | ForeignKey | Yes | - | Yes |
| is_parent_consolidated | BooleanField | No | False | No |

**Foreign Keys**:

- `supplier` → purchasing.Supplier
- `created_by` → users.User
- `parent_invoice` → purchasing.PurchaseInvoice

**Reverse Relations**:

- `child_invoices` (from purchasing.PurchaseInvoice)
- `items` (from purchasing.PurchaseInvoiceItem)
- `returns` (from purchasing.PurchaseReturn)

---

### PurchaseInvoiceItem

**Table**: `purchasing_purchaseinvoiceitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| invoice | ForeignKey | No | - | Yes |
| description | CharField | No | - | No |
| quantity | DecimalField | No | - | No |
| unit_price | DecimalField | No | - | No |
| discount | DecimalField | No | 0.00 | No |
| tax_rate | DecimalField | No | 0.00 | No |
| total_price | DecimalField | No | 0.00 | No |
| product_reference | CharField | Yes | - | No |

**Foreign Keys**:

- `invoice` → purchasing.PurchaseInvoice

---

### PurchaseOrder

**Table**: `purchasing_purchaseorder`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| reference | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| supplier | ForeignKey | No | - | Yes |
| date | DateField | No | <function now at 0x00000247D3A64680> | No |
| expected_date | DateField | Yes | - | No |
| warehouse | ForeignKey | No | - | Yes |
| untaxed_amount | DecimalField | No | 0 | No |
| tax_amount | DecimalField | No | 0 | No |
| total_amount | DecimalField | No | 0 | No |
| state | CharField | No | draft | No |
| created_by | ForeignKey | Yes | - | Yes |
| confirmed_by | ForeignKey | Yes | - | Yes |
| cancelled_by | ForeignKey | Yes | - | Yes |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `company` → core.Company
- `supplier` → purchasing.Supplier
- `warehouse` → inventory.Store
- `created_by` → users.User
- `confirmed_by` → users.User
- `cancelled_by` → users.User

**Reverse Relations**:

- `lines` (from purchasing.PurchaseOrderLine)
- `receipts` (from purchasing.GoodsReceipt)
- `supplierinvoice` (from purchasing.SupplierInvoice)

**Unique Together**:

- (reference, company)

---

### PurchaseOrderLine

**Table**: `purchasing_purchaseorderline`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | 1 | No |
| unit_price | DecimalField | No | 0 | No |
| discount_percent | DecimalField | No | 0 | No |
| discount_amount | DecimalField | No | 0 | No |
| tax | ForeignKey | Yes | - | Yes |
| tax_amount | DecimalField | No | 0 | No |
| subtotal | DecimalField | No | 0 | No |
| total | DecimalField | No | 0 | No |
| description | TextField | No | - | No |
| sequence | PositiveIntegerField | No | 10 | No |
| expected_date | DateField | Yes | - | No |

**Foreign Keys**:

- `order` → purchasing.PurchaseOrder
- `product` → inventory.Product
- `tax` → accounting.Tax

---

### PurchaseReturn

**Table**: `purchasing_purchasereturn`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| reference | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| supplier | ForeignKey | No | - | Yes |
| purchase_invoice | ForeignKey | Yes | - | Yes |
| date | DateField | No | <function now at 0x00000247D3A64680> | No |
| warehouse | ForeignKey | No | - | Yes |
| untaxed_amount | DecimalField | No | 0 | No |
| tax_amount | DecimalField | No | 0 | No |
| total_amount | DecimalField | No | 0 | No |
| state | CharField | No | draft | No |
| return_reason | CharField | No | other | No |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `company` → core.Company
- `supplier` → purchasing.Supplier
- `purchase_invoice` → purchasing.PurchaseInvoice
- `warehouse` → inventory.Store

**Reverse Relations**:

- `lines` (from purchasing.PurchaseReturnLine)

**Unique Together**:

- (reference, company)

---

### PurchaseReturnLine

**Table**: `purchasing_purchasereturnline`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| return_doc | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| quantity | DecimalField | No | 1 | No |
| unit_price | DecimalField | No | 0 | No |
| tax_amount | DecimalField | No | 0 | No |
| subtotal | DecimalField | No | 0 | No |
| total | DecimalField | No | 0 | No |
| description | TextField | No | - | No |
| sequence | PositiveIntegerField | No | 10 | No |
| return_reason | CharField | No | other | No |

**Foreign Keys**:

- `return_doc` → purchasing.PurchaseReturn
- `product` → inventory.Product

---

### Supplier

**Table**: `purchasing_supplier`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `purchase_orders` (from purchasing.PurchaseOrder)
- `goodsreceipt` (from purchasing.GoodsReceipt)
- `purchase_invoices` (from purchasing.PurchaseInvoice)
- `purchase_returns` (from purchasing.PurchaseReturn)
- `supplier_invoices` (from purchasing.SupplierInvoice)

---

### SupplierInvoice

**Table**: `purchasing_supplierinvoice`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| supplier | ForeignKey | No | - | Yes |
| purchase_order | ForeignKey | Yes | - | Yes |
| company | ForeignKey | No | - | Yes |
| branch | ForeignKey | No | - | Yes |
| invoice_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| due_date | DateField | Yes | - | No |
| state | CharField | No | draft | No |
| total_amount | DecimalField | No | 0 | No |
| paid_amount | DecimalField | No | 0 | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `supplier` → purchasing.Supplier
- `purchase_order` → purchasing.PurchaseOrder
- `company` → core.Company
- `branch` → core.Branch

---

## rent

### AssetItem

**Table**: `rent_assetitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| property | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| value | DecimalField | No | 0 | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `property` → rent.Property

---

### LeaseAgreement

**Table**: `rent_leaseagreement`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| property | ForeignKey | No | - | Yes |
| unit | ForeignKey | Yes | - | Yes |
| tenant | ForeignKey | Yes | - | Yes |
| start_date | DateField | Yes | - | No |
| end_date | DateField | Yes | - | No |
| rent_amount | DecimalField | No | 0 | No |
| payment_frequency | CharField | No | MONTHLY | No |
| deposit_amount | DecimalField | Yes | - | No |
| terms | TextField | No | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `property` → rent.Property
- `unit` → rent.PropertyUnit
- `tenant` → core.Company

---

### MaintenanceRequest

**Table**: `rent_maintenancerequest`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| property | ForeignKey | No | - | Yes |
| unit | ForeignKey | Yes | - | Yes |
| reported_by | ForeignKey | Yes | - | Yes |
| tenant_reporter | ForeignKey | Yes | - | Yes |
| description | TextField | No | - | No |
| status | CharField | No | pending | No |
| reported_date | DateField | Yes | - | No |
| completed_date | DateField | Yes | - | No |
| cost | DecimalField | Yes | - | No |
| is_unit_specific_cost | BooleanField | No | False | No |
| journal_entry | CharField | No | - | No |

**Foreign Keys**:

- `property` → rent.Property
- `unit` → rent.PropertyUnit
- `reported_by` → users.User
- `tenant_reporter` → core.Company

---

### Property

**Table**: `rent_property`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | Yes | - | Yes |
| branch | ForeignKey | Yes | - | Yes |
| property_type | ForeignKey | Yes | - | Yes |
| address | TextField | No | - | No |
| area | FloatField | Yes | - | No |
| bedrooms | IntegerField | Yes | - | No |
| bathrooms | IntegerField | Yes | - | No |
| purchase_value | DecimalField | No | 0 | No |
| market_value | DecimalField | No | 0 | No |
| monthly_rent | DecimalField | No | 0 | No |
| description | TextField | No | - | No |
| status | CharField | No | available | No |
| is_active | BooleanField | No | True | No |
| asset_account | ForeignKey | Yes | - | Yes |
| income_account | ForeignKey | Yes | - | Yes |
| expense_account | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| features | ManyToManyField | No | - | No |

**Foreign Keys**:

- `company` → core.Company
- `branch` → core.Branch
- `property_type` → rent.PropertyType
- `asset_account` → accounting.Account
- `income_account` → accounting.Account
- `expense_account` → accounting.Account

**Reverse Relations**:

- `images` (from rent.PropertyImage)
- `units` (from rent.PropertyUnit)
- `expenses` (from rent.PropertyExpense)
- `incomes` (from rent.PropertyIncome)
- `utility_consumptions` (from rent.UtilityConsumption)
- `asset_items` (from rent.AssetItem)
- `rentalcontractline` (from rent.RentalContractLine)
- `lease_agreements` (from rent.LeaseAgreement)
- `maintenance_requests` (from rent.MaintenanceRequest)

**Unique Together**:

- (company, code)

---

### PropertyExpense

**Table**: `rent_propertyexpense`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| property | ForeignKey | No | - | Yes |
| unit | ForeignKey | Yes | - | Yes |
| description | CharField | No | - | No |
| amount | DecimalField | No | 0 | No |
| date | DateField | No | - | No |

**Foreign Keys**:

- `property` → rent.Property
- `unit` → rent.PropertyUnit

---

### PropertyFeature

**Table**: `rent_propertyfeature`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `company` → core.Company

**Unique Together**:

- (company, code)

---

### PropertyImage

**Table**: `rent_propertyimage`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| property | ForeignKey | No | - | Yes |
| caption | CharField | No | - | No |
| image | CharField | No | - | No |

**Foreign Keys**:

- `property` → rent.Property

---

### PropertyIncome

**Table**: `rent_propertyincome`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| property | ForeignKey | No | - | Yes |
| unit | ForeignKey | Yes | - | Yes |
| description | CharField | No | - | No |
| amount | DecimalField | No | 0 | No |
| date | DateField | No | - | No |

**Foreign Keys**:

- `property` → rent.Property
- `unit` → rent.PropertyUnit

---

### PropertyType

**Table**: `rent_propertytype`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `company` → core.Company

**Reverse Relations**:

- `property` (from rent.Property)

**Unique Together**:

- (company, code)

---

### PropertyUnit

**Table**: `rent_propertyunit`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| property | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| area | FloatField | Yes | - | No |
| monthly_rent | DecimalField | No | 0 | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `property` → rent.Property

**Reverse Relations**:

- `expenses` (from rent.PropertyExpense)
- `incomes` (from rent.PropertyIncome)
- `utility_consumptions` (from rent.UtilityConsumption)
- `lease_agreements` (from rent.LeaseAgreement)
- `maintenance_requests` (from rent.MaintenanceRequest)

**Unique Together**:

- (property, name)

---

### RentalContract

**Table**: `rent_rentalcontract`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | Yes | - | Yes |
| branch | ForeignKey | Yes | - | Yes |
| tenant | ForeignKey | Yes | - | Yes |
| journal | ForeignKey | Yes | - | Yes |
| start_date | DateField | Yes | - | No |
| end_date | DateField | Yes | - | No |
| payment_frequency | CharField | No | monthly | No |
| security_deposit | DecimalField | No | 0 | No |
| notes | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `company` → core.Company
- `branch` → core.Branch
- `tenant` → core.Company
- `journal` → accounting.Journal

**Reverse Relations**:

- `lines` (from rent.RentalContractLine)

---

### RentalContractLine

**Table**: `rent_rentalcontractline`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| contract | ForeignKey | No | - | Yes |
| property | ForeignKey | No | - | Yes |
| monthly_rent | DecimalField | No | 0 | No |
| start_date | DateField | Yes | - | No |
| end_date | DateField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `contract` → rent.RentalContract
- `property` → rent.Property

---

### UtilityConsumption

**Table**: `rent_utilityconsumption`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| property | ForeignKey | No | - | Yes |
| unit | ForeignKey | Yes | - | Yes |
| utility_type | CharField | No | electricity | No |
| reading | FloatField | No | 0 | No |
| date | DateField | No | - | No |

**Foreign Keys**:

- `property` → rent.Property
- `unit` → rent.PropertyUnit

---

### Vehicle

**Table**: `rent_vehicle`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| is_available | BooleanField | No | True | No |

**Reverse Relations**:

- `lease_agreements` (from rent.VehicleLeaseAgreement)

---

### VehicleLeaseAgreement

**Table**: `rent_vehicleleaseagreement`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| vehicle | ForeignKey | No | - | Yes |
| tenant | ForeignKey | Yes | - | Yes |
| start_date | DateField | Yes | - | No |
| end_date | DateField | Yes | - | No |
| rent_rate | DecimalField | No | 0 | No |
| rate_unit | CharField | No | DAILY | No |
| pickup_odometer | IntegerField | No | 0 | No |
| pickup_fuel_level | IntegerField | No | 0 | No |
| return_odometer | IntegerField | Yes | - | No |
| return_fuel_level | IntegerField | Yes | - | No |
| deposit_amount | DecimalField | Yes | - | No |
| total_charge | DecimalField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `vehicle` → rent.Vehicle
- `tenant` → core.Company

---

## research

### ExperimentParticipant

**Table**: `research_experimentparticipant`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| researcher | ForeignKey | No | - | Yes |
| role | CharField | No | - | No |
| responsibilities | TextField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `experiment` → research.ResearchExperiment
- `researcher` → research.Researcher
- `created_by` → users.User

**Unique Together**:

- (experiment, researcher)

---

### ExperimentResult

**Table**: `research_experimentresult`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| experiment | ForeignKey | No | - | Yes |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| date_recorded | DateField | No | - | No |
| numeric_data | JSONField | Yes | - | No |
| observations | TextField | Yes | - | No |
| conclusions | TextField | Yes | - | No |
| verification_status | CharField | No | UNVERIFIED | No |
| verified_by | ForeignKey | Yes | - | Yes |
| verification_date | DateField | Yes | - | No |
| recorded_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `experiment` → research.ResearchExperiment
- `verified_by` → research.Researcher
- `recorded_by` → research.Researcher
- `updated_by` → users.User

---

### Patent

**Table**: `research_patent`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| patent_number | CharField | Yes | - | No |
| application_number | CharField | No | - | No |
| filing_date | DateField | No | - | No |
| grant_date | DateField | Yes | - | No |
| expiry_date | DateField | Yes | - | No |
| status | CharField | No | DRAFT | No |
| patent_office | CharField | No | - | No |
| country | CharField | No | - | No |
| url | CharField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |
| projects | ManyToManyField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `inventors` (from research.PatentInventor)

---

### PatentInventor

**Table**: `research_patentinventor`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| patent | ForeignKey | No | - | Yes |
| researcher | ForeignKey | No | - | Yes |
| order | PositiveSmallIntegerField | No | - | No |
| contribution | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `patent` → research.Patent
- `researcher` → research.Researcher

**Unique Together**:

- (patent, researcher)

---

### ProjectTeamMember

**Table**: `research_projectteammember`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| project | ForeignKey | No | - | Yes |
| researcher | ForeignKey | No | - | Yes |
| role | CharField | No | - | No |
| responsibilities | TextField | Yes | - | No |
| join_date | DateField | No | - | No |
| end_date | DateField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `project` → research.ResearchProject
- `researcher` → research.Researcher
- `created_by` → users.User
- `updated_by` → users.User

**Unique Together**:

- (project, researcher)

---

### Publication

**Table**: `research_publication`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| abstract | TextField | No | - | No |
| publication_type | CharField | No | - | No |
| status | CharField | No | DRAFT | No |
| journal_or_conference | CharField | Yes | - | No |
| volume | CharField | Yes | - | No |
| issue | CharField | Yes | - | No |
| pages | CharField | Yes | - | No |
| doi | CharField | Yes | - | No |
| url | CharField | Yes | - | No |
| publisher | CharField | Yes | - | No |
| publication_date | DateField | Yes | - | No |
| submission_date | DateField | Yes | - | No |
| acceptance_date | DateField | Yes | - | No |
| keywords | TextField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |
| projects | ManyToManyField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `authors` (from research.PublicationAuthor)

---

### PublicationAuthor

**Table**: `research_publicationauthor`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| publication | ForeignKey | No | - | Yes |
| researcher | ForeignKey | No | - | Yes |
| order | PositiveSmallIntegerField | No | - | No |
| is_corresponding | BooleanField | No | False | No |
| contribution | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `publication` → research.Publication
- `researcher` → research.Researcher

**Unique Together**:

- (publication, researcher)

---

### ResearchEquipment

**Table**: `research_researchequipment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| description | TextField | No | - | No |
| model | CharField | Yes | - | No |
| manufacturer | CharField | Yes | - | No |
| serial_number | CharField | Yes | - | No |
| acquisition_date | DateField | No | - | No |
| acquisition_cost | DecimalField | Yes | - | No |
| currency | CharField | No | EGP | No |
| location | CharField | No | - | No |
| status | CharField | No | OPERATIONAL | No |
| last_maintenance_date | DateField | Yes | - | No |
| next_maintenance_date | DateField | Yes | - | No |
| last_calibration_date | DateField | Yes | - | No |
| next_calibration_date | DateField | Yes | - | No |
| responsible_person | ForeignKey | Yes | - | Yes |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `responsible_person` → research.Researcher
- `created_by` → users.User
- `updated_by` → users.User

---

### Researcher

**Table**: `research_researcher`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | OneToOneField | No | - | Yes |
| employee_id | CharField | No | - | No |
| title | CharField | Yes | - | No |
| specialization | CharField | No | - | No |
| department | CharField | No | - | No |
| bio | TextField | Yes | - | No |
| education | TextField | Yes | - | No |
| experience | TextField | Yes | - | No |
| skills | TextField | Yes | - | No |
| publications_count | PositiveIntegerField | No | 0 | No |
| patents_count | PositiveIntegerField | No | 0 | No |
| projects_count | PositiveIntegerField | No | 0 | No |
| join_date | DateField | No | - | No |
| is_active | BooleanField | No | True | No |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `project_memberships` (from research.ProjectTeamMember)
- `led_experiments` (from research.ResearchExperiment)
- `experiment_participations` (from research.ExperimentParticipant)
- `verified_results` (from research.ExperimentResult)
- `recorded_results` (from research.ExperimentResult)
- `publications` (from research.PublicationAuthor)
- `patents` (from research.PatentInventor)
- `led_grants` (from research.ResearchGrant)
- `responsible_for_equipment` (from research.ResearchEquipment)
- `reviewed_reports` (from research.ResearchReport)
- `user` (from users.User)

---

### ResearchExperiment

**Table**: `research_researchexperiment`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| code | CharField | No | - | No |
| project | ForeignKey | No | - | Yes |
| description | TextField | No | - | No |
| protocol | TextField | No | - | No |
| status | CharField | No | PLANNED | No |
| start_date | DateField | Yes | - | No |
| end_date | DateField | Yes | - | No |
| lead_researcher | ForeignKey | No | - | Yes |
| location | CharField | Yes | - | No |
| materials_used | TextField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |
| equipment_used | ManyToManyField | No | - | No |

**Foreign Keys**:

- `project` → research.ResearchProject
- `lead_researcher` → research.Researcher
- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `participants` (from research.ExperimentParticipant)
- `results` (from research.ExperimentResult)

---

### ResearchGrant

**Table**: `research_researchgrant`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| grant_id | CharField | No | - | No |
| funding_agency | CharField | No | - | No |
| amount | DecimalField | No | - | No |
| currency | CharField | No | EGP | No |
| status | CharField | No | DRAFT | No |
| submission_date | DateField | Yes | - | No |
| start_date | DateField | Yes | - | No |
| end_date | DateField | Yes | - | No |
| principal_investigator | ForeignKey | No | - | Yes |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |
| projects | ManyToManyField | No | - | No |
| co_investigators | ManyToManyField | No | - | No |

**Foreign Keys**:

- `principal_investigator` → research.Researcher
- `created_by` → users.User
- `updated_by` → users.User

---

### ResearchObjective

**Table**: `research_researchobjective`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| project | ForeignKey | No | - | Yes |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| success_criteria | TextField | No | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `project` → research.ResearchProject
- `created_by` → users.User

---

### ResearchProject

**Table**: `research_researchproject`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| description | TextField | No | - | No |
| objectives | TextField | No | - | No |
| status | CharField | No | PROPOSED | No |
| start_date | DateField | Yes | - | No |
| expected_end_date | DateField | Yes | - | No |
| actual_end_date | DateField | Yes | - | No |
| budget | DecimalField | Yes | - | No |
| funding_source | CharField | Yes | - | No |
| principal_investigator | ForeignKey | No | - | Yes |
| collaborating_institutions | TextField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |
| title | CharField | No | - | No |
| priority | CharField | No | MEDIUM | No |
| keywords | TextField | Yes | - | No |
| status_notes | TextField | Yes | - | No |
| end_date | DateField | Yes | - | No |

**Foreign Keys**:

- `principal_investigator` → users.User
- `created_by` → users.User
- `updated_by` → users.User

**Reverse Relations**:

- `team_members` (from research.ProjectTeamMember)
- `experiments` (from research.ResearchExperiment)
- `reports` (from research.ResearchReport)
- `research_objectives_compat` (from research.ResearchObjective)
- `research_team` (from research.ResearchTeamMember)
- `tasks` (from research.ResearchTask)

---

### ResearchReport

**Table**: `research_researchreport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| title | CharField | No | - | No |
| project | ForeignKey | No | - | Yes |
| report_type | CharField | No | - | No |
| status | CharField | No | DRAFT | No |
| submission_date | DateField | Yes | - | No |
| period_start | DateField | Yes | - | No |
| period_end | DateField | Yes | - | No |
| content | TextField | No | - | No |
| summary | TextField | No | - | No |
| conclusions | TextField | Yes | - | No |
| recommendations | TextField | Yes | - | No |
| reviewer | ForeignKey | Yes | - | Yes |
| review_date | DateField | Yes | - | No |
| review_comments | TextField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `project` → research.ResearchProject
- `reviewer` → research.Researcher
- `created_by` → users.User
- `updated_by` → users.User

---

### ResearchTask

**Table**: `research_researchtask`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| project | ForeignKey | No | - | Yes |
| title | CharField | No | - | No |
| description | TextField | No | - | No |
| start_date | DateField | Yes | - | No |
| due_date | DateField | Yes | - | No |
| status | CharField | No | TODO | No |
| priority | CharField | No | MEDIUM | No |
| assigned_to | ForeignKey | Yes | - | Yes |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `project` → research.ResearchProject
- `assigned_to` → users.User
- `created_by` → users.User

---

### ResearchTeamMember

**Table**: `research_researchteammember`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| project | ForeignKey | No | - | Yes |
| user | ForeignKey | No | - | Yes |
| role | CharField | No | RESEARCHER | No |
| responsibilities | TextField | No | - | No |
| created_by | ForeignKey | No | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `project` → research.ResearchProject
- `user` → users.User
- `created_by` → users.User

**Unique Together**:

- (project, user)

---

## sales

### Customer

**Table**: `sales_customer`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| customer_type | CharField | No | individual | No |
| company | ForeignKey | No | - | Yes |
| branch | ForeignKey | No | - | Yes |
| address | TextField | Yes | - | No |
| city | CharField | Yes | - | No |
| country | CharField | Yes | - | No |
| phone | CharField | Yes | - | No |
| mobile | CharField | Yes | - | No |
| email | CharField | Yes | - | No |
| website | CharField | Yes | - | No |
| tax_id | CharField | Yes | - | No |
| credit_limit | DecimalField | No | 0 | No |
| payment_term | IntegerField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| notes | TextField | Yes | - | No |

**Foreign Keys**:

- `company` → core.Company
- `branch` → core.Branch

**Reverse Relations**:

- `sales_invoices` (from sales.SalesInvoice)
- `orders` (from sales.SalesOrder)
- `sales_returns` (from sales.SalesReturn)

**Indexes**:

- sales_custo_name_980413_idx: (name)
- sales_custo_company_48d7f1_idx: (company)
- sales_custo_is_acti_1b1d19_idx: (is_active)
- sales_custo_custome_890109_idx: (customer_type)

**Unique Together**:

- (name, company)

---

### Discount

**Table**: `sales_discount`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

### PaymentTerm

**Table**: `sales_paymentterm`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| days | IntegerField | No | 0 | No |

**Reverse Relations**:

- `sales_orders` (from sales.SalesOrder)

---

### PriceList

**Table**: `sales_pricelist`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| price_list_type | CharField | No | sale | No |
| start_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| end_date | DateField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| description | TextField | No | - | No |

**Foreign Keys**:

- `company` → core.Company

**Reverse Relations**:

- `items` (from sales.PriceListItem)

**Indexes**:

- sales_price_code_8c799f_idx: (code)
- sales_price_company_9ea25b_idx: (company)
- sales_price_is_acti_3e3141_idx: (is_active)
- sales_price_start_d_6facd2_idx: (start_date)
- sales_price_end_dat_78ebba_idx: (end_date)

**Unique Together**:

- (code, company)

---

### PriceListItem

**Table**: `sales_pricelistitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| price_list | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| price | DecimalField | No | - | No |
| min_quantity | DecimalField | No | 1 | No |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `price_list` → sales.PriceList
- `product` → inventory.Product

**Indexes**:

- sales_price_price_l_a0af90_idx: (price_list)
- sales_price_product_294cb0_idx: (product)
- sales_price_min_qua_868dc8_idx: (-min_quantity)

**Unique Together**:

- (price_list, product, min_quantity)

---

### SalesInvoice

**Table**: `sales_salesinvoice`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| invoice_number | CharField | No | - | No |
| customer | ForeignKey | No | - | Yes |
| invoice_date | DateField | No | - | No |
| due_date | DateField | No | - | No |
| status | CharField | No | draft | No |
| total_amount | DecimalField | No | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| created_by | ForeignKey | No | - | Yes |
| parent_invoice | ForeignKey | Yes | - | Yes |
| is_parent_consolidated | BooleanField | No | False | No |

**Foreign Keys**:

- `customer` → sales.Customer
- `created_by` → users.User
- `parent_invoice` → sales.SalesInvoice

**Reverse Relations**:

- `child_invoices` (from sales.SalesInvoice)
- `items` (from sales.SalesInvoiceItem)
- `sales_returns` (from sales.SalesReturn)

---

### SalesInvoiceItem

**Table**: `sales_salesinvoiceitem`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| invoice | ForeignKey | No | - | Yes |
| description | CharField | No | - | No |
| quantity | DecimalField | No | - | No |
| unit_price | DecimalField | No | - | No |
| discount | DecimalField | No | 0.00 | No |
| tax_rate | DecimalField | No | 0.00 | No |
| total_price | DecimalField | No | 0.00 | No |
| product_reference | CharField | Yes | - | No |

**Foreign Keys**:

- `invoice` → sales.SalesInvoice

**Reverse Relations**:

- `return_lines` (from sales.SalesReturnLine)

---

### SalesOrder

**Table**: `sales_salesorder`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| order_number | CharField | No | - | No |
| reference | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| customer | ForeignKey | No | - | Yes |
| order_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| validity_date | DateField | Yes | - | No |
| expected_delivery_date | DateField | Yes | - | No |
| payment_term | ForeignKey | Yes | - | Yes |
| untaxed_amount | DecimalField | No | 0 | No |
| tax_amount | DecimalField | No | 0 | No |
| total_amount | DecimalField | No | 0 | No |
| state | CharField | No | draft | No |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `company` → core.Company
- `customer` → sales.Customer
- `payment_term` → sales.PaymentTerm

---

### SalesReturn

**Table**: `sales_salesreturn`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| reference | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| customer | ForeignKey | No | - | Yes |
| invoice | ForeignKey | Yes | - | Yes |
| date | DateField | No | <function now at 0x00000247D3A64680> | No |
| untaxed_amount | DecimalField | No | 0 | No |
| tax_amount | DecimalField | No | 0 | No |
| total_amount | DecimalField | No | 0 | No |
| state | CharField | No | draft | No |
| return_reason | CharField | No | other | No |
| created_by | ForeignKey | Yes | - | Yes |
| posted_by | ForeignKey | Yes | - | Yes |
| cancelled_by | ForeignKey | Yes | - | Yes |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `company` → core.Company
- `customer` → sales.Customer
- `invoice` → sales.SalesInvoice
- `created_by` → users.User
- `posted_by` → users.User
- `cancelled_by` → users.User

**Reverse Relations**:

- `lines` (from sales.SalesReturnLine)

**Unique Together**:

- (reference, company)

---

### SalesReturnLine

**Table**: `sales_salesreturnline`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| return_order | ForeignKey | No | - | Yes |
| product | ForeignKey | No | - | Yes |
| invoice_line | ForeignKey | Yes | - | Yes |
| quantity | DecimalField | No | 1 | No |
| unit_price | DecimalField | No | 0 | No |
| discount_percent | DecimalField | No | 0 | No |
| discount_amount | DecimalField | No | 0 | No |
| tax_amount | DecimalField | No | 0 | No |
| subtotal | DecimalField | No | 0 | No |
| total | DecimalField | No | 0 | No |
| description | TextField | No | - | No |
| sequence | PositiveIntegerField | No | 10 | No |

**Foreign Keys**:

- `return_order` → sales.SalesReturn
- `product` → inventory.Product
- `invoice_line` → sales.SalesInvoiceItem

---

### SalesTarget

**Table**: `sales_salestarget`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| team | ForeignKey | Yes | - | Yes |
| user | ForeignKey | Yes | - | Yes |
| start_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| end_date | DateField | No | - | No |
| target_type | CharField | No | revenue | No |
| target_amount | DecimalField | No | - | No |
| description | TextField | No | - | No |

**Foreign Keys**:

- `company` → core.Company
- `team` → sales.SalesTeam
- `user` → users.User

**Indexes**:

- sales_sales_company_791950_idx: (company)
- sales_sales_start_d_41e25d_idx: (start_date)
- sales_sales_end_dat_384e1e_idx: (end_date)
- sales_sales_target__e06860_idx: (target_type)

---

### SalesTeam

**Table**: `sales_salesteam`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| code | CharField | No | - | No |
| company | ForeignKey | No | - | Yes |
| leader | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| description | TextField | No | - | No |
| members | ManyToManyField | No | - | No |

**Foreign Keys**:

- `company` → core.Company
- `leader` → users.User

**Reverse Relations**:

- `targets` (from sales.SalesTarget)

**Indexes**:

- sales_sales_code_b26607_idx: (code)
- sales_sales_company_caf73e_idx: (company)
- sales_sales_is_acti_45b30c_idx: (is_active)

**Unique Together**:

- (code, company)

---

### Tax

**Table**: `sales_tax`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| rate | DecimalField | No | - | No |

---

## security

### AuditLog

**Table**: `security_auditlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| user | ForeignKey | Yes | - | Yes |
| action | CharField | No | - | No |
| model_name | CharField | No | - | No |
| object_id | CharField | No | - | No |
| object_repr | CharField | No | - | No |
| changes | JSONField | No | <class 'dict'> | No |
| ip_address | GenericIPAddressField | No | - | No |
| user_agent | TextField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |

**Foreign Keys**:

- `user` → users.User

**Indexes**:

- security_au_user_id_88bbbb_idx: (user, timestamp)
- security_au_action_85f886_idx: (action, timestamp)
- security_au_model_n_ae2821_idx: (model_name, timestamp)
- security_au_ip_addr_f227e7_idx: (ip_address, timestamp)

---

### IPBlacklist

**Table**: `security_ipblacklist`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| ip_address | GenericIPAddressField | No | - | No |
| reason | CharField | No | - | No |
| description | TextField | No | - | No |
| blocked_by | ForeignKey | Yes | - | Yes |
| blocked_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| expires_at | DateTimeField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `blocked_by` → users.User

**Indexes**:

- security_ip_ip_addr_e6acc0_idx: (ip_address, is_active)
- security_ip_blocked_bf99f3_idx: (blocked_at)
- security_ip_expires_89f688_idx: (expires_at)

---

### LoginAttempt

**Table**: `security_loginattempt`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| username | CharField | No | - | No |
| ip_address | GenericIPAddressField | No | - | No |
| user_agent | TextField | No | - | No |
| success | BooleanField | No | - | No |
| failure_reason | CharField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| session_key | CharField | No | - | No |

**Indexes**:

- security_lo_usernam_140da1_idx: (username, timestamp)
- security_lo_ip_addr_7bfc42_idx: (ip_address, timestamp)
- security_lo_success_771bf8_idx: (success, timestamp)

---

### SecurityEvent

**Table**: `security_securityevent`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| user | ForeignKey | Yes | - | Yes |
| event_type | CharField | No | - | No |
| severity | CharField | No | low | No |
| ip_address | GenericIPAddressField | No | - | No |
| user_agent | TextField | No | - | No |
| description | TextField | No | - | No |
| additional_data | JSONField | No | <class 'dict'> | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| resolved | BooleanField | No | False | No |
| resolved_by | ForeignKey | Yes | - | Yes |
| resolved_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `user` → users.User
- `resolved_by` → users.User

**Indexes**:

- security_se_event_t_1a00f0_idx: (event_type, timestamp)
- security_se_user_id_6ceb62_idx: (user, timestamp)
- security_se_ip_addr_7e6b32_idx: (ip_address, timestamp)
- security_se_severit_d0a5b5_idx: (severity, resolved)

---

### SecuritySettings

**Table**: `security_securitysettings`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| user | OneToOneField | No | - | Yes |
| password_expiry_days | PositiveIntegerField | No | 90 | No |
| require_password_change | BooleanField | No | False | No |
| last_password_change | DateTimeField | Yes | - | No |
| session_timeout_minutes | PositiveIntegerField | No | 60 | No |
| max_concurrent_sessions | PositiveIntegerField | No | 3 | No |
| email_security_alerts | BooleanField | No | True | No |
| sms_security_alerts | BooleanField | No | False | No |
| allowed_ip_addresses | JSONField | No | <class 'list'> | No |
| blocked_countries | JSONField | No | <class 'list'> | No |
| created_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `user` (from users.User)

---

### TwoFactorAuth

**Table**: `security_twofactorauth`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| user | OneToOneField | No | - | Yes |
| is_enabled | BooleanField | No | False | No |
| method | CharField | No | sms | No |
| secret_key | CharField | No | - | No |
| backup_codes | JSONField | No | <class 'list'> | No |
| phone_number | CharField | No | - | No |
| last_used | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |

**Reverse Relations**:

- `user` (from users.User)

---

## seed_production

### InventoryVerification

**Table**: `seed_production_inventoryverification`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| company | ForeignKey | Yes | - | Yes |
| verification_date | DateTimeField | No | - | No |
| verified_by | CharField | No | - | No |
| status | CharField | No | pending | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company

---

### LotChangeLog

**Table**: `seed_production_lotchangelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| company | ForeignKey | Yes | - | Yes |
| lot_number | CharField | No | - | No |
| change_type | CharField | No | - | No |
| change_date | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company

---

### SeedInventoryMovement

**Table**: `seed_production_seedinventorymovement`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| seed_lot | ForeignKey | No | - | Yes |
| movement_type | CharField | No | - | No |
| movement_date | DateField | No | - | No |
| quantity_kg | DecimalField | No | - | No |
| reference_lot | ForeignKey | Yes | - | Yes |
| notes | TextField | Yes | - | No |
| performed_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `seed_lot` → seed_production.SeedProductionLot
- `reference_lot` → inventory.Lot
- `performed_by` → users.User

---

### SeedLotTest

**Table**: `seed_production_seedlottest`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| seed_lot | ForeignKey | No | - | Yes |
| test_type | CharField | No | - | No |
| test_date | DateField | No | <function now at 0x00000247D3A64680> | No |
| result | CharField | No | PENDING | No |
| notes | TextField | Yes | - | No |
| result_value | CharField | Yes | - | No |
| tested_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `seed_lot` → seed_production.SeedProductionLot
- `tested_by` → users.User

---

### SeedPackaging

**Table**: `seed_production_seedpackaging`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| company | ForeignKey | Yes | - | Yes |
| package_type | CharField | No | - | No |
| package_size | DecimalField | No | - | No |
| packaging_date | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company

---

### SeedProductionActivity

**Table**: `seed_production_seedproductionactivity`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| seed_lot | ForeignKey | No | - | Yes |
| activity_type | CharField | No | - | No |
| activity_date | DateField | No | - | No |
| description | TextField | No | - | No |
| performed_by | ForeignKey | Yes | - | Yes |
| materials_used | TextField | Yes | - | No |
| quantity_used | CharField | Yes | - | No |
| notes | TextField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `seed_lot` → seed_production.SeedProductionLot
- `performed_by` → users.User

---

### SeedProductionLot

**Table**: `seed_production_seedproductionlot`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| lot_number | CharField | No | - | No |
| production_order | ForeignKey | Yes | - | Yes |
| product | ForeignKey | No | - | Yes |
| branch | ForeignKey | Yes | - | Yes |
| status | CharField | No | PLANNED | No |
| parent_male_code | CharField | Yes | - | No |
| parent_female_code | CharField | Yes | - | No |
| is_parent_info_restricted | BooleanField | No | True | No |
| production_location_code | CharField | Yes | - | No |
| planned_planting_date | DateField | Yes | - | No |
| expected_production_date | DateField | Yes | - | No |
| expected_seed_quantity_kg | DecimalField | Yes | - | No |
| actual_planting_date | DateField | Yes | - | No |
| actual_harvest_date | DateField | Yes | - | No |
| harvested_quantity_kg | DecimalField | Yes | - | No |
| seeds_per_gram | DecimalField | Yes | - | No |
| treatment_material | CharField | Yes | - | No |
| treatment_date | DateField | Yes | - | No |
| germination_rate_percent | DecimalField | Yes | - | No |
| hybrid_purity_percent | DecimalField | Yes | - | No |
| passed_all_tests | BooleanField | Yes | - | No |
| origin_country | CharField | Yes | - | No |
| agricultural_certificate_number | CharField | Yes | - | No |
| final_lot_number | CharField | Yes | - | No |
| packaged_product_name | CharField | Yes | - | No |
| packaging_date | DateField | Yes | - | No |
| responsible_person | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `production_order` → seed_production.SeedProductionOrder
- `product` → inventory.Product
- `branch` → core.Branch
- `responsible_person` → users.User
- `created_by` → users.User

**Reverse Relations**:

- `tests` (from seed_production.SeedLotTest)
- `activities` (from seed_production.SeedProductionActivity)
- `inventory_movements` (from seed_production.SeedInventoryMovement)

---

### SeedProductionOrder

**Table**: `seed_production_seedproductionorder`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| updated_by | ForeignKey | Yes | - | Yes |
| order_number | CharField | No | - | No |
| product | ForeignKey | No | - | Yes |
| target_quantity_kg | DecimalField | No | - | No |
| parent_male_code | CharField | No | - | No |
| parent_male_quantity_kg | DecimalField | No | - | No |
| parent_female_code | CharField | No | - | No |
| parent_female_quantity_kg | DecimalField | No | - | No |
| branch | ForeignKey | Yes | - | Yes |
| production_location_code | CharField | No | - | No |
| planned_start_date | DateField | No | - | No |
| planned_end_date | DateField | No | - | No |
| status | CharField | No | DRAFT | No |
| notes | TextField | Yes | - | No |
| inventory_verified | BooleanField | No | False | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| assigned_to | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `updated_by` → users.User
- `product` → inventory.Product
- `branch` → core.Branch
- `created_by` → users.User
- `assigned_to` → users.User

**Reverse Relations**:

- `production_lots` (from seed_production.SeedProductionLot)

---

### SeedProductionPlan

**Table**: `seed_production_seedproductionplan`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| company | ForeignKey | Yes | - | Yes |
| plan_name | CharField | No | - | No |
| start_date | DateField | No | - | No |
| end_date | DateField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company

---

### SeedTreatmentLog

**Table**: `seed_production_seedtreatmentlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| is_active | BooleanField | No | True | No |
| company | ForeignKey | Yes | - | Yes |
| treatment_type | CharField | No | - | No |
| treatment_date | DateTimeField | No | - | No |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User
- `company` → core.Company

---

## sessions

### Session

**Table**: `django_session`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| session_key | CharField | No | - | No |
| session_data | TextField | No | - | No |
| expire_date | DateTimeField | No | - | Yes |

---

## setup

### CompanySettings

**Table**: `setup_companysettings`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| email | CharField | Yes | - | No |
| phone | CharField | Yes | - | No |
| address | CharField | Yes | - | No |
| tax_id | CharField | Yes | - | No |
| base_currency | CharField | No | USD | No |
| default_language | CharField | No | en | No |
| timezone | CharField | No | UTC | No |

---

### SetupWizardSession

**Table**: `setup_setupwizardsession`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| user | ForeignKey | No | - | Yes |
| current_step | CharField | No | welcome | No |
| completed_steps | JSONField | No | <class 'list'> | No |
| session_data | JSONField | No | <class 'dict'> | No |
| is_active | BooleanField | No | True | No |
| is_completed | BooleanField | No | False | No |
| started_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| completed_at | DateTimeField | Yes | - | No |

**Foreign Keys**:

- `user` → users.User

---

### SystemBackup

**Table**: `setup_systembackup`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| backup_type | CharField | No | manual | No |
| status | CharField | No | pending | No |
| file | FileField | Yes | - | No |
| file_size | PositiveBigIntegerField | Yes | - | No |
| backup_date | DateTimeField | Yes | - | No |
| database_version | CharField | Yes | - | No |
| system_version | CharField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### SystemInstallationStatus

**Table**: `setup_systeminstallationstatus`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| status | CharField | No | not_installed | No |
| version | CharField | No | 1.0.0 | No |
| installed_at | DateTimeField | Yes | - | No |
| installed_by | ForeignKey | Yes | - | Yes |
| last_upgrade_at | DateTimeField | Yes | - | No |
| installation_log | TextField | No | - | No |

**Foreign Keys**:

- `installed_by` → users.User

---

### SystemScheduledTask

**Table**: `setup_systemscheduledtask`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| task_type | CharField | No | - | No |
| command | CharField | No | - | No |
| frequency | CharField | No | daily | No |
| cron_expression | CharField | Yes | - | No |
| status | CharField | No | active | No |
| last_run | DateTimeField | Yes | - | No |
| next_run | DateTimeField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

---

### SystemSetting

**Table**: `setup_systemsetting`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| key | CharField | No | - | No |
| value | TextField | Yes | - | No |
| value_type | CharField | No | string | No |
| category | CharField | No | general | No |
| description | TextField | Yes | - | No |
| is_public | BooleanField | No | False | No |
| is_system | BooleanField | No | False | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User

---

### SystemTheme

**Table**: `setup_systemtheme`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | Yes | - | No |
| primary_color | CharField | No | #3498db | No |
| secondary_color | CharField | No | #2ecc71 | No |
| accent_color | CharField | No | #e74c3c | No |
| background_color | CharField | No | #f5f5f5 | No |
| text_color | CharField | No | #333333 | No |
| font_family_arabic | CharField | No | Cairo, sans-serif | No |
| font_family_english | CharField | No | Roboto, sans-serif | No |
| logo | FileField | Yes | - | No |
| favicon | FileField | Yes | - | No |
| login_background | FileField | Yes | - | No |
| custom_css | TextField | Yes | - | No |
| is_active | BooleanField | No | False | No |
| is_system | BooleanField | No | False | No |
| created_by | ForeignKey | Yes | - | Yes |
| updated_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User
- `updated_by` → users.User

---

## setup_wizard

### SetupConfiguration

**Table**: `setup_wizard_setupconfiguration`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| setup_complete | BooleanField | No | False | No |
| email_host | CharField | Yes | - | No |
| email_port | PositiveIntegerField | Yes | 587 | No |
| email_host_user | CharField | Yes | - | No |
| email_host_password | CharField | Yes | - | No |
| email_use_tls | BooleanField | No | True | No |
| email_use_ssl | BooleanField | No | False | No |
| default_from_email | CharField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

## system_backups

### BackupConfiguration

**Table**: `system_backups_backupconfiguration`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| is_active | BooleanField | No | True | No |
| is_default | BooleanField | No | False | No |
| storage_type | CharField | No | local | No |
| local_storage_path | CharField | No | - | No |
| cloud_provider | CharField | Yes | - | No |
| cloud_bucket | CharField | No | - | No |
| cloud_prefix | CharField | No | - | No |
| cloud_credentials | JSONField | No | <class 'dict'> | No |
| compression_type | CharField | No | gzip | No |
| encryption_enabled | BooleanField | No | False | No |
| encryption_key | CharField | No | - | No |
| retention_days | PositiveIntegerField | No | 30 | No |
| max_backups | PositiveIntegerField | No | 10 | No |
| notify_on_success | BooleanField | No | False | No |
| notify_on_failure | BooleanField | No | True | No |
| notification_emails | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `schedules` (from system_backups.BackupSchedule)
- `backup_logs` (from system_backups.BackupLog)

**Indexes**:

- system_back_is_defa_f1603f_idx: (is_default)
- system_back_is_acti_d1bf31_idx: (is_active)

---

### BackupLog

**Table**: `system_backups_backuplog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| configuration | ForeignKey | Yes | - | Yes |
| schedule | ForeignKey | Yes | - | Yes |
| backup_type | CharField | No | full | No |
| trigger_type | CharField | No | manual | No |
| status | CharField | No | pending | Yes |
| storage_location | CharField | No | - | No |
| started_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| completed_at | DateTimeField | Yes | - | No |
| duration_seconds | PositiveIntegerField | Yes | - | No |
| local_path | CharField | Yes | - | No |
| cloud_url | CharField | Yes | - | No |
| file_size | BigIntegerField | Yes | - | No |
| message | TextField | No | - | No |
| is_encrypted | BooleanField | No | False | No |
| is_compressed | BooleanField | No | True | No |
| compression_type | CharField | No | gzip | No |
| expiry_date | DateField | Yes | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `configuration` → system_backups.BackupConfiguration
- `schedule` → system_backups.BackupSchedule
- `created_by` → users.User

**Reverse Relations**:

- `restore_logs` (from system_backups.RestoreLog)

**Indexes**:

- system_back_status_1fa00a_idx: (status)
- system_back_started_e35578_idx: (-started_at)
- system_back_backup__d29456_idx: (backup_type)
- system_back_trigger_8e1128_idx: (trigger_type)
- system_back_expiry__91c68f_idx: (expiry_date)

---

### BackupSchedule

**Table**: `system_backups_backupschedule`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| description | TextField | No | - | No |
| configuration | ForeignKey | No | - | Yes |
| backup_type | CharField | No | full | No |
| frequency | CharField | No | daily | No |
| hour | PositiveSmallIntegerField | No | 0 | No |
| minute | PositiveSmallIntegerField | No | 0 | No |
| day_of_week | PositiveSmallIntegerField | Yes | - | No |
| day_of_month | PositiveSmallIntegerField | Yes | - | No |
| cron_expression | CharField | No | - | No |
| is_active | BooleanField | No | True | No |
| last_run | DateTimeField | Yes | - | No |
| next_run | DateTimeField | Yes | - | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `configuration` → system_backups.BackupConfiguration
- `created_by` → users.User

**Reverse Relations**:

- `backup_logs` (from system_backups.BackupLog)

**Indexes**:

- system_back_is_acti_bb799d_idx: (is_active)
- system_back_frequen_940590_idx: (frequency)
- system_back_next_ru_99944a_idx: (next_run)

---

### RestoreLog

**Table**: `system_backups_restorelog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| name | CharField | No | - | No |
| source_backup | ForeignKey | No | - | Yes |
| restore_type | CharField | No | full | No |
| trigger_type | CharField | No | manual | No |
| status | CharField | No | pending | Yes |
| started_at | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| completed_at | DateTimeField | Yes | - | No |
| duration_seconds | PositiveIntegerField | Yes | - | No |
| message | TextField | No | - | No |
| is_overwrite | BooleanField | No | False | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `source_backup` → system_backups.BackupLog
- `created_by` → users.User

**Indexes**:

- system_back_status_dd462b_idx: (status)
- system_back_started_578f4e_idx: (-started_at)
- system_back_restore_084ff0_idx: (restore_type)
- system_back_trigger_525319_idx: (trigger_type)

---

## system_monitoring

### Alert

**Table**: `system_monitoring_alert`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| alert_type | CharField | No | - | No |
| severity | CharField | No | - | No |
| message | TextField | No | - | No |
| source | CharField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| status | CharField | No | ACTIVE | No |
| acknowledged_by | ForeignKey | Yes | - | Yes |
| acknowledged_at | DateTimeField | Yes | - | No |
| resolved_at | DateTimeField | Yes | - | No |
| resolution_notes | TextField | No | - | No |
| related_metric | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `acknowledged_by` → users.User
- `related_metric` → system_monitoring.SystemMetric

**Indexes**:

- system_moni_timesta_09115f_idx: (timestamp, status)
- system_moni_status_3c56e7_idx: (status)
- system_moni_severit_79964a_idx: (severity)
- system_moni_alert_t_699a08_idx: (alert_type)
- system_moni_source_d9041f_idx: (source)

---

### ModuleStatus

**Table**: `system_monitoring_modulestatus`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| module_name | CharField | No | - | No |
| display_name | CharField | No | - | No |
| status | CharField | No | UNKNOWN | No |
| cpu_usage_percent | FloatField | Yes | - | No |
| memory_usage_mb | FloatField | Yes | - | No |
| disk_usage_mb | FloatField | Yes | - | No |
| response_time_ms | FloatField | Yes | - | No |
| active_users | PositiveIntegerField | Yes | - | No |
| last_error_message | TextField | No | - | No |
| last_error_timestamp | DateTimeField | Yes | - | No |
| last_heartbeat | DateTimeField | Yes | - | No |
| version | CharField | No | - | No |

---

### SystemMetric

**Table**: `system_monitoring_systemmetric`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| metric_name | CharField | No | - | No |
| metric_type | CharField | No | - | No |
| value | FloatField | No | - | No |
| unit | CharField | No | - | No |
| timestamp | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| source | CharField | No | - | No |

**Reverse Relations**:

- `alerts` (from system_monitoring.Alert)

**Indexes**:

- system_moni_timesta_79621f_idx: (timestamp, metric_type, metric_name)
- system_moni_metric__793621_idx: (metric_type)
- system_moni_source_8f7c2e_idx: (source)

---

## token_blacklist

### BlacklistedToken

**Table**: `token_blacklist_blacklistedtoken`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| token | OneToOneField | No | - | Yes |
| blacklisted_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `token` (from token_blacklist.OutstandingToken)

---

### OutstandingToken

**Table**: `token_blacklist_outstandingtoken`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | Yes | - | Yes |
| jti | CharField | No | - | No |
| token | TextField | No | - | No |
| created_at | DateTimeField | Yes | - | No |
| expires_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

**Reverse Relations**:

- `blacklistedtoken` (from token_blacklist.BlacklistedToken)

---

## translation

### TranslationService

**Table**: `translation_translationservice`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| service_id | UUIDField | No | <function uuid4 at 0x00000247D394F380> | No |
| name | CharField | No | - | No |
| service_type | CharField | No | - | No |
| api_key | CharField | No | - | No |
| api_endpoint | CharField | No | - | No |
| supported_languages | JSONField | No | <class 'list'> | No |
| characters_translated | BigIntegerField | No | 0 | No |
| translation_requests | PositiveIntegerField | No | 0 | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

---

## users

### User

**Table**: `users_user`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| password | CharField | No | - | No |
| is_superuser | BooleanField | No | False | No |
| email | CharField | No | - | No |
| username | CharField | No | - | No |
| first_name | CharField | No | - | No |
| last_name | CharField | No | - | No |
| is_active | BooleanField | No | True | No |
| is_staff | BooleanField | No | False | No |
| date_joined | DateTimeField | No | <function now at 0x00000247D3A64680> | No |
| last_login | DateTimeField | Yes | - | No |
| phone | CharField | Yes | - | No |
| title | CharField | Yes | - | No |
| department | CharField | Yes | - | No |
| employee_id | CharField | Yes | - | No |
| mobile | CharField | Yes | - | No |
| pending_password | CharField | Yes | - | No |
| password_reset_status | CharField | No | none | No |
| password_reset_requested_at | DateTimeField | Yes | - | No |
| password_reset_approved_at | DateTimeField | Yes | - | No |
| password_reset_approved_by | ForeignKey | Yes | - | Yes |
| email_verified | BooleanField | No | False | No |
| phone_verified | BooleanField | No | False | No |
| failed_login_attempts | PositiveIntegerField | No | 0 | No |
| last_failed_login | DateTimeField | Yes | - | No |
| account_locked_until | DateTimeField | Yes | - | No |
| password_changed_at | DateTimeField | Yes | - | No |
| language | CharField | No | ar | No |
| timezone | CharField | No | Africa/Cairo | No |
| groups | ManyToManyField | No | - | No |
| user_permissions | ManyToManyField | No | - | No |
| user_countries | ManyToManyField | No | - | No |
| user_companies | ManyToManyField | No | - | No |
| user_branches | ManyToManyField | No | - | No |

**Foreign Keys**:

- `password_reset_approved_by` → users.User

**Reverse Relations**:

- `logentry` (from admin.LogEntry)
- `outstandingtoken` (from token_blacklist.OutstandingToken)
- `company_created_by` (from core.Company)
- `company_updated_by` (from core.Company)
- `branch_created_by` (from core.Branch)
- `branch_updated_by` (from core.Branch)
- `department_created_by` (from core.Department)
- `department_updated_by` (from core.Department)
- `apikey_created_by` (from core.APIKey)
- `apikey_updated_by` (from core.APIKey)
- `core_api_keys` (from core.APIKey)
- `apikeylog_created_by` (from core.APIKeyLog)
- `apikeylog_updated_by` (from core.APIKeyLog)
- `approved_password_resets` (from users.User)
- `profile` (from users.UserProfile)
- `settings` (from users.UserSettings)
- `devices` (from users.UserDevice)
- `sessions` (from users.UserSession)
- `activities` (from users.UserActivity)
- `user_notification_preferences` (from users.UserNotificationPreference)
- `user_api_keys` (from users.UserAPIKey)
- `securityevent` (from security.SecurityEvent)
- `resolved_security_events` (from security.SecurityEvent)
- `ipblacklist` (from security.IPBlacklist)
- `twofactorauth` (from security.TwoFactorAuth)
- `securitysettings` (from security.SecuritySettings)
- `auditlog` (from security.AuditLog)
- `performancemetric` (from performance.PerformanceMetric)
- `databaseperformance` (from performance.DatabasePerformance)
- `apiperformance` (from performance.APIPerformance)
- `performanceoptimization` (from performance.PerformanceOptimization)
- `granted_user_permissions` (from permissions.UserRolePermission)
- `user_role_assignments` (from permissions.UserRoleAssignment)
- `assigned_user_roles` (from permissions.UserRoleAssignment)
- `granted_ai_permissions` (from permissions.AIRolePermission)
- `owned_ai_agents` (from permissions.AIAgent)
- `assigned_ai_roles` (from permissions.AIAgentRoleAssignment)
- `permission_audit_logs` (from permissions.PermissionAuditLog)
- `aiagent` (from ai_permissions.AIAgent)
- `agentrole` (from ai_permissions.AgentRole)
- `aipermissionauditlog` (from ai_permissions.AIPermissionAuditLog)
- `queryoptimization` (from database_optimization.QueryOptimization)
- `created_settings` (from setup.SystemSetting)
- `updated_settings` (from setup.SystemSetting)
- `created_themes` (from setup.SystemTheme)
- `updated_themes` (from setup.SystemTheme)
- `created_backups` (from setup.SystemBackup)
- `created_tasks` (from setup.SystemScheduledTask)
- `setup_sessions` (from setup.SetupWizardSession)
- `installations` (from setup.SystemInstallationStatus)
- `accounttype_created_by` (from accounting.AccountType)
- `accounttype_updated_by` (from accounting.AccountType)
- `currency_created_by` (from accounting.Currency)
- `currency_updated_by` (from accounting.Currency)
- `account_created_by` (from accounting.Account)
- `account_updated_by` (from accounting.Account)
- `fiscalyear_created_by` (from accounting.FiscalYear)
- `fiscalyear_updated_by` (from accounting.FiscalYear)
- `fiscalperiod_created_by` (from accounting.FiscalPeriod)
- `fiscalperiod_updated_by` (from accounting.FiscalPeriod)
- `journal_created_by` (from accounting.Journal)
- `journal_updated_by` (from accounting.Journal)
- `journalentry_created_by` (from accounting.JournalEntry)
- `journalentry_updated_by` (from accounting.JournalEntry)
- `posted_entries` (from accounting.JournalEntry)
- `journalentryline_created_by` (from accounting.JournalEntryLine)
- `journalentryline_updated_by` (from accounting.JournalEntryLine)
- `analyticaccount_created_by` (from accounting.AnalyticAccount)
- `analyticaccount_updated_by` (from accounting.AnalyticAccount)
- `tax_created_by` (from accounting.Tax)
- `tax_updated_by` (from accounting.Tax)
- `created_settlements` (from accounting.Settlement)
- `confirmed_settlements` (from accounting.Settlement)
- `cancelled_settlements` (from accounting.Settlement)
- `created_sales_invoices` (from sales.SalesInvoice)
- `created_sales_returns` (from sales.SalesReturn)
- `posted_sales_returns` (from sales.SalesReturn)
- `cancelled_sales_returns` (from sales.SalesReturn)
- `led_sales_teams` (from sales.SalesTeam)
- `sales_targets` (from sales.SalesTarget)
- `created_purchase_orders` (from purchasing.PurchaseOrder)
- `confirmed_purchase_orders` (from purchasing.PurchaseOrder)
- `cancelled_purchase_orders` (from purchasing.PurchaseOrder)
- `created_purchase_invoices` (from purchasing.PurchaseInvoice)
- `maintenancerequest` (from rent.MaintenanceRequest)
- `custom_admin_created_backups` (from custom_admin.BackupRecord)
- `created_restores` (from custom_admin.RestoreRecord)
- `custom_ui_elements` (from custom_admin.CustomUIElement)
- `custom_reports` (from custom_admin.CustomReport)
- `custom_menus` (from custom_admin.CustomMenu)
- `dashboard_widgets` (from custom_admin.DashboardWidget)
- `dashboard_layouts` (from custom_admin.DashboardLayout)
- `admin_notifications` (from custom_admin.AdminNotification)
- `ai_usage_reports` (from custom_admin.AIUsageReport)
- `resolved_alerts` (from custom_admin.SystemAlert)
- `audit_logs` (from custom_admin.AuditLog)
- `custom_admin_created_settings` (from custom_admin.SystemSetting)
- `preferences` (from custom_admin.UserPreference)
- `dashboard_settings` (from dashboard.UserDashboardSettings)
- `created_dashboard_widgets` (from ai_dashboard.DashboardWidget)
- `dashboardanalytics` (from ai_dashboard.DashboardAnalytics)
- `import_jobs` (from admin_data_import_export.ImportJob)
- `export_jobs` (from admin_data_import_export.ExportJob)
- `database_management_backup_logs` (from database_management.BackupLog)
- `database_management_restore_logs` (from database_management.RestoreLog)
- `db_connection_settings` (from database_management.DatabaseConnectionSettings)
- `database_management_backup_schedules` (from database_management.BackupSchedule)
- `health_monitoring_user_activities` (from health_monitoring.UserActivityLog)
- `notification_preferences` (from notifications.UserNotificationPreference)
- `received_notifications` (from notifications.Notification)
- `sent_notifications` (from notifications.Notification)
- `aiagentusagelog` (from admin_reports.AIAgentUsageLog)
- `backup_configurations` (from system_backups.BackupConfiguration)
- `backup_schedules` (from system_backups.BackupSchedule)
- `backup_logs` (from system_backups.BackupLog)
- `restore_logs` (from system_backups.RestoreLog)
- `acknowledged_alerts` (from system_monitoring.Alert)
- `diagnosis_sessions` (from internal_diagnosis_module.DiagnosisSession)
- `led_research_projects` (from research.ResearchProject)
- `created_research_projects` (from research.ResearchProject)
- `updated_research_projects` (from research.ResearchProject)
- `created_project_team_members` (from research.ProjectTeamMember)
- `updated_project_team_members` (from research.ProjectTeamMember)
- `created_experiments` (from research.ResearchExperiment)
- `updated_experiments` (from research.ResearchExperiment)
- `created_experiment_participants` (from research.ExperimentParticipant)
- `updated_experiment_results` (from research.ExperimentResult)
- `researcher_profile` (from research.Researcher)
- `created_researchers` (from research.Researcher)
- `updated_researchers` (from research.Researcher)
- `created_publications` (from research.Publication)
- `updated_publications` (from research.Publication)
- `created_patents` (from research.Patent)
- `updated_patents` (from research.Patent)
- `created_grants` (from research.ResearchGrant)
- `updated_grants` (from research.ResearchGrant)
- `created_equipment` (from research.ResearchEquipment)
- `updated_equipment` (from research.ResearchEquipment)
- `created_reports` (from research.ResearchReport)
- `updated_reports` (from research.ResearchReport)
- `researchobjective` (from research.ResearchObjective)
- `research_team_memberships` (from research.ResearchTeamMember)
- `created_research_team_members` (from research.ResearchTeamMember)
- `assigned_research_tasks` (from research.ResearchTask)
- `created_research_tasks` (from research.ResearchTask)
- `created_locations` (from agricultural_experiments.Location)
- `updated_locations` (from agricultural_experiments.Location)
- `created_seasons` (from agricultural_experiments.Season)
- `updated_seasons` (from agricultural_experiments.Season)
- `created_varieties` (from agricultural_experiments.Variety)
- `updated_varieties` (from agricultural_experiments.Variety)
- `agri_created_experiments` (from agricultural_experiments.Experiment)
- `agri_updated_experiments` (from agricultural_experiments.Experiment)
- `created_ai_analyses` (from agricultural_experiments.AIAnalysis)
- `created_external_varieties` (from agricultural_experiments.ExternalVariety)
- `created_external_variety_specifications` (from agricultural_experiments.ExternalVarietySpecification)
- `created_external_variety_yield_data` (from agricultural_experiments.ExternalVarietyYieldData)
- `created_harvests` (from agricultural_experiments.Harvest)
- `created_comparison_reports` (from agricultural_experiments.VarietyComparisonReport)
- `created_inventory_comparison_reports` (from agricultural_experiments.InventoryVarietyComparisonReport)
- `created_production_orders` (from agricultural_production.ProductionOrder)
- `updated_production_orders` (from agricultural_production.ProductionOrder)
- `responsible_operations` (from agricultural_production.ProductionOperation)
- `created_operations` (from agricultural_production.ProductionOperation)
- `updated_operations` (from agricultural_production.ProductionOperation)
- `created_production_batches` (from agricultural_production.ProductionBatch)
- `updated_production_batches` (from agricultural_production.ProductionBatch)
- `created_production_wastes` (from agricultural_production.ProductionWaste)
- `inventoryverification_created_by` (from seed_production.InventoryVerification)
- `inventoryverification_updated_by` (from seed_production.InventoryVerification)
- `lotchangelog_created_by` (from seed_production.LotChangeLog)
- `lotchangelog_updated_by` (from seed_production.LotChangeLog)
- `seedpackaging_created_by` (from seed_production.SeedPackaging)
- `seedpackaging_updated_by` (from seed_production.SeedPackaging)
- `seedproductionplan_created_by` (from seed_production.SeedProductionPlan)
- `seedproductionplan_updated_by` (from seed_production.SeedProductionPlan)
- `seedtreatmentlog_created_by` (from seed_production.SeedTreatmentLog)
- `seedtreatmentlog_updated_by` (from seed_production.SeedTreatmentLog)
- `seedproductionorder_updated_by` (from seed_production.SeedProductionOrder)
- `seed_orders_created` (from seed_production.SeedProductionOrder)
- `seed_orders_assigned` (from seed_production.SeedProductionOrder)
- `responsible_for_seed_lots` (from seed_production.SeedProductionLot)
- `seed_lots_created` (from seed_production.SeedProductionLot)
- `seed_tests_performed` (from seed_production.SeedLotTest)
- `seed_activities_performed` (from seed_production.SeedProductionActivity)
- `seed_movements_performed` (from seed_production.SeedInventoryMovement)
- `managed_farms` (from farms.Farm)
- `performed_activities` (from farms.FarmActivity)
- `nursery` (from nurseries.Nursery)
- `nurseryactivity` (from nurseries.NurseryActivity)
- `qualitycheck` (from nurseries.QualityCheck)
- `environmentallog` (from nurseries.EnvironmentalLog)
- `nurserysite` (from nurseries.NurserySite)
- `plant_diagnosis_requests` (from plant_diagnosis.PlantDiagnosisRequest)
- `varietytrial` (from variety_trials.VarietyTrial)
- `trialcost` (from variety_trials.TrialCost)
- `trialreport` (from variety_trials.TrialReport)
- `varietyrecommendation` (from variety_trials.VarietyRecommendation)
- `aianalysis` (from variety_trials.AIAnalysis)
- `uploaded_reference_files` (from ai.ReferenceFile)
- `uploaded_keyword_files` (from ai.KeywordFile)
- `ai_conversations` (from ai.Conversation)
- `ai_activities` (from ai.AIActivity)
- `api_keys` (from ai.APIKey)
- `created_data_sources` (from ai_analytics.AnalyticsDataSource)
- `created_datasets` (from ai_analytics.AnalyticsDataset)
- `created_models` (from ai_analytics.AnalyticsModel)
- `created_analytics_reports` (from ai_analytics.AnalyticsReport)
- `analytics_jobs` (from ai_analytics.AnalyticsJob)
- `ai_usage_logs` (from ai_services.AIUsageLog)
- `ai_usage_summaries` (from ai_services.AIUsageSummary)
- `integration_logs` (from a2a_integration.IntegrationLog)
- `created_agri_recommendations` (from ai_agriculture.AgriRecommendation)
- `updated_agri_recommendations` (from ai_agriculture.AgriRecommendation)
- `email_campaigns` (from email_messaging.EmailCampaign)
- `uploaded_files` (from cloud_services.CloudFile)
- `created_security_policies` (from ai_security.SecurityPolicy)
- `conducted_audits` (from ai_security.SecurityAudit)
- `reported_incidents` (from ai_security.SecurityIncident)
- `assigned_incidents` (from ai_security.SecurityIncident)
- `discovered_vulnerabilities` (from ai_security.SecurityVulnerability)
- `assigned_vulnerabilities` (from ai_security.SecurityVulnerability)
- `created_security_scans` (from ai_security.SecurityScan)
- `created_access_controls` (from ai_security.SecurityAccessControl)
- `conversation` (from intelligent_assistant.Conversation)
- `knowledgebase` (from intelligent_assistant.KnowledgeBase)
- `aiinsight` (from intelligent_assistant.AIInsight)
- `ai_preferences` (from intelligent_assistant.UserPreference)
- `aianalytics` (from intelligent_assistant.AIAnalytics)
- `owned_agents` (from ai_agents.Agent)
- `ai_roles` (from ai_agents.UserRole)
- `assigned_roles` (from ai_agents.UserRole)
- `assigned_agent_roles` (from ai_agents.AgentRole)
- `resolved_errors` (from ai_agents.ErrorLog)
- `ai_acknowledged_alerts` (from ai_monitoring.SystemAlert)
- `ai_resolved_alerts` (from ai_monitoring.SystemAlert)
- `ai_reports` (from ai_reports.AIReport)
- `report_templates` (from ai_reports.ReportTemplate)
- `acknowledged_insights` (from ai_reports.ReportInsight)
- `report_schedules` (from ai_reports.ReportSchedule)
- `training_datasets` (from ai_training.TrainingDataset)
- `training_jobs` (from ai_training.TrainingJob)
- `memory_contexts` (from ai_memory.MemoryContext)
- `created_memories` (from ai_memory.Memory)
- `updated_knowledge_bases` (from ai_memory.KnowledgeBase)
- `learning_patterns` (from ai_memory.LearningPattern)
- `memory_cleanups` (from ai_memory.MemoryCleanupLog)
- `ai_models` (from ai_models.AIModel)
- `model_deployments` (from ai_models.ModelDeployment)
- `model_usage_logs` (from ai_models.ModelUsageLog)
- `created_forecast_models` (from forecast.ForecastModel)
- `created_forecast_results` (from forecast.ForecastResult)
- `created_forecast_data_sources` (from forecast.ForecastDataSource)

**Indexes**:

- users_user_email_6f2530_idx: (email)
- users_user_usernam_65d164_idx: (username)
- users_user_is_acti_ddda02_idx: (is_active)

---

### UserActivity

**Table**: `users_useractivity`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| session | ForeignKey | Yes | - | Yes |
| activity_type | CharField | No | - | No |
| description | TextField | Yes | - | No |
| ip_address | GenericIPAddressField | Yes | - | No |
| content_type | ForeignKey | Yes | - | Yes |
| object_id | PositiveIntegerField | Yes | - | No |
| data | JSONField | Yes | <class 'dict'> | No |
| timestamp | DateTimeField | No | - | No |
| content_object | GenericForeignKey | No | - | No |

**Foreign Keys**:

- `user` → users.User
- `session` → users.UserSession
- `content_type` → contenttypes.ContentType

**Indexes**:

- users_usera_user_id_421934_idx: (user, activity_type)
- users_usera_timesta_b616d0_idx: (-timestamp)
- users_usera_content_100859_idx: (content_type, object_id)

---

### UserAPIKey

**Table**: `users_userapikey`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| name | CharField | No | - | No |
| key | CharField | No | - | No |
| is_active | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| expires_at | DateTimeField | Yes | - | No |
| last_used_at | DateTimeField | Yes | - | No |
| permissions | JSONField | No | <class 'dict'> | No |
| description | TextField | Yes | - | No |

**Foreign Keys**:

- `user` → users.User

**Indexes**:

- users_usera_user_id_0dd2f2_idx: (user, is_active)
- users_usera_key_5da6ed_idx: (key)
- users_usera_expires_c3b339_idx: (expires_at)

---

### UserDevice

**Table**: `users_userdevice`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| device_id | CharField | No | - | No |
| device_name | CharField | No | - | No |
| device_type | CharField | No | - | No |
| os_name | CharField | No | - | No |
| os_version | CharField | No | - | No |
| browser_name | CharField | Yes | - | No |
| browser_version | CharField | Yes | - | No |
| app_version | CharField | Yes | - | No |
| push_token | CharField | Yes | - | No |
| is_active | BooleanField | No | True | No |
| last_login | DateTimeField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

**Reverse Relations**:

- `sessions` (from users.UserSession)

**Indexes**:

- users_userd_user_id_a5f926_idx: (user, is_active)
- users_userd_device__c17433_idx: (device_id)

**Unique Together**:

- (user, device_id)

---

### UserNotificationPreference

**Table**: `users_usernotificationpreference`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| notification_type | CharField | No | - | No |
| email_enabled | BooleanField | No | True | No |
| sms_enabled | BooleanField | No | False | No |
| push_enabled | BooleanField | No | True | No |
| in_app_enabled | BooleanField | No | True | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `user` → users.User

**Indexes**:

- users_usern_user_id_a6ddfa_idx: (user)
- users_usern_notific_3b1849_idx: (notification_type)

**Unique Together**:

- (user, notification_type)

---

### UserProfile

**Table**: `users_userprofile`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | OneToOneField | No | - | Yes |
| avatar | FileField | Yes | - | No |
| bio | TextField | Yes | - | No |
| birth_date | DateField | Yes | - | No |
| gender | CharField | Yes | - | No |
| address | TextField | Yes | - | No |
| city | CharField | Yes | - | No |
| country | CharField | Yes | - | No |
| postal_code | CharField | Yes | - | No |
| website | CharField | Yes | - | No |
| social_links | JSONField | Yes | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `user` (from users.User)

**Indexes**:

- users_userp_user_id_d181df_idx: (user)

---

### UserSession

**Table**: `users_usersession`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | ForeignKey | No | - | Yes |
| session_key | CharField | No | - | No |
| device | ForeignKey | Yes | - | Yes |
| ip_address | GenericIPAddressField | Yes | - | No |
| user_agent | TextField | Yes | - | No |
| login_time | DateTimeField | No | - | No |
| last_activity | DateTimeField | No | - | No |
| logout_time | DateTimeField | Yes | - | No |
| is_active | BooleanField | No | True | No |

**Foreign Keys**:

- `user` → users.User
- `device` → users.UserDevice

**Reverse Relations**:

- `activities` (from users.UserActivity)

**Indexes**:

- users_users_user_id_3887fe_idx: (user, is_active)
- users_users_session_70af4d_idx: (session_key)
- users_users_login_t_f93e86_idx: (-login_time)

---

### UserSettings

**Table**: `users_usersettings`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| user | OneToOneField | No | - | Yes |
| theme | CharField | No | system | No |
| notifications_enabled | BooleanField | No | True | No |
| email_notifications | BooleanField | No | True | No |
| sms_notifications | BooleanField | No | False | No |
| push_notifications | BooleanField | No | True | No |
| dashboard_layout | JSONField | Yes | <class 'dict'> | No |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Reverse Relations**:

- `user` (from users.User)

**Indexes**:

- users_users_user_id_36e6ae_idx: (user)

---

## variety_trials

### AIAnalysis

**Table**: `variety_trials_aianalysis`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial | ForeignKey | No | - | Yes |
| analysis_date | DateTimeField | No | - | No |
| analysis_type | CharField | No | - | No |
| input_parameters | JSONField | No | - | No |
| results | JSONField | No | - | No |
| summary | TextField | No | - | No |
| confidence_score | DecimalField | Yes | - | No |
| recommendations | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |

**Foreign Keys**:

- `trial` → variety_trials.VarietyTrial
- `created_by` → users.User

---

### CompetitorVariety

**Table**: `variety_trials_competitorvariety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| variety_name | CharField | No | - | No |
| competitor_name | CharField | No | - | No |
| variety_code | CharField | No | - | No |

---

### FruitSpecification

**Table**: `variety_trials_fruitspecification`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial_variety | ForeignKey | No | - | Yes |
| evaluation_date | DateField | No | - | No |
| brix_value | DecimalField | Yes | - | No |
| color_rating | IntegerField | Yes | - | No |
| notes | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `trial_variety` → variety_trials.TrialVariety

---

### HarvestLog

**Table**: `variety_trials_harvestlog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial_variety | ForeignKey | No | - | Yes |
| harvest_date | DateField | No | - | No |
| harvest_number | PositiveIntegerField | No | 1 | No |
| notes | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `trial_variety` → variety_trials.TrialVariety

**Reverse Relations**:

- `quality_grades` (from variety_trials.HarvestQualityLog)

---

### HarvestQualityLog

**Table**: `variety_trials_harvestqualitylog`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| harvest_log | ForeignKey | No | - | Yes |
| quality_grade | CharField | No | - | No |
| fruit_count | PositiveIntegerField | Yes | - | No |
| fruit_weight_kg | DecimalField | Yes | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `harvest_log` → variety_trials.HarvestLog

---

### PlantSpecification

**Table**: `variety_trials_plantspecification`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial_variety | ForeignKey | No | - | Yes |
| evaluation_date | DateField | No | - | No |
| plant_vigor_rating | IntegerField | Yes | - | No |
| drought_tolerance_rating | IntegerField | Yes | - | No |
| notes | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `trial_variety` → variety_trials.TrialVariety

---

### TrialCost

**Table**: `variety_trials_trialcost`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial | ForeignKey | No | - | Yes |
| description | CharField | No | - | No |
| amount | DecimalField | No | - | No |
| date_incurred | DateField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `trial` → variety_trials.VarietyTrial
- `created_by` → users.User

---

### TrialFertilizationProgram

**Table**: `variety_trials_trialfertilizationprogram`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial | ForeignKey | No | - | Yes |
| fertilizer_name | CharField | No | - | No |
| application_date | DateField | No | - | No |
| notes | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `trial` → variety_trials.VarietyTrial

---

### TrialPesticideProgram

**Table**: `variety_trials_trialpesticideprogram`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial | ForeignKey | No | - | Yes |
| pesticide_name | CharField | No | - | No |
| application_date | DateField | No | - | No |
| effectiveness_rating | IntegerField | Yes | - | No |
| notes | TextField | No | - | No |
| created_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `trial` → variety_trials.VarietyTrial

---

### TrialReport

**Table**: `variety_trials_trialreport`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial | ForeignKey | No | - | Yes |
| report_date | DateField | No | - | No |
| title | CharField | No | - | No |
| summary | TextField | No | - | No |
| status | CharField | No | DRAFT | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `trial` → variety_trials.VarietyTrial
- `created_by` → users.User

---

### TrialVariety

**Table**: `variety_trials_trialvariety`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial | ForeignKey | No | - | Yes |
| plant_species_or_variety_name | CharField | No | - | No |
| variety_code | CharField | No | - | No |
| number_of_plants | PositiveIntegerField | No | 0 | No |
| notes | TextField | No | - | No |

**Foreign Keys**:

- `trial` → variety_trials.VarietyTrial

**Reverse Relations**:

- `harvest_logs` (from variety_trials.HarvestLog)
- `fruit_specifications` (from variety_trials.FruitSpecification)
- `plant_specifications` (from variety_trials.PlantSpecification)
- `recommendations` (from variety_trials.VarietyRecommendation)

**Unique Together**:

- (trial, plant_species_or_variety_name, variety_code)

---

### VarietyRecommendation

**Table**: `variety_trials_varietyrecommendation`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial_variety | ForeignKey | No | - | Yes |
| evaluation_date | DateField | No | - | No |
| overall_rating | IntegerField | No | - | No |
| recommendation | CharField | No | - | No |
| notes | TextField | No | - | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `trial_variety` → variety_trials.TrialVariety
- `created_by` → users.User

---

### VarietyTrial

**Table**: `variety_trials_varietytrial`

**Fields**:

| Field | Type | Null | Default | Index |
|-------|------|------|---------|-------|
| id | BigAutoField | No | - | No |
| trial_name | CharField | No | - | No |
| trial_code | CharField | No | - | No |
| planting_date | DateField | Yes | - | No |
| status | CharField | No | PLANNED | No |
| created_by | ForeignKey | Yes | - | Yes |
| created_at | DateTimeField | No | - | No |
| updated_at | DateTimeField | No | - | No |

**Foreign Keys**:

- `created_by` → users.User

**Reverse Relations**:

- `trial_varieties` (from variety_trials.TrialVariety)
- `costs` (from variety_trials.TrialCost)
- `fertilization_programs` (from variety_trials.TrialFertilizationProgram)
- `pesticide_programs` (from variety_trials.TrialPesticideProgram)
- `reports` (from variety_trials.TrialReport)
- `ai_analyses` (from variety_trials.AIAnalysis)

---

