# business_modules.purchasing.models.goods_receipt

## Imports
- business_modules.inventory.models
- core_modules.companies.models
- core_modules.core.models.base_models
- django.core.validators
- django.db
- django.utils
- django.utils.translation
- purchase_order
- supplier

## Classes
- GoodsReceipt
  - attr: `STATES`
  - attr: `name`
  - attr: `purchase_order`
  - attr: `supplier`
  - attr: `company`
  - attr: `branch`
  - attr: `warehouse`
  - attr: `receipt_date`
  - attr: `state`
  - attr: `notes`
  - method: `__str__`
- GoodsReceiptItem
  - attr: `goods_receipt`
  - attr: `product`
  - attr: `ordered_quantity`
  - attr: `received_quantity`
  - attr: `unit_of_measure`
  - attr: `notes`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`

## Functions
- __str__
- __str__

## Class Diagram

```mermaid
classDiagram
    class GoodsReceipt {
        +STATES
        +name
        +purchase_order
        +supplier
        +company
        +... (5 more)
        +__str__()
    }
    class GoodsReceiptItem {
        +goods_receipt
        +product
        +ordered_quantity
        +received_quantity
        +unit_of_measure
        +... (1 more)
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +unique_together
    }
    GoodsReceipt --> Meta
    GoodsReceipt --> Meta
    GoodsReceiptItem --> Meta
    GoodsReceiptItem --> Meta
```
