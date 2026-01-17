# business_modules.purchasing.invoices

## Imports
- business_modules.inventory.products
- contacts.models
- core_modules.organization.models
- decimal
- django.conf
- django.core.validators
- django.db
- django.utils.translation
- goods_receipt

## Classes
- PurchaseInvoice
  - attr: `supplier`
  - attr: `invoice_date`
  - attr: `approval_date`
  - attr: `due_date`
  - attr: `supplier_invoice_number`
  - attr: `status`
  - attr: `total_amount`
  - attr: `tax_amount`
  - attr: `discount_amount`
  - attr: `additional_costs_total`
  - attr: `currency`
  - attr: `exchange_rate_at_approval`
  - attr: `notes`
  - attr: `created_by`
  - attr: `approved_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `calculate_totals`
- PurchaseInvoiceItem
  - attr: `purchase_invoice`
  - attr: `grn_item`
  - attr: `product`
  - attr: `quantity`
  - attr: `unit_price`
  - attr: `tax_rate`
  - attr: `discount_percentage`
  - attr: `total_price`
  - attr: `notes`
  - method: `__str__`
  - method: `save`
  - method: `delete`
- PurchaseInvoiceExpense
  - attr: `purchase_invoice`
  - attr: `expense_description`
  - attr: `amount`
  - attr: `currency`
  - attr: `is_payable_to_supplier`
  - attr: `distribute_to_item_cost`
  - method: `__str__`
  - method: `save`
  - method: `delete`
- StatusChoices
  - attr: `DRAFT`
  - attr: `PENDING_APPROVAL`
  - attr: `APPROVED`
  - attr: `PARTIALLY_PAID`
  - attr: `FULLY_PAID`
  - attr: `REJECTED`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`

## Functions
- __str__
- calculate_totals
- __str__
- save
- delete
- __str__
- save
- delete

## Class Diagram

```mermaid
classDiagram
    class PurchaseInvoice {
        +supplier
        +invoice_date
        +approval_date
        +due_date
        +supplier_invoice_number
        +... (12 more)
        +__str__()
        +calculate_totals()
    }
    class PurchaseInvoiceItem {
        +purchase_invoice
        +grn_item
        +product
        +quantity
        +unit_price
        +... (4 more)
        +__str__()
        +save()
        +delete()
    }
    class PurchaseInvoiceExpense {
        +purchase_invoice
        +expense_description
        +amount
        +currency
        +is_payable_to_supplier
        +... (1 more)
        +__str__()
        +save()
        +delete()
    }
    class StatusChoices {
        +DRAFT
        +PENDING_APPROVAL
        +APPROVED
        +PARTIALLY_PAID
        +FULLY_PAID
        +... (1 more)
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    PurchaseInvoice --> Meta
    PurchaseInvoice --> Meta
    PurchaseInvoice --> Meta
    PurchaseInvoiceItem --> Meta
    PurchaseInvoiceItem --> Meta
    PurchaseInvoiceItem --> Meta
    PurchaseInvoiceExpense --> Meta
    PurchaseInvoiceExpense --> Meta
    PurchaseInvoiceExpense --> Meta
    StatusChoices --> Meta
    StatusChoices --> Meta
    StatusChoices --> Meta
```
