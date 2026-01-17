# services_modules.admin_affairs.models.position

## Imports
- department
- django.db

## Classes
- Position
  - attr: `title`
  - attr: `code`
  - attr: `department`
  - attr: `description`
  - attr: `is_managerial`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `get_employees_count`
  - method: `is_vacant`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- get_employees_count
- is_vacant

## Class Diagram

```mermaid
classDiagram
    class Position {
        +title
        +code
        +department
        +description
        +is_managerial
        +... (2 more)
        +__str__()
        +get_employees_count()
        +is_vacant()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Position --> Meta
```
