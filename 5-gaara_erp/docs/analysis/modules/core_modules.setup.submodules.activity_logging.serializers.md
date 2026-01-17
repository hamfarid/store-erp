# core_modules.setup.submodules.activity_logging.serializers

## Imports
- django.contrib.auth
- models
- rest_framework

## Classes
- UserSerializer
- ActivityLogSerializer
  - attr: `user`
  - attr: `action_type_display`
- ActivityLogCreateSerializer
- ErrorLogSerializer
  - attr: `user`
  - attr: `error_type_display`
- ErrorLogCreateSerializer
- ActivityLogSettingSerializer
  - attr: `created_by`
  - attr: `updated_by`
  - attr: `log_level_display`
- ActivityLogSettingUpdateSerializer
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class UserSerializer {
    }
    class ActivityLogSerializer {
        +user
        +action_type_display
    }
    class ActivityLogCreateSerializer {
    }
    class ErrorLogSerializer {
        +user
        +error_type_display
    }
    class ErrorLogCreateSerializer {
    }
    class ActivityLogSettingSerializer {
        +created_by
        +updated_by
        +log_level_display
    }
    class ActivityLogSettingUpdateSerializer {
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    ActivityLogSerializer --> Meta
    ActivityLogSerializer --> Meta
    ActivityLogSerializer --> Meta
    ActivityLogSerializer --> Meta
    ActivityLogSerializer --> Meta
    ActivityLogSerializer --> Meta
    ActivityLogSerializer --> Meta
    ActivityLogCreateSerializer --> Meta
    ActivityLogCreateSerializer --> Meta
    ActivityLogCreateSerializer --> Meta
    ActivityLogCreateSerializer --> Meta
    ActivityLogCreateSerializer --> Meta
    ActivityLogCreateSerializer --> Meta
    ActivityLogCreateSerializer --> Meta
    ErrorLogSerializer --> Meta
    ErrorLogSerializer --> Meta
    ErrorLogSerializer --> Meta
    ErrorLogSerializer --> Meta
    ErrorLogSerializer --> Meta
    ErrorLogSerializer --> Meta
    ErrorLogSerializer --> Meta
    ErrorLogCreateSerializer --> Meta
    ErrorLogCreateSerializer --> Meta
    ErrorLogCreateSerializer --> Meta
    ErrorLogCreateSerializer --> Meta
    ErrorLogCreateSerializer --> Meta
    ErrorLogCreateSerializer --> Meta
    ErrorLogCreateSerializer --> Meta
    ActivityLogSettingSerializer --> Meta
    ActivityLogSettingSerializer --> Meta
    ActivityLogSettingSerializer --> Meta
    ActivityLogSettingSerializer --> Meta
    ActivityLogSettingSerializer --> Meta
    ActivityLogSettingSerializer --> Meta
    ActivityLogSettingSerializer --> Meta
    ActivityLogSettingUpdateSerializer --> Meta
    ActivityLogSettingUpdateSerializer --> Meta
    ActivityLogSettingUpdateSerializer --> Meta
    ActivityLogSettingUpdateSerializer --> Meta
    ActivityLogSettingUpdateSerializer --> Meta
    ActivityLogSettingUpdateSerializer --> Meta
    ActivityLogSettingUpdateSerializer --> Meta
```
