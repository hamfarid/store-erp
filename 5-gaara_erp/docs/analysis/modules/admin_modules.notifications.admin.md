# admin_modules.notifications.admin

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
- NotificationTypeAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- NotificationChannelAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- UserNotificationPreferenceAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
- NotificationDeliveryAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`

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
    class NotificationTypeAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class NotificationChannelAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class UserNotificationPreferenceAdmin {
        +list_display
        +list_filter
        +search_fields
    }
    class NotificationDeliveryAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
```
