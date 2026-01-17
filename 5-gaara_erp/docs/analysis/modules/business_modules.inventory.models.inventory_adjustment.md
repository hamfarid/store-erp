# business_modules.inventory.models.inventory_adjustment

## Imports
- django.db
- django.utils.translation

## Classes
- InventoryAdjustment
  - attr: `adjustment_type`
  - attr: `quantity`
  - attr: `reason`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`

## Functions
- __str__

## Class Diagram

```mermaid
classDiagram
    class InventoryAdjustment {
        +adjustment_type
        +quantity
        +reason
        +created_at
        +updated_at
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    InventoryAdjustment --> Meta
```
