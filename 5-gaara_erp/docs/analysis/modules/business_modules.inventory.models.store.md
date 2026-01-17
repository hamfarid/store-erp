# business_modules.inventory.models.store

## Imports
- django.db
- django.utils.translation

## Classes
- Store
  - attr: `name`
  - attr: `location_description`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `is_available`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- is_available

## Class Diagram

```mermaid
classDiagram
    class Store {
        +name
        +location_description
        +is_active
        +created_at
        +updated_at
        +__str__()
        +is_available()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Store --> Meta
```
