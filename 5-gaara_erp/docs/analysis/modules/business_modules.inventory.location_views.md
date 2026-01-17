# business_modules.inventory.location_views

## Imports
- base
- django.db
- django_filters.rest_framework
- rest_framework

## Classes
- SimpleSiteSerializer
- SimpleStoreSerializer
- SimpleStorePermissionSerializer
- SiteViewSet
  - attr: `queryset`
  - attr: `serializer_class`
  - attr: `permission_classes`
  - attr: `filter_backends`
  - attr: `filterset_fields`
  - attr: `search_fields`
  - attr: `ordering_fields`
- StoreViewSet
  - attr: `queryset`
  - attr: `serializer_class`
  - attr: `permission_classes`
  - attr: `filter_backends`
  - attr: `filterset_fields`
  - attr: `search_fields`
  - attr: `ordering_fields`
- StorePermissionViewSet
  - attr: `queryset`
  - attr: `serializer_class`
  - attr: `permission_classes`
  - attr: `filter_backends`
  - attr: `filterset_fields`
  - attr: `ordering_fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`

## Class Diagram

```mermaid
classDiagram
    class SimpleSiteSerializer {
    }
    class SimpleStoreSerializer {
    }
    class SimpleStorePermissionSerializer {
    }
    class SiteViewSet {
        +queryset
        +serializer_class
        +permission_classes
        +filter_backends
        +filterset_fields
        +... (2 more)
    }
    class StoreViewSet {
        +queryset
        +serializer_class
        +permission_classes
        +filter_backends
        +filterset_fields
        +... (2 more)
    }
    class StorePermissionViewSet {
        +queryset
        +serializer_class
        +permission_classes
        +filter_backends
        +filterset_fields
        +... (1 more)
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
    SimpleSiteSerializer --> Meta
    SimpleSiteSerializer --> Meta
    SimpleSiteSerializer --> Meta
    SimpleStoreSerializer --> Meta
    SimpleStoreSerializer --> Meta
    SimpleStoreSerializer --> Meta
    SimpleStorePermissionSerializer --> Meta
    SimpleStorePermissionSerializer --> Meta
    SimpleStorePermissionSerializer --> Meta
    SiteViewSet --> Meta
    SiteViewSet --> Meta
    SiteViewSet --> Meta
    StoreViewSet --> Meta
    StoreViewSet --> Meta
    StoreViewSet --> Meta
    StorePermissionViewSet --> Meta
    StorePermissionViewSet --> Meta
    StorePermissionViewSet --> Meta
```
