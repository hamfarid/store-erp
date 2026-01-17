# business_modules.purchasing.models.stub_minimal

## Imports
- __future__

## Classes
- PurchaseInvoiceStatus
  - attr: `CONFIRMED`
  - attr: `PARTIALLY_PAID`
- _BaseInvoice
  - attr: `id`
  - attr: `remaining_balance`
  - attr: `objects`
  - attr: `is_settlement`
- PurchaseInvoice
- PurchaseReturn

## Module Variables
- `__all__`

## Class Diagram

```mermaid
classDiagram
    class PurchaseInvoiceStatus {
        +CONFIRMED
        +PARTIALLY_PAID
    }
    class _BaseInvoice {
        +id
        +remaining_balance
        +objects
        +is_settlement
    }
    class PurchaseInvoice {
    }
    class PurchaseReturn {
    }
```
