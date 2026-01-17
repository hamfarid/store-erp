# business_modules.sales.models.sales_order

## Imports
- core_modules.companies.models
- core_modules.core.models.base_models
- customer
- django.db
- django.utils
- django.utils.translation

## Classes
- PaymentTerm
  - attr: `name`
  - attr: `days`
  - method: `__str__`
- Tax
  - attr: `name`
  - attr: `rate`
  - method: `__str__`
- BaseModel
- SalesOrder
  - attr: `order_number`
  - attr: `reference`
  - attr: `company`
  - attr: `customer`
  - attr: `order_date`
  - attr: `validity_date`
  - attr: `expected_delivery_date`
  - attr: `payment_term`
  - attr: `untaxed_amount`
  - attr: `tax_amount`
  - attr: `total_amount`
  - attr: `state`
  - attr: `notes`
  - method: `__str__`
  - method: `confirm`
  - method: `cancel`
  - method: `calculate_amounts`
- Meta
  - attr: `app_label`
- Meta
  - attr: `app_label`
- Meta
  - attr: `abstract`
  - attr: `app_label`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `app_label`

## Functions
- __str__
- __str__
- __str__
- confirm
- cancel
- calculate_amounts

## Class Diagram

```mermaid
classDiagram
    class PaymentTerm {
        +name
        +days
        +__str__()
    }
    class Tax {
        +name
        +rate
        +__str__()
    }
    class BaseModel {
    }
    class SalesOrder {
        +order_number
        +reference
        +company
        +customer
        +order_date
        +... (8 more)
        +__str__()
        +confirm()
        +cancel()
        +calculate_amounts()
    }
    class Meta {
        +app_label
    }
    class Meta {
        +app_label
    }
    class Meta {
        +abstract
        +app_label
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +app_label
    }
    PaymentTerm --> Meta
    PaymentTerm --> Meta
    PaymentTerm --> Meta
    PaymentTerm --> Meta
    Tax --> Meta
    Tax --> Meta
    Tax --> Meta
    Tax --> Meta
    BaseModel --> Meta
    BaseModel --> Meta
    BaseModel --> Meta
    BaseModel --> Meta
    SalesOrder --> Meta
    SalesOrder --> Meta
    SalesOrder --> Meta
    SalesOrder --> Meta
```
