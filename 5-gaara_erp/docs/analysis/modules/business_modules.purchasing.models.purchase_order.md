# business_modules.purchasing.models.purchase_order

## Imports
- business_modules.inventory.models
- core_modules.companies.models
- decimal
- django.db
- django.utils
- django.utils.translation
- supplier

## Classes
- PurchaseOrder
  - attr: `name`
  - attr: `reference`
  - attr: `company`
  - attr: `supplier`
  - attr: `date`
  - attr: `expected_date`
  - attr: `warehouse`
  - attr: `untaxed_amount`
  - attr: `tax_amount`
  - attr: `total_amount`
  - attr: `state`
  - attr: `notes`
  - method: `__str__`
  - method: `confirm`
  - method: `cancel`
  - method: `calculate_amounts`
- PurchaseOrderLine
  - attr: `order`
  - attr: `product`
  - attr: `quantity`
  - attr: `unit_price`
  - attr: `discount_percent`
  - attr: `discount_amount`
  - attr: `tax_amount`
  - attr: `subtotal`
  - attr: `total`
  - attr: `description`
  - attr: `sequence`
  - attr: `expected_date`
  - method: `__str__`
  - method: `calculate_amounts`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- confirm
- cancel
- calculate_amounts
- __str__
- calculate_amounts

## Class Diagram

```mermaid
classDiagram
    class PurchaseOrder {
        +name
        +reference
        +company
        +supplier
        +date
        +... (7 more)
        +__str__()
        +confirm()
        +cancel()
        +calculate_amounts()
    }
    class PurchaseOrderLine {
        +order
        +product
        +quantity
        +unit_price
        +discount_percent
        +... (7 more)
        +__str__()
        +calculate_amounts()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +unique_together
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    PurchaseOrder --> Meta
    PurchaseOrder --> Meta
    PurchaseOrderLine --> Meta
    PurchaseOrderLine --> Meta
```
