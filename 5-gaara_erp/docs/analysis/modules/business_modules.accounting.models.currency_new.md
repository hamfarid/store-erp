# business_modules.accounting.models.currency_new

## Imports
- django.db
- django.utils.translation

## Classes
- Currency
  - attr: `code`
  - attr: `name`
  - attr: `symbol`
  - attr: `is_active`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__

## Class Diagram

```mermaid
classDiagram
    class Currency {
        +code
        +name
        +symbol
        +is_active
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Currency --> Meta
```
