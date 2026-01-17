# services_modules.beneficiaries.admin

## Imports
- django.contrib
- django.utils.translation
- models.beneficiary
- models.beneficiary_category

## Classes
- BeneficiaryCategoryAdmin
  - attr: `list_display`
  - attr: `search_fields`
- BeneficiaryAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`

## Class Diagram

```mermaid
classDiagram
    class BeneficiaryCategoryAdmin {
        +list_display
        +search_fields
    }
    class BeneficiaryAdmin {
        +list_display
        +list_filter
        +search_fields
    }
```
