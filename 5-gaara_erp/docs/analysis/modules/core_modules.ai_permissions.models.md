# core_modules.ai_permissions.models

## Imports
- django.conf
- django.db
- django.utils.translation

## Classes
- AIModel
  - attr: `name`
  - attr: `description`
  - attr: `model_type`
  - method: `__str__`
- AIModelPermission
  - attr: `MODEL_TYPE_TEXT`
  - attr: `MODEL_TYPE_IMAGE`
  - attr: `MODEL_TYPE_AUDIO`
  - attr: `MODEL_TYPE_VIDEO`
  - attr: `MODEL_TYPE_MULTIMODAL`
  - attr: `MODEL_TYPE_EMBEDDING`
  - attr: `MODEL_TYPE_CHOICES`
  - attr: `name`
  - attr: `model_type`
  - attr: `description`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- AIAgent
  - attr: `name`
  - attr: `description`
  - attr: `is_active`
  - attr: `created_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- AIRole
  - attr: `name`
  - attr: `description`
  - attr: `permissions`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- AgentRole
  - attr: `agent`
  - attr: `role`
  - attr: `scope`
  - attr: `valid_from`
  - attr: `valid_until`
  - attr: `is_active`
  - attr: `assigned_by`
  - attr: `created_at`
  - method: `__str__`
- AIPermissionAuditLog
  - attr: `ACTION_CHECK`
  - attr: `ACTION_GRANT`
  - attr: `ACTION_REVOKE`
  - attr: `ACTION_CHOICES`
  - attr: `agent`
  - attr: `action`
  - attr: `permission`
  - attr: `result`
  - attr: `details`
  - attr: `user`
  - attr: `timestamp`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- __str__
- __str__
- __str__
- __str__
- __str__

## Module Variables
- `NAME_LABEL`
- `DESCRIPTION_LABEL`
- `MODEL_TYPE_TEXT`
- `MODEL_TYPE_IMAGE`
- `MODEL_TYPE_AUDIO`
- `MODEL_TYPES`

## Class Diagram

```mermaid
classDiagram
    class AIModel {
        +name
        +description
        +model_type
        +__str__()
    }
    class AIModelPermission {
        +MODEL_TYPE_TEXT
        +MODEL_TYPE_IMAGE
        +MODEL_TYPE_AUDIO
        +MODEL_TYPE_VIDEO
        +MODEL_TYPE_MULTIMODAL
        +... (8 more)
        +__str__()
    }
    class AIAgent {
        +name
        +description
        +is_active
        +created_by
        +created_at
        +... (1 more)
        +__str__()
    }
    class AIRole {
        +name
        +description
        +permissions
        +is_active
        +created_at
        +... (1 more)
        +__str__()
    }
    class AgentRole {
        +agent
        +role
        +scope
        +valid_from
        +valid_until
        +... (3 more)
        +__str__()
    }
    class AIPermissionAuditLog {
        +ACTION_CHECK
        +ACTION_GRANT
        +ACTION_REVOKE
        +ACTION_CHOICES
        +agent
        +... (6 more)
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +unique_together
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +unique_together
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModel --> Meta
    AIModelPermission --> Meta
    AIModelPermission --> Meta
    AIModelPermission --> Meta
    AIModelPermission --> Meta
    AIModelPermission --> Meta
    AIModelPermission --> Meta
    AIAgent --> Meta
    AIAgent --> Meta
    AIAgent --> Meta
    AIAgent --> Meta
    AIAgent --> Meta
    AIAgent --> Meta
    AIRole --> Meta
    AIRole --> Meta
    AIRole --> Meta
    AIRole --> Meta
    AIRole --> Meta
    AIRole --> Meta
    AgentRole --> Meta
    AgentRole --> Meta
    AgentRole --> Meta
    AgentRole --> Meta
    AgentRole --> Meta
    AgentRole --> Meta
    AIPermissionAuditLog --> Meta
    AIPermissionAuditLog --> Meta
    AIPermissionAuditLog --> Meta
    AIPermissionAuditLog --> Meta
    AIPermissionAuditLog --> Meta
    AIPermissionAuditLog --> Meta
```
