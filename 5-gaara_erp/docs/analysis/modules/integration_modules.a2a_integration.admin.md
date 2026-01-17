# integration_modules.a2a_integration.admin

## Imports
- django.contrib
- django.db
- models

## Classes
- ExternalSystemAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- IntegrationConfigAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- APICredentialAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `exclude`
- IntegrationLogAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`

## Class Diagram

```mermaid
classDiagram
    class ExternalSystemAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class IntegrationConfigAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class APICredentialAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +exclude
    }
    class IntegrationLogAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
```
