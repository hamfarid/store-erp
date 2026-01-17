# business_modules.purchasing.models.payment_method

## Imports
- core_modules.core.models.base_models
- django.db
- django.utils.translation

## Classes
- PaymentMethod
  - attr: `name`
  - attr: `description`
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
    class PaymentMethod {
        +name
        +description
        +is_active
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    PaymentMethod --> Meta
```
