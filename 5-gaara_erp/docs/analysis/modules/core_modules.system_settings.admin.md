# core_modules.system_settings.admin

## Imports
- core_modules.setup.system_settings.models
- django.contrib
- django.utils.translation
- models

## Classes
- SystemSettingAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `fieldsets`
  - method: `save_model`
- CountryAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `fieldsets`
- CurrencyAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `fieldsets`
- EmailSettingAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `fieldsets`
- SetupWizardStatusAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `readonly_fields`
  - attr: `fieldsets`

## Functions
- save_model

## Class Diagram

```mermaid
classDiagram
    class SystemSettingAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +fieldsets
        +save_model()
    }
    class CountryAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +fieldsets
    }
    class CurrencyAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +fieldsets
    }
    class EmailSettingAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +fieldsets
    }
    class SetupWizardStatusAdmin {
        +list_display
        +list_filter
        +readonly_fields
        +fieldsets
    }
```
