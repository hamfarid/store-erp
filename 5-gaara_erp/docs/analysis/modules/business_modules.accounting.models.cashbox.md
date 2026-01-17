# business_modules.accounting.models.cashbox

## Imports
- __future__
- decimal
- django.conf
- django.db
- django.utils
- django.utils.translation
- typing

## Classes
- CashboxTransferStatus
  - attr: `PENDING`
  - attr: `APPROVED`
  - attr: `REJECTED`
  - attr: `COMPLETED`
  - attr: `CANCELLED`
- EngineerCashbox
  - attr: `company`
  - attr: `engineer`
  - attr: `current_balance`
  - attr: `last_updated`
  - method: `__str__`
  - method: `adjust_balance`
- CashboxTransferRequest
  - attr: `company`
  - attr: `source_cashbox`
  - attr: `target_cashbox`
  - attr: `amount`
  - attr: `status`
  - attr: `requested_by`
  - attr: `approved_by`
  - attr: `request_date`
  - attr: `approval_date`
  - attr: `completion_date`
  - attr: `notes`
  - attr: `rejection_reason`
  - method: `__str__`
  - method: `clean`
  - method: `approve`
  - method: `reject`
  - method: `complete`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `constraints`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- adjust_balance
- __str__
- clean
- approve
- reject
- complete

## Class Diagram

```mermaid
classDiagram
    class CashboxTransferStatus {
        +PENDING
        +APPROVED
        +REJECTED
        +COMPLETED
        +CANCELLED
    }
    class EngineerCashbox {
        +company
        +engineer
        +current_balance
        +last_updated
        +__str__()
        +adjust_balance()
    }
    class CashboxTransferRequest {
        +company
        +source_cashbox
        +target_cashbox
        +amount
        +status
        +... (7 more)
        +__str__()
        +clean()
        +approve()
        +reject()
        +complete()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +constraints
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    CashboxTransferStatus --> Meta
    CashboxTransferStatus --> Meta
    EngineerCashbox --> Meta
    EngineerCashbox --> Meta
    CashboxTransferRequest --> Meta
    CashboxTransferRequest --> Meta
```
