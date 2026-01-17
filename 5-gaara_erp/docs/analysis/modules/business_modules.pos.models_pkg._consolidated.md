# business_modules.pos.models_pkg._consolidated

## Imports
- business_modules.accounting.models
- business_modules.inventory.models
- core_modules.companies.models
- decimal
- django.core.validators
- django.db
- django.utils
- django.utils.translation

## Classes
- POSConfig
  - attr: `name`
  - attr: `company`
  - attr: `warehouse`
  - attr: `journal`
  - attr: `is_active`
  - attr: `allow_discount`
  - attr: `allow_price_change`
  - attr: `allow_credit_sales`
  - attr: `allow_returns`
  - attr: `receipt_header`
  - attr: `receipt_footer`
  - method: `__str__`
- POSSession
  - attr: `STATES`
  - attr: `name`
  - attr: `config`
  - attr: `opening_date`
  - attr: `closing_date`
  - attr: `state`
  - attr: `opening_balance`
  - attr: `closing_balance`
  - attr: `cash_register_balance`
  - attr: `notes`
  - method: `__str__`
- POSOrder
  - attr: `STATES`
  - attr: `name`
  - attr: `session`
  - attr: `date_order`
  - attr: `state`
  - attr: `amount_total`
  - attr: `amount_tax`
  - attr: `amount_paid`
  - attr: `amount_return`
  - attr: `note`
  - method: `__str__`
  - method: `recalculate_amounts`
  - method: `is_fully_paid`
- POSOrderLine
  - attr: `order`
  - attr: `product`
  - attr: `qty`
  - attr: `price_unit`
  - attr: `price_subtotal`
  - attr: `discount`
  - method: `__str__`
  - method: `_compute_subtotal`
  - method: `save`
  - method: `delete`
- POSPayment
  - attr: `PAYMENT_METHODS`
  - attr: `order`
  - attr: `payment_method`
  - attr: `amount`
  - attr: `payment_date`
  - method: `__str__`
  - method: `save`
  - method: `delete`
- Meta
  - attr: `app_label`
  - attr: `ordering`
  - attr: `unique_together`
- Meta
  - attr: `app_label`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `ordering`

## Functions
- __str__
- __str__
- __str__
- recalculate_amounts
- is_fully_paid
- __str__
- _compute_subtotal
- save
- delete
- __str__
- save
- delete

## Class Diagram

```mermaid
classDiagram
    class POSConfig {
        +name
        +company
        +warehouse
        +journal
        +is_active
        +... (6 more)
        +__str__()
    }
    class POSSession {
        +STATES
        +name
        +config
        +opening_date
        +closing_date
        +... (5 more)
        +__str__()
    }
    class POSOrder {
        +STATES
        +name
        +session
        +date_order
        +state
        +... (5 more)
        +__str__()
        +recalculate_amounts()
        +is_fully_paid()
    }
    class POSOrderLine {
        +order
        +product
        +qty
        +price_unit
        +price_subtotal
        +... (1 more)
        +__str__()
        +_compute_subtotal()
        +save()
        +delete()
    }
    class POSPayment {
        +PAYMENT_METHODS
        +order
        +payment_method
        +amount
        +payment_date
        +__str__()
        +save()
        +delete()
    }
    class Meta {
        +app_label
        +ordering
        +unique_together
    }
    class Meta {
        +app_label
        +ordering
    }
    class Meta {
        +app_label
        +ordering
    }
    class Meta {
        +app_label
        +ordering
    }
    class Meta {
        +app_label
        +ordering
    }
    POSConfig --> Meta
    POSConfig --> Meta
    POSConfig --> Meta
    POSConfig --> Meta
    POSConfig --> Meta
    POSSession --> Meta
    POSSession --> Meta
    POSSession --> Meta
    POSSession --> Meta
    POSSession --> Meta
    POSOrder --> Meta
    POSOrder --> Meta
    POSOrder --> Meta
    POSOrder --> Meta
    POSOrder --> Meta
    POSOrderLine --> Meta
    POSOrderLine --> Meta
    POSOrderLine --> Meta
    POSOrderLine --> Meta
    POSOrderLine --> Meta
    POSPayment --> Meta
    POSPayment --> Meta
    POSPayment --> Meta
    POSPayment --> Meta
    POSPayment --> Meta
```
