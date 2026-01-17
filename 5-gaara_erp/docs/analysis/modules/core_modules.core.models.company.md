# core_modules.core.models.company

## Imports
- base_models
- country
- django.db
- django.utils.translation

## Classes
- Company
  - attr: `name`
  - attr: `code`
  - attr: `description`
  - attr: `address`
  - attr: `phone`
  - attr: `email`
  - attr: `website`
  - attr: `country`
  - attr: `tax_number`
  - attr: `logo`
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
    class Company {
        +name
        +code
        +description
        +address
        +phone
        +... (6 more)
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Company --> Meta
```
