# business_modules.accounting.invoices

## Imports
- business_modules.accounting.models.tax
- business_modules.contacts.models
- business_modules.purchasing.models
- core_modules.organization.models
- decimal
- django.db
- django.utils.translation
- typing

## Classes
- SalesInvoice
  - attr: `STATUS_CHOICES`
  - attr: `invoice_number`
  - attr: `customer`
  - attr: `branch`
  - attr: `invoice_date`
  - attr: `due_date`
  - attr: `currency`
  - attr: `total_amount`
  - attr: `tax_amount`
  - attr: `net_amount`
  - attr: `paid_amount`
  - attr: `status`
  - attr: `notes`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- SalesInvoiceItem
  - attr: `sales_invoice`
  - attr: `product_description`
  - attr: `quantity`
  - attr: `unit_price`
  - attr: `discount_amount`
  - attr: `tax`
  - attr: `tax_amount`
  - attr: `line_total`
- PurchaseInvoice
  - attr: `STATUS_CHOICES`
  - attr: `invoice_number`
  - attr: `purchase_order`
  - attr: `supplier`
  - attr: `branch`
  - attr: `invoice_date`
  - attr: `due_date`
  - attr: `currency`
  - attr: `total_amount`
  - attr: `tax_amount`
  - attr: `net_amount`
  - attr: `paid_amount`
  - attr: `status`
  - attr: `notes`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- PurchaseInvoiceItem
  - attr: `purchase_invoice`
  - attr: `product_description`
  - attr: `quantity`
  - attr: `unit_price`
  - attr: `discount_amount`
  - attr: `tax`
  - attr: `tax_amount`
  - attr: `line_total`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`

## Functions
- __str__
- __str__

## Class Diagram

```mermaid
classDiagram
    class SalesInvoice {
        +STATUS_CHOICES
        +invoice_number
        +customer
        +branch
        +invoice_date
        +... (10 more)
        +__str__()
    }
    class SalesInvoiceItem {
        +sales_invoice
        +product_description
        +quantity
        +unit_price
        +discount_amount
        +... (3 more)
    }
    class PurchaseInvoice {
        +STATUS_CHOICES
        +invoice_number
        +purchase_order
        +supplier
        +branch
        +... (11 more)
        +__str__()
    }
    class PurchaseInvoiceItem {
        +purchase_invoice
        +product_description
        +quantity
        +unit_price
        +discount_amount
        +... (3 more)
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    SalesInvoice --> Meta
    SalesInvoice --> Meta
    SalesInvoice --> Meta
    SalesInvoice --> Meta
    SalesInvoiceItem --> Meta
    SalesInvoiceItem --> Meta
    SalesInvoiceItem --> Meta
    SalesInvoiceItem --> Meta
    PurchaseInvoice --> Meta
    PurchaseInvoice --> Meta
    PurchaseInvoice --> Meta
    PurchaseInvoice --> Meta
    PurchaseInvoiceItem --> Meta
    PurchaseInvoiceItem --> Meta
    PurchaseInvoiceItem --> Meta
    PurchaseInvoiceItem --> Meta
```
