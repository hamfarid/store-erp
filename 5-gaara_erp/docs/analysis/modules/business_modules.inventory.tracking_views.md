# business_modules.inventory.tracking_views

## Imports
- django_filters.rest_framework
- rest_framework
- serializers
- tracking

## Classes
- LotViewSet
  - attr: `queryset`
  - attr: `serializer_class`
  - attr: `permission_classes`
  - attr: `filter_backends`
  - attr: `filterset_fields`
  - attr: `search_fields`
  - attr: `ordering_fields`
- BatchViewSet
  - attr: `queryset`
  - attr: `serializer_class`
  - attr: `permission_classes`
  - attr: `filter_backends`
  - attr: `filterset_fields`
  - attr: `search_fields`
  - attr: `ordering_fields`

## Class Diagram

```mermaid
classDiagram
    class LotViewSet {
        +queryset
        +serializer_class
        +permission_classes
        +filter_backends
        +filterset_fields
        +... (2 more)
    }
    class BatchViewSet {
        +queryset
        +serializer_class
        +permission_classes
        +filter_backends
        +filterset_fields
        +... (2 more)
    }
```
