# utility_modules.utilities.views

## Imports
- rest_framework

## Classes
- IsAdminOrReadOnly
  - method: `has_permission`
- SystemMetricViewSet
  - attr: `permission_classes`
  - attr: `queryset`
  - attr: `serializer_class`
- DatabaseStatusViewSet
  - attr: `permission_classes`
  - attr: `queryset`
  - attr: `serializer_class`
- UserStatisticViewSet
  - attr: `permission_classes`
  - attr: `queryset`
  - attr: `serializer_class`
- SystemAlertViewSet
  - attr: `permission_classes`
  - attr: `queryset`
  - attr: `serializer_class`
  - method: `perform_update`
- UserActivityLogViewSet
  - attr: `permission_classes`
  - attr: `queryset`
  - attr: `serializer_class`
- SystemErrorLogViewSet
  - attr: `permission_classes`
  - attr: `queryset`
  - attr: `serializer_class`

## Functions
- has_permission
- perform_update

## Class Diagram

```mermaid
classDiagram
    class IsAdminOrReadOnly {
        +has_permission()
    }
    class SystemMetricViewSet {
        +permission_classes
        +queryset
        +serializer_class
    }
    class DatabaseStatusViewSet {
        +permission_classes
        +queryset
        +serializer_class
    }
    class UserStatisticViewSet {
        +permission_classes
        +queryset
        +serializer_class
    }
    class SystemAlertViewSet {
        +permission_classes
        +queryset
        +serializer_class
        +perform_update()
    }
    class UserActivityLogViewSet {
        +permission_classes
        +queryset
        +serializer_class
    }
    class SystemErrorLogViewSet {
        +permission_classes
        +queryset
        +serializer_class
    }
```
