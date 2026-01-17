# business_modules.purchasing.receipts

## Imports
- business_modules.inventory.base
- business_modules.inventory.products
- contacts.models
- decimal
- django.conf
- django.core.exceptions
- django.core.validators
- django.db
- django.utils
- django.utils.translation
- orders

## Classes
- GoodsReceiptNote
  - attr: `supplier`
  - attr: `purchase_order`
  - attr: `grn_date`
  - attr: `status`
  - attr: `received_by`
  - attr: `store`
  - attr: `notes`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `clean`
- GoodsReceiptNoteItem
  - attr: `grn`
  - attr: `po_item`
  - attr: `product`
  - attr: `received_quantity`
  - attr: `notes`
  - method: `__str__`
  - method: `clean`
- StatusChoices
  - attr: `DRAFT`
  - attr: `COMPLETED`
  - attr: `INVOICED`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`

## Functions
- __str__
- clean
- __str__
- clean

## Class Diagram

```mermaid
classDiagram
    class GoodsReceiptNote {
        +supplier
        +purchase_order
        +grn_date
        +status
        +received_by
        +... (4 more)
        +__str__()
        +clean()
    }
    class GoodsReceiptNoteItem {
        +grn
        +po_item
        +product
        +received_quantity
        +notes
        +__str__()
        +clean()
    }
    class StatusChoices {
        +DRAFT
        +COMPLETED
        +INVOICED
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    GoodsReceiptNote --> Meta
    GoodsReceiptNote --> Meta
    GoodsReceiptNoteItem --> Meta
    GoodsReceiptNoteItem --> Meta
    StatusChoices --> Meta
    StatusChoices --> Meta
```
