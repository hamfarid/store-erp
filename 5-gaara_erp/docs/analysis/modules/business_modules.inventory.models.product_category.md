# business_modules.inventory.models.product_category

## Imports
- django.db
- django.utils.translation

## Classes
- ProductCategory
  - attr: `name`
  - attr: `description`
  - attr: `parent`
  - attr: `is_active`
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
    class ProductCategory {
        +name
        +description
        +parent
        +is_active
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    ProductCategory --> Meta
```
