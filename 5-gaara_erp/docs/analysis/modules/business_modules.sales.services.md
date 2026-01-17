# business_modules.sales.services

## Imports
- business_modules.accounting.models.settlement
- business_modules.contacts.models
- django.db
- django.db.models
- django.utils
- models

## Classes
- SalesInvoiceService
  - method: `get_invoices`
  - method: `get_invoice`
  - method: `create_invoice`
  - method: `update_invoice`
  - method: `confirm_invoice`
  - method: `cancel_invoice`
  - method: `add_payment`
  - method: `get_customer_invoices_summary`
  - method: `get_customer_settlement_eligible_invoices`
  - method: `process_settlement_payment`

## Functions
- get_invoices
- get_invoice
- create_invoice
- update_invoice
- confirm_invoice
- cancel_invoice
- add_payment
- get_customer_invoices_summary
- get_customer_settlement_eligible_invoices
- process_settlement_payment

## Class Diagram

```mermaid
classDiagram
    class SalesInvoiceService {
        +get_invoices()
        +get_invoice()
        +create_invoice()
        +update_invoice()
        +confirm_invoice()
        +... (5 more)
    }
```
