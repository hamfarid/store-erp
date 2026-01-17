# integration_modules.ai.models.__init__

## Imports
- conversations
- django.conf
- django.db
- django.utils.translation
- learning_sources
- memory_and_learning

## Classes
- AISettings
  - attr: `key`
  - attr: `value`
  - attr: `description`
  - attr: `is_system`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- AIActivity
  - attr: `ACTIVITY_TYPES`
  - attr: `STATUS_CHOICES`
  - attr: `activity_type`
  - attr: `user`
  - attr: `agent_name`
  - attr: `service_name`
  - attr: `action`
  - attr: `details`
  - attr: `status`
  - attr: `created_at`
  - method: `__str__`
- AIIntegration
  - attr: `INTEGRATION_TYPES`
  - attr: `STATUS_CHOICES`
  - attr: `name`
  - attr: `integration_type`
  - attr: `module_path`
  - attr: `configuration`
  - attr: `status`
  - attr: `last_sync`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- APIKey
  - attr: `KEY_TYPES`
  - attr: `name`
  - attr: `key_type`
  - attr: `key_value`
  - attr: `is_active`
  - attr: `description`
  - attr: `expires_at`
  - attr: `created_at`
  - attr: `created_by`
  - method: `__str__`
- AIModel
  - attr: `name`
  - attr: `provider`
  - attr: `model_identifier`
  - attr: `is_active`
  - attr: `description`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `app_label`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `app_label`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `app_label`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `app_label`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`

## Functions
- __str__
- __str__
- __str__
- __str__
- __str__

## Module Variables
- `LABEL_CREATED_AT`
- `LABEL_UPDATED_AT`
- `LABEL_DESCRIPTION`
- `__all__`

## Class Diagram

```mermaid
classDiagram
    class AISettings {
        +key
        +value
        +description
        +is_system
        +created_at
        +... (1 more)
        +__str__()
    }
    class AIActivity {
        +ACTIVITY_TYPES
        +STATUS_CHOICES
        +activity_type
        +user
        +agent_name
        +... (5 more)
        +__str__()
    }
    class AIIntegration {
        +INTEGRATION_TYPES
        +STATUS_CHOICES
        +name
        +integration_type
        +module_path
        +... (5 more)
        +__str__()
    }
    class APIKey {
        +KEY_TYPES
        +name
        +key_type
        +key_value
        +is_active
        +... (4 more)
        +__str__()
    }
    class AIModel {
        +name
        +provider
        +model_identifier
        +is_active
        +description
        +... (2 more)
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +app_label
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +app_label
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +app_label
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +app_label
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    AISettings --> Meta
    AISettings --> Meta
    AISettings --> Meta
    AISettings --> Meta
    AISettings --> Meta
    AIActivity --> Meta
    AIActivity --> Meta
    AIActivity --> Meta
    AIActivity --> Meta
    AIActivity --> Meta
    AIIntegration --> Meta
    AIIntegration --> Meta
    AIIntegration --> Meta
    AIIntegration --> Meta
    AIIntegration --> Meta
    APIKey --> Meta
    APIKey --> Meta
    APIKey --> Meta
    APIKey --> Meta
    APIKey --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
```
