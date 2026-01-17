# admin_modules.notifications.backup_files.admin

## Imports
- django.contrib
- models

## Classes
- NotificationAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `list_editable`
  - method: `get_queryset`

## Functions
- get_queryset

## Class Diagram

```mermaid
classDiagram
    class NotificationAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +list_editable
        +get_queryset()
    }
```
