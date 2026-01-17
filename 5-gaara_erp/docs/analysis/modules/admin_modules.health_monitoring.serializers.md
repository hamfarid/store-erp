# admin_modules.health_monitoring.serializers

## Imports
- models
- rest_framework
- users_accounts.serializers

## Classes
- ServerMetricSerializer
- UserActivityLogSerializer
  - attr: `user`
- SystemEventLogSerializer
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- UserSerializer
  - attr: `username`
  - method: `create`
  - method: `update`

## Functions
- create
- update

## Class Diagram

```mermaid
classDiagram
    class ServerMetricSerializer {
    }
    class UserActivityLogSerializer {
        +user
    }
    class SystemEventLogSerializer {
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class UserSerializer {
        +username
        +create()
        +update()
    }
    ServerMetricSerializer --> Meta
    ServerMetricSerializer --> Meta
    ServerMetricSerializer --> Meta
    UserActivityLogSerializer --> Meta
    UserActivityLogSerializer --> Meta
    UserActivityLogSerializer --> Meta
    SystemEventLogSerializer --> Meta
    SystemEventLogSerializer --> Meta
    SystemEventLogSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
```
