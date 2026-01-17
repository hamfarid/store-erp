# core_modules.core.models.country

## Imports
- base_models
- django.db
- django.utils.translation

## Classes
- Country
  - attr: `name`
  - attr: `code`
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
    class Country {
        +name
        +code
        +is_active
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Country --> Meta
```
