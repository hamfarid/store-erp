# core_modules.core.models.currency

## Imports
- base_models
- decimal
- django.db
- django.utils.translation

## Classes
- Currency
  - attr: `name`
  - attr: `code`
  - attr: `symbol`
  - attr: `exchange_rate`
  - attr: `is_base`
  - attr: `is_active`
  - method: `__str__`
  - method: `save`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- save

## Class Diagram

```mermaid
classDiagram
    class Currency {
        +name
        +code
        +symbol
        +exchange_rate
        +is_base
        +... (1 more)
        +__str__()
        +save()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Currency --> Meta
```
