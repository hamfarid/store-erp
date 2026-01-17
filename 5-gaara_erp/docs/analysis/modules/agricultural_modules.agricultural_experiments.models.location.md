# agricultural_modules.agricultural_experiments.models.location

## Imports
- django.contrib.auth
- django.db
- django.utils.translation

## Classes
- Location
  - attr: `name`
  - attr: `code`
  - attr: `address`
  - attr: `coordinates`
  - attr: `area`
  - attr: `soil_type`
  - attr: `is_active`
  - attr: `notes`
  - attr: `created_at`
  - attr: `updated_at`
  - attr: `created_by`
  - attr: `updated_by`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class Location {
        +name
        +code
        +address
        +coordinates
        +area
        +... (7 more)
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Location --> Meta
```
