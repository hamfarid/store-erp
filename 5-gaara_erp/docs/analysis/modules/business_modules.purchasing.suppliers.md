# business_modules.purchasing.suppliers

## Imports
- contacts.models
- core_modules.organization.models
- decimal
- django.core.validators
- django.db
- django.utils.translation

## Classes
- SupplierProfile
  - attr: `contact`
  - attr: `payment_methods`
  - attr: `tax_id`
  - attr: `bank_account_details`
  - attr: `credit_limit`
  - attr: `default_currency`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`

## Functions
- __str__

## Class Diagram

```mermaid
classDiagram
    class SupplierProfile {
        +contact
        +payment_methods
        +tax_id
        +bank_account_details
        +credit_limit
        +... (1 more)
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    SupplierProfile --> Meta
```
