# business_modules.inventory.models.lot

## Imports
- django.db
- django.utils.translation

## Classes
- Lot
  - attr: `product`
  - attr: `name`
  - attr: `quantity`
  - attr: `expiration_date`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__

## Class Diagram

```mermaid
classDiagram
    class Lot {
        +product
        +name
        +quantity
        +expiration_date
        +is_active
        +... (2 more)
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Lot --> Meta
```
