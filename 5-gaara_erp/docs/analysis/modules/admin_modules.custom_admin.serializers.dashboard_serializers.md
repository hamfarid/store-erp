# admin_modules.custom_admin.serializers.dashboard_serializers

## Imports
- models
- rest_framework

## Classes
- DashboardWidgetSerializer
  - attr: `user_username`
- DashboardLayoutSerializer
  - attr: `user_username`
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
    class DashboardWidgetSerializer {
        +user_username
    }
    class DashboardLayoutSerializer {
        +user_username
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
    DashboardWidgetSerializer --> Meta
    DashboardWidgetSerializer --> Meta
    DashboardLayoutSerializer --> Meta
    DashboardLayoutSerializer --> Meta
```
