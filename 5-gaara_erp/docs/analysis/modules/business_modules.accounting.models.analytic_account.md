# business_modules.accounting.models.analytic_account

## Imports
- django.db
- django.utils.translation

## Classes
- AnalyticAccount
  - attr: `name`
  - attr: `code`
  - attr: `parent`
  - attr: `description`
  - attr: `is_active`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`

## Functions
- __str__

## Class Diagram

```mermaid
classDiagram
    class AnalyticAccount {
        +name
        +code
        +parent
        +description
        +is_active
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    AnalyticAccount --> Meta
```
