# admin_modules.health_monitoring.admin

## Imports
- django.contrib
- models

## Classes
- ServerMetricAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `date_hierarchy`
  - attr: `readonly_fields`
- UserActivityLogAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `date_hierarchy`
  - attr: `raw_id_fields`
  - attr: `readonly_fields`
- SystemEventLogAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `date_hierarchy`
  - attr: `readonly_fields`

## Class Diagram

```mermaid
classDiagram
    class ServerMetricAdmin {
        +list_display
        +list_filter
        +date_hierarchy
        +readonly_fields
    }
    class UserActivityLogAdmin {
        +list_display
        +list_filter
        +search_fields
        +date_hierarchy
        +raw_id_fields
        +... (1 more)
    }
    class SystemEventLogAdmin {
        +list_display
        +list_filter
        +search_fields
        +date_hierarchy
        +readonly_fields
    }
```
