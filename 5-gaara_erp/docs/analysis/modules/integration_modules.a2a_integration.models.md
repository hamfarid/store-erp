# integration_modules.a2a_integration.models

## Imports
- django.conf
- django.db
- django.utils
- django.utils.translation

## Classes
- ExternalSystem
  - attr: `SYSTEM_TYPES`
  - attr: `name`
  - attr: `system_type`
  - attr: `base_url`
  - attr: `description`
  - attr: `contact_person`
  - attr: `contact_email`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- IntegrationConfig
  - attr: `INTEGRATION_TYPES`
  - attr: `DIRECTION_TYPES`
  - attr: `name`
  - attr: `external_system`
  - attr: `integration_type`
  - attr: `direction`
  - attr: `endpoint_url`
  - attr: `data_format`
  - attr: `headers`
  - attr: `parameters`
  - attr: `schedule`
  - attr: `retry_count`
  - attr: `retry_delay`
  - attr: `timeout`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- APICredential
  - attr: `AUTH_TYPES`
  - attr: `name`
  - attr: `external_system`
  - attr: `auth_type`
  - attr: `key_id`
  - attr: `key_secret`
  - attr: `token`
  - attr: `token_expiry`
  - attr: `additional_data`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `is_token_valid`
- IntegrationLog
  - attr: `STATUS_CHOICES`
  - attr: `integration_config`
  - attr: `request_data`
  - attr: `response_data`
  - attr: `status`
  - attr: `status_code`
  - attr: `error_message`
  - attr: `execution_time`
  - attr: `retry_count`
  - attr: `created_by`
  - attr: `created_at`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- __str__
- __str__
- is_token_valid
- __str__

## Module Variables
- `__all__`

## Class Diagram

```mermaid
classDiagram
    class ExternalSystem {
        +SYSTEM_TYPES
        +name
        +system_type
        +base_url
        +description
        +... (5 more)
        +__str__()
    }
    class IntegrationConfig {
        +INTEGRATION_TYPES
        +DIRECTION_TYPES
        +name
        +external_system
        +integration_type
        +... (12 more)
        +__str__()
    }
    class APICredential {
        +AUTH_TYPES
        +name
        +external_system
        +auth_type
        +key_id
        +... (7 more)
        +__str__()
        +is_token_valid()
    }
    class IntegrationLog {
        +STATUS_CHOICES
        +integration_config
        +request_data
        +response_data
        +status
        +... (6 more)
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    ExternalSystem --> Meta
    ExternalSystem --> Meta
    ExternalSystem --> Meta
    ExternalSystem --> Meta
    IntegrationConfig --> Meta
    IntegrationConfig --> Meta
    IntegrationConfig --> Meta
    IntegrationConfig --> Meta
    APICredential --> Meta
    APICredential --> Meta
    APICredential --> Meta
    APICredential --> Meta
    IntegrationLog --> Meta
    IntegrationLog --> Meta
    IntegrationLog --> Meta
    IntegrationLog --> Meta
```
