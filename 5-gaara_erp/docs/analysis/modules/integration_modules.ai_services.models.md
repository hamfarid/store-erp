# integration_modules.ai_services.models

## Imports
- core_modules.base_models.models
- django.conf
- django.core.exceptions
- django.db
- django.utils
- django.utils.translation

## Classes
- AIModel
  - attr: `MODEL_TYPES`
  - attr: `name`
  - attr: `description`
  - attr: `model_type`
  - attr: `provider`
  - attr: `model_identifier`
  - attr: `is_active`
  - attr: `config`
  - attr: `cost_per_token`
  - attr: `usage_limit`
  - method: `__str__`
  - method: `clean`
- AIService
  - attr: `SERVICE_TYPES`
  - attr: `name`
  - attr: `description`
  - attr: `service_type`
  - attr: `models`
  - attr: `is_active`
  - attr: `config`
  - method: `__str__`
- AIServiceModel
  - attr: `service`
  - attr: `model`
  - attr: `is_default`
  - attr: `config_override`
  - method: `__str__`
  - method: `clean`
- AIUsageLog
  - attr: `service`
  - attr: `model`
  - attr: `user`
  - attr: `agent_id`
  - attr: `timestamp`
  - attr: `request_data`
  - attr: `response_data`
  - attr: `tokens_input`
  - attr: `tokens_output`
  - attr: `cost`
  - attr: `status`
  - attr: `error_message`
  - method: `__str__`
  - method: `calculate_cost`
  - method: `save`
- AIUsageSummary
  - attr: `PERIOD_TYPES`
  - attr: `period_type`
  - attr: `period_start`
  - attr: `period_end`
  - attr: `service`
  - attr: `model`
  - attr: `user`
  - attr: `request_count`
  - attr: `success_count`
  - attr: `error_count`
  - attr: `tokens_input`
  - attr: `tokens_output`
  - attr: `total_cost`
  - method: `__str__`
- AIMemoryIntegration
  - attr: `service`
  - attr: `memory_enabled`
  - attr: `short_term_memory_ttl`
  - attr: `long_term_memory_enabled`
  - attr: `memory_config`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `indexes`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`
  - attr: `unique_together`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`

## Functions
- __str__
- clean
- __str__
- __str__
- clean
- __str__
- calculate_cost
- save
- __str__
- __str__

## Class Diagram

```mermaid
classDiagram
    class AIModel {
        +MODEL_TYPES
        +name
        +description
        +model_type
        +provider
        +... (5 more)
        +__str__()
        +clean()
    }
    class AIService {
        +SERVICE_TYPES
        +name
        +description
        +service_type
        +models
        +... (2 more)
        +__str__()
    }
    class AIServiceModel {
        +service
        +model
        +is_default
        +config_override
        +__str__()
        +clean()
    }
    class AIUsageLog {
        +service
        +model
        +user
        +agent_id
        +timestamp
        +... (7 more)
        +__str__()
        +calculate_cost()
        +save()
    }
    class AIUsageSummary {
        +PERIOD_TYPES
        +period_type
        +period_start
        +period_end
        +service
        +... (8 more)
        +__str__()
    }
    class AIMemoryIntegration {
        +service
        +memory_enabled
        +short_term_memory_ttl
        +long_term_memory_enabled
        +memory_config
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +unique_together
        +indexes
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
        +unique_together
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIService --> Meta
    AIService --> Meta
    AIService --> Meta
    AIService --> Meta
    AIService --> Meta
    AIService --> Meta
    AIServiceModel --> Meta
    AIServiceModel --> Meta
    AIServiceModel --> Meta
    AIServiceModel --> Meta
    AIServiceModel --> Meta
    AIServiceModel --> Meta
    AIUsageLog --> Meta
    AIUsageLog --> Meta
    AIUsageLog --> Meta
    AIUsageLog --> Meta
    AIUsageLog --> Meta
    AIUsageLog --> Meta
    AIUsageSummary --> Meta
    AIUsageSummary --> Meta
    AIUsageSummary --> Meta
    AIUsageSummary --> Meta
    AIUsageSummary --> Meta
    AIUsageSummary --> Meta
    AIMemoryIntegration --> Meta
    AIMemoryIntegration --> Meta
    AIMemoryIntegration --> Meta
    AIMemoryIntegration --> Meta
    AIMemoryIntegration --> Meta
    AIMemoryIntegration --> Meta
```
