# core_modules.core.models.department

## Imports
- base_models
- branch
- company
- django.core.exceptions
- django.db
- django.utils.translation

## Classes
- Department
  - attr: `name`
  - attr: `description`
  - attr: `branch`
  - attr: `company`
  - attr: `parent_department`
  - attr: `is_active`
  - method: `__str__`
  - method: `clean`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `unique_together`

## Functions
- __str__
- clean

## Class Diagram

```mermaid
classDiagram
    class Department {
        +name
        +description
        +branch
        +company
        +parent_department
        +... (1 more)
        +__str__()
        +clean()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +unique_together
    }
    Department --> Meta
```
