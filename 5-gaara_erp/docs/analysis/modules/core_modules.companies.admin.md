# core_modules.companies.admin

## Imports
- django.contrib
- models

## Classes
- CountryAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
- CompanyAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
- BranchAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`

## Class Diagram

```mermaid
classDiagram
    class CountryAdmin {
        +list_display
        +search_fields
        +list_filter
    }
    class CompanyAdmin {
        +list_display
        +search_fields
        +list_filter
    }
    class BranchAdmin {
        +list_display
        +search_fields
        +list_filter
    }
```
