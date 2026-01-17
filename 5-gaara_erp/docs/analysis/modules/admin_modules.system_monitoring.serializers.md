# admin_modules.system_monitoring.serializers

## Imports
- django.contrib.auth
- models
- rest_framework

## Classes
- UserSimpleSerializer
- SystemMetricSerializer
- AlertSerializer
  - attr: `acknowledged_by`
  - attr: `related_metric`
  - attr: `severity_display`
  - attr: `status_display`
- ModuleStatusSerializer
  - attr: `status_display`
- Meta
  - attr: `model`
  - attr: `fields`
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

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class UserSimpleSerializer {
    }
    class SystemMetricSerializer {
    }
    class AlertSerializer {
        +acknowledged_by
        +related_metric
        +severity_display
        +status_display
    }
    class ModuleStatusSerializer {
        +status_display
    }
    class Meta {
        +model
        +fields
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
    UserSimpleSerializer --> Meta
    UserSimpleSerializer --> Meta
    UserSimpleSerializer --> Meta
    UserSimpleSerializer --> Meta
    SystemMetricSerializer --> Meta
    SystemMetricSerializer --> Meta
    SystemMetricSerializer --> Meta
    SystemMetricSerializer --> Meta
    AlertSerializer --> Meta
    AlertSerializer --> Meta
    AlertSerializer --> Meta
    AlertSerializer --> Meta
    ModuleStatusSerializer --> Meta
    ModuleStatusSerializer --> Meta
    ModuleStatusSerializer --> Meta
    ModuleStatusSerializer --> Meta
```
