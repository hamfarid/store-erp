# core_modules.companies.models

## Imports
- django.conf
- django.core.validators
- django.db
- django.utils.translation

## Classes
- Region
  - attr: `name`
  - attr: `code`
  - attr: `description`
  - attr: `is_active`
  - method: `__str__`
- Country
  - attr: `name`
  - attr: `code`
  - attr: `region`
  - attr: `is_active`
  - method: `__str__`
- Company
  - attr: `name`
  - attr: `code`
  - attr: `description`
  - attr: `country`
  - attr: `is_active`
  - attr: `created_by`
  - attr: `updated_by`
  - method: `__str__`
- Branch
  - attr: `name`
  - attr: `code`
  - attr: `company`
  - attr: `is_active`
  - attr: `created_by`
  - attr: `updated_by`
  - method: `__str__`
- Department
  - attr: `name`
  - attr: `code`
  - attr: `company`
  - attr: `description`
  - attr: `is_active`
  - attr: `created_by`
  - attr: `updated_by`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- __str__
- __str__
- __str__
- __str__

## Class Diagram

```mermaid
classDiagram
    class Region {
        +name
        +code
        +description
        +is_active
        +__str__()
    }
    class Country {
        +name
        +code
        +region
        +is_active
        +__str__()
    }
    class Company {
        +name
        +code
        +description
        +country
        +is_active
        +... (2 more)
        +__str__()
    }
    class Branch {
        +name
        +code
        +company
        +is_active
        +created_by
        +... (1 more)
        +__str__()
    }
    class Department {
        +name
        +code
        +company
        +description
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
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Region --> Meta
    Region --> Meta
    Region --> Meta
    Region --> Meta
    Region --> Meta
    Country --> Meta
    Country --> Meta
    Country --> Meta
    Country --> Meta
    Country --> Meta
    Company --> Meta
    Company --> Meta
    Company --> Meta
    Company --> Meta
    Company --> Meta
    Branch --> Meta
    Branch --> Meta
    Branch --> Meta
    Branch --> Meta
    Branch --> Meta
    Department --> Meta
    Department --> Meta
    Department --> Meta
    Department --> Meta
    Department --> Meta
```
