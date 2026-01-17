# business_modules.purchasing.requisitions

## Imports
- business_modules.inventory.products
- decimal
- django.conf
- django.core.exceptions
- django.core.validators
- django.db
- django.utils
- django.utils.translation
- hr.models

## Classes
- AnnualPurchaseRequisition
  - attr: `year`
  - attr: `department`
  - attr: `status`
  - attr: `creation_date`
  - attr: `created_by`
  - attr: `notes`
  - method: `__str__`
  - method: `clean`
- AnnualPurchaseRequisitionItem
  - attr: `annual_requisition`
  - attr: `product`
  - attr: `total_required_quantity`
  - attr: `consumed_quantity`
  - attr: `notes`
  - method: `__str__`
  - method: `remaining_quantity`
  - method: `clean`
- StatusChoices
  - attr: `OPEN`
  - attr: `CLOSED`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `ordering`
  - attr: `indexes`

## Functions
- __str__
- clean
- __str__
- remaining_quantity
- clean

## Class Diagram

```mermaid
classDiagram
    class AnnualPurchaseRequisition {
        +year
        +department
        +status
        +creation_date
        +created_by
        +... (1 more)
        +__str__()
        +clean()
    }
    class AnnualPurchaseRequisitionItem {
        +annual_requisition
        +product
        +total_required_quantity
        +consumed_quantity
        +notes
        +__str__()
        +remaining_quantity()
        +clean()
    }
    class StatusChoices {
        +OPEN
        +CLOSED
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +unique_together
        +ordering
        +... (1 more)
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +unique_together
        +ordering
        +... (1 more)
    }
    AnnualPurchaseRequisition --> Meta
    AnnualPurchaseRequisition --> Meta
    AnnualPurchaseRequisitionItem --> Meta
    AnnualPurchaseRequisitionItem --> Meta
    StatusChoices --> Meta
    StatusChoices --> Meta
```
