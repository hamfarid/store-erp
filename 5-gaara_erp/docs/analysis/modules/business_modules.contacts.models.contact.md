# business_modules.contacts.models.contact

## Imports
- django.db
- django.utils.translation

## Classes
- Contact
  - attr: `name`
  - attr: `email`
  - attr: `phone`
  - attr: `is_active`
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
    class Contact {
        +name
        +email
        +phone
        +is_active
        +created_at
        +... (1 more)
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    Contact --> Meta
```
