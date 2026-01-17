# core_modules.system_settings.serializers

## Imports
- models
- rest_framework

## Classes
- SystemSettingSerializer
  - attr: `category_display`
  - attr: `value_type_display`
- CountrySerializer
- CurrencySerializer
- EmailSettingSerializer
- SetupWizardStatusSerializer
  - attr: `current_step_display`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
  - attr: `extra_kwargs`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`

## Class Diagram

```mermaid
classDiagram
    class SystemSettingSerializer {
        +category_display
        +value_type_display
    }
    class CountrySerializer {
    }
    class CurrencySerializer {
    }
    class EmailSettingSerializer {
    }
    class SetupWizardStatusSerializer {
        +current_step_display
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
        +extra_kwargs
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    SystemSettingSerializer --> Meta
    SystemSettingSerializer --> Meta
    SystemSettingSerializer --> Meta
    SystemSettingSerializer --> Meta
    SystemSettingSerializer --> Meta
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    CurrencySerializer --> Meta
    CurrencySerializer --> Meta
    CurrencySerializer --> Meta
    CurrencySerializer --> Meta
    CurrencySerializer --> Meta
    EmailSettingSerializer --> Meta
    EmailSettingSerializer --> Meta
    EmailSettingSerializer --> Meta
    EmailSettingSerializer --> Meta
    EmailSettingSerializer --> Meta
    SetupWizardStatusSerializer --> Meta
    SetupWizardStatusSerializer --> Meta
    SetupWizardStatusSerializer --> Meta
    SetupWizardStatusSerializer --> Meta
    SetupWizardStatusSerializer --> Meta
```
