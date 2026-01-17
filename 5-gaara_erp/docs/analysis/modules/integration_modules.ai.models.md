# integration_modules.ai.models

## Imports
- django.conf
- django.db
- django.db.models
- django.utils
- django.utils.translation
- models
- models.conversations
- models.learning_sources
- models.memory_and_learning

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

## Functions
- __str__
- __str__
- __str__
- __str__

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
    AISettings --> Meta
    AISettings --> Meta
    AISettings --> Meta
    AISettings --> Meta
    AIActivity --> Meta
    AIActivity --> Meta
    AIActivity --> Meta
    AIActivity --> Meta
    AIIntegration --> Meta
    AIIntegration --> Meta
    AIIntegration --> Meta
    AIIntegration --> Meta
    APIKey --> Meta
    APIKey --> Meta
    APIKey --> Meta
    APIKey --> Meta
```
