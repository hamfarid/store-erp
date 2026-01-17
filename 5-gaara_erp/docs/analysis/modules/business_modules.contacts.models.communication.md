# business_modules.contacts.models.communication

## Imports
- django.db
- django.utils.translation

## Classes
- Communication
  - attr: `contact_type`
  - attr: `value`
  - attr: `is_primary`
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
    class Communication {
        +contact_type
        +value
        +is_primary
        +created_at
        +updated_at
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    Communication --> Meta
```
