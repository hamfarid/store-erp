# admin_modules.custom_admin.serializers.notifications_serializers

## Imports
- models
- rest_framework

## Classes
- AdminNotificationSerializer
  - attr: `user_username`
  - attr: `notification_type_display`
  - attr: `level_display`
- AIUsageReportSerializer
  - attr: `user_username`
- SystemAlertSerializer
  - attr: `alert_type_display`
  - attr: `severity_display`
  - attr: `resolved_by_username`
- AuditLogSerializer
  - attr: `user_username`
  - attr: `action_display`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`

## Class Diagram

```mermaid
classDiagram
    class AdminNotificationSerializer {
        +user_username
        +notification_type_display
        +level_display
    }
    class AIUsageReportSerializer {
        +user_username
    }
    class SystemAlertSerializer {
        +alert_type_display
        +severity_display
        +resolved_by_username
    }
    class AuditLogSerializer {
        +user_username
        +action_display
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    AdminNotificationSerializer --> Meta
    AdminNotificationSerializer --> Meta
    AdminNotificationSerializer --> Meta
    AdminNotificationSerializer --> Meta
    AIUsageReportSerializer --> Meta
    AIUsageReportSerializer --> Meta
    AIUsageReportSerializer --> Meta
    AIUsageReportSerializer --> Meta
    SystemAlertSerializer --> Meta
    SystemAlertSerializer --> Meta
    SystemAlertSerializer --> Meta
    SystemAlertSerializer --> Meta
    AuditLogSerializer --> Meta
    AuditLogSerializer --> Meta
    AuditLogSerializer --> Meta
    AuditLogSerializer --> Meta
```
