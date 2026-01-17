# agricultural_modules.farms.permissions

## Imports
- rest_framework

## Classes
- IsAdminOrReadOnly
  - method: `has_permission`
- IsOwnerOrAdminElseReadOnly
  - method: `has_object_permission`

## Functions
- has_permission
- has_object_permission

## Class Diagram

```mermaid
classDiagram
    class IsAdminOrReadOnly {
        +has_permission()
    }
    class IsOwnerOrAdminElseReadOnly {
        +has_object_permission()
    }
```
