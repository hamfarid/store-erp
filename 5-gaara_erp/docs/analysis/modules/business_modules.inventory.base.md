# business_modules.inventory.base

## Imports
- core_modules.organization.models
- decimal
- django.conf
- django.contrib
- django.contrib.auth.models
- django.core.exceptions
- django.db
- django.utils.translation

## Classes
- Site
  - attr: `name_ar`
  - attr: `name_en`
  - attr: `company`
  - attr: `address`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Store
  - attr: `STORE_CATEGORIES`
  - attr: `STORE_SPECIFIC_TYPES`
  - attr: `LOCATION_TYPES`
  - attr: `site`
  - attr: `branch`
  - attr: `parent`
  - attr: `name_ar`
  - attr: `name_en`
  - attr: `location_type`
  - attr: `category`
  - attr: `specific_type`
  - attr: `description`
  - attr: `requires_temp_control`
  - attr: `temperature_min`
  - attr: `temperature_max`
  - attr: `storage_cost_per_day`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `clean`
- StorePermission
  - attr: `ROLE_CHOICES`
  - attr: `store`
  - attr: `user`
  - attr: `role`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- UOM
  - attr: `name_ar`
  - attr: `name_en`
  - attr: `code`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- UOMConversion
  - attr: `from_uom`
  - attr: `to_uom`
  - attr: `conversion_factor`
  - attr: `created_at`
  - attr: `updated_at`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `unique_together`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`

## Functions
- __str__
- __str__
- clean
- __str__
- __str__

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class Site {
        +name_ar
        +name_en
        +company
        +address
        +is_active
        +... (2 more)
        +__str__()
    }
    class Store {
        +STORE_CATEGORIES
        +STORE_SPECIFIC_TYPES
        +LOCATION_TYPES
        +site
        +branch
        +... (14 more)
        +__str__()
        +clean()
    }
    class StorePermission {
        +ROLE_CHOICES
        +store
        +user
        +role
        +created_at
        +... (1 more)
        +__str__()
    }
    class UOM {
        +name_ar
        +name_en
        +code
        +is_active
        +created_at
        +... (1 more)
        +__str__()
    }
    class UOMConversion {
        +from_uom
        +to_uom
        +conversion_factor
        +created_at
        +updated_at
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +unique_together
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +unique_together
    }
    Site --> Meta
    Site --> Meta
    Site --> Meta
    Site --> Meta
    Site --> Meta
    Store --> Meta
    Store --> Meta
    Store --> Meta
    Store --> Meta
    Store --> Meta
    StorePermission --> Meta
    StorePermission --> Meta
    StorePermission --> Meta
    StorePermission --> Meta
    StorePermission --> Meta
    UOM --> Meta
    UOM --> Meta
    UOM --> Meta
    UOM --> Meta
    UOM --> Meta
    UOMConversion --> Meta
    UOMConversion --> Meta
    UOMConversion --> Meta
    UOMConversion --> Meta
    UOMConversion --> Meta
```
